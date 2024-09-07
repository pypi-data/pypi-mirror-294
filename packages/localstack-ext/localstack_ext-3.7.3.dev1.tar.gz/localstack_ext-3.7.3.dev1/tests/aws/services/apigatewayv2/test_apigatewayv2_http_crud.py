import pytest
from botocore.exceptions import ClientError
from localstack.aws.api.lambda_ import Runtime
from localstack.testing.aws.util import is_aws_cloud
from localstack.testing.pytest import markers
from localstack.utils.aws import arns
from localstack.utils.strings import short_uid
from localstack.utils.sync import retry
from tests.aws.services.apigateway.conftest import is_next_gen_api

TEST_LAMBDA_SIMPLE = """
def handler(event, context):
    return {}
"""


@pytest.fixture
def create_dummy_integration(aws_client):
    """This is a dummy integration to be used only to test CRUD operations over the provider."""

    def _create(api_id: str):
        integration = aws_client.apigatewayv2.create_integration(
            ApiId=api_id,
            IntegrationType="HTTP_PROXY",
            IntegrationUri="https://example.com",
            IntegrationMethod="GET",
            PayloadFormatVersion="1.0",
        )
        route = aws_client.apigatewayv2.create_route(
            ApiId=api_id,
            RouteKey="ANY /api",
            Target=f"integrations/{integration['IntegrationId']}",
            AuthorizationType="NONE",
        )
        return integration, route

    return _create


@pytest.mark.skipif(
    not is_next_gen_api() and not is_aws_cloud(), reason="Not implemented in legacy"
)
class TestApigatewayV2HttpDeploymentCrud:
    @pytest.fixture(autouse=True)
    def deployment_transformers(self, snapshot):
        snapshot.add_transformers_list(
            [
                snapshot.transform.key_value("api-id"),
                snapshot.transform.key_value("DeploymentId"),
            ]
        )

    @markers.aws.validated
    def test_get_deployment(self, create_v2_api, aws_client, create_dummy_integration, snapshot):
        apigw_client = aws_client.apigatewayv2
        http_api = create_v2_api(ProtocolType="HTTP")
        api_id = http_api["ApiId"]
        snapshot.match("api-id", api_id)
        create_dummy_integration(api_id)

        response = apigw_client.create_deployment(ApiId=api_id)
        deployment_id = response["DeploymentId"]

        # Get deployments from invalid api
        with pytest.raises(Exception) as e:
            apigw_client.get_deployments(ApiId="invalidId")
        snapshot.match("get-deployments-invalid-api", e.value.response)

        # Get deployment from invalid api
        with pytest.raises(Exception) as e:
            apigw_client.get_deployment(ApiId="invalidId", DeploymentId=deployment_id)
        snapshot.match("get-deployment-invalid-api", e.value.response)

        # Get deployment with invalid deployment
        with pytest.raises(Exception) as e:
            apigw_client.get_deployment(ApiId=api_id, DeploymentId="invalidId")
        snapshot.match("get-deployment-invalid-deployment", e.value.response)

        # Get deployments
        response = apigw_client.get_deployments(ApiId=api_id)
        snapshot.match("get-deployments", response)

        # Get deployment
        response = apigw_client.get_deployment(ApiId=api_id, DeploymentId=deployment_id)
        snapshot.match("get-deployment", response)

    @markers.aws.validated
    def test_create_deployment(self, create_v2_api, aws_client, snapshot, create_dummy_integration):
        apigw_client = aws_client.apigatewayv2
        http_api = create_v2_api(ProtocolType="HTTP")
        api_id = http_api["ApiId"]
        snapshot.match("api-id", api_id)
        create_dummy_integration(api_id)

        apigw_client.create_stage(ApiId=api_id, StageName="stage")
        apigw_client.create_stage(ApiId=api_id, StageName="auto", AutoDeploy=True)

        def _wait_for_auto_deploy():
            _response = apigw_client.get_stage(ApiId=api_id, StageName="auto")
            assert _response.get("DeploymentId")
            return _response

        # On aws there can be a delay for the deployment after creating a auto-deploy stage
        response = retry(_wait_for_auto_deploy)
        snapshot.match("create_auto-stage", response)

        def _sort_stages(stages: list[dict]):
            return sorted(stages, key=lambda stage: stage["StageName"])

        response = apigw_client.get_stages(ApiId=api_id)
        snapshot.match("stages-before-deployments", _sort_stages(response["Items"]))

        with pytest.raises(Exception) as e:
            apigw_client.create_deployment(ApiId="invalidId")
        snapshot.match("create-invalid-api-id", e.value.response)

        # if a stage name is provided, it must be of an existing stage
        with pytest.raises(Exception) as e:
            apigw_client.create_deployment(ApiId=api_id, StageName="stage1")
        snapshot.match("create-with-invalid-stage", e.value.response)

        # A deployment can be created with no stage
        response = apigw_client.create_deployment(ApiId=api_id)
        snapshot.match("create-with-no-stage", response)

        # A deployment with a stage name will attach itself to the stage
        response = apigw_client.create_deployment(ApiId=api_id, StageName="stage")
        snapshot.match("create-with-stage", response)

        response = apigw_client.get_stages(ApiId=api_id)
        snapshot.match("stages-after-named-stage-deployment", _sort_stages(response["Items"]))

        # A deployment to an auto-deploy stage is created, but will return "FAILED"
        response = apigw_client.create_deployment(ApiId=api_id, StageName="auto")
        snapshot.match("create-with-auto-deploy-stage", response)

        response = apigw_client.get_stages(ApiId=api_id)
        snapshot.match("get-stages-after", _sort_stages(response["Items"]))

    @markers.aws.validated
    def test_update_deployment(self, create_v2_api, aws_client, snapshot, create_dummy_integration):
        apigw_client = aws_client.apigatewayv2
        http_api = create_v2_api(ProtocolType="HTTP")
        api_id = http_api["ApiId"]
        snapshot.match("api-id", api_id)
        create_dummy_integration(api_id)

        apigw_client.create_stage(ApiId=api_id, StageName="stage")

        response = apigw_client.create_deployment(ApiId=api_id)
        snapshot.match("create-with-no-stage", response)
        deployment_id = response["DeploymentId"]

        # Attempt update with invalid api_id
        with pytest.raises(Exception) as e:
            apigw_client.update_deployment(
                ApiId="invalidID", DeploymentId=deployment_id, Description="invalid description"
            )
        snapshot.match("update-with-invalid-api", e.value.response)

        # Attempt update with invalid deployment id
        with pytest.raises(Exception) as e:
            apigw_client.update_deployment(
                ApiId=api_id, DeploymentId="invalidID", Description="invalid description"
            )
        snapshot.match("update-with-invalid-deployment", e.value.response)

        # Update without description
        response = apigw_client.update_deployment(ApiId=api_id, DeploymentId=deployment_id)
        snapshot.match("update-with-no-description", response)

        # Update the deployment description
        response = apigw_client.update_deployment(
            ApiId=api_id, DeploymentId=deployment_id, Description="description"
        )
        snapshot.match("update-deployment-with-description", response)

        # Update override description
        response = apigw_client.update_deployment(ApiId=api_id, DeploymentId=deployment_id)
        snapshot.match("update-override-description", response)

    @markers.aws.validated
    def test_delete_deployment(self, create_v2_api, aws_client, snapshot, create_dummy_integration):
        apigw_client = aws_client.apigatewayv2
        http_api = create_v2_api(ProtocolType="HTTP")
        api_id = http_api["ApiId"]
        snapshot.match("api-id", api_id)
        create_dummy_integration(api_id)

        apigw_client.create_stage(ApiId=api_id, StageName="stage")

        response = apigw_client.create_deployment(ApiId=api_id, StageName="stage")
        snapshot.match("create-deployment", response)
        deployment_id = response["DeploymentId"]

        # Attempt to delete from an invalid api id
        with pytest.raises(Exception) as e:
            apigw_client.delete_deployment(ApiId="invalidID", DeploymentId=deployment_id)
        snapshot.match("delete-invalid-api-id", e.value.response)

        # Attempt to delete an invalid deployment
        with pytest.raises(Exception) as e:
            apigw_client.delete_deployment(ApiId=api_id, DeploymentId="invalidID")
        snapshot.match("delete-invalid-deployment-id", e.value.response)

        # Attempt to delete while attach to a stage
        with pytest.raises(Exception) as e:
            apigw_client.delete_deployment(ApiId=api_id, DeploymentId=deployment_id)
        snapshot.match("delete-with-stage-still-pointing", e.value.response)

        apigw_client.delete_stage(ApiId=api_id, StageName="stage")

        # Successful delete
        response = apigw_client.delete_deployment(ApiId=api_id, DeploymentId=deployment_id)
        snapshot.match("delete-deployment", response)


@pytest.mark.skipif(
    not is_next_gen_api() and not is_aws_cloud(), reason="Not implemented in legacy"
)
class TestApigatewayV2HttpStageCrud:
    @pytest.fixture(autouse=True)
    def deployment_transformers(self, snapshot):
        snapshot.add_transformers_list(
            [
                snapshot.transform.key_value("api-id"),
                snapshot.transform.key_value("DeploymentId"),
            ]
        )

    @markers.aws.validated
    def test_get_stage(self, create_v2_api, aws_client, snapshot, create_dummy_integration):
        apigw_client = aws_client.apigatewayv2
        http_api = create_v2_api(ProtocolType="HTTP")
        api_id = http_api["ApiId"]
        snapshot.match("api-id", api_id)
        create_dummy_integration(api_id)
        apigw_client.create_stage(ApiId=api_id, StageName="stage")

        # Attempt get stages invalid api id
        with pytest.raises(Exception) as e:
            apigw_client.get_stages(ApiId="invalidID")
        snapshot.match("get-stages-invalid-api", e.value.response)

        # Attempt get stage invalid api id
        with pytest.raises(Exception) as e:
            apigw_client.get_stage(ApiId="invalidID", StageName="stage")
        snapshot.match("get-stage-invalid-api", e.value.response)

        # Attempt get stage invalid stage name
        with pytest.raises(Exception) as e:
            apigw_client.get_stage(ApiId=api_id, StageName="invalid")
        snapshot.match("get-stage-invalid-stage-name", e.value.response)

        # Successful get stages
        response = apigw_client.get_stages(ApiId=api_id)
        snapshot.match("get-stages", response)

        # Successful get stage
        response = apigw_client.get_stage(ApiId=api_id, StageName="stage")
        snapshot.match("get-stage", response)

    @markers.aws.validated
    def test_create_stage(self, create_v2_api, aws_client, snapshot, create_dummy_integration):
        apigw_client = aws_client.apigatewayv2
        http_api = create_v2_api(ProtocolType="HTTP")
        api_id = http_api["ApiId"]
        snapshot.match("api-id", api_id)
        integration, _ = create_dummy_integration(api_id)

        def _wait_for_auto_deploy(previous_deploy_id: str = ""):
            _response = apigw_client.get_stage(ApiId=api_id, StageName="auto")
            assert _response.get("DeploymentId") and _response["DeploymentId"] != previous_deploy_id
            return _response

        # Attempt to create stage with invalid api
        with pytest.raises(Exception) as e:
            apigw_client.create_stage(ApiId="invalid", StageName="stage")
        snapshot.match("create-stage-invalid-api", e.value.response)

        # Attempt to create stage with no stage name
        with pytest.raises(Exception) as e:
            apigw_client.create_stage(ApiId=api_id, StageName="")
        snapshot.match("create-stage-empty-string", e.value.response)

        # Attempt to create stage with /
        with pytest.raises(Exception) as e:
            apigw_client.create_stage(ApiId=api_id, StageName="stage/name")
        snapshot.match("create-stage-with-forward-slashes", e.value.response)

        # Attempt to create stage with $
        with pytest.raises(Exception) as e:
            apigw_client.create_stage(ApiId=api_id, StageName="$stage")
        snapshot.match("create-stage-with-special-char", e.value.response)

        # Successful stage creation
        response = apigw_client.create_stage(ApiId=api_id, StageName="stage")
        snapshot.match("create-stage", response)

        # attempt to create stage with same name
        with pytest.raises(Exception) as e:
            apigw_client.create_stage(ApiId=api_id, StageName="stage")
        snapshot.match("create-stage-with-same-name", e.value.response)

        # create $default stage
        response = apigw_client.create_stage(ApiId=api_id, StageName="$default")
        snapshot.match("create-default-stage", response)

        # create stage auto deploy
        response = apigw_client.create_stage(ApiId=api_id, StageName="auto", AutoDeploy=True)
        snapshot.match("create-stage-auto", response)
        # On aws there can be a delay for the deployment after creating an auto-deploy stage
        response = retry(_wait_for_auto_deploy)
        snapshot.match("get-stage-auto", response)
        auto_deploy_id = response["DeploymentId"]

        # create Stage from existing deployment
        response = apigw_client.create_stage(
            ApiId=api_id, StageName="from-existing", DeploymentId=auto_deploy_id
        )
        snapshot.match("create-stage-from-existing", response)

        # adding a route will trigger a deployment
        apigw_client.create_route(
            ApiId=api_id,
            RouteKey="ANY /new",
            Target=f"integrations/{integration['IntegrationId']}",
            AuthorizationType="NONE",
        )
        response = retry(lambda: _wait_for_auto_deploy(auto_deploy_id))
        snapshot.match("auto-deploy-stage", response)

    @markers.aws.validated
    def test_update_stage(self, create_v2_api, aws_client, snapshot, create_dummy_integration):
        apigw_client = aws_client.apigatewayv2
        http_api = create_v2_api(ProtocolType="HTTP")
        api_id = http_api["ApiId"]
        snapshot.match("api-id", api_id)
        create_dummy_integration(api_id)
        apigw_client.create_stage(ApiId=api_id, StageName="stage")

        # attempt to update stage with invalid api id
        with pytest.raises(Exception) as e:
            apigw_client.update_stage(
                ApiId="invalidId", StageName="stage", Description="description"
            )
        snapshot.match("update-with-invalid-api", e.value.response)

        # attempt to update stage with invalid stage name
        with pytest.raises(Exception) as e:
            apigw_client.update_stage(ApiId=api_id, StageName="invalid", Description="description")
        snapshot.match("update-with-invalid-stage-name", e.value.response)

        # Update stage description
        response = apigw_client.update_stage(
            ApiId=api_id, StageName="stage", Description="description"
        )
        snapshot.match("update-stage", response)

        # update stage deployment
        deployment_id = apigw_client.create_deployment(ApiId=api_id)["DeploymentId"]
        response = apigw_client.update_stage(
            ApiId=api_id, StageName="stage", DeploymentId=deployment_id
        )
        snapshot.match("update-stage-deployment", response)

        # Attempt to update to auto deploy and set deployment id
        with pytest.raises(Exception) as e:
            apigw_client.update_stage(
                ApiId=api_id, StageName="stage", AutoDeploy=True, DeploymentId=deployment_id
            )
        snapshot.match("update-auto-deploy-and-deployment-id", e.value.response)

        # Assert that the change to autodeploy was not applied
        response = apigw_client.get_stage(ApiId=api_id, StageName="stage")
        snapshot.match("get-stage-after-auto-deploy-update-fail", response)

        # update stage to auto deploy
        response = apigw_client.update_stage(ApiId=api_id, StageName="stage", AutoDeploy=True)
        snapshot.match("update-stage-auto", response)

        # Attempt to update deployment of auto deploy stage
        with pytest.raises(Exception) as e:
            apigw_client.update_stage(ApiId=api_id, StageName="stage", DeploymentId=deployment_id)
        snapshot.match("update-stage-deployment-auto-deploy", e.value.response)

    @markers.aws.validated
    def test_delete_stage(self, create_v2_api, aws_client, snapshot, create_dummy_integration):
        apigw_client = aws_client.apigatewayv2
        http_api = create_v2_api(ProtocolType="HTTP")
        api_id = http_api["ApiId"]
        snapshot.match("api-id", api_id)
        create_dummy_integration(api_id)
        apigw_client.create_stage(ApiId=api_id, StageName="stage")

        # Attempt to delete stage with invalid api id
        with pytest.raises(Exception) as e:
            apigw_client.delete_stage(ApiId="invalidId", StageName="stage")
        snapshot.match("delete-stage-invalid-api", e.value.response)

        # attempt to delete stage with invalid name
        with pytest.raises(Exception) as e:
            apigw_client.delete_stage(ApiId=api_id, StageName="invalid")
        snapshot.match("delete-stage-invalid-name", e.value.response)

        # Successful delete
        response = apigw_client.delete_stage(ApiId=api_id, StageName="stage")
        snapshot.match("delete-stage", response)

    @markers.aws.validated
    def test_auto_deploy_stage_http(
        self,
        create_v2_api,
        aws_client,
        create_lambda_function,
        region_name,
        snapshot,
    ):
        apigw_client = aws_client.apigatewayv2

        http_api = create_v2_api(ProtocolType="HTTP", Target="https://httpbin.org/anything")
        api_id = http_api["ApiId"]

        previous_deploy_id = ""

        retries = 5 if is_aws_cloud() else 1
        sleep = 1 if is_aws_cloud() else 0.5

        def _wait_for_auto_deploy():
            _response = apigw_client.get_stage(ApiId=api_id, StageName="$default")
            assert _response.get("DeploymentId") and _response["DeploymentId"] != previous_deploy_id
            return _response

        # Original deployment
        response = retry(_wait_for_auto_deploy, retries=retries, sleep=sleep)
        previous_deploy_id = response["DeploymentId"]

        # Creating a different api doesn't trigger
        create_v2_api(ProtocolType="HTTP")
        with pytest.raises(Exception):
            retry(_wait_for_auto_deploy, retries=retries, sleep=sleep)

        # update api triggers
        apigw_client.update_api(ApiId=api_id, CorsConfiguration={"AllowCredentials": True})
        response = retry(_wait_for_auto_deploy, retries=retries, sleep=sleep)
        previous_deploy_id = response["DeploymentId"]

        # Create integration doesn't trigger
        integration = aws_client.apigatewayv2.create_integration(
            ApiId=api_id,
            IntegrationType="HTTP_PROXY",
            IntegrationUri="https://httpbin.org/anything",
            IntegrationMethod="GET",
            PayloadFormatVersion="1.0",
        )
        with pytest.raises(Exception):
            retry(_wait_for_auto_deploy, retries=retries, sleep=sleep)

        # Creating a route triggers
        route = apigw_client.create_route(
            ApiId=api_id,
            RouteKey="ANY /api",
            Target=f"integrations/{integration['IntegrationId']}",
            AuthorizationType="NONE",
        )
        response = retry(_wait_for_auto_deploy, retries=retries, sleep=sleep)
        previous_deploy_id = response["DeploymentId"]

        # Updating a route triggers
        apigw_client.update_route(ApiId=api_id, RouteId=route["RouteId"], AuthorizationType="NONE")
        response = retry(_wait_for_auto_deploy, retries=retries, sleep=sleep)
        previous_deploy_id = response["DeploymentId"]

        # Updating an integration triggers
        apigw_client.update_integration(
            ApiId=api_id, IntegrationId=integration["IntegrationId"], PassthroughBehavior="NEVER"
        )
        response = retry(_wait_for_auto_deploy, retries=retries, sleep=sleep)
        previous_deploy_id = response["DeploymentId"]

        # Deleting a route triggers
        apigw_client.delete_route(ApiId=api_id, RouteId=route["RouteId"])
        response = retry(_wait_for_auto_deploy, retries=retries, sleep=sleep)
        previous_deploy_id = response["DeploymentId"]

        # deleting an integration doesn't trigger
        apigw_client.delete_integration(ApiId=api_id, IntegrationId=integration["IntegrationId"])
        with pytest.raises(Exception):
            retry(_wait_for_auto_deploy, retries=retries, sleep=sleep)

        # creates a lambda authorizer
        lambda_name = f"int-{short_uid()}"
        lambda_arn = create_lambda_function(
            handler_file=TEST_LAMBDA_SIMPLE,
            func_name=lambda_name,
            runtime=Runtime.python3_12,
        )["CreateFunctionResponse"]["FunctionArn"]
        auth_url = arns.apigateway_invocations_arn(lambda_arn, region_name)

        # creating an authorizer doesn't trigger
        authorizer = apigw_client.create_authorizer(
            ApiId=api_id,
            Name="test-authorizer",
            AuthorizerUri=auth_url,
            AuthorizerType="REQUEST",
            IdentitySource=["$request.header.Authorization"],
            AuthorizerPayloadFormatVersion="2.0",
        )
        with pytest.raises(Exception):
            retry(_wait_for_auto_deploy, retries=retries, sleep=sleep)

        # updating an authorizer triggers (even if not attached)
        apigw_client.update_authorizer(
            ApiId=api_id, AuthorizerId=authorizer["AuthorizerId"], AuthorizerUri=auth_url
        )
        response = retry(_wait_for_auto_deploy, retries=retries, sleep=sleep)
        previous_deploy_id = response["DeploymentId"]

        deployments = apigw_client.get_deployments(ApiId=api_id)
        snapshot.match("get-deployments", deployments)


class TestApigatewayV2HttpIntegrationCrud:
    # TODO add the ConnectionType to create_integration
    @pytest.mark.skipif(
        not is_next_gen_api() and not is_aws_cloud(), reason="Not implemented in legacy"
    )
    @markers.snapshot.skip_snapshot_verify(paths=["$..ConnectionType"])
    @markers.aws.validated
    def test_request_parameters_headers(self, create_v2_api, aws_client, snapshot):
        apigw_client = aws_client.apigatewayv2

        snapshot.add_transformers_list([snapshot.transform.key_value("IntegrationId")])

        http_api = create_v2_api(ProtocolType="HTTP")
        api_id = http_api["ApiId"]

        create_integration_kwargs = {
            "ApiId": api_id,
            "IntegrationType": "HTTP_PROXY",
            "IntegrationUri": "https://example.com",
            "IntegrationMethod": "GET",
            "PayloadFormatVersion": "1.0",
            "RequestParameters": {"append:header.header_value": "$request.headers.foo"},
        }

        # "$request.headers.foo" will be rejected
        with pytest.raises(Exception) as e:
            apigw_client.create_integration(**create_integration_kwargs)
        snapshot.match("create-invalid-mapping", e.value.response)

        # Can't do twice the same headers
        create_integration_kwargs["RequestParameters"] = {
            "append:header.header_1": "static value",
            "overwrite:header.header_1": "static value",
        }
        with pytest.raises(Exception) as e:
            apigw_client.create_integration(**create_integration_kwargs)
        snapshot.match("create-duplicate-headers", e.value.response)

        # Uniqueness is case insensitive
        create_integration_kwargs["RequestParameters"] = {
            "append:header.header_1": "static value",
            "overwrite:header.HEADER_1": "static value",
        }
        with pytest.raises(Exception) as e:
            apigw_client.create_integration(**create_integration_kwargs)
        snapshot.match("create-duplicate-headers-case-insensitive", e.value.response)

        # An empty mapping will be ignored on create
        create_integration_kwargs["RequestParameters"] = {"append:header.header_1": ""}
        response = apigw_client.create_integration(**create_integration_kwargs)
        snapshot.match("create-with-no-mapping", response)

        # create with all actions
        create_integration_kwargs["RequestParameters"] = {
            "append:header.header_append": "static value",
            "overwrite:header.header_overwrite": "$request.header.foo",
            "remove:header.header_remove": "''",
        }
        integration = apigw_client.create_integration(**create_integration_kwargs)
        snapshot.match("create-with-all-actions", integration)

        # passing the same header with an empty string will delete request parameter
        update_integration_kwargs = {
            "ApiId": api_id,
            "IntegrationId": integration["IntegrationId"],
            "RequestParameters": {
                "remove:header.header_remove": "",
            },
        }
        response = apigw_client.update_integration(**update_integration_kwargs)
        snapshot.match("update-delete-parameter-mapping", response)

        # A remove header must have single quotes
        update_integration_kwargs["RequestParameters"] = {"remove:header.header_remove": '""'}
        with pytest.raises(Exception) as e:
            apigw_client.update_integration(**update_integration_kwargs)
        snapshot.match("remove-needs-single-quotes", e.value.response)

        # Sending a parameter that exists with the same action but different casing will fail
        update_integration_kwargs["RequestParameters"] = {
            "append:header.header_appenD": "static value"
        }
        with pytest.raises(Exception) as e:
            apigw_client.update_integration(**update_integration_kwargs)
        snapshot.match("update-with-different-casing", e.value.response)

        # Sending a parameter with the same casing but different action will fail
        update_integration_kwargs["RequestParameters"] = {
            "overwrite:header.header_append": "static value"
        }
        with pytest.raises(Exception) as e:
            apigw_client.update_integration(**update_integration_kwargs)
        snapshot.match("update-with-different-action-will-fail", e.value.response)

        # Sending with same casing and same action create_integration()replace
        update_integration_kwargs["RequestParameters"] = {
            "append:header.header_append": "${request.header.foo}"
        }
        response = apigw_client.update_integration(**update_integration_kwargs)
        snapshot.match("update-with-same-casing-and-action", response)

        # Missing param_name
        update_integration_kwargs["RequestParameters"] = {"append:header": "static value"}
        with pytest.raises(Exception) as e:
            apigw_client.update_integration(**update_integration_kwargs)
        snapshot.match("missing-param-name", e.value.response)

        # sending multi headers
        update_integration_kwargs["RequestParameters"] = {
            "append:header.multi_header.1": "$request.header.foo",
            "append:header.multi_header.2": "static value",
            "overwrite:header.multi_header.3": "static value",
            "remove:header.multi_header.4": "''",
        }
        response = apigw_client.update_integration(**update_integration_kwargs)
        snapshot.match("update-with-multivalue", response)

        # sending complex value
        update_integration_kwargs["RequestParameters"] = {
            "append:header.append_header": "${request.body}followed with text$request.path",
        }
        response = apigw_client.update_integration(**update_integration_kwargs)
        snapshot.match("update-with-multiple-param", response)

        # missing closing curly braces
        update_integration_kwargs["RequestParameters"] = {
            "append:header.append_header": "${request.body",
        }
        with pytest.raises(Exception) as e:
            apigw_client.update_integration(**update_integration_kwargs)
        snapshot.match("update-missing-curly", e.value.response)

        # update with extra closing curly
        update_integration_kwargs["RequestParameters"] = {
            "append:header.append_header": "$request.body}",
        }
        with pytest.raises(Exception) as e:
            apigw_client.update_integration(**update_integration_kwargs)
        snapshot.match("update-extra-curly", e.value.response)

        # destinations are case-insensitive
        update_integration_kwargs["RequestParameters"] = {
            "append:HEADER.DestinatioN": "But they will be useless",
        }
        response = apigw_client.update_integration(**update_integration_kwargs)
        snapshot.match("update-case-sensitive", response)

        # Multiple errors
        update_integration_kwargs["RequestParameters"] = {
            "append:header.first": "valid",
            "append:header.First": "$invalid",
        }
        with pytest.raises(Exception) as e:
            apigw_client.update_integration(**update_integration_kwargs)
        snapshot.match("multiple-errors", e.value.response)

        # Reserved header
        update_integration_kwargs["RequestParameters"] = {"append:header.authorization": "illegal"}
        with pytest.raises(Exception) as e:
            apigw_client.update_integration(**update_integration_kwargs)
        snapshot.match("reserved-header", e.value.response)

        # Reserved header prefix
        update_integration_kwargs["RequestParameters"] = {
            "append:header.apigw-any-suffix": "illegal"
        }
        with pytest.raises(Exception) as e:
            apigw_client.update_integration(**update_integration_kwargs)
        snapshot.match("reserved-header-prefix", e.value.response)

        # Reserved header multiple errors
        update_integration_kwargs["RequestParameters"] = {"append:header.authorization": "$illegal"}
        with pytest.raises(Exception) as e:
            apigw_client.update_integration(**update_integration_kwargs)
        snapshot.match("reserved-header-multiple-errors", e.value.response)

        # A second $ in the value will start a new source
        update_integration_kwargs["RequestParameters"] = {"append:header.foo": "$request.path$"}
        response = apigw_client.update_integration(**update_integration_kwargs)
        snapshot.match("with-static-sign", response)

        # A source with $ with length 2 or less will become a static value
        update_integration_kwargs["RequestParameters"] = {"append:header.foo": "$a"}
        response = apigw_client.update_integration(**update_integration_kwargs)
        snapshot.match("with-sign-become-static", response)

        # A source with $ with length more than 2 will need to be valid
        update_integration_kwargs["RequestParameters"] = {"append:header.foo": "$aa"}
        with pytest.raises(Exception) as e:
            apigw_client.update_integration(**update_integration_kwargs)
        snapshot.match("sign-with-length-over-2", e.value.response)

        # any { in static value will fail
        update_integration_kwargs["RequestParameters"] = {"append:header.foo": "{"}
        with pytest.raises(Exception) as e:
            apigw_client.update_integration(**update_integration_kwargs)
        snapshot.match("open-curly", e.value.response)

        # any } in static value will fail
        update_integration_kwargs["RequestParameters"] = {"append:header.foo": "}"}
        with pytest.raises(Exception) as e:
            apigw_client.update_integration(**update_integration_kwargs)
        snapshot.match("close-curly", e.value.response)

        # any { in dynamic will fail
        update_integration_kwargs["RequestParameters"] = {
            "append:header.foo": "$request.header.foo{"
        }
        with pytest.raises(Exception) as e:
            apigw_client.update_integration(**update_integration_kwargs)
        snapshot.match("open-curly-in-dynamic", e.value.response)

        # any } in dynamic value will fail
        update_integration_kwargs["RequestParameters"] = {
            "append:header.foo": "$request.header.foo}"
        }
        with pytest.raises(Exception) as e:
            apigw_client.update_integration(**update_integration_kwargs)
        snapshot.match("close-curly-in-dynamic", e.value.response)

        # A { inside a ${} block is ok
        update_integration_kwargs["RequestParameters"] = {
            "append:header.foo": "${request.header.foo{}"
        }
        response = apigw_client.update_integration(**update_integration_kwargs)
        snapshot.match("open-curly-in-block", response)

        # any } in ${} value will fail as it will be seen as a `}` static value
        update_integration_kwargs["RequestParameters"] = {
            "append:header.foo": "${request.header.foo}}"
        }
        with pytest.raises(Exception) as e:
            apigw_client.update_integration(**update_integration_kwargs)
        snapshot.match("close-curly-in-block", e.value.response)

        # A $ at the end of a block isn't matched as there are no valid char after it
        update_integration_kwargs["RequestParameters"] = {
            "append:header.foo": "${request.header.foo$request.header.foo$}"
        }
        response = apigw_client.update_integration(**update_integration_kwargs)
        snapshot.match("greedy-block-match", response)

        # parameter name must match regex
        update_integration_kwargs["RequestParameters"] = {"append:header.foo%": ""}
        with pytest.raises(Exception) as e:
            apigw_client.update_integration(**update_integration_kwargs)
        snapshot.match("illegal-char-in-param-name", e.value.response)

    @pytest.mark.skipif(
        not is_next_gen_api() and not is_aws_cloud(), reason="Not implemented in legacy"
    )
    @markers.snapshot.skip_snapshot_verify(
        paths=[
            # TODO add the ConnectionType to create_integration
            "$..ConnectionType",
            # AWS adds an extra `.`
            "$.append-not-allowed..Message",
            "$.remove-not-allowed..Message",
        ]
    )
    @markers.aws.validated
    def test_request_parameters_path(self, create_v2_api, aws_client, snapshot):
        apigw_client = aws_client.apigatewayv2

        snapshot.add_transformers_list([snapshot.transform.key_value("IntegrationId")])

        http_api = create_v2_api(ProtocolType="HTTP")
        api_id = http_api["ApiId"]

        create_integration_kwargs = {
            "ApiId": api_id,
            "IntegrationType": "HTTP_PROXY",
            "IntegrationUri": "https://example.com",
            "IntegrationMethod": "GET",
            "PayloadFormatVersion": "1.0",
            "RequestParameters": {"overwrite:path": "$request.header.foo"},
        }
        integration = apigw_client.create_integration(**create_integration_kwargs)
        snapshot.match("create-with-path-override", integration)

        update_integration_kwargs = {
            "ApiId": api_id,
            "IntegrationId": integration["IntegrationId"],
            "RequestParameters": {
                "overwrite:path": "",
            },
        }

        # removing path parameter
        response = apigw_client.update_integration(**update_integration_kwargs)
        snapshot.match("remove-with-path-override", response)

        # path is case-insensitive
        update_integration_kwargs["RequestParameters"] = {
            "overwrite:Path": "$request.header.foo",
        }
        response = apigw_client.update_integration(**update_integration_kwargs)
        snapshot.match("update-case-sensitive", response)

        # append not allowed
        update_integration_kwargs["RequestParameters"] = {
            "append:path": "$request.header.foo",
        }
        with pytest.raises(Exception) as e:
            apigw_client.update_integration(**update_integration_kwargs)
        snapshot.match("append-not-allowed", e.value.response)

        # remove not allowed
        update_integration_kwargs["RequestParameters"] = {"remove:path": "''"}
        with pytest.raises(Exception) as e:
            apigw_client.update_integration(**update_integration_kwargs)
        snapshot.match("remove-not-allowed", e.value.response)

    @pytest.mark.skipif(
        not is_next_gen_api() and not is_aws_cloud(), reason="Not implemented in legacy"
    )
    @markers.snapshot.skip_snapshot_verify(
        # TODO add the ConnectionType to create_integration
        paths=["$..ConnectionType"]
    )
    @markers.aws.validated
    def test_response_parameters(self, create_v2_api, aws_client, snapshot):
        apigw_client = aws_client.apigatewayv2

        snapshot.add_transformers_list([snapshot.transform.key_value("IntegrationId")])

        http_api = create_v2_api(ProtocolType="HTTP")
        api_id = http_api["ApiId"]

        create_integration_kwargs = {
            "ApiId": api_id,
            "IntegrationType": "HTTP_PROXY",
            "IntegrationUri": "https://example.com",
            "IntegrationMethod": "GET",
            "PayloadFormatVersion": "1.0",
            "ResponseParameters": {"200": {"overwrite:header.header": "$response.header.foo"}},
        }

        integration = apigw_client.create_integration(**create_integration_kwargs)
        snapshot.match("create-with-header-override", integration)

        # remove parameter mapping with empty block
        update_integration_kwargs = {
            "ApiId": api_id,
            "IntegrationId": integration["IntegrationId"],
            "ResponseParameters": {"200": {}},
        }
        response = apigw_client.update_integration(**update_integration_kwargs)
        snapshot.match("update-remove-integration-response", response)

        # response under 200
        update_integration_kwargs["ResponseParameters"] = {
            "199": {"overwrite:header.header": "$response.header.foo"}
        }
        with pytest.raises(Exception) as e:
            apigw_client.update_integration(**update_integration_kwargs)
        snapshot.match("response-under-200", e.value.response)

        # response over 599
        update_integration_kwargs["ResponseParameters"] = {
            "600": {"overwrite:header.header": "$response.header.foo"}
        }
        with pytest.raises(Exception) as e:
            apigw_client.update_integration(**update_integration_kwargs)
        snapshot.match("response-over-599", e.value.response)

        # response not int
        update_integration_kwargs["ResponseParameters"] = {
            "200 ": {"overwrite:header.header": "$response.header.foo"}
        }
        with pytest.raises(Exception) as e:
            apigw_client.update_integration(**update_integration_kwargs)
        snapshot.match("response-not-int", e.value.response)

    @pytest.mark.skipif(
        not is_next_gen_api() and not is_aws_cloud(), reason="Not implemented in legacy"
    )
    @markers.snapshot.skip_snapshot_verify(
        # TODO add the ConnectionType to create_integration
        paths=["$..ConnectionType"]
    )
    @markers.aws.validated
    def test_response_parameters_statuscode(self, create_v2_api, aws_client, snapshot):
        apigw_client = aws_client.apigatewayv2

        snapshot.add_transformers_list([snapshot.transform.key_value("IntegrationId")])

        http_api = create_v2_api(ProtocolType="HTTP")
        api_id = http_api["ApiId"]

        create_integration_kwargs = {
            "ApiId": api_id,
            "IntegrationType": "HTTP_PROXY",
            "IntegrationUri": "https://example.com",
            "IntegrationMethod": "GET",
            "PayloadFormatVersion": "1.0",
            "ResponseParameters": {"200": {"overwrite:statuscode": "$response.header.foo"}},
        }

        integration = apigw_client.create_integration(**create_integration_kwargs)
        snapshot.match("create-with-statuscode-override", integration)

        # update with invalid mapping
        update_integration_kwargs = {
            "ApiId": api_id,
            "IntegrationId": integration["IntegrationId"],
            "ResponseParameters": {"200": {"overwrite:statuscode": "$resp.header.foo"}},
        }
        with pytest.raises(Exception) as e:
            apigw_client.update_integration(**update_integration_kwargs)
        snapshot.match("invalid-mapping", e.value.response)

        # update with static source
        update_integration_kwargs["ResponseParameters"] = {"200": {"overwrite:statuscode": "201"}}
        response = apigw_client.update_integration(**update_integration_kwargs)
        snapshot.match("update-static-code", response)

        # update with static under 100
        update_integration_kwargs["ResponseParameters"] = {"200": {"overwrite:statuscode": "99"}}
        with pytest.raises(Exception) as e:
            apigw_client.update_integration(**update_integration_kwargs)
        snapshot.match("update-static-below-100", e.value.response)

        # update with static 600 and above
        update_integration_kwargs["ResponseParameters"] = {"200": {"overwrite:statuscode": "600"}}
        with pytest.raises(Exception) as e:
            apigw_client.update_integration(**update_integration_kwargs)
        snapshot.match("update-static-above-600", e.value.response)

        # update with static source non int
        update_integration_kwargs["ResponseParameters"] = {"200": {"overwrite:statuscode": "20.1"}}
        with pytest.raises(Exception) as e:
            apigw_client.update_integration(**update_integration_kwargs)
        snapshot.match("update-static-code-non-int", e.value.response)

        # when a response is empty, it gets removed from the integration
        update_integration_kwargs["ResponseParameters"] = {"200": {"overwrite:statuscode": ""}}
        response = apigw_client.update_integration(**update_integration_kwargs)
        snapshot.match("update-with-empty-will-remove", response)

        # update with append
        update_integration_kwargs["ResponseParameters"] = {"200": {"append:statuscode": "201"}}
        with pytest.raises(Exception) as e:
            apigw_client.update_integration(**update_integration_kwargs)
        snapshot.match("update-with-append", e.value.response)

        # If multiple configuration are passed, all must be valid
        update_integration_kwargs["ResponseParameters"] = {
            "200": {"overwrite:statuscode": "201"},
            "201": {"append:statuscode": "201"},
        }
        with pytest.raises(Exception) as e:
            apigw_client.update_integration(**update_integration_kwargs)
        snapshot.match("update-not-all-valid", e.value.response)
        response = apigw_client.get_integration(
            ApiId=api_id, IntegrationId=integration["IntegrationId"]
        )
        snapshot.match("get-integration-after-invalid-update", response)

    @markers.aws.validated
    def test_http_integration_invalid_use_cases(self, aws_client, create_v2_api, snapshot):
        """
        This is just a bunch of negative tests to our HTTP integration.
        """
        result = create_v2_api(ProtocolType="HTTP", Name=f"{short_uid()}")
        api_id = result["ApiId"]

        with pytest.raises(ClientError) as e:
            aws_client.apigatewayv2.create_integration(
                ApiId=api_id,
                IntegrationType="HTTP_PROXY",
                IntegrationMethod="ANY",
                IntegrationUri="http://example.com",
            )
        snapshot.match("invalid-integration-req-no-payload", e.value.response)

        with pytest.raises(ClientError) as e:
            aws_client.apigatewayv2.create_integration(
                ApiId=api_id,
                IntegrationType="HTTP",  # HTTP v2 only supports HTTP_PROXY or AWS_PROXY
                PayloadFormatVersion="1.0",
                IntegrationMethod="ANY",
                IntegrationUri="http://example.com",
            )
        snapshot.match("invalid-integration-type", e.value.response)

        with pytest.raises(ClientError) as e:
            aws_client.apigatewayv2.create_integration(
                ApiId=api_id,
                IntegrationType="HTTP_PROXY",
                PayloadFormatVersion="2.0",  # HTTP v2 only supports 1.0
                IntegrationMethod="ANY",
                IntegrationUri="http://example.com",
            )
        snapshot.match("invalid-payload-format-version", e.value.response)

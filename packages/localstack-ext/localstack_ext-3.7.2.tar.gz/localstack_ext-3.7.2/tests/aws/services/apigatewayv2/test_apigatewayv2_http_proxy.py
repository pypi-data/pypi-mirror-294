import base64
import json

import pytest
import requests
from localstack.testing.aws.util import is_aws_cloud
from localstack.testing.pytest import markers
from localstack.utils.strings import short_uid
from localstack.utils.sync import retry
from tests.aws.services.apigateway.apigateway_fixtures import api_invoke_url
from tests.aws.services.apigateway.conftest import is_next_gen_api


@pytest.fixture
def apigwv2_httpbin_headers_transformers(snapshot):
    snapshot.add_transformers_list(
        [
            # as APIGW has multiple servers, the origin IP address varies between requests
            snapshot.transform.key_value("origin", "<origin>", reference_replacement=False),
            snapshot.transform.key_value("Forwarded", "<forwarded>", reference_replacement=False),
            snapshot.transform.jsonpath("$..headers.X-Amzn-Trace-Id", "trace-id"),
            snapshot.transform.jsonpath("$..headers.Host", "host"),
        ]
    )


class TestHttpApiHttpProxyIntegration:
    @markers.snapshot.skip_snapshot_verify(
        condition=lambda: not is_next_gen_api(),
        paths=[
            "$..headers.X-Amzn-Trace-Id",
            "$..headers.X-Localstack-Edge",
        ],
    )
    @markers.aws.validated
    def test_http_proxy_integration(
        self,
        aws_client,
        create_v2_api,
        apigw_echo_http_server_anything,
        snapshot,
        apigwv2_httpbin_headers_transformers,
    ):
        result = create_v2_api(ProtocolType="HTTP", Name=f"{short_uid()}")
        api_id = result["ApiId"]

        uri = apigw_echo_http_server_anything

        integration = aws_client.apigatewayv2.create_integration(
            ApiId=api_id,
            IntegrationType="HTTP_PROXY",
            PayloadFormatVersion="1.0",
            IntegrationMethod="ANY",
            IntegrationUri=uri,
        )
        integration_id = integration["IntegrationId"]

        # creates the /{proxy+} route
        aws_client.apigatewayv2.create_route(
            ApiId=api_id,
            RouteKey="ANY /api/{proxy+}",
            Target=f"integrations/{integration_id}",
            AuthorizationType="NONE",
        )

        # create the /api route
        aws_client.apigatewayv2.create_route(
            ApiId=api_id,
            RouteKey="ANY /api",
            Target=f"integrations/{integration_id}",
            AuthorizationType="NONE",
        )

        stage_name = "dev"
        aws_client.apigatewayv2.create_stage(
            ApiId=api_id,
            StageName=stage_name,
            AutoDeploy=True,
        )

        # assert responses
        for path in ["/api", "/api/anything"]:

            def invoke():
                _endpoint = api_invoke_url(api_id=api_id, stage=stage_name, path=path)
                _response = requests.post(
                    _endpoint,
                    json=json.dumps({"foo": "bar"}),
                    headers={"X-Test": "test", "User-Agent": "python/testing"},
                    params={"queryStringParam": "test"},
                    verify=False,
                )
                assert _response.status_code == 200
                return _response

            response = retry(invoke, sleep=1, retries=10)
            snapshot.match(f"invoke-{path}", response.json())

        for query_string_param, snapshot_name in (
            ("a=b&redirect_uri=http://localhost:3001/example-client/success", "qs-non-encoded"),
            (
                {"a": "b", "redirect_uri": "http://localhost:3001/example-client/success"},
                "qs-encoded",
            ),
        ):
            # assert that a request with a Query String containing a URL works
            endpoint = api_invoke_url(api_id=api_id, stage=stage_name, path="/api/test-qs")
            response = requests.post(
                endpoint,
                json=json.dumps({"foo": "bar"}),
                # this is hacky, but `requests` percent-encode requests per the standard. But AWS allows query string
                # parameters to not be URL encoded. Passing directly a string bypasses that
                params=query_string_param,
                headers={"User-Agent": "python/testing"},
                verify=False,
            )
            assert response.status_code == 200
            response = response.json()
            if not is_aws_cloud():
                # TODO: there's a weird case when API Gateway proxies a non-encoded request, it does not URL-encode
                #  the ':' character. For now this is handled here, but should be looked into.
                #  Weirdly, if the request _was_ encoded, then it fully encode it when forwarding
                if snapshot_name == "qs-non-encoded":
                    response["url"] = response["url"].replace("%3A", ":")

            snapshot.match(f"invoke-{snapshot_name}-with-url", response)

    @markers.snapshot.skip_snapshot_verify(
        paths=[
            "$.create-integration.ConnectionType",  # FIXME: parity issue
            "$.create-route.ApiKeyRequired",
            "$.invoke-api.headers.via",  # FIXME: missing header, but does not show up on httpbin.org, maybe removed?
            # all headers under are Lambda URL issue
            "$.invoke-api.headers.x-amzn-trace-id",
            "$.invoke-api.headers.x-amzn-tls-cipher-suite",
            "$.invoke-api.headers.x-amzn-tls-version",
            "$.invoke-api.headers.x-forwarded-for",
            "$.invoke-api.headers.x-forwarded-proto",
            "$.invoke-api.origin",
        ]
    )
    @markers.snapshot.skip_snapshot_verify(
        condition=lambda: not is_next_gen_api(),
        paths=[
            "$.create-stage.DefaultRouteSettings",
            "$.create-stage.LastUpdatedDate",
            "$.create-stage.RouteSettings",
            "$.create-stage.StageVariables",
            "$.create-stage.Tags",
            "$.invoke-api.headers.x-localstack-edge",  # FIXME: added by LS
        ],
    )
    @markers.aws.validated
    def test_http_integration_keeps_body_intact(
        self, aws_client, create_v2_api, create_echo_http_server, snapshot
    ):
        snapshot.add_transformer(
            [
                snapshot.transform.key_value("RouteId"),
                snapshot.transform.key_value("IntegrationId"),
                snapshot.transform.key_value("IntegrationUri"),
                snapshot.transform.key_value("domain"),
                snapshot.transform.key_value("host"),
                snapshot.transform.key_value("forwarded"),
                # Funny enough, the snapshot library keeps count of the trace-id of regular CRUD requests?
                snapshot.transform.key_value(
                    "x-amzn-trace-id", "<x-amzn-trace-id>", reference_replacement=False
                ),
                snapshot.transform.key_value("origin"),
                snapshot.transform.key_value("x-forwarded-for"),
                snapshot.transform.key_value("x-forwarded-port"),
            ]
        )
        echo_server_url = create_echo_http_server(trim_x_headers=False)

        result = create_v2_api(ProtocolType="HTTP", Name=f"test-http-{short_uid()}")
        api_id = result["ApiId"]

        create_integration = aws_client.apigatewayv2.create_integration(
            ApiId=api_id,
            IntegrationType="HTTP_PROXY",
            PayloadFormatVersion="1.0",
            IntegrationMethod="ANY",
            IntegrationUri=echo_server_url,
        )
        snapshot.match("create-integration", create_integration)
        integration_id = create_integration["IntegrationId"]

        # creates the /{proxy+} route
        create_route = aws_client.apigatewayv2.create_route(
            ApiId=api_id,
            RouteKey="ANY /api/{proxy+}",
            Target=f"integrations/{integration_id}",
            AuthorizationType="NONE",
        )
        snapshot.match("create-route", create_route)

        stage_name = "dev"
        create_stage = aws_client.apigatewayv2.create_stage(
            ApiId=api_id,
            StageName=stage_name,
            AutoDeploy=True,
        )
        snapshot.match("create-stage", create_stage)

        # multipart body
        body = (
            b"\r\n--4efd159eae0c4f4e125a5a509e073d85\r\n"
            b'Content-Disposition: form-data; name="formfield"\r\n\r\n'
            b"not a file, just a field"
            b"\r\n--4efd159eae0c4f4e125a5a509e073d85\r\n"
            b'Content-Disposition: form-data; name="foo"; filename="foo"\r\n'
            b"Content-Type: text/plain;\r\n\r\n"
            b"bar"
            b"\r\n\r\n--4efd159eae0c4f4e125a5a509e073d85--\r\n"
        )

        def invoke():
            _endpoint = api_invoke_url(api_id=api_id, stage=stage_name, path="/api/test")
            _response = requests.post(
                _endpoint,
                headers={
                    "Content-Type": "multipart/form-data; boundary=4efd159eae0c4f4e125a5a509e073d85",
                    "User-Agent": "python/test-request",
                },
                data=body,
                verify=False,
            )
            assert _response.status_code == 200
            return _response

        response = retry(invoke, sleep=1, retries=10)
        json_data = response.json()
        snapshot.match("invoke-api", json_data)

        form_data = base64.b64decode(json_data["data"])
        assert form_data == body

    @pytest.mark.skipif(
        condition=not is_next_gen_api() and not is_aws_cloud(),
        reason="Not properly implemented",
    )
    @markers.aws.validated
    def test_http_proxy_invalid_uri_with_stage_variables(self, aws_client, create_v2_api, snapshot):
        result = create_v2_api(
            ProtocolType="HTTP",
            Name=f"{short_uid()}",
            Target="http://${stageVariables.doesNotExists}",
            RouteKey="GET /bad-uri",
        )
        api_id = result["ApiId"]

        # assert responses
        _endpoint = api_invoke_url(api_id=api_id, path="/bad-uri")

        def invoke():
            _response = requests.get(_endpoint, verify=False)
            assert _response.status_code != 404
            return {"content": _response.json(), "statusCode": _response.status_code}

        response = retry(invoke, sleep=1 if is_aws_cloud() else 0.1, retries=5)
        snapshot.match("invoke-bad-uri", response)

    @pytest.mark.skipif(
        condition=not is_next_gen_api() and not is_aws_cloud(),
        reason="Not properly implemented",
    )
    @markers.aws.validated
    def test_http_proxy_passes_body_for_get_method(
        self,
        aws_client,
        create_v2_api,
        apigw_echo_http_server_anything,
        snapshot,
        apigwv2_httpbin_headers_transformers,
    ):
        result = create_v2_api(
            ProtocolType="HTTP",
            Name=f"{short_uid()}",
            Target=apigw_echo_http_server_anything,
            RouteKey="GET /get-request",
        )
        api_id = result["ApiId"]

        # assert responses
        _endpoint = api_invoke_url(api_id=api_id, path="/get-request")

        def invoke() -> dict:
            _response = requests.get(
                _endpoint,
                data="Sir, this is a Wendy's",
                verify=False,
                headers={"User-Agent": "python/testing"},
            )
            assert _response.status_code != 404
            return {"content": _response.json(), "statusCode": _response.status_code}

        response = retry(invoke, sleep=1 if is_aws_cloud() else 0.1, retries=5)
        snapshot.match("invoke-get-body", response)

    @markers.aws.validated
    @markers.snapshot.skip_snapshot_verify(
        condition=lambda: not is_next_gen_api(),
        paths=[
            "$..headers.Content-Length",
            "$..headers.X-Amzn-Trace-Id",
            "$..headers.X-Localstack-Edge",
        ],
    )
    def test_http_proxy_query_string_in_uri(
        self,
        aws_client,
        create_v2_api,
        apigw_echo_http_server_anything,
        snapshot,
        apigwv2_httpbin_headers_transformers,
    ):
        target_with_qs = f"{apigw_echo_http_server_anything}?uriQueryString=uriValue"
        result = create_v2_api(
            ProtocolType="HTTP",
            Name=f"{short_uid()}",
            Target=target_with_qs,
            RouteKey="GET /get-request",
        )
        api_id = result["ApiId"]

        # assert responses
        _endpoint = api_invoke_url(api_id=api_id, path="/get-request")

        def invoke() -> dict:
            _response = requests.get(
                _endpoint,
                params={"moreQueryString": "really"},
                verify=False,
                headers={"User-Agent": "python/testing"},
            )
            assert _response.status_code != 404
            return {"content": _response.json(), "statusCode": _response.status_code}

        response = retry(invoke, sleep=1 if is_aws_cloud() else 0.1, retries=5)
        snapshot.match("invoke-with-qs", response)

    @pytest.mark.skipif(
        condition=not is_next_gen_api() and not is_aws_cloud(),
        reason="Not properly implemented: it replaces the value, and does not render stage variables",
    )
    @markers.aws.validated
    def test_http_proxy_with_path_param_in_querystring(
        self,
        aws_client,
        create_v2_api,
        apigw_echo_http_server_anything,
        snapshot,
        apigwv2_httpbin_headers_transformers,
    ):
        target_with_qs = f"{apigw_echo_http_server_anything}?uriQueryString={{param}}&stage=${{stageVariables.test}}"
        result = create_v2_api(
            ProtocolType="HTTP",
            Name=f"{short_uid()}",
            Target=target_with_qs,
            RouteKey="GET /get-request/{param}",
        )
        api_id = result["ApiId"]

        # assert responses
        _endpoint = api_invoke_url(api_id=api_id, path="/get-request/testValue")

        def invoke() -> dict:
            _response = requests.get(
                _endpoint,
                verify=False,
                headers={"User-Agent": "python/testing"},
            )
            assert _response.status_code != 404
            return {"content": _response.json(), "statusCode": _response.status_code}

        response = retry(invoke, sleep=1 if is_aws_cloud() else 0.1, retries=5)
        # result is good, but AWS does not URL-encode the query string in the URI when sending it, and we do
        if not is_aws_cloud():
            response["content"]["url"] = (
                response["content"]["url"].replace("%7B", "{").replace("%7D", "}")
            )
        snapshot.match("invoke-with-qs-param", response)

    @markers.aws.validated
    @markers.snapshot.skip_snapshot_verify(
        condition=lambda: not is_next_gen_api(),
        paths=[
            "$..headers.Content-Length",
            "$..headers.X-Amzn-Trace-Id",
            "$..headers.X-Localstack-Edge",
        ],
    )
    def test_http_proxy_with_path_param(
        self,
        aws_client,
        create_v2_api,
        apigw_echo_http_server_anything,
        snapshot,
        apigwv2_httpbin_headers_transformers,
    ):
        target_with_param = apigw_echo_http_server_anything.replace("anything", "{param}")
        result = create_v2_api(
            ProtocolType="HTTP",
            Name=f"{short_uid()}",
            Target=target_with_param,
            RouteKey="GET /get-request/{param}",
        )
        api_id = result["ApiId"]

        # assert responses
        endpoint = api_invoke_url(api_id=api_id, path="/get-request/anything")

        def invoke() -> dict:
            _response = requests.get(
                endpoint,
                verify=False,
                headers={"User-Agent": "python/testing"},
            )
            assert _response.status_code != 404
            return {"content": _response.json(), "statusCode": _response.status_code}

        response = retry(invoke, sleep=1 if is_aws_cloud() else 0.1, retries=5)
        snapshot.match("invoke-with-path-param", response)

        get_endpoint = api_invoke_url(api_id=api_id, path="/get-request/get")
        response = requests.get(
            get_endpoint, verify=False, headers={"User-Agent": "python/testing"}
        )
        data = {"url": response.json()["url"]}
        snapshot.match("invoke-with-get-path-param", data)

    @markers.aws.validated
    @markers.snapshot.skip_snapshot_verify(
        condition=lambda: not is_next_gen_api(),
        paths=[
            "$..headers.Content-Length",
            "$..headers.X-Amzn-Trace-Id",
            "$..headers.X-Localstack-Edge",
        ],
    )
    def test_http_proxy_with_path_param_overwrite(
        self,
        aws_client,
        create_v2_api,
        apigw_echo_http_server_anything,
        snapshot,
        apigwv2_httpbin_headers_transformers,
    ):
        target = f"{apigw_echo_http_server_anything}/{{param}}/test"
        result = create_v2_api(ProtocolType="HTTP", Name=f"test-http-{short_uid()}")
        api_id = result["ApiId"]

        create_integration = aws_client.apigatewayv2.create_integration(
            ApiId=api_id,
            IntegrationType="HTTP_PROXY",
            PayloadFormatVersion="1.0",
            IntegrationMethod="ANY",
            IntegrationUri=target,
            RequestParameters={"overwrite:path": "anything"},
        )
        integration_id = create_integration["IntegrationId"]

        aws_client.apigatewayv2.create_route(
            ApiId=api_id,
            RouteKey="GET /get-request/{param}",
            Target=f"integrations/{integration_id}",
            AuthorizationType="NONE",
        )
        aws_client.apigatewayv2.create_stage(
            ApiId=api_id,
            StageName="$default",
            AutoDeploy=True,
        )

        # assert responses
        endpoint = api_invoke_url(api_id=api_id, path="/get-request/testValue")

        def invoke() -> dict:
            _response = requests.get(
                endpoint,
                verify=False,
                headers={"User-Agent": "python/testing"},
            )
            assert _response.status_code != 404
            return {"content": _response.json(), "statusCode": _response.status_code}

        response = retry(invoke, sleep=1 if is_aws_cloud() else 0.1, retries=5)
        snapshot.match("invoke-with-path-override", response)

    @markers.aws.validated
    @pytest.mark.skipif(
        condition=not is_next_gen_api() and not is_aws_cloud(),
        reason="Not properly implemented",
    )
    def test_http_proxy_with_path_param_overwrite_with_qs(
        self,
        aws_client,
        create_v2_api,
        apigw_echo_http_server_anything,
        snapshot,
        apigwv2_httpbin_headers_transformers,
    ):
        target = f"{apigw_echo_http_server_anything}/{{param}}/test?q=uriHardcoded"
        result = create_v2_api(ProtocolType="HTTP", Name=f"test-http-{short_uid()}")
        api_id = result["ApiId"]

        create_integration = aws_client.apigatewayv2.create_integration(
            ApiId=api_id,
            IntegrationType="HTTP_PROXY",
            PayloadFormatVersion="1.0",
            IntegrationMethod="ANY",
            IntegrationUri=target,
            RequestParameters={"overwrite:path": "anything?q1=overwriteHardcoded"},
        )
        integration_id = create_integration["IntegrationId"]

        aws_client.apigatewayv2.create_route(
            ApiId=api_id,
            RouteKey="GET /get-request/{param}",
            Target=f"integrations/{integration_id}",
            AuthorizationType="NONE",
        )
        aws_client.apigatewayv2.create_stage(
            ApiId=api_id,
            StageName="$default",
            AutoDeploy=True,
        )

        # assert responses
        endpoint = api_invoke_url(api_id=api_id, path="/get-request/testValue?q2=requestQuery")

        def invoke() -> dict:
            _response = requests.get(
                endpoint,
                verify=False,
                headers={"User-Agent": "python/testing"},
            )
            assert _response.status_code != 404
            return {"content": _response.json(), "statusCode": _response.status_code}

        response = retry(invoke, sleep=1 if is_aws_cloud() else 0.1, retries=5)
        snapshot.match("invoke-with-path-override-with-qs", response)

    @markers.aws.validated
    @pytest.mark.skipif(
        condition=not is_next_gen_api() and not is_aws_cloud(),
        reason="Not properly implemented",
    )
    def test_http_proxy_with_path_param_overwrite_multivalue(
        self,
        aws_client,
        create_v2_api,
        apigw_echo_http_server_anything,
        snapshot,
        apigwv2_httpbin_headers_transformers,
    ):
        target_no_query = f"{apigw_echo_http_server_anything}/{{param}}"
        target_query = f"{apigw_echo_http_server_anything}/{{param}}/test?q1=uriHardcoded"
        result = create_v2_api(ProtocolType="HTTP", Name=f"test-http-{short_uid()}")
        api_id = result["ApiId"]

        int_no_query_target_with_overwrite = aws_client.apigatewayv2.create_integration(
            ApiId=api_id,
            IntegrationType="HTTP_PROXY",
            PayloadFormatVersion="1.0",
            IntegrationMethod="ANY",
            IntegrationUri=target_no_query,
            RequestParameters={"overwrite:path": "anything?q1=hardcoded"},
        )
        int_id_no_query_target_with_overwrite = int_no_query_target_with_overwrite["IntegrationId"]

        int_query_target_no_overwrite = aws_client.apigatewayv2.create_integration(
            ApiId=api_id,
            IntegrationType="HTTP_PROXY",
            PayloadFormatVersion="1.0",
            IntegrationMethod="ANY",
            IntegrationUri=target_query,
        )
        int_id_query_target_no_overwrite = int_query_target_no_overwrite["IntegrationId"]

        int_no_query_target_no_overwrite = aws_client.apigatewayv2.create_integration(
            ApiId=api_id,
            IntegrationType="HTTP_PROXY",
            PayloadFormatVersion="1.0",
            IntegrationMethod="ANY",
            IntegrationUri=target_no_query,
        )
        int_id_no_query_target_no_overwrite = int_no_query_target_no_overwrite["IntegrationId"]

        aws_client.apigatewayv2.create_route(
            ApiId=api_id,
            RouteKey="GET /no-query-target-with-overwrite/{param}",
            Target=f"integrations/{int_id_no_query_target_with_overwrite}",
            AuthorizationType="NONE",
        )
        aws_client.apigatewayv2.create_route(
            ApiId=api_id,
            RouteKey="GET /query-target-no-overwrite/{param}",
            Target=f"integrations/{int_id_query_target_no_overwrite}",
            AuthorizationType="NONE",
        )
        aws_client.apigatewayv2.create_route(
            ApiId=api_id,
            RouteKey="GET /no-query-target-no-overwrite/{param}",
            Target=f"integrations/{int_id_no_query_target_no_overwrite}",
            AuthorizationType="NONE",
        )
        aws_client.apigatewayv2.create_stage(
            ApiId=api_id,
            StageName="$default",
            AutoDeploy=True,
        )

        # assert responses
        endpoint = api_invoke_url(
            api_id=api_id, path="/no-query-target-with-overwrite/testValue?q1=requestQuery"
        )

        def invoke(url) -> dict:
            _response = requests.get(
                url,
                verify=False,
                headers={"User-Agent": "python/testing"},
            )
            assert _response.status_code != 404
            return {"content": _response.json(), "statusCode": _response.status_code}

        response = retry(invoke, sleep=1 if is_aws_cloud() else 0.1, retries=5, url=endpoint)
        snapshot.match("invoke-no-query-target-with-overwrite", response)

        endpoint = api_invoke_url(
            api_id=api_id, path="/query-target-no-overwrite/testValue?q1=requestQuery"
        )
        response = invoke(endpoint)
        snapshot.match("invoke-query-target-no-overwrite", response)

        endpoint = api_invoke_url(
            api_id=api_id, path="/no-query-target-no-overwrite/testValue?q1=requestQuery"
        )
        response = invoke(endpoint)
        snapshot.match("invoke-no-query-target-no-overwrite", response)

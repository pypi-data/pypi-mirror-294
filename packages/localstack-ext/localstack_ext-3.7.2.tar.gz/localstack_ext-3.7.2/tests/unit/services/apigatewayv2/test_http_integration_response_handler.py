import pytest
from localstack.http import Request, Response
from localstack.pro.core.aws.api.apigatewayv2 import (
    Integration,
)
from localstack.pro.core.services.apigatewayv2.next_gen.execute_api.http.api import (
    HttpApiGatewayHandlerChain,
)
from localstack.pro.core.services.apigatewayv2.next_gen.execute_api.http.context import (
    HttpApiInvocationContext,
)
from localstack.pro.core.services.apigatewayv2.next_gen.execute_api.http.handlers import (
    HttpIntegrationResponseHandler,
)
from localstack.pro.core.services.apigatewayv2.next_gen.execute_api.http.invoke_exceptions import (
    InternalServerError,
)
from localstack.pro.core.services.apigatewayv2.next_gen.execute_api.http.variables import (
    HttpContextVariables,
)
from localstack.pro.core.services.apigatewayv2.next_gen.models import ApiDeployment, V2Api
from localstack.services.apigateway.next_gen.execute_api.context import EndpointResponse
from localstack.testing.config import TEST_AWS_ACCOUNT_ID, TEST_AWS_REGION_NAME
from werkzeug.datastructures import Headers

TEST_API_ID = "test-api"
TEST_API_STAGE = "stage"


@pytest.fixture
def default_context():
    """
    Create a context populated with what we would expect to receive from the chain at runtime.
    We assume that the parser and other handler have successfully populated the context to this point.
    """

    context = HttpApiInvocationContext(Request())

    # Frozen deployment populated by the router
    context.deployment = ApiDeployment(
        account_id=TEST_AWS_ACCOUNT_ID,
        region=TEST_AWS_REGION_NAME,
        http_api=V2Api(api_data={}),
    )

    # Context populated by parser handler before creating the invocation request
    context.region = TEST_AWS_REGION_NAME
    context.account_id = TEST_AWS_ACCOUNT_ID
    context.stage = TEST_API_STAGE
    context.api_id = TEST_API_ID

    # request = HttpInvocationRequestParser().create_invocation_request(context)
    # context.invocation_request = request

    context.integration = Integration()
    context.context_variables = HttpContextVariables(apiId=TEST_API_ID)
    context.stage_variables = {"stage_var": "stage var value"}
    context.endpoint_response = EndpointResponse(
        body=b'{"foo":"bar"}',
        status_code=200,
        headers=Headers({"content-type": "application/json", "multi": ["multi", "header"]}),
    )
    return context


@pytest.fixture
def integration_response_handler():
    """Returns a dummy integration response handler invoker for testing."""

    def _handler_invoker(context: HttpApiInvocationContext, response: Response):
        return HttpIntegrationResponseHandler()(HttpApiGatewayHandlerChain(), context, response)

    return _handler_invoker


class TestHttpIntegrationResponseHandler:
    def test_status_code_overwrite(self, default_context, integration_response_handler):
        default_context.integration["ResponseParameters"] = {"200": {"overwrite:statuscode": "300"}}

        response = Response()
        integration_response_handler(default_context, response)
        assert response.status_code == 300

    def test_unmatched_response(self, default_context, integration_response_handler):
        default_context.integration["ResponseParameters"] = {"201": {"overwrite:statuscode": "300"}}

        response = Response()
        integration_response_handler(default_context, response)
        assert response.status_code == 200

    def test_status_code_not_int(self, default_context, integration_response_handler):
        default_context.integration["ResponseParameters"] = {
            "200": {"overwrite:statuscode": "two hundred"}
        }

        response = Response()
        integration_response_handler(default_context, response)
        assert response.status_code == 200

    def test_status_code_out_of_range_under(self, default_context, integration_response_handler):
        default_context.integration["ResponseParameters"] = {"200": {"overwrite:statuscode": "99"}}

        response = Response()
        with pytest.raises(InternalServerError) as e:
            integration_response_handler(default_context, response)
        assert e.value.status_code == 503
        assert e.value.message == "Internal Server Error"

    def test_status_code_out_of_range_over(self, default_context, integration_response_handler):
        default_context.integration["ResponseParameters"] = {
            "200": {"overwrite:statuscode": "1000"}
        }

        response = Response()
        with pytest.raises(InternalServerError) as e:
            integration_response_handler(default_context, response)
        assert e.value.status_code == 503
        assert e.value.message == "Internal Server Error"

    def test_status_code_negative_integer(self, default_context, integration_response_handler):
        default_context.integration["ResponseParameters"] = {"200": {"overwrite:statuscode": "-1"}}

        response = Response()
        integration_response_handler(default_context, response)
        assert response.status_code == 200

    def test_header_complete_sources(self, default_context, integration_response_handler):
        default_context.integration["ResponseParameters"] = {
            "200": {
                "append:header.header_value": "$response.header.content-type",
                "append:header.from_multi": "$response.header.multi",
                "append:header.full_body": "$response.body",
                "append:header.body_foo": "$response.body.foo",
                "append:header.contextVar": "$context.apiId",
                "append:header.stage-Var": "$stageVariables.stage_var",
            }
        }

        response = Response()
        integration_response_handler(default_context, response)
        assert response.headers["content-type"] == "application/json"
        assert response.headers["header_value"] == "application/json"
        assert response.headers.getlist("multi") == ["multi", "header"]
        assert response.headers["from_multi"] == "multi,header"
        assert response.headers["full_body"] == '{"foo":"bar"}'
        assert response.headers["body_foo"] == "bar"
        assert response.headers["contextVar"] == TEST_API_ID
        assert response.headers["stage-var"] == "stage var value"

    def test_header_append_to_existing(self, default_context, integration_response_handler):
        default_context.integration["ResponseParameters"] = {
            "200": {"append:header.multi": "$response.header.content-type"}
        }

        response = Response()
        integration_response_handler(default_context, response)
        assert response.headers.getlist("multi") == ["multi", "header", "application/json"]

    def test_header_overwrite(self, default_context, integration_response_handler):
        default_context.integration["ResponseParameters"] = {
            "200": {"overwrite:header.multi": "$response.header.content-type"}
        }

        response = Response()
        integration_response_handler(default_context, response)
        assert response.headers.getlist("multi") == ["application/json"]

    def test_header_remove(self, default_context, integration_response_handler):
        default_context.integration["ResponseParameters"] = {"200": {"remove:header.multi": "''"}}

        response = Response()
        integration_response_handler(default_context, response)
        assert response.headers.getlist("multi") == []

    def test_populate_context_invocation_response(
        self, default_context, integration_response_handler
    ):
        default_context.integration["ResponseParameters"] = {
            "200": {
                "overwrite:statuscode": "300",
                "append:header.header_value": "$response.header.content-type",
            }
        }

        response = Response()
        integration_response_handler(default_context, response)
        assert default_context.invocation_response == {
            "body": b'{"foo":"bar"}',
            "headers": Headers(
                {
                    "content-type": "application/json",
                    "multi": ["multi", "header"],
                    "header_value": "application/json",
                    "Content-Length": "13",
                }
            ),
            "status_code": 300,
        }

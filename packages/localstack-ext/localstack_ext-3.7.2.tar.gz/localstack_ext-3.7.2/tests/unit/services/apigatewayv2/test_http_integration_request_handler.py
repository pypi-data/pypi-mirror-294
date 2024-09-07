from http import HTTPMethod

import pytest
from localstack.http import Request, Response
from localstack.pro.core.aws.api.apigatewayv2 import Integration, IntegrationType
from localstack.pro.core.services.apigatewayv2.next_gen.execute_api.http.api import (
    HttpApiGatewayHandlerChain,
)
from localstack.pro.core.services.apigatewayv2.next_gen.execute_api.http.context import (
    HttpApiInvocationContext,
)
from localstack.pro.core.services.apigatewayv2.next_gen.execute_api.http.handlers import (
    HttpIntegrationRequestHandler,
    HttpInvocationRequestParser,
)
from localstack.pro.core.services.apigatewayv2.next_gen.models import (
    ApiDeployment,
    V2Api,
)
from localstack.testing.config import TEST_AWS_ACCOUNT_ID, TEST_AWS_REGION_NAME
from werkzeug.datastructures.headers import Headers

TEST_API_ID = "test-api"
TEST_API_STAGE = "stage"


@pytest.fixture
def default_context():
    """
    Create a context populated with what we would expect to receive from the chain at runtime.
    We assume that the parser and other handler have successfully populated the context to this point.
    """

    context = HttpApiInvocationContext(
        Request(
            method=HTTPMethod.POST,
            headers={"header": ["header1", "header2"]},
            path=f"/{TEST_API_STAGE}/resource/path",
            query_string="qs=qs1&qs=qs2",
        )
    )

    # Frozen deployment populated by the router
    context.deployment = ApiDeployment(
        account_id=TEST_AWS_ACCOUNT_ID,
        region=TEST_AWS_REGION_NAME,
        http_api=V2Api(api_data={}),
    )
    context.stage = TEST_API_STAGE

    request = HttpInvocationRequestParser().create_invocation_request(context)
    context.invocation_request = request
    request["path_parameters"] = {"path_param": "path"}

    context.integration = Integration(
        IntegrationMethod="POST",
        IntegrationType=IntegrationType.HTTP_PROXY,
        IntegrationUri="http://example.com",
    )

    return context


@pytest.fixture
def integration_request_handler():
    """Returns a dummy integration request handler invoker for testing."""

    def _handler_invoker(context: HttpApiInvocationContext):
        return HttpIntegrationRequestHandler()(HttpApiGatewayHandlerChain(), context, Response())

    return _handler_invoker


class TestHandlerHttpIntegrationRequest:
    def test_noop(self, integration_request_handler, default_context):
        integration_request_handler(default_context)

        assert default_context.integration_request == {
            "body": b"",
            "headers": Headers({"header": ["header1", "header2"], "content-length": "0"}),
            "http_method": "POST",
            "query_string_parameters": {"qs": ["qs1", "qs2"]},
            "path_override": None,
            "uri": "http://example.com",
        }

    def test_append_header_existing(self, integration_request_handler, default_context):
        default_context.integration["RequestParameters"] = {"append:header.header": "header3"}
        integration_request_handler(default_context)

        assert default_context.integration_request == {
            "body": b"",
            "headers": Headers(
                {"header": ["header1", "header2", "header3"], "content-length": "0"}
            ),
            "http_method": "POST",
            "query_string_parameters": {"qs": ["qs1", "qs2"]},
            "path_override": None,
            "uri": "http://example.com",
        }

    def test_append_header_new(self, integration_request_handler, default_context):
        default_context.integration["RequestParameters"] = {
            "append:header.new-header": "new header"
        }
        integration_request_handler(default_context)

        assert default_context.integration_request == {
            "body": b"",
            "headers": Headers(
                {
                    "header": ["header1", "header2"],
                    "content-length": "0",
                    "new-header": "new header",
                }
            ),
            "http_method": "POST",
            "query_string_parameters": {"qs": ["qs1", "qs2"]},
            "path_override": None,
            "uri": "http://example.com",
        }

    def test_append_multiple_headers(self, integration_request_handler, default_context):
        default_context.integration["RequestParameters"] = {
            "append:header.header": "header3",
            "append:header.header.2": "header4",
        }
        integration_request_handler(default_context)

        assert default_context.integration_request == {
            "body": b"",
            "headers": Headers(
                {
                    "header": ["header1", "header2", "header3", "header4"],
                    "content-length": "0",
                }
            ),
            "http_method": "POST",
            "query_string_parameters": {"qs": ["qs1", "qs2"]},
            "path_override": None,
            "uri": "http://example.com",
        }

    def test_overwrite_header_existing(self, integration_request_handler, default_context):
        default_context.integration["RequestParameters"] = {"overwrite:header.header": "header3"}
        integration_request_handler(default_context)

        assert default_context.integration_request == {
            "body": b"",
            "headers": Headers({"header": ["header3"], "content-length": "0"}),
            "http_method": "POST",
            "query_string_parameters": {"qs": ["qs1", "qs2"]},
            "path_override": None,
            "uri": "http://example.com",
        }

    def test_overwrite_header_new(self, integration_request_handler, default_context):
        default_context.integration["RequestParameters"] = {
            "overwrite:header.new-header": "new header"
        }
        integration_request_handler(default_context)

        assert default_context.integration_request == {
            "body": b"",
            "headers": Headers(
                {
                    "header": ["header1", "header2"],
                    "content-length": "0",
                    "new-header": "new header",
                }
            ),
            "http_method": "POST",
            "query_string_parameters": {"qs": ["qs1", "qs2"]},
            "path_override": None,
            "uri": "http://example.com",
        }

    def test_overwrite_multiple_headers(self, integration_request_handler, default_context):
        default_context.integration["RequestParameters"] = {
            "overwrite:header.header": "header3",
            "overwrite:header.header.2": "header4",
        }
        integration_request_handler(default_context)

        assert default_context.integration_request["headers"].getlist("header") in [
            ["header3"],
            ["header4"],
        ]

    def test_remove_header_existing(self, integration_request_handler, default_context):
        default_context.integration["RequestParameters"] = {"remove:header.header": "''"}
        integration_request_handler(default_context)

        assert default_context.integration_request == {
            "body": b"",
            "headers": Headers({"content-length": "0"}),
            "http_method": "POST",
            "query_string_parameters": {"qs": ["qs1", "qs2"]},
            "path_override": None,
            "uri": "http://example.com",
        }

    def test_remove_header_new(self, integration_request_handler, default_context):
        default_context.integration["RequestParameters"] = {"remove:header.new-header": "''"}
        integration_request_handler(default_context)

        assert default_context.integration_request == {
            "body": b"",
            "headers": Headers({"header": ["header1", "header2"], "content-length": "0"}),
            "http_method": "POST",
            "query_string_parameters": {"qs": ["qs1", "qs2"]},
            "path_override": None,
            "uri": "http://example.com",
        }

    def test_append_and_overwrite_same_header(self, integration_request_handler, default_context):
        default_context.integration["RequestParameters"] = {
            "append:header.header": "header3",
            "overwrite:header.header.2": "header4",
        }
        integration_request_handler(default_context)

        assert default_context.integration_request == {
            "body": b"",
            "headers": Headers({"header": "header4", "content-length": "0"}),
            "http_method": "POST",
            "query_string_parameters": {"qs": ["qs1", "qs2"]},
            "path_override": None,
            "uri": "http://example.com",
        }

    def test_append_and_remove_same_header(self, integration_request_handler, default_context):
        default_context.integration["RequestParameters"] = {
            "append:header.header": "header3",
            "remove:header.header.2": "''",
        }
        integration_request_handler(default_context)

        assert default_context.integration_request == {
            "body": b"",
            "headers": Headers({"content-length": "0"}),
            "http_method": "POST",
            "query_string_parameters": {"qs": ["qs1", "qs2"]},
            "path_override": None,
            "uri": "http://example.com",
        }

    def test_overwrite_and_remove_same_header(self, integration_request_handler, default_context):
        default_context.integration["RequestParameters"] = {
            "overwrite:header.header": "header3",
            "remove:header.header.2": "''",
        }
        integration_request_handler(default_context)

        assert default_context.integration_request == {
            "body": b"",
            "headers": Headers({"content-length": "0"}),
            "http_method": "POST",
            "query_string_parameters": {"qs": ["qs1", "qs2"]},
            "path_override": None,
            "uri": "http://example.com",
        }

    def test_append_qs_existing(self, integration_request_handler, default_context):
        default_context.integration["RequestParameters"] = {"append:querystring.qs": "qs3"}
        integration_request_handler(default_context)

        assert default_context.integration_request == {
            "body": b"",
            "headers": Headers({"header": ["header1", "header2"], "content-length": "0"}),
            "http_method": "POST",
            "query_string_parameters": {"qs": ["qs1", "qs2", "qs3"]},
            "path_override": None,
            "uri": "http://example.com",
        }

    def test_append_qs_new(self, integration_request_handler, default_context):
        default_context.integration["RequestParameters"] = {"append:querystring.new-qs": "new qs"}
        integration_request_handler(default_context)

        assert default_context.integration_request == {
            "body": b"",
            "headers": Headers({"header": ["header1", "header2"], "content-length": "0"}),
            "http_method": "POST",
            "query_string_parameters": {"qs": ["qs1", "qs2"], "new-qs": ["new qs"]},
            "path_override": None,
            "uri": "http://example.com",
        }

    def test_append_multiple_qs(self, integration_request_handler, default_context):
        default_context.integration["RequestParameters"] = {
            "append:querystring.qs": "qs3",
            "append:querystring.qs.2": "qs4",
        }
        integration_request_handler(default_context)

        assert default_context.integration_request == {
            "body": b"",
            "headers": Headers({"header": ["header1", "header2"], "content-length": "0"}),
            "http_method": "POST",
            "query_string_parameters": {"qs": ["qs1", "qs2", "qs3", "qs4"]},
            "path_override": None,
            "uri": "http://example.com",
        }

    def test_overwrite_qs_existing(self, integration_request_handler, default_context):
        default_context.integration["RequestParameters"] = {"overwrite:querystring.qs": "qs3"}
        integration_request_handler(default_context)

        assert default_context.integration_request == {
            "body": b"",
            "headers": Headers({"header": ["header1", "header2"], "content-length": "0"}),
            "http_method": "POST",
            "query_string_parameters": {"qs": ["qs3"]},
            "path_override": None,
            "uri": "http://example.com",
        }

    def test_overwrite_qs_new(self, integration_request_handler, default_context):
        default_context.integration["RequestParameters"] = {
            "overwrite:querystring.new-qs": "new qs"
        }
        integration_request_handler(default_context)

        assert default_context.integration_request == {
            "body": b"",
            "headers": Headers({"header": ["header1", "header2"], "content-length": "0"}),
            "http_method": "POST",
            "query_string_parameters": {"qs": ["qs1", "qs2"], "new-qs": ["new qs"]},
            "path_override": None,
            "uri": "http://example.com",
        }

    def test_overwrite_multiple_qs(self, integration_request_handler, default_context):
        default_context.integration["RequestParameters"] = {
            "overwrite:querystring.qs": "qs3",
            "overwrite:querystring.qs.2": "qs4",
        }
        integration_request_handler(default_context)

        assert default_context.integration_request["query_string_parameters"]["qs"] in [
            ["qs3"],
            ["qs4"],
        ]

    def test_remove_qs_existing(self, integration_request_handler, default_context):
        default_context.integration["RequestParameters"] = {"remove:querystring.qs": "''"}
        integration_request_handler(default_context)

        assert default_context.integration_request == {
            "body": b"",
            "headers": Headers({"header": ["header1", "header2"], "content-length": "0"}),
            "http_method": "POST",
            "query_string_parameters": {},
            "path_override": None,
            "uri": "http://example.com",
        }

    def test_remove_qs_new(self, integration_request_handler, default_context):
        default_context.integration["RequestParameters"] = {"remove:querystring.new-qs": "''"}
        integration_request_handler(default_context)

        assert default_context.integration_request == {
            "body": b"",
            "headers": Headers({"header": ["header1", "header2"], "content-length": "0"}),
            "http_method": "POST",
            "query_string_parameters": {"qs": ["qs1", "qs2"]},
            "path_override": None,
            "uri": "http://example.com",
        }

    def test_append_and_overwrite_same_qs(self, integration_request_handler, default_context):
        default_context.integration["RequestParameters"] = {
            "append:querystring.qs": "qs3",
            "overwrite:querystring.qs.2": "qs4",
        }
        integration_request_handler(default_context)

        assert default_context.integration_request == {
            "body": b"",
            "headers": Headers({"header": ["header1", "header2"], "content-length": "0"}),
            "http_method": "POST",
            "query_string_parameters": {"qs": ["qs4"]},
            "path_override": None,
            "uri": "http://example.com",
        }

    def test_append_and_remove_same_qs(self, integration_request_handler, default_context):
        default_context.integration["RequestParameters"] = {
            "append:querystring.qs": "qs3",
            "remove:querystring.qs.2": "''",
        }
        integration_request_handler(default_context)

        assert default_context.integration_request == {
            "body": b"",
            "headers": Headers({"header": ["header1", "header2"], "content-length": "0"}),
            "http_method": "POST",
            "query_string_parameters": {},
            "path_override": None,
            "uri": "http://example.com",
        }

    def test_overwrite_and_remove_same_qs(self, integration_request_handler, default_context):
        default_context.integration["RequestParameters"] = {
            "overwrite:querystring.qs": "qs3",
            "remove:querystring.qs.2": "''",
        }
        integration_request_handler(default_context)

        assert default_context.integration_request == {
            "body": b"",
            "headers": Headers({"header": ["header1", "header2"], "content-length": "0"}),
            "http_method": "POST",
            "query_string_parameters": {},
            "path_override": None,
            "uri": "http://example.com",
        }

    def test_overwrite_path(self, integration_request_handler, default_context):
        default_context.integration["RequestParameters"] = {
            "overwrite:path": "new-path",
        }
        integration_request_handler(default_context)

        assert default_context.integration_request == {
            "body": b"",
            "headers": Headers({"header": ["header1", "header2"], "content-length": "0"}),
            "http_method": "POST",
            "query_string_parameters": {"qs": ["qs1", "qs2"]},
            "path_override": "new-path",
            "uri": "http://example.com",
        }

    def test_path_as_source(self, integration_request_handler, default_context):
        default_context.integration["RequestParameters"] = {
            "overwrite:header.header": "$request.path"
        }
        integration_request_handler(default_context)

        assert default_context.integration_request == {
            "body": b"",
            "headers": Headers({"header": ["/resource/path"], "content-length": "0"}),
            "http_method": "POST",
            "query_string_parameters": {"qs": ["qs1", "qs2"]},
            "path_override": None,
            "uri": "http://example.com",
        }

    def test_path_param_as_source(self, integration_request_handler, default_context):
        default_context.integration["RequestParameters"] = {
            "overwrite:header.header": "$request.path.path_param",
        }
        integration_request_handler(default_context)

        assert default_context.integration_request == {
            "body": b"",
            "headers": Headers({"header": ["path"], "content-length": "0"}),
            "http_method": "POST",
            "query_string_parameters": {"qs": ["qs1", "qs2"]},
            "path_override": None,
            "uri": "http://example.com",
        }

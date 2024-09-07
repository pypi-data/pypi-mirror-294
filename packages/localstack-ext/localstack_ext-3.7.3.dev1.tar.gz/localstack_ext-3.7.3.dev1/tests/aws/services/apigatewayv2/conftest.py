import json
import logging

import pytest
from localstack.http import Response
from localstack.testing.aws.util import is_aws_cloud
from localstack.testing.pytest.fixtures import PUBLIC_HTTP_ECHO_SERVER_URL
from localstack.utils.json import json_safe
from localstack.utils.strings import short_uid
from pytest_httpserver import HTTPServer
from rolo import Request

LOG = logging.getLogger(__name__)


@pytest.fixture
def create_v2_api(aws_client):
    apis = []

    def _create(**kwargs):
        if not kwargs.get("Name"):
            kwargs["Name"] = f"api-{short_uid()}"
        response = aws_client.apigatewayv2.create_api(**kwargs)
        apis.append(response)
        return response

    yield _create

    for api in apis:
        try:
            aws_client.apigatewayv2.delete_api(ApiId=api["ApiId"])
        except Exception as e:
            LOG.debug("Unable to delete API Gateway v2 API %s: %s", api, e)


@pytest.fixture
def apigw_echo_http_server(httpserver: HTTPServer):
    """Spins up a local HTTP echo server and returns the endpoint URL
    Aims at emulating more closely the output of httpbin.org that is used to create the
    snapshots
    TODO tests the behavior and outputs of all fields"""

    def _echo(request: Request) -> Response:
        headers = dict(request.headers)
        headers.pop("Connection", None)
        try:
            json_body = json.loads(request.data)
        except json.JSONDecodeError:
            json_body = None

        if raw_uri := request.environ.get("RAW_URI"):
            # strip leading slashes as httpbin.org would do
            raw_url = f"{request.host_url}{raw_uri.lstrip('/')}"
        else:
            raw_url = request.url

        multivalue_args = {}
        for key, value in request.args.items(multi=True):
            if key in multivalue_args:
                if isinstance(multivalue_args[key], list):
                    multivalue_args[key].append(value)
                else:
                    multivalue_args[key] = [multivalue_args[key], value]
            else:
                multivalue_args[key] = value

        result = {
            "args": multivalue_args,
            "data": request.data,
            "files": request.files,
            "form": request.form,
            "headers": headers,
            "json": json_body,
            "origin": request.remote_addr,
            "url": raw_url,
            "method": request.method,
        }
        response_body = json.dumps(json_safe(result))
        return Response(
            response_body,
            status=200,
            headers={
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Credentials": "true",
                "Content-Type": "application/json",
            },
        )

    httpserver.expect_request("").respond_with_handler(_echo)
    http_endpoint = httpserver.url_for("/")

    return http_endpoint


@pytest.fixture
def apigw_echo_http_server_anything(apigw_echo_http_server):
    """
    Returns an HTTP echo server URL for POST requests that work both locally and for parity tests (against real AWS)
    """
    if is_aws_cloud():
        return f"{PUBLIC_HTTP_ECHO_SERVER_URL}/anything"

    return f"{apigw_echo_http_server}/anything"

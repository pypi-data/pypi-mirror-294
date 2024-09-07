import json
from http import HTTPMethod

import pytest
from localstack.pro.core.services.apigatewayv2.next_gen.execute_api.http.context import (
    HttpApiInvocationContext,
    HttpInvocationRequest,
)
from localstack.pro.core.services.apigatewayv2.next_gen.execute_api.http.handlers import (
    HttpInvocationRequestParser,
)
from localstack.pro.core.services.apigatewayv2.next_gen.execute_api.http.variables import (
    HttpContextVariables,
    HttpContextVarsAuthorizer,
)
from localstack.pro.core.services.apigatewayv2.next_gen.execute_api.parameters_mapping import (
    HttpParametersMapper,
    ParameterMapping,
    ParameterType,
)
from localstack.services.apigateway.next_gen.execute_api.context import EndpointResponse
from localstack.utils.strings import to_bytes
from rolo import Request
from werkzeug.datastructures import Headers

TEST_API_ID = "test-api"
TEST_API_STAGE = "stage"
TEST_IDENTITY_API_KEY = "random-api-key"
TEST_USER_AGENT = "test/user-agent"


@pytest.fixture
def default_context_variables() -> HttpContextVariables:
    return HttpContextVariables(
        apiId=TEST_API_ID,
        authorizer=HttpContextVarsAuthorizer(error="test error"),
    )


@pytest.fixture
def default_invocation_request() -> HttpInvocationRequest:
    context = HttpApiInvocationContext(
        request=Request(
            method=HTTPMethod.POST,
            headers=Headers({"header_value": "test-header-value"}),
            path=f"{TEST_API_STAGE}/test/test-path-value",
            query_string="qs_value=test-qs-value",
        )
    )
    context.stage = TEST_API_STAGE
    context.api_id = TEST_API_ID

    invocation_request = HttpInvocationRequestParser().create_invocation_request(context)
    invocation_request["path_parameters"] = {"path_value": "test-path-value"}
    return invocation_request


@pytest.fixture
def default_endpoint_response() -> EndpointResponse:
    return EndpointResponse(
        body=b"",
        headers=Headers(),
        status_code=200,
    )


class TestParseParameterMappingChain:
    @pytest.fixture
    def parse_request_mapping(self):
        def _parse(mapping: str = "", destination: str = "append:header.foo"):
            parameter_mapping = ParameterMapping(
                destination_path=destination,
                mapping_expression=mapping,
                parameter_type=ParameterType.REQUEST,
            )
            return parameter_mapping

        return _parse

    def test_parse_single_static(self, parse_request_mapping):
        parameter = parse_request_mapping("oneWord")
        assert parameter.mapping_expressions == ["oneWord"]

        parameter = parse_request_mapping("two Words")
        assert parameter.mapping_expressions == ["two Words"]

    def test_parse_single_param(self, parse_request_mapping):
        parameter = parse_request_mapping("$request.body.pets[0].name")
        assert parameter.mapping_expressions == ["$request.body.pets[0].name"]

        parameter = parse_request_mapping("${request.body.pets[0].name}")
        assert parameter.mapping_expressions == ["${request.body.pets[0].name}"]

    def test_parse_param_with_whitespace(self, parse_request_mapping):
        parameter = parse_request_mapping("  $request.body.pets[0].name  ")
        assert parameter.mapping_expressions == ["$request.body.pets[0].name"]

        parameter = parse_request_mapping(
            "  $request.body.pets[0].name  ",
            destination="append:querystring.foo",
        )
        assert parameter.mapping_expressions == ["  ", "$request.body.pets[0].name", "  "]

    def test_parse_multiple_params(self, parse_request_mapping):
        parameter = parse_request_mapping("$request.body $request.path")
        assert parameter.mapping_expressions == ["$request.body", " ", "$request.path"]

        parameter = parse_request_mapping("$request.body static")
        assert parameter.mapping_expressions == ["$request.body", " static"]

        parameter = parse_request_mapping("static $request.body")
        assert parameter.mapping_expressions == ["static ", "$request.body"]

    def test_parse_enclosed_in_curly_braces(self, parse_request_mapping):
        parameter = parse_request_mapping("${request.body} ${request.path}")
        assert parameter.mapping_expressions == ["${request.body}", " ", "${request.path}"]

        parameter = parse_request_mapping("${request.body}static")
        assert parameter.mapping_expressions == ["${request.body}", "static"]

        parameter = parse_request_mapping("${request.body}static${request.path}")
        assert parameter.mapping_expressions == ["${request.body}", "static", "${request.path}"]

    def test_parse_with_white_space(self, parse_request_mapping):
        # This first one would result in a validation error
        parameter = parse_request_mapping("$request.body.pets[0].name\n")
        assert parameter.mapping_expressions == ["$request.body.pets[0].name\n"]

        parameter = parse_request_mapping("${request.body.pets[0].name}\n")
        assert parameter.mapping_expressions == ["${request.body.pets[0].name}", "\n"]

    def test_parse_with_extra_curly(self, parse_request_mapping):
        parameter = parse_request_mapping("${request.body}}")
        assert parameter.mapping_expressions == ["${request.body}", "}"]

    def test_chain_with_dynamic_sources(self, parse_request_mapping):
        parameter = parse_request_mapping("$request.body$request.path")
        assert parameter.mapping_expressions == ["$request.body", "$request.path"]

    def test_destination_path(self, parse_request_mapping):
        parameter = parse_request_mapping(destination="overwrite:path")
        assert parameter.action == "overwrite"
        assert parameter.full_destination == "path"
        assert parameter.destination == "path"
        assert parameter.param_name == ""

    def test_destination_with_param_name(self, parse_request_mapping):
        parameter = parse_request_mapping(destination="append:header.header_name")
        assert parameter.action == "append"
        assert parameter.full_destination == "header.header_name"
        assert parameter.destination == "header"
        assert parameter.param_name == "header_name"

    def test_destination_with_suffix(self, parse_request_mapping):
        parameter = parse_request_mapping(destination="append:header.header_name.1.2")
        assert parameter.action == "append"
        assert parameter.full_destination == "header.header_name.1.2"
        assert parameter.destination == "header"
        assert parameter.param_name == "header_name"


class TestApigatewayHttpRequestParametersMapping:
    def test_default_request_mapping_append(
        self, default_invocation_request, default_context_variables
    ):
        mapper = HttpParametersMapper()
        request_parameters = {
            "append:header.test": "$request.querystring.qs_value",
            "append:querystring.test": "$request.path.path_value",
        }

        mapping = mapper.map_http_integration_request(
            request_parameters=request_parameters,
            invocation_request=default_invocation_request,
            stage_variables={},
            context_variables=default_context_variables,
        )
        assert mapping == {
            "header": {
                "append": {"test": ["test-qs-value"]},
                "overwrite": {},
                "remove": [],
            },
            "path": None,
            "querystring": {
                "append": {"test": ["test-path-value"]},
                "overwrite": {},
                "remove": [],
            },
        }

    def test_default_request_mapping_overwrite(
        self, default_invocation_request, default_context_variables
    ):
        mapper = HttpParametersMapper()
        request_parameters = {
            "overwrite:header.header_value": "$request.querystring.qs_value",
            "overwrite:querystring.qs_value": "$request.path.path_value",
            "overwrite:path": "$request.path.path_value",
        }

        mapping = mapper.map_http_integration_request(
            request_parameters=request_parameters,
            invocation_request=default_invocation_request,
            stage_variables={},
            context_variables=default_context_variables,
        )
        assert mapping == {
            "header": {
                "append": {},
                "overwrite": {"header_value": ["test-qs-value"]},
                "remove": [],
            },
            "path": "test-path-value",
            "querystring": {
                "append": {},
                "overwrite": {"qs_value": ["test-path-value"]},
                "remove": [],
            },
        }

    def test_default_request_mapping_remove(
        self, default_invocation_request, default_context_variables
    ):
        mapper = HttpParametersMapper()
        request_parameters = {
            "remove:header.header_value": "",
            "remove:querystring.qs_value": "",
        }

        mapping = mapper.map_http_integration_request(
            request_parameters=request_parameters,
            invocation_request=default_invocation_request,
            stage_variables={},
            context_variables=default_context_variables,
        )
        assert mapping == {
            "header": {"append": {}, "overwrite": {}, "remove": ["header_value"]},
            "path": None,
            "querystring": {"append": {}, "overwrite": {}, "remove": ["qs_value"]},
        }

    def test_default_request_mapping_with_curly(
        self, default_invocation_request, default_context_variables
    ):
        mapper = HttpParametersMapper()
        request_parameters = {"append:header.header_value": "${request.querystring.qs_value}"}

        mapping = mapper.map_http_integration_request(
            request_parameters=request_parameters,
            invocation_request=default_invocation_request,
            stage_variables={},
            context_variables=default_context_variables,
        )
        assert mapping == {
            "header": {
                "append": {"header_value": ["test-qs-value"]},
                "overwrite": {},
                "remove": [],
            },
            "path": None,
            "querystring": {"append": {}, "overwrite": {}, "remove": []},
        }

    def test_context_variables(self, default_invocation_request, default_context_variables):
        mapper = HttpParametersMapper()
        request_parameters = {"append:header.test": "$context.apiId"}

        mapping = mapper.map_http_integration_request(
            request_parameters=request_parameters,
            invocation_request=default_invocation_request,
            stage_variables={},
            context_variables=default_context_variables,
        )

        assert mapping == {
            "header": {"append": {"test": ["test-api"]}, "overwrite": {}, "remove": []},
            "path": None,
            "querystring": {"append": {}, "overwrite": {}, "remove": []},
        }

    def test_nested_context_variables(self, default_invocation_request, default_context_variables):
        mapper = HttpParametersMapper()
        request_parameters = {"append:header.test": "$context.authorizer.error"}

        mapping = mapper.map_http_integration_request(
            request_parameters=request_parameters,
            invocation_request=default_invocation_request,
            stage_variables={},
            context_variables=default_context_variables,
        )
        assert mapping == {
            "header": {"append": {"test": ["test error"]}, "overwrite": {}, "remove": []},
            "path": None,
            "querystring": {"append": {}, "overwrite": {}, "remove": []},
        }

    def test_dict_context_variables(self, default_invocation_request, default_context_variables):
        mapper = HttpParametersMapper()
        request_parameters = {"append:header.test": "$context.authorizer"}

        mapping = mapper.map_http_integration_request(
            request_parameters=request_parameters,
            invocation_request=default_invocation_request,
            stage_variables={},
            context_variables=default_context_variables,
        )
        assert mapping == {
            "header": {"append": {}, "overwrite": {}, "remove": []},
            "path": None,
            "querystring": {"append": {}, "overwrite": {}, "remove": []},
        }

    def test_stage_variables(self, default_invocation_request, default_context_variables):
        mapper = HttpParametersMapper()
        request_parameters = {"append:header.test": "$stageVariables.stage_var"}

        mapping = mapper.map_http_integration_request(
            request_parameters=request_parameters,
            invocation_request=default_invocation_request,
            stage_variables={"stage_var": "test-stage_var"},
            context_variables=default_context_variables,
        )
        assert mapping == {
            "header": {
                "append": {"test": ["test-stage_var"]},
                "overwrite": {},
                "remove": [],
            },
            "path": None,
            "querystring": {"append": {}, "overwrite": {}, "remove": []},
        }

    def test_body_mapping(self, default_invocation_request, default_context_variables):
        mapper = HttpParametersMapper()
        request_parameters = {"append:header.test": "$request.body"}
        default_invocation_request["body"] = b"<This is a body value>"

        mapping = mapper.map_http_integration_request(
            request_parameters=request_parameters,
            invocation_request=default_invocation_request,
            stage_variables={},
            context_variables=default_context_variables,
        )
        assert mapping == {
            "header": {
                "append": {"test": ["<This is a body value>"]},
                "overwrite": {},
                "remove": [],
            },
            "path": None,
            "querystring": {"append": {}, "overwrite": {}, "remove": []},
        }

    def test_body_mapping_empty(self, default_invocation_request, default_context_variables):
        mapper = HttpParametersMapper()
        request_parameters = {"append:header.test": "$request.body"}
        default_invocation_request["body"] = b""

        mapping = mapper.map_http_integration_request(
            request_parameters=request_parameters,
            invocation_request=default_invocation_request,
            stage_variables={},
            context_variables=default_context_variables,
        )
        assert mapping == {
            "header": {"append": {"test": [""]}, "overwrite": {}, "remove": []},
            "path": None,
            "querystring": {"append": {}, "overwrite": {}, "remove": []},
        }

    def test_body_mapping_with_malformed_json(
        self, default_invocation_request, default_context_variables
    ):
        mapper = HttpParametersMapper()
        request_parameters = {"append:header.test": "$request.body"}
        default_invocation_request["body"] = b"{"

        mapping = mapper.map_http_integration_request(
            request_parameters=request_parameters,
            invocation_request=default_invocation_request,
            stage_variables={},
            context_variables=default_context_variables,
        )
        assert mapping == {
            "header": {"append": {"test": ["{"]}, "overwrite": {}, "remove": []},
            "path": None,
            "querystring": {"append": {}, "overwrite": {}, "remove": []},
        }

    def test_body_mapping_with_trailing_white_spaces(
        self, default_invocation_request, default_context_variables
    ):
        mapper = HttpParametersMapper()
        request_parameters = {"append:header.test": "$request.body"}
        default_invocation_request["body"] = b"2 spaces  3 spaces   "

        mapping = mapper.map_http_integration_request(
            request_parameters=request_parameters,
            invocation_request=default_invocation_request,
            stage_variables={},
            context_variables=default_context_variables,
        )
        assert mapping == {
            "header": {
                "append": {"test": ["2 spaces  3 spaces"]},
                "overwrite": {},
                "remove": [],
            },
            "path": None,
            "querystring": {"append": {}, "overwrite": {}, "remove": []},
        }

    def test_json_body_mapping(self, default_invocation_request, default_context_variables):
        mapper = HttpParametersMapper()
        request_parameters = {"append:header.test": "$request.body.petstore.pets[0].name"}
        default_invocation_request["body"] = to_bytes(
            json.dumps(
                {
                    "petstore": {
                        "pets": [
                            {"name": "nested pet name value", "type": "Dog"},
                            {"name": "second nested value", "type": "Cat"},
                        ]
                    }
                }
            )
        )

        mapping = mapper.map_http_integration_request(
            request_parameters=request_parameters,
            invocation_request=default_invocation_request,
            stage_variables={},
            context_variables=default_context_variables,
        )
        assert mapping == {
            "header": {
                "append": {"test": ["nested pet name value"]},
                "overwrite": {},
                "remove": [],
            },
            "path": None,
            "querystring": {"append": {}, "overwrite": {}, "remove": []},
        }

    def test_json_body_mapping_not_found(
        self, default_invocation_request, default_context_variables
    ):
        mapper = HttpParametersMapper()
        request_parameters = {"append:header.test": "$request.body.petstore.pets[0].name"}
        default_invocation_request["body"] = to_bytes(
            json.dumps(
                {
                    "petstore": {
                        "pets": {
                            "name": "nested pet name value",
                            "type": "Dog",
                        }
                    }
                }
            )
        )

        mapping = mapper.map_http_integration_request(
            request_parameters=request_parameters,
            invocation_request=default_invocation_request,
            stage_variables={},
            context_variables=default_context_variables,
        )
        assert mapping == {
            "header": {"append": {}, "overwrite": {}, "remove": []},
            "path": None,
            "querystring": {"append": {}, "overwrite": {}, "remove": []},
        }

    def test_json_body_mapping_full(self, default_invocation_request, default_context_variables):
        mapper = HttpParametersMapper()
        request_parameters = {"append:header.test": "$request.body.petstore.pets[0]"}
        default_invocation_request["body"] = to_bytes(
            json.dumps(
                {
                    "petstore": {
                        "pets": [
                            {"name": "nested pet name value", "type": "Dog"},
                            {"name": "second nested value", "type": "Cat"},
                        ]
                    }
                }
            )
        )

        mapping = mapper.map_http_integration_request(
            request_parameters=request_parameters,
            invocation_request=default_invocation_request,
            stage_variables={},
            context_variables=default_context_variables,
        )
        assert mapping == {
            "header": {
                "append": {"test": ['{"name": "nested pet name value", "type": "Dog"}']},
                "overwrite": {},
                "remove": [],
            },
            "path": None,
            "querystring": {"append": {}, "overwrite": {}, "remove": []},
        }

    def test_json_invalid_body(self, default_invocation_request, default_context_variables):
        mapper = HttpParametersMapper()
        request_parameters = {"append:header.test": "$request.body.petstore.pets[0].name"}
        default_invocation_request["body"] = to_bytes("{not a json]}")

        mapping = mapper.map_http_integration_request(
            request_parameters=request_parameters,
            invocation_request=default_invocation_request,
            stage_variables={},
            context_variables=default_context_variables,
        )
        assert mapping == {
            "header": {"append": {}, "overwrite": {}, "remove": []},
            "path": None,
            "querystring": {"append": {}, "overwrite": {}, "remove": []},
        }

    def test_multiheaders_mapping(self, default_invocation_request, default_context_variables):
        mapper = HttpParametersMapper()
        request_parameters = {"append:header.test": "$request.header.testMultiHeader"}
        headers = {"testMultiHeader": ["test1", "test2"]}
        default_invocation_request["headers"] = Headers(headers)

        mapping = mapper.map_http_integration_request(
            request_parameters=request_parameters,
            invocation_request=default_invocation_request,
            stage_variables={},
            context_variables=default_context_variables,
        )
        assert mapping == {
            "header": {
                "append": {"test": ["test1,test2"]},
                "overwrite": {},
                "remove": [],
            },
            "path": None,
            "querystring": {"append": {}, "overwrite": {}, "remove": []},
        }

    def test_multiheaders_case_insensitive_mapping(
        self, default_invocation_request, default_context_variables
    ):
        mapper = HttpParametersMapper()
        request_parameters = {"append:header.test": "$request.header.testMultiHeader"}
        headers = {"testMultiHeader": ["test1"], "testMULTIHeader": ["test2"]}
        default_invocation_request["headers"] = Headers(headers)

        mapping = mapper.map_http_integration_request(
            request_parameters=request_parameters,
            invocation_request=default_invocation_request,
            stage_variables={},
            context_variables=default_context_variables,
        )
        assert mapping == {
            "header": {
                "append": {"test": ["test1,test2"]},
                "overwrite": {},
                "remove": [],
            },
            "path": None,
            "querystring": {"append": {}, "overwrite": {}, "remove": []},
        }

    def test_multi_qs_mapping(self, default_invocation_request, default_context_variables):
        mapper = HttpParametersMapper()
        request_parameters = {"append:header.test": "$request.querystring.testMultiQs"}
        default_invocation_request["query_string_parameters"] = {"testMultiQs": ["test1", "test2"]}

        mapping = mapper.map_http_integration_request(
            request_parameters=request_parameters,
            invocation_request=default_invocation_request,
            stage_variables={},
            context_variables=default_context_variables,
        )
        assert mapping == {
            "header": {
                "append": {"test": ["test1,test2"]},
                "overwrite": {},
                "remove": [],
            },
            "path": None,
            "querystring": {"append": {}, "overwrite": {}, "remove": []},
        }

    def request_mapping_path_parameter(self, default_invocation_request, default_context_variables):
        mapper = HttpParametersMapper()
        request_parameters = {"append:header.test": "$request.path.path_value"}

        mapping = mapper.map_http_integration_request(
            request_parameters=request_parameters,
            invocation_request=default_invocation_request,
            stage_variables={},
            context_variables=default_context_variables,
        )
        assert mapping == {
            "header": {"append": {["test"]}, "overwrite": {}, "remove": []},
            "path": None,
            "querystring": {"append": {}, "overwrite": {}, "remove": []},
        }

    def test_request_mapping_missing_request_values(self, default_context_variables):
        mapper = HttpParametersMapper()
        request_parameters = {
            "append:header.test": "$request.querystring.qs_value",
            "append:querystring.test": "$request.path.path_value",
            "append:path.test": "$request.header.header_value",
        }
        request = HttpInvocationRequest(
            headers=Headers(), query_string_parameters={}, path_parameters={}, body=b""
        )

        mapping = mapper.map_http_integration_request(
            request_parameters=request_parameters,
            invocation_request=request,
            stage_variables={},
            context_variables=default_context_variables,
        )
        assert mapping == {
            "header": {"append": {}, "overwrite": {}, "remove": []},
            "path": None,
            "querystring": {"append": {}, "overwrite": {}, "remove": []},
        }

    def test_request_mapping_space_separated_values(
        self, default_invocation_request, default_context_variables
    ):
        mapper = HttpParametersMapper()
        request_parameters = {
            "append:header.test": "$request.querystring.qs_value $request.header.header_value"
        }

        mapping = mapper.map_http_integration_request(
            request_parameters=request_parameters,
            invocation_request=default_invocation_request,
            stage_variables={},
            context_variables=default_context_variables,
        )
        assert mapping == {
            "header": {
                "append": {"test": ["test-qs-value test-header-value"]},
                "overwrite": {},
                "remove": [],
            },
            "path": None,
            "querystring": {"append": {}, "overwrite": {}, "remove": []},
        }

    def test_request_mapping_no_space_separated_values(
        self, default_invocation_request, default_context_variables
    ):
        mapper = HttpParametersMapper()
        request_parameters = {
            "append:header.test": "$request.querystring.qs_value$request.header.header_value"
        }

        mapping = mapper.map_http_integration_request(
            request_parameters=request_parameters,
            invocation_request=default_invocation_request,
            stage_variables={},
            context_variables=default_context_variables,
        )
        assert mapping == {
            "header": {
                "append": {"test": ["test-qs-valuetest-header-value"]},
                "overwrite": {},
                "remove": [],
            },
            "path": None,
            "querystring": {"append": {}, "overwrite": {}, "remove": []},
        }

    def test_request_space_separated_values_with_static(
        self, default_invocation_request, default_context_variables
    ):
        mapper = HttpParametersMapper()
        request_parameters = {
            "append:header.test": "$request.querystring.qs_value and some other stuff$request.header.header_value"
        }

        mapping = mapper.map_http_integration_request(
            request_parameters=request_parameters,
            invocation_request=default_invocation_request,
            stage_variables={},
            context_variables=default_context_variables,
        )
        assert mapping == {
            "header": {
                "append": {"test": ["test-qs-value and some other stufftest-header-value"]},
                "overwrite": {},
                "remove": [],
            },
            "path": None,
            "querystring": {"append": {}, "overwrite": {}, "remove": []},
        }

    def test_request_with_whitespace(self, default_invocation_request, default_context_variables):
        mapper = HttpParametersMapper()
        request_parameters = {"append:header.test": "$request.querystring.qs_value\t"}

        mapping = mapper.map_http_integration_request(
            request_parameters=request_parameters,
            invocation_request=default_invocation_request,
            stage_variables={},
            context_variables=default_context_variables,
        )
        assert mapping == {
            "header": {"append": {}, "overwrite": {}, "remove": []},
            "path": None,
            "querystring": {"append": {}, "overwrite": {}, "remove": []},
        }

    def test_request_space_separated_values_missing_first(
        self, default_invocation_request, default_context_variables
    ):
        mapper = HttpParametersMapper()
        request_parameters = {
            "append:header.test": "$request.querystring.missing $request.header.header_value"
        }

        mapping = mapper.map_http_integration_request(
            request_parameters=request_parameters,
            invocation_request=default_invocation_request,
            stage_variables={},
            context_variables=default_context_variables,
        )
        assert mapping == {
            "header": {"append": {}, "overwrite": {}, "remove": []},
            "path": None,
            "querystring": {"append": {}, "overwrite": {}, "remove": []},
        }

    def test_request_space_separated_values_missing_last(
        self, default_invocation_request, default_context_variables
    ):
        mapper = HttpParametersMapper()
        request_parameters = {
            "append:header.test": "$request.querystring.qs_value $request.header.missing"
        }

        mapping = mapper.map_http_integration_request(
            request_parameters=request_parameters,
            invocation_request=default_invocation_request,
            stage_variables={},
            context_variables=default_context_variables,
        )
        assert mapping == {
            "header": {"append": {}, "overwrite": {}, "remove": []},
            "path": None,
            "querystring": {"append": {}, "overwrite": {}, "remove": []},
        }

    def test_json_body_with_static_and_multi_headers(
        self, default_invocation_request, default_context_variables
    ):
        mapper = HttpParametersMapper()
        request_parameters = {
            "append:header.test": '$request.body.pets something "static"/${request.header.MultiHeader}continued text'
        }
        default_invocation_request["body"] = to_bytes(json.dumps({"pets": ["dog", "cat"]}))
        default_invocation_request["headers"] = Headers({"MultiHeader": ["header1", "header2"]})

        mapping = mapper.map_http_integration_request(
            request_parameters=request_parameters,
            invocation_request=default_invocation_request,
            stage_variables={},
            context_variables=default_context_variables,
        )
        assert mapping == {
            "header": {
                "append": {
                    "test": ['["dog", "cat"] something "static"/header1,header2continued text']
                },
                "overwrite": {},
                "remove": [],
            },
            "path": None,
            "querystring": {"append": {}, "overwrite": {}, "remove": []},
        }

    def test_multiple_destination_for_same_target(
        self, default_invocation_request, default_context_variables
    ):
        mapper = HttpParametersMapper()
        request_parameters = {
            "append:header.test": "$request.querystring.qs_value",
            "append:header.test.2": "$request.header.header_value",
        }

        mapping = mapper.map_http_integration_request(
            request_parameters=request_parameters,
            invocation_request=default_invocation_request,
            stage_variables={},
            context_variables=default_context_variables,
        )
        assert mapping == {
            "header": {
                "append": {"test": ["test-qs-value", "test-header-value"]},
                "overwrite": {},
                "remove": [],
            },
            "path": None,
            "querystring": {"append": {}, "overwrite": {}, "remove": []},
        }

    def test_length_less_than_2_is_static(
        self, default_invocation_request, default_context_variables
    ):
        mapper = HttpParametersMapper()
        request_parameters = {"append:header.test": "$request.querystring.qs_value$1"}

        mapping = mapper.map_http_integration_request(
            request_parameters=request_parameters,
            invocation_request=default_invocation_request,
            stage_variables={},
            context_variables=default_context_variables,
        )
        assert mapping == {
            "header": {"append": {"test": ["test-qs-value$1"]}, "overwrite": {}, "remove": []},
            "path": None,
            "querystring": {"append": {}, "overwrite": {}, "remove": []},
        }

    def test_extra_curly_in_dynamic_block(
        self, default_invocation_request, default_context_variables
    ):
        mapper = HttpParametersMapper()
        request_parameters = {"append:header.test": "${request.querystring.qs_value{}"}

        mapping = mapper.map_http_integration_request(
            request_parameters=request_parameters,
            invocation_request=default_invocation_request,
            stage_variables={},
            context_variables=default_context_variables,
        )
        assert mapping == {
            "header": {"append": {}, "overwrite": {}, "remove": []},
            "path": None,
            "querystring": {"append": {}, "overwrite": {}, "remove": []},
        }


class TestApigatewayHttpResponseParametersMapping:
    def test_sources(
        self, default_invocation_request, default_endpoint_response, default_context_variables
    ):
        mapper = HttpParametersMapper()
        response_parameters = {
            "append:header.header_value": "$response.header.test",
            "append:header.body": "$response.body",
            "append:header.api_id": "$context.apiId",
            "append:header.body_json_path": "$response.body.test",
            "append:header.stage_var": "$stageVariables.my_var",
        }

        default_endpoint_response["body"] = b'{"test":"body_value"}'
        default_endpoint_response["headers"].set("test", "test_header")
        mapping = mapper.map_http_integration_response(
            response_parameters=response_parameters,
            integration_response=default_endpoint_response,
            context_variables=default_context_variables,
            stage_variables={"my_var": "stage var value"},
        )
        assert mapping == {
            "header": {
                "append": {
                    "header_value": ["test_header"],
                    "body": ['{"test":"body_value"}'],
                    "api_id": [TEST_API_ID],
                    "body_json_path": ["body_value"],
                    "stage_var": ["stage var value"],
                },
                "overwrite": {},
                "remove": [],
            },
            "statuscode": "",
        }

    def test_status_code(
        self, default_invocation_request, default_endpoint_response, default_context_variables
    ):
        mapper = HttpParametersMapper()
        response_parameters = {"overwrite:statuscode": "$response.header.status"}

        default_endpoint_response["headers"].set("status", "200")
        mapping = mapper.map_http_integration_response(
            response_parameters=response_parameters,
            integration_response=default_endpoint_response,
            context_variables=default_context_variables,
            stage_variables={},
        )
        assert mapping == {
            "header": {"append": {}, "overwrite": {}, "remove": []},
            "statuscode": "200",
        }

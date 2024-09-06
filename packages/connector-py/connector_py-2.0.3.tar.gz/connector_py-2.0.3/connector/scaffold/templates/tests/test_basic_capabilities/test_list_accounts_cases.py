"""Cases for testing ``list_accounts`` operation."""

import typing as t

import httpx
from connector.serializers.request import (
    ListAccountsRequest,
    Request,
)
from connector.serializers.response import (
    EncounteredErrorResponse,
    ListAccountsResponse,
    PaginationData,
    Response,
)
from connector.utils.test import http_error_message

from {name}.integration import BASE_URL
from tests.conftest import INVALID_AUTH, VALID_AUTH
from tests.type_definitions import MockedResponse, ResponseBodyMap

TestCase: t.TypeAlias = tuple[
    Request[ListAccountsRequest],
    ResponseBodyMap,
    Response[ListAccountsResponse] | Response[EncounteredErrorResponse],
]


def case_list_accounts_200() -> TestCase:
    """Successful request."""
    args = Request(
        request=ListAccountsRequest(),
        auth=VALID_AUTH,
    )
    response_body_map = {{
        "GET": {{
            "/users?limit=5&offset=0": MockedResponse(
                status_code=httpx.codes.OK,
                response_body={{}},
            ),
        }},
    }}
    expected_response = Response(
        response=ListAccountsResponse(
            accounts=[],
        ),
        raw_data=None,
        page=PaginationData(
            token="9182a8656e64706f696e74a62f7573657273a66f666673657400",
            size=5,
        ),
    )
    return args, response_body_map, expected_response


def case_list_accounts_200_no_accounts() -> TestCase:
    """No accounts found."""
    args = Request(
        request=ListAccountsRequest(),
        auth=VALID_AUTH,
    )
    response_body_map = {{
        "GET": {{
            "/users?limit=5&offset=0": MockedResponse(
                status_code=httpx.codes.OK,
                response_body={{}},
            ),
        }},
    }}
    expected_response = Response(
        response=ListAccountsResponse(
            accounts=[],
        ),
        raw_data=None,
        page=PaginationData(
            token="9182a8656e64706f696e74a62f7573657273a66f666673657400",
            size=5,
        ),
    )
    return args, response_body_map, expected_response


def case_list_accounts_401() -> TestCase:
    """Unauthorized request should fail."""
    args = Request(
        request=ListAccountsRequest(),
        auth=INVALID_AUTH,
    )
    response_body_map = {{
        "GET": {{
            "/users?limit=5&offset=0": MockedResponse(
                status_code=httpx.codes.UNAUTHORIZED,
                response_body={{}},
            ),
        }},
    }}
    expected_response = Response(
        response=EncounteredErrorResponse(
            message=http_error_message(
                f"{{BASE_URL}}/users?limit=5&offset=0",
                httpx.codes.UNAUTHORIZED,
            ),
            status_code=httpx.codes.UNAUTHORIZED,
            error_code="{hyphenated_name}.unauthorized",
            raised_by="HTTPStatusError",
            raised_in="{name}.integration:list_accounts",
        ),
    )
    return args, response_body_map, expected_response

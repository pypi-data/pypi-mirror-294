"""Cases for testing ``delete_account`` operation."""

import typing as t

import httpx
from connector.serializers.request import (
    DeleteAccountRequest,
    Request,
)
from connector.serializers.response import (
    DeleteAccountResponse,
    EncounteredErrorResponse,
    Response,
)
from connector.utils.test import http_error_message

from {name}.integration import BASE_URL
from tests.conftest import INVALID_AUTH, VALID_AUTH
from tests.type_definitions import MockedResponse, ResponseBodyMap

TestCase: t.TypeAlias = tuple[
    Request[DeleteAccountRequest],
    ResponseBodyMap,
    Response[DeleteAccountResponse] | Response[EncounteredErrorResponse],
]


def case_delete_account_204() -> TestCase:
    """Successful deletion request."""
    args = Request[DeleteAccountRequest](
        request=DeleteAccountRequest(
            account_id="1",
        ),
        auth=VALID_AUTH,
        include_raw_data=True,
    )
    response_body_map = {{
        "DELETE": {{
            f"/users/{{args.request.account_id}}": MockedResponse(
                status_code=httpx.codes.NO_CONTENT,
                response_body=None,
            ),
        }},
    }}
    expected_response = Response[DeleteAccountResponse](
        response=DeleteAccountResponse(deleted=True),
        raw_data={{
            f"{{BASE_URL}}/users/{{args.request.account_id}}": None,
        }},
    )
    return args, response_body_map, expected_response


def case_delete_account_404() -> TestCase:
    """Not found request should fail."""
    args = Request[DeleteAccountRequest](
        request=DeleteAccountRequest(
            account_id="non_existent",
        ),
        auth=VALID_AUTH,
    )
    response_body_map = {{
        "DELETE": {{
            f"/users/{{args.request.account_id}}": MockedResponse(
                status_code=httpx.codes.NOT_FOUND,
                response_body={{
                    "error": {{
                        "message": "Not found",
                        "code": 2100,
                    }},
                }},
            ),
        }},
    }}
    expected_response = Response[EncounteredErrorResponse](
        response=EncounteredErrorResponse(
            message=http_error_message(
                f"{{BASE_URL}}/users/{{args.request.account_id}}",
                httpx.codes.NOT_FOUND,
            ),
            status_code=httpx.codes.NOT_FOUND,
            error_code="{hyphenated_name}.not_found",
            raised_by="HTTPStatusError",
            raised_in="{name}.integration:delete_account",
        ),
    )
    return args, response_body_map, expected_response


def case_delete_account_401() -> TestCase:
    """Unauthorized request should fail."""
    args = Request[DeleteAccountRequest](
        request=DeleteAccountRequest(
            account_id="1",
        ),
        auth=INVALID_AUTH,
    )
    response_body_map = {{
        "DELETE": {{
            f"/users/{{args.request.account_id}}": MockedResponse(
                status_code=httpx.codes.UNAUTHORIZED,
                response_body=None,
            ),
        }},
    }}
    expected_response = Response[EncounteredErrorResponse](
        response=EncounteredErrorResponse(
            message=http_error_message(
                f"{{BASE_URL}}/users/{{args.request.account_id}}",
                httpx.codes.UNAUTHORIZED,
            ),
            status_code=httpx.codes.UNAUTHORIZED,
            error_code="{hyphenated_name}.unauthorized",
            raised_by="HTTPStatusError",
            raised_in="{name}.integration:delete_account",
        ),
    )
    return args, response_body_map, expected_response

"""Cases for testing ``validate_credentials`` operation."""

import typing as t

import httpx
from connector.serializers.request import (
    Request,
    ValidateCredentialsRequest,
)
from connector.serializers.response import (
    EncounteredErrorResponse,
    Response,
    ValidateCredentialsResponse,
)
from connector.utils.test import http_error_message

from {name}.integration import BASE_URL
from tests.conftest import INVALID_AUTH, VALID_AUTH
from tests.type_definitions import MockedResponse, ResponseBodyMap

TestCase: t.TypeAlias = tuple[
    Request[ValidateCredentialsRequest],
    ResponseBodyMap,
    Response[ValidateCredentialsResponse] | Response[EncounteredErrorResponse],
]


def case_validate_credentials_200() -> TestCase:
    """Successful request."""
    args = Request(
        request=ValidateCredentialsRequest(),
        auth=VALID_AUTH,
    )
    response_body_map = {{
        "GET": {{
            "/users?limit=1": MockedResponse(
                status_code=httpx.codes.OK,
                response_body={{}},
            )
        }}
    }}
    expected_response = Response(
        response=ValidateCredentialsResponse(valid=True),
        raw_data=None,
    )
    return args, response_body_map, expected_response


def case_validate_credentials_401() -> TestCase:
    """Unauthorized request should fail."""

    args = Request(
        request=ValidateCredentialsRequest(),
        auth=INVALID_AUTH,
    )
    response_body_map = {{
        "GET": {{
            "/users?limit=1": MockedResponse(
                status_code=httpx.codes.UNAUTHORIZED,
                response_body={{}},
            )
        }}
    }}
    expected_response = Response(
        response=EncounteredErrorResponse(
            message=http_error_message(
                f"{{BASE_URL}}/users?limit=1",
                401,
            ),
            status_code=httpx.codes.UNAUTHORIZED,
            error_code=f"{hyphenated_name}.unauthorized",
            raised_by="HTTPStatusError",
            raised_in=f"{name}.integration:validate_credentials",
        )
    )
    return args, response_body_map, expected_response

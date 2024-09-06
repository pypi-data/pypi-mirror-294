"""Cases for testing ``list_entitlements`` operation."""

import typing as t

import httpx
from connector.serializers.request import (
    ListEntitlementsRequest,
    PaginationArgs,
    Request,
)
from connector.serializers.response import (
    EncounteredErrorResponse,
    ListEntitlementsResponse,
    Response,
)
from connector.utils.test import http_error_message

from tests.conftest import INVALID_AUTH, VALID_AUTH
from tests.type_definitions import MockedResponse, ResponseBodyMap

TestCase: t.TypeAlias = tuple[
    Request[ListEntitlementsRequest],
    ResponseBodyMap,
    Response[ListEntitlementsResponse] | Response[EncounteredErrorResponse],
]


def case_list_entitlements_200() -> TestCase:
    """Successful request."""
    args = Request(
        request=ListEntitlementsRequest(
            resource_type="",
            resource_integration_specific_id="",
        ),
        auth=VALID_AUTH,
        page=PaginationArgs(
            size=5,
        ),
    )
    response_body_map = {{
        "GET": {{
            "/example": MockedResponse(
                status_code=httpx.codes.OK,
                response_body={{}},
            ),
        }},
    }}
    expected_response = Response(
        response=ListEntitlementsResponse(
            entitlements=[],
        ),
        raw_data={{}},
    )
    return args, response_body_map, expected_response


INVALID_ARGS = Request[ListEntitlementsRequest](
    request=ListEntitlementsRequest(
        resource_type="",
        resource_integration_specific_id="",
    ),
    auth=INVALID_AUTH,
    page=PaginationArgs(
        size=5,
    ),
)


def case_list_entitlements_401() -> TestCase:
    """Unauthorized request should fail."""
    response_body_map = {{
        "GET": {{
            "/example": MockedResponse(
                status_code=httpx.codes.UNAUTHORIZED,
                response_body={{}},
            ),
        }},
    }}

    expected_response = Response(
        response=EncounteredErrorResponse(
            message=http_error_message(
                "",
                401,
            ),
            status_code=httpx.codes.UNAUTHORIZED,
            error_code="{name}.unauthorized",
            raised_by="HTTPStatusError",
            raised_in="{name}.integration:list_entitlements",
        ),
        raw_data=None,
    )

    return INVALID_ARGS, response_body_map, expected_response


def case_list_entitlements_400() -> TestCase:
    """Bad request should fail."""

    response_body_map = {{
        "GET": {{
            "/example": MockedResponse(
                status_code=httpx.codes.BAD_REQUEST,
                response_body={{}},
            ),
        }},
    }}

    expected_response = Response(
        response=EncounteredErrorResponse(
            message=http_error_message(
                "",
                400,
            ),
            status_code=httpx.codes.BAD_REQUEST,
            error_code="{name}.bad_request",
            raised_by="HTTPStatusError",
            raised_in="{name}.integration:list_entitlements",
        ),
        raw_data=None,
    )

    return INVALID_ARGS, response_body_map, expected_response

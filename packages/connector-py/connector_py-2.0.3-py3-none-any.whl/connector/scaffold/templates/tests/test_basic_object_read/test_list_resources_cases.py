"""Cases for testing ``list_resources`` operation."""

import typing as t

import httpx
from connector.serializers.request import (
    ListResourcesRequest,
    Request,
)
from connector.serializers.response import (
    EncounteredErrorResponse,
    ListResourcesResponse,
    Response,
)
from connector.utils.test import http_error_message

from tests.conftest import INVALID_AUTH, VALID_AUTH
from tests.type_definitions import MockedResponse, ResponseBodyMap

TestCase: t.TypeAlias = tuple[
    Request[ListResourcesRequest],
    ResponseBodyMap,
    Response[ListResourcesResponse] | Response[EncounteredErrorResponse],
]


def case_list_resources_200() -> TestCase:
    """Successful request."""
    args = Request(
        request=ListResourcesRequest(
            resource_type="",
        ),
        auth=VALID_AUTH,
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
        response=ListResourcesResponse(
            resources=[],
        ),
        raw_data={{}},
    )
    return args, response_body_map, expected_response


def case_list_resources_401() -> TestCase:
    """Unauthorized request should fail."""
    args = Request(
        request=ListResourcesRequest(
            resource_type="",
        ),
        auth=INVALID_AUTH,
    )

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
            error_code=f"{hyphenated_name}.unauthorized",
            raised_by="HTTPStatusError",
            raised_in=f"{name}.integration:list_resources",
        )
    )

    return args, response_body_map, expected_response

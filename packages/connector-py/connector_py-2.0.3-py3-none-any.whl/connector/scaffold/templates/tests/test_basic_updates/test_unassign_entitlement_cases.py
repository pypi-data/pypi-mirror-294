"""Cases for testing ``unassign_entitlement`` operation."""

import typing as t

import httpx
from connector.serializers.request import (
    Request,
    UnassignEntitlementRequest,
)
from connector.serializers.response import (
    EncounteredErrorResponse,
    Response,
    UnassignEntitlementResponse,
)
from connector.utils.test import http_error_message
from tests.conftest import INVALID_AUTH, VALID_AUTH
from tests.type_definitions import ResponseBodyMap, MockedResponse

TestCase: t.TypeAlias = tuple[
    Request[UnassignEntitlementRequest],
    ResponseBodyMap,
    Response[UnassignEntitlementResponse] | Response[EncounteredErrorResponse],
]

# repeat following casess for all entitlements

def case_unassign_entitlement_1_401() -> TestCase:
    """Unauthorized request should fail."""
    args = Request(
        request=UnassignEntitlementRequest(
            account_integration_specific_id="",
            resource_integration_specific_id="",
            resource_type="",
            entitlement_integration_specific_id="",
            entitlement_type="",
        ),
        auth=INVALID_AUTH,
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
        response=EncounteredErrorResponse(
            message=http_error_message(
                "",
                401,
            ),
            status_code=httpx.codes.UNAUTHORIZED,
            error_code="{hyphenated_name}.unauthorized",
            raised_by="HTTPStatusError",
            raised_in="{name}.integration:unassign_entitlement",
        ),
        raw_data={{}},
    )
    return args, response_body_map, expected_response


def case_assign_entitlement_1_404() -> TestCase:
    """Authorized request for non-existing entitlement should fail."""
    args = Request(
        request=UnassignEntitlementRequest(
            account_integration_specific_id="",
            resource_integration_specific_id="",
            resource_type="",
            entitlement_integration_specific_id="",
            entitlement_type="",
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
        response=EncounteredErrorResponse(
            message=http_error_message(
                "",
                404,
            ),
            status_code=httpx.codes.NOT_FOUND,
            error_code="{hyphenated_name}.not_found",
            raised_by="HTTPStatusError",
            raised_in="{name}.integration:unassign_entitlement",
        ),
        raw_data={{}},
    )
    return args, response_body_map, expected_response


def case_unassign_entitlement_1_200() -> TestCase:
    """Successfully unassign entitlement."""
    args = Request(
        request=UnassignEntitlementRequest(
            account_integration_specific_id="",
            resource_integration_specific_id="",
            resource_type="",
            entitlement_integration_specific_id="",
            entitlement_type="",
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
        response=UnassignEntitlementResponse(unassigned=True),
        raw_data=None,
    )
    return args, response_body_map, expected_response

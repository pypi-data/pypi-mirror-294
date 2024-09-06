"""Cases for testing ``assign_entitlement`` operation."""
import copy
import typing as t

import httpx
from connector.serializers.request import (
    AssignEntitlementRequest,
    Request,
)
from connector.serializers.response import (
    AssignEntitlementResponse,
    EncounteredErrorResponse,
    Response,
)
from connector.utils.test import http_error_message

from tests.conftest import INVALID_AUTH, VALID_AUTH
from tests.type_definitions import MockedResponse, ResponseBodyMap

TestCase: t.TypeAlias = tuple[
    Request[AssignEntitlementRequest],
    ResponseBodyMap,
    Response[AssignEntitlementResponse] | Response[EncounteredErrorResponse],
]

VALID_ASSIGN_REQUEST = Request[AssignEntitlementRequest](
    request=AssignEntitlementRequest(
        account_integration_specific_id="",
        resource_integration_specific_id="",
        resource_type="",
        entitlement_integration_specific_id="",
        entitlement_type="",
    ),
    auth=VALID_AUTH,
)
INVALID_ASSIGN_REQUEST = Request[AssignEntitlementRequest](
    request=AssignEntitlementRequest(
        account_integration_specific_id="",
        resource_integration_specific_id="",
        resource_type="",
        entitlement_integration_specific_id="",
        entitlement_type="",
    ),
    auth=INVALID_AUTH,
)

# repeat following cases for all entitlements
def case_assign_entitlement_1_401() -> TestCase:
    """Unauthorized request should fail."""
    args = INVALID_ASSIGN_REQUEST
    response_body_map ={{
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
            error_code="{hyphenated_name}.unauthorized",
            raised_by="HTTPStatusError",
            raised_in="{name}.integration:assign_entitlement",
        ),
        raw_data={{}},
    )
    return args, response_body_map, expected_response


def case_assign_entitlement_1_404() -> TestCase:
    """Authorized request for non-existing entitlement should fail."""
    args = VALID_ASSIGN_REQUEST
    response_body_map ={{
        "GET": {{
            "/example": MockedResponse(
                status_code=httpx.codes.NOT_FOUND,
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
    )
    return args, response_body_map, expected_response


def case_assign_entitlement_1_400() -> TestCase:
    """Authorized bad request should fail."""
    args = VALID_ASSIGN_REQUEST
    response_body_map ={{
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
            error_code="{hyphenated_name}.bad_request",
            raised_by="HTTPStatusError",
            raised_in="{name}.integration:unassign_entitlement",
        ),
    )
    return args, response_body_map, expected_response


def case_assign_entitlement_1_200() -> TestCase:
    """Succeed with changing entitlement."""
    args = VALID_ASSIGN_REQUEST
    response_body_map ={{
        "GET": {{
            "/example": MockedResponse(
                status_code=httpx.codes.OK,
                response_body={{}},
            ),
        }},
    }}
    expected_response = Response(
        response=AssignEntitlementResponse(assigned=True),
        raw_data=None,
    )
    return args, response_body_map, expected_response

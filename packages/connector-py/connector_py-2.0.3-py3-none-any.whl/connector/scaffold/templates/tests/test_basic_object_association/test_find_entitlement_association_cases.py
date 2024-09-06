"""Cases for testing ``test_find_entitlement_associations`` operation."""
import typing as t

import httpx
from connector.serializers.request import (
    FindEntitlementAssociationsRequest,
    Request,
)
from connector.serializers.response import (
    EncounteredErrorResponse,
    FindEntitlementAssociationsResponse,
    Response,
)
from connector.utils.test import http_error_message

from {name}.integration import BASE_URL
from tests.conftest import INVALID_AUTH, VALID_AUTH
from tests.type_definitions import MockedResponse, ResponseBodyMap

TestCase: t.TypeAlias = tuple[
    Request[FindEntitlementAssociationsRequest],
    ResponseBodyMap,
    Response[FindEntitlementAssociationsResponse] | Response[EncounteredErrorResponse],
]

# repeat following cases for all resource types
def case_find_entitlement_associations_1_401() -> TestCase:
    """Unauthorized request should fail."""
    args = Request(
        request=FindEntitlementAssociationsRequest(
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
                f"{{BASE_URL}}/",
                401,
            ),
            status_code=httpx.codes.UNAUTHORIZED,
            error_code="{hyphenated_name}.unauthorized",
            raised_by="HTTPStatusError",
            raised_in="{name}.integration:find_entitlement_associations",
        ),
        raw_data={{}},
    )
    return args, response_body_map, expected_response


def case_find_entitlement_associations_1_404() -> TestCase:
    """Authorized request for non-existing entitlement should fail."""
    args = Request(
        request=FindEntitlementAssociationsRequest(),
        auth=VALID_AUTH,
    )
    response_body_map = {{
        "GET": {{
            "/": MockedResponse(
                status_code=httpx.codes.NOT_FOUND,
                response_body={{}},
            ),
        }},
    }}
    expected_response = Response(
        response=EncounteredErrorResponse(
            message=http_error_message(
                f"{{BASE_URL}}/",
                404,
            ),
            status_code=httpx.codes.NOT_FOUND,
            error_code="{hyphenated_name}.not_found",
            raised_by="HTTPStatusError",
            raised_in="{name}.integration:find_entitlement_associations",
        ),
        raw_data={{}},
    )
    return args, response_body_map, expected_response



def case_find_entitlement_associations_1_200() -> TestCase:
    """Succeed with finding entitlement associations."""
    args = Request(
        request=FindEntitlementAssociationsRequest(),
        auth=VALID_AUTH,
    )
    response_body_map = {{
        "GET": {{
            "/": MockedResponse(
                status_code=httpx.codes.OK,
                response_body={{}},
            ),
        }},
    }}
    expected_response = Response(
        response=FindEntitlementAssociationsResponse(associations=[]),
        raw_data={{}},
    )
    return args, response_body_map, expected_response


def case_find_entitlement_associations_1_empty_200() -> TestCase:
    """Succeed with getting empty entitlement associations."""
    args = Request(
        request=FindEntitlementAssociationsRequest(),
        auth=VALID_AUTH,
    )
    response_body_map = {{
        "GET": {{
            "/": MockedResponse(
                status_code=httpx.codes.OK,
                response_body={{}},
            ),
        }},
    }}
    expected_response = Response(
        response=FindEntitlementAssociationsResponse(
            associations=[],
        ),
        raw_data={{}},
    )
    return args, response_body_map, expected_response

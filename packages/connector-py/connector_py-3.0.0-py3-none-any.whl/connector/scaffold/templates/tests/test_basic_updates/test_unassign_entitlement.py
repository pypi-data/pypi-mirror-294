import pytest
import pytest_cases
from connector.capability import CapabilityName
from connector.serializers.request import (
    Request,
    UnassignEntitlementRequest,
)
from connector.serializers.response import (
    Response,
    UnassignEntitlementResponse,
)
from {name}.integration import integration

from tests.type_definitions import ClientContextManager, ResponseBodyMap

@pytest.mark.skip(reason="Function not implemented yet, remove after implementation of tested function.")
@pytest_cases.parametrize_with_cases(
    ["args", "response_body_map", "expected_response"],
    cases=[
        "tests.test_basic_updates.test_unassign_entitlement_cases",
    ],
)
def test_validate_unassign_entitlement(
    httpx_async_client: ClientContextManager,
    args: Request[UnassignEntitlementRequest],
    response_body_map: ResponseBodyMap,
    expected_response: Response[UnassignEntitlementResponse],
) -> None:
    """Test ``unassign-entitlement`` operation."""
    with httpx_async_client(args.get_oauth().access_token, response_body_map):
        response = integration.dispatch(CapabilityName.UNASSIGN_ENTITLEMENT, args.model_dump_json())

    assert response == expected_response.model_dump_json()

import pytest_cases
from connector.capability import CapabilityName
from connector.serializers.request import (
    ListAccountsRequest,
    Request,
)
from connector.serializers.response import (
    EncounteredErrorResponse,
    ListAccountsResponse,
    Response,
)
from {name}.integration import integration

from tests.type_definitions import ClientContextManager, ResponseBodyMap


@pytest_cases.parametrize_with_cases(
    ["args", "response_body_map", "expected_response"],
    cases=[
        "tests.test_basic_capabilities.test_list_accounts_cases",
    ],
)
def test_list_accounts(
    httpx_async_client: ClientContextManager,
    args: Request[ListAccountsRequest],
    response_body_map: ResponseBodyMap,
    expected_response: Response[ListAccountsResponse] | Response[EncounteredErrorResponse],
) -> None:
    with httpx_async_client(args.get_oauth().access_token, response_body_map):
        response = integration.dispatch(CapabilityName.LIST_ACCOUNTS, args.model_dump_json())

    assert response == expected_response.model_dump_json()

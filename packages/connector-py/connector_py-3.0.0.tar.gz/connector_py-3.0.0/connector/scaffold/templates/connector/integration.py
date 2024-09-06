import httpx
from connector.capability import CapabilityName
from connector.errors import HTTPHandler
from connector.integration import Integration
from connector.serializers.request import (
    ActivateAccountRequest,
    AssignEntitlementRequest,
    CreateAccountRequest,
    DeactivateAccountRequest,
    DeleteAccountRequest,
    FindEntitlementAssociationsRequest,
    ListAccountsRequest,
    ListCustomAttributesSchemaRequest,
    ListEntitlementsRequest,
    ListResourcesRequest,
    Request,
    RequestData,
    UnassignEntitlementRequest,
    ValidateCredentialsRequest,
)
from connector.serializers.response import (
    ActivateAccountResponse,
    AssignEntitlementResponse,
    CreateAccountResponse,
    DeactivateAccountResponse,
    DeleteAccountResponse,
    FindEntitlementAssociationsResponse,
    FoundAccountData,
    ListAccountsResponse,
    ListCustomAttributesSchemaResponse,
    ListEntitlementsResponse,
    ListResourcesResponse,
    PaginationData,
    Response,
    UnassignEntitlementResponse,
    ValidateCredentialsResponse,
)
from {name}.auth import Auth
from {name}.serializers.pagination import DEFAULT_PAGE_SIZE, NextPageToken, Pagination

BASE_URL = "https://scaffold.com"


def build_client(request: Request[RequestData]) -> httpx.AsyncClient:
    """Prepare client contenxt manager for calling PagerDuty API."""
    return httpx.AsyncClient(
        auth=Auth(access_token=request.get_oauth().access_token),
        base_url=BASE_URL,
    )


integration = Integration(
    app_id="{hyphenated_name}",
    auth=None,
    exception_handlers=[
        (httpx.HTTPStatusError, HTTPHandler, None),
    ],
)

@integration.register_capability(CapabilityName.VALIDATE_CREDENTIALS)
async def validate_credentials(
    args: Request[ValidateCredentialsRequest],
) -> Response[ValidateCredentialsResponse]:
    async with build_client(args) as client:
        r = await client.get("/users", params={{"limit": 1}})
        r.raise_for_status()
        data = r.json()

    return Response(
        response=ValidateCredentialsResponse(valid=True),
        raw_data={{
            f"{{BASE_URL}}/users?limit=1": data,
        }}
        if args.include_raw_data
        else None,
    )

@integration.register_capability(CapabilityName.LIST_ACCOUNTS)
async def list_accounts(args: Request[ListAccountsRequest]) -> Response[ListAccountsResponse]:
    endpoint = "/users"
    try:
        current_pagination = NextPageToken(args.pagination_token).paginations()[0]
    except IndexError:
        current_pagination = Pagination.default(endpoint)

    page_size = args.pagination_size or DEFAULT_PAGE_SIZE
    async with build_client(args) as client:
        r = await client.get(
            endpoint,
            params={{"limit": page_size, "offset": current_pagination.offset}},
        )
        r.raise_for_status()
        data = r.json()
        accounts = []

        if True:
            next_pagination = [
                Pagination(
                    endpoint=endpoint,
                    offset=current_pagination.offset + len(accounts),
                )
            ]
        else:
            next_pagination = []

        next_page_token = NextPageToken.from_paginations(next_pagination).token

    return Response(
        response=ListAccountsResponse(
            accounts=accounts,
        ),
        raw_data = {{
            f"{{BASE_URL}}/users?limit=1": data,
        }} if args.include_raw_data else None,
        page=PaginationData(
            token=next_page_token,
            size=page_size,
        )
        if next_page_token
        else None,
    )

# @integration.register_capability(CapabilityName.LIST_RESOURCES)
async def list_resources(args: Request[ListResourcesRequest]) -> Response[ListResourcesResponse]:
    raise NotImplementedError

# @integration.register_capability(CapabilityName.LIST_ENTITLEMENTS)
async def list_entitlements(
    args: Response[ListEntitlementsRequest],
) -> Response[ListEntitlementsResponse]:
    raise NotImplementedError

# @integration.register_capability(CapabilityName.FIND_ENTITLEMENT_ASSOCIATIONS)
async def find_entitlement_associations(
    args: Request[FindEntitlementAssociationsRequest],
) -> Response[FindEntitlementAssociationsResponse]:
    raise NotImplementedError

# @integration.register_capability(CapabilityName.ASSIGN_ENTITLEMENT)
async def assign_entitlement(args: AssignEntitlementRequest) -> Response[AssignEntitlementResponse]:
    raise NotImplementedError

# @integration.register_capability(CapabilityName.UNASSIGN_ENTITLEMENT)
async def unassign_entitlement(args: UnassignEntitlementRequest) -> Response[UnassignEntitlementResponse]:
    raise NotImplementedError

# @integration.register_capability(CapabilityName.LIST_CUSTOM_ATTRIBUTES_SCHEMA)
async def list_custom_attributes_schema(args: Request[ListCustomAttributesSchemaRequest]) -> Response[ListCustomAttributesSchemaResponse]:
    raise NotImplementedError


# @integration.register_capability(CapabilityName.CREATE_ACCOUNT)
async def create_account(
    args: Request[CreateAccountRequest],
) -> Response[CreateAccountResponse]:
    raise NotImplementedError


# @integration.register_capability(CapabilityName.DELETE_ACCOUNT)
async def delete_account(
    args: Request[DeleteAccountRequest],
) -> Response[DeleteAccountResponse]:
    raise NotImplementedError


# @integration.register_capability(CapabilityName.ACTIVATE_ACCOUNT)
async def activate_account(
    args: Request[ActivateAccountRequest],
) -> Response[ActivateAccountResponse]:
    raise NotImplementedError


# @integration.register_capability(CapabilityName.DEACTIVATE_ACCOUNT)
async def deactivate_account(
    args: Request[DeactivateAccountRequest],
) -> Response[DeactivateAccountResponse]:
    raise NotImplementedError

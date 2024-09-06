"""Cases for testing ``create_account`` operation."""

import typing as t

import httpx
from connector.serializers.request import (
    CreateAccount,
    CreateAccountEntitlement,
    CreateAccountRequest,
    Request,
)
from connector.serializers.response import (
    CreateAccountResponse,
    EncounteredErrorResponse,
    Response,
)
from connector.utils.test import http_error_message

from {name}.integration import BASE_URL
from tests.conftest import INVALID_AUTH, VALID_AUTH
from tests.type_definitions import MockedResponse, ResponseBodyMap

TestCase: t.TypeAlias = tuple[
    Request[CreateAccountRequest],
    ResponseBodyMap,
    Response[CreateAccountResponse] | Response[EncounteredErrorResponse],
]


def case_create_account_201() -> TestCase:
    """Successful creation request."""
    args = Request[CreateAccountRequest](
        request=CreateAccountRequest(
            account=CreateAccount(
                email="jw7rT@example.com",
                given_name="John",
                family_name="Doe",
            ),
            entitlements=[
                CreateAccountEntitlement(
                    integration_specific_id="read_only_user",
                    integration_specific_resource_id="dev-lumos",
                    entitlement_type="role",
                ),
                CreateAccountEntitlement(
                    integration_specific_id="license-1",
                    integration_specific_resource_id="dev-lumos",
                    entitlement_type="license",
                ),
            ],
        ),
        auth=VALID_AUTH,
        include_raw_data=True,
    )
    user_id = "1"
    response_body = {{
        "user": {{
            "id": user_id,
            "email": args.request.account.email,
            "name": f"{{args.request.account.given_name}} {{args.request.account.family_name}}",
            "html_url": f"https://dev-lumos.pagerduty.com/users/{{user_id}}",
            "role": args.request.entitlements[0].integration_specific_id,
            "license": {{"id": args.request.entitlements[1].integration_specific_id}},
        }},
    }}
    response_body_map = {{
        "POST": {{
            "/users": MockedResponse(
                status_code=httpx.codes.CREATED,
                response_body=response_body,
            ),
         }},
     }}
    expected_response = Response[CreateAccountResponse](
        response=CreateAccountResponse(created=True),
        raw_data={{
            f"{{BASE_URL}}/": response_body,
        }},
    )
    return args, response_body_map, expected_response


def case_create_account_400_missing_email() -> TestCase:
    """Invalid request when creating an account without user email."""
    args = Request[CreateAccountRequest](
        request=CreateAccountRequest(
            account=CreateAccount(),
            entitlements=[],
        ),
        auth=VALID_AUTH,
    )
    response_body_map ={{
        "POST": {{
            "/users": MockedResponse(
                status_code=httpx.codes.BAD_REQUEST,
                response_body={{}},
            ),
        }},
    }}
    expected_response = Response[EncounteredErrorResponse](
        response=EncounteredErrorResponse(
            message="Email is required, provide 'email' in account data",
            error_code="{hyphenated_name}.bad_request",
            raised_by="ConnectorError",
            raised_in="{name}.integration:create_account",
        ),
        raw_data=None,
    )
    return args, response_body_map, expected_response


def case_create_account_400_missing_name() -> TestCase:
    """Invalid request when creating an account without user given and family names."""
    args = Request[CreateAccountRequest](
        request=CreateAccountRequest(
            account=CreateAccount(email="jw7rT@example.com"),
            entitlements=[],
        ),
        auth=VALID_AUTH,
    )
    response_body_map ={{
        "POST": {{
            "/users": MockedResponse(
                status_code=httpx.codes.BAD_REQUEST,
                response_body={{}},
            ),
        }},
    }}
    expected_response = Response[EncounteredErrorResponse](
        response=EncounteredErrorResponse(
            message="Name is required, provide both 'given_name' and 'family_name' in account data",
            error_code="{hyphenated_name}.bad_request",
            raised_by="ConnectorError",
            raised_in="{name}.integration:create_account",
        ),
    )
    return args, response_body_map, expected_response


def case_create_account_400_too_many_entitlements() -> TestCase:
    """Invalid request when creating an account with too many provided entitlements."""
    args = Request[CreateAccountRequest](
        request=CreateAccountRequest(
            account=CreateAccount(
                email="jw7rT@example.com",
                given_name="John",
                family_name="Doe",
            ),
            entitlements=[
                CreateAccountEntitlement(
                    integration_specific_id="",
                    integration_specific_resource_id="dev-lumos",
                    entitlement_type="",
                ),
                CreateAccountEntitlement(
                    integration_specific_id="",
                    integration_specific_resource_id="dev-lumos",
                    entitlement_type="",
                ),
                CreateAccountEntitlement(
                    integration_specific_id="license-1",
                    integration_specific_resource_id="dev-lumos",
                    entitlement_type="",
                ),
            ],
        ),
        auth=VALID_AUTH,
    )
    response_body_map ={{
        "POST": {{
            "/users": MockedResponse(
                status_code=httpx.codes.BAD_REQUEST,
                response_body={{}},
            ),
        }},
    }}
    expected_response = Response[EncounteredErrorResponse](
        response=EncounteredErrorResponse(
            message="Too many entitlements provided",
            error_code="{hyphenated_name}.bad_request",
            raised_by="ConnectorError",
            raised_in="{name}.integration:create_account",
        ),
    )
    return args, response_body_map, expected_response


def case_create_account_400_invalid_entitlements() -> TestCase:
    """Invalid request when creating an account with too many provided entitlements."""
    args = Request(
        request=CreateAccountRequest(
            account=CreateAccount(
                email="jw7rT@example.com",
                given_name="John",
                family_name="Doe",
            ),
            entitlements=[
                CreateAccountEntitlement(
                    integration_specific_id="",
                    integration_specific_resource_id="dev-lumos",
                    entitlement_type="",
                ),
                CreateAccountEntitlement(
                    integration_specific_id="",
                    integration_specific_resource_id="dev-lumos",
                    entitlement_type="",
                ),
            ],
        ),
        auth=VALID_AUTH,
    )
    response_body_map ={{
        "POST": {{
            "/users": MockedResponse(
                status_code=httpx.codes.BAD_REQUEST,
                response_body={{}},
            ),
        }},
    }}
    expected_response = Response(
        response=EncounteredErrorResponse(
            message="The same entitlement type provided",
            error_code="{hyphenated_name}.bad_request",
            raised_by="ConnectorError",
            raised_in="{name}.integration:create_account",
        ),
    )
    return args, response_body_map, expected_response


def case_create_account_401() -> TestCase:
    """Unauthorized request should fail."""
    args = Request(
        request=CreateAccountRequest(
            account=CreateAccount(
                email="jw7rT@example.com",
                given_name="John",
                family_name="Doe",
            ),
            entitlements=[],
        ),
        auth=INVALID_AUTH,
    )
    response_body_map = {{
        "POST": {{
            "/users": MockedResponse(status_code=httpx.codes.UNAUTHORIZED, response_body=None),
        }},
    }}
    expected_response = Response(
        response=EncounteredErrorResponse(
            message=http_error_message("https://api.pagerduty.com/users", httpx.codes.UNAUTHORIZED),
            status_code=httpx.codes.UNAUTHORIZED,
            error_code="{hyphenated_name}.unauthorized",
            raised_by="HTTPStatusError",
            raised_in="{name}.integration:create_account",
        ),
    )
    return args, response_body_map, expected_response

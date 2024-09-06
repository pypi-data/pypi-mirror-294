"""Test cases for ``get_capability_annotations`` function."""
import typing as t

import pytest_cases
from connector.serializers.request import Request, RequestData, ValidateCredentialsRequest
from connector.serializers.response import Response, ResponseData, ValidateCredentialsResponse

TestCaseCorrect: t.TypeAlias = tuple[
    t.Callable[[Request[RequestData]], Response[ResponseData]],
    tuple[type[Request[RequestData]], type[Response[ResponseData]]],
]


@pytest_cases.case(tags=("correct",))
def case_correct_capability() -> TestCaseCorrect:
    def capability(
        args: Request[ValidateCredentialsRequest],
    ) -> Response[ValidateCredentialsResponse]:
        return Response[ValidateCredentialsResponse](
            response=ValidateCredentialsResponse(valid=True),
            raw_data=None,
        )

    expected_annotations = (
        Request[ValidateCredentialsRequest],
        Response[ValidateCredentialsResponse],
    )
    return capability, expected_annotations


@pytest_cases.case(tags=("missing_annotation",))
def case_missing_argument_annotation() -> (
    t.Callable[[Request[RequestData]], Response[ResponseData]]
):
    def capability(args) -> Response[ValidateCredentialsResponse]:
        return Response[ValidateCredentialsResponse](
            response=ValidateCredentialsResponse(valid=True),
            raw_data=None,
        )

    return capability  # type: ignore[return-value]


@pytest_cases.case(tags=("missing_annotation",))
def case_missing_return_annotation() -> t.Callable[[Request[RequestData]], Response[ResponseData]]:
    def capability(args: Request[ValidateCredentialsRequest]):
        return Response[ValidateCredentialsResponse](
            response=ValidateCredentialsResponse(valid=True),
            raw_data=None,
        )

    return capability  # type: ignore[return-value]


@pytest_cases.case(tags=("missing_annotation",))
def case_missing_annotations() -> t.Callable[[Request[RequestData]], Response[ResponseData]]:
    def capability(args):
        return Response[ValidateCredentialsResponse](
            response=ValidateCredentialsResponse(valid=True),
            raw_data=None,
        )

    return capability  # type: ignore[return-value]

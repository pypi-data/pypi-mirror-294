import logging
from abc import abstractmethod
from typing import Any, Callable, List, Tuple

from connector.generated import Error, ErrorCode, ErrorResponse


class ConnectorError(Exception):
    """
    Base exception class for Lumos connectors.
    Preferred way to raise exceptions inside the conenctors.
    `raise ConnectorError(message, error_code)`

    message: str (Custom error message)
    error_code: ErrorCode (The actual error code, eg. "internal_error")
    """

    def __init__(self, message: str, error_code: ErrorCode):
        self.error_code = error_code
        self.message = message


class ExceptionHandler:
    """
    Abstract class for handling exceptions. You can subclass this to create your own exception handler.
    """

    def __init__(self):
        pass

    @staticmethod
    @abstractmethod
    def handle(
        e: Exception,
        original_func: Any,
        response: ErrorResponse,
        error_code: ErrorCode | None = None,
    ) -> ErrorResponse:
        """
        Handle an exception. (ErrorHandler signature typing)

        e: Exception (An exception that was raised)
        original_func: FunctionType (The original method that was called, eg. validate_credentials)
        response: ErrorResp (The output of the connector call)
        error_code: ErrorCode | None (The actual error code, eg. "internal_error")
        """
        return response


class DefaultHandler(ExceptionHandler):
    """
    Default exception handler that handles the basic HTTPX/GQL extraction (etc.) and chains onto the global handler.
    These are operations that are always done on the raised error.
    """

    @staticmethod
    def handle(
        e: Exception,
        original_func: Any,
        response: ErrorResponse,
        error_code: ErrorCode | None = None,
    ) -> ErrorResponse:
        status_code: int | None = None

        # HTTPX HTTP Status code
        if hasattr(e, "response") and hasattr(e.response, "status_code"):  # type: ignore
            status_code = e.response.status_code  # type: ignore
        # GraphQL error code
        if hasattr(e, "code"):
            status_code = e.code  # type: ignore

        # Populating some base info
        response.error.message = e.message if hasattr(e, "message") else str(e)  # type: ignore
        response.error.status_code = status_code
        # TODO: add line number
        response.error.raised_in = f"{original_func.__module__}:{original_func.__name__}"
        response.error.raised_by = f"{e.__class__.__name__}"

        # ConnectorError already has an error code attached, so we need to chain
        if isinstance(e, ConnectorError):
            response.error.error_code = error_code if error_code else e.error_code
        else:
            # Otherwise, it is an unexpected error from an app_id
            response.error.error_code = error_code if error_code else ErrorCode.UNEXPECTED_ERROR

        return response


class HTTPHandler(ExceptionHandler):
    """
    Default exception handler for simple HTTP exceptions.
    If you want to handle more complicated exceptions, you can create your own instead.
    """

    @staticmethod
    def handle(
        e: Exception,
        original_func: Any,
        response: ErrorResponse,
        error_code: ErrorCode | None = None,
    ) -> ErrorResponse:
        match response.error.status_code:
            case 400:
                response.error.error_code = ErrorCode.BAD_REQUEST
            case 401:
                response.error.error_code = ErrorCode.UNAUTHORIZED
            case 403:
                response.error.error_code = ErrorCode.PERMISSION_DENIED
            case 404:
                response.error.error_code = ErrorCode.NOT_FOUND
            case _:
                response.error.error_code = ErrorCode.API_ERROR

        return response


ErrorMap = List[Tuple[type[Exception], type[ExceptionHandler], ErrorCode | None]]

logger = logging.getLogger(__name__)


def handle_exception(
    exception_classes: ErrorMap, error: Exception, func: Callable[[Any], Any], app_id: str
) -> ErrorResponse:
    """
    Decorator that adds error handling to a method. Uses the default Lumos error handler if no exception handler is provided.

    Example:
    ```python
    @exception_handler(
        (httpx.HTTPStatusError, ExceptionHandler, "error.code"),
    )
    async def verify_credentials(self, args: ValidateCredentialsArgs) -> ValidateCredentialsResp:
        pass
    ```

    Args:
        exception_classes (tuple): Tuple of exception classes to be handled. Map of exception class to handler function.

    Returns
    -------
        function: Decorated function.
    """

    resp = ErrorResponse(
        is_error=True, error=Error(message=str(error), error_code=ErrorCode.UNEXPECTED_ERROR)
    )

    resp = DefaultHandler.handle(
        error,
        func,
        resp,
        None,
    )

    if not isinstance(error, ConnectorError):
        for exception_class, handler, code in exception_classes:
            if isinstance(error, exception_class) and handler:
                resp = handler.handle(error, func, resp, code)

    logger.error(f"{resp.error.error_code}: {resp.error.message}")
    return resp

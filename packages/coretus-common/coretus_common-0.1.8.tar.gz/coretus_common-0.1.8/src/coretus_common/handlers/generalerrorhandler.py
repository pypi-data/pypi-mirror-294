from fastapi import Request, HTTPException
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from src.coretus_common.errors.baseerror import BaseExceptionHandler


class HTTPExceptionHandler(BaseExceptionHandler):
    """
    Handles HTTP exceptions.

    Inherits:
        BaseExceptionHandler: Base handler for exceptions.
    """

    def __init__(self):
        super().__init__(HTTPException)

    def handle(self, request: Request, exc: HTTPException) -> JSONResponse:
        """
        Handle HTTP exceptions and return a JSON response.

        Args:
            request (Request): The HTTP request object.
            exc (HTTPException): The HTTP exception to handle.

        Returns:
            JSONResponse: The JSON response with HTTP error details.
        """
        return JSONResponse(
            status_code=exc.status_code,
            content={"message": exc.detail, "error": str(exc)},
        )


class ValidationExceptionHandler(BaseExceptionHandler):
    """
    Handles request validation exceptions.

    Inherits:
        BaseExceptionHandler: Base handler for exceptions.
    """

    def __init__(self):
        super().__init__(RequestValidationError)

    def handle(self, request: Request, exc: RequestValidationError) -> JSONResponse:
        """
        Handle validation exceptions and return a JSON response.

        Args:
            request (Request): The HTTP request object.
            exc (RequestValidationError): The validation exception to handle.

        Returns:
            JSONResponse: The JSON response with validation error details.
        """
        return JSONResponse(
            status_code=422,
            content={"message": "Validation error", "error": str(exc)},
        )


class ValueExceptionHandler(BaseExceptionHandler):
    """
    Handles value errors.

    Inherits:
        BaseExceptionHandler: Base handler for exceptions.
    """

    def __init__(self):
        super().__init__(ValueError)

    def handle(self, request: Request, exc: ValueError) -> JSONResponse:
        """
        Handle value errors and return a JSON response.

        Args:
            request (Request): The HTTP request object.
            exc (ValueError): The value error to handle.

        Returns:
            JSONResponse: The JSON response with value error details.
        """
        return JSONResponse(
            status_code=400,
            content={"message": "Value error.", "error": str(exc)}
        )


class KeyExceptionHandler(BaseExceptionHandler):
    """
    Handles key errors.

    Inherits:
        BaseExceptionHandler: Base handler for exceptions.
    """

    def __init__(self):
        super().__init__(KeyError)

    def handle(self, request: Request, exc: KeyError) -> JSONResponse:
        """
        Handle key errors and return a JSON response.

        Args:
            request (Request): The HTTP request object.
            exc (KeyError): The key error to handle.

        Returns:
            JSONResponse: The JSON response with key error details.
        """
        return JSONResponse(
            status_code=500,
            content={"message": "Required key is missing in the data.", "error": str(exc)}
        )


class AttributeExceptionHandler(BaseExceptionHandler):
    """
    Handles attribute errors.

    Inherits:
        BaseExceptionHandler: Base handler for exceptions.
    """

    def __init__(self):
        super().__init__(AttributeError)

    def handle(self, request: Request, exc: AttributeError) -> JSONResponse:
        """
        Handle attribute errors and return a JSON response.

        Args:
            request (Request): The HTTP request object.
            exc (AttributeError): The attribute error to handle.

        Returns:
            JSONResponse: The JSON response with attribute error details.
        """
        return JSONResponse(
            status_code=500,
            content={"message": "Attribute is missing in the data.", "error": str(exc)}
        )


class TypeExceptionHandler(BaseExceptionHandler):
    """
    Handles type errors.

    Inherits:
        BaseExceptionHandler: Base handler for exceptions.
    """

    def __init__(self):
        super().__init__(TypeError)

    def handle(self, request: Request, exc: TypeError) -> JSONResponse:
        """
        Handle type errors and return a JSON response.

        Args:
            request (Request): The HTTP request object.
            exc (TypeError): The type error to handle.

        Returns:
            JSONResponse: The JSON response with type error details.
        """
        print(exc)
        return JSONResponse(
            status_code=400,
            content={"message": "Invalid type in data.", "error": str(exc)}
        )


class GenericExceptionHandler(BaseExceptionHandler):
    """
    Handles generic exceptions.

    Inherits:
        BaseExceptionHandler: Base handler for exceptions.
    """

    def __init__(self):
        super().__init__(Exception)

    def handle(self, request: Request, exc: Exception) -> JSONResponse:
        """
        Handle generic exceptions and return a JSON response.

        Args:
            request (Request): The HTTP request object.
            exc (Exception): The generic exception to handle.

        Returns:
            JSONResponse: The JSON response with generic error details.
        """
        return JSONResponse(
            status_code=500,
            content={"message": "Internal Server Error", "error": str(exc)}
        )

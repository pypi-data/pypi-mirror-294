from fastapi import Request
from fastapi.responses import JSONResponse
from jwt import exceptions
from src.coretus_common.errors.baseerror import BaseExceptionHandler


class JWTExceptionHandler(BaseExceptionHandler):
    """
    Handles JWT-related exceptions.

    Inherits:
        BaseExceptionHandler: Base handler for exceptions.
    """

    def __init__(self):
        super().__init__(exceptions.PyJWTError)

    def handle(self, request: Request, exc: exceptions.PyJWTError) -> JSONResponse:
        """
        Handle JWT exceptions and return a JSON response.

        Args:
            request (Request): The HTTP request object.
            exc (exceptions.PyJWTError): The JWT exception to handle.

        Returns:
            JSONResponse: The JSON response with JWT error details.
        """
        if isinstance(exc, exceptions.ExpiredSignatureError):
            return JSONResponse(
                status_code=401,
                content={"message": "You are not authorise to make request", "error": str(exc)}
            )
        return JSONResponse(
            status_code=401,
            content={"message": "You are not authorise to make request", "error": str(exc)}
        )

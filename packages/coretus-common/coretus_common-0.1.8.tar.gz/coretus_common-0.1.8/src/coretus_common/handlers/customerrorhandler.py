from typing import Type
from fastapi import Request
from fastapi.responses import JSONResponse
from src.coretus_common.errors.baseerror import BaseExceptionHandler


class CustomExceptionHandler(BaseExceptionHandler):
    """
    Handler for custom exceptions.

    Args:
        error_class (Type[Exception]): The exception class to handle.
        status_code (int): HTTP status code to return.
        message (str): Custom message to include in the response.
    """

    def __init__(self, error_class: Type[Exception], status_code: int, message: str):
        super().__init__(error_class)
        self.status_code = status_code
        self.message = message

    def handle(self, request: Request, exc: Exception) -> JSONResponse:
        """
        Handle the custom exception and return a JSON response.

        Args:
            request (Request): The HTTP request object.
            exc (Exception): The custom exception to handle.

        Returns:
            JSONResponse: The JSON response with custom message and error details.
        """
        return JSONResponse(
            status_code=self.status_code,
            content={"message": self.message, "error": str(exc)},
        )

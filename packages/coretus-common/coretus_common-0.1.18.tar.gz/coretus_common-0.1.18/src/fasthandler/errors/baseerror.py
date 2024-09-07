from abc import ABC, abstractmethod
from typing import Type

from fastapi import Request
from fastapi.responses import JSONResponse


class BaseExceptionHandler(ABC):
    """
    Abstract base class for exception handlers.

    Args:
        error_class (Type[Exception]): The exception class to handle.
    """

    def __init__(self, error_class: Type[Exception]):
        self.error_class = error_class

    @abstractmethod
    def handle(self, request: Request, exc: Exception) -> JSONResponse:
        """
        Handle the exception and return a JSON response.

        Args:
            request (Request): The HTTP request object.
            exc (Exception): The exception to handle.

        Returns:
            JSONResponse: The JSON response to return.
        """
        pass

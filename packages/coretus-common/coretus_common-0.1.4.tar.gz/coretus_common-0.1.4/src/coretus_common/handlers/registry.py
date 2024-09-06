from fastapi import FastAPI
from src.coretus_common.handlers import (
    CustomExceptionHandler,
    ValueExceptionHandler,
    HTTPExceptionHandler,
    AttributeExceptionHandler,
    ValidationExceptionHandler,
    KeyExceptionHandler,
    GenericExceptionHandler,
    TypeExceptionHandler
)
from src.coretus_common.middleware import MiddlewareRegistry


class ExceptionHandlerRegistry:
    """
    Registers and manages exception handlers for the FastAPI application.
    """

    def __init__(self, app: FastAPI):
        """
        Initialize the registry with default exception handlers and middleware.

        Args:
            app (FastAPI): The FastAPI application instance.
        """
        self.app = app
        self.middleware_registry = MiddlewareRegistry(app)
        self.middleware_registry.register_exception_middleware()

        # List of default handlers
        exception_handlers = [
            GenericExceptionHandler,
            HTTPExceptionHandler,
            AttributeExceptionHandler,
            ValidationExceptionHandler,
            KeyExceptionHandler,
            TypeExceptionHandler,
            ValueExceptionHandler
        ]

        # Register all default handlers
        for handler in exception_handlers:
            self.register(handler)

    def register(self, exc_class):
        """
        Register an exception handler for a specific exception class.

        Args:
            exc_class: The exception handler class to register.
        """
        handler_instance = exc_class()
        self.app.add_exception_handler(handler_instance.error_class, handler_instance.handle)

    def register_custom_exception(self, exc_class, status_code: int, message: str):
        """
        Register a custom exception handler with a specific status code and message.

        Args:
            exc_class: The custom exception class to handle.
            status_code (int): The HTTP status code to return.
            message (str): The custom message to include in the response.
        """
        custom_handler = CustomExceptionHandler(exc_class, status_code, message)
        self.app.add_exception_handler(custom_handler.error_class, custom_handler.handle)

from bson.errors import BSONError
from fastapi import Request
from fastapi.responses import JSONResponse
from pymongo.errors import (PyMongoError, WriteError, DuplicateKeyError, InvalidOperation,
                            OperationFailure, BulkWriteError, CursorNotFound, DocumentTooLarge)
from src.coretus_common.errors.baseerror import BaseExceptionHandler
from src.coretus_common.utils.mongo_validations import MongoValidationUtils


class DuplicateKeyExceptionHandler(BaseExceptionHandler):
    """
    Handles duplicate key errors in MongoDB.

    Inherits:
        BaseExceptionHandler: Base handler for exceptions.
    """

    def __init__(self):
        super().__init__(DuplicateKeyError)

    def handle(self, request: Request, exc: DuplicateKeyError) -> JSONResponse:
        """
        Handle duplicate key errors and return a JSON response.

        Args:
            request (Request): The HTTP request object.
            exc (DuplicateKeyError): The duplicate key error to handle.

        Returns:
            JSONResponse: The JSON response with duplicate key error details.
        """
        message = MongoValidationUtils.get_duplicate_validation(exc)
        return JSONResponse(status_code=400, content={"message": message, "error": str(exc)})


class CursorNotFoundExceptionHandler(BaseExceptionHandler):
    """
    Handles cursor not found errors in MongoDB.

    Inherits:
        BaseExceptionHandler: Base handler for exceptions.
    """

    def __init__(self):
        super().__init__(CursorNotFound)

    def handle(self, request: Request, exc: CursorNotFound) -> JSONResponse:
        """
        Handle cursor not found errors and return a JSON response.

        Args:
            request (Request): The HTTP request object.
            exc (CursorNotFound): The cursor not found error to handle.

        Returns:
            JSONResponse: The JSON response with cursor not found error details.
        """
        return JSONResponse(status_code=404,
                            content={"message": "Cursor not found, it may have been timed out or closed.",
                                     "error": str(exc)})


class WriteErrorHandler(BaseExceptionHandler):
    """
    Handles write errors in MongoDB.

    Inherits:
        BaseExceptionHandler: Base handler for exceptions.
    """

    def __init__(self):
        super().__init__(WriteError)

    def handle(self, request: Request, exc: WriteError) -> JSONResponse:
        """
        Handle write errors and return a JSON response.

        Args:
            request (Request): The HTTP request object.
            exc (WriteError): The write error to handle.

        Returns:
            JSONResponse: The JSON response with write error details.
        """
        messages = MongoValidationUtils.get_write_validation(exc)
        return JSONResponse(status_code=400, content={"message": messages, "error": str(exc)})


class BulkWriteErrorHandler(BaseExceptionHandler):
    """
    Handles bulk write errors in MongoDB.

    Inherits:
        BaseExceptionHandler: Base handler for exceptions.
    """

    def __init__(self):
        super().__init__(BulkWriteError)

    def handle(self, request: Request, exc: BulkWriteError) -> JSONResponse:
        """
        Handle bulk write errors and return a JSON response.

        Args:
            request (Request): The HTTP request object.
            exc (BulkWriteError): The bulk write error to handle.

        Returns:
            JSONResponse: The JSON response with bulk write error details.
        """
        messages = MongoValidationUtils.get_write_validation(exc)
        return JSONResponse(status_code=400, content={"message": messages, "error": str(exc)})


class InvalidOperationExceptionHandler(BaseExceptionHandler):
    """
    Handles invalid operation errors in MongoDB.

    Inherits:
        BaseExceptionHandler: Base handler for exceptions.
    """

    def __init__(self):
        super().__init__(InvalidOperation)

    def handle(self, request: Request, exc: InvalidOperation) -> JSONResponse:
        """
        Handle invalid operation errors and return a JSON response.

        Args:
            request (Request): The HTTP request object.
            exc (InvalidOperation): The invalid operation error to handle.

        Returns:
            JSONResponse: The JSON response with invalid operation error details.
        """
        if hasattr(exc, 'details'):
            return JSONResponse(
                status_code=400,
                content={"message": str(exc.details['errmsg']), "error": str(exc)}
            )
        else:
            return JSONResponse(
                status_code=400,
                content={"message": "Invalid Operation", "error": str(exc)}
            )


class OperationFailureExceptionHandler(BaseExceptionHandler):
    """
    Handles operation failure errors in MongoDB.

    Inherits:
        BaseExceptionHandler: Base handler for exceptions.
    """

    def __init__(self):
        super().__init__(OperationFailure)

    def handle(self, request: Request, exc: OperationFailure) -> JSONResponse:
        """
        Handle operation failure errors and return a JSON response.

        Args:
            request (Request): The HTTP request object.
            exc (OperationFailure): The operation failure error to handle.

        Returns:
            JSONResponse: The JSON response with operation failure error details.
        """
        if hasattr(exc, 'details') and 'errmsg' in exc.details:
            return JSONResponse(
                status_code=500,
                content={"message": str(exc.details['errmsg']), "error": str(exc)}
            )
        else:
            return JSONResponse(
                status_code=400,
                content={"message": "Operation failed", "error": str(exc)}
            )


class MongoExceptionHandler(BaseExceptionHandler):
    """
    Handles various MongoDB-related exceptions by delegating to specific handlers.

    Inherits:
        BaseExceptionHandler: Base handler for exceptions.
    """

    def __init__(self):
        super().__init__(PyMongoError)
        self.handlers = [
            DuplicateKeyExceptionHandler(),
            CursorNotFoundExceptionHandler(),
            WriteErrorHandler(),
            BulkWriteErrorHandler(),
            InvalidOperationExceptionHandler(),
            OperationFailureExceptionHandler()
        ]

    def handle(self, request: Request, exc: PyMongoError) -> JSONResponse:
        """
        Handle MongoDB exceptions by delegating to the appropriate handler.

        Args:
            request (Request): The HTTP request object.
            exc (PyMongoError): The MongoDB exception to handle.

        Returns:
            JSONResponse: The JSON response based on the specific MongoDB error handler.
        """
        for handler in self.handlers:
            if isinstance(exc, handler.error_class):
                return handler.handle(request, exc)
        return JSONResponse(status_code=500, content={"message": "MongoDB error", "error": str(exc)})


class BsonExceptionHandler(BaseExceptionHandler):
    """
    Handles BSON errors.

    Inherits:
        BaseExceptionHandler: Base handler for exceptions.
    """

    def __init__(self):
        super().__init__(BSONError)

    def handle(self, request: Request, exc: BSONError) -> JSONResponse:
        """
        Handle BSON errors and return a JSON response.

        Args:
            request (Request): The HTTP request object.
            exc (BSONError): The BSON error to handle.

        Returns:
            JSONResponse: The JSON response with BSON error details.
        """
        if isinstance(exc, DocumentTooLarge):
            return JSONResponse(
                status_code=413,
                content={"message": "Document Too Large.", "error": str(exc)}
            )
        return JSONResponse(
            status_code=400,
            content={"message": str(exc), "error": str(exc)}
        )

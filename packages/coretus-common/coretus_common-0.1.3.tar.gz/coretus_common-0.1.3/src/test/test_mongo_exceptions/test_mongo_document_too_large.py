from fastapi import FastAPI
from fastapi.testclient import TestClient
from pymongo.errors import DocumentTooLarge
from src.coretus_common.handlers import ExceptionHandlerRegistry, BsonExceptionHandler

# Mock FastAPI app
app = FastAPI()
registry = ExceptionHandlerRegistry(app)
registry.register(BsonExceptionHandler)

@app.get("/test-mongo-document-too-large")
async def mongo_document_too_large():
    """
    Endpoint to test the BSON document too large exception handler.

    Raises:
        DocumentTooLarge: A simulated error to trigger the exception handler.
    """

    raise DocumentTooLarge("Document is too large")

client = TestClient(app)

def test_mongo_document_too_large_handler():
    """
    Tests the BSON document too large exception handler for the /test-mongo-document-too-large endpoint.

    Asserts:
        - The response status code is 413.
        - The response message is "Document Too Large."
    """
    response = client.get("/test-mongo-document-too-large")
    assert response.status_code == 413
    assert response.json()["message"] == "Document Too Large."

from fastapi import FastAPI
from fastapi.testclient import TestClient
from pymongo.errors import DuplicateKeyError
from src.coretus_common.handlers import ExceptionHandlerRegistry, MongoExceptionHandler

# Mock FastAPI app
app = FastAPI()
registry = ExceptionHandlerRegistry(app)
registry.register(MongoExceptionHandler)

@app.get("/test-mongo-duplicate-key-error")
async def mongo_duplicate_key_error():
    """
    Endpoint to test the MongoDB duplicate key error handler.

    Raises:
        DuplicateKeyError: A duplicate key error to trigger the MongoExceptionHandler.
    """
    error_details = {
        "keyValue": {"email": "test@example.com"}
    }
    raise DuplicateKeyError(error = "duplicate key error", code=1, details=error_details)

client = TestClient(app)

def test_mongo_duplicate_key_error_handler():
    """
    Tests the MongoDB duplicate key error handler for the /test-mongo-duplicate-key-error endpoint.

    Asserts:
        - The response status code is 400.
        - The response message indicates the email is already used.
    """
    response = client.get("/test-mongo-duplicate-key-error")
    print(response.json())
    assert response.status_code == 400
    assert response.json()["message"] == "This email is already used, please try another."

from fastapi import FastAPI
from fastapi.testclient import TestClient
from pymongo.errors import InvalidOperation
from src.coretus_common.handlers import ExceptionHandlerRegistry, MongoExceptionHandler

# Mock FastAPI app
app = FastAPI()
registry = ExceptionHandlerRegistry(app)
registry.register(MongoExceptionHandler)

@app.get("/test-mongo-invalid-operation")
async def mongo_invalid_operation():
    """
    Endpoint to test the MongoDB invalid operation handler.

    Raises:
        InvalidOperation: Simulates an invalid operation error from MongoDB.
    """
    raise InvalidOperation("Invalid operation", {"errmsg": "Cannot perform the operation"})

client = TestClient(app)

def test_mongo_invalid_operation_handler():
    """
    Tests the MongoDB invalid operation handler for the /test-mongo-invalid-operation endpoint.

    Asserts:
        - The response status code is 400.
        - The response message is "Invalid Operation".
    """
    response = client.get("/test-mongo-invalid-operation")
    print(response.json())
    assert response.status_code == 400
    assert response.json()["message"] == "Invalid Operation"

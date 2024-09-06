from fastapi import FastAPI
from fastapi.testclient import TestClient
from pymongo.errors import OperationFailure
from src.coretus_common.handlers import ExceptionHandlerRegistry, MongoExceptionHandler

# Mock FastAPI app
app = FastAPI()
registry = ExceptionHandlerRegistry(app)
registry.register(MongoExceptionHandler)

@app.get("/test-mongo-operation-failure")
async def mongo_operation_failure():
    """
    Endpoint to test the MongoDB operation failure handler.

    Raises:
        OperationFailure: Simulates an operation failure in MongoDB.
    """
    raise OperationFailure(error = "Operation failed", details={"errmsg": "The operation has failed"})

client = TestClient(app)

def test_mongo_operation_failure_handler():
    """
    Tests the MongoDB operation failure handler for the /test-mongo-operation-failure endpoint.

    Asserts:
        - The response status code is 500.
        - The response message is "The operation has failed".
    """
    response = client.get("/test-mongo-operation-failure")
    assert response.status_code == 500
    assert response.json()["message"] == "The operation has failed"

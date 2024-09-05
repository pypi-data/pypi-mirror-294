from fastapi import FastAPI
from fastapi.testclient import TestClient
from pymongo.errors import WriteError
from src.coretus_common.handlers import ExceptionHandlerRegistry, MongoExceptionHandler

# Mock FastAPI app
app = FastAPI()
registry = ExceptionHandlerRegistry(app)
registry.register(MongoExceptionHandler)

@app.get("/test-mongo-write-error")
async def mongo_write_error():
    """
    Endpoint to test MongoDB write error handling.

    Raises:
        WriteError: A simulated MongoDB write error indicating a missing 'name' property.
    """
    error_details = {
        "errInfo": {
            "details": {
                "schemaRulesNotSatisfied": [
                    {
                        "operatorName": "required",
                        "missingProperties": ["name"]
                    }
                ]
            }
        }
    }
    raise WriteError(error = "The 'name' property is required.", code=1, details = error_details)

client = TestClient(app)

def test_mongo_write_error_handler():
    """
    Tests the MongoDB write error handler for the /test-mongo-write-error endpoint.

    Asserts:
        - The response status code is 400.
        - The response message contains information about the missing 'name' property.
    """
    response = client.get("/test-mongo-write-error")
    assert response.status_code == 400
    assert "name:  This field is required" in response.json()["message"]

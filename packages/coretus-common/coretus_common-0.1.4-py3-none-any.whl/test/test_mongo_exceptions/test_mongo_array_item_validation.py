from fastapi import FastAPI
from fastapi.testclient import TestClient
from pymongo.errors import WriteError
from src.coretus_common.handlers import ExceptionHandlerRegistry
from src.coretus_common. handlers import MongoExceptionHandler

# Mock FastAPI app
app = FastAPI()
registry = ExceptionHandlerRegistry(app)
registry.register(MongoExceptionHandler)

@app.get("/test-mongo-array-item-validation")
async def mongo_array_item_validation():
    """
    Endpoint to test MongoDB array item validation handling.

    Raises:
        WriteError: Simulates a MongoDB write error with array item validation details.
    """
    error_details = {
        "errInfo": {
            "details": {
                "schemaRulesNotSatisfied": [
                    {
                        "operatorName": "items",
                        "itemIndex": 2,
                        "details": [
                            {
                                "operatorName": "required",
                                "missingProperties": ["name"]
                            }
                        ]
                    }
                ]
            }
        }
    }
    raise WriteError("Array item 3 missing required property 'name'", code=1, details=error_details)

client = TestClient(app)

def test_mongo_array_item_validation_handler():
    """
    Tests the handling of MongoDB array item validation errors.

    Asserts:
        - The response status code is 400.
        - The response message contains the validation error details.
    """
    response = client.get("/test-mongo-array-item-validation")
    assert response.status_code == 400
    assert ".2.name:  This field is required" in response.json()["message"]

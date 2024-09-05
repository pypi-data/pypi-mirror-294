from fastapi import FastAPI
from fastapi.testclient import TestClient
from pymongo.errors import WriteError
from src.coretus_common.handlers import ExceptionHandlerRegistry, MongoExceptionHandler

# Mock FastAPI app
app = FastAPI()
registry = ExceptionHandlerRegistry(app)
registry.register(MongoExceptionHandler)

@app.get("/test-mongo-nested-schema-rules")
async def mongo_nested_schema_rules():
    """
    Endpoint to test the MongoDB nested schema rules handler.

    Raises:
        WriteError: Simulated nested schema write error with details about
        missing properties in nested schema rules.
    """
    error_details = {
        "errInfo": {
            "details": {
                "schemaRulesNotSatisfied": [
                    {
                        "operatorName": "properties",
                        "propertiesNotSatisfied": [
                            {
                                "propertyName": "address",
                                "details": [
                                    {
                                        "operatorName": "required",
                                        "missingProperties": ["street", "city"]
                                    }
                                ]
                            }
                        ]
                    }
                ]
            }
        }
    }
    raise WriteError(error = "nested schema write error", details=error_details, code=1)

client = TestClient(app)

def test_mongo_nested_schema_rules_handler():
    """
    Tests the MongoDB nested schema rules handler for the
    /test-mongo-nested-schema-rules endpoint.

    Asserts:
        - The response status code is 400.
        - The response message contains required field errors for address.street and address.city.
    """
    response = client.get("/test-mongo-nested-schema-rules")
    assert response.status_code == 400
    assert "address.street:  This field is required" in response.json()["message"]
    assert "address.city:  This field is required" in response.json()["message"]

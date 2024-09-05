from fastapi import FastAPI
from fastapi.testclient import TestClient
from pymongo.errors import WriteError

from src.coretus_common.handlers import ExceptionHandlerRegistry, MongoExceptionHandler

# Mock FastAPI app
app = FastAPI()
registry = ExceptionHandlerRegistry(app)
registry.register(MongoExceptionHandler)

@app.get("/test-mongo-custom-reason")
async def mongo_custom_reason():
  """
  Endpoint to test the MongoDB custom reason handler.

  Raises:
      WriteError: Simulates a MongoDB WriteError with custom error details.
  """
  error_details = {
  "errInfo": {
    "failingDocumentId": "630d093a931191850b40d0a9",
    "details": {
      "operatorName": "$jsonSchema",
      "title": "Student Object Validation",
      "schemaRulesNotSatisfied": [
        {
          "operatorName": "properties",
          "propertiesNotSatisfied": [
            {
              "propertyName": "gpa",
              "description": "'gpa' must be a double if the field exists",
              "details": [
                {
                  "operatorName": "bsonType",
                  "specifiedAs": {
                    "bsonType": ["double"]
                  },
                  "reason": "type did not match",
                  "consideredValue": 3,
                  "consideredType": "int"
                }
              ]
            }
          ]
        }
      ]
    }
  }
}

  raise WriteError(error = "gpa:  type did not match",  details=error_details)

client = TestClient(app)

def test_mongo_custom_reason_handler():
  """
  Tests the MongoDB custom reason handler for the /test-mongo-custom-reason endpoint.

  Asserts:
      - The response status code is 400.
      - The response message contains the custom error reason.
  """
  response = client.get("/test-mongo-custom-reason")
  assert response.status_code == 400
  assert "gpa:  type did not match" in response.json()["message"]

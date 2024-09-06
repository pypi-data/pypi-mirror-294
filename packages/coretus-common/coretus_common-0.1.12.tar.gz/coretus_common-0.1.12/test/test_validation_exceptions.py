from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.testclient import TestClient
from src.coretus_common.handlers import ExceptionHandlerRegistry
# Mock FastAPI app
app = FastAPI()
ExceptionHandlerRegistry(app)

@app.get("/test-validation-exception")
async def validation_exception(request: Request):
    """
    Endpoint to test the validation exception handler.

    Raises:
        RequestValidationError: Triggers a validation exception for testing purposes.
    """
    raise RequestValidationError([])

client = TestClient(app)

def test_validation_exception_handler():
    """
    Tests the validation exception handler for the /test-validation-exception endpoint.

    Asserts:
        - The response status code is 422.
        - The response message is "Validation error".
    """
    response = client.get("/test-validation-exception")
    assert response.status_code == 422
    assert response.json()["message"] == "Validation error"

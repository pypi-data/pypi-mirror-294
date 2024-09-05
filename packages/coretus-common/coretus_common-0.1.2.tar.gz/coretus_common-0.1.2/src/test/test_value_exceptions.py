from fastapi import FastAPI
from fastapi.testclient import TestClient
from src.coretus_common.handlers import ExceptionHandlerRegistry

# Mock FastAPI app
app = FastAPI()
ExceptionHandlerRegistry(app)

@app.get("/test-value-exception")
async def value_exception():
    """
    Endpoint to test the value exception handler.

    Raises:
        ValueError: An invalid value error to trigger the exception handler.
    """
    raise ValueError("Invalid value")

client = TestClient(app)

def test_value_exception_handler():
    """
    Tests the value exception handler for the /test-value-exception endpoint.

    Asserts:
        - The response status code is 400.
        - The response message is "Value error."
    """
    response = client.get("/test-value-exception")
    assert response.status_code == 400
    assert response.json()["message"] == "Value error."

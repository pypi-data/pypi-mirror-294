from fastapi import FastAPI
from fastapi.testclient import TestClient
from src.coretus_common.handlers import ExceptionHandlerRegistry

# Mock FastAPI app
app = FastAPI()
ExceptionHandlerRegistry(app)

@app.get("/test-type-exception")
async def type_exception():
    """
    Endpoint to test the type exception handler.

    Raises:
        TypeError: An error to trigger the type exception handler.
    """
    raise TypeError("Invalid type")

client = TestClient(app)

def test_type_exception_handler():
    """
    Tests the type exception handler for the /test-type-exception endpoint.

    Asserts:
        - The response status code is 400.
        - The response message is "Invalid type in data."
    """
    response = client.get("/test-type-exception")
    assert response.status_code == 400
    assert response.json()["message"] == "Invalid type in data."

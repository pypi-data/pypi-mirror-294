from fastapi import FastAPI
from fastapi.testclient import TestClient
from src.coretus_common.handlers import ExceptionHandlerRegistry

# Mock FastAPI app
app = FastAPI()
ExceptionHandlerRegistry(app)

@app.get("/test-key-exception")
async def key_exception():
    """
    Endpoint to test the key exception handler.

    Raises:
        KeyError: A key error to trigger the key exception handler.
    """
    raise KeyError("Missing key")

client = TestClient(app)

def test_key_exception_handler():
    """
    Tests the key exception handler for the /test-key-exception endpoint.

    Asserts:
        - The response status code is 500.
        - The response message is "Required key is missing in the data."
    """
    response = client.get("/test-key-exception")
    assert response.status_code == 500
    assert response.json()["message"] == "Required key is missing in the data."

from fastapi import FastAPI
from fastapi.testclient import TestClient
from src.coretus_common.handlers import ExceptionHandlerRegistry

app = FastAPI()
ExceptionHandlerRegistry(app)

@app.get("/test-generic-exception")
async def endpoint_with_generic_exception():
    """
    Endpoint to test the generic exception handler.

    Raises:
        Exception: A generic error to trigger the exception handler.
    """
    raise Exception("Generic error")

client = TestClient(app)

def test_generic_exception_handler():
    """
    Tests the generic exception handler for the /test-generic-exception endpoint.

    Asserts:
        - The response status code is 500.
        - The response message is "Internal Server Error".
    """
    response = client.get("/test-generic-exception")
    print(response.json())
    assert response.status_code == 500
    assert response.json()["message"] == "Internal Server Error"
from fastapi import FastAPI
from fastapi.testclient import TestClient
from src.coretus_common.handlers import ExceptionHandlerRegistry

# Mock FastAPI app
app = FastAPI()
ExceptionHandlerRegistry(app)


@app.get("/test-attribute-exception")
async def attribute_exception():
    """
    Endpoint that raises an AttributeError to test the attribute exception handler.

    Raises:
        AttributeError: Simulates missing attribute error.
    """
    raise AttributeError("Missing attribute")

client = TestClient(app)

def test_attribute_exception_handler():
    """
    Test case for handling attribute exceptions.

    Sends a GET request to the /test-attribute-exception endpoint and
    verifies that the response has a 500 status code and the correct error message.
    """
    response = client.get("/test-attribute-exception")
    assert response.status_code == 500
    assert response.json()["message"] == "Attribute is missing in the data."

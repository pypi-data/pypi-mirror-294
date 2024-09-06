from fastapi import FastAPI
from fastapi.testclient import TestClient
from src.coretus_common.errors import CustomException
from src.coretus_common.handlers import ExceptionHandlerRegistry

# Mock FastAPI app
app = FastAPI()
ExceptionHandlerRegistry(app)


def test_custom_exception_handler():
    """
    Tests the custom exception handler for CustomException.

    Defines a route that raises a CustomException, registers a custom
    exception handler for CustomException, and verifies that the handler
    returns the correct status code and message in the response.

    Asserts:
        response.status_code: 400
        response.json()["message"]: "Custom error occurred"
    """
    @app.get("/test-custom-exception")
    async def custom_exception():
        raise CustomException(detail="Custom error", code=1001)

    ExceptionHandlerRegistry(app).register_custom_exception(CustomException, 400, "Custom error occurred")

    client = TestClient(app)
    response = client.get("/test-custom-exception")
    assert response.status_code == 400
    assert response.json()["message"] == "Custom error occurred"

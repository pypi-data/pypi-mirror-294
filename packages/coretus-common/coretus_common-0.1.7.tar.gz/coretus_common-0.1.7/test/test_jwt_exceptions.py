from fastapi import FastAPI
from fastapi.testclient import TestClient
from jwt import ExpiredSignatureError
from src.coretus_common.handlers import ExceptionHandlerRegistry, JWTExceptionHandler

# Mock FastAPI app
app = FastAPI()
registry = ExceptionHandlerRegistry(app)
registry.register(JWTExceptionHandler)



@app.get("/test-jwt-exception")
async def jwt_exception():
    """
    Endpoint to test JWT expiration exception handling.

    Raises:
        ExpiredSignatureError: Simulates an expired JWT token error.
    """
    raise ExpiredSignatureError("Token has expired")

client = TestClient(app)

def test_jwt_exception_handler():
    """
    Tests the JWT exception handler for the /test-jwt-exception endpoint.

    Asserts:
        - The response status code is 401.
        - The response message is "You are not authorise to make request".
    """
    response = client.get("/test-jwt-exception")
    assert response.status_code == 401
    assert response.json()["message"] == "You are not authorise to make request"

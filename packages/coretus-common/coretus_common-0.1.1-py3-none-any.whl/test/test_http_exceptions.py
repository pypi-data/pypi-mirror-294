from fastapi import FastAPI, HTTPException
from fastapi.testclient import TestClient
from src.coretus_common.handlers import ExceptionHandlerRegistry

# Mock FastAPI app
app = FastAPI()
ExceptionHandlerRegistry(app)

@app.get("/test-http-exception")
async def http_exception():
    """
    Endpoint to test the HTTP exception handler.

    Raises:
        HTTPException: A 404 error with the message "Item not found".
    """
    raise HTTPException(status_code=404, detail="Item not found")

client = TestClient(app)

def test_http_exception_handler():
    """
    Tests the HTTP exception handler for the /test-http-exception endpoint.

    Asserts:
        - The response status code is 404.
        - The response message is "Item not found".
    """
    response = client.get("/test-http-exception")
    assert response.status_code == 404
    assert response.json()["message"] == "Item not found"

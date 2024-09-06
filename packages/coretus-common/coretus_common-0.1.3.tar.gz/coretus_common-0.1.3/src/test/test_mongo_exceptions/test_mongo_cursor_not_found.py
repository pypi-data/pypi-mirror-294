from fastapi import FastAPI
from fastapi.testclient import TestClient
from pymongo.errors import CursorNotFound
from src.coretus_common.handlers import ExceptionHandlerRegistry, MongoExceptionHandler

# Mock FastAPI app
app = FastAPI()
registry = ExceptionHandlerRegistry(app)
registry.register(MongoExceptionHandler)

@app.get("/test-mongo-cursor-not-found")
async def mongo_cursor_not_found():
    """
    Endpoint to test the MongoDB cursor not found exception handler.

    Raises:
        CursorNotFound: Simulates a cursor not found error.
    """
    raise CursorNotFound("Cursor not found")

client = TestClient(app)

def test_mongo_cursor_not_found_handler():
    """
    Tests the MongoDB cursor not found exception handler for the
    /test-mongo-cursor-not-found endpoint.

    Asserts:
        - The response status code is 404.
        - The response message is "Cursor not found, it may have been timed out or closed."
    """
    response = client.get("/test-mongo-cursor-not-found")
    assert response.status_code == 404
    assert response.json()["message"] == "Cursor not found, it may have been timed out or closed."

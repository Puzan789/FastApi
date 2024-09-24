from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_read_main():
    response = client.get("/items/foo",headers={"X-Token": "thegreathammer"})
    assert response.status_code == 200
    assert response.json() == {"id": "bar", "title": "foo", "description": "root"}


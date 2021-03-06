from fastapi.testclient import TestClient
from ..main import app

from httpx import AsyncClient
import pytest

client = TestClient(app)

def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()['success'] == True
    assert response.json()['message'] == "ok"
    
    data = response.json()['data']
    assert data['greetings'] == "HELLO WORLD"

def test_send_feedback():
    body = {
            "title": "I love this API",
            "description": "Its very simple and quick, also very fast"
            }
    response = client.post("/send-feedback/", json=body)
    assert response.status_code == 200
    assert response.json()['success'] == True
    assert response.json()['data'] != None

def test_update_feedback():
    body = {
            "title": "Updated!",
            "description": "Yes, this object was updated"
            }
    response = client.put("/feedback/1" , json=body)
    assert response.status_code == 200
    assert response.json()['success'] == True
    assert response.json()['data'] != None

@pytest.mark.anyio
async def test_async_root():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/")
    assert response.status_code == 200
    assert response.json()['message'] == "ok"

def test_sql_query():
    res = client.get("/get_sql_query/")
    assert res.status_code == 200 
    assert res.json()['success'] == True

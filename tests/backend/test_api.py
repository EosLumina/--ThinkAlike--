import pytest
from fastapi.testclient import TestClient
from backend.api.routes import router

client = TestClient(router)

def test_read_root():
    response = client.get('/')
    assert response.status_code == 200
    assert response.json() == {'message': 'Welcome to ThinkAlike API'}

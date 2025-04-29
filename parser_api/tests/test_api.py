import pytest
from fastapi.testclient import TestClient
from parser_api.api.main import app

client = TestClient(app)

def test_read_main():
    """Test main endpoint"""
    response = client.get("/")
    assert response.status_code == 200

def test_get_products():
    """Test get products endpoint"""
    response = client.get("/api/v1/products")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_update_products():
    """Test update products endpoint"""
    response = client.post("/api/v1/update", json={"address": "Москва, Чонгарский бул., 7"})
    assert response.status_code == 200
    assert "message" in response.json() 
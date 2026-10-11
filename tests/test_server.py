"""Tests for FastAPI server."""
import pytest
from fastapi.testclient import TestClient
from server import app

client = TestClient(app)


class TestHealthEndpoint:
    def test_health(self):
        response = client.get("/health")
        assert response.status_code == 200
        assert response.json()["status"] == "healthy"


class TestRootEndpoint:
    def test_root(self):
        response = client.get("/")
        assert response.status_code == 200


class TestLanguagesEndpoint:
    def test_list_languages(self):
        response = client.get("/languages")
        assert response.status_code == 200
        assert "en" in response.json()["languages"]


class TestTranslateEndpoint:
    def test_basic_translate(self):
        response = client.post("/translate", json={
            "text": "hello", "source": "en", "target": "es"
        })
        assert response.status_code == 200
        data = response.json()
        assert data["source"] == "hello"
        assert "target" in data
        assert 0.0 <= data["confidence"] <= 1.0

    def test_translate_missing_fields(self):
        response = client.post("/translate", json={"text": "hello"})
        assert response.status_code == 422


class TestBatchEndpoint:
    def test_batch_translate(self):
        response = client.post("/batch", json={
            "items": [
                {"text": "hello", "source": "en", "target": "es"},
                {"text": "world", "source": "en", "target": "fr"},
            ]
        })
        assert response.status_code == 200
        assert len(response.json()["results"]) == 2


class TestTransliterateEndpoint:
    def test_basic_transliterate(self):
        response = client.post("/transliterate", json={
            "text": "hello", "language": "en"
        })
        assert response.status_code == 200
        assert "ipa" in response.json()

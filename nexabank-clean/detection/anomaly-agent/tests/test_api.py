
from fastapi.testclient import TestClient

from app import config, db
from app.main import app


def test_health_endpoint():
    with TestClient(app) as client:
        response = client.get("/health")

    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_stats_endpoint():
    with TestClient(app) as client:
        response = client.get("/stats")

    assert response.status_code == 200
    assert "events_total" in response.json()
    assert "alerts_total" in response.json()


def test_events_requires_api_key():
    original_key = config.INGEST_API_KEY
    config.INGEST_API_KEY = "test-secret-key"

    try:
        with TestClient(app) as client:
            response = client.post("/events", json={})

        assert response.status_code == 401
    finally:
        config.INGEST_API_KEY = original_key


def test_events_rejects_invalid_api_key():
    original_key = config.INGEST_API_KEY
    config.INGEST_API_KEY = "test-secret-key"

    try:
        with TestClient(app) as client:
            response = client.post(
                "/events",
                headers={"X-API-Key": "wrong-key"},
                json={},
            )

        assert response.status_code == 401
    finally:
        config.INGEST_API_KEY = original_key

def test_health_reports_baseline_agents():
    with TestClient(app) as client:
        response = client.get("/health")

    assert response.status_code == 200
    assert response.json()["baseline_agents"] == 3


def test_events_rejects_invalid_payload_with_valid_key():
    original_key = config.INGEST_API_KEY
    config.INGEST_API_KEY = "test-secret-key"

    try:
        with TestClient(app) as client:
            response = client.post(
                "/events",
                headers={"X-API-Key": "test-secret-key"},
                json={},
            )

        assert response.status_code == 422
    finally:
        config.INGEST_API_KEY = original_key


def test_events_rejects_wrong_key_even_with_payload():
    original_key = config.INGEST_API_KEY
    config.INGEST_API_KEY = "test-secret-key"

    payload = {
        "event_time": "2026-10-10T09:00:00Z",
        "event_type": "transaction",
        "agent_id": "AG-1001",
        "assigned_region": "Lagos",
        "region": "Lagos",
        "device_id": "TAB-1001",
        "cert_dn": "CN=AG-1001,OU=Agents,O=NexaBank",
        "amount": 10000,
        "result": "success",
    }

    try:
        with TestClient(app) as client:
            response = client.post(
                "/events",
                headers={"X-API-Key": "wrong-key"},
                json=payload,
            )

        assert response.status_code == 401
    finally:
        config.INGEST_API_KEY = original_key

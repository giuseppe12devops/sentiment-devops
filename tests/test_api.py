from fastapi.testclient import TestClient
from app import app

client = TestClient(app)


def test_predict():
    # Verifico che la API risponda con i campi richiesti
    response = client.post("/predict", json={"review": "This product is amazing! I love it."})
    assert response.status_code == 200
    assert response.json()["sentiment"] == "positive"
    assert 0 <= response.json()["confidence"] <= 1


def test_review_vuota():
    # Una recensione vuota non deve essere accettata
    response = client.post("/predict", json={"review": "  "})
    assert response.status_code == 400


def test_review_mancante():
    response = client.post("/predict", json={})
    assert response.status_code == 422


def test_metrics():
    response = client.get("/metrics")
    assert response.status_code == 200
    assert "http_request_duration_seconds" in response.text
    assert "prediction_errors_total" in response.text
    assert "process_cpu_seconds_total" in response.text
    assert "process_resident_memory_bytes" in response.text

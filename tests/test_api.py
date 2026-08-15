from fastapi.testclient import TestClientfrom ml_service.api.main import appclient = TestClient(app)def test_health():    response = client.get("/health")    assert response.status_code == 200    assert response.json()["status"] == "ok"def test_predict_valid():    response = client.post(        "/predict",        json={"sepal_length": 5.1, "sepal_width": 3.5, "petal_length": 1.4, "petal_width": 0.2},    )    assert response.status_code == 200    assert response.json()["label"] in {"setosa", "versicolor", "virginica"}def test_predict_rejects_out_of_range():    response = client.post(        "/predict",        json={"sepal_length": 9999, "sepal_width": 3.5, "petal_length": 1.4, "petal_width": 0.2},    )    assert response.status_code == 422

def test_metrics_endpoint():
    client.get("/health")  # generate at least one request
    response = client.get("/metrics")
    assert response.status_code == 200
    body = response.json()
    assert "total_requests" in body
    assert set(body["latency_ms"]) == {"p50_ms", "p95_ms", "p99_ms"}


def test_latency_header_present():
    response = client.get("/health")
    assert "X-Process-Time-Ms" in response.headers

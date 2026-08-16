from __future__ import annotations

import time

from fastapi import FastAPI, HTTPException, Response
from prometheus_client import CONTENT_TYPE_LATEST, generate_latest

from ml_service.api.schemas import PredictRequest, PredictResponse
from ml_service.config import load_config
from ml_service.data.validation import DataValidationError, validate_features
from ml_service.model.predict import get_predictor
from ml_service.monitoring.metrics import REQUEST_COUNT, REQUEST_LATENCY

app = FastAPI(title="ML Service", version="0.1.0")


@app.middleware("http")
async def track_metrics(request, call_next):
    start = time.perf_counter()
    response = await call_next(request)
    duration = time.perf_counter() - start
    endpoint = request.url.path
    REQUEST_LATENCY.labels(request.method, endpoint).observe(duration)
    REQUEST_COUNT.labels(request.method, endpoint, response.status_code).inc()
    response.headers["X-Process-Time-Ms"] = f"{duration * 1000:.2f}"
    return response


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/metrics")
def get_metrics():
    return Response(content=generate_latest(), media_type=CONTENT_TYPE_LATEST)


@app.post("/predict", response_model=PredictResponse)
def predict(request: PredictRequest):
    cfg = load_config()
    features = [getattr(request, name) for name in cfg.feature_names]
    try:
        validate_features(features, cfg)
    except DataValidationError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc
    result = get_predictor().predict(features)
    return PredictResponse(**result)

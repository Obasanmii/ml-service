# ml-service

![CI](https://github.com/Obasanmii/ml-service/actions/workflows/ci.yml/badge.svg)

An end-to-end machine learning service built to production conventions: a
model served behind a real API, with input validation, reproducible training,
data-drift monitoring, containerization, and CI. The model itself is
deliberately simple — the focus is the engineering around it.

## Architecture

- **Training** (`src/ml_service/model/train.py`): trains a classifier, scores
  it on held-out data, and saves both the model and a reference sample for
  drift monitoring.
- **Serving** (`src/ml_service/api/main.py`): a FastAPI app that loads the
  model once and serves predictions from named feature inputs.
- **Validation** (`src/ml_service/data/validation.py`): rejects malformed or
  implausible requests before they reach the model.
- **Monitoring** (`src/ml_service/monitoring/drift.py`): a per-feature
  Kolmogorov–Smirnov test that flags when live data drifts from training data.
- **CI** (`.github/workflows/ci.yml`): runs the test suite and builds the
  Docker image on every push.

## Run it locally

```bash
pip install -r requirements.txt
PYTHONPATH=src uvicorn ml_service.api.main:app --reload
```

Then open http://localhost:8000/docs to try the API.

## Test

```bash
pytest -v
```

## Observability

The service instruments every request and exposes operational metrics:

- Each response carries an `X-Process-Time-Ms` header reporting how long the request took.
- `GET /metrics` returns live JSON: total request count, server error count, and
  p50/p95/p99 latency computed over a rolling window of recent requests.

Latency is tracked with percentiles rather than a simple average, since the tail
(p95/p99) is what reflects the slowest requests users actually experience.

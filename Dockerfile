FROM python:3.13-slim

WORKDIR /app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY src ./src
COPY config ./config

ENV PYTHONPATH=/app/src

RUN python -m ml_service.model.train

EXPOSE 8000
CMD ["uvicorn", "ml_service.api.main:app", "--host", "0.0.0.0", "--port", "8000"]

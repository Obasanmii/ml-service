from __future__ import annotations

from pathlib import Path

import yaml
from pydantic import BaseModel

class Config(BaseModel):
    model_path: str = "models/model.joblib"
    reference_data_path: str = "models/reference.csv"
    feature_names: list[str] = ["sepal_length", "sepal_width", "petal_length", "petal_width"]
    target_names: list[str] = ["setosa", "versicolor", "virginica"]
    drift_threshold: float = 0.1
    feature_bounds: dict[str, list[float]] = {
        "sepal_length" : [3.0, 10.0],
        "sepal_width": [1.0, 7.0],
        "petal_length": [0.5, 10.0],
        "petal_width": [0.1, 5.0],
        }

def load_config(path: str = "config/config.yaml") -> Config:
    p = Path(path)
    if p.exists():
        data = yaml.safe_load(p.read_text()) or {}
        return Config(**data)
    return Config()
import os
from datetime import datetime, timezone
from pathlib import Path
from uuid import uuid4

import psycopg2
import torch
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from prometheus_fastapi_instrumentator import Instrumentator

from .model import RiskClassifier
from .train import run_training

app = FastAPI(title="ML Service", version="0.2.0")

MODEL_PATH = os.getenv("ML_MODEL_PATH", "app/models/risk_model.pt")
DATASET_PATH = os.getenv("ML_DATASET_PATH", "app/datasets/cve_attack_training.csv")

model = RiskClassifier()
model_version = "bootstrap"
last_metrics = {"precision": 0.0, "recall": 0.0, "f1": 0.0, "samples": 0}


class FeaturesIn(BaseModel):
    values: list[float]


class TrainRequest(BaseModel):
    epochs: int = 20
    dataset_path: str = DATASET_PATH


def _db_conn():
    return psycopg2.connect(
        host="postgres",
        dbname=os.getenv("POSTGRES_DB", "threat_modeling"),
        user=os.getenv("POSTGRES_USER", "tm_user"),
        password=os.getenv("POSTGRES_PASSWORD", "tm_pass"),
        port=os.getenv("POSTGRES_PORT", "5432"),
    )


def _load_model_if_exists() -> bool:
    path = Path(MODEL_PATH)
    if not path.exists():
        return False

    state = torch.load(path, map_location="cpu")
    model.load_state_dict(state)
    model.eval()
    return True


def _store_ml_run(metrics: dict, dataset_ref: str, version: str) -> None:
    run_id = str(uuid4())
    with _db_conn() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO ml_runs (id, model_name, model_version, dataset_ref, precision_score, recall_score, f1_score, metadata)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s::jsonb)
                """,
                (
                    run_id,
                    "risk-classifier",
                    version,
                    dataset_ref,
                    metrics["precision"],
                    metrics["recall"],
                    metrics["f1"],
                    '{"pipeline":"cve-attack-retrain"}',
                ),
            )
        conn.commit()


@app.on_event("startup")
def startup_load_model():
    _load_model_if_exists()


@app.get("/health")
def health():
    return {
        "status": "ok",
        "service": "ml-service",
        "framework": "pytorch",
        "model_version": model_version,
    }


@app.get("/model/info")
def model_info():
    return {
        "model_version": model_version,
        "model_path": MODEL_PATH,
        "last_metrics": last_metrics,
    }


@app.post("/train")
def train_model(payload: TrainRequest):
    global model, model_version, last_metrics

    try:
        trained_model, metrics = run_training(
            epochs=payload.epochs,
            dataset_path=payload.dataset_path,
            model_out_path=MODEL_PATH,
        )
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Training failed: {exc}") from exc

    model = trained_model
    model.eval()

    model_version = datetime.now(timezone.utc).strftime("%Y%m%d%H%M%S")
    last_metrics = metrics

    try:
        _store_ml_run(metrics, payload.dataset_path, model_version)
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Trained but failed to persist run: {exc}") from exc

    return {
        "status": "trained",
        "model_version": model_version,
        "metrics": metrics,
    }


@app.post("/predict")
def predict(payload: FeaturesIn):
    if len(payload.values) != 8:
        raise HTTPException(status_code=400, detail="Expected 8 features")

    x = torch.tensor([payload.values], dtype=torch.float32)
    with torch.no_grad():
        logits = model(x)
        probs = torch.softmax(logits, dim=1).tolist()[0]
        pred = int(torch.argmax(logits, dim=1).item())

    labels = ["low", "medium", "high"]
    return {
        "predicted_class": labels[pred],
        "confidence": max(probs),
        "probabilities": dict(zip(labels, probs)),
        "model_version": model_version,
    }


Instrumentator().instrument(app).expose(app)

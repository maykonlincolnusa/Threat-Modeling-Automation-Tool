from __future__ import annotations

from pathlib import Path

import pandas as pd
import torch
import torch.nn as nn
import torch.optim as optim
from sklearn.metrics import precision_recall_fscore_support
from sklearn.model_selection import train_test_split

from .model import RiskClassifier

LABELS = ["low", "medium", "high"]
LABEL_TO_ID = {name: idx for idx, name in enumerate(LABELS)}


def run_training(
    epochs: int = 20,
    dataset_path: str = "app/datasets/cve_attack_training.csv",
    model_out_path: str = "app/models/risk_model.pt",
):
    data = pd.read_csv(dataset_path)

    feature_cols = [
        "feature_exposure",
        "feature_complexity",
        "feature_auth_gap",
        "feature_data_sensitivity",
        "feature_network_surface",
        "feature_third_party",
        "feature_misconfig",
        "feature_monitoring_gap",
    ]

    x = data[feature_cols].values
    y = data["label"].map(LABEL_TO_ID).values

    x_train, x_val, y_train, y_val = train_test_split(
        x, y, test_size=0.25, random_state=42, stratify=y
    )

    x_train = torch.tensor(x_train, dtype=torch.float32)
    y_train = torch.tensor(y_train, dtype=torch.long)
    x_val = torch.tensor(x_val, dtype=torch.float32)

    model = RiskClassifier(input_dim=len(feature_cols), hidden_dim=24, classes=3)
    criterion = nn.CrossEntropyLoss()
    optimizer = optim.Adam(model.parameters(), lr=1e-3)

    model.train()
    for _ in range(epochs):
        logits = model(x_train)
        loss = criterion(logits, y_train)
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

    model.eval()
    with torch.no_grad():
        preds = torch.argmax(model(x_val), dim=1).cpu().numpy()

    precision, recall, f1, _ = precision_recall_fscore_support(
        y_val, preds, average="weighted", zero_division=0
    )

    model_path = Path(model_out_path)
    model_path.parent.mkdir(parents=True, exist_ok=True)
    torch.save(model.state_dict(), model_path)

    metrics = {
        "precision": float(round(precision, 4)),
        "recall": float(round(recall, 4)),
        "f1": float(round(f1, 4)),
        "samples": int(len(data)),
        "model_path": str(model_path),
    }

    return model, metrics

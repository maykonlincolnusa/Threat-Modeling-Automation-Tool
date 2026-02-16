import torch
import torch.nn as nn


class RiskClassifier(nn.Module):
    def __init__(self, input_dim: int = 8, hidden_dim: int = 16, classes: int = 3):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(input_dim, hidden_dim),
            nn.ReLU(),
            nn.Dropout(0.2),
            nn.Linear(hidden_dim, classes),
        )

    def forward(self, x):
        return self.net(x)

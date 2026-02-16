from fastapi import FastAPI
from prometheus_fastapi_instrumentator import Instrumentator

from .routers import auth, health, orchestration

app = FastAPI(title="Threat Modeling API Gateway", version="0.2.0")
app.include_router(health.router, tags=["health"])
app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(orchestration.router, prefix="/v1", tags=["orchestration"])

Instrumentator().instrument(app).expose(app)

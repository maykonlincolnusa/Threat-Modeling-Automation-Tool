import os
from datetime import datetime, timezone
from uuid import uuid4

import httpx
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel

from ..messaging import ThreatQueuePublisher
from ..security import UserClaims, require_roles

router = APIRouter()

ASSET_SERVICE_URL = f"http://asset-service:{os.getenv('ASSET_SERVICE_PORT', '8001')}"
THREAT_ENGINE_URL = f"http://threat-engine-service:{os.getenv('THREAT_ENGINE_PORT', '8002')}"
ML_SERVICE_URL = f"http://ml-service:{os.getenv('ML_SERVICE_PORT', '8003')}"


class ThreatSubmission(BaseModel):
    asset_id: str
    category: str
    description: str
    likelihood: float
    impact: float


@router.get("/overview")
async def overview(_user: UserClaims = Depends(require_roles(["viewer", "analyst", "admin"]))):
    async with httpx.AsyncClient(timeout=5.0) as client:
        try:
            assets = (await client.get(f"{ASSET_SERVICE_URL}/assets")).json()
            threats = (await client.get(f"{THREAT_ENGINE_URL}/threats")).json()
            ml_health = (await client.get(f"{ML_SERVICE_URL}/health")).json()
        except Exception as exc:
            raise HTTPException(status_code=503, detail=str(exc)) from exc

    return {
        "assets_count": len(assets),
        "threats_count": len(threats),
        "ml_service": ml_health,
    }


@router.post("/threats/submit")
def submit_threat_event(
    payload: ThreatSubmission,
    user: UserClaims = Depends(require_roles(["analyst", "admin"])),
):
    event_id = str(uuid4())
    message = {
        "event_id": event_id,
        "created_by": user.sub,
        "created_at": datetime.now(timezone.utc).isoformat(),
        **payload.model_dump(),
    }

    try:
        ThreatQueuePublisher().publish(message)
    except Exception as exc:
        raise HTTPException(status_code=503, detail=f"Queue publish failed: {exc}") from exc

    return {"status": "queued", "event_id": event_id, "queue": os.getenv("THREAT_QUEUE_NAME", "threats.ingest")}

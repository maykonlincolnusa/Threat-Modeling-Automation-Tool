import json
import os
from uuid import uuid4

import psycopg2
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from prometheus_fastapi_instrumentator import Instrumentator

app = FastAPI(title="Asset Service", version="0.1.0")


class AssetIn(BaseModel):
    name: str
    asset_type: str
    business_criticality: str
    owner: str | None = None
    tags: list[str] = Field(default_factory=list)


def _db_conn():
    return psycopg2.connect(
        host="postgres",
        dbname=os.getenv("POSTGRES_DB", "threat_modeling"),
        user=os.getenv("POSTGRES_USER", "tm_user"),
        password=os.getenv("POSTGRES_PASSWORD", "tm_pass"),
        port=os.getenv("POSTGRES_PORT", "5432"),
    )


@app.get("/health")
def health():
    return {"status": "ok", "service": "asset-service"}


@app.get("/assets")
def list_assets():
    try:
        with _db_conn() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    SELECT id::text, name, asset_type, business_criticality, owner, tags
                    FROM assets
                    ORDER BY created_at DESC
                    """
                )
                rows = cur.fetchall()
    except Exception as exc:
        raise HTTPException(status_code=503, detail=f"DB error: {exc}") from exc

    return [
        {
            "id": row[0],
            "name": row[1],
            "asset_type": row[2],
            "business_criticality": row[3],
            "owner": row[4],
            "tags": row[5],
        }
        for row in rows
    ]


@app.post("/assets")
def create_asset(payload: AssetIn):
    asset_id = str(uuid4())
    try:
        with _db_conn() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    INSERT INTO assets (id, name, asset_type, business_criticality, owner, tags)
                    VALUES (%s, %s, %s, %s, %s, %s::jsonb)
                    RETURNING id::text, name, asset_type, business_criticality, owner, tags
                    """,
                    (
                        asset_id,
                        payload.name,
                        payload.asset_type,
                        payload.business_criticality,
                        payload.owner,
                        json.dumps(payload.tags),
                    ),
                )
                row = cur.fetchone()
            conn.commit()
    except Exception as exc:
        raise HTTPException(status_code=503, detail=f"DB error: {exc}") from exc

    return {
        "id": row[0],
        "name": row[1],
        "asset_type": row[2],
        "business_criticality": row[3],
        "owner": row[4],
        "tags": row[5],
    }


Instrumentator().instrument(app).expose(app)

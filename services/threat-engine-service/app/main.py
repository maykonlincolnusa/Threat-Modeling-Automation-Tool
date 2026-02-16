import json
import os
import threading
import time
from uuid import uuid4

import pika
import psycopg2
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from prometheus_fastapi_instrumentator import Instrumentator

app = FastAPI(title="Threat Engine Service", version="0.2.0")

RABBITMQ_HOST = os.getenv("RABBITMQ_HOST", "rabbitmq")
RABBITMQ_PORT = int(os.getenv("RABBITMQ_PORT", "5672"))
RABBITMQ_USER = os.getenv("RABBITMQ_USER", "tm_user")
RABBITMQ_PASSWORD = os.getenv("RABBITMQ_PASSWORD", "tm_pass")
THREAT_QUEUE = os.getenv("THREAT_QUEUE_NAME", "threats.ingest")

_consumer_started = False


class ThreatIn(BaseModel):
    asset_id: str
    category: str
    description: str
    likelihood: float
    impact: float


def _db_conn():
    return psycopg2.connect(
        host="postgres",
        dbname=os.getenv("POSTGRES_DB", "threat_modeling"),
        user=os.getenv("POSTGRES_USER", "tm_user"),
        password=os.getenv("POSTGRES_PASSWORD", "tm_pass"),
        port=os.getenv("POSTGRES_PORT", "5432"),
    )


def _insert_threat(payload: dict):
    threat_id = str(uuid4())
    with _db_conn() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO threat_scenarios (id, asset_id, framework, category, description, likelihood, impact, status)
                VALUES (%s, %s, 'STRIDE', %s, %s, %s, %s, 'open')
                RETURNING id::text, asset_id::text, category, description, likelihood, impact, risk_score, status
                """,
                (
                    threat_id,
                    payload["asset_id"],
                    payload["category"],
                    payload["description"],
                    payload["likelihood"],
                    payload["impact"],
                ),
            )
            row = cur.fetchone()
        conn.commit()

    return {
        "id": row[0],
        "asset_id": row[1],
        "category": row[2],
        "description": row[3],
        "likelihood": float(row[4]),
        "impact": float(row[5]),
        "risk_score": float(row[6]),
        "status": row[7],
    }


def _consume_loop():
    credentials = pika.PlainCredentials(RABBITMQ_USER, RABBITMQ_PASSWORD)

    while True:
        try:
            connection = pika.BlockingConnection(
                pika.ConnectionParameters(host=RABBITMQ_HOST, port=RABBITMQ_PORT, credentials=credentials)
            )
            channel = connection.channel()
            channel.queue_declare(queue=THREAT_QUEUE, durable=True)

            def _handler(ch, method, _properties, body):
                try:
                    payload = json.loads(body.decode("utf-8"))
                    _insert_threat(payload)
                    ch.basic_ack(delivery_tag=method.delivery_tag)
                except Exception:
                    ch.basic_nack(delivery_tag=method.delivery_tag, requeue=False)

            channel.basic_qos(prefetch_count=5)
            channel.basic_consume(queue=THREAT_QUEUE, on_message_callback=_handler)
            channel.start_consuming()
        except Exception:
            time.sleep(5)


@app.on_event("startup")
def start_consumer():
    global _consumer_started
    if _consumer_started:
        return

    thread = threading.Thread(target=_consume_loop, daemon=True)
    thread.start()
    _consumer_started = True


@app.get("/health")
def health():
    return {
        "status": "ok",
        "service": "threat-engine-service",
        "queue": THREAT_QUEUE,
        "consumer_started": _consumer_started,
    }


@app.get("/threats")
def list_threats():
    try:
        with _db_conn() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    SELECT id::text, asset_id::text, category, description, likelihood, impact, risk_score, status
                    FROM threat_scenarios
                    ORDER BY created_at DESC
                    """
                )
                rows = cur.fetchall()
    except Exception as exc:
        raise HTTPException(status_code=503, detail=f"DB error: {exc}") from exc

    return [
        {
            "id": row[0],
            "asset_id": row[1],
            "category": row[2],
            "description": row[3],
            "likelihood": float(row[4]),
            "impact": float(row[5]),
            "risk_score": float(row[6]),
            "status": row[7],
        }
        for row in rows
    ]


@app.post("/threats")
def create_threat(payload: ThreatIn):
    try:
        return _insert_threat(payload.model_dump())
    except Exception as exc:
        raise HTTPException(status_code=503, detail=f"DB error: {exc}") from exc


Instrumentator().instrument(app).expose(app)

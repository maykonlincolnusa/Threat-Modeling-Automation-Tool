# Threat Modeling Automation Tool

A foundational platform for threat modeling automation with a microservices architecture, deep learning, an operational dashboard, and MCP support.

## Architecture

- `api-gateway`: HTTP entrypoint, JWT + RBAC, and event publishing.
- `asset-service`: asset registration and inventory (PostgreSQL).
- `threat-engine-service`: threat engine with RabbitMQ consumer and persistence.
- `ml-service`: deep learning model training/inference (PyTorch) with CVE/ATT&CK retraining.
- `dashboard-service`: monitoring dashboard (Streamlit).
- `mcp-server`: MCP server for threat modeling tools.
- `postgres`: relational persistence.
- `rabbitmq`: asynchronous messaging between services.
- `redis`: auxiliary cache/light queue.
- `prometheus` + `grafana`: observability.

## Security (JWT + RBAC)

Login endpoint:

```bash
curl -X POST http://localhost:8000/auth/token \
  -H "Content-Type: application/json" \
  -d '{"username":"analyst","password":"analyst123"}'
```

Demo users:
- `viewer` / `viewer123`
- `analyst` / `analyst123`
- `admin` / `admin123`

## Asynchronous Queue (RabbitMQ)

Submit threats asynchronously through the gateway:

```bash
curl -X POST http://localhost:8000/v1/threats/submit \
  -H "Authorization: Bearer <TOKEN>" \
  -H "Content-Type: application/json" \
  -d '{
    "asset_id":"00000000-0000-0000-0000-000000000001",
    "category":"Tampering",
    "description":"Tampering detected in API payload",
    "likelihood":0.6,
    "impact":0.7
  }'
```

The `threat-engine-service` consumes from the `threats.ingest` queue and persists data in PostgreSQL.

## Deep Learning (CVE/ATT&CK Retraining)

Base dataset: `services/ml-service/app/datasets/cve_attack_training.csv`

Trigger retraining:

```bash
curl -X POST http://localhost:8003/train \
  -H "Content-Type: application/json" \
  -d '{"epochs":25}'
```

Inspect model info:

```bash
curl http://localhost:8003/model/info
```

## Run the Stack

1. Copy `.env.example` to `.env`.
2. Run `docker compose up --build`.
3. Access:
   - API Gateway: `http://localhost:8000/docs`
   - RabbitMQ UI: `http://localhost:15672` (`tm_user/tm_pass`)
   - Dashboard: `http://localhost:8501`
   - Prometheus: `http://localhost:9090`
   - Grafana: `http://localhost:3000` (`admin/admin`)

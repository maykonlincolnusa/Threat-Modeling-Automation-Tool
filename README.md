<div align="center">

# 🔐 Threat Modeling Automation Tool

### *AI-Powered Threat Analysis & Security Intelligence Platform*

[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![Docker](https://img.shields.io/badge/Docker-Compose-2496ED.svg)](https://docs.docker.com/compose/)
[![PyTorch](https://img.shields.io/badge/PyTorch-2.0+-red.svg)](https://pytorch.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-green.svg)](https://fastapi.tiangolo.com/)
[![RabbitMQ](https://img.shields.io/badge/RabbitMQ-3.12-orange.svg)](https://www.rabbitmq.com/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

**[Features](#-key-features)** •
**[Architecture](#-architecture)** •
**[Quick Start](#-quick-start)** •
**[API Reference](#-api-reference)** •
**[Security](#-security-jwt--rbac)** •
**[Monitoring](#-monitoring--observability)**

---

</div>

## 🌟 Overview

The **Threat Modeling Automation Tool** is an enterprise-grade platform that combines modern microservices architecture with deep learning to automate and enhance threat modeling processes. Built for security teams, DevSecOps engineers, and risk analysts, it provides intelligent threat detection, automated risk assessment, and comprehensive security insights.

### 🎯 What Makes This Special?

🧠 **AI-Powered Analysis**
- Deep learning models trained on CVE and ATT&CK datasets
- Automated threat categorization and risk scoring
- Continuous model retraining with new security intelligence
- PyTorch-based neural networks for pattern recognition

🏗️ **Microservices Architecture**
- Fully containerized with Docker Compose
- Event-driven design with RabbitMQ
- Horizontal scalability for enterprise workloads
- Independent service deployment and updates

🔐 **Enterprise Security**
- JWT authentication with role-based access control (RBAC)
- Three-tier permission system (Viewer, Analyst, Admin)
- Secure API gateway with request validation
- Encrypted communication between services

📊 **Real-Time Monitoring**
- Live Streamlit dashboard for threat visualization
- Prometheus metrics collection
- Grafana dashboards for observability
- Real-time event streaming and alerts

🔌 **MCP Integration**
- Model Context Protocol (MCP) server support
- Seamless integration with security tools
- Extensible plugin architecture
- Automated threat model generation

---

## ✨ Key Features

### 🎯 Threat Intelligence
- **Automated Threat Detection**: AI-powered identification of security risks
- **STRIDE Framework**: Complete coverage of Spoofing, Tampering, Repudiation, Information Disclosure, Denial of Service, and Elevation of Privilege
- **Risk Scoring**: Automated likelihood and impact assessment
- **Threat Database**: Comprehensive PostgreSQL storage with full audit trails

### 🤖 Machine Learning
- **Deep Neural Networks**: PyTorch models for threat classification
- **CVE Integration**: Training on Common Vulnerabilities and Exposures data
- **ATT&CK Mapping**: MITRE ATT&CK framework alignment
- **Continuous Learning**: Automated retraining on new threat intelligence
- **Model Versioning**: Track and rollback ML model versions

### 🔄 Asynchronous Processing
- **RabbitMQ Integration**: High-throughput message queuing
- **Event-Driven Architecture**: Decoupled services for better scalability
- **Async API Endpoints**: Non-blocking threat submission
- **Dead Letter Queues**: Robust error handling and retry mechanisms

### 📈 Asset Management
- **Asset Inventory**: Centralized tracking of all system components
- **Dependency Mapping**: Understand relationships between assets
- **Risk Profiles**: Per-asset threat exposure analysis
- **Compliance Tracking**: Regulatory requirement monitoring

---

## 🏗️ Architecture

### System Components

```
┌─────────────────────────────────────────────────────────────────┐
│                         API Gateway                              │
│              (JWT Auth, RBAC, Request Routing)                   │
└─────────────────────┬───────────────────────────────────────────┘
                      │
        ┌─────────────┼─────────────┬──────────────┬──────────────┐
        │             │             │              │              │
        ▼             ▼             ▼              ▼              ▼
┌──────────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐
│    Asset     │ │  Threat  │ │    ML    │ │Dashboard │ │   MCP    │
│   Service    │ │  Engine  │ │ Service  │ │ Service  │ │  Server  │
└──────┬───────┘ └────┬─────┘ └────┬─────┘ └────┬─────┘ └──────────┘
       │              │            │            │
       └──────┬───────┴────────────┴────────────┘
              │
      ┌───────┴────────┬──────────────┬─────────────┐
      ▼                ▼              ▼             ▼
┌──────────┐    ┌──────────┐   ┌──────────┐  ┌──────────┐
│PostgreSQL│    │ RabbitMQ │   │  Redis   │  │Prometheus│
└──────────┘    └──────────┘   └──────────┘  └────┬─────┘
                                                   │
                                                   ▼
                                             ┌──────────┐
                                             │ Grafana  │
                                             └──────────┘
```

### 📦 Service Descriptions

| Service | Technology | Purpose |
|---------|-----------|---------|
| **API Gateway** | FastAPI | HTTP entrypoint, authentication, authorization, request routing |
| **Asset Service** | FastAPI + PostgreSQL | Asset registration, inventory management, dependency tracking |
| **Threat Engine** | FastAPI + RabbitMQ | Threat processing, risk analysis, STRIDE categorization |
| **ML Service** | FastAPI + PyTorch | Deep learning inference, model training, CVE/ATT&CK integration |
| **Dashboard** | Streamlit | Real-time monitoring, threat visualization, analytics |
| **MCP Server** | Python | Model Context Protocol implementation for tool integration |
| **PostgreSQL** | PostgreSQL 15 | Primary data store for all services |
| **RabbitMQ** | RabbitMQ 3.12 | Message broker for async processing |
| **Redis** | Redis 7 | Caching layer and lightweight queuing |
| **Prometheus** | Prometheus | Metrics collection and time-series database |
| **Grafana** | Grafana | Observability dashboards and alerting |

---

## 🚀 Quick Start

### Prerequisites

- Docker 20.10+ and Docker Compose 2.0+
- 4GB+ RAM available for containers
- Ports 8000-8004, 5432, 5672, 6379, 9090, 3000, 8501, 15672 available

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/maykonlincolnusa/Threat-Modeling-Automation-Tool.git
cd Threat-Modeling-Automation-Tool
```

### 2️⃣ Configure Environment

```bash
cp .env.example .env
```

Edit `.env` with your preferred settings:

```bash
# Database
POSTGRES_USER=threat_user
POSTGRES_PASSWORD=threat_pass
POSTGRES_DB=threat_modeling

# RabbitMQ
RABBITMQ_USER=tm_user
RABBITMQ_PASSWORD=tm_pass

# JWT Secret (change in production!)
JWT_SECRET_KEY=your-super-secret-jwt-key-change-in-production

# Service Ports
API_GATEWAY_PORT=8000
ASSET_SERVICE_PORT=8001
THREAT_ENGINE_PORT=8002
ML_SERVICE_PORT=8003
MCP_SERVER_PORT=8004
DASHBOARD_PORT=8501
```

### 3️⃣ Launch the Platform

```bash
docker compose up --build
```

Wait for all services to start (approximately 2-3 minutes on first run).

### 4️⃣ Access the Services

| Service | URL | Credentials |
|---------|-----|-------------|
| **API Gateway** | http://localhost:8000/docs | See authentication section |
| **Dashboard** | http://localhost:8501 | No auth required |
| **RabbitMQ Management** | http://localhost:15672 | tm_user / tm_pass |
| **Grafana** | http://localhost:3000 | admin / admin |
| **Prometheus** | http://localhost:9090 | No auth required |

---

## 🔐 Security (JWT + RBAC)

### Authentication Flow

The platform uses JWT (JSON Web Tokens) for stateless authentication with three role levels:

| Role | Permissions | Use Case |
|------|-------------|----------|
| **Viewer** | Read-only access to threats and assets | Stakeholders, management |
| **Analyst** | Read + Write threats, submit for analysis | Security analysts, DevSecOps |
| **Admin** | Full access including user management | Security team leads, administrators |

### Getting an Access Token

**Endpoint:** `POST /auth/token`

```bash
curl -X POST http://localhost:8000/auth/token \
  -H "Content-Type: application/json" \
  -d '{
    "username": "analyst",
    "password": "analyst123"
  }'
```

**Response:**

```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "role": "analyst"
}
```

### Demo User Accounts

| Username | Password | Role | Description |
|----------|----------|------|-------------|
| `viewer` | `viewer123` | Viewer | Read-only access |
| `analyst` | `analyst123` | Analyst | Standard security analyst |
| `admin` | `admin123` | Admin | Full administrative access |

⚠️ **Production Warning**: Change these credentials immediately in production environments!

### Using the Token

Include the JWT token in the `Authorization` header:

```bash
curl -X GET http://localhost:8000/v1/assets \
  -H "Authorization: Bearer YOUR_TOKEN_HERE"
```

---

## 📡 API Reference

### Asset Management

#### Create Asset

```bash
curl -X POST http://localhost:8000/v1/assets \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Web Application Server",
    "type": "server",
    "description": "Production web application backend",
    "criticality": "high",
    "environment": "production"
  }'
```

#### List Assets

```bash
curl -X GET http://localhost:8000/v1/assets \
  -H "Authorization: Bearer $TOKEN"
```

#### Get Asset Details

```bash
curl -X GET http://localhost:8000/v1/assets/{asset_id} \
  -H "Authorization: Bearer $TOKEN"
```

### Threat Submission

#### Submit Threat (Asynchronous)

```bash
curl -X POST http://localhost:8000/v1/threats/submit \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "asset_id": "00000000-0000-0000-0000-000000000001",
    "category": "Tampering",
    "description": "Potential API payload manipulation detected",
    "likelihood": 0.6,
    "impact": 0.7,
    "mitigation": "Implement input validation and request signing"
  }'
```

**Response:**

```json
{
  "message": "Threat submitted for processing",
  "task_id": "550e8400-e29b-41d4-a716-446655440000"
}
```

#### Get Threats

```bash
curl -X GET http://localhost:8000/v1/threats \
  -H "Authorization: Bearer $TOKEN"
```

### Machine Learning

#### Trigger Model Retraining

```bash
curl -X POST http://localhost:8003/train \
  -H "Content-Type: application/json" \
  -d '{
    "epochs": 25,
    "batch_size": 32,
    "learning_rate": 0.001
  }'
```

#### Get Model Information

```bash
curl http://localhost:8003/model/info
```

**Response:**

```json
{
  "model_type": "ThreatClassifier",
  "version": "1.0.0",
  "last_trained": "2026-02-16T10:30:00Z",
  "accuracy": 0.94,
  "parameters": 124500,
  "classes": ["Spoofing", "Tampering", "Repudiation", "Information Disclosure", "Denial of Service", "Elevation of Privilege"]
}
```

#### Predict Threat Category

```bash
curl -X POST http://localhost:8003/predict \
  -H "Content-Type: application/json" \
  -d '{
    "description": "Unauthorized access attempt to admin panel",
    "features": {
      "source_ip": "192.168.1.100",
      "failed_attempts": 15,
      "time_window": 300
    }
  }'
```

---

## 🔄 Asynchronous Processing with RabbitMQ

### Queue Architecture

The platform uses RabbitMQ for decoupled, scalable threat processing:

```
API Gateway → [threats.ingest] → Threat Engine → PostgreSQL
                     ↓
              [ml.inference] → ML Service
                     ↓
              [notifications]
```

### Message Flow

1. **Threat Submission**: API Gateway publishes to `threats.ingest` queue
2. **Processing**: Threat Engine consumes messages, analyzes threats
3. **ML Inference**: Complex threats routed to ML Service via `ml.inference`
4. **Persistence**: Results stored in PostgreSQL
5. **Notifications**: Critical threats published to `notifications` queue

### Monitoring Queues

Access RabbitMQ Management UI at http://localhost:15672

- **Username**: tm_user
- **Password**: tm_pass

View queue depths, message rates, and consumer status.

---

## 🤖 Deep Learning (CVE/ATT&CK Integration)

### Training Dataset

The ML service uses a curated dataset combining:

- **CVE Database**: Common Vulnerabilities and Exposures
- **MITRE ATT&CK**: Adversarial tactics, techniques, and procedures
- **Custom Threat Intelligence**: Organization-specific threat data

**Location:** `services/ml-service/app/datasets/cve_attack_training.csv`

### Model Architecture

```python
ThreatClassifier(
  input_dim=128,
  hidden_layers=[256, 128, 64],
  num_classes=6,  # STRIDE categories
  dropout=0.3
)
```

### Retraining Process

#### 1. Prepare Training Data

Add new samples to `cve_attack_training.csv`:

```csv
threat_description,category,severity,cve_id,attack_technique
SQL injection in login form,Tampering,high,CVE-2024-1234,T1190
XSS in comment section,Information Disclosure,medium,CVE-2024-5678,T1059
```

#### 2. Trigger Training

```bash
curl -X POST http://localhost:8003/train \
  -H "Content-Type: application/json" \
  -d '{
    "epochs": 25,
    "batch_size": 32,
    "learning_rate": 0.001,
    "validation_split": 0.2
  }'
```

#### 3. Monitor Training Progress

```bash
curl http://localhost:8003/train/status
```

#### 4. Evaluate Model

```bash
curl http://localhost:8003/model/evaluate
```

**Response:**

```json
{
  "accuracy": 0.94,
  "precision": 0.92,
  "recall": 0.91,
  "f1_score": 0.915,
  "confusion_matrix": [[...]]
}
```

### Model Deployment

Trained models are automatically versioned and can be rolled back:

```bash
# List model versions
curl http://localhost:8003/models/versions

# Rollback to previous version
curl -X POST http://localhost:8003/models/rollback/{version_id}
```

---

## 📊 Monitoring & Observability

### Streamlit Dashboard

**URL:** http://localhost:8501

Features:
- 📈 Real-time threat statistics
- 🎯 STRIDE category distribution
- 🔥 Heat maps of asset criticality
- 📉 Trend analysis over time
- 🚨 Active threat alerts
- 📊 Risk score visualization

### Prometheus Metrics

**URL:** http://localhost:9090

Available metrics:
- `threat_submissions_total`: Total threats submitted
- `threat_processing_duration_seconds`: Processing time histogram
- `ml_inference_requests_total`: ML service requests
- `model_prediction_accuracy`: Current model accuracy
- `rabbitmq_queue_depth`: Message queue depth
- `http_request_duration_seconds`: API latency

### Grafana Dashboards

**URL:** http://localhost:3000 (admin/admin)

Pre-configured dashboards:
1. **Threat Overview**: High-level threat statistics
2. **ML Performance**: Model accuracy and inference metrics
3. **Service Health**: Container resource usage
4. **Queue Monitoring**: RabbitMQ message flow
5. **API Performance**: Request rates and latencies

---

## 🗂️ Database Schema

### PostgreSQL Tables

#### Assets Table

```sql
CREATE TABLE assets (
    id UUID PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    type VARCHAR(50),
    description TEXT,
    criticality VARCHAR(20),
    environment VARCHAR(50),
    created_at TIMESTAMP,
    updated_at TIMESTAMP
);
```

#### Threats Table

```sql
CREATE TABLE threats (
    id UUID PRIMARY KEY,
    asset_id UUID REFERENCES assets(id),
    category VARCHAR(50),
    description TEXT,
    likelihood DECIMAL(3,2),
    impact DECIMAL(3,2),
    risk_score DECIMAL(5,2),
    status VARCHAR(20),
    mitigation TEXT,
    created_at TIMESTAMP,
    updated_at TIMESTAMP
);
```

#### ML Models Table

```sql
CREATE TABLE ml_models (
    id UUID PRIMARY KEY,
    version VARCHAR(50),
    architecture TEXT,
    accuracy DECIMAL(5,4),
    trained_at TIMESTAMP,
    is_active BOOLEAN
);
```

---

## 🔧 Configuration

### Environment Variables

Complete `.env` configuration:

```bash
# Database Configuration
POSTGRES_HOST=postgres
POSTGRES_PORT=5432
POSTGRES_USER=threat_user
POSTGRES_PASSWORD=threat_pass
POSTGRES_DB=threat_modeling

# RabbitMQ Configuration
RABBITMQ_HOST=rabbitmq
RABBITMQ_PORT=5672
RABBITMQ_USER=tm_user
RABBITMQ_PASSWORD=tm_pass
RABBITMQ_VHOST=/

# Redis Configuration
REDIS_HOST=redis
REDIS_PORT=6379
REDIS_PASSWORD=

# JWT Configuration
JWT_SECRET_KEY=your-secret-key-here
JWT_ALGORITHM=HS256
JWT_EXPIRATION_MINUTES=1440

# ML Service Configuration
ML_MODEL_PATH=/app/models
ML_DATASET_PATH=/app/datasets
ML_BATCH_SIZE=32
ML_LEARNING_RATE=0.001

# Prometheus Configuration
PROMETHEUS_PORT=9090

# Grafana Configuration
GRAFANA_PORT=3000
GRAFANA_ADMIN_USER=admin
GRAFANA_ADMIN_PASSWORD=admin
```

---

## 🧪 Development

### Running Tests

```bash
# Unit tests
docker compose run --rm api-gateway pytest tests/unit

# Integration tests
docker compose run --rm api-gateway pytest tests/integration

# All tests with coverage
docker compose run --rm api-gateway pytest --cov=app tests/
```

### Local Development

```bash
# Install dependencies
pip install -r requirements.txt

# Run service locally
cd services/api-gateway
uvicorn app.main:app --reload --port 8000
```

### Adding a New Service

1. Create service directory in `services/`
2. Add Dockerfile and requirements.txt
3. Update docker-compose.yml
4. Add service discovery configuration
5. Update API gateway routing

---

## 🐳 Docker Compose Services

### Service Dependencies

```yaml
version: '3.8'

services:
  postgres:
    image: postgres:15
    # PostgreSQL for all services
  
  rabbitmq:
    image: rabbitmq:3.12-management
    # Message broker
  
  redis:
    image: redis:7-alpine
    # Caching layer
  
  api-gateway:
    depends_on: [postgres, rabbitmq, redis]
    # Main API entry point
  
  asset-service:
    depends_on: [postgres]
    # Asset management
  
  threat-engine:
    depends_on: [postgres, rabbitmq]
    # Threat processing
  
  ml-service:
    depends_on: [postgres]
    # Machine learning
  
  dashboard:
    depends_on: [api-gateway]
    # Streamlit dashboard
  
  prometheus:
    # Metrics collection
  
  grafana:
    depends_on: [prometheus]
    # Visualization
```

---

## 🛠️ Troubleshooting

### Common Issues

#### Services Not Starting

```bash
# Check logs
docker compose logs -f [service-name]

# Restart specific service
docker compose restart [service-name]

# Rebuild and restart
docker compose up --build [service-name]
```

#### Database Connection Issues

```bash
# Check PostgreSQL status
docker compose exec postgres pg_isready

# Connect to database
docker compose exec postgres psql -U threat_user -d threat_modeling
```

#### RabbitMQ Queue Problems

```bash
# Check queue status
docker compose exec rabbitmq rabbitmqctl list_queues

# Purge queue
docker compose exec rabbitmq rabbitmqctl purge_queue threats.ingest
```

#### Memory Issues

```bash
# Check container resource usage
docker stats

# Increase Docker memory limit in Docker Desktop settings
# Recommended: 4GB minimum
```

---

## 🚀 Deployment

### Production Considerations

#### Security
- [ ] Change all default passwords
- [ ] Use strong JWT secret keys
- [ ] Enable HTTPS/TLS
- [ ] Implement network segmentation
- [ ] Enable PostgreSQL SSL
- [ ] Configure firewall rules

#### Scaling
- [ ] Use managed PostgreSQL (AWS RDS, Azure Database)
- [ ] Deploy RabbitMQ cluster
- [ ] Implement Redis Cluster
- [ ] Use Kubernetes for orchestration
- [ ] Configure horizontal pod autoscaling
- [ ] Implement CDN for dashboard

#### Monitoring
- [ ] Set up centralized logging (ELK Stack)
- [ ] Configure alerting in Grafana
- [ ] Implement uptime monitoring
- [ ] Set up error tracking (Sentry)
- [ ] Configure backup automation

### Kubernetes Deployment

```bash
# Coming soon
kubectl apply -f k8s/
```

---

## 📚 API Documentation

Full interactive API documentation available at:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

### API Versioning

The API uses URI versioning:

- `/v1/` - Current stable version
- `/v2/` - Next version (when available)

### Rate Limiting

Default rate limits:
- **Authenticated**: 1000 requests/hour
- **Unauthenticated**: 100 requests/hour

---

## 🤝 Contributing

Contributions are welcome! Please follow these guidelines:

### Development Workflow

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Code Standards

- Follow PEP 8 for Python code
- Add type hints to all functions
- Write docstrings for classes and methods
- Add unit tests for new features
- Update documentation

### Testing

```bash
# Run linting
flake8 services/

# Run type checking
mypy services/

# Run tests
pytest tests/ --cov
```

---

## 🗺️ Roadmap

### Version 1.0 (Current)
- [x] Microservices architecture
- [x] JWT authentication with RBAC
- [x] RabbitMQ async processing
- [x] Deep learning threat classification
- [x] Real-time dashboard
- [x] Prometheus + Grafana monitoring

### Version 2.0 (Planned)
- [ ] Graph database for attack path analysis
- [ ] Advanced ML models (Transformers, Graph Neural Networks)
- [ ] Multi-tenancy support
- [ ] Threat intelligence feed integration
- [ ] Automated penetration testing
- [ ] Compliance framework mapping (NIST, ISO 27001)
- [ ] Mobile app for threat alerts
- [ ] Slack/Teams integration

### Version 3.0 (Future)
- [ ] AI-powered mitigation recommendations
- [ ] Blockchain-based audit trail
- [ ] Zero-trust architecture assessment
- [ ] Supply chain security analysis
- [ ] Quantum-safe cryptography readiness
- [ ] AR/VR threat visualization

---

## 📖 Documentation

### Additional Resources

- [STRIDE Threat Modeling Guide](https://docs.microsoft.com/en-us/azure/security/develop/threat-modeling-tool)
- [MITRE ATT&CK Framework](https://attack.mitre.org/)
- [CVE Database](https://cve.mitre.org/)
- [OWASP Top 10](https://owasp.org/www-project-top-ten/)

### Training Materials

- **Video Tutorials**: Coming soon
- **Blog Posts**: Coming soon
- **Webinars**: Coming soon

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 👨‍💻 Author

**Maykon Lincoln USA**

- GitHub: [@maykonlincolnusa](https://github.com/maykonlincolnusa)
- LinkedIn: [Maykon Lincoln](https://linkedin.com/in/maykonlincolnusa)

---

## 🙏 Acknowledgments

- MITRE Corporation for the ATT&CK Framework
- NIST for cybersecurity guidelines
- OWASP community for security best practices
- Open source contributors

---

## 💬 Support

Need help? Have questions?

- 🐛 [Report Bug](https://github.com/maykonlincolnusa/Threat-Modeling-Automation-Tool/issues)
- 💡 [Request Feature](https://github.com/maykonlincolnusa/Threat-Modeling-Automation-Tool/issues)
- 📧 Email: [maykon_zero@hotmail.com]
- 🌐 maykonlincoln.com [Discussions](https://github.com/maykonlincolnusa/Threat-Modeling-Automation-Tool/discussions)

---

## ⭐ Star History

If you find this project useful, please consider giving it a star!

[![Star History Chart](https://api.star-history.com/svg?repos=maykonlincolnusa/Threat-Modeling-Automation-Tool&type=Date)](https://star-history.com/#maykonlincolnusa/Threat-Modeling-Automation-Tool&Date)

---

<div align="center">

### 🛡️ Built with security in mind

**Protecting systems through intelligent automation**

**[⬆ Back to top](#-threat-modeling-automation-tool)**

</div>

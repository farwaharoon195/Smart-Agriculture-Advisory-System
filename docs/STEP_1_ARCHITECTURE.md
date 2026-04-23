# STEP 1: Project Architecture

## 1) High-Level Components

- **Frontend (React + Vite):** Farmer dashboard with Urdu/English toggle.
- **Backend (Flask REST API):** Business logic and orchestration.
- **PostgreSQL:** Structured transactional data (users, profiles, advisory records).
- **MongoDB:** Unstructured/semi-structured data (weather snapshots, image metadata).
- **ML Services:** Crop recommendation, disease detection, market price prediction.

## 2) Folder Structure

```
Smart-Agriculture-Advisory-System/
├── backend/
│   ├── app/
│   │   ├── api/               # REST endpoints
│   │   ├── core/              # Config, DB initialization, logging
│   │   ├── models/            # SQLAlchemy entities (PostgreSQL)
│   │   ├── repositories/      # Data-access layer
│   │   ├── services/          # Domain services (advisory logic)
│   │   ├── schemas/           # DTOs/validators (expandable)
│   │   ├── ml/                # ML artifacts/pipelines (expandable)
│   │   └── utils/             # shared helpers
│   ├── tests/
│   ├── run.py
│   ├── requirements.txt
│   └── Dockerfile
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   ├── services/          # API client layer
│   │   └── i18n/              # Urdu/English translations
│   ├── index.html
│   ├── package.json
│   └── Dockerfile
├── docs/
│   └── STEP_1_ARCHITECTURE.md
├── docker-compose.yml
└── README.md
```

## 3) Request/Data Flow

1. Farmer interacts with dashboard.
2. Frontend calls Flask API.
3. API routes call domain services.
4. Services read/write PostgreSQL via repositories.
5. Weather/image snapshots can be saved to MongoDB.
6. API returns recommendations/advisories/predictions.

## 4) Core Design Principles

- **Clean architecture layers:** API -> Service -> Repository -> DB.
- **OOP + SOLID:** Each service handles one responsibility.
- **Extensibility:** Rule-based modules can be replaced by trained ML models.
- **Observability:** Centralized logging in backend core.
- **Deployment-ready:** Dockerized services with environment-based config.

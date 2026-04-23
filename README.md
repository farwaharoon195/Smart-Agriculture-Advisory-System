# Smart Agriculture Advisory System (Punjab, Pakistan)

Production-oriented full-stack starter for farmer advisory:
- Crop recommendation
- Disease detection (rule-based + pluggable ML)
- Irrigation guidance (weather-driven)
- Market price prediction
- Urdu-ready frontend
- SMS alert simulation

## Quick Start (Docker)
```bash
docker compose up --build
```

- Frontend: http://localhost:5173
- Backend API: http://localhost:8000/api/health

## Local Dev
### Backend
```bash
cd backend
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
python run.py
```

### Frontend
```bash
cd frontend
npm install
npm run dev
```

## Architecture
See `docs/STEP_1_ARCHITECTURE.md`.

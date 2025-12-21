# Calricula Project Context

## Project Overview
**Calricula** is an AI-assisted Curriculum Management System designed for the Los Angeles Community College District (LACCD). It facilitates the creation, modification, and approval of Course Outlines of Record (CORs) and Programs, ensuring compliance with state regulations (Title 5, PCAH).

### Tech Stack
- **Frontend:** Next.js 15 (App Router), Tailwind CSS, Luminous Design System.
- **Backend:** Python FastAPI, SQLModel (ORM), PostgreSQL.
- **AI Integration:** Google Gemini 2.5 Flash, File Search API (RAG).
- **Authentication:** Firebase Authentication (Email/Password).
- **Infrastructure:** Docker Compose.

## Architecture & Directory Structure
```
calricula/
├── backend/                # Python FastAPI backend
│   ├── app/
│   │   ├── api/            # API Route definitions
│   │   ├── core/           # Config, database, security
│   │   ├── models/         # SQLModel database schemas
│   │   ├── services/       # Business logic (Compliance, AI, etc.)
│   │   └── schemas/        # Pydantic models for API request/response
│   ├── alembic/            # Database migrations
│   ├── seeds/              # Data seeding scripts
│   └── tests/              # Pytest suite
├── frontend/               # Next.js frontend
│   ├── src/
│   │   ├── app/            # App Router pages and layouts
│   │   ├── components/     # React components (Luminous Design System)
│   │   ├── contexts/       # React Contexts (Auth, etc.)
│   │   └── lib/            # Utilities and API clients
│   └── e2e/                # Playwright E2E tests
├── calricula_docs/         # Documentation (PRDs, Knowledge Base)
└── docker-compose.yml      # Service orchestration
```

## Development & Usage

### Running the Application
**Recommended:** Use Docker Compose to start the full stack (Frontend, Backend, DB).
```bash
docker-compose up
```
- **Frontend:** http://localhost:3001
- **Backend API:** http://localhost:8001
- **API Docs:** http://localhost:8001/docs

**Local Backend (Manual):**
```bash
cd backend
source venv/bin/activate
uvicorn app.main:app --reload --port 8000
```

**Local Frontend (Manual):**
```bash
cd frontend
npm install
npm run dev
```

### Testing
- **Backend:** `pytest`
- **Frontend (Unit):** `npm test` (Jest)
- **Frontend (E2E):** `npx playwright test`

### Database Management
- **Migrations:** Alembic is used.
  - Create migration: `alembic revision --autogenerate -m "message"`
  - Apply migration: `alembic upgrade head`
- **Seeding:**
  - Run `python -m seeds.seed_all` (from `backend/` dir) to populate initial data.

## Coding Conventions

### Backend (Python)
- **Formatting:** `black`
- **Import Sorting:** `isort`
- **Type Checking:** `mypy`
- **Style:** Adhere to PEP 8. Use strictly typed Pydantic models and SQLModel for DB interactions.

### Frontend (TypeScript/React)
- **Linting:** `npm run lint` (ESLint)
- **Styling:** Tailwind CSS with **Luminous Design System** tokens (e.g., `luminous-card`, `luminous-button-primary`).
- **Structure:** Use Next.js App Router conventions.

## Key Files
- `README.md`: General project info and quick start.
- `CLAUDE.md`: AI assistant context (contains useful detailed info).
- `docker-compose.yml`: Service definitions.
- `backend/app/main.py`: Backend entry point.
- `frontend/next.config.js`: Next.js configuration.

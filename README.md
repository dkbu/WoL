# Museum

Museum is a collaborative, wiki-like knowledge graph. Participants contribute concepts, draw links between them, and assess their reliability. The first release runs as a single self-hosted installation; the architecture is designed to support federation between multiple museums in the future.

---

## Technology stack

| Layer | Technology |
|-------|-----------|
| Backend | Python 3.12, FastAPI, SQLAlchemy 2.x, Alembic |
| Database | PostgreSQL 16 |
| Frontend | React 18, Vite |
| Deployment | Docker Compose, nginx |
| Python env | uv |

---

## Repository structure

```
museum/
├── backend/               Python/FastAPI application
│   ├── pyproject.toml
│   ├── alembic.ini
│   ├── alembic/           Migration scripts
│   └── app/
│       ├── main.py        FastAPI application entry point
│       ├── config.py      Pydantic settings (env-based)
│       ├── db/            SQLAlchemy engine and session
│       ├── models/        ORM models (Base class)
│       ├── schemas/       Pydantic request/response schemas
│       ├── api/           API route handlers
│       └── services/      Business logic
│
├── frontend/              React/Vite frontend
│   ├── package.json
│   ├── vite.config.js
│   └── src/
│
├── docker/
│   ├── backend/Dockerfile
│   └── frontend/Dockerfile + nginx.conf
│
├── compose.yml            Production Docker Compose
├── .env.example           Template for environment variables
└── README.md
```

---

## Local development prerequisites

- **Python 3.12+** with **[uv](https://docs.astral.sh/uv/)** installed
- **Node.js 20+** and **npm**

PostgreSQL is not required for local development. The backend uses a local SQLite
database by default and stores it in `backend/museum.db`.

---

## Local development setup

### 1. Optional: use PostgreSQL instead

The default SQLite database is enough for local development. To use PostgreSQL,
set `DB_URL` in `backend/.env` instead:

```dotenv
DB_URL=postgresql+psycopg2://museum:your-password@localhost:5432/museum
```

If `DB_URL` is set, it takes precedence over the individual `DB_*` settings.

### 2. Optional: create the PostgreSQL database

Connect to your local PostgreSQL instance and run:

```sql
CREATE DATABASE museum;
CREATE USER museum WITH PASSWORD 'your-password';
GRANT ALL PRIVILEGES ON DATABASE museum TO museum;
```

### 3. Configure environment variables

```powershell
Copy-Item .env.example backend\.env
```

For the default SQLite setup, no database variables are required. Set `DB_URL`
only if you want to use PostgreSQL.

### 4. Install Python dependencies

```powershell
cd backend
uv sync
```

This creates a `.venv` directory inside `backend/` and installs all dependencies.

### 5. Run database migrations

```powershell
# Still inside backend/
uv run alembic upgrade head
```

### 6. Start the backend development server

```powershell
uv run uvicorn app.main:app --reload
```

The API is now available at `http://localhost:8000`.  
Interactive docs: `http://localhost:8000/docs`.

### 7. Install frontend dependencies

Open a second terminal:

```powershell
cd frontend
npm install
```

### 7. Start the frontend development server

```powershell
npm run dev
```

The frontend is now available at `http://localhost:5173`.  
API requests to `/api/*` are proxied to the backend automatically.

---

## Running tests

```powershell
cd backend
uv run pytest
```

---

## Database migrations

Create a new migration after changing models:

```powershell
cd backend
uv run alembic revision --autogenerate -m "describe your change"
uv run alembic upgrade head
```

---

## Production deployment

### Prerequisites

A Linux server with Docker and Docker Compose installed.

### 1. Configure environment variables

```bash
cp .env.example .env
```

Edit `.env` and set a strong `DB_PASSWORD` and any other values appropriate for your environment. **Never commit `.env` to version control.**

### 2. Build and start

```bash
docker compose up -d --build
```

This starts three containers:

| Container | Role |
|-----------|------|
| `db` | PostgreSQL (data persisted in `postgres_data` volume) |
| `backend` | FastAPI application |
| `frontend` | nginx serving the React build, proxying `/api` to backend |

### 3. Run migrations in production

```bash
docker compose exec backend uv run alembic upgrade head
```

### 4. Access the application

The frontend is available on port 80 (configurable via `FRONTEND_PORT` in `.env`).

### Persistent database storage

PostgreSQL data is stored in the named Docker volume `postgres_data`.  
Recreating or updating containers does **not** delete the museum's data.

To back up the database:

```bash
docker compose exec db pg_dump -U museum museum > backup.sql
```

---

## Health check

```
GET /api/health
```

Returns:

```json
{ "status": "ok", "database": "ok" }
```

`database` will be `"unavailable"` if the backend cannot reach PostgreSQL.

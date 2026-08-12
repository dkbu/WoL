# Copilot Prompt: Scaffold the Museum MVP

You are scaffolding a new project called **Museum**.

Museum is a collaborative, wiki-like knowledge graph. A "museum" is an independent installation of the system. The first version runs as a single museum, but the architecture must be suitable for future federation between multiple museums.

Your task at this stage is **ONLY to scaffold the project**. Do not implement the complete application or invent features that are not specified below.

## Goals

Create a clean, maintainable project structure containing:

* A Python/FastAPI backend
* A JavaScript frontend
* PostgreSQL database support
* SQLAlchemy for database access
* Alembic for database migrations
* uv for Python dependency and environment management
* Containerized production deployment using Docker Compose
* Configuration through environment variables
* A clear separation between frontend, backend, and database

The developer environment is Windows, so local development must NOT require Docker, WSL, a virtual machine, or another emulator.

The production/deployment environment will initially target a Linux server capable of running Docker/OCI-compatible containers.

---

# Technology Choices

## Backend

Use:

* Python
* FastAPI
* SQLAlchemy 2.x
* Alembic
* Pydantic
* uv

Use modern Python typing throughout.

Do not use Django.

The backend should expose a REST/JSON API.

## Database

Use PostgreSQL.

Database connection information must come entirely from environment/configuration rather than being hardcoded.

Use SQLAlchemy for database access.

Use Alembic for schema migrations.

Do not use database-specific SQL unless there is a good reason.

## Frontend

Use JavaScript.

React is acceptable and preferred if it makes the project structure cleaner, but do not introduce unnecessary complexity.

The frontend communicates with the backend through its HTTP API.

The frontend must not access PostgreSQL directly.

Production frontend assets should be buildable into static files.

## Containers

Provide a Docker Compose configuration for production/self-hosted deployment.

The Compose setup should contain, at minimum:

* Frontend/web server
* Backend
* PostgreSQL

Database data must be stored in a persistent volume so that recreating containers does not destroy the museum's data.

The application should not depend on Docker during local development.

---

# Project Structure

Use a structure broadly similar to:

```
museum/
├── backend/
│   ├── pyproject.toml
│   ├── uv.lock
│   ├── alembic.ini
│   ├── alembic/
│   └── app/
│       ├── main.py
│       ├── config.py
│       ├── db/
│       ├── models/
│       ├── schemas/
│       ├── api/
│       └── services/
│
├── frontend/
│   ├── package.json
│   ├── src/
│   └── ...
│
├── docker/
│   ├── backend/
│   └── frontend/
│
├── compose.yml
├── .env.example
├── .gitignore
├── README.md
└── ...
```

Adjust the exact structure if there is a strong technical reason, but keep the frontend/backend separation clear.

---

# Initial Backend Requirements

Create a minimal FastAPI application that:

* Starts successfully
* Provides a health-check endpoint
* Loads configuration from environment variables
* Can connect to PostgreSQL
* Has SQLAlchemy configured
* Has Alembic configured
* Can run database migrations
* Has a basic API router structure

For example, provide:

```
GET /api/health
```

which returns a simple JSON response indicating that the backend is running.

Do not implement concept functionality yet.

---

# Initial Database Setup

Set up SQLAlchemy and Alembic so that:

* A database engine/session can be created
* Models can be added cleanly later
* Alembic can detect model changes
* Migrations can be run against PostgreSQL

Do not create the complete Museum data model yet.

A minimal test table may be created only if needed to demonstrate that migrations work.

---

# Initial Frontend

Create a minimal frontend that:

* Starts locally using the chosen JavaScript tooling
* Displays a basic Museum page
* Can call the backend health endpoint
* Displays whether the backend is reachable

Keep the UI extremely simple.

Do not implement the actual Museum interface yet.

---

# Configuration

Create `.env.example` containing configuration needed for local development and production.

At minimum, account for:

* Database host
* Database port
* Database name
* Database user
* Database password
* Backend/API URL
* Application environment

Never commit real secrets.

The application should fail clearly if required configuration is missing.

---

# Local Development

The README must explain how to develop without Docker.

Assume:

* Windows
* uv is installed
* PostgreSQL is installed locally
* Node.js/npm is available if required by the frontend

Document commands for:

1. Installing Python dependencies with uv
2. Creating/using the uv-managed environment
3. Running Alembic migrations
4. Starting the FastAPI development server
5. Installing frontend dependencies
6. Starting the frontend development server

Do not require WSL, Docker, a VM, or another Linux environment for local development.

---

# Production Deployment

Create a Docker Compose configuration suitable as the basis for a self-hosted Museum installation.

The deployment should contain:

```
frontend/web server
      │
      ▼
   backend
      │
      ▼
  PostgreSQL
```

Use persistent storage for PostgreSQL.

Do not expose PostgreSQL publicly.

The backend should communicate with PostgreSQL using the internal Compose network.

The frontend should communicate with the backend appropriately.

Make the setup as simple as reasonably possible for a future Museum operator.

The README should contain basic deployment instructions.

---

# Future Federation Requirements

Federation is NOT implemented now.

However, the architecture must not make federation unnecessarily difficult later.

Keep these requirements in mind when scaffolding:

* Concepts will eventually have globally unique identifiers.
* Users will eventually have globally meaningful identities.
* Comments belong to the creator's museum.
* Links belong to the creator's museum.
* Karma is local to a museum.
* Reliability classifications are local to a museum.
* A future link may connect concepts belonging to different museums.

Do not implement federation APIs, synchronization, ActivityPub, or any other federation protocol yet.

Do not assume that database auto-increment integers are suitable as public/global identifiers.

Prefer UUID/UUIDv7-style identifiers for entities that will eventually be exposed externally.

---

# Development Principles

Keep the initial implementation boring and maintainable.

Do NOT introduce:

* Microservices
* Kubernetes
* Redis
* Message queues
* Graph databases
* Elasticsearch
* Event sourcing
* Complex caching
* Authentication providers
* Cloud-specific services

unless they are genuinely necessary for the scaffold.

The application should initially be a conventional monolithic FastAPI application backed by PostgreSQL.

The conceptual graph does NOT require a graph database.

---

# Code Quality

Use:

* Clear naming
* Type hints
* Small modules
* Dependency injection where appropriate
* Environment-based configuration
* Clear error handling

Avoid:

* Large monolithic files
* Hardcoded credentials
* Global mutable state
* Unnecessary abstractions
* Placeholder code pretending to implement functionality

Add a small number of useful tests demonstrating that:

* The backend starts
* The health endpoint works
* Database configuration works

Do not build a large test suite yet.

---

# README

The README should explain:

1. What Museum is, in one paragraph
2. Technology stack
3. Repository structure
4. Local development prerequisites
5. Local development setup
6. How to run the backend
7. How to run the frontend
8. How to run database migrations
9. How to run the containerized deployment
10. How persistent database storage works

The README should be understandable to a developer who has not previously worked on this project.

---

# Important Constraint

This is a **scaffold task, not an implementation task**.

Do not implement:

* Concepts
* Links
* Comments
* Karma
* Reliability voting
* Watching
* Notifications
* Search
* Federation

except for the minimal structural placeholders necessary to establish the architecture.

The desired result is a clean project that starts successfully and is ready for the first feature to be implemented.

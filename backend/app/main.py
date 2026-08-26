from __future__ import annotations

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.admin import router as admin_router
from app.api.auth import router as auth_router
from app.api.health import router as health_router
from app.api.knowledge import router as knowledge_router
from app.api.users import router as users_router
from app.config import settings

app = FastAPI(
    title="Museum",
    description="Museum backend API",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.backend_cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

prefix = "/api"

app.include_router(health_router, prefix=prefix)
app.include_router(auth_router, prefix=prefix)
app.include_router(knowledge_router, prefix=prefix)
app.include_router(users_router, prefix=prefix)
app.include_router(admin_router, prefix=prefix)

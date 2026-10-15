from __future__ import annotations

from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.api.admin import router as admin_router
from app.api.auth import router as auth_router
from app.api.grouping import router as grouping_router
from app.api.health import router as health_router
from app.api.knowledge import router as knowledge_router
from app.api.users import router as users_router
from app.config import settings
from app.errors import ForbiddenError, NotFoundError

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


@app.exception_handler(NotFoundError)
def not_found_handler(request: Request, exc: NotFoundError) -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND, content={"detail": str(exc)}
    )


@app.exception_handler(ForbiddenError)
def forbidden_handler(request: Request, exc: ForbiddenError) -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_403_FORBIDDEN, content={"detail": str(exc)}
    )


prefix = "/api"

app.include_router(health_router, prefix=prefix)
app.include_router(auth_router, prefix=prefix)
app.include_router(knowledge_router, prefix=prefix)
app.include_router(grouping_router, prefix=prefix)
app.include_router(users_router, prefix=prefix)
app.include_router(admin_router, prefix=prefix)

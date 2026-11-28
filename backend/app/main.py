"""
Royals Intelligence - FastAPI Main Application Entrypoint
"""

from contextlib import asynccontextmanager
from datetime import datetime, timezone
from fastapi import FastAPI, Request, status, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError

from app.core.config import settings
from app.core.logging import logger
from app.api.v1.router import api_router
from app.schemas.health import RootHealthResponse


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup initialization
    logger.info(f"Starting {settings.PROJECT_NAME} API v{settings.APP_VERSION}")
    logger.info(f"Environment: {settings.ENVIRONMENT} | Debug: {settings.DEBUG}")
    logger.info(f"Database Target: {settings.POSTGRES_HOST}:{settings.POSTGRES_PORT}/{settings.POSTGRES_DB}")
    yield
    # Graceful shutdown cleanup
    logger.info(f"Shutting down {settings.PROJECT_NAME} API services.")


app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.APP_VERSION,
    description="Rajasthan Royals Cricket Intelligence, Performance Analytics and IPL 2027 Auction Decision Support Platform.",
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
)

# CORS Security Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_origin_regex=r"^https://.*\.vercel\.app$",
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)


def _get_cors_headers(request: Request) -> dict:
    """Helper to attach permissive CORS headers to exception responses matching allowed origins."""
    origin = request.headers.get("origin")
    if origin and (
        origin in settings.BACKEND_CORS_ORIGINS
        or origin.endswith(".vercel.app")
        or "localhost" in origin
        or "127.0.0.1" in origin
    ):
        return {
            "Access-Control-Allow-Origin": origin,
            "Access-Control-Allow-Credentials": "true",
            "Access-Control-Allow-Headers": "*",
            "Access-Control-Allow-Methods": "GET, POST, PUT, PATCH, DELETE, OPTIONS",
        }
    return {}


# Centralized Exception Handlers (RFC-7807 Problem Details)
@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    headers = _get_cors_headers(request)
    if exc.headers:
        headers.update(exc.headers)
    return JSONResponse(
        status_code=exc.status_code,
        headers=headers,
        content={
            "title": "HTTP Error",
            "status": exc.status_code,
            "detail": exc.detail,
            "instance": request.url.path,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        },
    )


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    logger.warning(f"Request validation failure on {request.url.path}: {exc}")
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        headers=_get_cors_headers(request),
        content={
            "title": "Unprocessable Entity",
            "status": 422,
            "detail": exc.errors(),
            "instance": request.url.path,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        },
    )


@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unhandled server error on {request.url.path}: {exc}", exc_info=True)
    detail_msg = str(exc) if settings.DEBUG else "An unexpected internal server error occurred."
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        headers=_get_cors_headers(request),
        content={
            "title": "Internal Server Error",
            "status": 500,
            "detail": detail_msg,
            "instance": request.url.path,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        },
    )


# Root Health Probe
@app.get(
    "/health",
    response_model=RootHealthResponse,
    tags=["Health & Diagnostics"],
    summary="Root Service Liveness Probe",
    description="Lightweight liveness probe for orchestrators and ingress routers.",
)
async def root_health() -> RootHealthResponse:
    return RootHealthResponse(
        status="healthy",
        project=settings.PROJECT_NAME,
        version=settings.APP_VERSION,
        environment=settings.ENVIRONMENT,
        timestamp=datetime.now(timezone.utc).isoformat(),
    )


# Mount Versioned API Routes (/api/v1)
app.include_router(api_router, prefix=settings.API_V1_PREFIX)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host=settings.HOST, port=settings.PORT, reload=settings.DEBUG)

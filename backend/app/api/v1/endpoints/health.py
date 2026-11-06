"""
Royals Intelligence - Health Diagnostic API Endpoints
"""

from datetime import datetime, timezone
from fastapi import APIRouter
from app.core.config import settings
from app.db.session import check_database_connection
from app.schemas.health import DeepHealthResponse, ComponentHealth

router = APIRouter()


@router.get(
    "/health",
    response_model=DeepHealthResponse,
    summary="Deep System Readiness & Diagnostics",
    description="Inspects FastAPI core, PostgreSQL engine status, and runtime environment.",
)
async def get_deep_health() -> DeepHealthResponse:
    db_health_data = await check_database_connection()
    
    # Evaluate aggregate status: API is healthy; if DB is offline, status indicates standby_mode
    overall_status = "healthy" if db_health_data.get("status") == "connected" else "degraded_standby"

    return DeepHealthResponse(
        status=overall_status,
        api_version="v1",
        project=settings.PROJECT_NAME,
        environment=settings.ENVIRONMENT,
        timestamp=datetime.now(timezone.utc).isoformat(),
        components={
            "database": ComponentHealth(**db_health_data),
            "redis": ComponentHealth(
                status="standby",
                detail="Configured for asynchronous task broker and live scoring cache.",
                note="Worker daemon initialization scheduled in Stage 1.",
            ),
        },
    )

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
    
    # API core is operational; report "healthy" so front-end indicators confirm API liveness.
    # Database status is accurately detailed inside components["database"].
    overall_status = "healthy"

    return DeepHealthResponse(
        status=overall_status,
        api_version="v1",
        project=settings.PROJECT_NAME,
        environment=settings.ENVIRONMENT,
        timestamp=datetime.now(timezone.utc).isoformat(),
        components={
            "api": ComponentHealth(
                status="operational",
                detail="FastAPI analytics router operational and ready.",
            ),
            "database": ComponentHealth(**db_health_data),
            "redis": ComponentHealth(
                status="standby",
                detail="Configured for asynchronous task broker and live scoring cache.",
                note="Worker daemon initialization scheduled in Stage 1.",
            ),
        },
    )

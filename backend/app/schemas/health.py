"""
Royals Intelligence - Health Schemas
Pydantic models for service liveness and readiness diagnostic endpoints.
"""

from typing import Dict, Any, Optional
from pydantic import BaseModel, Field


class RootHealthResponse(BaseModel):
    status: str = Field(..., description="Operational status of the service (e.g. 'healthy')")
    project: str = Field(..., description="Official project identifier")
    version: str = Field(..., description="Application version release tag")
    environment: str = Field(..., description="Deployment environment mode")
    timestamp: str = Field(..., description="ISO 8601 UTC timestamp")


class ComponentHealth(BaseModel):
    status: str
    engine: Optional[str] = None
    latency_ms: Optional[float] = None
    pool_size: Optional[int] = None
    detail: Optional[str] = None
    note: Optional[str] = None


class DeepHealthResponse(BaseModel):
    status: str = Field(..., description="Overall platform operational readiness status")
    api_version: str = Field(..., description="API specification version")
    project: str = Field(..., description="Project name")
    environment: str = Field(..., description="Deployment environment")
    timestamp: str = Field(..., description="ISO 8601 UTC timestamp")
    components: Dict[str, ComponentHealth] = Field(..., description="Subsystem health statuses")

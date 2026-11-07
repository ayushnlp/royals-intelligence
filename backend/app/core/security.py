"""
Royals Intelligence - Server-Side Security & Access Control
Enforces strict server-side authentication, role-based authorization,
and deny-by-default policies. Client-asserted role headers are rejected.
"""

from typing import List, Optional
from pydantic import BaseModel
from fastapi import Header, HTTPException, status, Depends
from app.core.config import settings
from app.core.logging import logger

ROLE_SCOUT_ADMIN = "rr_scout_admin"
ROLE_LEAD_ANALYST = "rr_lead_analyst"
ROLE_PUBLIC = "public"


class AuthenticatedUser(BaseModel):
    """Verified principal identity established by trusted server credentials."""
    user_id: str
    username: str
    roles: List[str]
    auth_method: str

    def has_role(self, role: str) -> bool:
        return role in self.roles


async def get_current_user_optional(
    authorization: Optional[str] = Header(None, alias="Authorization"),
    x_api_key: Optional[str] = Header(None, alias="X-API-Key"),
    x_user_role: Optional[str] = Header(None, alias="x-user-role"),
) -> Optional[AuthenticatedUser]:
    """
    Extracts and verifies server credentials from Authorization (Bearer) or X-API-Key headers.
    Security Boundary:
    - Never trusts client-controlled 'x-user-role' headers.
    - If a client asserts an unverified role without valid credentials, the request is rejected.
    - Returns None if no authentication is presented (anonymous public access).
    """
    # 1. Audit for forged / client-controlled role header abuse
    if x_user_role and x_user_role.strip().lower() in [ROLE_SCOUT_ADMIN, ROLE_LEAD_ANALYST]:
        # If client asserts a privileged role, require valid matching credentials
        token = None
        if authorization and authorization.startswith("Bearer "):
            token = authorization.split("Bearer ")[1].strip()
        elif x_api_key:
            token = x_api_key.strip()
            
        if not token or token not in [settings.SCOUT_ADMIN_API_KEY, settings.LEAD_ANALYST_API_KEY]:
            logger.warning(f"Security Alert: Rejected forged client role header '{x_user_role}' without valid credentials.")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Untrusted client-controlled role header rejected. Authenticate using trusted server credentials.",
                headers={"WWW-Authenticate": "Bearer"},
            )

    # 2. Extract credential token
    token = None
    auth_method = "bearer"
    if authorization:
        if authorization.startswith("Bearer "):
            token = authorization.split("Bearer ")[1].strip()
        else:
            token = authorization.strip()
    elif x_api_key:
        token = x_api_key.strip()
        auth_method = "api_key"

    # 3. Anonymous user
    if not token:
        return None

    # 4. Validate against server credentials
    if token == settings.SCOUT_ADMIN_API_KEY:
        return AuthenticatedUser(
            user_id="rr_scout_admin_01",
            username="rr_scout_admin",
            roles=[ROLE_SCOUT_ADMIN, ROLE_LEAD_ANALYST],
            auth_method=auth_method,
        )
    elif token == settings.LEAD_ANALYST_API_KEY:
        return AuthenticatedUser(
            user_id="rr_lead_analyst_01",
            username="rr_lead_analyst",
            roles=[ROLE_LEAD_ANALYST],
            auth_method=auth_method,
        )
    else:
        logger.warning("Security Alert: Invalid authentication token provided.")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials.",
            headers={"WWW-Authenticate": "Bearer"},
        )


async def require_authenticated_user(
    user: Optional[AuthenticatedUser] = Depends(get_current_user_optional),
) -> AuthenticatedUser:
    """Deny-by-default: Requires any valid authenticated principal."""
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication required. Provide valid credentials via Bearer token or X-API-Key.",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user


async def require_scout_admin(
    user: Optional[AuthenticatedUser] = Depends(get_current_user_optional),
) -> AuthenticatedUser:
    """
    Deny-by-default: Requires verified Rajasthan Royals Scout Administrator role.
    Rejects anonymous users (401) and insufficient privileges (403).
    """
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication required. Rajasthan Royals Scout Administrator credentials needed.",
            headers={"WWW-Authenticate": "Bearer"},
        )
    if not user.has_role(ROLE_SCOUT_ADMIN):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Insufficient permissions. Operation restricted to Rajasthan Royals Scout Administrators.",
        )
    return user


async def require_lead_analyst(
    user: Optional[AuthenticatedUser] = Depends(get_current_user_optional),
) -> AuthenticatedUser:
    """Deny-by-default: Requires Lead Analyst or Scout Admin privileges."""
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication required. Rajasthan Royals Analyst credentials needed.",
            headers={"WWW-Authenticate": "Bearer"},
        )
    if not (user.has_role(ROLE_LEAD_ANALYST) or user.has_role(ROLE_SCOUT_ADMIN)):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Insufficient permissions. Operation restricted to Lead Cricket Analysts.",
        )
    return user

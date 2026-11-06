#!/usr/bin/env python3
"""
Royals Intelligence - Stage 0 Environment Verification Script
Validates Python runtime, dependencies, backend imports, and configuration.
"""

import sys
import os
from pathlib import Path

# Set backend in path
ROOT_DIR = Path(__file__).resolve().parent.parent
BACKEND_DIR = ROOT_DIR / "backend"
sys.path.insert(0, str(BACKEND_DIR))


def run_checks():
    print("=" * 60)
    print("ROYALS INTELLIGENCE — STAGE 0 ENVIRONMENT AUDIT")
    print("=" * 60)

    # Check 1: Python Version
    py_ver = sys.version_info
    print(f"[1/6] Python Version: {py_ver.major}.{py_ver.minor}.{py_ver.micro} ... ", end="")
    if py_ver.major == 3 and py_ver.minor >= 11:
        print("PASS")
    else:
        print("FAIL (Requires Python 3.11+)")

    # Check 2: Core Packages Import
    print("[2/6] Importing Core Backend Dependencies ... ", end="")
    try:
        import fastapi
        import pydantic
        import sqlalchemy
        import alembic
        import asyncpg
        import pytest
        import numpy
        import pandas
        print("PASS")
    except ImportError as e:
        print(f"FAIL ({e})")
        return False

    # Check 3: Configuration Loading
    print("[3/6] Loading Pydantic Settings ... ", end="")
    try:
        from app.core.config import settings
        assert settings.PROJECT_NAME == "Royals Intelligence"
        assert settings.API_V1_PREFIX == "/api/v1"
        print(f"PASS (App: '{settings.PROJECT_NAME}', Env: '{settings.ENVIRONMENT}')")
    except Exception as e:
        print(f"FAIL ({e})")
        return False

    # Check 4: FastAPI Application & Router Initialization
    print("[4/6] Initializing FastAPI App & Routes ... ", end="")
    try:
        from app.main import app
        route_paths = [r.path for r in app.routes]
        assert "/health" in route_paths
        assert "/api/v1/health" in route_paths
        print(f"PASS ({len(route_paths)} routes registered)")
    except Exception as e:
        print(f"FAIL ({e})")
        return False

    # Check 5: SQLAlchemy Declarative Base & Engine
    print("[5/6] Inspecting Async SQLAlchemy Base ... ", end="")
    try:
        from app.db.base import Base
        from app.db.session import engine
        assert len(Base.metadata.tables) == 0  # Stage 0: zero dummy tables
        assert engine.url.drivername == "postgresql+asyncpg"
        print("PASS (Base clean, zero dummy tables created)")
    except Exception as e:
        print(f"FAIL ({e})")
        return False

    # Check 6: Directory Structure Integrity
    print("[6/6] Verifying Data & Reports Boundaries ... ", end="")
    required_dirs = [
        ROOT_DIR / "data" / "raw",
        ROOT_DIR / "data" / "processed",
        ROOT_DIR / "data" / "external",
        ROOT_DIR / "data" / "metadata",
        ROOT_DIR / "reports" / "generated",
        ROOT_DIR / "reports" / "templates",
        ROOT_DIR / "docs",
    ]
    all_exist = all(d.exists() and d.is_dir() for d in required_dirs)
    if all_exist:
        print("PASS (All partitions verified)")
    else:
        print("FAIL (Missing directories)")
        return False

    print("=" * 60)
    print("STAGE 0 BACKEND VERIFICATION RESULT: ALL CHECKS PASSED")
    print("=" * 60)
    return True


if __name__ == "__main__":
    success = run_checks()
    sys.exit(0 if success else 1)

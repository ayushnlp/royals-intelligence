"""
Royals Intelligence - Structured Logging Setup
Provides standardized JSON-formatted or console loggers across all platform modules.
"""

import logging
import sys
from app.core.config import settings


def setup_logging() -> logging.Logger:
    """Configures root logger with level and format matching project configuration."""
    log_level = getattr(logging, settings.LOG_LEVEL.upper(), logging.INFO)
    
    # Configure root format
    formatter = logging.Formatter(
        fmt="%(asctime)s [%(levelname)s] [%(name)s]: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(formatter)
    
    root_logger = logging.getLogger("royals_intelligence")
    root_logger.setLevel(log_level)
    
    # Avoid duplicate handlers if reloaded
    if not root_logger.handlers:
        root_logger.addHandler(handler)
        
    return root_logger


logger = setup_logging()

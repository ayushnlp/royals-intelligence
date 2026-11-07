"""
Royals Intelligence - Database Declarative Base
Central metadata registry for all future SQLAlchemy models.
"""

import uuid
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import MetaData

# Standard naming convention for constraints to assist Alembic migrations
convention = {
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s",
}

metadata = MetaData(naming_convention=convention)


def generate_uuid() -> str:
    """Generate canonical UUID4 string."""
    return str(uuid.uuid4())


class Base(DeclarativeBase):
    metadata = metadata

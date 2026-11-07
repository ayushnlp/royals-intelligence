"""
Royals Intelligence - Data Governance Database Models
SQLAlchemy 2.0 models for Data Sources, Datasets, Manifests, Ingestion Runs,
Validation Audit Logs, Lineage References, and Data Quality Metrics.
"""

import uuid
from datetime import datetime
from typing import Optional
from sqlalchemy import (
    String, Integer, Float, Boolean, DateTime, Text,
    ForeignKey, UniqueConstraint, Index
)
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base


def generate_uuid() -> str:
    """Generate canonical UUID4 string."""
    return str(uuid.uuid4())


class DataSourceModel(Base):
    """Cataloged external or proprietary data provider."""
    __tablename__ = "data_sources"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=generate_uuid)
    source_id: Mapped[str] = mapped_column(String(50), unique=True, index=True)  # e.g., 'cricsheet_open', 'rr_data_pack'
    name: Mapped[str] = mapped_column(String(120), nullable=False)
    tier: Mapped[str] = mapped_column(String(20), nullable=False)  # 'TIER_1', 'TIER_2', 'TIER_3', 'TIER_4'
    category: Mapped[str] = mapped_column(String(40), nullable=False)
    official_url: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    access_method: Mapped[str] = mapped_column(String(40), nullable=False)  # 'OPEN_HTTP', 'MANUAL_UPLOAD', 'DIRECT_ZIP'
    license_type: Mapped[str] = mapped_column(String(50), nullable=False)
    update_frequency: Mapped[str] = mapped_column(String(40), nullable=False)
    rate_limit_rpm: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    health_status: Mapped[str] = mapped_column(String(30), default="OPERATIONAL")
    data_classification: Mapped[str] = mapped_column(String(40), default="PUBLIC")  # 'PUBLIC', 'INTERNAL_SCOUTING', 'RR_PROPRIETARY_CONFIDENTIAL'
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    # Relationships
    datasets: Mapped[list["DatasetModel"]] = relationship("DatasetModel", back_populates="source")
    ingestion_runs: Mapped[list["IngestionRunModel"]] = relationship("IngestionRunModel", back_populates="source")


class DatasetModel(Base):
    """Logical dataset entity (e.g. 'smat_2024_ball_by_ball', 'rr_2026_uncapped_pack')."""
    __tablename__ = "datasets"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=generate_uuid)
    dataset_key: Mapped[str] = mapped_column(String(100), unique=True, index=True)
    name: Mapped[str] = mapped_column(String(150), nullable=False)
    competition_id: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    season: Mapped[Optional[str]] = mapped_column(String(20), nullable=True)
    source_id: Mapped[str] = mapped_column(String(36), ForeignKey("data_sources.id"), nullable=False)
    version: Mapped[str] = mapped_column(String(20), default="1.0.0")
    data_classification: Mapped[str] = mapped_column(String(40), default="PUBLIC")  # 'PUBLIC', 'INTERNAL_SCOUTING', 'RR_PROPRIETARY_CONFIDENTIAL'
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    # Relationships
    source: Mapped["DataSourceModel"] = relationship("DataSourceModel", back_populates="datasets")
    manifests: Mapped[list["DatasetManifestModel"]] = relationship("DatasetManifestModel", back_populates="dataset")


class IngestionRunModel(Base):
    """Audit log of an execution of the data acquisition/ingestion pipeline."""
    __tablename__ = "ingestion_runs"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=generate_uuid)
    run_id: Mapped[str] = mapped_column(String(80), unique=True, index=True)
    source_id: Mapped[str] = mapped_column(String(36), ForeignKey("data_sources.id"), nullable=False)
    competition_id: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    season: Mapped[Optional[str]] = mapped_column(String(20), nullable=True)
    status: Mapped[str] = mapped_column(String(30), default="PENDING")  # 'PENDING', 'IN_PROGRESS', 'COMPLETED', 'FAILED'
    started_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    completed_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    duration_seconds: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    total_records: Mapped[int] = mapped_column(Integer, default=0)
    valid_records: Mapped[int] = mapped_column(Integer, default=0)
    rejected_records: Mapped[int] = mapped_column(Integer, default=0)
    idempotent_skips: Mapped[int] = mapped_column(Integer, default=0)
    completeness_percentage: Mapped[float] = mapped_column(Float, default=0.0)
    error_message: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    # Relationships
    source: Mapped["DataSourceModel"] = relationship("DataSourceModel", back_populates="ingestion_runs")
    validation_results: Mapped[list["ValidationResultModel"]] = relationship("ValidationResultModel", back_populates="run", cascade="all, delete-orphan")


class DatasetManifestModel(Base):
    """Cryptographic provenance record and artifact inventory for a dataset."""
    __tablename__ = "dataset_manifests"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=generate_uuid)
    manifest_key: Mapped[str] = mapped_column(String(100), unique=True, index=True)
    dataset_id: Mapped[str] = mapped_column(String(36), ForeignKey("datasets.id"), nullable=False)
    run_id: Mapped[str] = mapped_column(String(80), nullable=False)
    raw_file_count: Mapped[int] = mapped_column(Integer, default=0)
    processed_file_count: Mapped[int] = mapped_column(Integer, default=0)
    checksum_sha256: Mapped[str] = mapped_column(String(64), nullable=False)
    completeness_percentage: Mapped[float] = mapped_column(Float, default=100.0)
    validation_status: Mapped[str] = mapped_column(String(30), default="VALIDATED")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    # Relationships
    dataset: Mapped["DatasetModel"] = relationship("DatasetModel", back_populates="manifests")


class ValidationResultModel(Base):
    """Granular audit entry for validation checks during ingestion."""
    __tablename__ = "validation_results"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=generate_uuid)
    run_id: Mapped[str] = mapped_column(String(36), ForeignKey("ingestion_runs.id", ondelete="CASCADE"), nullable=False, index=True)
    entity_type: Mapped[str] = mapped_column(String(50), nullable=False)  # 'delivery', 'player', 'scorecard'
    entity_id: Mapped[str] = mapped_column(String(100), nullable=False)
    rule_name: Mapped[str] = mapped_column(String(80), nullable=False)
    severity: Mapped[str] = mapped_column(String(20), default="CRITICAL")  # 'CRITICAL', 'WARNING'
    passed: Mapped[bool] = mapped_column(Boolean, default=True)
    message: Mapped[str] = mapped_column(Text, nullable=False)
    field_name: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    raw_value: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    # Relationships
    run: Mapped["IngestionRunModel"] = relationship("IngestionRunModel", back_populates="validation_results")


class SourceReferenceModel(Base):
    """Lineage linkage tying any database row back to its exact raw source artifact."""
    __tablename__ = "source_references"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=generate_uuid)
    entity_table: Mapped[str] = mapped_column(String(50), nullable=False, index=True)
    entity_id: Mapped[str] = mapped_column(String(36), nullable=False, index=True)
    source_name: Mapped[str] = mapped_column(String(50), nullable=False)
    source_file_or_url: Mapped[str] = mapped_column(String(255), nullable=False)
    checksum_sha256: Mapped[Optional[str]] = mapped_column(String(64), nullable=True)
    ingested_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    __table_args__ = (
        Index("ix_source_ref_lookup", "entity_table", "entity_id"),
    )


class DataQualityRecordModel(Base):
    """Player and match level data quality diagnostics (missing fields, conflicts)."""
    __tablename__ = "data_quality_records"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=generate_uuid)
    entity_type: Mapped[str] = mapped_column(String(50), nullable=False, index=True)  # 'player', 'match'
    entity_id: Mapped[str] = mapped_column(String(36), nullable=False, index=True)
    completeness_score: Mapped[float] = mapped_column(Float, default=100.0)
    has_conflicts: Mapped[bool] = mapped_column(Boolean, default=False)
    conflict_details: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    missing_fields: Mapped[Optional[str]] = mapped_column(Text, nullable=True)  # Comma-separated or JSON list
    is_quarantined: Mapped[bool] = mapped_column(Boolean, default=False)
    verified_by: Mapped[Optional[str]] = mapped_column(String(60), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

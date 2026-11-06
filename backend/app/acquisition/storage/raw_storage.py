"""
Royals Intelligence - Raw Data Storage Manager
Handles immutable file storage, SHA-256 cryptographic checksums, and duplicate detection.
"""

import hashlib
import shutil
from pathlib import Path
from datetime import datetime, timezone
from typing import Optional, Tuple, Dict, Any
from app.core.logging import logger
from app.core.config import get_repo_root
from app.schemas.contracts.ingestion_contracts import FileArtifactMetadata


class RawStorageManager:
    """Manages raw data storage partitions, immutable snapshots, and SHA-256 hashing."""

    def __init__(self, base_raw_dir: Optional[Path] = None):
        if base_raw_dir is None:
            root_dir = get_repo_root()
            self.base_raw_dir = root_dir / "data" / "raw"
        else:
            self.base_raw_dir = Path(base_raw_dir)

    @staticmethod
    def calculate_sha256(file_path: Path) -> str:
        """Calculate SHA-256 checksum for a file."""
        sha256_hash = hashlib.sha256()
        with open(file_path, "rb") as f:
            for byte_block in iter(lambda: f.read(65536), b""):
                sha256_hash.update(byte_block)
        return sha256_hash.hexdigest()

    @staticmethod
    def calculate_bytes_sha256(data: bytes) -> str:
        """Calculate SHA-256 checksum for byte content."""
        return hashlib.sha256(data).hexdigest()

    def store_raw_file(
        self,
        source_path: Path,
        subfolder: str,
        target_filename: Optional[str] = None,
        check_existing_checksums: Optional[Dict[str, str]] = None
    ) -> Tuple[FileArtifactMetadata, bool]:
        """
        Stores an acquired raw file into a partitioned subfolder.
        Returns (FileArtifactMetadata, is_new).
        If an identical file exists (matching SHA-256), returns (metadata, False) without overwriting.
        """
        dest_dir = self.base_raw_dir / subfolder
        dest_dir.mkdir(parents=True, exist_ok=True)

        checksum = self.calculate_sha256(source_path)
        file_size = source_path.stat().st_size
        suffix = source_path.suffix.lstrip(".").lower()
        if suffix not in ["json", "csv", "parquet", "zip"]:
            suffix = "json"

        # Check duplicate via provided known checksums
        if check_existing_checksums and checksum in check_existing_checksums.values():
            logger.info(f"Duplicate file detected via checksum {checksum}. Skipping redundant write.")
            existing_path = [k for k, v in check_existing_checksums.items() if v == checksum][0]
            metadata = FileArtifactMetadata(
                file_path=str(existing_path),
                file_name=Path(existing_path).name,
                file_format=suffix,  # type: ignore
                file_size_bytes=file_size,
                checksum_sha256=checksum,
                created_at=datetime.now(timezone.utc),
            )
            return metadata, False

        # Generate immutable filename if not specified
        if not target_filename:
            timestamp_str = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
            target_filename = f"{source_path.stem}_{timestamp_str}{source_path.suffix}"

        dest_file = dest_dir / target_filename
        
        # If destination exists and has identical checksum, skip
        if dest_file.exists():
            existing_hash = self.calculate_sha256(dest_file)
            if existing_hash == checksum:
                logger.info(f"Identical file already exists at {dest_file}. Idempotent skip.")
                metadata = FileArtifactMetadata(
                    file_path=str(dest_file),
                    file_name=dest_file.name,
                    file_format=suffix,  # type: ignore
                    file_size_bytes=file_size,
                    checksum_sha256=checksum,
                    created_at=datetime.now(timezone.utc),
                )
                return metadata, False
            else:
                # Collision with different content: never silently overwrite, append timestamp
                timestamp_str = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S_%f")
                dest_file = dest_dir / f"{source_path.stem}_{timestamp_str}{source_path.suffix}"

        # Copy file safely
        shutil.copy2(source_path, dest_file)
        logger.info(f"Stored raw file at {dest_file} (SHA256: {checksum[:12]}...)")

        metadata = FileArtifactMetadata(
            file_path=str(dest_file),
            file_name=dest_file.name,
            file_format=suffix,  # type: ignore
            file_size_bytes=file_size,
            checksum_sha256=checksum,
            created_at=datetime.now(timezone.utc),
        )
        return metadata, True

    def store_raw_bytes(
        self,
        content: bytes,
        subfolder: str,
        filename: str,
        file_format: str = "json"
    ) -> Tuple[FileArtifactMetadata, bool]:
        """
        Stores in-memory bytes as an immutable raw artifact.
        """
        dest_dir = self.base_raw_dir / subfolder
        dest_dir.mkdir(parents=True, exist_ok=True)

        checksum = self.calculate_bytes_sha256(content)
        file_size = len(content)

        dest_file = dest_dir / filename
        if dest_file.exists():
            existing_hash = self.calculate_sha256(dest_file)
            if existing_hash == checksum:
                metadata = FileArtifactMetadata(
                    file_path=str(dest_file),
                    file_name=dest_file.name,
                    file_format=file_format,  # type: ignore
                    file_size_bytes=file_size,
                    checksum_sha256=checksum,
                    created_at=datetime.now(timezone.utc),
                )
                return metadata, False
            else:
                timestamp_str = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S_%f")
                dest_file = dest_dir / f"{Path(filename).stem}_{timestamp_str}{Path(filename).suffix}"

        with open(dest_file, "wb") as f:
            f.write(content)

        metadata = FileArtifactMetadata(
            file_path=str(dest_file),
            file_name=dest_file.name,
            file_format=file_format,  # type: ignore
            file_size_bytes=file_size,
            checksum_sha256=checksum,
            created_at=datetime.now(timezone.utc),
        )
        return metadata, True

"""
File Compass - HNSW-based semantic file search for AI workstations.

Provides fast semantic search across code, documentation, and config files
using HNSW indexing with nomic-embed-text embeddings via Ollama.
"""

__version__ = "0.1.0"
__author__ = "Mikey Frilot"

import os
from pathlib import Path


def get_data_dir() -> Path:
    """
    Get the user-writable data directory for file-compass.

    Priority:
    1. FILE_COMPASS_DATA_DIR environment variable
    2. ~/.file-compass (cross-platform user home)

    Returns:
        Path to data directory (created if needed)
    """
    if env_dir := os.environ.get("FILE_COMPASS_DATA_DIR"):
        data_dir = Path(env_dir)
    else:
        data_dir = Path.home() / ".file-compass"

    data_dir.mkdir(parents=True, exist_ok=True)
    return data_dir


def get_default_paths() -> tuple[Path, Path, Path]:
    """
    Get default paths for database, index, and SQLite files.

    Returns:
        Tuple of (db_path, index_path, sqlite_path)
    """
    db_path = get_data_dir()
    index_path = db_path / "file_compass.hnsw"
    sqlite_path = db_path / "files.db"
    return db_path, index_path, sqlite_path


# Lazy defaults - computed on first access, not at import time
DEFAULT_DB_PATH: Path = None  # type: ignore
DEFAULT_INDEX_PATH: Path = None  # type: ignore
DEFAULT_SQLITE_PATH: Path = None  # type: ignore


def _init_defaults():
    """Initialize default paths lazily."""
    global DEFAULT_DB_PATH, DEFAULT_INDEX_PATH, DEFAULT_SQLITE_PATH
    if DEFAULT_DB_PATH is None:
        DEFAULT_DB_PATH, DEFAULT_INDEX_PATH, DEFAULT_SQLITE_PATH = get_default_paths()

from __future__ import annotations

import os
import shutil
import sys
from pathlib import Path

APP_NAME: str = "Lock"
DATABASE_FILENAME: str = ".database.db"
SEED_DATABASE_RELATIVE_PATH: tuple[str, str] = ("database", "seed.db")


def bundle_root() -> Path:
    """Return the runtime root for both source and PyInstaller builds."""
    if getattr(sys, "frozen", False):
        return Path(getattr(sys, "_MEIPASS", Path(sys.executable).resolve().parent))
    return Path(__file__).resolve().parents[1]


def resource_path(*parts: str) -> str:
    """Resolve an application asset path in source or bundled mode."""
    return str(bundle_root().joinpath(*parts))


def app_data_dir() -> Path:
    """Return a writable per-user directory for application state."""
    home: Path = Path.home()

    if sys.platform == "win32":
        base_dir: Path = Path(os.getenv("APPDATA", home / "AppData" / "Roaming"))
    elif sys.platform == "darwin":
        base_dir = home / "Library" / "Application Support"
    else:
        base_dir = Path(os.getenv("XDG_DATA_HOME", home / ".local" / "share"))

    lock_dir: Path = base_dir / APP_NAME
    lock_dir.mkdir(parents=True, exist_ok=True)
    return lock_dir


def ensure_database_file() -> Path:
    """Ensure the runtime database exists in a writable location and return it."""
    target_path: Path = app_data_dir() / DATABASE_FILENAME
    if target_path.exists():
        return target_path

    legacy_path: Path = Path(resource_path("database", DATABASE_FILENAME))
    if legacy_path.exists():
        shutil.copy2(legacy_path, target_path)
        return target_path

    seed_path: Path = Path(resource_path(*SEED_DATABASE_RELATIVE_PATH))
    if seed_path.exists():
        shutil.copy2(seed_path, target_path)
    else:
        target_path.touch()

    return target_path

from __future__ import annotations

import os
import platform
import subprocess
import sys
import tarfile
import zipfile
from pathlib import Path

APP_NAME: str = "Lock"


def run_command(command: list[str], cwd: Path) -> None:
    print(f"Running: {' '.join(command)}")
    subprocess.run(command, cwd=cwd, check=True)


def build_onefile(root_dir: Path) -> Path:
    separator: str = ";" if os.name == "nt" else ":"
    exe_name: str = f"{APP_NAME}.exe" if os.name == "nt" else APP_NAME

    command: list[str] = [
        sys.executable,
        "-m",
        "PyInstaller",
        "--noconfirm",
        "--clean",
        "--onefile",
        "--name",
        APP_NAME,
        "--collect-all",
        "customtkinter",
        "--add-data",
        f"assets{separator}assets",
        "--add-data",
        f"database/seed.db{separator}database",
        "main.py",
    ]

    if platform.system().lower() != "darwin":
        command.insert(6, "--windowed")

    run_command(command, root_dir)
    return root_dir / "dist" / exe_name


def archive_executable(
    executable_path: Path, output_dir: Path, version_tag: str
) -> Path:
    system_name: str = platform.system().lower()
    platform_name: str = {
        "darwin": "macos",
        "windows": "windows",
        "linux": "linux",
    }.get(system_name, system_name)

    output_dir.mkdir(parents=True, exist_ok=True)
    artifact_stem: str = f"{APP_NAME}-{version_tag}-{platform_name}"

    if os.name == "nt":
        archive_path: Path = output_dir / f"{artifact_stem}.zip"
        with zipfile.ZipFile(
            archive_path, mode="w", compression=zipfile.ZIP_DEFLATED
        ) as zip_file:
            zip_file.write(executable_path, executable_path.name)
        return archive_path

    archive_path = output_dir / f"{artifact_stem}.tar.gz"
    with tarfile.open(archive_path, mode="w:gz") as tar_file:
        tar_file.add(executable_path, arcname=executable_path.name)
    return archive_path


def main() -> None:
    root_dir: Path = Path(__file__).resolve().parents[1]
    release_dir: Path = root_dir / "release"
    version_tag: str = os.getenv("GITHUB_REF_NAME", "dev")

    executable_path: Path = build_onefile(root_dir)
    archive_path: Path = archive_executable(executable_path, release_dir, version_tag)
    print(f"Created release artifact: {archive_path}")


if __name__ == "__main__":
    main()

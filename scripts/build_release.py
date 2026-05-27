from __future__ import annotations

import os
import platform
import subprocess
import sys
import tarfile
import zipfile
from pathlib import Path

APP_NAME: str = "Lock"
ICON_PATH: str = os.path.join("assets", "icon", "logo.png")


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
        "--windowed",
        "--name",
        APP_NAME,
        "--icon",
        ICON_PATH,
        "--collect-all",
        "customtkinter",
        "--add-data",
        f"assets{separator}assets",
        "--add-data",
        f"database/seed.db{separator}database",
        "main.py",
    ]

    run_command(command, root_dir)
    return root_dir / "dist" / exe_name


def archive_executable(
    executable_path: Path, output_dir: Path, version_tag: str
) -> Path:
    target_label: str = os.getenv("BUILD_TARGET", "").strip()
    system_name: str = platform.system().lower()
    platform_name: str = {
        "darwin": "macos",
        "windows": "windows",
        "linux": "linux",
    }.get(system_name, system_name)
    machine_name: str = platform.machine().lower()
    machine_aliases: dict[str, str] = {
        "amd64": "x64",
        "x86_64": "x64",
        "arm64": "arm64",
        "aarch64": "arm64",
    }
    arch_name: str = machine_aliases.get(machine_name, machine_name)
    artifact_target: str = target_label if target_label else f"{platform_name}-{arch_name}"

    output_dir.mkdir(parents=True, exist_ok=True)
    artifact_stem: str = f"{APP_NAME}-{version_tag}-{artifact_target}"

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

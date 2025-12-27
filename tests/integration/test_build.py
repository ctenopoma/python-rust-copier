import os
import shutil
import subprocess
from pathlib import Path

import pytest

DEFAULT_ANSWERS = {
    "project_name": "Build Ready Rust Python",
    "package_name": "build_pkg",
    "version": "0.3.0",
    "author": "Build Bot",
    "license": "MIT",
    "description": "Build pipeline validation for PyO3 template",
    "python_version": "3.14",
    "rust_toolchain": "stable",
    "uv_lock": True,
    "ffi_boundary": "PyO3",
    "target_platform": "Both",
    "use_docker": False,
}


_REQUIRES = {
    "uv": shutil.which("uv") is not None,
    "cargo": shutil.which("cargo") is not None,
}


def _render_template(tmp_path: Path, answers: dict[str, object]) -> Path:
    repo_root = Path(__file__).resolve().parents[2]
    template_dir = repo_root  # Template files now at root level
    assert template_dir.exists(), f"Template directory missing: {template_dir}"

    cmd: list[str] = ["copier", "copy", "--trust"]
    for key, value in answers.items():
        cmd.extend(["-d", f"{key}={value}"])
    cmd.extend([str(template_dir), str(tmp_path)])

    result = subprocess.run(cmd, capture_output=True, text=True)
    assert result.returncode == 0, f"copier failed ({result.returncode}): {result.stderr}\n{result.stdout}"
    return tmp_path


def _run(cmd: list[str], cwd: Path) -> subprocess.CompletedProcess[str]:
    env = os.environ.copy()
    env.setdefault("UV_LINK_MODE", "copy")  # avoid symlink issues on Windows
    return subprocess.run(cmd, cwd=cwd, capture_output=True, text=True, env=env, encoding="utf-8", errors="replace")


def test_build_pipeline(tmp_path: Path) -> None:
    if not all(_REQUIRES.values()):
        missing = ", ".join(sorted(tool for tool, present in _REQUIRES.items() if not present))
        pytest.skip(f"Skipping build pipeline test; missing tools: {missing}")

    project_dir = _render_template(tmp_path, DEFAULT_ANSWERS)

    sync = _run(["uv", "sync", "--group", "dev"], cwd=project_dir)
    assert sync.returncode == 0, f"uv sync failed: {sync.stderr}\n{sync.stdout}"

    develop = _run(["uv", "run", "maturin", "develop", "--quiet"], cwd=project_dir)
    assert develop.returncode == 0, f"maturin develop failed: {develop.stderr}\n{develop.stdout}"

    build = _run(["uv", "build"], cwd=project_dir)
    assert build.returncode == 0, f"uv build failed: {build.stderr}\n{build.stdout}"

    dist = project_dir / "dist"
    wheel_files = list(dist.glob("*.whl"))
    sdist_files = list(dist.glob("*.tar.gz"))
    assert wheel_files, "Expected wheel artifact in dist/"
    assert sdist_files, "Expected sdist artifact in dist/"

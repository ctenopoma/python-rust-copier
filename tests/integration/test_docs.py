import os
import shutil
import subprocess
from pathlib import Path

import pytest

DEFAULT_ANSWERS = {
    "project_name": "Docs Stub Project",
    "package_name": "docs_pkg",
    "version": "0.4.0",
    "author": "Docs Author",
    "license": "MIT",
    "description": "Sphinx documentation test scaffold",
    "python_version": "3.14",
    "rust_toolchain": "stable",
    "uv_lock": True,
    "ffi_boundary": "PyO3",
    "target_platform": "Both",
    "use_docker": False,
}


_REQUIRES = {
    "uv": shutil.which("uv") is not None,
}


def _render_template(tmp_path: Path, answers: dict[str, object]) -> Path:
    repo_root = Path(__file__).resolve().parents[2]
    template_dir = repo_root / "template"
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
    env.setdefault("UV_LINK_MODE", "copy")
    return subprocess.run(cmd, cwd=cwd, capture_output=True, text=True, env=env, encoding="utf-8", errors="replace")


def test_docs_build(tmp_path: Path) -> None:
    if not all(_REQUIRES.values()):
        missing = ", ".join(sorted(tool for tool, present in _REQUIRES.items() if not present))
        pytest.skip(f"Skipping docs test; missing tools: {missing}")

    project_dir = _render_template(tmp_path, DEFAULT_ANSWERS)

    sync = _run(["uv", "sync", "--group", "dev"], cwd=project_dir)
    assert sync.returncode == 0, f"uv sync failed: {sync.stderr}\n{sync.stdout}"

    docs_out = project_dir / "build" / "docs"
    build = _run(["uv", "run", "sphinx-build", "-b", "html", "docs", str(docs_out)], cwd=project_dir)
    assert build.returncode == 0, f"sphinx-build failed: {build.stderr}\n{build.stdout}"

    index_html = docs_out / "index.html"
    assert index_html.exists(), "index.html not found in docs output"

    index_content = index_html.read_text(encoding="utf-8")
    assert DEFAULT_ANSWERS["project_name"] in index_content, "Project name missing in index.html"

    warnings = [line for line in build.stdout.splitlines() if "warning:" in line.lower()]
    assert len(warnings) <= 3, f"Too many Sphinx warnings ({len(warnings)}): {warnings}"

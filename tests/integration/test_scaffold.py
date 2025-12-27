import json
import subprocess
from pathlib import Path


DEFAULT_ANSWERS = {
    "project_name": "Demo Rust Python",
    "package_name": "demo_pkg",
    "version": "0.2.0",
    "author": "Example Dev",
    "license": "MIT",
    "description": "Demo scaffold for Rust-backed Python package",
    "python_version": "3.14",
    "rust_toolchain": "stable",
    "uv_lock": True,
    "ffi_boundary": "PyO3",
    "target_platform": "Both",
    "use_docker": False,
}


def render_template(tmp_path: Path, answers: dict[str, object]) -> Path:
    repo_root = Path(__file__).resolve().parents[2]
    template_dir = repo_root  # Template files now at root level
    assert template_dir.exists(), f"Template directory missing: {template_dir}"

    cmd: list[str] = ["copier", "copy", "--trust"]
    for key, value in answers.items():
        cmd.extend(["-d", f"{key}={value}"])
    cmd.extend([str(template_dir), str(tmp_path)])

    result = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace")
    assert (
        result.returncode == 0
    ), f"copier failed ({result.returncode}): {result.stderr}\n{result.stdout}"
    return tmp_path


def test_scaffold_structure_and_commands(tmp_path: Path) -> None:
    project_dir = render_template(tmp_path, DEFAULT_ANSWERS)

    expected_files = [
        "pyproject.toml",
        "Cargo.toml",
        "noxfile.py",
        "README.md",
        "ruff.toml",
        "src/lib.rs",
        "CHANGELOG.md",
        f"{DEFAULT_ANSWERS['package_name']}/__init__.py",
    ]
    for rel_path in expected_files:
        target = project_dir / rel_path
        assert target.exists(), f"Missing expected file: {target}"

    pyproject = (project_dir / "pyproject.toml").read_text(encoding="utf-8")
    # Check for Python version requirement (may include upper bound like ">=3.14,<3.15")
    assert f">={DEFAULT_ANSWERS['python_version']}" in pyproject
    for dev_tool in ("maturin", "ruff", "pyrefly", "pytest"):
        assert dev_tool in pyproject, f"{dev_tool} missing from dependency groups"

    ruff_config = (project_dir / "ruff.toml").read_text(encoding="utf-8")
    assert f"py{DEFAULT_ANSWERS['python_version'].replace('.', '')}" in ruff_config

    readme = (project_dir / "README.md").read_text(encoding="utf-8")
    for cmd in ("uv sync --group dev", "uv run maturin develop", "uv run ruff check", "uv run pytest"):
        assert cmd in readme, f"Expected bootstrap command missing: {cmd}"

    changelog = (project_dir / "CHANGELOG.md").read_text(encoding="utf-8")
    assert DEFAULT_ANSWERS["project_name"] in changelog
    assert DEFAULT_ANSWERS["version"] in changelog

    # copier_log.txt may not exist when using -d flags, check if present
    log_path = project_dir / "copier_log.txt"
    if log_path.exists():
        log_lines = log_path.read_text(encoding="utf-8").splitlines()
        assert log_lines, "copier log was not written"
        last_entry = json.loads(log_lines[-1])
        assert last_entry["answers"]["package_name"] == DEFAULT_ANSWERS["package_name"]

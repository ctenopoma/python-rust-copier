import subprocess
import tempfile
from pathlib import Path


def test_render_template_default_answers() -> None:
    repo_root = Path(__file__).resolve().parents[2]
    template_dir = repo_root / "template"
    assert template_dir.exists(), f"Template directory missing: {template_dir}"

    with tempfile.TemporaryDirectory() as tmpdir:
        tmp_path = Path(tmpdir)
        cmd: list[str] = [
            "copier",
            "copy",
            "--trust",
            "--defaults",
            str(template_dir),
            str(tmp_path),
        ]
        result = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace")
        assert result.returncode == 0, f"copier failed: {result.stderr}\n{result.stdout}"

        items = list(tmp_path.iterdir())
        assert items, "Rendered project appears empty"

        # Check for key generated files
        pyproject = tmp_path / "pyproject.toml"
        cargo = tmp_path / "Cargo.toml"
        readme = tmp_path / "README.md"
        assert pyproject.exists(), "pyproject.toml not found"
        assert cargo.exists(), "Cargo.toml not found"
        assert readme.exists(), "README.md not found"


def test_deterministic_dry_run() -> None:
    repo_root = Path(__file__).resolve().parents[2]
    template_dir = repo_root / "template"
    assert template_dir.exists(), f"Template directory missing: {template_dir}"

    with tempfile.TemporaryDirectory() as tmpdir_a, tempfile.TemporaryDirectory() as tmpdir_b:
        render_a = Path(tmpdir_a)
        render_b = Path(tmpdir_b)

        answers = {
            "project_name": "Deterministic Test",
            "package_name": "det_pkg",
            "version": "0.5.0",
            "author": "Bot",
            "license": "Apache-2.0",
            "description": "Determinism check",
            "python_version": "3.11",
            "rust_toolchain": "stable",
            "uv_lock": False,
            "ffi_boundary": "PyO3",
            "target_platform": "Both",
            "use_docker": False,
        }
        cmd_base: list[str] = ["copier", "copy", "--trust"]
        for key, value in answers.items():
            cmd_base.extend(["-d", f"{key}={value}"])

        cmd_a = cmd_base + [str(template_dir), str(render_a)]
        result_a = subprocess.run(cmd_a, capture_output=True, text=True, encoding="utf-8", errors="replace")
        assert result_a.returncode == 0, f"First render failed: {result_a.stderr}\n{result_a.stdout}"

        cmd_b = cmd_base + [str(template_dir), str(render_b)]
        result_b = subprocess.run(cmd_b, capture_output=True, text=True, encoding="utf-8", errors="replace")
        assert result_b.returncode == 0, f"Second render failed: {result_b.stderr}\n{result_b.stdout}"

        # Compare file content (skip copier_log.txt which includes timestamps)
        files_a = {
            path.relative_to(render_a): path.read_bytes()
            for path in render_a.rglob("*")
            if path.is_file() and path.name != "copier_log.txt"
        }
        files_b = {
            path.relative_to(render_b): path.read_bytes()
            for path in render_b.rglob("*")
            if path.is_file() and path.name != "copier_log.txt"
        }
        assert files_a.keys() == files_b.keys(), "Rendered file sets differ between runs"

        for rel_path, content_a in files_a.items():
            content_b = files_b[rel_path]
            assert content_a == content_b, f"File content differs: {rel_path}"

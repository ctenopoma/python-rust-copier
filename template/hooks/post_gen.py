import json
from datetime import datetime
from pathlib import Path

LOG_FILE = "copier_log.txt"
ANSWERS_FILE = "copier-answers.yml"
METADATA_FILE = "template-metadata.json"
CHANGELOG_FILE = "CHANGELOG.md"

try:
    import yaml  # type: ignore
except Exception:  # pragma: no cover - best effort import
    yaml = None


def _load_answers(path: Path) -> dict:
    if not path.exists():
        return {}

    if yaml is not None:
        return yaml.safe_load(path.read_text(encoding="utf-8")) or {}

    # Minimal fallback parser for simple key: value answers when PyYAML is absent
    answers: dict[str, str] = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        if ":" not in line or line.strip().startswith("#"):
            continue
        key, _, value = line.partition(":")
        answers[key.strip()] = value.strip().strip("'\"")
    return answers


def _write_json(path: Path, payload: dict) -> None:
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def _append_changelog(project_root: Path, answers: dict, timestamp: str) -> str:
    changelog = project_root / CHANGELOG_FILE
    if not changelog.exists():
        changelog.write_text("# Changelog\n\n", encoding="utf-8")

    project = answers.get("project_name") or "project"
    version = answers.get("version") or "0.0.0"
    package = answers.get("package_name") or "package"
    entry = f"- {timestamp}: Scaffolded {project} v{version} ({package})\n"

    with changelog.open("a", encoding="utf-8") as f:
        f.write(entry)
    return entry


def main() -> None:
    project_root = Path.cwd()
    answers = _load_answers(project_root / ANSWERS_FILE)
    timestamp = datetime.utcnow().replace(microsecond=0).isoformat() + "Z"
    entry = {"timestamp": timestamp, "answers": answers}

    try:
        with (project_root / LOG_FILE).open("a", encoding="utf-8") as log_file:
            log_file.write(json.dumps(entry, ensure_ascii=False) + "\n")
        print(f"[post_gen] logged copier answers to {LOG_FILE}")
    except Exception as exc:  # pragma: no cover - logging errors are non-fatal
        print(f"[post_gen] failed to write log: {exc}")

    _write_json(project_root / METADATA_FILE, entry)
    changelog_entry = _append_changelog(project_root, answers, timestamp)
    print(f"[post_gen] appended changelog entry: {changelog_entry.strip()}")


if __name__ == "__main__":
    main()

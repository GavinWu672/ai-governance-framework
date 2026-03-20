#!/usr/bin/env python3
"""
Intake external project facts into a provenance-rich framework artifact.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

from memory_pipeline.memory_layout import resolve_memory_file

SCHEMA_VERSION = "1.0"
ARTIFACT_TYPE = "external-project-facts-intake"


def _sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def resolve_external_project_facts_file(repo_root: Path) -> Path:
    memory_root = repo_root / "memory"
    candidate = resolve_memory_file(memory_root, "tech_stack")
    if not candidate.exists():
        raise FileNotFoundError(
            f"external project facts not found under {memory_root}; expected 02_tech_stack.md or 02_project_facts.md"
        )
    return candidate


def build_external_project_facts_intake(repo_root: Path) -> dict:
    repo_root = repo_root.resolve()
    source_file = resolve_external_project_facts_file(repo_root)
    content = source_file.read_text(encoding="utf-8")
    captured_at = datetime.now(timezone.utc).isoformat()

    return {
        "schema_version": SCHEMA_VERSION,
        "artifact_type": ARTIFACT_TYPE,
        "captured_at": captured_at,
        "repo": {
            "name": repo_root.name,
            "root": str(repo_root),
        },
        "fact_source": {
            "logical_name": "tech_stack",
            "source_file": str(source_file),
            "source_filename": source_file.name,
            "content_sha256": _sha256_text(content),
        },
        "provenance": {
            "source_type": "external-memory-facts",
            "sync_direction": "external_to_framework",
            "memory_root": str(source_file.parent),
            "repo_root": str(repo_root),
            "captured_from": str(source_file),
        },
        "content": content,
    }


def default_output_path(project_root: Path, repo_root: Path) -> Path:
    return project_root / "artifacts" / "external-project-facts" / f"{repo_root.name}.json"


def write_intake_artifact(payload: dict, output_path: Path) -> Path:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return output_path


def format_human(payload: dict, output_path: Path | None = None) -> str:
    lines = [
        "[external_project_facts_intake]",
        f"repo={payload['repo']['name']}",
        f"repo_root={payload['repo']['root']}",
        f"source_file={payload['fact_source']['source_file']}",
        f"source_filename={payload['fact_source']['source_filename']}",
        f"sync_direction={payload['provenance']['sync_direction']}",
        f"content_sha256={payload['fact_source']['content_sha256']}",
    ]
    if output_path is not None:
        lines.append(f"output={output_path}")
    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser(description="Intake external project facts into a framework artifact.")
    parser.add_argument("--repo", required=True, help="External repo root")
    parser.add_argument("--project-root", default=".", help="Framework project root for default artifact output")
    parser.add_argument("--output", help="Optional explicit output path")
    parser.add_argument("--format", choices=["human", "json"], default="human")
    args = parser.parse_args()

    repo_root = Path(args.repo).resolve()
    project_root = Path(args.project_root).resolve()
    payload = build_external_project_facts_intake(repo_root)
    output_path = Path(args.output).resolve() if args.output else default_output_path(project_root, repo_root)
    write_intake_artifact(payload, output_path)

    if args.format == "json":
        print(json.dumps({**payload, "output": str(output_path)}, ensure_ascii=False, indent=2))
    else:
        print(format_human(payload, output_path))


if __name__ == "__main__":
    main()

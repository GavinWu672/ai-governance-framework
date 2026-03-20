from __future__ import annotations

import json
import shutil
from pathlib import Path

from governance_tools.external_project_facts_intake import (
    ARTIFACT_TYPE,
    build_external_project_facts_intake,
    default_output_path,
    resolve_external_project_facts_file,
    write_intake_artifact,
)


FIXTURE_ROOT = Path("tests/_tmp_external_project_facts_intake")


def _reset_fixture(name: str) -> Path:
    path = FIXTURE_ROOT / name
    if path.exists():
        shutil.rmtree(path)
    path.mkdir(parents=True, exist_ok=True)
    return path


def test_resolve_external_project_facts_file_accepts_external_alias() -> None:
    root = _reset_fixture("resolve_alias")
    repo_root = root / "Kernel-Driver-Contract"
    memory_root = repo_root / "memory"
    memory_root.mkdir(parents=True)
    source = memory_root / "02_project_facts.md"
    source.write_text("# Project Facts\n\n- target_os: windows\n", encoding="utf-8")

    resolved = resolve_external_project_facts_file(repo_root)

    assert resolved == source


def test_build_external_project_facts_intake_includes_provenance() -> None:
    root = _reset_fixture("build_payload")
    repo_root = root / "Kernel-Driver-Contract"
    source = repo_root / "memory" / "02_project_facts.md"
    source.parent.mkdir(parents=True)
    source.write_text("# Project Facts\n\n- target_os: windows\n", encoding="utf-8")

    payload = build_external_project_facts_intake(repo_root)

    assert payload["artifact_type"] == ARTIFACT_TYPE
    assert payload["repo"]["name"] == "Kernel-Driver-Contract"
    assert payload["fact_source"]["source_filename"] == "02_project_facts.md"
    assert payload["provenance"]["source_type"] == "external-memory-facts"
    assert payload["provenance"]["sync_direction"] == "external_to_framework"
    assert payload["content"].startswith("# Project Facts")
    assert payload["fact_source"]["content_sha256"]


def test_write_intake_artifact_uses_framework_artifact_root() -> None:
    root = _reset_fixture("write_artifact")
    project_root = root / "framework"
    repo_root = root / "Kernel-Driver-Contract"
    source = repo_root / "memory" / "02_project_facts.md"
    source.parent.mkdir(parents=True)
    source.write_text("# Project Facts\n\n- target_os: windows\n", encoding="utf-8")

    payload = build_external_project_facts_intake(repo_root)
    output_path = default_output_path(project_root, repo_root)
    written = write_intake_artifact(payload, output_path)

    assert written == output_path
    saved = json.loads(output_path.read_text(encoding="utf-8"))
    assert saved["repo"]["name"] == "Kernel-Driver-Contract"
    assert saved["fact_source"]["source_filename"] == "02_project_facts.md"

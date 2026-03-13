from __future__ import annotations

import shutil
from pathlib import Path

from governance_tools.governance_auditor import audit_governance


FIXTURE_ROOT = Path("tests/_tmp_governance_auditor")


def _reset_fixture(name: str) -> Path:
    path = FIXTURE_ROOT / name
    if path.exists():
        shutil.rmtree(path)
    path.mkdir(parents=True, exist_ok=True)
    return path


def _write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def _seed_minimal_project(root: Path) -> None:
    _write(root / "README.md", "scripts/run-runtime-governance.sh\n")
    _write(root / ".github/workflows/governance.yml", "runtime-enforcement\nscripts/run-runtime-governance.sh --mode ci\n")
    _write(root / "runtime_hooks/README.md", "scripts/run-runtime-governance.sh\n")
    _write(root / "runtime_hooks/core/pre_task_check.py", "# ok\n")
    _write(root / "runtime_hooks/core/post_task_check.py", "# ok\n")
    _write(root / "runtime_hooks/core/session_end.py", "# ok\n")
    _write(root / "runtime_hooks/dispatcher.py", "# ok\n")
    _write(root / "scripts/run-runtime-governance.sh", "#!/usr/bin/env bash\n")
    _write(root / "governance/HUMAN-OVERSIGHT.md", "ok\n")
    _write(root / "governance/AGENT.md", "ok\n")
    _write(root / "governance/TESTING.md", "ok\n")
    _write(root / "governance/SYSTEM_PROMPT.md", "cross-project private include\n")
    _write(root / "governance/ARCHITECTURE.md", "AdditionalIncludeDirectories\n")
    _write(root / "governance/REVIEW_CRITERIA.md", "C9 Project Include Boundary\n")
    _write(root / "governance/rules/common/core.md", "ok\n")
    _write(root / "governance/rules/python/coding.md", "ok\n")
    _write(root / "governance/rules/cpp/build_boundary.md", "AdditionalIncludeDirectories\n")
    _write(root / "governance/rules/refactor/behavior_lock.md", "ok\n")
    _write(root / "governance/rules/refactor/boundary_safety.md", "ok\n")


def test_governance_auditor_passes_on_repo_root():
    result = audit_governance(Path(".").resolve())
    assert result["ok"] is True
    assert result["errors"] == []


def test_governance_auditor_detects_missing_runtime_enforcement():
    root = _reset_fixture("missing_runtime")
    _seed_minimal_project(root)
    (root / "scripts/run-runtime-governance.sh").unlink()

    result = audit_governance(root)

    assert result["ok"] is False
    assert any("runtime:scripts/run-runtime-governance.sh" in error for error in result["errors"])


def test_governance_auditor_detects_build_boundary_alignment_drift():
    root = _reset_fixture("boundary_drift")
    _seed_minimal_project(root)
    _write(root / "governance/rules/cpp/build_boundary.md", "missing expected marker\n")

    result = audit_governance(root)

    assert result["ok"] is False
    assert any("alignment:build-boundary" in error for error in result["errors"])

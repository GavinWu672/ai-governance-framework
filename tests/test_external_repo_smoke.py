from __future__ import annotations

from pathlib import Path

from governance_tools.external_repo_smoke import infer_smoke_rules, run_external_repo_smoke


def _write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def test_infer_smoke_rules_includes_common_and_external_pack(tmp_path: Path) -> None:
    rules_root = tmp_path / "rules"
    _write(rules_root / "firmware" / "safety.md", "# Firmware safety\n")

    rules = infer_smoke_rules({"rule_roots": [str(rules_root)]})

    assert rules == ["common", "firmware"]


def test_run_external_repo_smoke_succeeds_for_valid_external_contract(tmp_path: Path) -> None:
    _write(
        tmp_path / "PLAN.md",
        "> **最後更新**: 2026-03-15\n> **Owner**: tester\n> **Freshness**: Sprint (7d)\n",
    )
    _write(tmp_path / "AGENTS.md", "# Agents\n")
    _write(tmp_path / "CHECKLIST.md", "# Checklist\n")
    _write(tmp_path / "rules" / "firmware" / "safety.md", "# Firmware safety\n")
    _write(tmp_path / "validators" / "check.py", "def x():\n    return True\n")
    _write(
        tmp_path / "contract.yaml",
        "\n".join(
            [
                "name: sample-contract",
                "domain: firmware",
                "documents:",
                "  - CHECKLIST.md",
                "ai_behavior_override:",
                "  - AGENTS.md",
                "rule_roots:",
                "  - rules",
                "validators:",
                "  - validators/check.py",
            ]
        ),
    )

    result = run_external_repo_smoke(tmp_path)

    assert result.ok is True
    assert result.rules == ["common", "firmware"]
    assert result.pre_task_ok is True
    assert result.session_start_ok is True


def test_run_external_repo_smoke_fails_for_missing_external_rule_pack(tmp_path: Path) -> None:
    _write(
        tmp_path / "PLAN.md",
        "> **最後更新**: 2026-03-15\n> **Owner**: tester\n> **Freshness**: Sprint (7d)\n",
    )
    _write(
        tmp_path / "contract.yaml",
        "\n".join(
            [
                "name: broken-contract",
                "rule_roots:",
                "  - missing-rules",
            ]
        ),
    )

    result = run_external_repo_smoke(tmp_path)

    assert result.ok is False
    assert result.pre_task_ok is False or result.session_start_ok is False
    assert any("Unknown rule packs" in item or "PLAN.md" not in item for item in result.errors)

#!/usr/bin/env python3
"""
Runtime post-task governance checks.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from governance_tools.contract_validator import validate_contract
from governance_tools.driver_evidence_validator import validate_driver_evidence
from governance_tools.failure_completeness_validator import validate_failure_completeness
from governance_tools.public_api_diff_checker import check_public_api_diff
from governance_tools.refactor_evidence_validator import validate_refactor_evidence
from governance_tools.rule_pack_loader import parse_rule_list
from memory_pipeline.session_snapshot import create_session_snapshot


def _merge_runtime_checks(errors: list[str], warnings: list[str], checks: dict | None) -> None:
    if not checks:
        return

    for warning in checks.get("warnings", []):
        warnings.append(f"runtime-check: {warning}")

    for error in checks.get("errors", []):
        errors.append(f"runtime-check: {error}")


def _merge_refactor_evidence_checks(errors: list[str], warnings: list[str], checks: dict | None, rules: list[str]) -> dict | None:
    if "refactor" not in rules:
        return None

    result = validate_refactor_evidence(checks)
    for warning in result["warnings"]:
        warnings.append(f"refactor-evidence: {warning}")
    for error in result["errors"]:
        errors.append(f"refactor-evidence: {error}")
    return result


def _merge_public_api_diff_checks(
    errors: list[str],
    warnings: list[str],
    checks: dict | None,
    rules: list[str],
    api_before_files: list[Path] | None,
    api_after_files: list[Path] | None,
) -> dict | None:
    if "refactor" not in rules:
        return None

    result = None
    if checks and checks.get("public_api_diff"):
        result = checks["public_api_diff"]
    elif api_before_files and api_after_files:
        result = check_public_api_diff(api_before_files, api_after_files)
    else:
        return None

    for warning in result.get("warnings", []):
        warnings.append(f"public-api-diff: {warning}")
    for error in result.get("errors", []):
        errors.append(f"public-api-diff: {error}")
    return result


def _merge_failure_completeness_checks(errors: list[str], warnings: list[str], checks: dict | None, rules: list[str]) -> dict | None:
    if not checks:
        return None

    result = validate_failure_completeness(checks, require_cleanup=("refactor" in rules))
    for warning in result["warnings"]:
        warnings.append(f"failure-completeness: {warning}")
    for error in result["errors"]:
        errors.append(f"failure-completeness: {error}")
    return result


def _merge_driver_evidence_checks(errors: list[str], warnings: list[str], checks: dict | None, rules: list[str]) -> dict | None:
    if "kernel-driver" not in rules:
        return None

    result = validate_driver_evidence(checks)
    for warning in result["warnings"]:
        warnings.append(f"driver-evidence: {warning}")
    for error in result["errors"]:
        errors.append(f"driver-evidence: {error}")
    return result


def run_post_task_check(
    response_text: str,
    risk: str,
    oversight: str,
    memory_mode: str | None = None,
    memory_root: Path | None = None,
    snapshot_task: str | None = None,
    snapshot_summary: str | None = None,
    create_snapshot: bool = False,
    checks: dict | None = None,
    api_before_files: list[Path] | None = None,
    api_after_files: list[Path] | None = None,
) -> dict:
    validation = validate_contract(response_text)
    errors = list(validation.errors)
    warnings = list(validation.warnings)
    fields = validation.fields
    resolved_memory_mode = memory_mode or fields.get("MEMORY_MODE", "").strip() or "candidate"
    resolved_rules = parse_rule_list(fields.get("RULES", ""))
    snapshot_result = None
    effective_checks = dict(checks or {})

    if not validation.contract_found:
        errors.append("Missing governance contract in task output")

    if risk == "high" and oversight == "auto":
        errors.append("High-risk task completed without required oversight")

    if resolved_memory_mode == "durable" and oversight == "auto":
        errors.append("Durable memory requires oversight != auto")

    if resolved_memory_mode == "durable" and oversight == "review-required":
        warnings.append("Durable memory should typically be promoted after explicit review completion")

    _merge_runtime_checks(errors, warnings, effective_checks)
    public_api_diff = _merge_public_api_diff_checks(
        errors,
        warnings,
        effective_checks,
        resolved_rules,
        api_before_files,
        api_after_files,
    )
    if public_api_diff:
        effective_checks["public_api_diff"] = public_api_diff
        effective_checks["interface_stability_verified"] = public_api_diff.get("ok", False)
    failure_completeness = _merge_failure_completeness_checks(errors, warnings, effective_checks, resolved_rules)
    refactor_evidence = _merge_refactor_evidence_checks(errors, warnings, effective_checks, resolved_rules)
    driver_evidence = _merge_driver_evidence_checks(errors, warnings, effective_checks, resolved_rules)

    if create_snapshot and validation.contract_found and validation.compliant and not errors:
        if memory_root is None:
            errors.append("Snapshot creation requested without memory_root")
        else:
            snapshot_result = create_session_snapshot(
                memory_root=memory_root,
                task=snapshot_task or fields.get("PLAN", "unspecified-task"),
                summary=snapshot_summary or "Post-task candidate memory snapshot",
                source_text=response_text,
                risk=risk,
                oversight=oversight,
            )

    return {
        "ok": validation.contract_found and validation.compliant and len(errors) == 0,
        "contract_found": validation.contract_found,
        "compliant": validation.compliant,
        "fields": fields,
        "memory_mode": resolved_memory_mode,
        "rules": resolved_rules,
        "snapshot": snapshot_result,
        "checks": effective_checks if effective_checks else None,
        "public_api_diff": public_api_diff,
        "failure_completeness": failure_completeness,
        "refactor_evidence": refactor_evidence,
        "driver_evidence": driver_evidence,
        "errors": errors,
        "warnings": warnings,
    }


def format_human_result(result: dict) -> str:
    lines = [
        f"ok={result['ok']}",
        f"contract_found={result['contract_found']}",
        f"compliant={result['compliant']}",
        f"memory_mode={result['memory_mode']}",
    ]
    if result["snapshot"]:
        lines.append(f"snapshot={result['snapshot']['snapshot_path']}")
    if result["public_api_diff"]:
        lines.append(f"public_api_removed={len(result['public_api_diff']['removed'])}")
        lines.append(f"public_api_added={len(result['public_api_diff']['added'])}")
        lines.append(f"public_api_ok={result['public_api_diff']['ok']}")
    if result["failure_completeness"] is not None:
        lines.append(f"failure_completeness_ok={result['failure_completeness']['ok']}")
    if result["refactor_evidence"] is not None:
        lines.append(f"refactor_evidence_ok={result['refactor_evidence']['ok']}")
    if result["driver_evidence"] is not None:
        lines.append(f"driver_evidence_ok={result['driver_evidence']['ok']}")
    for warning in result["warnings"]:
        lines.append(f"warning: {warning}")
    for error in result["errors"]:
        lines.append(f"error: {error}")
    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser(description="Run post-task governance checks.")
    parser.add_argument("--file", "-f", help="Response file; defaults to stdin")
    parser.add_argument("--risk", default="medium")
    parser.add_argument("--oversight", default="auto")
    parser.add_argument("--memory-mode")
    parser.add_argument("--memory-root")
    parser.add_argument("--snapshot-task")
    parser.add_argument("--snapshot-summary")
    parser.add_argument("--create-snapshot", action="store_true")
    parser.add_argument("--checks-file")
    parser.add_argument("--api-before", action="append", default=[])
    parser.add_argument("--api-after", action="append", default=[])
    parser.add_argument("--format", choices=["human", "json"], default="human")
    args = parser.parse_args()

    if args.file:
        response_text = Path(args.file).read_text(encoding="utf-8")
    else:
        response_text = sys.stdin.read()

    checks = json.loads(Path(args.checks_file).read_text(encoding="utf-8")) if args.checks_file else None

    result = run_post_task_check(
        response_text,
        risk=args.risk,
        oversight=args.oversight,
        memory_mode=args.memory_mode,
        memory_root=Path(args.memory_root) if args.memory_root else None,
        snapshot_task=args.snapshot_task,
        snapshot_summary=args.snapshot_summary,
        create_snapshot=args.create_snapshot,
        checks=checks,
        api_before_files=[Path(path) for path in args.api_before],
        api_after_files=[Path(path) for path in args.api_after],
    )

    if args.format == "json":
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(format_human_result(result))

    sys.exit(0 if result["ok"] else 1)


if __name__ == "__main__":
    main()

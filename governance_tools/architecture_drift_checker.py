#!/usr/bin/env python3
"""
Heuristic architecture drift checks for changed files or diff text.
"""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path


PRIVATE_PEER_INCLUDE_RE = re.compile(
    r'#include\s+[<"](?P<path>(?:\.\./|[A-Za-z0-9_\-]+/).*(?:Global\.h|GlMySql\.h|[^">]+\.h))[>"]'
)
ADDITIONAL_INCLUDE_RE = re.compile(
    r"AdditionalIncludeDirectories\s*[:=]?.*(etoken_server|database_service|DongleServer|SERVERMultithread)",
    re.IGNORECASE,
)
BOUNDARY_DRIFT_RE = re.compile(
    r"\b(Domain|Infrastructure|Adapter|Application)\b.{0,40}\b(move|depend|reference|cross|leak)\b",
    re.IGNORECASE,
)


def _scan_text(text: str, *, scope: str = "feature") -> dict:
    errors: list[str] = []
    warnings: list[str] = []
    findings: list[dict] = []

    for match in PRIVATE_PEER_INCLUDE_RE.finditer(text):
        include_path = match.group("path")
        if "../" in include_path or "/" in include_path:
            errors.append(f"Cross-project private include detected: {include_path}")
            findings.append(
                {
                    "kind": "cross_project_private_include",
                    "severity": "error",
                    "detail": include_path,
                }
            )

    if ADDITIONAL_INCLUDE_RE.search(text):
        detail = ADDITIONAL_INCLUDE_RE.search(text).group(1)
        errors.append(f"AdditionalIncludeDirectories references peer-private path: {detail}")
        findings.append(
            {
                "kind": "additional_include_peer_path",
                "severity": "error",
                "detail": detail,
            }
        )

    if scope == "refactor":
        for match in BOUNDARY_DRIFT_RE.finditer(text):
            detail = match.group(0).strip()
            warnings.append(f"Potential refactor boundary drift: {detail}")
            findings.append(
                {
                    "kind": "refactor_boundary_drift",
                    "severity": "warning",
                    "detail": detail,
                }
            )

    return {
        "ok": len(errors) == 0,
        "errors": errors,
        "warnings": warnings,
        "findings": findings,
    }


def check_architecture_drift(file_paths: list[Path] | None = None, diff_text: str = "", scope: str = "feature") -> dict:
    file_paths = file_paths or []
    aggregate = {"ok": True, "errors": [], "warnings": [], "findings": [], "files": []}

    if diff_text:
        result = _scan_text(diff_text, scope=scope)
        aggregate["errors"].extend(result["errors"])
        aggregate["warnings"].extend(result["warnings"])
        aggregate["findings"].extend(result["findings"])

    for path in file_paths:
        text = path.read_text(encoding="utf-8")
        result = _scan_text(text, scope=scope)
        aggregate["files"].append({"path": str(path), "ok": result["ok"]})
        aggregate["errors"].extend(result["errors"])
        aggregate["warnings"].extend(result["warnings"])
        aggregate["findings"].extend(result["findings"])

    aggregate["ok"] = len(aggregate["errors"]) == 0
    return aggregate


def main() -> None:
    parser = argparse.ArgumentParser(description="Check architecture drift heuristics.")
    parser.add_argument("--file", action="append", default=[])
    parser.add_argument("--diff-file")
    parser.add_argument("--scope", default="feature")
    args = parser.parse_args()

    diff_text = Path(args.diff_file).read_text(encoding="utf-8") if args.diff_file else ""
    result = check_architecture_drift(
        file_paths=[Path(path) for path in args.file],
        diff_text=diff_text,
        scope=args.scope,
    )
    print(json.dumps(result, ensure_ascii=False, indent=2))
    raise SystemExit(0 if result["ok"] else 1)


if __name__ == "__main__":
    main()

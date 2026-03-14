#!/usr/bin/env python3
"""
Build an index over generated change-control artifacts.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path


def _extract_summary_line(path: Path) -> str | None:
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.startswith("summary="):
            return line
    return None


def _priority_score(summary_line: str | None, session_start_json: Path | None = None) -> tuple[int, int, int, str]:
    if not summary_line:
        return (99, 99, 99, "")

    text = summary_line.lower()
    risk_order = {
        "proposal_risk=high": 0,
        "proposal_risk=medium": 1,
        "proposal_risk=low": 2,
    }
    risk_rank = 3
    for token, rank in risk_order.items():
        if token in text:
            risk_rank = rank
            break

    domain_rank = _domain_priority_rank(session_start_json)
    decision_rank = 1 if "runtime_decision=blocked" in text else 0
    promoted_rank = 1 if "promoted=false" in text else 0
    return (risk_rank, domain_rank, -decision_rank - promoted_rank, text)


def _load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def _normalize_session_start_payload(payload: dict) -> dict:
    if payload.get("event_type") == "session_start" and isinstance(payload.get("result"), dict):
        return payload["result"]
    return payload


def _domain_priority_rank(session_start_json: Path | None) -> int:
    if session_start_json is None or not session_start_json.exists():
        return 99

    try:
        payload = _normalize_session_start_payload(_load_json(session_start_json))
    except (OSError, json.JSONDecodeError):
        return 99

    domain_contract = payload.get("domain_contract") or {}
    domain_raw = domain_contract.get("raw") or {}
    domain = str(domain_raw.get("domain", "")).strip().lower()

    rank_map = {
        "kernel-driver": 0,
        "firmware": 1,
    }
    return rank_map.get(domain, 50 if domain else 99)


def _contract_resolution_suffix(session_start_json: Path | None) -> str:
    if session_start_json is None or not session_start_json.exists():
        return ""

    try:
        payload = _normalize_session_start_payload(_load_json(session_start_json))
    except (OSError, json.JSONDecodeError):
        return ""

    contract_resolution = payload.get("contract_resolution") or {}
    domain_contract = payload.get("domain_contract") or {}
    domain_raw = domain_contract.get("raw") or {}

    parts = []
    if contract_resolution.get("source"):
        parts.append(f"contract_source={contract_resolution['source']}")
    if domain_contract.get("name"):
        parts.append(f"contract_name={domain_contract['name']}")
    if domain_raw.get("domain"):
        parts.append(f"contract_domain={domain_raw['domain']}")
    if domain_raw.get("plugin_version"):
        parts.append(f"plugin_version={domain_raw['plugin_version']}")
    return " | " + " | ".join(parts) if parts else ""


def build_change_control_index(artifacts_dir: Path) -> str:
    summary_files = sorted(artifacts_dir.glob("*_change_control_summary.txt"))
    session_files = sorted(artifacts_dir.glob("*_session_start.txt"))
    json_files = sorted(artifacts_dir.glob("*_session_start.json"))
    json_lookup = {path.name.replace("_session_start.json", ""): path for path in json_files}
    summary_entries = [(path, _extract_summary_line(path)) for path in summary_files]
    priority_entries = sorted(
        summary_entries,
        key=lambda item: _priority_score(
            item[1],
            json_lookup.get(item[0].name.replace("_change_control_summary.txt", "")),
        ),
    )

    lines = ["[change_control_index]", f"artifacts_dir={artifacts_dir}"]
    lines.append(
        "summary="
        + " | ".join(
            [
                f"change_control_summaries={len(summary_files)}",
                f"session_start_notes={len(session_files)}",
                f"session_start_envelopes={len(json_files)}",
            ]
        )
    )
    lines.append("[review_order]")
    lines.append("1. read [priority_change_control_summaries] first")
    lines.append("2. inspect *_session_start.txt if proposal/startup context needs more detail")
    lines.append("3. inspect *_session_start.json for machine-readable detail")

    if priority_entries:
        lines.append("[priority_change_control_summaries]")
        for path, summary_line in priority_entries:
            session_start_json = json_lookup.get(path.name.replace("_change_control_summary.txt", ""))
            suffix = _contract_resolution_suffix(session_start_json)
            if summary_line:
                lines.append(f"{path.name} | {summary_line}{suffix}")
            else:
                lines.append(path.name)

    if summary_entries:
        lines.append("[change_control_summaries]")
        for path, summary_line in summary_entries:
            session_start_json = json_lookup.get(path.name.replace("_change_control_summary.txt", ""))
            suffix = _contract_resolution_suffix(session_start_json)
            if summary_line:
                lines.append(f"{path.name} | {summary_line}{suffix}")
            else:
                lines.append(path.name)

    if session_files:
        lines.append("[session_start_notes]")
        for path in session_files:
            lines.append(path.name)

    if json_files:
        lines.append("[session_start_envelopes]")
        for path in json_files:
            lines.append(path.name)

    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser(description="Build an index for change-control artifacts.")
    parser.add_argument("--artifacts-dir", required=True)
    parser.add_argument("--output")
    args = parser.parse_args()

    rendered = build_change_control_index(Path(args.artifacts_dir))
    if args.output:
        Path(args.output).write_text(rendered + "\n", encoding="utf-8")
    print(rendered)


if __name__ == "__main__":
    main()

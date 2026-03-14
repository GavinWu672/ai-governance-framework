#!/usr/bin/env python3
"""
Minimal domain contract discovery for external governance plugins.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


def _parse_scalar(value: str) -> str:
    parsed = value.strip()
    if len(parsed) >= 2 and parsed[0] == parsed[-1] and parsed[0] in {'"', "'"}:
        return parsed[1:-1]
    return parsed


def _parse_contract_yaml(text: str) -> dict:
    data: dict[str, object] = {}
    current_list_key: str | None = None

    for line_number, raw_line in enumerate(text.splitlines(), start=1):
        stripped = raw_line.strip()
        if not stripped or stripped.startswith("#"):
            continue

        if raw_line[: len(raw_line) - len(raw_line.lstrip(" "))]:
            if not current_list_key or not stripped.startswith("- "):
                raise ValueError(f"Unsupported contract.yaml structure on line {line_number}: {raw_line}")
            value = _parse_scalar(stripped[2:])
            data.setdefault(current_list_key, [])
            casted = data[current_list_key]
            assert isinstance(casted, list)
            casted.append(value)
            continue

        current_list_key = None
        if ":" not in stripped:
            raise ValueError(f"Invalid contract.yaml line {line_number}: {raw_line}")

        key, raw_value = stripped.split(":", 1)
        key = key.strip()
        value = raw_value.strip()

        if not value:
            data[key] = []
            current_list_key = key
            continue

        data[key] = _parse_scalar(value)

    return data


def _resolve_paths(contract_root: Path, items: list[str]) -> list[Path]:
    resolved: list[Path] = []
    for item in items:
        path = Path(item)
        resolved.append(path if path.is_absolute() else (contract_root / path).resolve())
    return resolved


def _as_list(value: object) -> list[str]:
    if value is None:
        return []
    if isinstance(value, list):
        return [str(item) for item in value]
    return [str(value)]


def _load_document(path: Path) -> dict:
    exists = path.exists()
    return {
        "path": str(path),
        "exists": exists,
        "content": path.read_text(encoding="utf-8").strip() if exists else "",
    }


def _load_validator(path: Path) -> dict:
    return {
        "name": path.stem,
        "path": str(path),
        "exists": path.exists(),
    }


def load_domain_contract(contract_file: str | Path | None) -> dict | None:
    if contract_file is None:
        return None

    contract_path = Path(contract_file).resolve()
    data = _parse_contract_yaml(contract_path.read_text(encoding="utf-8"))
    contract_root = contract_path.parent

    documents = _resolve_paths(contract_root, _as_list(data.get("documents")))
    ai_behavior_override = _resolve_paths(contract_root, _as_list(data.get("ai_behavior_override")))
    rule_roots = _resolve_paths(contract_root, _as_list(data.get("rule_roots")))
    validators = _resolve_paths(contract_root, _as_list(data.get("validators")))

    return {
        "name": data.get("name", contract_path.stem),
        "contract_path": str(contract_path),
        "contract_root": str(contract_root),
        "documents": [_load_document(path) for path in documents],
        "ai_behavior_override": [_load_document(path) for path in ai_behavior_override],
        "rule_roots": [str(path) for path in rule_roots],
        "validators": [_load_validator(path) for path in validators],
        "raw": data,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Load a domain contract from contract.yaml.")
    parser.add_argument("--contract", required=True)
    parser.add_argument("--format", choices=["human", "json"], default="human")
    args = parser.parse_args()

    contract = load_domain_contract(args.contract)
    if contract is None:
        print("ERROR: contract not found", file=sys.stderr)
        raise SystemExit(1)

    if args.format == "json":
        print(json.dumps(contract, ensure_ascii=False, indent=2))
        return

    lines = [
        "[domain_contract]",
        f"name={contract['name']}",
        f"contract_path={contract['contract_path']}",
        f"documents={len(contract['documents'])}",
        f"ai_behavior_override={len(contract['ai_behavior_override'])}",
        f"rule_roots={len(contract['rule_roots'])}",
        f"validators={len(contract['validators'])}",
    ]
    for item in contract["documents"]:
        lines.append(f"document: {Path(item['path']).name} exists={item['exists']}")
    for item in contract["ai_behavior_override"]:
        lines.append(f"behavior_override: {Path(item['path']).name} exists={item['exists']}")
    for item in contract["validators"]:
        lines.append(f"validator: {item['name']} exists={item['exists']}")
    print("\n".join(lines))


if __name__ == "__main__":
    main()

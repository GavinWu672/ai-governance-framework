#!/usr/bin/env python3
"""
Shared governance metadata for external domain contracts.
"""

from __future__ import annotations


DOMAIN_PRIORITY_RANK = {
    "kernel-driver": 0,
    "firmware": 1,
}


def normalize_domain_name(value: str | None) -> str:
    return str(value or "").strip().lower()


def domain_priority_rank(domain: str | None) -> int:
    normalized = normalize_domain_name(domain)
    if not normalized:
        return 99
    return DOMAIN_PRIORITY_RANK.get(normalized, 50)

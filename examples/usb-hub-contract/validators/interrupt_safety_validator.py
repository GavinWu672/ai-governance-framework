#!/usr/bin/env python3
"""
Placeholder validator for future validator-interface design.
"""


def describe() -> dict:
    return {
        "name": "interrupt_safety_validator",
        "requires": ["interrupt_safety_review"],
        "returns": ["warnings", "errors", "signals"],
    }

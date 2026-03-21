#!/usr/bin/env python3
"""
Shim: re-exports FailureCompletenessValidator for contract-based discovery.
"""
from governance_tools.failure_completeness_validator import FailureCompletenessValidator

__all__ = ["FailureCompletenessValidator"]

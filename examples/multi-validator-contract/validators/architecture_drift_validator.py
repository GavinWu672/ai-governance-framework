#!/usr/bin/env python3
"""
Shim: re-exports ArchitectureDriftValidator for contract-based discovery.
"""
from governance_tools.architecture_drift_checker import ArchitectureDriftValidator

__all__ = ["ArchitectureDriftValidator"]

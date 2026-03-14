#!/usr/bin/env python3
"""
Advisory validator for ISR safety patterns.
"""

from governance_tools.validator_interface import DomainValidator, ValidatorResult


class InterruptSafetyValidator(DomainValidator):
    FORBIDDEN_IN_ISR = ["printf", "malloc", "free", "HAL_Delay", "osDelay"]

    @property
    def rule_ids(self) -> list[str]:
        return ["hub-firmware", "HUB-004"]

    def validate(self, payload: dict) -> ValidatorResult:
        checks = payload.get("checks", {})
        isr_code = checks.get("isr_code", "")
        warnings = [
            f"HUB-ISR-001: '{fn}' called inside ISR"
            for fn in self.FORBIDDEN_IN_ISR
            if fn in isr_code
        ]
        return ValidatorResult(
            ok=len(warnings) == 0,
            rule_ids=self.rule_ids,
            warnings=warnings,
            evidence_summary=f"Checked {len(self.FORBIDDEN_IN_ISR)} forbidden patterns in ISR code",
            metadata={"mode": "advisory"},
        )

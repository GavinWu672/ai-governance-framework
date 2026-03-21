# Multi-Validator Contract Checklist

This contract demonstrates how to register multiple governance validators
from the `governance_tools` library into a domain contract.

## Registered Validators

| Validator | Scope |
|-----------|-------|
| ArchitectureDriftValidator | feature, refactor |
| DriverEvidenceValidator | kernel-driver |
| FailureCompletenessValidator | feature, refactor |
| RefactorEvidenceValidator | refactor |

## Usage

Reference this contract via `--contract examples/multi-validator-contract/contract.yaml`
when running `post_task_check` or any governance smoke tool.

# C# Architecture AI Governance Rules

## Purpose

This contract defines mandatory AI constraints for C# domain-driven projects.
Domain layer isolation violations cause architectural drift that is hard to reverse.
These rules are enforced via static pattern checks, not a full AST analysis.

## Core Constraints

- The agent must not generate `[DllImport]`, `[LibraryImport]`, or `extern static`
  declarations inside files that reside under `domain_roots`.
- The agent must not recommend `RuntimeInformation`, `OperatingSystem.Is*`,
  or `Environment.OSVersion` calls in domain layer code.
- The agent must not assume a violation is a false positive without explicit triage.

## No-Assumption Policy

The agent must not assume any of the following without a concrete source:

- Whether a file path is inside `domain_roots` or `infrastructure_roots`
- Whether a pattern match is intentional or accidental
- Whether a triage record exists for a given violation

If a required fact is missing, stop and ask for clarification.

## Validator Failure Policy

- An `ARCH_*` rule in advisory mode must be acknowledged in the PR description
  if the agent's changes produce a violation.
- The agent must not claim a violation is benign without a triage record.

## Triage Gate

- Every violation produced by a validator must appear in `triage/triage.json`
  before the violation can be marked as resolved.
- An untriaged violation is treated as advisory-blocking until reviewed.

## Scope Boundary

- This contract is a pre-merge static pattern checker.
- It does not replace Roslyn analysis, architecture tests (ArchUnitNET), or code review.
- Passing all checks does not indicate the architecture is correct end-to-end.

## Related Documents

- `contract.yaml`
- `rules/arch.md`
- `triage/schema.json`
- `docs/unit-test-strategy.md` (from framework root)

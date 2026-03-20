# Governance Runtime v2.6

Updated: 2026-03-20

This document captures the next architecture step after the current runtime
spine: move from "mixed enforcement with selected hard stops" to a
runtime-centered decision system with explicit constraint handling.

The machine-readable companion artifact is
`governance/governance_decision_model.v2.6.json`.

## Why v2.6 Exists

The current repository already has:

- a real runtime path
- external domain contracts
- validator execution
- evidence ingestion
- selected `hard_stop_rules`

That is enough to prove the seam is real, but it is still a transitional
enforcement model. The missing piece is a constraint layer that answers four
questions consistently:

1. Was a governance rule violated?
2. Who owns the decision?
3. How does that violation affect the verdict?
4. What fallback behavior is mandatory when the runtime is uncertain or broken?

v2.6 introduces that missing contract.

## Core Addition

### Enforcement Model

The `Governance Constraint Layer` is not a new repo layer. It is the runtime's
decision contract.

Its job is to make the following machine-checkable:

- ownership constraints
- policy precedence
- evidence validity and trust
- violation impact on verdicts
- fallback behavior under runtime or integration failure

The runtime remains the only place allowed to compute the final governance
verdict. External domain repos keep supplying domain knowledge, not local
decision engines.

## Executable Matrices

v2.6 upgrades three existing matrices and adds one new matrix.

### 1. Decision Ownership Matrix

Required fields:

| Field | Purpose |
| --- | --- |
| `concern` | What decision area is being governed |
| `owner` | Runtime, policy author, reviewer, or domain contract |
| `can_override` | Who may override the default owner |
| `override_path` | Required escalation path |
| `trace_required` | Whether the override must leave durable trace |
| `violation_effect` | `stop`, `escalate`, `degrade`, or `record-only` |

This closes the old gap where ownership was descriptive but not enforceable.

### 2. Policy Precedence Matrix

Required fields:

| Field | Purpose |
| --- | --- |
| `policy_type` | Runtime, repo, domain, reviewer, or emergency policy |
| `scope` | Where the policy applies |
| `override_target` | Which lower layer it may override |
| `allowed` | Whether the override is legal |
| `conflict_resolution` | How ties or conflicts are resolved |
| `violation_effect` | Verdict impact when precedence is violated |

This prevents illegal or ambiguous override behavior from remaining implicit.

### 3. Evidence Classification Matrix

Required fields:

| Field | Purpose |
| --- | --- |
| `evidence_kind` | The normalized evidence type |
| `required` | Whether it is mandatory for a decision path |
| `producer` | Expected source |
| `schema` | Expected structure |
| `validation_rule` | How validity is checked |
| `trust_level` | `high`, `medium`, `low`, or `unknown` |
| `missing_effect` | Verdict impact if missing |

This separates "evidence exists" from "evidence is valid and trustworthy."

### 4. Violation Handling Matrix

Required fields:

| Field | Purpose |
| --- | --- |
| `violation_type` | The normalized failure or contract breach |
| `detected_by` | Runtime component that detects it |
| `severity` | Expected seriousness |
| `default_verdict_impact` | Default verdict impact |
| `override_allowed` | Whether a human may legally override it |
| `trace_required` | Whether override or downgrade must be logged |

This is the table that turns exceptions into predictable behavior.

Minimum v2.6 violation types:

- `missing_required_evidence`
- `invalid_evidence_schema`
- `policy_conflict`
- `illegal_override`
- `runtime_failure`
- `integration_failure`
- `domain_contract_violation`

## Determinism Contract

The runtime can no longer assume perfect determinism once evidence order, async
pipelines, retries, and LLM-assisted reasoning are involved.

v2.6 therefore defines a lightweight determinism contract:

- the same evidence snapshot plus the same policy snapshot must produce the same
  verdict
- reasoning traces may differ in wording, but not in policy inputs, evidence
  references, or final verdict
- re-evaluation is allowed, but result changes require a recorded cause
- accepted causes are evidence change, policy change, runtime version change, or
  an explicitly traced human override

This protects trust when the same commit is evaluated more than once.

## External Contract Boundary

The external contract repos are affected, but not invalidated.

### Domain Assets That Stay

- `contract.yaml`
- domain rules
- validator logic
- fixtures
- domain documents

### Integration Seams That Must Move

- hook-stage-specific enforcement assumptions
- direct `hard_stop_rules` outcome escalation as the main decision mechanism
- advisory versus blocking logic defined outside the runtime decision contract
- fixture assumptions that depend on old hook-stage routing

### Boundary To Protect

Do not push final decision logic into each domain repo.

The correct split is:

- domain repos provide facts, rules, validators, and evidence producers
- the framework runtime owns verdict computation, precedence resolution,
  violation handling, and fallback behavior

## Current Interpretation

Today:

- the repo has a working runtime spine
- selected domain rules can already block outcomes
- enforcement is still transitional and partly seam-driven

Target:

- runtime becomes the single decision source
- matrices become executable specification, not just documentation
- violations affect verdicts through one normalized model
- external contracts keep their domain assets while losing scattered decision
  ownership

## Related Files

- `governance/governance_decision_model.v2.6.json`
- `docs/status/domain-enforcement-matrix.md`
- `docs/status/runtime-governance-status.md`
- `runtime_hooks/README.md`

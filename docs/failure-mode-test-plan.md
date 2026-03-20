# Failure Mode Test Plan

This document defines the first deliberate break-tests for the governance
runtime. The goal is not to validate happy-path utility, but to validate that
the system remains predictable when evidence, policy, or runtime execution goes
wrong.

## Current Position

The repository has a stronger control plane than execution plane:

- the v2.6 decision model exists as an explicit spec
- validator payloads are versioned and provenance-aware
- runtime session end emits minimal verdict and trace artifacts

The next trust gate is different:

- failure behavior must be exercised, not just described
- determinism must be checked with repeated inputs
- runtime outputs must stay reviewable under degraded conditions

## Initial Failure Modes

The first test wave covers five scenarios:

1. `missing_required_evidence`
2. `invalid_evidence_schema`
3. `policy_conflict`
4. `runtime_failure`
5. `determinism_replay`

These align with the current v2.6 decision model and the user's stricter
definition of what should count as a future `1.0`.

## Expected Outcomes

Each failure-mode scenario must define:

- the injected fault
- the runtime component expected to detect it
- the expected verdict impact
- the expected trace / verdict artifact visibility
- the determinism expectation

The machine-readable source of truth for these scenarios is:

- `governance/failure_mode_test_matrix.v0.1.json`

## Acceptance Direction

This plan should be considered established only when the runtime can
progressively demonstrate all of the following:

- repeated identical evidence and policy snapshots produce the same verdict
- degraded inputs still produce a reviewable runtime artifact
- policy conflicts do not bypass runtime ownership
- runtime failures fail closed or escalate in a declared way
- missing or invalid evidence does not silently pass through as success

## Scope Note

This is intentionally a minimal first slice. It defines the break-test contract
before building a full fault-injection harness.

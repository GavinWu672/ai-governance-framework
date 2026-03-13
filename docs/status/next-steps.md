# Next Steps

Updated: 2026-03-13

## Why The `passed` Count Changes

The `passed` number is not expected to stay fixed across turns.

Reasons:

- each turn only runs the most relevant test subset for the files changed in that step
- some turns validate a single tool or validator
- other turns validate a larger integration slice across runtime hooks, rule packs, and evidence ingestion

Examples:

- `3 passed` when only `public_api_diff_checker.py` was under validation
- `20 passed` when driver evidence ingestion and post-task runtime integration were validated together
- `25 passed` when architecture drift v2, driver evidence, ingestion, and runtime post-task checks were validated together

This means:

- different `passed` counts do **not** imply instability by themselves
- the meaningful signal is whether the targeted suite for that step passed cleanly

## Current Completed Milestones

The following items are now in place on the working tree:

- `public_api_diff_checker.py`
- `kernel-driver` seed platform pack
- `platform` rule-pack category
- `driver_evidence_validator.py`
- driver-oriented ingestion in `test_result_ingestor.py`
- architecture drift v2 with before/after dependency-edge diff
- advisory `rule_pack_suggestions` in `state_generator.py`

## Highest-Value Remaining Work

### 1. Refresh Status Documents

Update `docs/status/runtime-governance-status.md` so it reflects:

- `platform` category
- `kernel-driver` pack
- `public_api_diff_checker.py`
- `driver_evidence_validator.py`
- driver-oriented evidence ingestion
- architecture drift v2
- advisory suggester output in `state_generator.py`

Why this matters:

- the implementation has moved ahead of the status document
- repo readers should not need commit archaeology to understand current capability

### 2. Push Current Working Tree

Several completed features are not pushed yet.

Why this matters:

- the remote branch is behind local capability
- status, README, and runtime behavior should stay aligned

### 3. Kernel-Driver Pack Refinement

Current kernel-driver pack is a strong seed, but still generic.

Recommended next split:

- `kernel-driver`
- later optional `kmdf`
- later optional `wdm`
- later optional `umdf`

Why this is not first:

- the generic seed pack is already useful
- splitting too early increases maintenance cost before usage patterns stabilize

### 4. Public API Diff Integration Beyond Refactor

Current behavior:

- public API diff is mainly used as a `refactor` evidence signal

Potential next step:

- allow interface-sensitive feature work to opt in explicitly
- record public API diff results in session summaries or curated memory

### 5. Evidence Ingestion Expansion

Current ingestion supports:

- `pytest-text`
- `junit-xml`
- `sdv-text`
- `msbuild-warning-text`

Reasonable next additions:

- `wdk-analysis-text`
- `compiler-warning-json`
- `sarif`

Why this matters:

- these formats are closer to real static-analysis and security-tool outputs
- they reduce ad hoc parsing in downstream validators

### 6. Memory / Audit Tightening

Potential follow-up work:

- store evidence summaries in session close artifacts
- preserve driver-specific evidence decisions in curated memory or audit summaries
- make promotion decisions more transparent for high-risk platform work

## Boundary To Protect

The repo should continue to evolve by:

- adding rule content
- adding evidence validators
- adding lightweight structural checks

It should avoid turning into:

- a heavy language-analysis platform
- a driver-development IDE workflow replacement
- a generic policy-engine runtime

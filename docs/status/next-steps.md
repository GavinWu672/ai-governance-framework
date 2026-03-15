# Next Steps

Updated: 2026-03-15

## Current Focus

The runtime spine is complete enough that the highest-value work is no longer "add more framework pieces."

The next phase is:

- connect real project facts to the existing domain slices
- deepen semantic verification from pattern-based checks toward stronger structure-aware analysis
- reduce workflow friction and strengthen practical commit/merge-time governance
- strengthen proposal-time guidance without turning the repo into a policy engine
- tighten the review surface around startup and change-control artifacts

## Highest-Value Remaining Work

### 1. Real Facts Intake

Current status:

- three external domain contracts now exist
- mixed enforcement already runs across firmware, kernel-driver, and ic-verification slices
- most current validation still depends on fixtures or sample facts, not production codebases

Next step:

- connect one real domain repo to the existing fact-intake flow
- prioritize confirmed facts over broader new abstractions
- run at least one true AI-session replay against real evidence, not only fixtures

Why this matters:

- the main gap is no longer runtime plumbing; it is grounding the existing system in real project truth

### 2. Public API Diff Deepening

Current status:

- `public_api_diff_checker.py` exists
- public API diff already affects post-task verdicts and audit artifacts

Next step:

- improve signature normalization
- better distinguish additive changes from compatibility risk
- keep pushing the checker from pattern-based compatibility hints toward stronger structure-aware reasoning

Why this matters:

- interface stability is still one of the weakest proof chains

### 3. Architecture Drift Reasoning

Current status:

- `architecture_drift_checker.py` already performs edge-diff and heuristic boundary checks
- `architecture_impact_estimator.py` now uses these signals in proposal-time guidance

Next step:

- broaden dependency reasoning beyond edge additions/removals
- improve module-boundary summaries
- correlate public/private API drift and boundary drift

Why this matters:

- the framework can detect more drift than before, but not yet reason deeply about architecture semantics

### 4. Workflow Interception Coverage

Current status:

- `pre_task_check` and `post_task_check` human outputs are more usable
- `suggested_rules_preview`, `suggested_skills`, `suggested_agent` exist
- `session_start.py` and `change_proposal_builder.py` provide startup/proposal context
- `change_control_summary.py` and `change_control_index.py` provide review-facing startup/change-control artifacts
- contract-aware smoke/dispatcher paths now exist
- external hook installation, onboarding, readiness, and smoke flows already exist

Next step:

- keep reducing friction in everyday usage
- make git-hook and CI-gate paths harder to skip in normal commit/merge flows
- keep improving external onboarding and contract-aware runtime entrypoints
- avoid framing IDE-native or token-by-token code-generation interception as an in-scope goal

Why this matters:

- the main interception problem is now practical workflow coverage, not missing validator execution

### 5. Failure Completeness Refinement

Current status:

- failure validators already exist
- runtime can gate on failure completeness evidence

Next step:

- strengthen exception-path evidence handling
- improve rollback / cleanup verification quality
- support richer metadata instead of relying mainly on signals and naming

Why this matters:

- current checks are useful but still partly heuristic

## Current Completed Milestones

The following items are now in place on `main`:

- `public_api_diff_checker.py`
- `kernel-driver` seed platform pack
- `platform` rule-pack category
- `driver_evidence_validator.py`
- driver-oriented ingestion in `test_result_ingestor.py`
- architecture drift v2 with before/after dependency-edge diff
- advisory `rule_pack_suggestions` in `state_generator.py`
- `.github` agent / skill governance layer
- `session_start.py` and shared session-start runtime flow
- proposal-time guidance and `change_proposal_builder.py`
- human-readable startup/proposal output improvements
- `change_control_summary.py` and `change_control_index.py`
- CI/runtime smoke startup artifacts: handoff notes, JSON envelopes, summaries, and index

### 6. Kernel-Driver Pack Refinement

Current kernel-driver pack is a strong seed, but still generic.

Recommended next split:

- `kernel-driver`
- later optional `kmdf`
- later optional `wdm`
- later optional `umdf`

Why this is not first:

- the generic seed pack is already useful
- splitting too early increases maintenance cost before usage patterns stabilize

### 7. Evidence Ingestion Expansion

Current ingestion supports:

- `pytest-text`
- `junit-xml`
- `sdv-text`
- `msbuild-warning-text`
- `sarif`
- `wdk-analysis-text`

Reasonable next additions:

- `compiler-warning-json`
- additional driver/security-tool evidence shapes when real usage justifies them

Why this matters:

- these formats are closer to real static-analysis and security-tool outputs
- they reduce ad hoc parsing in downstream validators

### 8. Memory / Audit Tightening

Potential follow-up work:

- store evidence summaries in session close artifacts
- preserve driver-specific evidence decisions in curated memory or audit summaries
- make promotion decisions more transparent for high-risk platform work
- keep proposal-time impact and runtime evidence linked in durable audit records

### 9. Review Surface Tightening

Potential follow-up work:

- make `change_control_summary` consume session-end summaries directly from more workflow entry points
- keep CI artifact naming and README instructions tightly aligned
- decide whether `INDEX.txt` should evolve into a richer human summary or stay intentionally lightweight

## Why The `passed` Count Changes

The `passed` number is not expected to stay fixed across turns.

Reasons:

- each turn only runs the most relevant test subset for the files changed in that step
- some turns validate a single tool or validator
- other turns validate a larger integration slice across runtime hooks, rule packs, and evidence ingestion

This means:

- different `passed` counts do **not** imply instability by themselves
- the meaningful signal is whether the targeted suite for that step passed cleanly

## Boundary To Protect

The repo should continue to evolve by:

- adding rule content
- adding evidence validators
- adding lightweight structural checks
- adding guided startup/proposal layers

It should avoid turning into:

- a heavy language-analysis platform
- a driver-development IDE workflow replacement
- a generic policy-engine runtime
- a code-generation-time interception layer inside the AI tool itself

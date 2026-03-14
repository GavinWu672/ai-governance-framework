# Knowledge Base

## Runtime Governance Maturity Snapshot

- The repository now operates as an AI Coding Runtime Governance Framework prototype with a full runtime spine:
  `session_start -> pre_task_check -> post_task_check -> session_end -> memory pipeline`.
- Multi-harness runtime support exists for Claude Code, Codex, and Gemini through native payload normalization, shared events, adapters, and dispatcher routing.
- Rule-pack governance is no longer limited to language packs; it now includes scope, language, framework, platform, and custom categories.
- Proposal-time governance is active. `architecture_impact_estimator.py` and `change_proposal_builder.py` produce structured previews before implementation begins.
- Reviewable change-control artifacts are now part of the governance surface via startup handoff notes, JSON envelopes, `change_control_summary.py`, and `change_control_index.py`.
- The runtime governance loop is real, but interception coverage is not yet fully closed across every developer and agent entrypoint.

## Evidence And Enforcement

- Evidence ingestion currently supports `pytest-text`, `junit-xml`, `sdv-text`, `msbuild-warning-text`, `sarif`, and `wdk-analysis-text`.
- Evidence is not only collected; it already feeds runtime validation through:
  - `failure_completeness_validator.py`
  - `refactor_evidence_validator.py`
  - `public_api_diff_checker.py`
  - `driver_evidence_validator.py`
  - `architecture_drift_checker.py`
- Current enforcement is evidence-aware and boundary-aware, but it is not yet a full semantic policy decision engine.

## Domain Extension Seam

- The repository now has an external domain validator seam rather than a fully mature plugin platform.
- `contract.yaml` discovery, external rule roots, validator preflight, and advisory validator execution are already working.
- The first domain vertical slice exists through `examples/usb-hub-contract/`, which validates firmware-specific constraints inside the governance runtime.
- Firmware evidence routing can currently infer interrupt context from explicit fields, `diff_text`, unified diff snippets, changed source files, and file-based `diff_file` inputs.
- This seam is intentionally advisory-first while payload shape and enforcement semantics are still being learned from real domain workflows.
- Multi-domain reviewer artifacts now preserve shared contract context:
  - `contract_source`
  - `contract_name`
  - `contract_domain`
  - `plugin_version`
  - `contract_risk_tier`
- Current built-in domain governance tiers are intentionally small and explicit:
  - `kernel-driver` = `high`
  - `firmware` = `medium`

## Boundary To Protect

- Packs provide governance context.
- Skills provide behavior guidance.
- Runtime checks and policies make decisions.
- Suggestions remain advisory and must not silently mutate the active contract.
- The repository should continue to act as a governance framework, not become a generic AI orchestration OS.

## Positioning

- The repository's rarest asset is the runtime governance lifecycle:
  `AI coding -> governance runtime -> evidence -> artifacts -> reviewer`.
- Rule packs and validators matter, but they derive their value from this runtime governance pipeline rather than replacing it.
- The current system should be described as a governance framework prototype with:
  - a complete runtime governance skeleton
  - an external domain validator seam
  - a first firmware domain vertical slice

## Planned Integration Direction

- A planned next step is to integrate the framework with `USB-Hub-Firmware-Architecture-Contract` as an external domain extension, not by merging repos.
- The intended seam is `contract.yaml` discovery, with the framework responsible for lifecycle/runtime governance and the firmware repo responsible for domain facts, rule packs, and validators.
- The next proof point after USB-Hub should be a second domain slice so the abstraction can be validated beyond firmware alone.

## Working Agreement

- For this repository, each task should be completed, reviewed, committed, and pushed before starting the next task.
- Task sequencing should favor small, isolated changesets so integration progress remains easy to audit and rollback.


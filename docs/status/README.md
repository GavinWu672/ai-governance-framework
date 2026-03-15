# Status Index

Updated: 2026-03-15

This directory contains the repository's stable status-facing documents.

## Current Entry Points

- [Trust Signal Dashboard](trust-signal-dashboard.md)
  - the fastest stable landing page for adoption and release-facing trust signals
  - points to `trust_signal_overview.py`, `trust_signal_snapshot.py`, `trust_signal_publication_reader.py`, and CI-generated trust-signal artifacts
  - the generated artifacts now also carry publication-level manifest/index metadata plus published history/index pages for stable linking, browsing, and reader-friendly consumption

- [Runtime Governance Status](runtime-governance-status.md)
  - the broader implementation and maturity snapshot
  - describes what is complete, what is still advisory, and where the main gaps remain

- [Domain Enforcement Matrix](domain-enforcement-matrix.md)
  - the clearest cross-domain view of `hard_stop_rules` vs advisory-only policy
  - use this when you want to compare enforcement posture across external contract repos

- Generated Status Snapshot (`generated/`)
  - optional local/published output from `trust_signal_snapshot.py --publish-docs-status`
  - intended for a stable repo-local consumption path when you want latest/history/site outputs under one predictable directory
  - read it through `governance_tools/trust_signal_publication_reader.py --docs-status` if you want the latest generated publication summary without resolving file paths manually
  - `generated/README.md` is the landing page for that generated root
  - core generated pages:
    - `generated/README.md`
    - `generated/PUBLICATION_INDEX.md`
    - `generated/site/README.md`
    - `generated/site/domain-enforcement-matrix.md`

- [Next Steps](next-steps.md)
  - forward-looking work recommendations
  - use this when you want direction, not only current-state reporting

## Recommended Reading Order

1. Start with [Trust Signal Dashboard](trust-signal-dashboard.md)
2. Then read [Runtime Governance Status](runtime-governance-status.md)
3. Then read [Domain Enforcement Matrix](domain-enforcement-matrix.md)
4. If generated, start with `generated/README.md`
5. Then review `generated/site/README.md` for the latest published snapshot
6. Use [Next Steps](next-steps.md) for future work planning

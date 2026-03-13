---
name: governance-runtime
description: Runtime governance compatibility rules for AI-assisted changes. Use when changing runtime hooks, validators, evidence ingestion, audit flow, state generation, or other governance-sensitive code paths.
---

# Governance Runtime Skill

This repository is governed by runtime-aware checks and evidence-aware validation.

## Required Mindset

Do not treat this repository like a generic coding repo.

Changes must remain compatible with:

- runtime hooks
- evidence ingestion
- policy evaluation
- memory and audit pipeline
- reviewable project truth

## Required Behavior

Before changing code, identify whether the task may affect:

- pre-task checks
- post-task checks
- session-end behavior
- evidence ingestion
- state generation
- rule pack suggestion logic
- curated audit outputs

## High-Risk Areas

Treat these as high-risk:

- dispatcher behavior
- event normalization
- adapter interfaces
- evidence parsing
- validation severity logic
- public API diff logic
- architecture drift logic
- failure completeness logic

## Anti-Regression Rules

Do not:

- weaken enforcement silently
- remove signals because they are noisy without documenting the tradeoff
- reduce evidence visibility
- hide uncertainty behind confident wording
- bypass governance steps for convenience

## Required Summary For High-Risk Changes

For any high-risk change, explain:

- what governance stage was affected
- whether enforcement strength changed
- whether evidence quality changed
- whether auditability changed
- whether workflow friction increased or decreased

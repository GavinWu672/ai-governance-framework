# Copilot Repository Instructions

This repository uses an AI Coding Runtime Governance Framework.

All AI-assisted changes must follow these principles:

## Core Principles

1. Prefer minimal, reviewable changes over broad rewrites.
2. Do not perform uncontrolled refactors.
3. Do not change architecture boundaries unless the task explicitly requires it.
4. Do not modify public APIs unless the change is intentional and explained.
5. Preserve auditability: the reason for the change should be reconstructable from task context, code diff, and evidence artifacts.

## Required Behavior

Before making non-trivial changes, the agent should:

- identify the task scope
- identify likely impacted modules
- identify whether architecture, public API, tests, or refactor-sensitive areas are involved
- prefer applicable rule packs when suggested by repository state

After making changes, the agent should:

- summarize what changed
- summarize what was intentionally not changed
- call out risks, assumptions, and follow-up validation needs
- avoid claiming success without evidence

## Refactor Policy

Refactors are high-risk by default.

The agent must not:

- rename modules casually
- move files without need
- rewrite large sections for cleanliness unless explicitly requested
- combine functional change and broad structural cleanup in one step unless required

If a refactor is necessary, the agent should explain:

- why the refactor is needed
- what boundaries are affected
- whether public APIs changed
- what evidence supports safety

## Testing And Evidence

Prefer evidence-backed claims.

Examples of acceptable evidence include:

- pytest output
- junit xml
- sarif
- msbuild warnings
- wdk analysis output
- public API diff
- architecture drift signals

Do not state that a change is safe, complete, or verified unless supported by evidence.

## Governance Compatibility

This repository may provide:

- rule pack suggestions
- pre-task guidance
- post-task validation
- session-end summaries
- curated audit artifacts

Treat repository governance outputs as high-priority project truth.

## Default Collaboration Style

- be precise
- be conservative with scope
- preserve architecture intent
- make reasoning reviewable
- optimize for long-term maintainability, not just local success

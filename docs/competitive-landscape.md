# Competitive Landscape

Updated: 2026-03-15

This document records the closest known open-source and commercial reference points for
`ai-governance-framework`.

Its purpose is not to claim feature parity. It is to keep the repository's positioning
honest:

- what is directly comparable
- what is only adjacent
- and what remains distinctive about this framework

## Short Positioning Summary

The most precise current positioning is:

- a runtime-governance prototype for AI coding workflows
- strongest on multi-repo external domain contracts
- stronger on mixed enforcement and reviewer publication surfaces than most nearby open-source peers
- intentionally not trying to become a full IDE-native interception layer or enterprise-wide AI compliance suite

## Quick Comparison View

| Project | Runtime enforcement | External domain contracts | Reviewer / trust publication | Primary center of gravity |
|---------|---------------------|---------------------------|------------------------------|---------------------------|
| `ai-governance-framework` | strong prototype | strong | strong | multi-repo runtime governance |
| `AI-Governor-Framework` | lighter / guidance-first | limited | lighter | repo-embedded governance rules |
| `GAAI-framework` | workflow-governed | limited | moderate | governed delivery workflow |
| `agentic-engineering-framework` | strongest direct peer on interception | limited | moderate | mechanical repo enforcement |
| `TinySDLC` | moderate | limited | moderate | multi-role SDLC orchestration |

This table is intentionally directional, not a claim of exact feature parity.

## Closest Open-Source References

### 1. AI-Governor-Framework

Reference:

- <https://github.com/Fr-e-d/AI-Governor-Framework>

Why it is close:

- repo-embedded governance rules
- project-aware constraints
- emphasis on architecture respect
- strong "AI should behave like a disciplined engineering partner" framing

Where it most resembles this repository:

- governance documents
- rule-driven behavioral constraints
- contract-like boundaries around AI work

Where this repository differs:

- stronger runtime lifecycle framing
- explicit external domain contract seam across multiple repos
- richer reviewer/audit publication surfaces
- more emphasis on validators that can affect post-task decisions, not only background rule guidance

### 2. GAAI-framework

Reference:

- <https://github.com/Fr-e-d/GAAI-framework>

Why it is close:

- governed delivery system framing
- explicit process boundaries
- context isolation between workflow phases

Where it most resembles this repository:

- proposal/planning discipline
- governed execution flow
- emphasis on repeatable delivery structure rather than prompt craft alone

Where this repository differs:

- stronger runtime hook / validator path
- more explicit mixed enforcement through `hard_stop_rules`
- more emphasis on trust-signal, release, and reviewer-handoff artifacts
- more emphasis on architecture/runtime evidence than on delivery-phase role choreography

### 3. agentic-engineering-framework

Reference:

- <https://github.com/DimitriGeelen/agentic-engineering-framework>

Why it is close:

- explicitly presents itself as a governance layer for AI coding tools
- emphasizes mechanical enforcement rather than soft guidelines
- focuses on continuity, rules, and blocking risky actions

Where it most resembles this repository:

- runtime governance framing
- task gate mindset
- practical enforcement posture

Where this repository differs:

- broader reviewer/audit publication path
- stronger external domain contract story
- richer cross-repo policy comparison and onboarding surfaces
- less focused on becoming a single-repo "mechanical door lock" and more focused on publishable, multi-domain governance posture

This is currently the closest reference point for interception-coverage thinking.

### 4. TinySDLC

Reference:

- <https://github.com/Minh-Tam-Solution/tinysdlc>

Why it is adjacent:

- structured handoffs
- role separation
- local-first orchestration

Where it most resembles this repository:

- reviewer handoff mindset
- structured flow instead of ad hoc prompting

Where it differs:

- more orchestrator / multi-role workflow oriented
- less centered on repo-native runtime governance and external contract seams
- closer to SDLC role choreography than contract-aware post-task runtime enforcement

## Adjacent, But Not Direct Peers

### VerifyWise

Reference:

- <https://github.com/bluewave-labs/verifywise>

Use it as a benchmark for:

- auditability
- governance visibility
- higher-level AI governance communication

Not a direct peer because:

- it is closer to AI governance / GRC than AI coding runtime governance

### Guardrails AI

References:

- <https://github.com/guardrails-ai/guardrails>
- <https://guardrailsai.com/>

Use it as a benchmark for:

- runtime validation patterns
- policy-style output control

Not a direct peer because:

- it is primarily an LLM-output/runtime validation system, not a repo-level coding governance framework

### CodeRabbit

Reference:

- <https://www.coderabbit.ai/>

Use it as a benchmark for:

- reviewer UX
- PR-facing consumption surfaces
- trust and adoption messaging

Not a direct peer because:

- it is primarily an AI-assisted review product, not an external-contract runtime governance framework

## What Currently Feels Distinctive Here

The clearest current differentiators of `ai-governance-framework` are:

- a real runtime governance loop:
  - `session_start -> pre_task_check -> post_task_check -> session_end -> memory pipeline`
- external domain contracts that live in separate repos
- mixed enforcement through domain validators plus `hard_stop_rules`
- reviewer-facing publication surfaces:
  - trust signals
  - release surfaces
  - reviewer handoff bundles
- memory artifacts that preserve domain contract metadata, not only generic session logs
- domain-specific governance for high-context and safety-sensitive areas such as firmware, kernel-driver, and IC verification

That means the repository is not only "AI rules in a repo."

It is closer to:

- a multi-repo runtime governance stack for AI coding

than to:

- a prompt pack
- a role-play orchestrator
- or a generic LLM guardrail wrapper

## Practical Borrowing Strategy

The most useful thing is not to copy any one project wholesale.

Instead:

- borrow interception ideas from `agentic-engineering-framework`
- borrow repo-embedded rule UX from `AI-Governor-Framework` and `GAAI-framework`
- borrow reviewer-surface clarity from products like `CodeRabbit`
- borrow auditability and visibility ideas from `VerifyWise`

This keeps the repository grounded in the parts of those projects that match its actual scope,
instead of drifting toward feature imitation for its own sake.

## Boundary To Preserve

While learning from these projects, this repository should still avoid drifting into:

- a plugin marketplace
- a generic multi-agent orchestration OS
- a code-generation-time interception layer inside the AI tool itself
- an enterprise-wide AI compliance platform far beyond coding governance

## One-Sentence Positioning

Compared with the nearest open-source references, `ai-governance-framework` is strongest when described as a multi-repo AI coding runtime-governance prototype with external domain contracts, mixed enforcement, and reviewer/audit publication surfaces.

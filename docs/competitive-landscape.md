# Competitive Landscape

Updated: 2026-03-15

This document records the closest known open-source and commercial reference points for
`ai-governance-framework`.

Its purpose is not to claim feature parity. It is to keep the repository's positioning
honest:

- what is directly comparable
- what is only adjacent
- and what remains distinctive about this framework

Important scope note:

- the comparisons below are directional
- they are based on public positioning, repository-visible structure, and top-level workflow emphasis
- they should not be read as exhaustive proof that another project cannot support a given pattern
- this document is safer when used to explain this repository's design choices than when used to claim another project definitively lacks a feature

## Short Positioning Summary

The most precise current positioning is:

- a runtime-governance prototype for AI coding workflows
- designed around multi-repo external domain contracts
- currently emphasizes mixed enforcement and reviewer publication surfaces
- intentionally not trying to become a full IDE-native interception layer or enterprise-wide AI compliance suite

## Quick Comparison View

| Project | Visible emphasis | Primary center of gravity | Why it is useful to compare |
|---------|------------------|---------------------------|-----------------------------|
| `ai-governance-framework` | multi-repo runtime governance, mixed enforcement, reviewer publication | runtime governance across framework + external contracts | reference row |
| `AI-Governor-Framework` | repo rules, architecture respect, guided behavior | repo-embedded governance rules | useful for rule UX and in-repo constraints |
| `GAAI-framework` | governed workflow and delivery structure | governed delivery workflow | useful for process and backlog discipline |
| `agentic-engineering-framework` | mechanical repo enforcement and task gating | mechanical runtime/repo enforcement | useful for practical interception ideas |
| `agent-governance-toolkit` | agent action policy enforcement and sandboxing | action-level agent governance | useful for layer comparison against runtime architecture governance |
| `TinySDLC` | role handoffs and SDLC choreography | multi-role SDLC orchestration | useful for handoff and role separation ideas |

This table is intentionally directional and should be read as a comparison of visible emphasis, not an exhaustive feature audit.

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

What this repository currently emphasizes in addition:

- a stronger runtime lifecycle framing
- an explicit external domain contract seam across multiple repos
- richer reviewer/audit publication surfaces
- validators that can affect post-task decisions, not only background rule guidance

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

What this repository currently emphasizes in addition:

- a stronger runtime hook / validator path
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

What this repository currently emphasizes in addition:

- a broader reviewer/audit publication path
- a stronger external domain contract story
- richer cross-repo policy comparison and onboarding surfaces
- a publishable, multi-domain governance posture rather than only a single-repo enforcement story

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

What this repository currently emphasizes instead:

- repo-native runtime governance and external contract seams
- contract-aware post-task runtime enforcement
- reviewer/audit publication surfaces over role choreography

### 5. agent-governance-toolkit

Reference:

- <https://github.com/microsoft/agent-governance-toolkit>

Why it is close enough to matter:

- it treats governance as an execution-time concern rather than only prompt guidance
- it emphasizes policy enforcement around agent actions and tool use
- it is a strong reference point for action-level interception thinking

Where it differs in layer:

- this repository focuses on task/session-boundary governance for coding work
- it appears focused on agent-action governance, identity, and execution policy around the agent runtime itself

Why that distinction matters:

- their core question is closer to "is this agent action allowed or safe?"
- this repository's core question is closer to "does this code/task output respect architecture, domain, and review boundaries?"

This makes it an important benchmark, but not a one-to-one peer.

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

### SAFi

Reference:

- <https://github.com/jnamaya/SAFi>

Use it as a benchmark for:

- runtime output governance
- value/constitution framing
- post-generation audit patterns

Not a direct peer because:

- it is better understood as output/runtime governance for AI behavior rather than repo-native coding architecture governance

### GitHub Spec Kit

Reference:

- public GitHub Spec Kit materials / repos

Use it as a benchmark for:

- spec-driven development
- executable specification workflows
- reducing "prompt-and-pray" through explicit planning artifacts

Not a direct peer because:

- it is more naturally read as specification-driven implementation guidance than as mixed-enforcement runtime governance

It is complementary:

- spec-driven generation and contract-driven post-task governance can coexist

### Sovereign-OS

Reference:

- public Sovereign-OS materials / repos

Use it as a benchmark for:

- append-only governance trails
- mission/budget/rule declaration
- governance over agent resource usage

Not a direct peer because:

- it is closer to budget/token/mission governance than software architecture boundary governance

### GitHub Agent HQ / Agentic Workflows

Reference:

- public GitHub platform materials and reporting

Use it as a benchmark for:

- platform-level agent governance
- central mission control and auditability
- enterprise-facing agent operations

Not a direct peer because:

- it is platform governance for agent operations
- this repository is domain-knowledge governance for architecture-sensitive coding workflows

This distinction is important when explaining why a repo-level governance framework still has value alongside platform-native agent governance.

### Agent Behavioral Contracts (ABC) / POLARIS

References:

- public academic literature and workshop papers

Use them as benchmarks for:

- formal contract thinking
- drift bounds
- validator-gated orchestration
- stronger theoretical framing around runtime governance

Not direct peers because:

- they are better treated as theory and research direction, not drop-in repo-native coding governance systems

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

- borrow git-hook / CI-gate interception ideas from `agentic-engineering-framework`
- study action-level governance boundaries from `agent-governance-toolkit` without drifting into generation-time interception goals
- borrow repo-embedded rule UX from `AI-Governor-Framework` and `GAAI-framework`
- borrow reviewer-surface clarity from products like `CodeRabbit`
- borrow auditability and visibility ideas from `VerifyWise`
- treat `GitHub Spec Kit`, `ABC`, and `POLARIS` as useful framing for specification/contract rigor rather than direct implementation targets

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

---
audience: agent-runtime
authority: canonical
can_override: false
overridden_by: ~
default_load: always
---

# AGENT.md
**AI Agent Behavioral Contract - v4.3**

> **Version**: 4.3 | **Priority**: 4 (Behavioral Contract)
>
> Defines how the agent thinks, acts, decides, and escalates.
> Identity is defined by `SYSTEM_PROMPT.md`. Escalation authority is `HUMAN-OVERSIGHT.md`.
> This file is the canonical repo-local behavioral contract for `L0/L1/L2`
> classification and execution expectations. Workspace-level `AGENTS.md`
> defines session behavior and operating etiquette, not repo governance levels.

---

## 1. Level Alignment

- Declared `L0` but involves domain logic, boundary crossing, native interop, workflow ownership, or behavior change -> **upgrade to L1**
- Declared `L1` but involves core domain, security, data integrity, flash path, or irreversible state transitions -> **upgrade to L2**

Uncertain classification -> upgrade, do not downgrade.

---

## 2. Operating Modes

### 2.1 `SCOPE = review` -> Auditor Sub-Mode

When `SCOPE = review`:
- execution pipeline is suspended
- `REVIEW_CRITERIA.md` governs behavior
- the agent is a skeptical verifier, not the implementer

### 2.2 L0 - Fast Track

Allowed only when **all** conditions hold:
- scope limited to typo, comments, formatting, naming, or equivalent presentation-only cleanup
- or narrowly bounded UI/prototype shaping that does not change domain behavior
- no domain logic change
- no boundary crossing
- no I/O, native interop, or resource lifetime change
- intent and outcome are unambiguous

L0 fast-track execution path:
1. state the bounded surface being changed
2. state why the work remains presentation-only or behavior-neutral
3. implement the minimum change
4. capture one lightweight verification step
5. record any upgrade trigger immediately if the work stops being trivial

L0 does **not** require the full `Analyze -> Define -> Test -> Implement`
ceremony when the task remains inside this fast-track boundary.

Forbidden even in `L0`:
- native interop
- memory ownership changes
- domain/infrastructure interaction
- conditional behavior introduction
- retry logic, acquisition logic, sequencing logic
- schema changes
- API contract changes
- persistence, network, filesystem, or time-dependent behavior

Upgrade from `L0` to `L1` immediately when any of the following appear:
- visual changes require behavior changes to make sense
- a schema, DTO, or payload shape must change
- more than one reasonable UX or implementation path exists with different trade-offs
- verification needs more than a smoke/manual check
- the change starts touching reusable component logic instead of presentation-only wiring

### 2.3 Low-Risk L1 Examples

The following are typically **L1 but low-risk**, not L2:
- UI copy consistency
- status color tokenization
- hint/warning message consistency
- message box severity normalization
- success/wait/failure prompt completion

These remain `L1` because they affect user-facing behavior, but they are not automatically critical-path work.

### 2.4 L2 - Critical

Applies to:
- core domain logic
- native or interop boundaries
- flash/programming/firmware sequencing
- security, correctness, or data-integrity critical paths

Must fully apply `ARCHITECTURE.md` and `TESTING.md`, and must not take shortcuts without human approval.

---

## 3. Execution Pipeline

For `L0`, use the fast-track path in Section 2.2.

For `L1+`, default workflow is:

1. **Analyze** - behavior and constraints first
2. **Define** - contracts, boundaries, failure paths
3. **Test/Verify Plan** - what evidence will prove safety
4. **Implement** - minimum compliant change
5. **Refactor** - only under evidence protection

Do not skip a step when the omission would hide risk. Do not force ceremony when the task is clearly bounded and low risk.

---

## 4. Continue / Escalate / Stop

### 4.1 Continue

Proceed directly when:
- task is bounded
- risk is low
- next evidence step is clear
- no human-value choice is being hidden

### 4.2 Escalate

Escalate when:
- more than one reasonable path exists with materially different trade-offs
- adjacent work is safe, but extension beyond that point becomes ambiguous
- commit scope cannot be kept clean
- touched files overlap with unrelated dirty worktree changes
- classification or architecture impact is unclear but not yet a hard red line

### 4.3 Stop

Stop only when:
- hard safety or architecture red line is triggered
- correctness cannot be defended
- governance documents conflict materially
- human authorization is required for a truly high-risk action

Do not use `STOP` as a substitute for normal engineering judgment.

---

## 5. Architecture Guardrails

- Domain must not depend on OS, filesystem, network, UI, time, or environment state
- Infrastructure must remain replaceable
- any abstraction must answer: "What breaks in 2 years if not abstracted?"

Unclear answer -> escalate or stop depending on risk.

---

## 6. Workflow Reality Rules

### 6.1 Adjacent Engineering Work

The agent may perform bounded adjacent engineering work without separate approval when it stays within current touched scope and does not cross a hard boundary:
- build/test
- debugging
- review
- commit preparation
- governance analysis
- documentation synchronization

### 6.2 Dirty Worktree Policy

When the worktree is already dirty:
- unrelated dirty files may be ignored
- unrelated untracked files do not block the task
- overlapping edits in touched files -> **ESCALATE**
- commit scope cannot be separated cleanly -> **ESCALATE**

Do not revert unrelated changes.

### 6.3 Legacy Refactor Start Policy

For legacy/refactor tasks:
- confirm the canonical toolchain first
- confirm the canonical build command first
- validate the chosen baseline before treating it as stable

If baseline verification fails, continue only as analysis unless the human explicitly accepts the risk.

---

## 7. Language-Specific Rules

### C++

- explicit ownership/lifetime
- prefer RAII
- guard error paths
- flag undefined behavior risks
- no exceptions across ABI boundaries

### C#

- prevent infrastructure leakage into domain
- validate async failure paths
- UI thread-affecting updates must use `Dispatcher.UIThread` or equivalent

### Objective-C / Swift / JS

Apply equivalent explicit-boundary and explicit-error-model discipline.

---

## 8. Tech Debt Policy

Any compromise must record:
- reason
- risk
- explicit removal condition

No removal condition -> reject the compromise.

---

## 9. Forbidden Behaviors

- expand beyond instruction scope
- refactor unrelated areas for cleanliness
- add speculative abstractions
- fake or inflate evidence
- assume intent under ambiguity

---

## 10. Definition of Success

Success means:
- behavior is explicit
- failure paths are guarded
- boundary rules remain intact
- the chosen evidence matches the risk
- progress remains implementable, not just discussable

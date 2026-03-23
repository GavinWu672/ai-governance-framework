# KDC Domain Adapter Summary

> Domain: `kernel-driver`
> Status: active summary
> Target: low-token adapter view for `Kernel-Driver-Contract`
> Primary sources:
> - `Kernel-Driver-Contract/contract.yaml`
> - `Kernel-Driver-Contract/AGENTS.md`
> - `Kernel-Driver-Contract/KERNEL_DRIVER_CHECKLIST.md`
> - `Kernel-Driver-Contract/KERNEL_DRIVER_ARCHITECTURE.md`
> - `Kernel-Driver-Contract/rules/kernel-driver/safety.md`

---

## Overview

`Kernel-Driver-Contract` is a Windows kernel-driver governance slice.

Its core model is not "general C correctness". It is:

- fact-gated driver reasoning
- lifecycle / state-invariant enforcement
- hard-stop safety rules for IRQL, ISR/DPC, IRP, sync primitive, static-analysis, and unit-test boundaries

This domain should be treated as hardware-facing and failure-intolerant.
If key platform facts are unknown, the agent must stop implementation guidance rather than improvise.

## Decision Model

The domain expects this reasoning order before non-trivial guidance:

1. classify missing vs confirmed facts
2. identify active lifecycle state and applicable `KSTATE-*` rules
3. decide whether guidance is allowed, blocked, or limited to review notes
4. cite the governing rule ID when constraining or rejecting advice

If that order is skipped, the response is not contract-compliant.

## Fact Classes

### Human-mandatory facts

These must not be invented by the agent.

Examples:

- driver model: `WDM` / `KMDF` / `UMDF`
- target OS / active WDK version
- PnP model and power-managed status
- maximum reachable IRQL
- interrupt model
- DMA model
- config-space access level
- pool allocation policy
- Driver Verifier / SDV availability when relevant

Rule:

- if a required human-mandatory fact is unresolved, stop implementation guidance
- ask for the missing source or confirmed fact

### AI-verifiable facts

These may be derived from code, but must be surfaced as derived observations with source locations.

Examples:

- IO buffering model
- IOCTL surface presence
- device naming / security descriptor model
- remove-lock usage
- locking primitive model
- IRP completion model
- cleanup / unwind pattern

Rule:

- bounded code scan is allowed
- derived facts must not be silently promoted into hardware truth

## Architecture Invariants

The architecture model is state-bound, not just layered.

Important invariants:

- PnP state controls hardware resource visibility
- low-power states restrict legal work
- ISR / DPC work must remain non-blocking and non-pageable
- DMA ownership is valid only within the correct started-device lifetime
- namespace / IOCTL exposure is treated as part of the driver contract
- every acquisition path needs explicit teardown across start, stop, surprise-remove, remove, cancel, and power transitions

Practical reading:

- if lifecycle state is unknown, stop
- if resource lifetime is unclear, stop
- if teardown is missing, block or escalate

## Hard-Stop Rules

The contract currently promotes these rule IDs as blocking:

- `KD-002` no paged / blocking access at `DISPATCH_LEVEL`
- `KD-003` no synchronous wait in IRP completion paths
- `KD-006` synchronization primitive must match IRQL
- `KD-007` ISR / DPC must remain non-blocking and non-pageable
- `KD-010` static-analysis / verifier-clean requirement on changed paths

Also important:

- `KD-011` user-mode unit tests must use real seams; no fake `ntddk.h` / `wdf.h` / WDK-header stubbing

## Validator Surface

Registered validators:

- `irql_safety_validator.py`
- `dpc_isr_validator.py`
- `pool_type_validator.py`
- `sync_primitive_validator.py`
- `pageable_section_validator.py`
- `dispatch_routine_validator.py`
- `static_analysis_validator.py`

What they mean in practice:

- IRQL and interrupt-path safety are first-class review surfaces
- sync primitive choice is checked against execution level
- pageable / non-pageable discipline is explicit
- dispatch registration and static-analysis evidence matter

## AI Guidance Constraints

When operating inside this domain, the agent should:

- prefer review notes over speculative implementation when facts are incomplete
- state IRQL expectations explicitly
- preserve cleanup / unwind paths
- preserve remove / surprise-remove / power-transition safety boundaries
- recommend `WdfXxx`-level patterns only when the underlying driver model is actually confirmed

The agent must not:

- recommend kernel APIs when current IRQL is unknown
- assume paged memory is safe everywhere
- suggest blocking or pageable work at `DISPATCH_LEVEL` or above
- suggest hardware access when start / power / interrupt lifetime is unresolved
- suppress or work around validator `HARD-STOP` findings
- propose fake WDK-header stubs for user-mode unit tests

## Integration Notes

Use this summary as the default slim domain view for token-sensitive runtime paths.

Escalate to the full contract when:

- a human-mandatory fact is missing and the exact checklist field matters
- a lifecycle-sensitive path needs the full `KSTATE-*` framing
- validator findings need full rule/context mapping
- reviewer handoff needs source-precise contract language

## Expected Runtime Effect

This summary is meant to replace high-cost inline kernel-driver contract loading for:

- onboarding-shaped sessions
- normal L1 review / implementation sessions
- repo-type classification paths that only need the domain's decision skeleton

The expected benefit is lower `domain_contract` token cost while preserving:

- fact-stop behavior
- state-invariant framing
- hard-stop rule awareness
- validator surface awareness

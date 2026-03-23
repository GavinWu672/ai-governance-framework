# KDC Domain Adapter Summary

> Domain: kernel-driver-contract
> Status: PLACEHOLDER — human must fill this in
> Target tokens: ~1,500 (vs full contract ~13,605)
> Source: Kernel-Driver-Contract/contract.yaml

---

## Overview

**Kernel Driver Contract (KDC)** governs AI-assisted development of Windows kernel-mode drivers.
All changes must conform to KMDF/WDM/UMDF safety rules, WHQL submission requirements,
and ISR/DPC safety constraints.

---

## Key Rules (Summary)

| Category | Constraint |
|----------|-----------|
| Memory safety | No heap allocation in ISR/DPC; use lookaside lists |
| IRQL discipline | Functions must document IRQL preconditions; callers must verify |
| IRP handling | Always complete IRPs; never leak pending IRPs |
| Registry access | Use Reg* APIs only at PASSIVE_LEVEL |
| Synchronisation | Prefer spin locks for short critical sections; ERESOURCE for long ones |
| Code signing | All production builds must be EV-signed before submission |

---

## Validator Summary

- `irql_check` — Validates IRQL annotations in function declarations
- `irp_completion` — Checks all IRP dispatch paths complete or mark-pending
- `whql_preflight` — Validates WHQL submission checklist fields

---

## Architecture Constraints

- `src/` — Driver source; all files subject to cpp + kernel-driver rules
- `validators/` — Governance validators; not subject to driver rules
- `fixtures/` — Test fixtures; not subject to driver rules

---

## AI Behaviour Overrides

- Prefer explicit error handling over assertions in kernel code
- Never suggest dynamic memory allocation in interrupt handlers
- Always recommend WdfXxx APIs over legacy WDM equivalents where available
- Flag any `KeAcquireSpinLock` usage without paired `KeReleaseSpinLock`

---

_This summary was auto-generated as a placeholder. Replace with actual contract content
after reviewing Kernel-Driver-Contract/contract.yaml and associated governance documents._

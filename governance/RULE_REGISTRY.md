---
audience: agent-runtime
authority: canonical
default_load: always
---

# Governance Rule Registry

This file is the authoritative registry of valid rule pack names.
Any rule pack not listed here will cause `Unknown rule packs: [...]` errors.

Machine-readable by `governance_tools/rule_classifier.py`.

Rule packs are selected at session start based on:
- `repo_type`: firmware | product | service | tooling
- `task_type`: general | refactor | release | review | onboarding | test
- `load_mode`: always | context_aware

`always` packs are loaded in every session regardless of context.
`context_aware` packs are activated only when `repo_type` and `task_type` match.

---

## Valid Rule Packs (Quick Reference)

| Pack Name | Description | Typical Use |
|---|---|---|
| `common` | Universal baseline rules | All repos (always include) |
| `cpp` | C/C++ code standards | Firmware, driver, embedded repos |
| `csharp` | C# code standards | .NET, Avalonia repos |
| `kernel-driver` | Kernel/driver-specific constraints | KDC and similar driver repos |
| `python` | Python code standards | Service, tooling repos |
| `refactor` | Refactoring guidance | Any repo undergoing refactor |
| `release` | Release checklist rules | Release sessions |
| `review_gate` | Review gate checklist | Review sessions |
| `swift` | Swift code standards | iOS/macOS repos |
| `avalonia` | Avalonia UI framework rules | Desktop app repos |
| `typescript` | TypeScript/Node.js standards | Product repos |
| `electron` | Electron IPC security rules | Electron app repos |
| `nextjs` | Next.js routing and rendering rules | Next.js product repos |
| `supabase` | Supabase RLS and auth rules | Supabase-backed repos |
| `firmware_isr` | ISR safety and RTOS constraints | Firmware repos |

---

## Rule Packs (Machine-Readable Metadata)

### common

```yaml
name: common
load_mode: always
repo_type: [all]
task_type: [all]
risk_level: [all]
description: "Core coding standards — loaded in every session"
```

### refactor

```yaml
name: refactor
load_mode: context_aware
repo_type: [all]
task_type: [refactor]
risk_level: [all]
description: "Refactoring patterns — activated when task_type=refactor"
```

### release

```yaml
name: release
load_mode: context_aware
repo_type: [all]
task_type: [release]
risk_level: [all]
description: "Release checklist rules — activated when task_type=release"
```

### typescript

```yaml
name: typescript
load_mode: context_aware
repo_type: [product]
task_type: [all]
risk_level: [all]
description: "TypeScript/Node.js best practices for product repos"
```

### python

```yaml
name: python
load_mode: context_aware
repo_type: [service, tooling]
task_type: [all]
risk_level: [all]
description: "Python coding standards for service and tooling repos"
```

### electron

```yaml
name: electron
load_mode: context_aware
repo_type: [product]
task_type: [all]
risk_level: [all]
description: "Electron IPC security and process isolation rules"
```

### avalonia

```yaml
name: avalonia
load_mode: context_aware
repo_type: [product]
task_type: [all]
risk_level: [all]
description: "Avalonia UI component and threading rules"
```

### cpp

```yaml
name: cpp
load_mode: context_aware
repo_type: [firmware, product]
task_type: [all]
risk_level: [all]
description: "C++ memory safety and RAII rules"
```

### csharp

```yaml
name: csharp
load_mode: context_aware
repo_type: [product]
task_type: [all]
risk_level: [all]
description: "C# async patterns and null safety rules"
```

### swift

```yaml
name: swift
load_mode: context_aware
repo_type: [product]
task_type: [all]
risk_level: [all]
description: "Swift value-type safety and concurrency rules"
```

### nextjs

```yaml
name: nextjs
load_mode: context_aware
repo_type: [product]
task_type: [all]
risk_level: [all]
description: "Next.js routing, data fetching, and rendering rules"
```

### supabase

```yaml
name: supabase
load_mode: context_aware
repo_type: [product]
task_type: [all]
risk_level: [all]
description: "Supabase RLS policies and auth integration rules"
```

### firmware_isr

```yaml
name: firmware_isr
load_mode: context_aware
repo_type: [firmware]
task_type: [all]
risk_level: [all]
description: "ISR safety, RTOS constraints, and HAL boundary rules for firmware repos"
```

### kernel-driver

```yaml
name: kernel-driver
load_mode: context_aware
repo_type: [firmware]
task_type: [all]
risk_level: [all]
description: "Kernel/driver-specific constraints for KDC and similar driver repos"
```

### review_gate

```yaml
name: review_gate
load_mode: context_aware
repo_type: [all]
task_type: [review]
risk_level: [all]
description: "Review gate checklist — activated for review task sessions"
```

---

## How Rule Packs Are Selected

Rule packs are selected by `_get_default_rule_packs()` in `adopt_governance.py`
based on detected repo type, or passed explicitly via `--rules` CLI argument.

Use `get_context_aware_rule_packs()` or `available_rule_packs()` from
`governance_tools/rule_pack_loader.py` to enumerate valid options programmatically.

---

## ⚠️ `onboarding` is NOT a valid rule pack

`onboarding` is **not** a rule pack name. If you see:

```
Unknown rule packs: ['onboarding']
```

This means `adopt_governance.py` or a calling script is passing `"onboarding"` as a
rule pack argument. Fix by removing it and using `get_context_aware_rule_packs()` or
an explicit valid pack from the table above.

**Correct approach for onboarding sessions:**

| Repo Type | Rule Packs |
|---|---|
| Firmware / driver repo | `["common", "cpp", "kernel-driver"]` |
| Product repo (TypeScript) | `["common"]` |
| Service repo (Python) | `["common", "python"]` |
| Unknown | `["common"]` |

Onboarding sessions use the same rule packs as regular L1 sessions for that repo type.
There is no special `onboarding` rule pack.

# Domain Enforcement Matrix

Updated: 2026-03-15

This page is the stable in-repo entry point for comparing enforcement posture
across external domain-contract repos.

Use it when you want to answer:

- which domains are still advisory-only
- which domains now support mixed enforcement
- which rule IDs are currently routed through `hard_stop_rules`

## Fastest Local Command

```bash
python governance_tools/external_contract_policy_index.py \
  --repo D:/USB-Hub-Firmware-Architecture-Contract \
  --repo D:/Kernel-Driver-Contract \
  --repo D:/IC-Verification-Contract \
  --format human
```

Markdown output:

```bash
python governance_tools/external_contract_policy_index.py \
  --repo D:/USB-Hub-Firmware-Architecture-Contract \
  --repo D:/Kernel-Driver-Contract \
  --repo D:/IC-Verification-Contract \
  --format markdown
```

## Current Reading

At the moment, the framework's three real external contract repos all expose a
mixed-enforcement posture:

| Repo | Domain | Hard-Stop Rules | Advisory Surface |
| --- | --- | --- | --- |
| `USB-Hub-Firmware-Architecture-Contract` | `firmware` | `HUB-004` | broader firmware review, e.g. `HUB-001` |
| `Kernel-Driver-Contract` | `kernel-driver` | `KD-002`, `KD-003` | pool-allocation guidance such as `KD-005` |
| `IC-Verification-Contract` | `ic-verification` | `ICV-001` | clock/reset declaration checks such as `ICV-002` |

## Why This Matters

This matrix makes one important project boundary explicit:

- the framework no longer stops at validator discovery
- domain validators already execute
- selected domain rule IDs can now affect runtime outcomes through `hard_stop_rules`

But this still does **not** mean:

- every domain rule is hard-stop
- every domain has equally deep evidence
- the framework has become a full policy engine

The matrix is here to keep those enforcement boundaries legible.

## Related Sources

- [Status Index](README.md)
- [Runtime Governance Status](runtime-governance-status.md)
- [Trust Signal Dashboard](trust-signal-dashboard.md)

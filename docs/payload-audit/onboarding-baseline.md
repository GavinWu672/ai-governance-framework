# Onboarding Payload Baseline

> Date: 2026-03-23
> Scope: onboarding / adoption-shaped payload measurements
> Tool: `governance_tools/payload_audit_logger.py`

---

## Step 7 Rebaseline -- framework self-onboarding-shaped run (2026-03-23)

> Task: `Adopt governance baseline for external repo`
> Commit: `37b2331`

| Field | Value |
|------|------|
| session_type | `onboarding` |
| ok | `true` |
| combined_estimate | `21088` |
| result_dict_total | `9208` |
| rendered_output | `11880` |
| warning_count | `4` |
| top fields | `pre_task_check`, `domain_contract`, `state`, `change_proposal`, `rule_pack_suggestions` |

### Delta vs prior onboarding baseline

| Metric | Prior | Step 7 | Delta |
|------|------:|--------:|------:|
| combined_estimate | `60623` | `21088` | `-39535` |
| reduction | - | - | `-65.2%` |

Interpretation:
- This path is now dramatically lower than the old Kernel-Driver-Contract onboarding baseline.
- The main gain is from summary-first / framework-self contract shape, not from generic L1 compression alone.
- The runtime now emits a dedicated `onboarding-*.jsonl` lane for onboarding tasks.
- Windows terminal output now falls back safely when the active code page cannot encode some Unicode characters.

---

## Step 1 Initial KDC Onboarding Baseline (2026-03-23)

### Session A -- onboarding ok=True

| Component | Tokens | Share |
|------|-------:|------:|
| Governance + Domain Contract | `27640` | `45.6%` |
| Rendered output overhead | `32983` | `54.4%` |
| **Session total** | **`60623`** | `100%` |

### Session B -- onboarding ok=False

> Failure reason: `Unknown rule packs: ['onboarding']`

| Component | Tokens | Share |
|------|-------:|------:|
| Governance + Domain Contract | `27215` | `45.2%` |
| Rendered output overhead | `32983` | `54.8%` |
| **Session total** | **`60198`** | `100%` |

Interpretation:
- The old KDC onboarding path was dominated by a heavy inline domain contract plus large rendered output.
- Even the failure case stayed expensive because the rendered response surface was still large.

---

## KDC Summary-First Recheck (2026-03-23)

> Target: `Kernel-Driver-Contract`
> Mode: in-process `build_session_start_context()` measurement with `summary_first`

| Field | Value |
|------|------|
| combined_estimate | `37142` |
| result_dict_total | `17170` |
| rendered_output | `19972` |
| domain_contract_tokens | `1840` |
| domain_contract_slim | `true` |
| summary_source | `kernel-driver-adapter-summary.md` |

### Delta vs old KDC onboarding baseline

| Metric | Prior | Summary-first | Delta |
|------|------:|-------------:|------:|
| combined_estimate | `60623` | `37142` | `-23481` |
| domain_contract field | `13605` | `1840` | `-11765` |
| reduction | - | - | `-38.7%` |

Interpretation:
- Filling `kernel-driver-adapter-summary.md` produced a real reduction, not just a projected one.
- The biggest direct gain is the domain-contract slice itself.
- Total onboarding cost is still substantial because `pre_task_check` and rendered output remain large.
- External-repo audit artifact emission for this rerun was blocked by sandbox write permissions, so this measurement was captured in-process rather than by writing a new external JSONL line.

---

## Key Takeaways

1. The old KDC onboarding path was not mainly expensive because of adoption logic; it was expensive because of contract and output shape.
2. `kernel-driver-adapter-summary.md` is now live and materially lowers the KDC onboarding path.
3. The next optimization target is not "fill the KDC summary" anymore; it is `pre_task_check` and rendered output on the onboarding path.
4. A dedicated onboarding short-circuit may still be worth testing, but only after measuring whether it reduces those two remaining dominant slices.

## Next Actions

1. Reduce `pre_task_check` cost on the KDC onboarding path.
2. Reduce rendered-output size on the same path.
3. Decide whether onboarding deserves its own short-circuit now that summary-first is live.
4. Re-run a true external-repo onboarding audit once write access to the external repo's `docs/payload-audit/` directory is available.

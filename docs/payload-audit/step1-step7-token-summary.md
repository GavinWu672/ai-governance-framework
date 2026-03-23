# Step 1-Step 7 Token Summary

> Date: 2026-03-23
> Purpose: summarize the token impact of the full Step 1-Step 7 roadmap.

## Measurement Basis

This summary uses:

- Step 1 initial baselines already recorded in:
  - [L0-baseline.md](/e:/BackUp/Git_EE/ai-governance-framework/docs/payload-audit/L0-baseline.md)
  - [L1-baseline.md](/e:/BackUp/Git_EE/ai-governance-framework/docs/payload-audit/L1-baseline.md)
  - [onboarding-baseline.md](/e:/BackUp/Git_EE/ai-governance-framework/docs/payload-audit/onboarding-baseline.md)
- Step 7 rebaseline measurements recorded in the same files

## Per-Flow Change

| Flow | Step 1 | Step 7 | Delta | Reduction |
|------|-------:|-------:|------:|----------:|
| `L0` | `19330` | `6550` | `-12780` | `-66.1%` |
| `L1` | `24743` | `21564` | `-3179` | `-12.8%` |
| `Onboarding` | `60623` | `21088` | `-39535` | `-65.2%` |

## Combined Totals

### Observed total

This uses all three current Step 7 measurements as-is.

| Metric | Total |
|------|------:|
| Step 1 combined | `104696` |
| Step 7 combined | `49202` |
| Net reduction | `-55494` |
| Overall reduction | `-53.0%` |

### Strict comparable total

This excludes the onboarding comparison because the old onboarding baseline was a heavy `Kernel-Driver-Contract` run, while the new Step 7 onboarding-shaped measurement was a framework self-run. That makes it useful, but not fully apples-to-apples.

| Metric | Total |
|------|------:|
| Step 1 strict (`L0 + L1`) | `44073` |
| Step 7 strict (`L0 + L1`) | `28114` |
| Net reduction | `-15959` |
| Overall reduction | `-36.2%` |

## Interpretation

- The roadmap clearly succeeded for `L0`.
- The roadmap produced a real but smaller gain for generic `L1`.
- The biggest observed reduction came from the onboarding-shaped path.
- Step 7 itself did not make generic `L1` cheaper; the `L1` Step 7 run is slightly above the prior post-Step-5b+6 number.
- The strongest remaining optimization leverage is still domain-summary / onboarding shaping, not more output-tier work in isolation.

## Key Inflection

The most important shift in this roadmap was not just reducing input payload.
It was recognizing that output design was also part of the token problem.

That said, the rebaseline shows the effect is uneven:

- `output tier separation` helped make heavy onboarding-style output much cheaper
- but it did not automatically reduce all normal `L1` sessions

## Remaining Follow-Ups

Highest-value next candidates:

1. Fill [kdc-adapter-summary.md](/e:/BackUp/Git_EE/ai-governance-framework/docs/domain-summaries/kdc-adapter-summary.md) with real content
2. Decide whether onboarding deserves its own explicit short-circuit path
3. Re-evaluate whether `Step 3b` full memory refactor is still worth the cost
4. Fix the Windows `cp950` JSON output issue in [session_start.py](/e:/BackUp/Git_EE/ai-governance-framework/runtime_hooks/core/session_start.py)

## Caveats

- The onboarding comparison is operationally useful but not fully like-for-like.
- `session_start.py` can still hit a Windows `UnicodeEncodeError` when printing large JSON to a `cp950` terminal.
- The audit record is still reliable even when that terminal output fails.

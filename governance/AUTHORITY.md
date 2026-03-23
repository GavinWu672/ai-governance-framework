# Governance Authority Table

> machine-readable: true
> version: 1.0.0
> updated: 2026-03-23

## Authority Levels

- `canonical` — 唯一真實來源，衝突時最高優先，不得被 derived 覆蓋
- `reference`  — 可信來源，可被 canonical 覆蓋，不得被 derived 覆蓋
- `derived`    — 從 canonical/reference 生成的快取或摘要，衝突時最低優先

## Audience Types

- `agent-runtime`   — session_start 永遠載入
- `agent-on-demand` — 命中特定條件才載入
- `human-only`      — agent 永遠不載入

## Default Load Modes

- `always`       — 無條件載入（僅限 canonical/derived agent-runtime 文件）
- `on-demand`    — 依 context 判斷是否載入
- `incremental`  — 只載增量 candidates，不做 full rescan
- `never`        — 永遠不載入（human-only 文件）

---

## Authority Table

| document | audience | authority | can_override | overridden_by | default_load |
|----------|----------|-----------|--------------|---------------|--------------|
| `governance/SYSTEM_PROMPT.md` | agent-runtime | canonical | false | — | always |
| `governance/AGENT.md` | agent-runtime | canonical | false | — | always |
| `governance/PLAN.md` | agent-runtime | canonical | false | — | always |
| `governance/ARCHITECTURE.md` | agent-on-demand | reference | false | SYSTEM_PROMPT.md | on-demand |
| `governance/TESTING.md` | agent-on-demand | reference | false | AGENT.md | on-demand |
| `governance/NATIVE-INTEROP.md` | agent-on-demand | reference | false | AGENT.md | on-demand |
| `governance/HUMAN-OVERSIGHT.md` | human-only | reference | false | — | never |
| `governance/REVIEW_CRITERIA.md` | human-only | reference | false | — | never |
| `AGENTS.md` (workspace) | agent-runtime | derived | false | AGENT.md | always |
| `.github/copilot-instructions.md` | agent-runtime | derived | false | AGENT.md | always |
| `.github/agents/*.agent.md` | agent-on-demand | derived | false | AGENT.md | on-demand |
| `domain contract (full)` | agent-on-demand | canonical | false | — | on-demand |
| `domain adapter summary` | agent-runtime | derived | false | domain contract | always |
| `memory/02_project_facts.md` | agent-runtime | canonical | false | — | incremental |
| `memory/03_decisions.md` | agent-runtime | canonical | false | — | incremental |
| `memory/reviewer_handoff_*` | agent-on-demand | derived | false | 03_decisions.md | on-demand |
| `memory/framework_artifact_*` | agent-on-demand | derived | false | — | on-demand |
| `memory/external_repo_aliases` | agent-on-demand | reference | false | — | on-demand |

---

## Conflict Resolution Rules

優先順序（高到低）：
```
canonical > reference > derived
```

具體規則：

1. `canonical` vs `reference` → canonical 優先，reference 的衝突欄位被忽略
2. `canonical` vs `derived`   → canonical 優先，derived 視為過期快取
3. `reference` vs `derived`   → reference 優先
4. workspace instruction（AGENTS.md、copilot-instructions）→ 永遠不得覆蓋 repo canonical
5. `agent-on-demand` 文件     → 可讀取 reference，但不得修改 canonical 的判斷結果
6. `derived` 文件             → 禁止作為 session_start 的唯一判斷依據

---

## Memory Source Authority

| memory source | authority | promotion policy |
|---------------|-----------|-----------------|
| `02_project_facts.md` | canonical | 直接 promote |
| `03_decisions.md` | canonical | 直接 promote |
| `04_patterns.md` | reference | 評估後 promote |
| reviewer handoff summary | derived | cache only，不 promote 為 truth |
| framework artifact cache | derived | cache only，不 promote 為 truth |
| external repo aliases | reference | 評估後 promote，不覆蓋 canonical |

---

## Loading Condition Summary

| task_level | always | on-demand | incremental | never |
|------------|--------|-----------|-------------|-------|
| L0 | ✅ | ❌ | ✅ candidates only | ❌ |
| L1 | ✅ | ✅ | ✅ candidates only | ❌ |
| L2 | ✅ | ✅ | ✅ candidates only | ❌ |
| any | human-only 永遠 ❌ | | | |

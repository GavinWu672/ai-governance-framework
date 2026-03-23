# L0 Payload Baseline

> 產出日期: 2026-03-23
> 樣本數: 1 筆（Hearth repo）
> Token 計算方式: estimate
> Tool: `governance_tools/payload_audit_logger.py`

## Token 分布

| 類別 | Token 數 | 占比 |
|------|---------|------|
| Governance 文件（always-load） | ~3,954 | 20% |
| Domain Contracts | ~3,360 | 17% |
| Memory 檔案 | — | — |
| Rendered output overhead | ~11,106 | 57% |
| **Session 總計（combined estimate）** | **~19,330** | 100% |

## 對比 L1（無 contract）：24,743 tokens

L0 比 L1 少約 22%，主要差異來自 on-demand 文件未載入（ARCHITECTURE.md、TESTING.md 等）。

## Top 3 Token 黑洞

| 排名 | 欄位 | Token（此 session） | % of total |
|------|------|-------------------|-----------|
| 🥇 1 | `pre_task_check` | ~3,954 | ~20% |
| 🥈 2 | `domain_contract` | ~3,360 | ~17% |
| 🥉 3 | rendered output overhead | ~11,106 | ~57% |

## 優化建議

- L0 的 `pre_task_check` 仍然執行完整的 pre-task 流程（建議 Step 5 後可精簡）
- `domain_contract` 在 L0 仍被載入 — 即使是 Hearth 自身的 contract
  - 若 L0 任務明確不涉及 domain，應可跳過 contract 載入（Step 5 的 upgrade_trigger 機制）
- Rendered output overhead（JSON/human 格式化）占 57% — 僅做 CI gate check 時建議只用 `--format human` + 丟棄 state/change_proposal 欄位

## Authority Filter 確認

| 文件 | L0 載入 | 符合預期 |
|------|--------|---------|
| SYSTEM_PROMPT.md | ✅ | ✅ |
| AGENT.md | ✅ | ✅ |
| PLAN.md | ✅ | ✅ |
| ARCHITECTURE.md | ❌ | ✅（on-demand，L0 不載） |
| REVIEW_CRITERIA.md | ❌ | ✅（human-only，永不） |
| HUMAN-OVERSIGHT.md | ❌ | ✅（human-only，永不） |

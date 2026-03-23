# L1 Payload Baseline

> 產出日期: 2026-03-23
> 樣本數: 2 筆（Hearth repo × 1 + Kernel-Driver-Contract × 1）
> Token 計算方式: estimate
> Tool: `governance_tools/payload_audit_logger.py`

## Token 分布

### Session A — L1，無 domain contract（Hearth repo）

| 類別 | Token 數 | 占比 |
|------|---------|------|
| Governance 文件（always + on-demand） | ~5,166 | 21% |
| Domain Contracts | ~3,360 | 14% |
| State（含 refactor rules proposal） | ~1,712 | 7% |
| Change Proposal | ~362 | 1% |
| Rendered output overhead | ~14,143 | 57% |
| **Session 總計** | **~24,743** | 100% |

### Session B — L1，含 domain contract（Kernel-Driver-Contract）

| 類別 | Token 數 | 占比 |
|------|---------|------|
| Governance 文件（always + on-demand） | ~14,035 | 23% |
| Domain Contracts（KDC，rich contract） | ~13,605 | 22% |
| State | ~393 | 1% |
| Validator preflight | ~252 | 0% |
| Rendered output overhead | ~32,338 | 53% |
| **Session 總計** | **~60,623** | 100% |

**關鍵發現：有 rich domain contract（KDC）的 L1 session 比無 contract 多 ~2.45×**

## Top 3 Token 黑洞（跨兩 sessions 平均）

| 排名 | 欄位 | 平均 Token | 最大值 | KDC session 占比 |
|------|------|-----------|--------|----------------|
| 🥇 1 | `pre_task_check` | ~10,794 | 14,035 | ~23% |
| 🥈 2 | `domain_contract` | ~10,190 | 13,605 | ~22% |
| 🥉 3 | `state` | ~546 | 1,712 | ~1% |

**Runner-up：** `change_proposal` (~290) · `validator_preflight` (~252) · `rule_pack_suggestions` (~258)

## Domain Adapter Summary 現況確認

**結論：目前全是 full contract**

KDC 的 `domain_contract` 欄位包含完整 rule documents、validator specs、AI-behaviour overrides、document previews。
沒有任何 summary / adapter 層。這是 Step 4 最大的優化機會。

## 優化建議

1. **`domain_contract` 文件內容懶加載** — 目前所有 documents 無條件 inline，與 impact files 無關
2. **`pre_task_check` architecture impact 上限** — KDC session 的 `architecture_impact_preview` 過長
3. **`domain adapter summary`** — 建立 contract 摘要層（Step 4 核心工作），預估可節省 KDC session 的 ~22% token

## Authority Filter 確認（L1）

| 文件 | L1 載入 | 符合預期 |
|------|--------|---------|
| SYSTEM_PROMPT.md | ✅ | ✅ |
| AGENT.md | ✅ | ✅ |
| PLAN.md | ✅ | ✅ |
| ARCHITECTURE.md | ✅ | ✅（on-demand，L1 載） |
| TESTING.md | ✅ | ✅（on-demand，L1 載） |
| REVIEW_CRITERIA.md | ❌ | ✅（human-only，永不） |
| HUMAN-OVERSIGHT.md | ❌ | ✅（human-only，永不） |

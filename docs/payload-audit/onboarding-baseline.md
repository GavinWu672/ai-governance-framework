# Onboarding Payload Baseline

> 產出日期: 2026-03-23
> 樣本數: 2 筆（Kernel-Driver-Contract — ok × 1 + fail × 1）
> Token 計算方式: estimate
> Tool: `governance_tools/payload_audit_logger.py`

## Token 分布

### Session A — Onboarding ok=True（KDC）

| 類別 | Token 數 | 占比 |
|------|---------|------|
| Governance 文件 + Domain Contract | ~27,640 | ~46% |
| Rendered output overhead | ~32,983 | ~54% |
| **Session 總計** | **~60,623** | 100% |

### Session B — Onboarding ok=False（KDC，unknown rule pack: `onboarding`）

| 類別 | Token 數 | 占比 |
|------|---------|------|
| Governance 文件 + Domain Contract | ~27,215 | ~45% |
| Rendered output overhead | ~32,983 | ~55% |
| **Session 總計** | **~60,198** | 100% |

**差異：ok=False session 比 ok=True 少 ~425 tokens**（error 路徑提前終止部分 proposal 計算）

## Governance Health（Onboarding Sessions）

| 指標 | 值 |
|------|-----|
| ok=False sessions | 1 / 2（50%） |
| 失敗原因 | `Unknown rule packs: ['onboarding']` |
| 警告 | PLAN.md is STALE（KDC repo 的 PLAN.md 未更新） |
| 建議 | 對 KDC 跑 `adopt_governance.py --refresh` |

## Top 3 Token 黑洞（onboarding sessions）

與 L1 KDC session 相同（因為 onboarding session 的 payload 結構與 L1 domain session 相同）：

| 排名 | 欄位 | Token | 占比 |
|------|------|-------|------|
| 🥇 1 | `pre_task_check`（含 domain contract validation） | ~14,035 | ~23% |
| 🥈 2 | `domain_contract`（KDC full contract inline） | ~13,605 | ~22% |
| 🥉 3 | rendered output overhead | ~32,338 | ~53% |

## 關鍵發現

1. **Onboarding session 的 token 分布與 L1 domain session 相同** — 說明 adopt_governance.py 跑完後的 session_start 沒有特殊優化
2. **`onboarding` 不是有效 rule pack 名稱** — adopt_governance.py 的預設 rule 設定需修正，不應傳入 `onboarding` 作為 rule pack
3. **KDC PLAN.md 需要更新** — 對外部 repo 的 adopt 後應自動提示 PLAN.md 過期

## 優化建議

1. 修正 `adopt_governance.py` 的預設 rule pack 設定（移除 `onboarding` 這個無效名稱）
2. Onboarding session 可以用 L0 payload（只需確認 authority/contract 存在，不需要完整 architecture analysis）
3. 建立 onboarding-specific short-circuit（Step 5 的 upgrade_trigger 可加入 `"task_type": "onboarding"` 案例）

## 執行命令（重現此 baseline）

```bash
# Session A（ok=True）
export GOVERNANCE_PAYLOAD_AUDIT=1
python governance_tools/adopt_governance.py --target /e/BackUp/Git_EE/Kernel-Driver-Contract --refresh
python runtime_hooks/core/session_start.py \
  --project-root /e/BackUp/Git_EE/Kernel-Driver-Contract \
  --risk medium --task-level L1 --task-type onboarding \
  --contract /e/BackUp/Git_EE/Kernel-Driver-Contract/contract.yaml

# Session B（ok=False，rule pack 錯誤）
python runtime_hooks/core/session_start.py \
  --project-root /e/BackUp/Git_EE/Kernel-Driver-Contract \
  --risk medium --task-level L1 --task-type onboarding \
  --rules "onboarding" \
  --contract /e/BackUp/Git_EE/Kernel-Driver-Contract/contract.yaml
```

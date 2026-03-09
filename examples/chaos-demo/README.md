# 💥 Chaos Demo — AI 架構破壞 vs 治理攔截

> **情境**: 你有一個三層架構的 Python 服務（API → Service → Repository）。
> 架構紅線是：**Repository 層不能包含業務邏輯，Service 層不能直接操作 HTTP**。
>
> **目標**: 展示 AI 在沒有治理文件時如何破壞架構，以及治理框架如何介入。
>
> **時間**: 約 10 分鐘閱讀

---

## 📂 專案結構（起始狀態）

```
chaos-demo/
├── src/
│   ├── api.py          ← HTTP 層（接收請求 → 呼叫 service）
│   ├── service.py      ← 業務邏輯層（驗證、計算、協調）
│   └── repository.py   ← 資料存取層（只做 DB 讀寫）
├── ARCHITECTURE.md     ← 架構紅線（有治理版才有）
├── PLAN.md             ← 當前計畫（有治理版才有）
└── memory/
    └── 01_active_task.md
```

---

## 🔴 第一幕：沒有治理（10 秒看懂問題）

### 情境

Repository 層目前只有純 DB 操作。你請 AI「優化一下查詢邏輯，加個快取」。

**你說**：
```
repository.py 查詢太慢了，幫我加個快取，順便如果查不到就從外部 API 抓
```

**AI 回覆（無治理）**：
```python
# repository.py  ← AI 修改後

import httpx
import functools

class UserRepository:
    def __init__(self, db, cache):
        self.db = db
        self.cache = cache

    def get_user(self, user_id: str):
        # 快取檢查
        if cached := self.cache.get(f"user:{user_id}"):
            return cached

        # DB 查詢
        user = self.db.query("SELECT * FROM users WHERE id = ?", user_id)

        # ← 問題：Repository 層開始呼叫外部 HTTP API
        if not user:
            response = httpx.get(f"https://legacy-api.internal/users/{user_id}")
            user = response.json()
            self.db.insert("users", user)  # 還順便寫入 DB

        self.cache.set(f"user:{user_id}", user)
        return user
```

**結果**：
```
❌ Repository 層現在包含：
   - HTTP client 邏輯（httpx.get）
   - 業務判斷（找不到才去抓）
   - 資料同步邏輯（抓到就寫入）

❌ 架構邊界徹底模糊

❌ 未來問題：
   - 測試 repository 必須 mock HTTP
   - Service 層不知道 repository 可能觸發外部呼叫
   - 當外部 API 掛掉，DB 查詢也會超時
```

**這次破壞沒有任何警告。** CI 通過（程式碼可以跑），git commit 成功，破壞悄悄進入 main branch。

---

## 🟢 第二幕：有治理（AI 被重新導向）

同樣的請求，但這次 AI 先讀了治理文件。

### ARCHITECTURE.md（架構紅線）

```markdown
## 架構分層規則（不可違反）

### Repository 層
- ✅ 允許：SQL 查詢、DB 讀寫、連線管理
- ❌ 禁止：HTTP 呼叫、業務邏輯、快取策略

### Service 層
- ✅ 允許：業務邏輯、協調多個 repository、呼叫外部服務
- ❌ 禁止：直接操作 HTTP request/response 物件

### 違規後果
違反分層規則的代碼必須在 PR review 中被擋下。
```

**AI 回覆（有治理）**：

```
[Governance Contract]
LANG    = Python
LEVEL   = L2
SCOPE   = refactor
PLAN    = PLAN.md
LOADED  = SYSTEM_PROMPT, HUMAN-OVERSIGHT, ARCHITECTURE
CONTEXT = chaos-demo — UserService refactor; NOT: HTTP layer changes
PRESSURE = SAFE (23/200)

---

我讀到了 ARCHITECTURE.md 的架構分層規則。

你的需求「加快取 + 從外部 API fallback」需要拆成兩部分：

1. **快取** → 可以在 Repository 層加（這是 DB 存取優化，合法）
2. **外部 API fallback** → 這是業務邏輯，**必須在 Service 層處理**

根據架構紅線，Repository 不能包含 HTTP 呼叫。

建議方案：

**repository.py（只加快取）**
\`\`\`python
def get_user(self, user_id: str):
    if cached := self.cache.get(f"user:{user_id}"):
        return cached
    user = self.db.query("SELECT * FROM users WHERE id = ?", user_id)
    if user:
        self.cache.set(f"user:{user_id}", user)
    return user  # ← 找不到時回傳 None，不做業務決策
\`\`\`

**service.py（負責 fallback 邏輯）**
\`\`\`python
def get_user(self, user_id: str):
    user = self.user_repo.get_user(user_id)
    if not user:
        # Service 層才呼叫外部 API
        user = self.legacy_client.fetch_user(user_id)
        if user:
            self.user_repo.save_user(user)
    return user
\`\`\`

這樣架構邊界保持清晰，要繼續嗎？
```

**結果**：
```
✅ Repository 層只做 DB + 快取（合法）
✅ Service 層負責 fallback 業務邏輯（合法）
✅ 架構邊界完整保留
✅ AI 主動說明為何這樣拆，而不是直接改錯
```

---

## 🔵 第三幕：CI 防線（技術層備援）

即使 AI 沒有讀到 ARCHITECTURE.md，CI 仍然有一道防線。

### contract_validator.py

如果 AI 回覆裡沒有合規的 `[Governance Contract]` 區塊（表示 AI 沒有完成初始化）：

```bash
$ echo "<AI 直接修改 repository.py 的回覆>" | \
  python governance_tools/contract_validator.py

🚨 [Governance Contract] 區塊不存在
   AI 回覆不合規 — 請要求 AI 重新初始化並輸出合規區塊

exit code: 2
```

### verify_phase_gates.sh

推送前自動驗證專案狀態：

```bash
$ bash scripts/verify_phase_gates.sh

╔══════════════════════════════════════════╗
║   Phase Gate Verification                ║
╚══════════════════════════════════════════╝

── Gate 1 / 單元測試 ──────────────────────────
  ✅ pytest 通過

── Gate 2 / PLAN.md 新鮮度 ────────────────────
  ❌ PLAN.md CRITICAL (15d) — 請更新後再宣告完成

══════════════════════════════════════════
  結果: 1/4 Gates 通過
  🚨 1 項未通過 — 請修復後再宣告 Phase 完成

exit code: 1
```

PLAN.md 沒有更新（表示架構修改沒有反映在計畫中）→ CI 擋住 push。

---

## 📊 Before / After 總結

| 面向 | 沒有治理 | 有治理 |
|------|---------|-------|
| AI 行為 | 直接修改，不問 | 先讀架構規範，再提方案 |
| 架構邊界 | 被悄悄破壞 | 保持清晰 |
| 問題發現時間 | Code review 或 production 才發現 | 對話階段就攔截 |
| CI | 通過（功能沒壞） | 驗證 PLAN.md 更新、tests pass |
| 技術債 | 每次 AI 協作都在累積 | 有文件化的邊界限制累積速度 |

---

## ⚠️ 誠實說明

**AI 遵守 ARCHITECTURE.md 是指導性的，不是技術強制**。

在真實場景中，AI 仍然可能在長對話中「遺忘」架構規則，或在沒讀到文件的情況下直接修改。
`contract_validator.py` 可以驗證 AI 是否完成初始化，但不能保證每一行代碼都符合架構約束。

這是目前框架的已知限制。詳見 [LIMITATIONS.md](../../docs/LIMITATIONS.md)。

---

## 🚀 自己跑一遍

```bash
# 1. 把治理文件部署到你的專案
bash deploy_to_memory.sh --target /path/to/your/project

# 2. 在 Claude Code 或 Cursor 中載入 ARCHITECTURE.md
# 直接把路徑告訴 AI：
# 「請讀取 ARCHITECTURE.md 後再開始工作」

# 3. 嘗試讓 AI 做一個會越過架構邊界的修改
# 觀察它是否主動提出分層方案，還是直接改錯

# 4. 驗證 CI
bash scripts/verify_phase_gates.sh
```

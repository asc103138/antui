# 專案規範與工作指引 (AGENTS.md)

## 專案基本資訊
- **專案名稱**：antui
- **主要用途**：工具庫 / 套件開發
- **Obsidian 對應筆記**：`D:\opencode\我的筆記\antui\專案工作流程.md`（注意：本機路徑勿 commit 到公開儲存庫）

## 開工流程
1. 讀取 `AGENTS.md`、`ANTIGRAVITY.md`、`handoff.md`。
2. 讀取專案筆記或相關進度記錄。
3. 執行 `git status` 與檢視近期 commit。
4. 回報當前狀態與建議下一步。
5. 不自動執行 pull / commit / push。

## 收工流程
1. 檢查敏感資料（API Key、Token、個資等），嚴禁寫入。
2. **執行成品一票否決檢查**：執行 `python scripts/audit_gatekeeper.py` 與 Playwright 實體驗收，未過一律砍掉重練。
3. 更新專案進度至 `handoff.md`。
4. 規則若有調整才更新 `AGENTS.md`。
5. 檢查 `git status` 與 `git diff`。
6. 只 stage 本次相關檔案（嚴禁無差別 `git add .`）。
7. 自動執行 commit 並同步推送至線上 Git 遠端儲存庫（git push）。
8. 回報同步結果。

## 安全與 Git 規範
- **嚴禁硬編碼機密**：API 金鑰、個人憑證或 Token 切勿寫入程式碼或 Markdown 文件中。
- **Commit 紀律**：保持每次 commit 意圖單一清晰，提交前仔細審查 diff。

## 設計工程全套工藝標準 (Emil Kowalski Design Engineering Baseline)
**【核心立論】本專案將 Emil Kowalski 的「全套設計工程工藝（Design Engineering）」設定為本專案的「起步底線（Minimum Bar / Baseline）」。這絕非妥協折衷的低標設計，而是將業界頂級的品味、物理真實感與微小細節，視為專案不可退讓的及格門檻：**

### 1. 核心哲學：無形細節的疊加力量 (Unseen Details Compound)
- **美感即槓桿 (Beauty is Leverage)**：優秀的預設值與流體動態是產品最深的護城河。
- **無形細節疊加**：千百個使用者未曾自覺的細微正確（如 Paul Graham 所言），匯聚成驚艷的產品靈魂。
- **品味是刻意訓練的直覺**：不容忍粗糙過渡，持續逆向工程優秀互動。

### 2. 審查報告格式（強制要求）
所有動效審查必須使用 Markdown 表格，欄位為 `| Before | After | Why |`，一項一列，明確指陳問題與物理修正原理。

### 3. 動畫決策框架（Frequency Framework）
- **高頻操作（每日百次以上，如快捷鍵、搜尋框開關、命令列）**：**絕對不加動態**，必須瞬開瞬關，避免造成延遲感。
- **中頻操作（列表導航、標籤切換）**：大幅簡化或微縮時長（<= 150ms）。
- **低頻操作（彈窗 Modal、抽屜 Drawer、通知 Toast）**：允許標準動效，但嚴格控制在 180ms ~ 300ms 內。

### 4. 感知效能 (Perceived Performance)
- **心理時鐘 > 客觀時鐘**：快速旋轉的 Spinner 比慢速更讓人覺得載入迅速；180ms 的 Select 比 400ms 俐落數倍。
- **連鎖工具列跳過延遲**：Tooltip 連續觸發時跳過延遲與進場動畫，營造極速感。

### 5. 動效曲線與物理真實感 (Physics & Easing)
- **禁止使用 `ease-in` 於 UI 進場**：進場元素必須用強烈自訂曲線的 `ease-out`（如 `cubic-bezier(0.23, 1, 0.32, 1)`），提供即時回饋感。
- **嚴禁從 `scale(0)` 憑空出現**：真實世界沒有零體積物體，入場起點至少為 `scale(0.95)` 搭配 `opacity: 0`。
- **嚴禁無差別 `transition: all`**：必須精確指定過渡屬性（如 `transform, opacity, box-shadow`），避免引發不必要的 layout/repaint 效能消耗。
- **彈簧物理與中斷性 (Interruptibility)**：支援手勢互動保留速度動量，中斷時不重設為零。
- **彈出層（Popover/Dropdown）具備 Origin-Aware**：必須依賴觸發來源縮放，而非全部機械式置中。

### 6. 微互動與點擊回饋 (Micro-interactions)
- **按鈕與可點擊元素必備 `:active`**：按下時必須具備 `transform: scale(0.97)` 微縮觸感，證明介面即時響應用戶動作。

## 成品一票否決檢查機制 (Zero-Tolerance Gatekeeper Protocol)
**【核心鐵律】任何交付之成品（網頁、組件、教材、文件、工作流）必須通過五重嚴格檢查。只要踩中任一項「一票否決紅線（Fatal Red Flags）」，判定為 FAIL，立即「砍掉重練（Hard Reset）」！嚴禁修補苟且、嚴禁帶病過關！**

### 1. 驗收五重鐵律（一票否決紅線 Fatal Red Flags）
1. **動效工藝物理紅線**：
   - ❌ 出現無差別 `transition: all`（一律砍掉重練）。
   - ❌ 出現 `scale(0)` 憑空生成（一律砍掉重練，入場起點最低 `scale(0.95)` 搭配 `opacity: 0`）。
   - ❌ UI 進場使用 `ease-in` 或線性 `linear`（一律砍掉重練，必須使用強烈自訂曲線 `ease-out`）。
   - ❌ 可點擊按鈕/標籤缺少 `:active` 物理微縮（`scale(0.96~0.98)`）（一律砍掉重練）。
   - ❌ 高頻操作（快捷鍵、搜尋、開關）加入多餘動畫延遲（一律砍掉重練，必須瞬開瞬關）。
2. **多情境可視性與空間層級紅線**：
   - ❌ 日間/夜間任一模式下元件被隱藏、不可見或對比度破裂（例如日間被 `display: none` 或 `z-index` 負值遮蔽）（一律砍掉重練）。
   - ❌ 背景動態層攔截使用者點擊（缺少 `pointer-events: none`）（一律砍掉重練）。
3. **行動端原生感紅線**：
   - ❌ 缺少 `-webkit-tap-highlight-color: transparent` 造成點擊藍灰閃爍（一律砍掉重練）。
   - ❌ 視窗尺寸未適配 `100dvh` / `100svh` 而死板使用 `100vh` 造成手機瀏覽器破版（一律砍掉重練）。
   - ❌ 表單輸入框字體小於 16px 造成 iOS Safari 強迫畫面縮放（一律砍掉重練）。
   - ❌ 按鈕/控制項未鎖定 `user-select: none` 造成長按誤選字（一律砍掉重練）。
4. **實體渲染檢驗紅線**：
   - ❌ **嚴禁「腦補通過」**：必須實際以終端、Playwright 瀏覽器或實機檢視渲染畫面（DOM 計算屬性、截圖），無客觀證據直接否決。
   - ❌ 瀏覽器控制台或執行期存在未處理錯誤（Console Error / Unhandled Exception）（一律砍掉重練）。
5. **資安與 Commit 紀律紅線**：
   - ❌ 硬編碼任何 API Key、Token 或機敏本機路徑（一律砍掉重練）。
   - ❌ 無差別 `git add .`（一律拒絕）。

### 2. 裁決判定標準與處置流程
- **判定 FAIL（違規 ≥ 1 項）**：
  1. 拒絕合併、拒絕 Commit、拒絕交付。
  2. 立即宣告觸發「砍掉重練（Hard Reset）」機制。
  3. 丟棄瑕疵實作，依規範重新乾淨實作，直到 100% 綠燈通過。
- **判定 PASS（違規 = 0 項）**：
  1. 產出 `| Before | After | Why |` 動效審查報告或檢驗合格清單。
  2. 方可進入收工流程、Stage 相關檔案、Commit 並推送。

### 3. 自動化巡檢工具
每次交付前強制執行自動化檢查：
```bash
python scripts/audit_gatekeeper.py
```
（回傳 Exit Code 1 即代表違規，觸發砍掉重練；Exit Code 0 代表合格）




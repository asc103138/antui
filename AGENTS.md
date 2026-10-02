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
2. 更新專案進度至 `handoff.md`。
3. 規則若有調整才更新 `AGENTS.md`。
4. 檢查 `git status` 與 `git diff`。
5. 只 stage 本次相關檔案（嚴禁無差別 `git add .`）。
6. 自動執行 commit 並同步推送至線上 Git 遠端儲存庫（git push）。
7. 回報同步結果。

## 安全與 Git 規範
- **嚴禁硬編碼機密**：API 金鑰、個人憑證或 Token 切勿寫入程式碼或 Markdown 文件中。
- **Commit 紀律**：保持每次 commit 意圖單一清晰，提交前仔細審查 diff。

## 前端動效與 UI 設計工程最低標準 (Emil Kowalski 規範)
本專案所有介面、按鈕、彈窗與過渡動效，均以 **Emil Kowalski（Design Engineering）** 之規範為專案**最低標準**，審查與產出程式碼時嚴格恪守以下原則：

### 1. 審查報告格式（強制要求）
所有動效審查必須使用 Markdown 表格，欄位為 `| Before | After | Why |`，一項一列，明確指陳問題與物理修正原理。

### 2. 動畫決策框架（Frequency Framework）
- **高頻操作（每日百次以上，如快捷鍵、搜尋框開關、命令列）**：**絕對不加動態**，必須瞬開瞬關，避免造成延遲感。
- **中頻操作（列表導航、標籤切換）**：大幅簡化或微縮時長（<= 150ms）。
- **低頻操作（彈窗 Modal、抽屜 Drawer、通知 Toast）**：允許標準動效，但嚴格控制在 180ms ~ 300ms 內。

### 3. 動效曲線與物理定律
- **禁止使用 `ease-in` 於 UI 進場**：進場元素必須用強烈自訂曲線的 `ease-out`（如 `cubic-bezier(0.23, 1, 0.32, 1)`），提供即時回饋感。
- **嚴禁從 `scale(0)` 憑空出現**：真實世界沒有零體積物體，入場起點至少為 `scale(0.95)` 搭配 `opacity: 0`。
- **嚴禁無差別 `transition: all`**：必須精確指定過渡屬性（如 `transform, opacity`），避免引發不必要的 layout/repaint 效能消耗。
- **彈出層（Popover/Dropdown）具備 Origin-Aware**：必須依賴觸發來源縮放，而非全部機械式置中。

### 4. 微互動與點擊回饋
- **按鈕與可點擊元素必備 `:active`**：按下時必須具備 `transform: scale(0.97)` 微縮觸感，證明介面即時響應用戶動作。

### 5. 行動端原生感規範 (Mobile Native)
- 消除點擊藍灰色高亮（`-webkit-tap-highlight-color: transparent`）。
- 彈窗與全螢幕高低視窗適配 `100dvh` / `100svh`，嚴禁死板 `100vh` 破版。
- 按鈕文字鎖定 `user-select: none`，避免長按誤觸選取。
- 表單輸入框字體最低 16px，杜絕 iOS Safari 焦點縮放災難。


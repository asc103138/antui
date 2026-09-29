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
6. 使用者確認後再執行 commit 與 push。
7. 回報同步結果。

## 安全與 Git 規範
- **嚴禁硬編碼機密**：API 金鑰、個人憑證或 Token 切勿寫入程式碼或 Markdown 文件中。
- **Commit 紀律**：保持每次 commit 意圖單一清晰，提交前仔細審查 diff。

---
name: antigravity-env-setup
description: 開發環境建置——Git、GitHub CLI、Node.js、uv 等工具之先偵測再安裝與驗證。說「建置環境」「安裝開發環境」「環境建置」時載入。
---

# 開發環境建置（AntiGravity 版）

## 核心原則
1. **先偵測再安裝**：每個工具先執行版本查詢，已存在則跳過，避免重複安裝。
2. **每步都要驗證**：安裝完成後務必印出版本號確認可用。
3. **PowerShell 規範**：Windows 執行環境使用 `;` 分隔指令，避免使用 `&&` 或不必要的錯誤重導向（`2>&1`）。

---

## 依序檢查與安裝

### 1. Git
- **檢查**：
  ```powershell
  git --version
  ```
- **安裝**（若未安裝）：
  ```powershell
  winget install --id Git.Git -e --source winget
  ```

### 2. GitHub CLI (gh)
- **檢查**：
  ```powershell
  gh --version
  ```
- **安裝**（若未安裝）：
  ```powershell
  winget install --id GitHub.cli -e --source winget
  ```

### 3. Node.js (LTS)
- **檢查**：
  ```powershell
  node -v; npm -v
  ```
- **安裝**（若未安裝）：
  ```powershell
  winget install --id OpenJS.NodeJS.LTS -e --source winget
  ```

### 4. uv (Python 工具與虛擬環境管理)
- **檢查**：
  ```powershell
  uv --version
  ```
- **安裝**（若未安裝）：
  ```powershell
  winget install --id astral-sh.uv -e --source winget
  ```
  *備案（若 WinGet 被權限限制）：*
  ```powershell
  powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
  ```

---

## 總體驗證指令
```powershell
git --version; gh --version; node -v; npm -v; uv --version
```
全部正常輸出版號即完成環境建置。

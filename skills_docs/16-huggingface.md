---
name: antigravity-huggingface
description: 掛接 Hugging Face 官方生態（MCP 伺服器、hf CLI、Agent Skills 與模型/資料集/Spaces 工作流）。說「Hugging Face」「HF」「huggingface」「下載模型」「找資料集」「搜尋Spaces」「掛接HF」「查論文」時載入。
---

# Hugging Face 全域工作流指引（AntiGravity 版）

整合 Hugging Face 官方生態，包含 **MCP 伺服器**、**`hf` CLI**、**Agent Skills** 以及 **Hub 資源（Models / Datasets / Spaces / Papers）** 互動工作流。

---

## 🔴 隱私與資安紅線（最高優先原則）

1. **嚴禁外洩學生個資**：
   - 絕不可將未去識別化或含有未成年學生姓名、座號、成績、照片、錄音之資料上傳至任何公開或私有之 Hugging Face Datasets 或 Spaces。
2. **嚴禁洩漏 Access Token**：
   - Hugging Face Token（`hf_xxxx`）嚴禁硬編碼（hardcode）在程式碼或 commit 到任何 Git 儲存庫中。
   - 一律透過本機環境變數（`$env:HF_TOKEN`）或 `hf auth login` 本機憑證管理。
3. **授權條款遵循**：
   - 下載或微調模型前，請確認該模型或資料集的授權條款（如 Apache-2.0, MIT, Llama Community License 等），確保符合教育或開發用途。

---

## 一、認證設定（Authentication）

### 1. 取得 Access Token
1. 前往 [Hugging Face Settings > Tokens](https://huggingface.co/settings/tokens)。
2. 建立新 Token（一般查詢與下載選取 `Read` 權限；需上傳或建立 Space 則選取 `Write`）。

### 2. 本機憑證設定
- **方式 A：使用 CLI 登入（推薦，寫入本機安全憑證）**
  ```powershell
  hf auth login
  ```
- **方式 B：設定 PowerShell 環境變數**
  ```powershell
  $env:HF_TOKEN = "hf_你的Token"
  ```

---

## 二、Hugging Face 官方 MCP 伺服器

已全域註冊於 `~/.gemini/config/mcp_config.json`：
```json
"huggingface": {
  "serverUrl": "https://huggingface.co/mcp"
}
```

### 自然語言使用方式
AI Agent 可直接透過 MCP 自然語言對話使用 Hub 資源：
- **模型搜尋**：「搜尋 Hugging Face 上適合繁體中文微調的小型 LLM（如 Qwen 2.5 或 Llama 3）」
- **資料集探索**：「尋找適合台灣國小語文或繁體中文常識問答的 Dataset」
- **Space 工具調用**：「尋找能夠將音訊轉逐字稿的 Gradio Space，並展示連結與用法」
- **研究論文**：「查閱近期關於 Agentic Workflow 或 reasoning models 的 Daily Papers」

---

## 三、本機 `hf` CLI 核心操作指南

系統已透過 `uv tool` 全域安裝官方最新 `hf` CLI（v2.0+）。

### 1. 模型（Models）與檔案
```powershell
# 搜尋模型
hf models list --search "qwen traditional chinese"

# 查看模型卡與資訊
hf models info "Qwen/Qwen2.5-7B-Instruct"

# 下載模型或特定權重檔案
hf download "Qwen/Qwen2.5-0.5B-Instruct"
hf download "meta-llama/Llama-3.2-1B-Instruct" config.json
```

### 2. 資料集（Datasets）
```powershell
# 搜尋公開資料集
hf datasets list --search "taiwanese"

# 查看資料集檔案結構
hf datasets list "swivid/calm"
```

### 3. Spaces 與展示應用
```powershell
# 搜尋 Space
hf spaces list --search "whisper"

# 檢視 Space 狀態與日誌
hf spaces info "username/space-name"
hf spaces logs "username/space-name"
```

### 4. 本機快取清理（節省硬碟空間）
```powershell
# 掃描本地 HF 快取佔用情況
hf cache scan

# 刪除指定或無用的快取
hf cache delete
```

---

## 四、Agent Skills 技能庫連動

官方 Agent Skills 已安裝至系統中，可隨選呼叫：

| 技能名稱 | 用途與情境 |
| :--- | :--- |
| `hf-cli` | 精通所有 `hf` 終端指令（模型、資料集、空間、Jobs、Sandbox） |
| `huggingface-datasets` | 透過 Dataset Viewer API 檢視分頁、篩選並取得 Parquet 連結 |
| `huggingface-gradio` | 快速建置 Python Gradio Web 介面與互動展示 |
| `huggingface-best` | 依據評測榜單與基準測試，為特定任務推薦最佳模型 |
| `huggingface-papers` | 檢索與結構化閱讀 Hugging Face 每日精選論文（Daily Papers） |
| `huggingface-spaces` | 建立、部署與設定 Spaces（包含 Docker、ZeroGPU 與環境變數） |
| `huggingface-local-models` | 評估本機規格，挑選合適的 GGUF / llama.cpp 本地離線模型 |

---

## 五、進階磁碟掛載（hf-mount）

若需要「不下載、零等待、隨選即讀」大型模型或儲存庫：
- 官方專案：[huggingface/hf-mount](https://github.com/huggingface/hf-mount)
- 透過 FUSE / NFS 技術將 Hub Repos / Storage Buckets 掛載為虛擬本機磁碟，適合直接串接 Python / pandas 讀取。

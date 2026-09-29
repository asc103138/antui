---
name: antigravity-file-toolkit
description: 安裝 agent 的內部工具包三合一——A 文件處理（Word/Excel/PPT/PDF/圖片/QR/轉 Markdown 的 Python 標配 10 套件）、B 影音工具（yt-dlp／FFmpeg／deno）、C 語音（Edge-TTS 讓 agent 開口說話）。說「裝內部工具包」「裝教學檔案處理工具包」「裝 Python 檔案工具」「裝 yt-dlp」「裝影音下載工具」「讓 agent 會說話」「裝 Edge-TTS」「裝語音」時載入。
---

# 內部工具包 三合一（文件／影音／語音）

## 核心規則（防呆守則）
1. **禁止全域 pip**：A 段一律裝進專案的 `.venv`，C 段使用 `uv tool install`（獨立環境），不污染系統 Python。
2. **禁止逐項上網研究**：套件版本解析交給 `uv`，不要逐一開網頁查詢。
3. **三段各自獨立**：A（文件）、B（影音）、C（語音）彼此獨立，任一段失敗不影響其他兩段。

---

## 🟢 標配 A：文件處理（Python 10 套件）

### 涵蓋套件
- `python-docx`（Word 生成與讀寫）
- `openpyxl`（Excel 試算表處理）
- `python-pptx`（PowerPoint 簡報生成）
- `pypdf`（PDF 合併／拆分／浮水印）
- `PyMuPDF`（PDF 文字抽取／轉圖片）
- `reportlab`（生成 PDF 與浮水印）
- `Pillow`（圖片裁切／去白邊／合成）
- `matplotlib`（統計圖表繪製）
- `qrcode[pil]`（QR Code 產生）
- `markitdown[pdf,docx,pptx,xlsx]`（多格式文件轉 Markdown）

### 安裝步驟
1. 取得工具包：
   ```bash
   git clone https://github.com/mathruffian-dot/ai-agent-ep03.git
   cd ai-agent-ep03
   ```
   > ⚠️ 預設分支為 `master`，請勿指定 `-b main`。

2. 安裝虛擬環境與套件（Windows）：
   ```powershell
   powershell.exe -NoProfile -ExecutionPolicy Bypass -File ".\install_windows.ps1"
   ```
   *或手動執行：*
   ```powershell
   uv venv --python 3.12 .venv
   uv pip install --python .venv\Scripts\python.exe -r requirements-core.txt
   ```

3. 驗證：
   ```powershell
   .\.venv\Scripts\python.exe verify_core.py
   ```
   > 看到 `CORE_OK: 10/10` 且 exit code 為 `0` 即代表成功。

---

## 🔵 標配 B：影音工具（yt-dlp / FFmpeg / deno）

### 安裝步驟（Windows WinGet）
```powershell
winget install yt-dlp.yt-dlp Gyan.FFmpeg DenoLand.Deno
```

### 驗證
```powershell
yt-dlp --version
ffmpeg -version
deno --version
```

---

## 🟣 標配 C：語音合成（Edge-TTS）

### 安裝步驟
```powershell
uv tool install edge-tts
```

### 驗證與使用
```powershell
edge-tts --voice zh-TW-HsiaoChenNeural --text "內部工具包語音測試成功" --write-media test.mp3
```
常用台灣中文語音：
- `zh-TW-HsiaoChenNeural`（女聲）
- `zh-TW-YunJheNeural`（男聲）

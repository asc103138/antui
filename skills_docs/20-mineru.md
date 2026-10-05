---
name: antigravity-mineru
description: 使用 MinerU (v4.0+) 進行高精準度多模態 PDF 與文件結構化解析（支援圖文原位對齊、跨頁表格、LaTeX公式還原與 OCR 模式）。當使用者提到「MinerU」、「解析含圖PDF」、「考卷PDF轉檔」、「掃描版PDF轉Markdown」、「論文轉Markdown」或需要解決「PDF內圖片與文字排版錯位、表格公式辨識」時載入此技能。
---

# Antigravity MinerU 文件解析技能

## 🎯 技能定位與核心價值
MinerU（OpenDataLab 開源）為新一代專為 LLM 與 AI Agent 打造的深度學習多模態文件解析引擎。
相較於一般的傳統 PDF 工具（如 pypdf、pdfplumber、MarkItDown），MinerU 能徹底解決以下痛點：
1. **圖文錯位問題**：透過深度學習版面分析模型（Layout Analysis），將圖說與圖片切片原位插入在正文段落間，而非雜亂堆放於文末。
2. **複雜跨頁表格**：自動辨識並還原為乾淨的 Markdown / HTML 表格結構。
3. **數學公式還原**：行內公式（Inline）與獨立區塊公式（Block）精準轉譯為標準 LaTeX 語法。
4. **掃描件與圖中文字**：內建 OCR 模式，將插圖、照片與掃描內容中的印刷文字轉為可檢索、可編輯文字層。
5. **100% 本機端運算**：所有解析與模型推論均在使用者本機端完成，敏感考卷、公文與個資絕不上傳外部伺服器。

---

## 💻 安裝與環境配置

可透過 `uv` 快速將 MinerU 4.0 CLI 工具安裝至全域環境：

### 1. 全域 CLI 安裝（推薦）
```bash
# 全域安裝 MinerU 4.0 工具鏈
uv tool install mineru-kit

# 或安裝包含完整相依套件
uv tool install "mineru[full]"
```

### 2. 專案虛擬環境安裝（依需求）
```bash
uv pip install mineru
```

### 3. 模型權重下載
本地端首次執行解析時，系統會自動下載所需的視覺與版面模型權重至快取目錄（`~/.mineru/models`）。
若欲提前下載：
```bash
# 下載 basic 檔位模型（約數百 MB ~ 1GB，速度快且能滿足大部分考卷需求）
mineru-kit models download --tier basic

# 下載 standard 檔位模型（含進階多模態視覺模型）
mineru-kit models download --tier standard
```

---

## 🛠️ CLI 常用指令範例

系統安裝後提供 `mineru-kit` 與 `mineru` 指令：

### 1. 標準解析（將 PDF 轉為含圖 Markdown）
```bash
mineru-kit parse "考卷.pdf" -o "./output"
```
解析完成後會在 `./output/考卷/` 產生：
- `考卷.md`（內含圖文原位對齊、表格與 LaTeX 公式）
- `images/`（切片出的所有高解析度圖片與插圖）

### 2. 指定頁碼解析
```bash
mineru-kit parse "講義.pdf" -o "./output" -p "1-3,5"
```

### 3. 強制 OCR 模式（適用掃描件或大量文字在圖裡的考卷）
```bash
mineru-kit parse "掃描考卷.pdf" -o "./output" --ocr-mode ocr
```

### 4. 檔位模式（Tier）
```bash
mineru-kit parse "論文.pdf" -o "./output" --tier basic
```
- `flash`：極速文字解析（輕量）
- `basic`：版面分析 ＋ 基礎模型（平衡速度與精準度）
- `standard`：版面分析 ＋ VLM 視覺語言模型精準解析

---

## 🐍 Python 自動化腳本範例

除了 CLI 操作，可在 Python 腳本或 Agent 工作流中呼叫 MinerU 進行批次自動化解析：

```python
import os
import subprocess
from pathlib import Path

def parse_pdf_with_mineru(pdf_path: str, output_dir: str = "./output", tier: str = "basic", ocr: bool = False):
    """
    使用 MinerU 解析 PDF 為結構化 Markdown 與圖檔切片
    """
    pdf_path = Path(pdf_path).resolve()
    output_dir = Path(output_dir).resolve()
    output_dir.mkdir(parents=True, exist_ok=True)
    
    cmd = [
        "mineru-kit", "parse",
        str(pdf_path),
        "-o", str(output_dir),
        "--tier", tier
    ]
    if ocr:
        cmd.extend(["--ocr-mode", "ocr"])
        
    print(f"正在使用 MinerU 解析: {pdf_path.name}...")
    result = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8")
    
    if result.returncode == 0:
        doc_folder = output_dir / pdf_path.stem
        md_file = doc_folder / f"{pdf_path.stem}.md"
        print(f"解析成功！輸出目錄: {doc_folder}")
        print(f"Markdown 檔案: {md_file}")
        return doc_folder
    else:
        print(f"解析失敗: {result.stderr}")
        return None
```

---

## ⚡ 跨平台硬體加速配置 (`~/.mineru/config.yaml`)

- **Windows 環境**：
  - 若具備 NVIDIA GPU，可設定 `device-mode: cuda` 享受極速推論。
  - 若為一般文書筆電，預設使用 `device-mode: cpu` 即可順暢運作。
- **macOS Apple Silicon 環境**：
  - 支援 Metal (`device-mode: mps`) 硬體加速。
  - 自動符合 Unicode NFC 繁中檔名正規化標準。

# Antigravity MinerU 文件解析技能 (`antigravity-mineru`)

專為教育工作者、行政人員與 AI Agent 打造的高精準度多模態 PDF 與文件結構化解析工具包，以 **MinerU (v4.0+)** 深度學習引擎為核心，整合本機 PDF 萬用處理能力。

---

## 🌟 核心特色

1. **圖文原位精準對齊**：透過版面佈局分析模型（Layout Analysis），將圖說與切片插圖原位插入在相應正文段落間，不再散落文末。
2. **跨頁表格自動還原**：複雜段考成績表、公文表格自動轉為乾淨的標準 Markdown / HTML 表格結構。
3. **LaTeX 數理公式轉譯**：無論是行內公式還是獨立區塊公式，皆精確辨識轉譯為標準 LaTeX。
4. **雙模式 OCR 文字辨識**：支援圖中文字與掃描文件 OCR 解析，將純圖片轉為可編輯、可搜尋的文字層。
5. **100% 本機端零外洩運算**：所有模型推論均在使用者本機端完成，符合教育與行政機密保護原則。
6. **跨平台加速支援**：支援 Windows（NVIDIA CUDA / CPU）與 macOS（Apple Silicon MPS）硬體加速。

---

## 📁 專案結構

```
pdf技能/
├── scripts/
│   ├── parse_pdf.py          # 核心解析腳本（支援 CLI 參數與 Python 模組調用）
│   └── sync_git.py           # 專案多端與 GitHub 雙向同步工具
├── AGENTS.md                 # 專案規範與工作指引
├── ANTIGRAVITY.md            # 專案指引入口
├── handoff.md                # 專案交接與進度記錄
├── README.md                 # 專案介紹說明
├── SKILL.md                  # AntiGravity 技能定義
└── .gitignore                # Git 忽略設定
```

---

## 🚀 快速開始

### 1. 安裝環境需求
建議使用 `uv` 進行快速安裝：

```bash
# 全域安裝 MinerU 4.0 CLI 工具（推薦）
uv tool install mineru-kit

# 或安裝包含完整多模態依賴
uv tool install "mineru[full]"
```

### 2. 提前下載基礎模型（選用）
本地端首次解析時會自動下載模型至快取目錄（`~/.mineru/models`）。若欲提前預熱：
```bash
mineru-kit models download --tier basic
```

### 3. 命令列解析 PDF
可直接使用內建模組腳本或 `mineru-kit`：

```bash
# 使用本專案 Python 腳本解析
python scripts/parse_pdf.py "考卷.pdf" -o "./output" --tier basic

# 或直接調用 mineru-kit
mineru-kit parse "考卷.pdf" -o "./output"
```

解析完成後會在 `./output/考卷/` 輸出：
- `考卷.md`（含圖文對齊、表格與 LaTeX 公式之 Markdown 檔案）
- `images/`（切片出的所有高解析度圖片與插圖）

---

## 🐍 Python 模組調用範例

```python
from scripts.parse_pdf import parse_pdf_with_mineru

output_folder = parse_pdf_with_mineru(
    pdf_path="數學段考卷.pdf",
    output_dir="./output",
    tier="basic",
    ocr=True
)
print(f"解析產出目錄：{output_folder}")
```

---

## 🔗 相關連結與整合
- **全域技能路徑**：`~/.gemini/config/skills/20-mineru`
- **進階文件技能**：`~/.gemini/config/skills/14-advanced-docs`
- **GitHub 儲存庫**：[https://github.com/asc103138/antigravity-mineru](https://github.com/asc103138/antigravity-mineru)

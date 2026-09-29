---
name: antigravity-advanced-docs
description: 奕鈞老師進階文件處理 Skill——整合 Word (python-docx)、PDF 萬用處理 (黑白省墨列印 / 畫質壓縮 / 旋轉校正 / 拆分轉圖打包 / 頁碼浮水印 / pypdf / PyMuPDF / pdfplumber)、Excel (openpyxl / pandas) 與圖片 (Pillow) 自動化處理。支援按需隨選安裝、本機運算 100% 零資安外洩。說「進階文件處理」「進階文書工具」「處理 Word」「合併 PDF」「拆分 PDF」「分析 Excel」「段考成績」「批次圖片處理」「黑白省墨」「PDF壓縮」「旋轉PDF」「PDF加頁碼」「PDF加浮水印」「PDF轉圖片」時載入。
---

# AI Agent 進階文件處理 Skill（教學與行政自動化）

專為教育工作者、行政人員與 AI Agent 打造的進階本機文件處理自動化工具包，承接核心文件 Skill（07-file-toolkit）之能力，整合奕鈞老師「PDF 萬用工具」之核心處理邏輯，支援 Word 試卷排版、PDF 全功能編排擷取、黑白省墨列印轉換、Excel 巨量統計與圖片批次轉換。

---

## 核心守則與資安紅線

1. **100% 本機端運算（零資安外洩）**：處理段考試卷、學生個資、校務機密公文時，所有程式碼均在使用者本機環境執行，絕不將文件或資料上傳至第三方外部伺服器或雲端。
2. **智慧隨選載入（按需安裝）**：不強求一開始就安裝所有套件，AI Agent 應先分析任務需求（如只處理 PDF 則僅需 `pypdf`/`pymupdf`），再建議或執行安裝。
3. **隔離虛擬環境（防污染）**：嚴禁全域系統 `pip install`，一律使用專案目錄下的 `.venv` 或 `uv` 獨立管理。

---

## 工具分工表

| 工具套件 | 主要用途 | 適用情境 |
|---|---|---|
| `pypdf` | 批次合併、分割、旋轉、浮水印 | 多份 PDF 合成單檔、抽離指定頁碼、加蓋半透明浮水印、頁面旋轉校正 |
| `PyMuPDF` (`fitz`) | 高速渲染、轉圖、黑白省墨、檔案壓縮 | 一鍵轉高畫質黑白灰階（省墨列印）、PDF 轉高解析 PNG 圖片包、極速檔案瘦身 |
| `reportlab` | 產製高品質標準 PDF、向量頁碼 | 家長通知單、活動結業證書、自動依序編排標準頁碼（Page X of Y） |
| `pdfplumber` | PDF 表格與文字精準結構擷取 | 擷取各校段考考卷表格、公文內容文字結構分析 |
| `python-docx` | Word 生成、讀取與修改 | 備課講義、學習單排版、試卷自動生成、段落文字搜尋取代 |
| `openpyxl` | Excel 活頁簿讀寫與格式排版 | 建立多分頁活頁簿、設定單元格顏色、公式、框線 |
| `pandas` | 高速資料清洗與成績統計 | 段考全校大表排序、各班平均、PR 值與標準差計算 |
| `Pillow` | 圖片縮放、轉換與修飾 | 教材圖片批次縮圖、轉檔（PNG/JPG/WebP）、去背或裁切 |

---

## 環境配置與按需安裝指引

使用 `uv` 於專案內管理虛擬環境（快速、可靠）：

### 1. 建立虛擬環境（若尚未建立）
```powershell
uv venv --python 3.12 .venv
```

### 2. 隨選安裝指令（依任務挑選）

- **PDF 萬用處理任務（產製／合併／解析／轉圖／省墨／壓縮）**：
  ```powershell
  uv pip install --python .venv\Scripts\python.exe pypdf pymupdf pdfplumber reportlab
  ```
- **Word 試卷與講義處理任務**：
  ```powershell
  uv pip install --python .venv\Scripts\python.exe python-docx
  ```
- **Excel 成績處理與統計任務**：
  ```powershell
  uv pip install --python .venv\Scripts\python.exe openpyxl pandas
  ```
- **圖片批次處理任務**：
  ```powershell
  uv pip install --python .venv\Scripts\python.exe Pillow
  ```
- **一次安裝完整進階工具包**：
  ```powershell
  uv pip install --python .venv\Scripts\python.exe python-docx openpyxl pandas pypdf pymupdf pdfplumber reportlab Pillow
  ```

---

## 常用作業腳本範例

### 範例一：多份 PDF 批次合併與指定順序（pypdf）
```python
from pypdf import PdfMerger

def merge_pdfs(pdf_list, output_path):
    """將多份 PDF 依序整合成單一檔案"""
    merger = PdfMerger()
    for pdf in pdf_list:
        merger.append(pdf)
    merger.write(output_path)
    merger.close()
    print(f"成功合併 {len(pdf_list)} 個檔案至 {output_path}")
```

### 範例二：高畫質黑白灰階轉換（學校省墨列印神器，PyMuPDF）
```python
import fitz

def convert_to_grayscale_pdf(input_path, output_path, dpi=200):
    """一鍵將彩色講義、電子書轉換為高畫質黑白灰階版 PDF，保留細緻文字與圖形輪廓"""
    doc = fitz.open(input_path)
    out_doc = fitz.open()
    for page in doc:
        # 以灰階色彩空間渲染頁面
        pix = page.get_pixmap(colorspace=fitz.csGRAY, dpi=dpi)
        img_pdf = fitz.open("pdf", pix.tobytes("pdf"))
        out_doc.insert_pdf(img_pdf)
    out_doc.save(output_path, garbage=4, deflate=True)
    out_doc.close()
    doc.close()
    print(f"已完成黑白灰階轉換：{output_path}（省墨列印專用）")
```

### 範例三：單頁／批次多頁自由旋轉校正（修正倒置掃描文件，pypdf）
```python
from pypdf import PdfReader, PdfWriter

def rotate_pdf_pages(input_path, output_path, rotation_map='all', default_angle=90):
    """
    旋轉指定頁面角度（順時針 90, 180, 270 度）
    rotation_map: 'all' 代表整份旋轉；或傳入 dict，例如 {0: 90, 2: 180}
    """
    reader = PdfReader(input_path)
    writer = PdfWriter()
    for idx, page in enumerate(reader.pages):
        if rotation_map == 'all':
            page.rotate(default_angle)
        elif isinstance(rotation_map, dict) and idx in rotation_map:
            page.rotate(rotation_map[idx])
        writer.add_page(page)
    with open(output_path, "wb") as f:
        writer.write(f)
    print(f"頁面旋轉完成：{output_path}")
```

### 範例四：選定頁面獨立匯出 或 批次打包轉 PNG 圖片 ZIP（PyMuPDF）
```python
import os, zipfile
import fitz

def export_pdf_to_images_zip(input_path, zip_output_path, page_range=None, dpi=200):
    """將 PDF 指定頁面（或全部頁面）轉成高解析度 PNG 圖片並打包成 ZIP"""
    doc = fitz.open(input_path)
    pages = page_range if page_range else range(len(doc))
    with zipfile.ZipFile(zip_output_path, 'w', compression=zipfile.ZIP_DEFLATED) as zipf:
        for pno in pages:
            page = doc[pno]
            pix = page.get_pixmap(dpi=dpi)
            img_bytes = pix.tobytes("png")
            zipf.writestr(f"page_{pno + 1:03d}.png", img_bytes)
    doc.close()
    print(f"已匯出 {len(pages)} 頁圖片並打包至 {zip_output_path}")
```

### 範例五：自訂畫質壓縮與檔案瘦身（PyMuPDF）
```python
import fitz

def compress_pdf(input_path, output_path):
    """清理未使用物件並啟用最高壓縮率，大幅縮減掃描檔體積"""
    doc = fitz.open(input_path)
    doc.save(output_path, garbage=4, deflate=True, clean=True)
    doc.close()
    orig_size = os.path.getsize(input_path) / (1024 * 1024)
    new_size = os.path.getsize(output_path) / (1024 * 1024)
    print(f"壓縮完成：{orig_size:.2f}MB -> {new_size:.2f}MB")
```

### 範例六：客製防外流浮水印與自動重編標準頁碼（ReportLab + pypdf）
```python
import io
from pypdf import PdfReader, PdfWriter
from reportlab.pdfgen import canvas

def add_watermark_and_page_numbers(input_path, output_path, watermark_text=None, add_page_num=True):
    """多份合併後自動重新編排標準頁碼（- X / Y -）與添加防外流半透明浮水印"""
    reader = PdfReader(input_path)
    writer = PdfWriter()
    total_pages = len(reader.pages)

    for idx, page in enumerate(reader.pages):
        width = float(page.mediabox.width)
        height = float(page.mediabox.height)
        packet = io.BytesIO()
        can = canvas.Canvas(packet, pagesize=(width, height))
        
        # 1. 客製半透明防外流浮水印
        if watermark_text:
            can.saveState()
            can.setFont("Helvetica-Bold", 38)
            can.setFillColorRGB(0.6, 0.6, 0.6, alpha=0.22)
            can.translate(width / 2, height / 2)
            can.rotate(45)
            can.drawCentredString(0, 0, watermark_text)
            can.restoreState()
        
        # 2. 自動重編標準頁碼（底部中央）
        if add_page_num:
            can.setFont("Helvetica", 10)
            can.setFillColorRGB(0.3, 0.3, 0.3)
            can.drawCentredString(width / 2, 25, f"- {idx + 1} / {total_pages} -")
        
        can.save()
        packet.seek(0)
        overlay_reader = PdfReader(packet)
        page.merge_page(overlay_reader.pages[0])
        writer.add_page(page)

    with open(output_path, "wb") as f:
        writer.write(f)
    print(f"已添加頁碼與浮水印：{output_path}")
```

### 範例七：成績大表批次統計與總分計算（pandas）
```python
import pandas as pd

def process_scores(excel_path, output_path):
    df = pd.read_excel(excel_path)
    subject_cols = ['國語', '數學', '英語', '自然', '社會']
    df['總分'] = df[subject_cols].sum(axis=1)
    df['平均'] = df[subject_cols].mean(axis=1).round(1)
    df['總分班排名'] = df['總分'].rank(ascending=False, method='min').astype(int)
    df.sort_values(by='總分班排名', inplace=True)
    df.to_excel(output_path, index=False)
    print(f"成績計算完成，已儲存至 {output_path}")
```

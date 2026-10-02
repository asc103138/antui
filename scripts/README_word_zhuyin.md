# Word (.docx) 國字自動注音標註與學習單排版工具

專為國小教學現場打造的 Word 國字自動注音標註工具，支援多音字上下文精準識別、雙列表格學習單排版與多音字複查清單。

---

## 🌟 核心特色

1. **台灣教育部標準讀音 ＆ 破音字/多音字上下文片語庫**：
   - 解決開源拼音庫繁體常見詞誤判問題（如：「長度」讀 ㄔㄤˊ、「長大」讀 ㄓㄤˇ、「音樂」讀 ㄩㄝˋ、「快樂」讀 ㄌㄜˋ、「銀行」讀 ㄏㄤˊ、「便宜」讀 ㄆㄧㄢˊ 等）。
   - 採用最長片語優先貪婪匹配（Max-Match），未命中詞彙自動調用通用注音庫。

2. **三種教學專用排版模式**：
   - **`table`（雙列表格模式，預設推薦）**：
     - 第一列為注音（字級 8.5~9pt、置中、緊湊行距）。
     - 第二列為國字（字級 16pt、標楷體粗體、置中）。
     - 自動依行切分，無邊框乾淨排版，適合低中年級閱讀學習單列印。
   - **`ruby`（Word 原生旁註模式）**：
     - 底層產出 `<w:ruby>` OpenXML 標籤，注音置於國字上方，保留原始文字段落流動。
   - **`inline`（行內夾註模式）**：
     - 將文字標註為 `國字(注音)` 格式，適合教案與純文字講義。

3. **防呆與多音字人工複查報告（Audit Report）**：
   - 處理完成後，終端機即時列出本次文件中所有被轉換的「多音字清單」，包含：**位置（段落）、目標字、選用讀音、命中上下文詞彙、所有候選讀音**，讓教師以 10 秒鐘快速人工巡檢。

---

## 🚀 使用方法

### 1. 單檔處理（預設雙列表格模式）
```bash
# 產出雙列表格注音 Word 檔（預設輸出至 test_sample_table_zhuyin.docx）
python scripts/word_zhuyin_annotator.py test_sample.docx

# 指定輸出檔案名稱
python scripts/word_zhuyin_annotator.py input.docx -o output_zhuyin.docx
```

### 2. 切換排版模式
```bash
# 模式 A：雙列表格模式 (小學列印學習單推薦)
python scripts/word_zhuyin_annotator.py input.docx --mode table

# 模式 B：Word 原生注音標記 (Ruby)
python scripts/word_zhuyin_annotator.py input.docx --mode ruby

# 模式 C：行中夾註模式 如「長(ㄓㄤˇ)大」
python scripts/word_zhuyin_annotator.py input.docx --mode inline
```

### 3. 整體資料夾批次處理
```bash
# 批次處理指定資料夾內的所有 .docx 檔案
python scripts/word_zhuyin_annotator.py --folder "D:/my_sheets/" --mode table
```

### 4. 自訂每行字數（表格模式）
```bash
# 預設每行 18 字，可依 A4 橫式或字體大小調整為 15 或 20 字
python scripts/word_zhuyin_annotator.py input.docx --line-chars 16
```

---

## 🛠️ 擴充多音字片語字典
若有校內特定生字或特殊詞彙需自訂讀音，可直接在 [`scripts/zhuyin_dict.py`](./zhuyin_dict.py) 的 `POLYPHONIC_PHRASES` 字典中新增詞彙即可。

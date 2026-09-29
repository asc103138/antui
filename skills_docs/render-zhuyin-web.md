---
name: render-zhuyin-web
description: Automatically annotate every eligible Han character in static or dynamic web pages or Word (.docx) exam papers with contextual Mandarin Zhuyin/Bopomofo, complete-coverage validation, inline text flow, blackboard vertical layout, and vocabulary exam generation (看注音寫國字/看國字寫注音). Use when building, editing, reviewing, or fixing HTML, CSS, JavaScript, React, Vue, Svelte pages or Word documents that must add 注音 to Chinese text, handle polyphonic words, or generate elementary school vocabulary exams. 當使用者提到「加注音」「網頁加注音」「注音標註」「國字注音」「注音排版」「黑板直式注音」「中文直式注音」「破音字」「多音字」「注音符號」「生字題」「國語考卷」「看注音寫國字」「看國字寫注音」「出考卷」「Word注音」「docx注音」「render-zhuyin-web」時載入。
---

# Render Zhuyin Web（全頁國字注音自動標註、排版與 Word 考卷生字題產出技能）

> 來源專案：[chunsheng612/render-zhuyin-web](https://github.com/chunsheng612/render-zhuyin-web.git)（由方方老師開發）  
> 直式注音聲調配置依循**經濟部標準檢驗局**數位排版規範與教育部審定讀音政策。

自動為網頁與 Word 考卷中每個合法的漢字加上上下文感知注音（Mandarin Zhuyin / Bopomofo），確保「發音解析、視覺排版、零缺漏嚴格驗證、生字評量試卷產出」一體化完成。

---

## 快速工具與資源（本 Skill 內建）

- **核心渲染引擎**：`assets/zhuyin-renderer/zhuyin-renderer.js`
- **標準注音樣式**：`assets/zhuyin-renderer/zhuyin-renderer.css`
- **CLI 命令行標註工具**：`scripts/annotate-cli.js`
- **Word 考卷生字題生成器**：`scripts/generate_zhuyin_exam.py`
- **互動式預覽 Demo 頁**：`examples/demo.html`
- **詳細參考規範**：
  - `references/full-page-integration.md`（完整 DOM / React / Vue / Svelte 整合）
  - `references/blackboard-zhuyin-logic.md`（黑板直式注音排版幾何與標檢局調號規則）
  - `references/pronunciation-policy.md`（教育部多音字讀音政策與破音字詞覆寫指引）

---

## 核心工作流程（必經七步驟）

1. **識別待標註文字**：找出頁面或題目中所有需加註音的純文字節點，排除標籤或加註 `data-no-zhuyin`。
2. **繁簡轉換標準化**：使用 `opencc-js`（tw -> cn）取得拼音字典標準形式（僅用於查表，原字完整保留於介面）。
3. **連續漢字段落上下文解析**：整串傳送給 `pinyin-pro`（`{ toneType: "num", type: "array" }`），保留上下文以正確判斷「快樂／音樂」、「銀行／行人」等破音字。**嚴禁用單字逐一查表取代整句上下文**。
4. **數字拼音轉注音**：轉換零聲母、ü、j/q/x、y/w 規則，保留漢字與注音 1:1 映射。
5. **套用覆寫字典**：依序支援詞彙級（`phraseOverrides`）、單字級（`overrides`）與特定位置（`overrideResolver`）。
6. **產生排版標籤或 Word OpenXML 節點**：
   - **橫排行內（Inline Prose）**：以 `bb-zhuyin-pair--inline` 排版，支援正常斷行與無障礙讀屏（`aria-hidden="true"`）。
   - **黑板直排（Blackboard Vertical）**：依標檢局調號標準，標準調號（ˊˇˋ）置於末符右上角不佔寬度，輕聲（˙）置於頂端專屬槽，數字百分比（如 100%）在漢字槽內橫向群組，波浪號／破折號自動轉直式︱。
   - **Word 原生注音標記（Ruby）**：產出 `<w:ruby>` OpenXML 節點，支援 Microsoft Word 完整原生編輯與列印。
   - **考卷方格／田字格作答欄**：以標準 Word Table 產生上注音、下空白方框之標準生字題。
7. **嚴格零缺漏驗證（Zero-Missing Coverage）**：執行 `validateCoverage(root)`，確認 `coverage === 1` 且無任何 unresolved 字符。

---

## 常用使用情境與程式碼

### 1. 快速 CLI 命令列工具使用
在終端機中直接標註文字或檔案：
```bash
# 取得行內 HTML 標籤
node scripts/annotate-cli.js "快樂的音樂會"

# 取得 JSON / Token 陣列（檢視讀音與覆蓋率）
node scripts/annotate-cli.js "今天我們到銀行開戶，路上有很多行人。" --format tokens

# 批次處理文字檔並輸出 HTML
node scripts/annotate-cli.js --file article.txt --out article-zhuyin.html
```

### 2. 靜態網頁與 CDN 零安裝引入範本
在 HTML `<head>` 中引入：
```html
<link rel="stylesheet" href="assets/zhuyin-renderer/zhuyin-renderer.css">
<script src="https://cdn.jsdelivr.net/npm/opencc-js@1.0.5/dist/umd/full.js"></script>
<script src="https://cdn.jsdelivr.net/npm/pinyin-pro@3.27.0/dist/index.js"></script>
<script src="assets/zhuyin-renderer/zhuyin-renderer.js"></script>
```

在 JS 中呼叫：
```js
const toSimplified = OpenCC.Converter({ from: "tw", to: "cn" });
// 產生行內 HTML
const inlineHTML = BlackboardZhuyin.buildInlineTextHTML("快樂的音樂會", {
  pinyinFn: pinyinPro.pinyin,
  pinyinTextNormalizer: toSimplified
});

// 產生黑板直排 HTML
const verticalHTML = BlackboardZhuyin.buildVerticalTextHTML("快樂學習\n天天向上", {
  pinyinFn: pinyinPro.pinyin,
  pinyinTextNormalizer: toSimplified,
  fs: 48 // 漢字基準字級
});
```

### 3. 動態 DOM 整頁自動加注音（Non-framework）
```js
const session = BlackboardZhuyin.annotateElement(document.body, {
  pinyinFn: pinyinPro.pinyin,
  pinyinTextNormalizer: toSimplified,
  strict: true,
  observeMutations: true // 自動監聽後續 DOM 變化
});
```

### 4. 國小國語 Word (.docx) 考卷生字題產出
透過 `scripts/generate_zhuyin_exam.py` 可以自動將課文或詞彙轉為 Word 考卷，產出：
1. **看注音寫國字**：上方精確注音（含調號），下方空白方框（田字格風格），學生手寫國字。
2. **看國字寫注音**：國字題幹後方自動留出 `（　　）` 作答欄。
3. **全文附注音閱讀測驗**：採用 Word 底層原生 `<w:ruby>` 格式，字距行距不破版，相容所有 Office 版本。
4. **一鍵雙份產出**：同步產出「學生作答卷」與「教師詳解卷（紅字答案）」。

執行指令：
```bash
python scripts/generate_zhuyin_exam.py
```
（產出檔案預設位於 `output/` 目錄）

---

## 驗證清單（驗收標準）

- [ ] 執行 `npm test` 單元測試全數通過。
- [ ] 涵蓋率測試：`validateCoverage(root).coverage === 1`，unresolved 清單為空。
- [ ] 破音字校驗：「快樂／音樂」（ㄌㄜˋ／ㄩㄝˋ）、「銀行／行人」（ㄏㄤˊ／ㄒㄧㄥˊ）。
- [ ] 特殊拼音校驗：葉、眼、楊、女、溫、居、窘（y/w、ü、j/q/x 轉注音）。
- [ ] 聲調位置校驗：一、二、三、四聲與輕聲（˙ㄉㄜ）。
- [ ] 直排符號校驗：ASCII 數字/英文橫向成組、波浪與「至」正確轉直排破折號。
- [ ] 無障礙閱讀校驗：螢幕報讀軟體朗讀時，每個漢字僅報讀一次，不重複朗讀注音 track。
- [ ] Word 試卷驗證：生成的 `.docx` 能在 Microsoft Word 中正確開啟，注音與方格對齊工整，無 XML 損壞。

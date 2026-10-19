# Antigravity Motion Explainer (解說動畫影片工作流)

用自然語言與程式碼製作「原理解說動畫影片」的端到端全自動工作流。

整合 **HyperFrames**（HTML + GSAP 物理幾何動態）、**微軟 Edge-TTS 台灣神經語音**、**自動字幕對齊**、**60-30-10 極簡三色主題**、**源石黑體子集化** 與 **Review Loop 聯絡單審查**，一鍵渲染可直接用於教學投影或 YouTube 發布的 1080p 60fps MP4 動畫影片。

---

## 🌟 核心特色

1. **零 GPU 依賴的中文語音合成**：內建微軟台灣語音（預設 `zh-TW-HsiaoChenNeural` 溫和女聲 / `zh-TW-YunJheNeural` 穩重男聲），自然流暢。
2. **純 CSS/GSAP 幾何物理動態**：以 HTML 與 GSAP 3 建構，支援高精度 SVG 路徑描繪、旋轉、形變與數值滾動。
3. **60-30-10 極簡色彩系統**：60% 背景色、30% 主體骨架、10% 亮眼結論強調，消除視覺雜訊。
4. **字型子集化技術**：自動抽取全片中文字元，將 15MB 源石黑體壓縮至 ~140KB，徹底消除 Puppeteer 渲染逾時。
5. **Review Loop 自我審查機制**：自動生成 4x4 視覺節奏聯絡單（Contact Sheet），一目瞭然排查版型衝突與字幕重疊。
6. **教育審查相容**：深度整合 `g4-curriculum-review`，可直接套用於國中小各科知識點與迷思診斷解說。

---

## 📦 安裝與環境需求

- Node.js 20+
- FFmpeg（需加入系統 PATH）
- Python 3.10+
- HyperFrames CLI：`npm install -g hyperframes`

Python 相依套件：
```bash
pip install -r requirements.txt
```

---

## 🚀 快速開始

### 1. 初始化動畫專案
```bash
hyperframes init videos/<專案名稱> --non-interactive --example=blank --skill=faceless-explainer
```

### 2. 獲取開源字型
```bash
bash scripts/fetch_fonts.sh videos/<專案名稱>
```

### 3. 生成旁白語音與對齊字幕
```bash
python3 scripts/edge_tts_voice.py --project videos/<專案名稱> --voice zh-TW-HsiaoChenNeural --rate="-5%"
python3 scripts/voice_meta.py videos/<專案名稱>
python3 scripts/patch_captions.py videos/<專案名稱>
```

### 4. 套用主題與字型子集化
```bash
python3 scripts/theme.py videos/<專案名稱>
python3 scripts/subset_fonts.py videos/<專案名稱>
```

### 5. 審查與渲染
```bash
# 語法與佈局檢查
cd videos/<專案名稱> && npm run check

# 生成 Review Contact Sheet
python3 ../../scripts/sheet.py --project . --video renders/draft.mp4 --beats --out renders/sheets/beats.png

# 渲染高畫質 MP4
npm run render
```

---

## 📄 授權條款

MIT License. 源石黑體基於 SIL Open Font License 1.1 授權。

# 國小四年級社會科第二單元《家鄉的傳統住屋與生活器具》

本資料夾收納康軒版國小四年級上學期社會第二單元之全套互動教學動畫簡報、原理解說影片、背景圖片與測試驗收工具。

---

## 📁 資料夾內容架構

- **`index.html` / `社會第二單元.html` / `社會二單元.html`**：
  - 14 頁全互動式 HTML 教學簡報。
  - 遵循 Emil Kowalski 設計工程工藝標準（零無差別 `transition: all`、零 `scale(0)`、進場自訂強烈曲線、`:active` 微縮觸感、適配 `100dvh`/`100svh`）。
  - 包含教室超大投影字體、全卡片考證圖說、手繪三合院格局圖、Slide 6 建築物理 Canvas 解剖台、Slide 9 器具機械物理 Canvas 模擬台、Slide 12 小偵探抓錯擂台、Slide 13 習作深度檢討 (P.12-17) 工作台。
- **`社會第二單元.mp4` / `social_explainer_125s.mp4`**：
  - 205.32 秒（3分25秒）1080p 高畫質關鍵原理解說動畫影片（嵌入 Slide 5 影音劇場）。
  - `social_explainer_silent.mp4`（無聲備份版）
  - `social_explainer_tts.mp3`（微軟臺灣女聲神經語音 `zh-TW-HsiaoChenNeural` 旁白音訊檔）。
- **`assets/`**：
  - 全套 14 頁專屬 AI 繪本背景插畫（`bg_slide1.jpg` ~ `bg_slide14.jpg`），16:9 比例、無可讀文字、溫暖臺灣鄉土色調。
- **`renders/`**：
  - 14 頁 Playwright 實機瀏覽器渲染驗收截圖。
- **`render_social_video.py`**：
  - 高解析度視訊幀生成與 FFmpeg 壓制腳本。
- **`test_deck_social.py`**：
  - Playwright 端到端驗收自動化腳本。
- **`自我檢測審查報告_社會二單元傳統住屋與器具.md`**：
  - 三階漏斗審查報告與 Before / After / Why 動效審查表。

---

## 🚀 課堂使用方式
直接以現代瀏覽器（Edge / Chrome / Safari）雙擊打開 `index.html` 或 `社會第二單元.html` 即可全螢幕離線流暢投影教學。

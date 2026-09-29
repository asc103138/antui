# 專案交接筆記 (handoff.md)

## 目前進度
- [x] 完成新專案基礎結構初始化（`AGENTS.md`, `ANTIGRAVITY.md`, `README.md`, `.gitignore`, `handoff.md`）
- [x] 完成本地 Git 儲存庫初始化與初始提交
- [x] 建立 GitHub 私有儲存庫並完成初次推送
- [x] 引入 `gem-to-agent-kit`，完成環境依賴安裝（`python-pptx`, `yt-dlp` 等）
- [x] 完成「素養命題助手」Gem 升級為 Antigravity 工作流（建立 `competency-test-generator` Skill、`/generate-test` Workflow 與 `generate_exam_docx.py` 試卷自動排版腳本）
- [x] 成功通過範例試卷生成驗證（輸出學生卷與教師卷 Word 檔）
- [x] 完成國小四年級翰林版國語第三課《鏡頭下的家鄉》Canva 填空繪圖教材（執行 RDQ 規格確立）
  - 生成 16:9 相容 Canva 之原生 PPTX（含 1 頁田字四象限總覽 ＋ 4 頁分段放大相框頁）
  - 產出 A4 橫向黑白列印學習單 PDF 與單檔 HTML（支援瀏覽器列印）
  - 產出教師參考答案卷與教學指引（`教師參考答案與教學指引.md`）
- [x] 完成中秋彩繪柚子教學影片分鏡與 NotebookLM 簡報輸出（執行第二次 RDQ 規格確立）
  - 透過 `gemini-notebook-mcp` 建立專屬筆記本並產出「360 Pomelo Cinema」Studio 簡報（下載 PDF 與 PPTX）
  - 依據 `antigravity-video-specs` 02 教學影片規範產出 `SCRIPT.md`（11個鏡頭，單行字幕≤25字）與 `DESIGN.md`
  - 納入「順時針四面環繞」與「防沾染操作守則」（由上而下、先勾邊後上色、雙指捏頂底旋轉）
- [x] 完成 STEAM 教師社群成果製作專案初始化與技能部署（`steam成果製作`）
  - 同步部署 `steam-community-docs` 全域技能（`scripts/`, `references/templates/`, `assets/`）
  - 完成 Windows 11 Word 原生轉存 PDF 與 Edge 海報渲染環境
  - 預先生成 115 年 10 月 30 日活動簽到表（內聘講師：王怡婷 老師）於 `steam成果製作/1030/` 目錄


## 下一步規劃
- [ ] 支援更多科目（國文、自然、社會、英文）之生活情境出題範本
- [ ] 結合 Antigravity 內建生圖（Nano Banana Pro）自動生成試卷情境插圖
- [ ] 若需合成影片，執行 Edge-TTS 旁白生成與 Playwright/FFmpeg 影音渲染匯出 MP4
- [ ] 評估是否將四段鏡頭畫面繪圖示範加入 Canva 範本投影片中
- [ ] 確定套件的程式語言與建置工具（例如 TypeScript / Vite / Rollup / npm / pnpm）
- [ ] 初始化 `package.json` 或專案設定檔
- [ ] 開始核心模組/工具功能實作

## 踩坑與注意事項
- Google Gemini 外部分享連結預設需登入且常隱藏 Instructions，若無法直接複製可由 Gem 自報家門或直接根據科目/年級/單元由 Agent 生成標準 108 課綱試題。

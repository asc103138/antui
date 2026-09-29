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
- [x] 整合 AntiGravity 2 全域技能庫與跨電腦同步架構
  - 盤點並補齊全域 23 個技能，新增 7 大核心主題（`02-essentials`, `04-github-obsidian`, `06-second-brain`, `07-supabase`, `09-ollama`, `10-gemini`, `13-chezmoi`）
  - 升級 `01-notebooklm`：導入 6 階段狀態機、防循環規則與 `Test-NotebookLMConnection.ps1` 診斷腳本
  - 設定 Windows 使用者全域環境變數 `PYTHONUTF8 = 1`（防呆 CP950 編碼問題）
  - 設定 `GEMINI_API_KEY` 使用者環境變數並通過 Google AI Studio 唯讀連線測試（HTTP 200 OK）
- [x] 建立 chezmoi 跨電腦同步系統與新私有儲存庫
  - 安裝 `chezmoi v2.73.0`，全域技能與 MCP 設定納管並推送至私有庫 `asc103138/dotfiles`
  - 第二台電腦只需執行 `chezmoi init --apply asc103138/dotfiles` 即可一鍵還原技能
- [x] 完成 GitHub 帳號切換與專案遷移
  - GitHub CLI 認證切換至作用中帳號 `asc103138`（謝敦元）
  - Git 全域提交作者更新為 `謝敦元 <305822202+asc103138@users.noreply.github.com>`
  - 建立專屬私有儲存庫 `asc103138/antui`，切換 remote 並完成初次推送
- [x] 對接 Obsidian 本機第二大腦駕駛艙
  - Vault 路徑：`D:\opencode\我的筆記`
  - 建立專案駕駛艙筆記：`D:\opencode\我的筆記\antui\專案工作流程.md`
  - 更新 `AGENTS.md` 自動連結駕駛艙
- [x] 研讀奕鈞老師「PDF 萬用工具 v3.1」並升級全域文書處理技能
  - 升級 `14-advanced-docs`：新增高畫質黑白灰階轉換（省墨列印）、自訂壓縮檔案瘦身、單/多頁旋轉校正、拆分轉 PNG 打包 ZIP、重編標準頁碼與半透明浮水印
  - 同步將最新技能版本推送至 `asc103138/dotfiles`
- [x] 建置「敦元老師的 AntiGravity 技能倉庫」公開展示網站（1:1 參照 ijun-ai.com 風格與功能規格）
  - 建立全靜態網站架構（`index.html`, `tools.html`, `style.css`, `script.js`, `data.json`），免額外工具鏈即可直出
  - 完美重現 ijun-ai.com 高質感日夜雙主題（日間溫暖米白+亮橘 / 夜間深邃海藍+科技青色）
  - 實作即時關鍵字搜尋、熱門快搜標籤（RDQ、PDF、第二大腦、NotebookLM、chezmoi、STEAM 等）與六大類別快速導覽
  - 打造互動式 `SKILL.md` 內文彈窗閱讀器（含輕量 Markdown 解析、程式碼高亮、引用塊與一鍵複製完整 Prompt 規格）
  - 實作觸發語一鍵複製與 Toast 即時通知反饋
  - 撰寫 `scripts/build_site_data.py` 自動化建置腳本，自動掃描收錄 25 款全域與本地技能至 `data.json` 並備份於 `skills_docs/`
  - 經 Playwright MCP 實體瀏覽器渲染測試（日夜切換、彈窗閱讀、分類過濾與捲軸均通過驗證）
  - 調用 `antigravity-draw`（04-draw）生圖技能為 7 大核心技能（RDQ、PDF進階文件處理、教師第二大腦、NotebookLM、chezmoi跨裝置同步、STEAM社群公文、素養命題助手）生成專屬 16:9 3D 全息科技封面縮圖（存放於 `assets/covers/`），並於前端實作無圖卡片自動幾何科技漸層封套（Fallback Cover）
  - 更新 `README.md` 詳細提供本機預覽指令與 GitHub Pages 免費一鍵公開部署指南
- [x] 將儲存庫切換為 Public 並正式完成 GitHub Pages 自動建置部署
  - 儲存庫切換為公開（Public），對應公開分享目標
  - 調用 GitHub Pages API 正式啟用，並經 GitHub Actions `pages-build-deployment` 自動編譯推送
  - 線上生產環境網址實測驗證通過（HTTP 200 OK）：`https://asc103138.github.io/antui/`

## 下一步規劃
- [ ] 支援更多科目（國文、自然、社會、英文）之生活情境出題範本
- [ ] 結合 Antigravity 內建生圖（Nano Banana Pro）自動生成試卷情境插圖
- [ ] 若需合成影片，執行 Edge-TTS 旁白生成與 Playwright/FFmpeg 影音渲染匯出 MP4
- [ ] 評估是否將四段鏡頭畫面繪圖示範加入 Canva 範本投影片中
- [ ] 確定套件的程式語言與建置工具（例如 TypeScript / Vite / Rollup / npm / pnpm）
- [ ] 初始化 `package.json` 或專案設定檔
- [ ] 開始核心模組/工具功能實作
- [ ] 於第二台電腦透過 `chezmoi init --apply asc103138/dotfiles` 驗證一鍵同步

## 踩坑與注意事項
- **Windows CP950 編碼解法**：已永久在使用者環境變數設定 `PYTHONUTF8 = 1`，避免 Python、nlm、uv 輸出中文字元時拋出 `UnicodeDecodeError`。
- **機敏資訊隔離原則**：API 金鑰與 Token 嚴禁進入 Git 儲存庫，chezmoi 只同步指令與可攜式設定，每台電腦獨立驗證授權。
- Google Gemini 外部分享連結預設需登入且常隱藏 Instructions，若無法直接複製可由 Gem 自報家門或直接根據科目/年級/單元由 Agent 生成標準 108 課綱試題。

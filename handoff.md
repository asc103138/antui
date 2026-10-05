# 專案交接筆記 (handoff.md)

## 目前進度
- [x] 完成 `04-draw` 生圖技能全面升級為 **Nano Banana 2** 專屬架構規範，並同步更新至公開展示網站與 chezmoi 跨裝置管理庫
  - **診斷與架構校準**：排查確認原技能為舊版通用草稿，未指定特定架構；全面升級為 Google Gemini Flash Image / Nano Banana 2 原生架構。
  - **全域技能升級**：更新 `~/.gemini/config/skills/04-draw/SKILL.md`，完整規範 AntiGravity 原生 `generate_image` 之參數規範（`Prompt`、`AspectRatio`、多模態 `ImagePaths` 參考圖）、四大情境提示詞範本（國小高對比黑白試卷線稿、16:9 全息簡報底圖/封面、扁平化去背圖標、角色一致性三視圖卡）與繁體文字後製鐵律。
  - **本機快速腳本**：新增 Windows 原生免金鑰 PowerShell 快速生圖腳本 `draw.ps1`。
  - **dotfiles 與展示網站同步**：納入 `asc103138/dotfiles` 跨電腦同步管理（Commit `2d057c0` 已推送）；更新 `d:\antui` 之 `data.json` 與 `skills_docs/`，展示網站技能收錄達 41 款。
- [x] 完成 STEAM 教師社群（梧棲區中正國小）行政成果與報銷單據全套自動化模組
  - 建立全域技能 `steam-community-docs`，支援 115 年度推動校園 STEAM 教育實施計畫成果表、簽到表、內聘講師領據自動生成。
  - 完成 10/01 場次（王怡婷老師「micro:bit 甩繩軌跡神射手跨域教學」）成果表（含 4 大亮點、2 欄照片集錦、A4 海報）、親筆簽到表、領據生成，並配置 Gmail SMTP 全域寄件通道。
  - 完成 10/05 場次（「學生學習成效分析與教案修正」）全套成果表（3 頁完整排版、2 欄照片集錦、A4 海報）、親筆簽到表送審版、雙講師兩張獨立單獨領據（曾泊淞 2 節 2,000 元、謝敦元 2 節 2,000 元），並已透過 Gmail 成功寄發成果信至教育局承辦信箱。
  - 確立最新領據範本標準（`1005領據_正楷底線空白版`）：上方「領款人」與下方「具領人」全面配置標準手寫長底線，嚴禁電腦套印講師姓名，提供清晰簽名位置供講師親筆簽收。
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
- [x] 完成 Hugging Face 全域生態掛接與展示網站技能庫擴充（技能庫收錄擴增至 34 款）
  - 全域註冊 Hugging Face 官方 MCP 伺服器（`mcp_config.json`，支援端點 `https://huggingface.co/mcp`）
  - 透過 `uv tool` 全域安裝最新 `hf` CLI（v2.0.0）終端工具，可直接於 PowerShell 呼叫
  - 新增全域 `16-huggingface` 技能，並同步 7 大官方 Agent Skills（`hf-cli`、`huggingface-datasets`、`huggingface-gradio`、`huggingface-best`、`huggingface-spaces`、`huggingface-papers`、`huggingface-local-models`）
  - 更新 `scripts/build_site_data.py` 分類與首頁推薦，重新產出 `data.json` 與 `skills_docs/`
  - 更新全域 `00-install-all` 技能清單納入 `16-huggingface`
  - 將 MCP 設定與新增技能檔案納入 `chezmoi` 跨電腦同步管理
- [x] 修復展示網站在行動載具（Mobile）上索引與導覽失效問題
  - 修正 Sticky Header 遮蔽問題：全域區塊與分類卡片加入 `scroll-margin-top: 85px`，解決行動裝置跳轉時標題被頂部 72px 導覽列遮蔽之問題。
  - 行動版導覽抽屜（Hamburger Menu）體驗升級：改為全螢幕抽屜覆蓋（`fixed` + 滿版按鈕），點擊項目後精準平滑滾動並自動收合選單，點擊外側空白自動關閉。
  - 橫向滑動分類軌（Scroll Ribbon）：行動端分類標籤與熱門快搜標籤改為原生橫向流暢滑動，避免大量標籤垂直換行推擠畫面。
  - 分類篩選與熱門關鍵字連動自動捲動：點擊分類膠囊或熱門關鍵字後，即時平滑捲動至技能目錄區，並將當前選中膠囊自動置中於橫向軌道；過濾狀態下自動隱藏靜態精選區塊，直接呈現篩選結果，徹底解決手機上點擊無視覺反應的假死問題。
  - 輸入框支援 Enter 鍵收起虛擬鍵盤並平滑捲動，並協調搜尋字串與分類篩選之切換邏輯，杜絕跨條件衝突。
  - 經 Playwright MCP 實體模擬 iPhone 390x844 視窗完成漢堡選單、分類點選、關鍵字檢索、彈窗閱讀與重置搜尋之端到端驗證。

- [x] 完成 108 課綱國小四年級（第二學習階段）國語文、數學、社會三大學科生活素養命題模組研發
  - 國語文模組：《走讀家鄉尋找老手藝：傳統竹編與綠色生活》（對應 5-Ⅱ-3、5-Ⅱ-4、6-Ⅱ-1、國-E-A1、國-E-B1、國-E-C2），設計篇章文意推論、圖表數據分析、給阿公的感謝便條生活應用寫作（附 4 級 Rubrics）。
  - 數學模組：《校園綠色市集與園藝花圃規劃》（對應 N-4-2、S-4-3、D-4-1、數-E-A1、數-E-A2、數-E-B1、數-E-B2、數-E-C1），設計四則混合括號運算、長方形中央步道扣除之實際種植面積分割計算、小白菜採收折線圖數據增長差值分析與低溫變因決策。
  - 社會模組：《家鄉的生命之泉——百年老水圳與水資源守護》（對應 1b-Ⅱ-1、2a-Ⅱ-1、3a-Ⅱ-1、社-E-A1、社-E-B1、社-E-B3、社-E-C1），設計水圳開鑿史地脈絡價值、水圳上中下游水質檢測表污染判讀、小學生具體護水方案公民行動倡議（附 4 級 Rubrics）。
  - 調用生圖工具（04-draw / Nano Banana Pro）生成三張適合學校黑白試卷列印的高對比黑白線稿情境插圖，存放於 `gem/assets/exam_images/`。
  - 成功完成 Word 自動排版輸出，於 `gem/output/` 產出學生卷（3份）與教師詳解卷（3份），含素養雙向細目表與評分規準。
  - 升級 `competency-test-generator/SKILL.md`，並更新展示網站 `data.json` 與 `skills_docs/`。

- [x] 完成 micro:bit 融入國小資訊教育 100 篇系統性文獻回顧（PRISMA 矩陣與 CSV 資料庫）
  - 嚴格落實指導教授「完全屏除主觀自陳問卷」之要求，全數收錄客觀成就測驗、實作規準盲評（ICC 信度）、程式碼複雜度指標與系統日誌行為數據。
  - 完整收錄 100 篇國內頂尖師培碩博士論文與國際頂刊（Computers & Education, IEEE TLT, ACM TOCE/SIGCSE, BJET），涵蓋五大核心向度（Cluster A 客觀測驗 35 篇、Cluster B 實作規準 15 篇、Cluster C 代碼結構 20 篇、Cluster D 跨域STEAM 15 篇、Cluster E GenAI鷹架與PRIMM 15 篇）。
  - 產出 Markdown 矩陣總表 [microbit_literature_matrix.md](file:///d:/antui/research/microbit_literature_matrix.md) 與 Excel 專用 [microbit_literature_matrix.csv](file:///d:/antui/research/microbit_literature_matrix.csv)，並提供自動化匯出腳本 `scripts/export_literature_matrix.py`。
- [x] 完成 NotebookLM 專屬研讀庫建置與雙人學術 Podcast（Audio Overview）生成
  - 建立研讀庫「micro:bit 融入國小資訊教育 100 篇文獻探討研究庫」（ID: `d8457d44-8433-43b2-a882-8233cf1c8cc0`），上傳並成功索引 100 篇客觀文獻矩陣。
  - 啟動 Studio 雙人對談音訊（Audio Overview，Artifact ID: `969c8e08-8a6c-48e3-b570-f1fb9decd876`），以繁體中文深入剖析「屏除自陳問卷、轉向三大客觀評量取徑」之學術典範轉移。
  - 驗證跨文獻語意檢索與提問範本，可即時輔助第二章文獻探討與教育統計設計。

- [x] 完成 115 學年度校內語文競賽【梧棲區中正國小・四年丙班】專屬 7 大項目「20 天在校集訓 ＋ 4 週末假日自學增量」全套系統建置
  - 期程嚴格鎖定：115 年 10 月 5 日（週一）至 10 月 30 日（週五），整整 4 週、20 個在校集訓日（Day 01 至 Day 20），並正式納入 4 個週末假日自主自學與作業增量（週末一 10/10~11、週末二 10/17~18、週末三 10/24~25、週末四 10/31~11/01），共 24 個時段全排程。
  - 最新規範落實：「遇到假日改為自學與回家作業增量」，學生版提供明確增量作業（作業增量 A、B、C）與家長評核欄；老師版提供週末自學指引與週一晨間統一驗收指標規準。
  - 項目分類與資料夾獨立歸檔（存放於 `115校內語文競賽/四年丙班_各項目培訓資料庫/`）：
    1. `01_寫字書法組`：28字楷書＋落款（中正國小四年丙班 ○○○書），含九宮格臨摹框、28字間架結構與通病解析，週末增量宣紙大篇幅實寫與字解。
    2. `02_作文組`：現場出題600-800字，起承轉合四階段、五感摹寫、修辭庫、90分鐘配速、兩篇高分範文，週末增量300~600字長篇練筆與60分鐘全篇模考。
    3. `03_國語字音字形組`：400題全國賽真題（每日10音+10形），學生版答案完全挖空（留白作答框），老師版含完整標準注音國字詳解，週末增量50~60題大型挖空卷與個人錯題卡。
    4. `04_國語朗讀組`：林清玄〈藍蝴蝶〉400字，學生版無注音大字稿與換氣符號練習，老師版全篇聲情符號標記稿，週末增量全篇10~12遍計時、鏡前抬頭訓練與家庭朗讀會。
    5. `05_臺灣台語朗讀組`：周世雄〈04 阿公變魔術〉380字，學生版純漢字挖空拼音稿，老師版漢字+臺羅拼音+變調解析，週末增量全篇10~12遍計時、長輩聽讀糾錯與入聲促音特訓。
    6. `06_國語演說組`：二擇一題目420字雙篇示範講稿、四格骨架心智圖草稿單、三大手勢與台風評量，週末增量420字完全背誦脫稿8遍、眼神三角掃視與3分鐘按鈴演練。
    7. `07_臺灣台語情境演說組`：〈食中晝〉看圖演說示範講稿、5大評判即席問答（Q&A）標準台語回答話術與自主擬答單，週末增量看圖演講8遍、5題提問隨機抽測3輪與全套流程彩排。
  - 檔案規格：每個項目完整產出「老師版（指導指引＋每日進度評量表）」與「學生版（在校挖空學習單＋自評表）」之 Markdown (.md)、Word (.docx) 與微軟原生高清 PDF (.pdf)，共計 42 份精編文件，全部完成測試與轉檔驗證。

- [x] 完成語文競賽子專案初始化與全新全域技能固化（`school-language-contest-coach`）
  - 子專案配置：在 `115校內語文競賽/` 目錄建立 `AGENTS.md`、`ANTIGRAVITY.md`、`README.md`、`.gitignore`，確立專案規範與工作指引。
  - 封裝全新全域技能：`C:\Users\ccps\.gemini\config\skills\school-language-contest-coach/`
    - `SKILL.md`：詳列 7 大項目規範、四大鐵律（年級鎖定、雙軌獨立、日曆聯動、三格式交付）、SOP 四步驟與觸發語。
    - `scripts/`：封裝 `docx_styler.py`（公文/考卷級排版樣式庫）、`pdf_converter.py`（Word COM 高清轉 PDF 工具）與 `generator.py`（主控生成引擎）。
    - `references/`：建立 `contest_spec_template.json` 結構化競賽參數範本。
  - 展示網站同步收錄：更新 `scripts/build_site_data.py` 將新技能收錄至「🏫 教育實戰與社群成果」類別，重構 `data.json`（擴增至 35 款技能）並同步至 `skills_docs/`。
  - 加入 chezmoi 跨電腦同步管理：已執行 `chezmoi add` 納管最新技能設定。

- [x] 完成國小四年級運動會創意進場舞蹈教學影片製作（個人示範版 ＆ 全班團練版）
  - 依據 `claude-video-specs` 02 教學影片規範與 SOIL 教學脈絡（引起動機 ➔ 動作拆解 ➔ 喚起行動），為國小四年級學童打造完整的 4 組 8 拍進場舞教學。
  - 徹底解決音畫脫軌與 BGM 斷音問題：
    - 捨棄純瀏覽器錄影可能產生的 JavaScript seek lag 累積誤差，改採 **FFmpeg 14 分段獨立合成管線（`build_full_video.py`）**。
    - 示範與驗收段落直接裁切原影片音訊進行**物理級音畫鎖定（100% 精準對齊）**。
    - 解說段落背景音樂維持 18% 底襯（Ducking），示範與驗收拉回 100% 全音量，全片音樂無縫貫穿不中斷。
    - 全段強制統一編碼規格：1080p 30fps、AAC 48000Hz 雙聲道 192kbps，杜絕 Concat demuxer 採樣率錯置導致的聲音 2 倍速/時長拉長問題。
- [x] 完成國小四年級教材與試題全域自我檢測審查機制（`17-g4-curriculum-review`）與子專案初始化（`g4-curriculum`）
  - 建立全域審查技能：`C:\Users\ccps\.gemini\config\skills\17-g4-curriculum-review/`（含三階漏斗機制、狀態機、判定邏輯、中正國小版本查詢指南、四年級 CLT 認知負荷檢核量表、常見迷思庫與自動快篩腳本）。
  - 鎖定授課版本與策略：數學（南一版）、國語（翰林版）、社會（康軒版）；中階未達標時鎖定「極簡一鍵選擇（象限Ⅳ）」RDQ 訪談。
  - 完成專案初始化：於 `D:\antui\g4-curriculum` 建立獨立專案，關聯 GitHub 公開儲存庫 `asc103138/g4-curriculum`，啟用 GitHub Pages（`https://asc103138.github.io/g4-curriculum/`），並同步建立 Obsidian 筆記 `D:\opencode\我的筆記\g4-curriculum\專案工作流程.md`。
- [x] 完成 Word (.docx) 國字自動注音標註與學習單排版工具研發並固化為全域技能（`18-word-zhuyin`）
  - 整合教育部審定多音字/破音字片語優先字典（`zhuyin_dict.py`），完美解決「長度/長大、音樂/快樂、銀行/行人、便宜/方便、重新/重要」等 15 處繁體破音字誤判。
  - 支援三大排版模式：雙列表格模式（上注音下國字，最適小學列印）、Word 原生 Ruby 旁註模式與行內夾註模式。
  - 內建終端多音字人工複查報告表（Audit Report），供教師快速巡檢。
  - 全域技能固化：安裝至 `C:\Users\ccps\.gemini\config\skills\18-word-zhuyin/`，納入 chezmoi 跨電腦同步管理，公開展示網站收錄擴增至 37 款全域技能並產生專屬 3D 科技封面（`cover_18_word_zhuyin.jpg`）。
- [x] 安裝 Emil Kowalski 全域設計工程技能並將動效最低標準正式納入專案規範與展示網站重構
  - 全域技能安裝：引進知名設計工程師 Emil Kowalski（Linear/Vercel、Sonner 作者）開源之 `emil-design-eng`（設計工程與動畫審查核心哲學）與 `mobile-native`（行動端 Web 原生質感與 CSS 修復）技能，安裝至 `C:\Users\ccps\.gemini\config\skills/`，並補強繁體中文語境觸發詞。
  - 確立專案最低標準：更新 `AGENTS.md`，明訂全案前端動效與 UI 以 Emil Kowalski 規範為最低標準（要求 `| Before | After | Why |` 表格審查、高頻操作零動畫、入場強烈 `ease-out`、嚴禁 `scale(0)` 憑空出現、嚴禁 `transition: all`、按鈕必備 `:active` 微縮觸感、行動端消除點擊反白閃爍與 `100dvh` 適配）。
  - 一鍵全面重構：依審查報告重構 `style.css`，消滅所有 `transition: all`，導入 `--ease-out`、`--ease-in-out`、`--ease-drawer` 自訂物理曲線；為所有按鈕與觸發標籤加入 `user-select: none;` 與 `:active` 觸感；以 Sonner 規格優化 Toast 與 Modal 彈窗平滑進場。
  - 專案資料同步建置：更新 `scripts/build_site_data.py` 新增「🎨 介面美學與動效工程」類別，重新產出 `data.json`（技能庫擴增至 39 款、7 大主題），同步產生 `skills_docs/` 並在首頁新增「Emil 動效標準」與「手機原生」熱門檢索膠囊。
- [x] 完成網頁全面同步 iPhone 18 Pro 旗艦旗艦美學與主視覺重塑（依據 Emil Kowalski 最低標準執行）
  - **Apple OLED Black & Desert Titanium 雙色主題**：重構全站色系，夜間模式升級為 iPhone 18 Pro OLED 純黑（`#000000`）搭配深空黑鈦（`#121215`）、自然鈦（`#f5f5f7`）與沙漠金（`#e4c988`）；日間模式升級為 Apple 陶瓷銀白（`#f5f5f7`）與深空灰字體。
  - **Apple Spatial Lighting 空間環境光源**：背景注入 Apple 旗艦發布會等級之環境空間微光（Radial Gradient Spatial Mesh），营造無垠深邃沉浸感。
  - **Dynamic Island 動態島膠囊主視覺**：Hero 標籤全新重構為 Apple 旗艦動態島膠囊，內建微秒級雷達即時綠色脈衝光圈（Live Radar Ping）與沙漠金尊爵標籤。
  - **Apple Keynote 鈦金屬金屬漸層標題**：首頁主標題重塑為大字號金屬光澤漸層（`linear-gradient(180deg, #FFFFFF 15%, #D2D2D7 55%, #86868B 100%)`）搭配 `-0.035em` 緊湊字距與微光外暈。
  - **Apple Spotlight 懸浮搜尋島**：搜尋框改為圓弧流線 Omnibar 膠囊，支援 28px 超高飽和毛玻璃（Spatial Blur）、內建焦點環與 Apple 黑白高對比選中膠囊。
  - **Apple Hardware Chamfer 倒角卡片與 Action Button**：卡片升級為 22px iPhone 連續曲率（Squircle），卡片邊界注入高階鈦金屬雷射倒角高光；按鈕全面改為圓潤 Action Button 膠囊，按下時呈現 `scale(0.96)` 物理微縮。
  - **原生 iOS 底部抽屜把手（Sheet Drag Handle）**：手機版 Modal 頂部嵌入 iOS 原生抽屜把手，Toast 升級為動態島懸浮膠囊。
- [x] 全面落實 Emil Kowalski 設計工程最高工藝標準、修復 #featured 佈局、注入背景空間流體極光與 GAS 全域標準
  - 確立全套工藝為底線：修訂 `AGENTS.md`，明訂全套設計工程標準為專案起步底線（絕非妥協低標），確立無形細節疊加、美感即槓桿、感知效能、彈簧物理與中斷性等 7 大維度。
  - 修復 `#featured` 核心推薦區塊：修正按鈕擠壓切角問題，新增 `.btn-icon` 獨立圓形膠囊樣式；按鈕高度全面提升至 42px（貼合 Apple 44px 觸控熱區）；將 `emil-design-eng` 納入精選首位，展示上限放寬至 8 款完美雙欄/四欄對稱卡片。
  - 植入 Apple 旗艦空間流體極光背景（Spatial Ambient Fluid Aurora）：三大異步有機流光島（22s / 28s / 25s）搭配微型科技空間點陣，純 GPU 合成層硬體加速（`will-change: transform`，零 Reflow 耗能），支援 OLED 深空純黑與陶瓷白日夜雙模式。
  - 打造頂級夜空流星系統 (Celestial Meteors)：在夜間模式背景植入 3 顆不同軌跡、長度與異步週期的彗尾流星（8s / 11s / 15s），偶爾帶著璀璨核心與微光彗尾劃過天際，白天模式自動隱藏維持清爽，完全 0 耗能不干擾內容閱讀。
  - 全域技能 `08-sheets-gas` 規格全面升級：在全域技能庫注入 GAS 前端網頁設計工程與行動原生最高標準（100dvh、輸入框最低 16px、`:active` 微縮、Sonner 級 Toast），並同步至 chezmoi 遠端 dotfiles 私有庫。
  - 資產快取推進至 `v5.2`。
- [x] 診斷並徹底重構天頂流星雨系統（排除四大隱形盲點，升級為 6 顆異步天網織流）
  - **根本原因診斷**：經實體瀏覽器抓屏診斷，確認原本流星不可見之四大真凶：① 日間模式因 `[data-theme="light"] .meteor { display: none !important; }` 被全域隱藏；② 置於 `.spatial-bg-mesh` 內（`z-index: -1`），完全被不透明的卡片與主內容遮蓋；③ 3 顆流星週期 8s~15s 且 flash 僅佔不到 10%，稀疏度過高；④ 尺寸過於纖細（2px）且軌跡短。
  - **獨立浮動層結構**：抽出為獨立 `<div class="meteor-shower-layer">`，`z-index: 40` 搭配 `pointer-events: none`（浮於卡片上層穿透，不干擾任何按鈕點擊與滾動）。
  - **晨昏雙態極光配色**：夜間模式採用純白璀璨光核（5px）＋ 湛藍金色漸層尾焰；日間模式升級為晨曦極光流星（Apple 湛藍 `#0071e3` ＋ 天青科技光暈），白天夜晚皆能欣賞。
  - **天網織流交錯節奏**：擴增為 6 顆流星，軌跡加長至 410px~520px，長度 160px~230px，延遲交錯於 0.4s ~ 4.9s 異步循環（5.6s ~ 7.8s 週期），隨時抬頭皆能見到優雅流星劃過。
- [x] 建立成品一票否決檢查機制 (Zero-Tolerance Gatekeeper Protocol) 與自動化巡檢工具
  - **核心理念立論**：確立「不符合就砍掉重練（Hard Reset）」鐵律，拒絕帶病交付與修修補補。
  - **五重鐵律紅線確立**：動效工藝（禁 `transition: all`、禁 `scale(0)`、禁進場 `ease-in`、必備 `:active` 微縮）、多情境可視性（禁日夜模式遮蔽、禁攔截點擊）、行動端原生（必備 `100dvh`、消除點擊閃爍、字體 ≥ 16px、防誤選）、實體渲染檢驗（嚴禁腦補 pass、控制台零錯誤）、資安與 Commit 紀律（嚴禁洩漏金鑰、禁止無差別 add）。
  - **自動化巡檢工具實裝**：建立 `scripts/audit_gatekeeper.py`，全自動逐行靜態掃描 CSS/HTML/JS 與資安金鑰，违规即 Exit 1 觸發砍掉重練。
  - **工作指引更新**：寫入 `AGENTS.md` 並融入收工流程，作為全體 Agent 開發與交付不可逾越之最高門檻。
- [x] 完成 `html-slide-builder` 儲存庫全域設定與展示網站同步（全域技能庫收錄擴增至 40 款）
  - **全域技能庫部署**：依據 `asc103138/html-slide-builder` 於 `~/.gemini/config/skills/19-html-slide-builder` 建立完整技能規範，整合 Reveal.js 骨架、Firebase Firestore 即時文字雲與單選投票、clip-path 滑桿前後演示、AntiGravity 原生生圖（`generate_image`）與 PIL 亮度去背腳本（`scripts/remove_bg.py`，支援 Windows 萬用字元路徑）。
  - **全域安裝清單升級**：更新 `00-install-all` 技能清單納入 `17-g4-curriculum-review`、`18-word-zhuyin` 與 `19-html-slide-builder`。
  - **chezmoi 跨裝置同步**：將 `19-html-slide-builder` 與 `00-install-all` 同步納管，並已推播同步至私有 dotfiles 儲存庫（`asc103138/dotfiles`）。
  - **展示網站收錄與視覺資產**：調用 `generate_image` 生成專屬 3D 霓虹全息科技封面（`cover_19_html_slide_builder.jpg`），更新 `scripts/build_site_data.py` 分類對應，重新生成 `data.json` 與 `skills_docs/19-html-slide-builder.md`。
  - **嚴格驗收合格**：通過 `audit_gatekeeper.py` 零容忍檢查，經 Playwright 實體瀏覽器渲染測試驗證卡片展示、即時觸發詞一鍵複製與 Markdown 彈窗閱讀器互動完全無誤。
- [x] 完成 `g4-curriculum` 國小四年級教材審查全域設定部署與強制本機教科書實體審查條件強化
  - **全域規則確立**：建立 `~/.gemini/config/rules/curriculum-review-protocol.md`，納入南一數、翰林國、康軒社版本鎖定與三階漏斗審查（最低門檻一票否決、中階RDQ、高階亮點與同型態輸出）。
  - **核心前置紅線（Gate 0 Hard Stop）**：確立「本機教科書為唯一真實依據（Ground Truth）」；生字詞彙必須透過 `check_curriculum.py` 與本機課習真實 PDF 語料進行精確比對（Exact Substring Match），嚴禁 AI 憑空假審查；若本機缺少教材資料夾（`115四上數課習/`、`115四上國課習/`、`115社會課習/`），強制中斷阻擋並提示教師自行合法放置，絕對嚴禁腦補放行。
  - **全域技能與腳本升級**：升級 `17-g4-curriculum-review`（納入 `check_curriculum.py` v2.1、`review-protocol.md`、`RDQ-spec`）；更新 `05-workflow` 與 `00-install-all`。
  - **chezmoi 跨裝置同步**：已將全域規則、升級技能與腳本納管並推送至私有 dotfiles 儲存庫（`asc103138/dotfiles`，Commit: `a634325`）。
  - **工作區架構就緒**：`d:\antui\四年級教材審查機制` 已對齊 `asc103138/g4-curriculum` 完整架構。
- [x] 修復 `family-activity-writing` 簡報第二頁文字雲無法打字輸入問題，並實作重置與防搶鍵機制
  - **根本原因診斷**：確認三大真凶：① Reveal.js 全域鍵盤監聽在注音輸入法選字（Space/數字鍵/Enter）時因缺乏 `event.target` 深度檢驗而搶鍵跳頁；② `e.stopImmediatePropagation()` 阻斷了後續 `Enter` 送出監聽器，導致按下 Enter 無法觸發送出；③ `await addDoc` 同步卡住介面且在離線或權限受限時造成按鈕鎖死。
  - **鍵盤防搶鍵防護**：升級 Reveal.js `keyboardCondition(event)` 同時檢查 `event.target`、`composedPath` 與 `activeElement`；在輸入框監聽中阻止向上冒泡，並直接原生支援 `Enter` 送出與 `Escape` 清除。
  - **互動與重置按鈕強化**：在輸入卡片新增明顯的「🔄 重置」按鈕（供新班級重複使用）與「✕」清除文字按鈕；點擊卡片任何空白處自動聚焦輸入框；切換至第二頁時自動聚焦；送出改為樂觀即時更新（0ms 零延遲），背景非同步同步 Firestore。
  - **Emil Kowalski 規範與實體渲染驗收**：按鈕加入 `:active` scale(0.97) 微縮觸感與輕量 Toast 反饋；經 Playwright 實體瀏覽器抓屏驗證，Enter 送出與重置按鈕 100% 正常；變更已推送至 `asc103138/family-activity-writing`（Commit: `5c97a4a`），並同步更新全域 `19-html-slide-builder` 模板與 chezmoi。




## 下一步規劃
- [ ] 依四年級南一數學與康軒社會單元進度，持續產出符合三階審查之試題與素養學習單
- [ ] 聆聽並下載 NotebookLM 生成之雙人學術對談 Podcast
- [ ] 依據 100 篇文獻與研究變項，草擬論文第二章文獻探討（2.1 實體運算評量演進、2.2 Bebras客觀測驗與實作規準雙軌設計）
- [ ] 規劃教育統計分析架構（ANCOVA 迴歸同質性檢定、二因子混合設計 ANOVA、ICC 雙盲評分者信度標準作業流程）
- [ ] 配合教師授課進度與各版本教科書（康軒、翰林、南一）進一步微調單元題庫
- [ ] 探討將試卷直接轉存 PDF 列印檔之自動化流程（結合 14-advanced-docs）
- [ ] 確定套件的程式語言與建置工具（例如 TypeScript / Vite / Rollup / npm / pnpm）
- [ ] 於第二台電腦透過 `chezmoi init --apply asc103138/dotfiles` 驗證一鍵同步

## 踩坑與注意事項
- **Windows CP950 編碼解法**：已永久在使用者環境變數設定 `PYTHONUTF8 = 1`，避免 Python、nlm、uv 輸出中文字元時拋出 `UnicodeDecodeError`。
- **機敏資訊隔離原則**：API 金鑰與 Token 嚴禁進入 Git 儲存庫，chezmoi 只同步指令與可攜式設定，每台電腦獨立驗證授權。
- Google Gemini 外部分享連結預設需登入且常隱藏 Instructions，若無法直接複製可由 Gem 自報家門或直接根據科目/年級/單元由 Agent 生成標準 108 課綱試題。

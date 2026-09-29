# 敦元老師的 AntiGravity 技能倉庫 (DUN-YUAN AI / antui)

> 專為教師、教育現場與 AI 開發者打造的 AntiGravity 2 全域技能展示站與數位備課工作流庫。  
> 100% 本機端隱私防護、零個資外洩，支援 `chezmoi` 跨電腦秒級無痛同步。

![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)
![AntiGravity: 2.0](https://img.shields.io/badge/AntiGravity-2.0-blue.svg)
![Skills: 24+](https://img.shields.io/badge/Skills-24%2B-brightgreen.svg)

---

## 🌟 網站特色

- 🎨 **日間／夜間雙主題（Day & Night Mode）**：
  - 日間模式：溫暖米白、質感亮橘與清新藍調，閱讀舒適護眼。
  - 夜間模式：深邃夜空海藍（Deep Navy）結合科技青色（Cyber Cyan），兼具極簡與專業感。
- 🔍 **即時智慧搜尋與熱門標籤檢索**：
  - 支援技能名稱、觸發語、類別與內文關鍵字即時模糊比對。
  - 提供 RDQ、PDF、第二大腦、NotebookLM、語音、chezmoi、STEAM 等熱門快搜按鈕。
- 📖 **互動式 SKILL.md 內文閱讀器（Modal Viewer）**：
  - 點擊卡片直接展開完整 Markdown 技術規格與系統 Prompt。
  - 具備語法高亮、引用塊與一鍵複製整篇 Skill 規範功能。
- 📋 **觸發語一鍵複製與 Toast 即時反饋**：
  - 點擊常用觸發語句（如 `「進階文件處理」`、`「RDQ訪談」`），秒級複製到剪貼簿。
- 🔄 **chezmoi 跨裝置秒級無痛同步**：
  - 技能庫已納管至私有儲存庫 `asc103138/dotfiles`，在新電腦上一行指令全數還原。
- ⚡ **自動化建置腳本**：
  - 內建 `python scripts/build_site_data.py`，全自動掃描本機全域技能，即時更新 `data.json` 與靜態文件。

---

## 🧭 技能核心分類

1. **🎯 智能工作流與方法論**：RDQ 需求探索四象限法、開工/收工/專案初始化 SOP、全域懶人包一鍵安裝、新手必備工具盤點。
2. **🧠 第二大腦與筆記生態**：教師第二大腦三層知識體系、Obsidian 專案筆記本地對接、GitHub + Obsidian 雙向駕駛艙、NotebookLM MCP/CLI 自動化。
3. **📑 文件與多媒體神器**：PDF 萬用處理（黑白省墨/自訂壓縮/旋轉校正/頁碼浮水印）、Office 三合一套件（Word/Excel/Edge-TTS）、Groq Whisper 高速轉錄與逐字稿清洗、Nano Banana Pro 繪圖生圖、三類影片製作規範。
4. **☁️ 雲端後端與本地模型**：Gemini API 安全配置、Supabase Postgres MCP、Firebase 後端整合、Google 試算表資料庫 + Apps Script 免費後端、Ollama 離線模型。
5. **⚙️ 環境工程與系統維護**：開發環境自動建置（Git/Node/uv）、GitHub CLI 認證、chezmoi 跨電腦同步、Playwright 瀏覽器控制、Windows 開機與登入效能診斷。
6. **🏫 教育實戰與社群成果**：STEAM 教師社群成果表/簽到表/領據自動生成、108 課綱素養命題助手（Word 考卷自動排版）。

---

## 🚀 本地預覽與開發

本專案為純前端靜態架構（HTML5 + CSS3 + Vanilla JS + JSON），無需安裝繁雜的前端建置工具：

1. **啟動本機預覽伺服器**：
   ```bash
   python -m http.server 8000
   ```
2. **在瀏覽器開啟**：
   - 完整首頁：[http://localhost:8000/index.html](http://localhost:8000/index.html)
   - 技能倉庫：[http://localhost:8000/tools.html](http://localhost:8000/tools.html)

---

## 🔄 技能更新與資料同步

當您在本機 `C:\Users\ccps\.gemini\config\skills` 新增或修改任何技能時，只需執行：

```bash
python scripts/build_site_data.py
```

腳本將自動：
1. 掃描所有技能之 `SKILL.md` 與 YAML Frontmatter。
2. 提取乾淨的簡介、類別、圖示與常用觸發詞。
3. 將全數 `SKILL.md` 備份複製至 `skills_docs/`。
4. 重新產出結構化之 `data.json`。

---

## 🌐 部署至 GitHub Pages

本專案已建立在根目錄，若要免費公開部署至 GitHub Pages：
1. 將本次更動推送至 GitHub 遠端儲存庫：`git push origin main`
2. 前往 GitHub 儲存庫 `asc103138/antui` 的 **Settings** -> **Pages**。
3. 在 **Build and deployment** 下方的 **Source** 選擇 `Deploy from a branch`。
4. **Branch** 選擇 `main`，資料夾選擇 `/ (root)`，點擊 **Save**。
5. 數十秒後即可透過專屬網址公開參閱：
   👉 **`https://asc103138.github.io/antui/`**

---

## 📄 專案規範與維護

- 協作規範與開工/收工流程：請參考 [AGENTS.md](file:///d:/antui/AGENTS.md)。
- 開發進度與交接紀錄：請參考 [handoff.md](file:///d:/antui/handoff.md)。
- Obsidian 專案駕駛艙：`D:\opencode\我的筆記\antui\專案工作流程.md`。

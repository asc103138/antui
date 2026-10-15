# Antigravity MinerU 文件解析技能 - AGENTS.md

## 專案資訊
- **專案名稱**：Antigravity MinerU 文件解析技能與進階 PDF 工具包 (`antigravity-mineru`)
- **專案用途**：使用 MinerU (v4.0+) 進行高精準度多模態 PDF 與文件結構化解析（支援圖文原位對齊、跨頁表格還原、LaTeX 數學公式、OCR 文字層提取），並整合本機進階 PDF 萬用處理（合併、灰階省墨、壓縮、頁碼浮水印等）。
- **主要工作目錄**：`d:\antui\pdf技能`
- **獨立 Git 目錄**：`d:\antigravity-mineru`
- **GitHub 儲存庫**：https://github.com/asc103138/antigravity-mineru（公開 Repository）
- **母庫關聯**：`d:\antui` (https://github.com/asc103138/antui)
- **全域技能對應**：`~/.gemini/config/skills/20-mineru`、`~/.gemini/config/skills/14-advanced-docs`

## Obsidian 關聯筆記
- **Obsidian 根路徑**：`D:\opencode\我的筆記`
- **專案對應筆記**：`D:\opencode\我的筆記\antui\pdf-mineru-文件解析.md`
- **專案總覽駕駛艙**：`D:\opencode\我的筆記\antui\專案工作流程.md`

## 核心設計與安全原則
1. **100% 本機端運算（零資安外洩）**：
   - 處理校務機密公文、段考試卷、學生個資或教職員檔案時，所有模型推論與檔案解析均在本機環境執行。
   - 嚴禁將未經授權之文件或資料上傳至第三方外部伺服器或公有雲。
2. **多模態圖文對齊保證**：
   - 解析複雜排版之文件時，優先使用 MinerU 版面分析（Layout Analysis），確保圖片切片與正文段落原位對齊，杜絕插圖堆疊文末問題。
   - 表格一律轉譯為標準 Markdown / HTML 表格；數理公式轉譯為標準 LaTeX。
3. **按需隨選與虛擬環境隔離**：
   - 透過 `uv tool install mineru-kit` 管理全域 CLI，或使用 `.venv` 虛擬環境隔離 Python 套件，避免污染系統全域環境。
4. **Git 同步規範**：
   - 嚴禁硬編碼任何 API Key、Token、密碼或個資。
   - 收工時執行 `python scripts/sync_git.py "<commit_message>"`，自動將修改同步至專屬 Git 目錄（`d:\antigravity-mineru`）並推送至線上 GitHub 儲存庫，同時與母庫 `asc103138/antui` 及全域技能目錄保持同步。

# STEAM 社群活動成果表、簽到表、領據一鍵生成 Skill (`steam-community-docs`)

專為**臺中市梧棲區中正國民小學**「**臺中市115年度推動校園STEAM教育實施計畫**」教師社群打造之專屬自動化生成技能。

---

## 🌟 功能亮點

1. **依照片自動生成成果**：提供活動照片與日期，AI 自動分析照片中的智高積木組裝、天平量測與共備歷程，生成合規成果表（含活動目的、活動說明、成果亮點與照片圖說）。
2. **計畫書 8 場次自動對應**：自動比對已核可計畫書之場次規劃與主題，活動名稱與主題無縫接軌。
3. **內聘講師輪流機制**：社群成員（謝敦元、王怡婷、李仁耀、曾泊淞）輪流擔任內聘講師，確認人選後自動產生內聘講師領據與簽到表職稱標記。
4. **自動圖片排版與壓縮**：照片自動調整方向（EXIF校正）、適度壓縮後置入 Word 2欄式表格，排版俐落不破版。
5. **Word + PDF 雙格式同步產出**：產出 `.docx` 同步轉存 `.pdf`，隨開即印、立刻簽章。
6. **專屬日期目錄歸檔**：一鍵建立以日期命名的資料夾（如 `0926/`），所有文件整齊歸位。
7. **Gmail 成果信件發送與確認**：自動套用標準官方繳交範本寄送至 `tc.steam114@gmail.com`，僅夾帶《成果表》與《簽到表》，寄出前在對話中呈現完整內容經確認後才發送。

---

## 📁 檔案結構

```
steam社群申請/
├── scripts/
│   ├── generate_docs.py      # 一鍵生成腳本（支援 CLI 與 Python 呼叫）
│   ├── members.json          # 社群成員班底基本資料
│   └── sessions_plan.json    # 8 場次主題與預設目的說明
├── rdq/
│   └── RDQ-spec-steam-community-docs-20260926.md # RDQ 需求規格確認卡
├── 成果表.docx                # 原始範本
├── 簽到表範本.docx            # 原始範本
└── 領據.docx                  # 原始範本
```

全域 Skill 位置：`~/.gemini/config/skills/steam-community-docs/`

---

## 🚀 使用方式

### 方式一：在 Antigravity 對話中直接呼叫（推薦）
只要對 Antigravity 說：
> 「這是我今天（例如 09/26）活動的照片（上傳照片或指定資料夾），請幫我產生成果表、簽到表與領據。」

Antigravity 會自動：
1. 比對計畫書場次。
2. 詢問今天是由哪位社群成員輪流擔任內聘講師。
3. 分析照片內容並在對話中呈現成果大綱預覽。
4. 確認後一鍵在 `0926/` 資料夾內產出所有 Word 與 PDF 檔案！

### 方式二：在終端機執行指令
```bash
python3 scripts/generate_docs.py \
  --date 0926 \
  --time 13:00-15:00 \
  --session-num 6 \
  --lecturer "王怡婷" \
  --photos-dir "./photos"
```

---

## 💻 跨裝置與跨平台設定（Windows 11 / macOS）

當您在另一台電腦（例如學校或家中的 Windows 11 電腦）時，可直接從本 Git 儲存庫快速同步並啟用技能：

### 🪟 Windows 11 快速設定
1. 將本專案 Clone 或下載解壓縮至 Windows 電腦：
   ```cmd
   git clone https://github.com/asc103138/steam-community-docs.git
   cd steam-community-docs
   ```
2. 直接滑鼠雙擊 **`setup.bat`**（或於命令提示字元執行 `python scripts\install_skill.py`）。

3. 腳本會自動檢查 Python 套件、將 Skill 同步至 Windows 之 `%USERPROFILE%\.gemini\config\skills\steam-community-docs`，完成後即可在 Windows 11 上的 Antigravity 直接使用！

### 🍏 macOS 快速設定
1. 在終端機執行：
   ```bash
   ./setup.sh
   # 或 python3 scripts/install_skill.py
   ```
2. 系統自動完成套件檢查與 `~/.gemini/config/skills/steam-community-docs` 配置。


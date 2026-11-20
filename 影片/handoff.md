# 影片專案交接紀錄 (handoff.md)

## 已完成事項 (2026-10-16)
- [x] **讀取與安裝 `shanshiba-workflow-colab` 技能與工具鏈**：
  - 完整解析 `https://github.com/mathruffian-dot/shanshiba-workflow-colab.git` 架構（三層架構、十條核心鐵律、Colab G4 雲端算圖、BreezyVoice 台灣腔配音、五遍自審機制）。
  - 安裝全域技能 `shanshiba-drama`（AI 短劇九階段編劇）與 `blender-previs`（Blender 3D 預演與交付包）至 `C:\Users\ccps\.gemini\config\skills\`。
  - 透過 `uv tool install google-colab-cli` 安裝官方 Colab CLI（v0.7.4），並執行 `cloud/colab_cli_windows_patch.py` 完成 Windows `termios` 修補。
  - 執行 `setup/detect_hardware.py` 硬體檢測，確認本機無獨立 NVIDIA GPU，確立「本機劇本/首幀/配音/後製合成 ＋ 雲端 Colab G4 H3 生成」雙軌架構。
- [x] **完成 `d:\antui\影片` 專案初始化**：
  - 部署 `shanshiba-workflow-colab` 完整目錄（`agent/`, `cloud/`, `configs/`, `docs/`, `pipeline/`, `setup/`, `sfx/`, `templates/`, `tools/`）。
  - 建立標準規範檔：`AGENTS.md`、`ANTIGRAVITY.md`、`CLAUDE.md`、`handoff.md`。
- [x] **完成《micro:bit 8人跳繩智慧教練》2 分鐘搞笑教學影片製作（`pipeline/microbit_jumprope_coach/`）**：
  - 將 7 週 18 頁網頁教材濃縮為「三大搞笑崩潰現場 × 四大運算思維超能力」16 鏡＋片尾共 **120.0 秒（整整 2 分鐘）** 教學影片。
  - 產出完整九階段劇本與鏡表 `SCRIPT.md`、三階漏斗教材審查報告 `CURRICULUM_REVIEW.md`、山獅霸標準格式 `film.json`。
  - 產出 1080p 24fps 完整有聲教學影片 `out/cut/film_1080p.mp4` 與 720p 手機審片版 `out/cut/film_720p_phone.mp4`。

## 已完成事項 (2026-11-17)
- [x] **完成《康軒四上社會第三單元：家鄉的傳統信仰與老街》3 分鐘趣味複習影片（`pipeline/g4_social_unit3_review/`）**：
  - 讀取雲端硬碟 `G:\我的雲端硬碟\115四上期末教材\社會課習\` 之 3-1 與 3-2 課本及習作 PDF，完成三階漏斗教材審查報告 `CURRICULUM_REVIEW.md`。
  - 撰寫 22 鏡九階段劇本 `SCRIPT.md`、山獅霸標準 `film.json` 與 1080p 24fps 動態合成引擎 `build_3min_social_film.py`。
  - 完成雙角色台灣國語配音（Windows OneCore `Zhiwei` / `Yating`）、22 鏡首幀、頂部教學重點 HUD ＋ 右側社會筆記小卡、雙色 ASS 字幕、CC0 音效配樂與 10 秒金色法陣片尾，輸出 **180.0 秒（整整 3 分鐘）** 成片 `out/cut/film_1080p.mp4` 與手機版 `out/cut/film_720p_phone.mp4`。
  - 通過 `review.py` 自審（0 黑畫面、0 定格、響度 `-15.7 LUFS`、0 台詞重疊、0 台詞截斷）。

## 已完成事項 (2026-11-20)
- [x] **完成《康軒四上社會習作 P.18–21 引導習寫趣味影片》雙版本（`pipeline/g4_social_wb_p18_21/`）**：
  - 經 RDQ 需求探索四象限法確認規格並存檔 `rdq/RDQ-spec-wb-p18-21-20261120.md`（`status: confirmed`）。
  - 新增 4 張習作情境專屬 16:9 Pixar 3D 首幀，並搭配螢光筆動態圈詞動畫、3 秒課堂思考倒數提示卡（S06, S10, S12）、易錯字提醒（尊、虔、禁）與模擬習作填空框。
  - 輸出雙版本 120.0 秒 1080p 24fps 成片：`out/cut/film_guide_1080p.mp4`（課堂引導留白版）與 `out/cut/film_answer_1080p.mp4`（解答核對版），皆通過 `review.py` 自審（0 黑畫面、0 定格、`-15.8 LUFS`、0 重疊、0 截斷）。
  - **v2 雙欄大字版升級**：經 RDQ v2 規格確認（`revisions: 1`），改採「左 55% 全新本片生圖動畫＋左上單行膠囊、右 45% 48px 超大字習作白板」分割佈局，徹底解決字體太小與遮擋角色問題。

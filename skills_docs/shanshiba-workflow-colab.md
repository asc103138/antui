---
name: shanshiba-workflow-colab
description: 山獅霸的多重宇宙 AI 短片製作全套工作流（Colab 雲端 G4 / 本機雙軌版）。整合 16:9 24fps 劇本、角色定妝照（Qwen-Image 2.1）、首幀（Qwen-Image-Edit）、台灣腔配音（BreezyVoice / Edge-TTS）、MiniMax H3 影片生成（本機或 Google Colab G4 雲端）、MiniMax Music 3 配樂、金色咒印法陣片尾與五遍自動化自審（review.py）。當使用者說「山獅霸工作流」、「做 AI 短片」、「教學影片製作」、「Colab 跑 H3」、「make_film」、「shanshiba」或要將教材轉成搞笑情境短片時載入此技能。
---

# 山獅霸的多重宇宙：AI 短片與搞笑教學影片工作流 (`shanshiba-workflow-colab`)

本技能封裝自 [`mathruffian-dot/shanshiba-workflow-colab`](https://github.com/mathruffian-dot/shanshiba-workflow-colab.git)，提供從「選題 ➔ 劇本 ➔ 定妝照與首幀 ➔ 台灣國語配音 ➔ H3 影片生成（本機或 Google Colab G4）➔ 後製混音與字幕 ➔ 金色法陣片尾 ➔ 五遍自審」的端到端自動化管線。

---

## 一、全域與本機標準路徑

| 組件 | 路徑 | 說明 |
|:---|:---|:---|
| **主專案與範本庫** | `d:\antui\影片` | 完整包含 `cloud/`、`tools/`、`templates/`、`sfx/`（58 個 CC0 音效）、`pipeline/` |
| **全域工具目錄** | `C:\AI\tools`（與 `d:\antui\影片\tools` 同步） | `h3_shot.py`、`gen_image.py`、`breezyvoice_batch.py`、`fonts.py` 等 |
| **編劇子技能** | `~/.gemini/config/skills/shanshiba-drama` | 九階段編劇、16:9 橫式劇本格式、單鏡 $\le 12\text{s}$ 鏡表切分 |
| **預演子技能** | `~/.gemini/config/skills/blender-previs` | Blender 3D 空間鎖定、鏡位契約與 H3 提示詞素材包 |
| **Colab CLI** | `colab`（`uv tool install google-colab-cli`） | 已套用 `cloud/colab_cli_windows_patch.py` 解決 Windows `termios` 錯誤 |

---

## 二、山獅霸工作流十條核心鐵律（必守）

1. **H3 提示詞一律用官方六段格式**：由 `tools/h3_shot.py` 或 `make_film.py` 從 `film.json` 自動組裝，絕不手寫。
2. **預設只給首幀**：多人鏡加身份參考圖會多長出一個人；單人鏡才附定妝照。
3. **DMAD 4 步就是定稿**（`"draft": true`）：抽到滿意的直接用，不開 EasyCache。
4. **單鏡時長嚴格控制在 4–12 秒**（`24 fps`）：超過 12 秒容易漂移或自己切鏡。
5. **不說話的臉必須給靜音引導音軌**：否則 H3 角色會自己亂嘟囔。
6. **畫面上的中文一律後製疊字**：AI 生圖與 H3 畫面嚴禁內建中文字（會變亂碼），所有教學重點 HUD 字卡、程式碼積木與 ASS 字幕一律由後製腳本疊加。
7. **台灣腔配音與破音字標註**：BreezyVoice 或 Edge-TTS 台灣國語聲線（`zh-TW-YunJheNeural` / `zh-TW-HsiaoChenNeural`），念不準的多音字直接標注音（如 `連假[:ㄐㄧㄚ4]`、`怎[:ㄗㄣ3]麼辦`）。
8. **低頭或轉身再露臉必鎖尾幀**：避免轉身後換臉。
9. **先測最難一鏡再批次**：確認構圖與表演無誤再跑全片。
10. **五遍自審合格才交付**：執行 `review.py` 檢查逐鏡抽格、ASR 聽寫、雜訊、黑畫面／定格／響度（`-15.5 LUFS`，`alimiter` 必加 `level=false`）、切點明暗與台詞重疊（必須 `0` 重疊、`0` 截斷）。

---

## 三、雙軌執行模式（依硬體自動切換）

### 模式 A：本機無獨顯／快速產出教學短片（1080p 24fps 動態合成管線）
適用情境：需要在本機直接將教材（如 HTML 投影片、課文、專題）快速轉成 1～2 分鐘搞笑情境教學影片。
1. 使用 `shanshiba-drama` 撰寫 `SCRIPT.md` 與 `film.json`。
2. 調用生圖工具產出 16:9 無字首幀（`out/first/S01.png` ...）。
3. 執行 `build_2min_teaching_film.py`：
   - 自動生成台灣國語雙角色配音並裁切頭尾靜音。
   - 為每鏡渲染 Ken Burns 電影緩推／緩拉動態、頂部教學積木 HUD 字卡（遵循 Emil Kowalski 自訂 `ease-out` 曲線）與右上角即時互動模擬面板（如 micro:bit 5×5 LED 點陣）。
   - 呼叫 `templates/ending/render_ending.py` 渲染金色咒印法陣片尾。
   - 混入 `sfx/` CC0 真實音效與背景配樂（台詞期間自動壓低 Ducking 至 25%），經 EBU R128 響度正規化至 `-15.5 LUFS`，燒錄雙色 ASS 字幕，輸出 `out/cut/film_1080p.mp4` 與 `film_720p_phone.mp4`。

### 模式 B：Google Colab G4 雲端算圖（MiniMax H3 嘴型與肢體生成）
適用情境：需要將 `film.json` 送上雲端 G4（RTX PRO 6000 Blackwell 96GB）跑完整 MiniMax H3 影片與 BreezyVoice。
```powershell
# 1. 首次使用先在終端機登入 Google AI Pro 帳號
colab usage

# 2. 啟動 Colab G4 並執行雲端管線
cd d:\antui\影片
python cloud/colab_h3.py start
python cloud/colab_h3.py film pipeline/<片名資料夾> chars masters frames voices h3 amb edl music ending cut review

# 3. 驗收完成確定不再重拍後關機
python cloud/colab_h3.py stop
```

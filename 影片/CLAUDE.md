# 山獅霸的多重宇宙 × 國小資訊科技搞笑教學短片工作流

> **2026-10-16 〈甩一下跳五下？！micro:bit 跳繩智慧教練大作戰〉v1 成片與 Colab 交付包**：
> - 劇本與鏡表：[SCRIPT.md](file:///d:/antui/影片/pipeline/microbit_jumprope_coach/SCRIPT.md)
> - H3 / Colab 全自動設定檔：[film.json](file:///d:/antui/影片/pipeline/microbit_jumprope_coach/film.json)
> - 2 分鐘（120.0 秒）1080p 24fps 完整教學成片：[film_1080p.mp4](file:///d:/antui/影片/pipeline/microbit_jumprope_coach/out/cut/film_1080p.mp4)

## 專案簡介
結合 `mathruffian-dot/shanshiba-workflow-colab`（山獅霸的多重宇宙 AI 短片工作流）與臺中市梧棲區中正國小四年級資訊科技 7 週專題《micro:bit 8人跳繩智慧教練》，打造 **2 分鐘（120 秒）搞笑校園情境教學影片**。

## 影片規格
| 項目 | 設定 |
|---|---|
| 畫面比例 | 16:9 橫式 |
| 解析度 | 1920×1080 (Full HD) |
| 幀率 | 24 fps |
| 總時長 | **120.0 秒（正片 16 鏡 110.0 秒 ＋ 金色法陣片尾 10.0 秒）** |
| 單鏡長度 | 5.0–8.0 秒（嚴格遵守 ≤12 秒鐵律） |

## 必讀（開工前）
- 寫劇本：用 `shanshiba-drama` 技能。
- 預演與鏡位：用 `blender-previs` 技能。
- H3 與 Colab 雲端算圖：使用 `pipeline/microbit_jumprope_coach/film.json` 搭配 `cloud/colab_h3.py` 或 `make_film.py`。
- 本機直出合成：使用 `pipeline/microbit_jumprope_coach/build_2min_teaching_film.py`（結合 AI 分鏡繪圖、台灣國語雙角色配音、CC0 實體音效、動態積木 HUD 疊加與金色法陣片尾）。

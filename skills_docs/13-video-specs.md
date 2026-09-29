---
name: antigravity-video-specs
description: 三類影片製作規範（活動紀錄／教學影片／社群科普）與自動化工作流。說「做影片」「我要做影片」「製作教學影片」「製作科普影片」「製作活動紀錄影片」「claude-video-specs」「影片製作規範」時載入。
---

# 三類影片製作規範與工作流（claude-video-specs）

## 說明
基於 `d:\claude-video-specs` 的三類影片製作規範（SOIL 教學心法 + 林長揚簡報原則），搭配 Edge-TTS、源石黑體、HTML5/CSS 動畫、Playwright 網頁錄製與 FFmpeg 音視合成。

## 觸發情境
- 「我要做影片」/「做一支影片」
- 「做活動紀錄影片」/「做教學影片」/「做社群科普」
- 「按照規範做影片」/「啟動 claude-video-specs」

## 核心鐵律（最高安全防線，動工前必讀）
1. **嚴禁未對齊直接開工**：第一步必須先產出 `SCRIPT.md`（分鏡與字幕）與 `DESIGN.md`（視覺規範：字體/配色/字級/版面/節奏）交由使用者審查，明確確認後才能寫 code 或渲染。
2. **字幕規範**：單行 ≤ 25 字，以不換行為原則。
3. **Playwright 錄影**：
   - 依賴安裝於 `%TEMP%\cvs-render\`，避免在 GDrive 產生 node_modules。
   - 錄製使用 `?render=true` 參數自動隱藏點擊遮罩並自動播放。
4. **FFmpeg 合成**：
   - 音訊淡出使用 `st`（秒）標籤：`afade=t=out:st=<秒數>:d=<時長>`。
   - 影音合併必加 `-map 0:v:0 -map 1:a:0`，防止空白音軌覆蓋。

## 三類影片規範
- **01 活動紀錄影片**（60–180s）：口白 + 大字卡 + BGM 過場，重現當下氛圍。規範：`d:\claude-video-specs\specs\01-活動紀錄影片.md`，範本：`d:\claude-video-specs\examples\01-marathon-light\`
- **02 教學影片**（4–8 min）：SOIL 1-3 引擎 + 課堂動畫 + Edge-TTS 旁白。規範：`d:\claude-video-specs\specs\02-教學影片.md`，範本：`d:\claude-video-specs\examples\02-factors-multiples\`
- **03 社群科普影片**（2–3 min）：前 3 秒強 Hook + 多版面切換 + 照片佐證。規範：`d:\claude-video-specs\specs\03-社群科普影片.md`，範本：`d:\claude-video-specs\examples\03-ai-context\`

## 執行 5 階段流程
1. **階段 1 環境確認**：執行 `python d:\claude-video-specs\install\setup.py check`。
2. **階段 2 類型選擇**：確認欲製作的影片類型（01/02/03）。
3. **階段 3 腳本與試作**：
   - 撰寫 `SCRIPT.md` 與 `DESIGN.md` 並經使用者確認。
   - 複製範本至工作目錄。
   - 序列執行 Edge-TTS 產出旁白音訊。
   - Playwright 錄製無聲 webm。
   - FFmpeg 合成音軌與影片輸出 mp4。
4. **階段 4 調整反饋**：微調字幕、視覺、動畫節奏或素材。
5. **階段 5 定案與歸檔**。

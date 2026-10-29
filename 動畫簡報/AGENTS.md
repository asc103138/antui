# 社會教學動畫簡報 - AGENTS.md

## 專案資訊
- **專案名稱**：社會教學動畫簡報 (Social Studies Motion Deck)
- **所屬分支**：`社會教學動畫簡報`
- **主要用途**：國小四年級社會科（康軒版四上第二單元）14 頁互動式教學動畫簡報與 205 秒超高畫質 MP4 關鍵原理解說動畫系統
- **核心檔案**：
  - `index.html` / `社會二單元.html`：14 頁全互動式 HTML 教學簡報
  - `social_explainer_125s.mp4`：205.32 秒 1080p 教學原理解說動畫影片
  - `render_social_video.py`：高解析度視訊幀生成與 FFmpeg 壓制腳本
  - `test_deck_social.py`：Playwright 端到端驗收腳本
  - `自我檢測審查報告_社會二單元傳統住屋與器具.md`：三階漏斗審查報告

## Obsidian 關聯筆記
- **Vault 路徑**：`D:\opencode\我的筆記\antui\`
- **專案駕駛艙**：`D:\opencode\我的筆記\antui\社會教學動畫簡報-專案駕駛艙.md`

## 必守規則與門禁
1. **Emil Kowalski 設計工程工藝底線**：
   - 零無差別 `transition: all`。
   - 零 `scale(0)` 憑空進場。
   - 零進場 `ease-in`（全域自訂強烈曲線 `cubic-bezier(0.16, 1, 0.3, 1)`）。
   - 按鈕必備 `:active { transform: scale(0.97); }` 微縮觸感。
   - 適配 `100dvh` / `100svh`，防止行動端破版。
   - 全域 `-webkit-tap-highlight-color: transparent;` 消除點擊灰閃。
2. **全套門禁自動化檢查**：
   - 每次提交前強制執行 `python ../scripts/audit_gatekeeper.py` 與 `uv run --with playwright python test_deck_social.py`。
3. **資安守門**：
   - 嚴禁硬編碼任何 API Key、Token 或機敏金鑰。

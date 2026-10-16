# 影片專案（山獅霸工作流 Colab 版 × micro:bit 跳繩智慧教練教學影片） - AGENTS.md

## 專案資訊
- **專案名稱**：shanshiba-video-studio (`d:\antui\影片`)
- **專案用途**：以 `shanshiba-workflow-colab`（山獅霸的多重宇宙 AI 短片工作流）結合國小四年級資訊科技與體育跨域教材《micro:bit 8人跳繩智慧教練》，製作 2 分鐘（120 秒）16:9 24fps 搞笑情境教學影片。
- **主要工作目錄**：`d:\antui\影片`
- **教材來源**：`https://asc103138.github.io/html-slide-builder/microbit-jumprope-coach/`
- **核心技能**：
  - `shanshiba-drama`（AI 短劇編劇，九階段流程、16:9 劇本與 ≤12s 鏡表）
  - `blender-previs`（Blender 3D 預演、鏡位契約與提示詞包）
  - `g4-curriculum-review`（國小四年級教材三階漏斗審查機制）

## Obsidian 關聯筆記
- **Vault 路徑**：`D:\opencode\我的筆記`
- **專案駕駛艙**：`D:\opencode\我的筆記\antui\影片專案工作流程.md`

## 影片與劇本核心規格（山獅霸工作流鐵律）
1. **畫面比例與幀率**：**16:9 橫式**、**1920×1080**、**24 fps**。
2. **單鏡時長限制**：每鏡 **4–12 秒**（MiniMax H3 超過 12 秒易漂移或自切鏡）。
3. **說話與配音規範**：
   - 同一鏡同一時間**只讓一個人說話**。
   - 看得到臉但無台詞的鏡頭必須給**靜音引導音軌**（避免角色自己嘟囔）。
   - 多音字/破音字直接標注音（如 `連假[:ㄐㄧㄚ4]`）。
4. **畫面文字規範**：首幀與 AI 生成畫面禁止內建中文字（避免亂碼），所有教學重點字卡、程式碼積木與字幕**一律由後製疊加**。
5. **片尾規範**：採用 `templates/ending/render_ending.py` 標準金色咒印法陣片尾與 AI 工具揭露名單。

## 工作與安全規則
- 回應使用繁體中文（台灣）。
- 嚴格遵守母專案 `d:\antui\AGENTS.md` 之 Emil Kowalski 設計工程底線與成品一票否決檢查（`python ../scripts/audit_gatekeeper.py`）。
- 絕不 commit API Key、Token、密碼或個人隱私資料。
- **全域教材審查規範**：教學影片與腳本必須落實 `g4-curriculum-review` 三階漏斗審查（第一階課綱正確性、第二階四年級 CLT 認知負荷與單行字幕 ≤20 字、第三階「機械彈跳誤判 1下跳4下」迷思診斷與梧棲中正國小在地情境）。

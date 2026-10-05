---
name: antigravity-draw
description: AntiGravity 生圖指引（Nano Banana 2 引擎）。說「生圖」「畫圖」「產生圖片」「教材插圖」「視覺素材」時載入。
---

# 生圖指南（Nano Banana 2 / AntiGravity 版）

本技能為 AntiGravity 2 全域生圖規範，核心生圖引擎採用 **Nano Banana 2**（Google Gemini Flash Image / Imagen 3 世代架構）。
具備**極速生成**、**高指令遵循度**、**多模態圖生圖**與**角色風格一致性（Character Consistency）**。

---

## 一、生圖路線

| 路線 | 說明 | 適用情境 | 需求 |
|------|------|----------|------|
| **路線 A：AntiGravity 原生生圖（首選 / 預設）** | 呼叫內建 `generate_image` 工具（Nano Banana 2 引擎） | 對話中產圖、教材插圖、封面設計、UI 原型 | 免金鑰，吃訂閱配額池 |
| **路線 B：本機腳本生圖（備用）** | 呼叫 `draw.ps1` 腳本（免 Python、免 GPU） | 終端指令批次產圖、自動化工作流 | Windows PowerShell |
| **路線 C：開發者 API 路線** | 使用 Google GenAI SDK / Gemini API 批次產生 | 需自訂程式碼管線或大規模生成 | `GEMINI_API_KEY` |

---

## 二、路線 A：原生生圖工具標準呼叫規範

在 AntiGravity 環境中，直接調用 `generate_image` 工具：

### 工具參數規範
- **`Prompt`**：詳細影像描述（建議結構見第三節，英文構圖細節尤佳，繁中語意精確理解）。
- **`ImageName`**：全小寫加底線，最多 3 個單字（例如 `bamboo_craft_g4`, `hero_cover_banner`）。
- **`AspectRatio`**：
  - `1:1`（方形，圖標、貼紙、頭像、社群貼文）
  - `16:9`（橫幅，簡報封面、投影片底圖、YouTube 封面）
  - `9:16`（直幅，手機全螢幕背景、直式海報）
  - `4:3` / `3:4`（標準教學講義、試卷直式配圖）
  - `3:2` / `2:3`（相片標準比例）
- **`ImagePaths`**（可選）：最多傳入 3 個本機圖片絕對路徑，用於**以圖生圖**、**風格參考**或**保持角色外觀一致性**。

---

## 三、Nano Banana 2 專用提示詞模組與四大範本

### 建議提示詞結構
```
生成一張圖片：
用途：[如：國小四年級考卷插圖 / 簡報背景 / 教材圖標]
尺寸比例：[1:1 / 16:9 / 4:3 等]
主體與主題：[畫面核心角色、物體、動作]
背景與環境：[環境氛圍、光線、留白區域]
風格細節：[黑白線稿 / 3D 全息 / 極簡向量扁平 / 寫實攝影]
色彩規範：[純黑白 / 暗色霓虹漸層 / 柔和教育系粉彩]
禁止元素（Negative）：[無漸層、無陰影、無文字、無外框等]
輸出路徑：[如：assets/exam_images/xxx.png]
```

---

### 範本 1：學校試卷情境插圖（高對比黑白向量線稿）
> **教學專用鐵律**：適合學校黑白影印機複印，避免灰階雜點。
```
Prompt:
High-contrast black and white vector line art illustration for elementary school worksheet.
Pure white background, clean black outlines only, zero shading, no gradients, no grey tones, no screentone, no textures.
Subject: [一位國小學生與老爺爺一起在戶外編織竹簍，桌上放著竹條與工具].
Clear composition, educational and friendly style, sharp contours suitable for black-and-white photocopy.
```

---

### 範本 2：教材與簡報 16:9 封面 / 全息背景
> **簡報專用**：大量負空間（留白）供標題與內文排版。
```
Prompt:
A modern 16:9 widescreen educational presentation background, dark neon cyber-minimalist style.
Deep indigo and navy gradient backdrop with subtle glowing geometric wireframe patterns and soft particle light effects.
Generous empty negative space in the center and left for text overlay.
Clean, professional, high-end 3D holographic aesthetic, 8K resolution feel, no text, no letters.
```

---

### 範本 3：扁平化教學圖標（Flat Icon / Sticker）
> **圖標專用**：純色背景便於 Pillow 自動去背與裁切。
```
Prompt:
Single isolated flat vector icon of [a green leaf with water drop representing water conservation],
minimalist sticker style, bold outlines, vibrant flat colors, isolated on pure solid white background (#FFFFFF).
Centered composition, no shadows, no complex background, suitable for easy background removal.
```

---

### 範本 4：連續故事與角色一致性（Character Consistency）
若需產出多張具有相同主角的漫畫、繪本或情境圖：
1. **第一步（先產角色設定卡）**：
   ```
   Prompt: Character model sheet of [an 10-year-old Taiwanese boy named Xiao-Ming, wearing yellow school uniform, round glasses, messy black hair, dynamic poses: front, side, back view], pure white background, consistent character design.
   ```
2. **第二步（後續分鏡帶入參考圖）**：
   呼叫 `generate_image` 時，將第一步生成的設定圖路徑傳入 `ImagePaths: ["C:/.../char_sheet.png"]`，並在 Prompt 中說明：「Maintain exact same character features, clothes, hair from reference image, in [new action/scene]」。

---

## 四、鐵則與限制

1. **圖中文字一律走後製**：
   - Nano Banana 2 雖具備基本文字能力，但**複雜繁體中文漢字極易失真或生出錯別字**。
   - **鐵則**：生圖時明確要求「no text, no watermark」，產出無文字底圖後，再透過前端 CSS、PowerPoint、Canva 或 Pillow 腳本疊加清晰向量文字。
2. **UI 原型生圖嚴禁周邊裝置框**：
   - 產生使用者介面（UI）設計稿時，僅生成介面本身，**切勿包覆筆電螢幕外殼或手機金屬邊框**（No device frames），除非使用者特別要求。
3. **檔案存放規範**：
   - 考卷插圖一律存放至 `assets/exam_images/` 或專案 `assets/`。
   - 簡報封面存放至 `assets/covers/`。
   - 生成完成後回報可點擊之 Markdown 相對或絕對檔案連結。
4. **機敏資訊隔離**：
   - 嚴禁將任何 API Key 寫入公開程式碼、專案文件或 Git commit 歷史中。

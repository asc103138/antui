---
name: antigravity-sheets-gas
description: 用 Google 試算表當資料庫、Apps Script 網頁應用程式當後端，讓網頁作品「關掉還記得住」。零安裝、不用 clasp、不用 Node。內建 Emil Kowalski 全套設計工程與行動原生前端標準（流體極光背景、Apple Pro 卡片、44px 觸控熱區、Sonner 級 Toast）。說「用試算表存資料」「GAS 後端」「表單收資料」「讓網頁能存東西」「做課堂回饋牆」「做線上報名表」「GAS 網站設計」「GAS 網頁應用」時載入。
---

# Google 試算表 ＋ Apps Script 網頁應用程式 (GAS Web App)

## 核心優勢
- **全程零安裝**：不用 clasp、不用 Node.js，直接在瀏覽器與本機完成。
- **學校帳號友善**：老師自己的內部腳本不受網管 `admin_policy_enforced` 限制。
- **改版網址不變**：更新版本無需重新產製 QR Code 或通知使用者。
- **起步即頂級工藝**：**全面以 Emil Kowalski 設計工程全套標準為最低底線**，杜絕死板粗糙的老舊表單，預設交付具備 Apple 旗艦空間感與流體動態的高級 Web App。

---

## 🎨 GAS 前端網頁設計工程全套工藝標準 (Design Engineering Baseline)
凡透過本技能生成的任何 GAS 網頁（如課堂回饋牆、活動簽到系統、線上報名表、儀表板、互動小工具），**強制以 Emil Kowalski 設計工程規範為及格底線**，嚴格遵守以下 6 大維度：

### 1. 空間環境微光與流體極光背景 (Spatial Ambient Fluid Aurora)
- **拒絕純白死灰死板背景**：全面植入純 CSS GPU 合成層加速之流體光島（`will-change: transform`，零 Reflow 耗能）。
- **呼吸式有機流動**：結合互質非整數倍週期（22s / 28s / 25s）三大光島與微型點陣紋理（`spatial-grid-pattern`），營造 Apple 空間運算立體縱深。
- **日夜雙主題無縫適配**：夜間 OLED 純黑搭配深海藍/鈦金微光；日間陶瓷白搭配柔和晨曦金。

### 2. 行動端原生體驗鐵律 (Mobile Native)
- **視窗高度鎖定 `100dvh`**：外層容器與彈窗嚴禁死板 `100vh`（會受 Safari / Chrome 動態網址列遮擋破版），必須使用 `min-height: 100dvh`。
- **輸入框防放大**：所有 `<input>`、`<textarea>`、`<select>` 字體大小**最低強制 16px**（`font-size: max(16px, 1rem)`），徹底杜絕 iOS 聚焦時畫面暴衝放大的災難。
- **消除點擊藍灰高亮**：全域加入 `* { -webkit-tap-highlight-color: transparent; }`。
- **按鈕防文字選取**：所有按鈕標配 `user-select: none; -webkit-user-select: none;`。

### 3. 觸覺微互動與 44px 觸控熱區 (Tactile Micro-interactions)
- **按鈕按下必備反饋**：所有按鈕、標籤與卡片必備 `:active { transform: scale(0.96~0.97); }`。
- **符合 Apple HIG 熱區**：主要按鈕高度至少 `42px ~ 44px`，拇指點擊輕鬆命中。
- **高感知效能 (Perceived Performance)**：按鈕點擊後即刻呈現狀態過渡，提交按鈕在等待 GAS 後端時呈現極速流暢 Spinner，禁止介面假死。

### 4. 嚴格動態曲線與物理定律 (Physics & Easing)
- **全面消滅 `transition: all`**：精確限定過渡屬性（`transform, opacity, box-shadow`）。
- **進場曲線**：嚴禁使用遲鈍的 `ease-in`，一律使用強烈自訂曲線 `--ease-out: cubic-bezier(0.23, 1, 0.32, 1)`。
- **嚴禁從 `scale(0)` 憑空出現**：卡片與彈窗進場起點為 `scale(0.96) translateY(12px)`。

### 5. Sonner 規格浮動膠囊 Toast 通知
- 嚴禁使用瀏覽器古老死板的 `alert()` 或 `confirm()`。
- 資料送出成功或發生錯誤時，一律以 Sonner 規格的浮動膠囊 Toast 提示（微距 14px 彈入，200ms 就位，手機端自適應居中）。

---

## 🛠️ 標準 GAS 前端頂級樣式庫範本 (Copy-and-Paste Standard)

當生成 GAS 網頁時，直接套用此高工藝標準樣式架構：

```html
<!DOCTYPE html>
<html lang="zh-TW" data-theme="dark">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0, viewport-fit=cover">
  <title>GAS Web App</title>
  <style>
    :root {
      --ease-out: cubic-bezier(0.23, 1, 0.32, 1);
      --page-bg: #000000;
      --page-surface: #121215;
      --page-surface-strong: #1a1a1f;
      --page-border: rgba(255, 255, 255, 0.12);
      --page-text: #f5f5f7;
      --page-muted: #86868b;
      --accent-blue: #2997ff;
      --accent-gold: #e4c988;
      --radius-sm: 10px;
      --radius-md: 18px;
      --radius-full: 9999px;
    }

    [data-theme="light"] {
      --page-bg: #f5f5f7;
      --page-surface: #ffffff;
      --page-surface-strong: #ffffff;
      --page-border: rgba(0, 0, 0, 0.08);
      --page-text: #1d1d1f;
      --page-muted: #86868b;
      --accent-blue: #0071e3;
      --accent-gold: #c5a059;
    }

    *, *::before, *::after {
      box-sizing: border-box;
      margin: 0;
      padding: 0;
      -webkit-tap-highlight-color: transparent;
    }

    body {
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Noto Sans TC", sans-serif;
      background-color: var(--page-bg);
      color: var(--page-text);
      min-height: 100dvh;
      min-height: 100vh;
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      padding: 24px 16px;
      position: relative;
      overflow-x: hidden;
    }

    /* 背景空間流體極光 (Apple Spatial Fluid Aurora) */
    .spatial-bg-mesh {
      position: fixed;
      inset: 0;
      pointer-events: none;
      z-index: -1;
      overflow: hidden;
      contain: strict;
    }

    .spatial-orb {
      position: absolute;
      border-radius: 50%;
      filter: blur(85px);
      -webkit-filter: blur(85px);
      will-change: transform;
      opacity: 0.7;
    }

    .orb-1 {
      top: -10vh;
      left: 10vw;
      width: 55vw;
      height: 55vw;
      max-width: 600px;
      max-height: 600px;
      background: radial-gradient(circle, rgba(41, 151, 255, 0.2) 0%, transparent 70%);
      animation: drift-1 22s cubic-bezier(0.45, 0, 0.55, 1) infinite alternate;
    }

    .orb-2 {
      bottom: -10vh;
      right: 5vw;
      width: 50vw;
      height: 50vw;
      max-width: 550px;
      max-height: 550px;
      background: radial-gradient(circle, rgba(228, 201, 136, 0.16) 0%, transparent 70%);
      animation: drift-2 26s cubic-bezier(0.45, 0, 0.55, 1) infinite alternate;
    }

    @keyframes drift-1 {
      0% { transform: translate3d(0, 0, 0) scale(1); }
      100% { transform: translate3d(8vw, 12vh, 0) scale(1.12); }
    }

    @keyframes drift-2 {
      0% { transform: translate3d(0, 0, 0) scale(1); }
      100% { transform: translate3d(-10vw, -10vh, 0) scale(1.15); }
    }

    /* Apple Squircle 卡片容器 */
    .app-card {
      background: var(--page-surface);
      border: 1px solid var(--page-border);
      border-radius: 22px;
      width: 100%;
      max-width: 540px;
      padding: 32px 28px;
      box-shadow: 0 16px 40px rgba(0, 0, 0, 0.4);
      transform: scale(0.97) translateY(10px);
      opacity: 0;
      animation: card-enter 240ms var(--ease-out) forwards;
    }

    @keyframes card-enter {
      to { transform: scale(1) translateY(0); opacity: 1; }
    }

    /* 表單元件：杜絕 iOS 縮放 */
    .form-group {
      margin-bottom: 20px;
    }

    .form-label {
      display: block;
      font-size: 0.88rem;
      font-weight: 600;
      color: var(--page-muted);
      margin-bottom: 8px;
    }

    .form-input, .form-textarea {
      width: 100%;
      font-size: 16px; /* 鐵律：最低 16px 杜絕 iOS 縮放 */
      font-family: inherit;
      background: rgba(255, 255, 255, 0.05);
      border: 1px solid var(--page-border);
      border-radius: var(--radius-sm);
      color: var(--page-text);
      padding: 12px 16px;
      outline: none;
      transition: border-color 150ms ease, box-shadow 150ms ease;
    }

    .form-input:focus, .form-textarea:focus {
      border-color: var(--accent-blue);
      box-shadow: 0 0 0 3px rgba(41, 151, 255, 0.2);
    }

    /* Action 按鈕：42px 觸摸熱區 + :active 微縮 */
    .btn-submit {
      width: 100%;
      min-height: 44px;
      background: var(--accent-blue);
      color: #ffffff;
      font-size: 0.95rem;
      font-weight: 650;
      border: none;
      border-radius: var(--radius-full);
      cursor: pointer;
      display: inline-flex;
      align-items: center;
      justify-content: center;
      gap: 8px;
      user-select: none;
      -webkit-user-select: none;
      transition: transform 140ms var(--ease-out), box-shadow 150ms ease;
      box-shadow: 0 4px 14px rgba(41, 151, 255, 0.35);
    }

    .btn-submit:active {
      transform: scale(0.96);
    }

    /* Sonner 規格浮動膠囊 Toast */
    .toast {
      position: fixed;
      bottom: 24px;
      background: #1a1a1f;
      color: #f5f5f7;
      border: 1px solid rgba(255, 255, 255, 0.15);
      padding: 12px 22px;
      border-radius: var(--radius-full);
      font-size: 0.92rem;
      font-weight: 600;
      box-shadow: 0 12px 32px rgba(0, 0, 0, 0.45);
      z-index: 9999;
      transform: translateY(14px) scale(0.96);
      opacity: 0;
      pointer-events: none;
      transition: transform 220ms var(--ease-out), opacity 180ms var(--ease-out);
    }

    .toast.show {
      transform: translateY(0) scale(1);
      opacity: 1;
    }
  </style>
</head>
<body>
  <div class="spatial-bg-mesh" aria-hidden="true">
    <div class="spatial-orb orb-1"></div>
    <div class="spatial-orb orb-2"></div>
  </div>

  <div class="app-card">
    <!-- 內容與表單 -->
  </div>

  <div id="toast" class="toast"></div>
</body>
</html>
```

---

## 後端開發與部署流程

### 步驟一：建立 Google 試算表
1. 建立新試算表，設定工作表名稱（例如 `data`）。
2. 在第 1 列建立欄位標題（例如：`timestamp`、`name`、`feedback`）。

### 步驟二：開啟 Apps Script
點選選單「**擴充功能**」→「**Apps Script**」。

### 步驟三：編寫後端程式碼（範例）
```javascript
function doGet(e) {
  const sheet = SpreadsheetApp.getActiveSpreadsheet().getSheetByName("data");
  const rows = sheet.getDataRange().getValues();
  const headers = rows.shift();
  const data = rows.map(row => {
    let obj = {};
    headers.forEach((h, i) => obj[h] = row[i]);
    return obj;
  });
  return ContentService.createTextOutput(JSON.stringify(data))
    .setMimeType(ContentService.MimeType.JSON);
}

function doPost(e) {
  try {
    const sheet = SpreadsheetApp.getActiveSpreadsheet().getSheetByName("data");
    const payload = JSON.parse(e.postData.contents);
    sheet.appendRow([new Date(), payload.name, payload.feedback]);
    return ContentService.createTextOutput(JSON.stringify({ status: "success" }))
      .setMimeType(ContentService.MimeType.JSON);
  } catch (err) {
    return ContentService.createTextOutput(JSON.stringify({ status: "error", message: err.message }))
      .setMimeType(ContentService.MimeType.JSON);
  }
}
```

### 步驟四：部署為網頁應用程式
1. 點擊右上角「**部署**」→「**新增部署作業**」。
2. 種類選擇「**網頁應用程式**」。
3. 設定：
   - **執行身分**：我 (Me)
   - **誰可以存取**：所有人 (Anyone)
4. 點擊「部署」，授權存取後複製「**網頁應用程式網址**」。

### 步驟五：前端串接（JavaScript）
```javascript
const GAS_URL = "你的網頁應用程式網址";

// 讀取資料
async function loadData() {
  const res = await fetch(GAS_URL);
  const data = await res.json();
  return data;
}

// 寫入資料
async function sendData(payload) {
  const res = await fetch(GAS_URL, {
    method: "POST",
    body: JSON.stringify(payload)
  });
  return await res.json();
}
```

### 步驟六：更新與改版（維持同一網址）
若修改程式碼：
1. 點選「**部署**」→「**管理部署作業**」。
2. 點擊鉛筆圖示（編輯）。
3. 「版本」選「**新版本**」。
4. 點擊「**部署**」。網址將維持不變！


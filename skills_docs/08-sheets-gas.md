---
name: antigravity-sheets-gas
description: 用 Google 試算表當資料庫、Apps Script 網頁應用程式當後端，讓網頁作品「關掉還記得住」。零安裝、不用 clasp、不用 Node。說「用試算表存資料」「GAS 後端」「表單收資料」「讓網頁能存東西」「做課堂回饋牆」「做線上報名表」時載入。
---

# Google 試算表 ＋ Apps Script 網頁應用程式

## 核心優勢
- **全程零安裝**：不用 clasp、不用 Node.js，直接在瀏覽器完成。
- **學校帳號友善**：老師自己的內部腳本不受網管 `admin_policy_enforced` 限制。
- **改版網址不變**：更新版本無需重新產製 QR Code 或通知使用者。

---

## 開發與部署流程

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
  console.log(data);
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

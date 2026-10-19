// test_deck.mjs - Playwright 端到端實體瀏覽器渲染驗證腳本（前三段內容深究 14 頁專屬）
import { chromium } from "playwright";
import { pathToFileURL } from "url";
import path from "path";
import fs from "fs";

async function run() {
  const baseDir = path.resolve(".");
  const indexHtml = path.join(baseDir, "index.html");
  const rendersDir = path.join(baseDir, "renders");
  if (!fs.existsSync(rendersDir)) fs.mkdirSync(rendersDir, { recursive: true });

  console.log("🚀 啟動 Playwright 實機瀏覽器渲染驗收（前三段內容深究版本）...");
  const errors = [];

  const browser = await chromium.launch({ headless: true });
  const context = await browser.newContext({ viewport: { width: 1920, height: 1080 } });
  const page = await context.newPage();

  page.on("console", (msg) => {
    if (msg.type() === "error") {
      errors.push(`[Console Error] ${msg.text()}`);
    }
  });

  page.on("pageerror", (err) => {
    errors.push(`[Unhandled Error] ${err.message}`);
  });

  const fileUrl = pathToFileURL(indexHtml).href;
  await page.goto(fileUrl, { waitUntil: "networkidle" });

  // 1. 截圖 Slide 1 (封面)
  const p1Shot = path.join(rendersDir, "deck_slide1_deepdive.png");
  await page.screenshot({ path: p1Shot });
  console.log(`📸 Slide 1 截圖完成: ${p1Shot}`);

  // 2. 切換至 Slide 6 (關鍵頁：前三段原理解說動畫)
  await page.evaluate(() => goToSlide(6));
  await page.waitForTimeout(600);
  const p6Shot = path.join(rendersDir, "deck_slide6_video.png");
  await page.screenshot({ path: p6Shot });
  console.log(`📸 Slide 6 (前三段動畫關鍵頁) 截圖完成: ${p6Shot}`);

  const videoSrc = await page.$eval("#explainer-video source", (el) => el.getAttribute("src"));
  console.log(`🎬 Slide 6 影片標籤驗證: src = ${videoSrc}`);

  // 3. 切換至 Slide 14 (終極思辨檢測)
  await page.evaluate(() => goToSlide(14));
  await page.waitForTimeout(400);

  // 點擊選項 C (「又遠又近」哲思觀點)
  await page.click(".quiz-option:nth-child(3)");
  await page.waitForTimeout(300);
  const feedback = await page.innerText("#quiz-feedback");
  console.log(`🎯 終極思辨反饋: ${feedback}`);

  if (!feedback.includes("讀懂了課文標題的靈魂")) {
    throw new Error("終極思辨反饋未正確顯示！");
  }

  const p14Shot = path.join(rendersDir, "deck_slide14_quiz.png");
  await page.screenshot({ path: p14Shot });
  console.log(`📸 Slide 14 (終極思辨互動) 截圖完成: ${p14Shot}`);

  await browser.close();

  if (errors.length > 0) {
    console.error(`❌ 發現瀏覽器執行期錯誤 (${errors.length} 個):`);
    errors.forEach((e) => console.error("  ", e));
    process.exit(1);
  } else {
    console.log("✅ [PERFECT PASS] 瀏覽器實體渲染 0 控制台錯誤，端到端互動全部合格！");
  }
}

run().catch((err) => {
  console.error("Test failed:", err);
  process.exit(1);
});

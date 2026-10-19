// test_deck.mjs - Playwright 端到端實體瀏覽器渲染驗證腳本
import { chromium } from "playwright";
import { pathToFileURL } from "url";
import path from "path";
import fs from "fs";

async function run() {
  const baseDir = path.resolve(".");
  const indexHtml = path.join(baseDir, "index.html");
  const rendersDir = path.join(baseDir, "renders");
  if (!fs.existsSync(rendersDir)) fs.mkdirSync(rendersDir, { recursive: true });

  console.log("🚀 啟動 Playwright 實機瀏覽器渲染驗收...");
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
  const p1Shot = path.join(rendersDir, "deck_slide1_cover.png");
  await page.screenshot({ path: p1Shot });
  console.log(`📸 Slide 1 截圖完成: ${p1Shot}`);

  // 2. 切換至 Slide 5 (關鍵頁：原理解說動畫)
  await page.evaluate(() => goToSlide(5));
  await page.waitForTimeout(600);
  const p5Shot = path.join(rendersDir, "deck_slide5_video.png");
  await page.screenshot({ path: p5Shot });
  console.log(`📸 Slide 5 (動畫關鍵頁) 截圖完成: ${p5Shot}`);

  const videoSrc = await page.$eval("#explainer-video source", (el) => el.getAttribute("src"));
  console.log(`🎬 Slide 5 影片標籤驗證: src = ${videoSrc}`);

  // 3. 切換至 Slide 11 (隨堂測驗)
  await page.evaluate(() => goToSlide(11));
  await page.waitForTimeout(400);

  // 點擊正確選項 B
  await page.click(".quiz-option:nth-child(2)");
  await page.waitForTimeout(300);
  const feedback = await page.innerText("#quiz-feedback");
  console.log(`🎯 測驗互動反饋: ${feedback}`);

  if (!feedback.includes("回答完全正確")) {
    throw new Error("測驗反饋未正確顯示！");
  }

  const p11Shot = path.join(rendersDir, "deck_slide11_quiz.png");
  await page.screenshot({ path: p11Shot });
  console.log(`📸 Slide 11 (測驗互動) 截圖完成: ${p11Shot}`);

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

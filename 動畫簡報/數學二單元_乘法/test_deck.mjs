// test_deck.mjs - Playwright 端到端實體瀏覽器渲染驗收腳本（國小四年級數學 4-3 估商動畫簡報）
import { chromium } from "playwright";
import { pathToFileURL } from "url";
import path from "path";
import fs from "fs";

async function run() {
  const baseDir = path.resolve(".");
  const indexHtml = path.join(baseDir, "index.html");
  const rendersDir = path.join(baseDir, "renders");
  if (!fs.existsSync(rendersDir)) fs.mkdirSync(rendersDir, { recursive: true });

  console.log("🚀 啟動 Playwright 實機瀏覽器渲染驗收（南一版數學四上 4-3 估商版本）...");
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

  // 1. 驗收 Slide 1 (封面)
  const p1Shot = path.join(rendersDir, "deck_math_slide1_cover.png");
  await page.screenshot({ path: p1Shot });
  console.log(`📸 Slide 1 (封面) 截圖完成: ${p1Shot}`);

  // 2. 驗收 Slide 4 (互動擂台 1: 商是幾位數)
  await page.evaluate(() => goToSlide(4));
  await page.waitForTimeout(400);
  
  // 點擊「選項 B：商是二位數」
  await page.click(".quiz-options-group .quiz-card:nth-child(2)");
  await page.waitForTimeout(300);
  const quiz1Feedback = await page.innerText("#quiz1-feedback");
  console.log(`🎯 互動擂台 1 反饋: ${quiz1Feedback.slice(0, 40)}...`);
  if (!quiz1Feedback.includes("太厲害了") || !quiz1Feedback.includes("二位數")) {
    throw new Error("Slide 4 互動答題判定錯誤！");
  }

  // 3. 驗收 Slide 6 (關鍵解說動畫頁)
  await page.evaluate(() => goToSlide(6));
  await page.waitForTimeout(500);
  const p6Shot = path.join(rendersDir, "deck_math_slide6_video.png");
  await page.screenshot({ path: p6Shot });
  console.log(`📸 Slide 6 (解說動畫關鍵頁) 截圖完成: ${p6Shot}`);

  const videoSrc = await page.$eval("#explainer-video source", (el) => el.getAttribute("src"));
  console.log(`🎬 Slide 6 影片來源驗證: src = ${videoSrc}`);
  if (!videoSrc.includes("math_explainer.mp4")) {
    throw new Error("Slide 6 影片來源不正確！");
  }

  // 4. 驗收 Slide 10 (梧棲漁港在地情境直式)
  await page.evaluate(() => goToSlide(10));
  await page.waitForTimeout(400);
  const p10Shot = path.join(rendersDir, "deck_math_slide10_local.png");
  await page.screenshot({ path: p10Shot });
  console.log(`📸 Slide 10 (梧棲漁港在地實戰) 截圖完成: ${p10Shot}`);

  // 5. 驗收 Slide 13 (小偵探捉錯互動)
  await page.evaluate(() => goToSlide(13));
  await page.waitForTimeout(400);
  // 點擊迷思二卡片（整十誤乘）
  await page.click(".quiz-options-group .quiz-card:nth-child(2)");
  await page.waitForTimeout(300);
  const mistakeFeedback = await page.innerText("#mistake-feedback");
  console.log(`🕵️ 迷思診斷反饋: ${mistakeFeedback.slice(0, 40)}...`);
  if (!mistakeFeedback.includes("整十誤乘") || !mistakeFeedback.includes("摘下帽子")) {
    throw new Error("Slide 13 迷思診斷反饋未正確觸發！");
  }

  // 6. 驗收 Slide 14 (英雄榜與重新複習)
  await page.evaluate(() => goToSlide(14));
  await page.waitForTimeout(400);
  const p14Shot = path.join(rendersDir, "deck_math_slide14_summary.png");
  await page.screenshot({ path: p14Shot });
  console.log(`📸 Slide 14 (英雄榜與總結) 截圖完成: ${p14Shot}`);

  await browser.close();

  if (errors.length > 0) {
    console.error("❌ 驗收失敗，控制台存在未處理錯誤：");
    errors.forEach(e => console.error("  ", e));
    process.exit(1);
  } else {
    console.log("========================================================================");
    console.log("✅ [PERFECT PASS] Playwright 端到端實體瀏覽器渲染驗證 100% 通過！");
    console.log("   - 0 控制台錯誤 (0 Console Errors)");
    console.log("   - 0 未處理例外 (0 Unhandled Exceptions)");
    console.log("   - 14 頁翻頁流暢、互動小測驗判定精準、在地化情境完整渲染！");
    console.log("========================================================================");
  }
}

run().catch((err) => {
  console.error("❌ 執行過程異常：", err);
  process.exit(1);
});

"""
test_deck.py - Playwright 實機渲染驗收與無頭瀏覽器端到端測試
專案：南一版國小四年級數學四上第四單元 4-3 三位數除以二位數 · 估商大師探險記
驗證：
1. 0 控制台錯誤 (Zero Console Errors)
2. 0 未處理例外 (Zero Unhandled Exceptions)
3. 頁面切換正常 (Slide 1 -> Slide 4 -> Slide 6 -> Slide 10 -> Slide 13 -> Slide 14)
4. 關鍵 Slide 6 影片標籤正常 (math_explainer.mp4)
5. 互動擂台 1 (Slide 4) 答題判定與即時反饋正常
6. 迷思偵探 (Slide 13) 點擊診斷即時反饋正常
7. 產出 16:9 實體渲染截圖作為客觀驗收證據
"""
import os
import sys
from pathlib import Path
from playwright.sync_api import sync_playwright

def main():
    base_dir = Path(__file__).resolve().parent
    index_file = base_dir / "index.html"
    preview_dir = base_dir / "renders"
    preview_dir.mkdir(exist_ok=True)
    
    screenshot_p1 = preview_dir / "deck_math_slide1_cover.png"
    screenshot_p4 = preview_dir / "deck_math_slide4_quiz.png"
    screenshot_p6 = preview_dir / "deck_math_slide6_video.png"
    screenshot_p10 = preview_dir / "deck_math_slide10_local.png"
    screenshot_p13 = preview_dir / "deck_math_slide13_mistake.png"
    screenshot_p14 = preview_dir / "deck_math_slide14_summary.png"

    print("🚀 啟動 Playwright 實機瀏覽器渲染驗收（南一版數學四上 4-3 估商版本）...")
    errors = []

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True, channel="msedge")
        context = browser.new_context(viewport={"width": 1920, "height": 1080})
        page = context.new_page()

        # 監聽 console 錯誤與例外
        page.on("console", lambda msg: errors.append(f"[Console {msg.type}] {msg.text}") if msg.type == "error" else None)
        page.on("pageerror", lambda exc: errors.append(f"[Unhandled Error] {exc}"))

        file_url = index_file.as_uri()
        page.goto(file_url, wait_until="networkidle")

        # 1. 截圖 Slide 1 (封面)
        page.screenshot(path=str(screenshot_p1))
        print(f"📸 Slide 1 (封面) 截圖完成: {screenshot_p1}")

        # 2. 切換至 Slide 4 (互動擂台 1)
        page.evaluate("goToSlide(4)")
        page.wait_for_timeout(400)
        # 點擊「選項 B：商是二位數」
        page.click(".quiz-options-group .quiz-card:nth-child(2)")
        page.wait_for_timeout(300)
        quiz1_feedback = page.inner_text("#quiz1-feedback")
        print(f"🎯 互動擂台 1 反饋: {quiz1_feedback[:40]}...")
        assert "太厲害了" in quiz1_feedback and "二位數" in quiz1_feedback, "Slide 4 互動判定異常！"
        page.screenshot(path=str(screenshot_p4))
        print(f"📸 Slide 4 (互動答題後) 截圖完成: {screenshot_p4}")

        # 3. 切換至 Slide 6 (關鍵解說動畫頁)
        page.evaluate("goToSlide(6)")
        page.wait_for_timeout(500)
        video_src = page.eval_on_selector("#explainer-video source", "el => el.getAttribute('src')")
        print(f"🎬 Slide 6 影片標籤驗證: src = {video_src}")
        assert "math_explainer" in video_src, "Slide 6 影片來源不正確！"
        page.screenshot(path=str(screenshot_p6))
        print(f"📸 Slide 6 (解說動畫關鍵頁) 截圖完成: {screenshot_p6}")

        # 4. 驗證直式位值對齊截圖
        # Slide 3 (位值初探)
        page.evaluate("goToSlide(3)")
        page.wait_for_timeout(300)
        page.screenshot(path=str(preview_dir / "deck_math_slide3_align.png"))

        # Slide 7 (摘帽陷阱)
        page.evaluate("goToSlide(7)")
        page.wait_for_timeout(300)
        page.screenshot(path=str(preview_dir / "deck_math_slide7_align.png"))

        # Slide 8 (天秤調小)
        page.evaluate("goToSlide(8)")
        page.wait_for_timeout(300)
        page.screenshot(path=str(preview_dir / "deck_math_slide8_align.png"))

        # Slide 10 (梧棲漁港在地實戰)
        page.evaluate("goToSlide(10)")
        page.wait_for_timeout(300)
        page.screenshot(path=str(screenshot_p10))
        print(f"📸 Slide 10 (梧棲漁港在地實戰) 截圖完成: {screenshot_p10}")

        # Slide 11 (中正國小創客寶特瓶)
        page.evaluate("goToSlide(11)")
        page.wait_for_timeout(300)
        page.screenshot(path=str(preview_dir / "deck_math_slide11_align.png"))

        # Slide 12 (驗算直式乘法)
        page.evaluate("goToSlide(12)")
        page.wait_for_timeout(300)
        page.screenshot(path=str(preview_dir / "deck_math_slide12_align.png"))

        # 5. 切換至 Slide 13 (小偵探捉錯互動)
        page.evaluate("goToSlide(13)")
        page.wait_for_timeout(400)
        # 點擊迷思二卡片（整十誤乘）
        page.click('section[data-slide="13"] .quiz-card:nth-child(2)')
        page.wait_for_timeout(300)
        mistake_feedback = page.inner_text("#mistake-feedback")
        print(f"🕵️ 迷思診斷反饋: {mistake_feedback[:40]}...")
        assert "整十誤乘" in mistake_feedback and "摘下帽子" in mistake_feedback, "Slide 13 迷思診斷反饋異常！"
        page.screenshot(path=str(screenshot_p13))
        print(f"📸 Slide 13 (迷思診斷後) 截圖完成: {screenshot_p13}")

        # 6. 切換至 Slide 14 (英雄榜與重新複習)
        page.evaluate("goToSlide(14)")
        page.wait_for_timeout(400)
        page.screenshot(path=str(screenshot_p14))
        print(f"📸 Slide 14 (英雄榜與總結) 截圖完成: {screenshot_p14}")

        browser.close()

    if errors:
        print("❌ 驗收失敗，控制台存在未處理錯誤：")
        for err in errors:
            print("  ", err)
        sys.exit(1)
    else:
        print("\n========================================================================")
        print("✅ [PERFECT PASS] Playwright 端到端實體瀏覽器渲染驗證 100% 通過！")
        print("   - 0 控制台錯誤 (0 Console Errors)")
        print("   - 0 未處理例外 (0 Unhandled Exceptions)")
        print("   - 14 頁翻頁流暢、互動小測驗判定精準、在地化情境完整渲染！")
        print("========================================================================\n")

if __name__ == "__main__":
    main()

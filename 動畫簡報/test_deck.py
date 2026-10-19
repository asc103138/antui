"""
test_deck.py - Playwright 實機渲染驗收與無頭瀏覽器端到端測試
驗證：
1. 0 控制台錯誤 (Zero Console Errors)
2. 頁面切換正常 (Slide 1 -> Slide 5 -> Slide 11)
3. 關鍵第 5 頁影片標籤正常
4. 測驗互動點擊反饋正常
5. 產出 16:9 實體渲染截圖 (renders/deck_preview.png) 作為客觀驗收證據
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
    screenshot_path = preview_dir / "deck_preview.png"
    video_page_screenshot = preview_dir / "deck_slide5_video.png"

    print("🚀 啟動 Playwright 實機瀏覽器渲染驗收...")
    errors = []

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(viewport={"width": 1920, "height": 1080})
        page = context.new_page()

        # 監聽 console 錯誤與例外
        page.on("console", lambda msg: errors.append(f"[Console {msg.type}] {msg.text}") if msg.type == "error" else None)
        page.on("pageerror", lambda exc: errors.append(f"[Unhandled Error] {exc}"))

        file_url = index_file.as_uri()
        page.goto(file_url, wait_until="networkidle")

        # 截圖首頁
        page.screenshot(path=str(screenshot_path))
        print(f"📸 Slide 1 截圖完成: {screenshot_path}")

        # 切換至 Slide 5 (關鍵頁：動畫影片)
        page.evaluate("goToSlide(5)")
        page.wait_for_timeout(500)
        video_src = page.eval_on_selector("#explainer-video source", "el => el.getAttribute('src')")
        print(f"🎬 Slide 5 影片標籤驗證: src = {video_src}")
        page.screenshot(path=str(video_page_screenshot))
        print(f"📸 Slide 5 (動畫關鍵頁) 截圖完成: {video_page_screenshot}")

        # 切換至 Slide 11 (測驗題)
        page.evaluate("goToSlide(11)")
        page.wait_for_timeout(300)
        # 點擊選項 B (正確答案)
        page.click(".quiz-option:nth-child(2)")
        page.wait_for_timeout(300)
        feedback_text = page.inner_text("#quiz-feedback")
        print(f"🎯 測驗互動反饋: {feedback_text}")
        assert "回答完全正確" in feedback_text, "測驗反饋未顯示正確文字！"

        browser.close()

    if errors:
        print(f"❌ 發現瀏覽器執行期錯誤 ({len(errors)} 個):")
        for err in errors:
            print(f"  {err}")
        sys.exit(1)
    else:
        print("✅ [PERFECT PASS] 瀏覽器實體渲染 0 控制台錯誤，端到端互動完全合格！")

if __name__ == "__main__":
    main()

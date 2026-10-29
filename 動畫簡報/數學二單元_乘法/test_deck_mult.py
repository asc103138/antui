import asyncio
import os
from pathlib import Path
from playwright.async_api import async_playwright

async def run_test():
    async with async_playwright() as p:
        browser = await p.chromium.launch(
            channel="msedge",
            headless=True
        )
        context = await browser.new_context(
            viewport={"width": 1920, "height": 1080},
            device_scale_factor=1
        )
        page = await context.new_page()

        console_errors = []
        page.on("console", lambda msg: console_errors.append(msg.text) if msg.type == "error" else None)
        page.on("pageerror", lambda err: console_errors.append(str(err)))

        html_path = Path("d:/antui/動畫簡報/index.html").resolve()
        url = f"file:///{html_path.as_posix()}"
        print(f"Navigating to {url}...")
        await page.goto(url, wait_until="networkidle")

        renders_dir = Path("d:/antui/動畫簡報/renders")
        renders_dir.mkdir(parents=True, exist_ok=True)

        # 1. 封面截圖
        await page.screenshot(path=str(renders_dir / "deck_mult_slide1_cover.png"))
        print("Captured Slide 1 Cover")

        # 2. 測試翻頁到 Slide 5 (關鍵動畫頁 1)
        await page.evaluate("goToSlide(5)")
        await page.wait_for_timeout(500)
        # 測試動畫 1 播放與進度條
        has_play_1 = await page.is_visible("#btn-play-1")
        has_slider_1 = await page.is_visible("#slider-1")
        print(f"Slide 5 Animation 1 Controls: play={has_play_1}, slider={has_slider_1}")
        # 觸發播放
        await page.click("#btn-play-1")
        await page.wait_for_timeout(800)
        await page.screenshot(path=str(renders_dir / "deck_mult_slide5_anim1.png"))
        print("Captured Slide 5 (Animation 1: 位值跳躍)")

        # 3. 測試翻頁到 Slide 6 (關鍵動畫頁 2: 2008x24 兩層演繹)
        await page.evaluate("goToSlide(6)")
        await page.wait_for_timeout(500)
        has_play_2 = await page.is_visible("#btn-play-2")
        has_slider_2 = await page.is_visible("#slider-2")
        print(f"Slide 6 Animation 2 Controls: play={has_play_2}, slider={has_slider_2}")
        # 觸發步驟前進
        await page.click("#btn-play-2")
        await page.wait_for_timeout(1000)
        await page.screenshot(path=str(renders_dir / "deck_mult_slide6_anim2_2008x24.png"))
        print("Captured Slide 6 (Animation 2: 2008x24 四位數乘二位數兩層直式)")

        # 4. 測試翻頁到 Slide 8 (關鍵動畫頁 3: 迷思天秤)
        await page.evaluate("goToSlide(8)")
        await page.wait_for_timeout(500)
        has_play_3 = await page.is_visible("#btn-play-3")
        has_slider_3 = await page.is_visible("#slider-3")
        print(f"Slide 8 Animation 3 Controls: play={has_play_3}, slider={has_slider_3}")
        await page.click("#btn-play-3")
        await page.wait_for_timeout(800)
        await page.screenshot(path=str(renders_dir / "deck_mult_slide8_anim3_balance.png"))
        print("Captured Slide 8 (Animation 3: 錯位天秤)")

        # 5. 測試翻頁到 Slide 9 (迷思二：中間有 0 乘法)
        await page.evaluate("goToSlide(9)")
        await page.wait_for_timeout(400)
        await page.screenshot(path=str(renders_dir / "deck_mult_slide9_zero_trap.png"))
        print("Captured Slide 9 (中間有 0 乘法)")

        # 6. 測試翻頁到 Slide 11 (習作實戰題：1350x12 兩層直式)
        await page.evaluate("goToSlide(11)")
        await page.wait_for_timeout(400)
        await page.screenshot(path=str(renders_dir / "deck_mult_slide11_workbook.png"))
        print("Captured Slide 11 (習作實戰 1350x12)")

        # 7. 測試翻頁到 Slide 13 (小偵探捉錯)
        await page.evaluate("goToSlide(13)")
        await page.wait_for_timeout(400)
        await page.click(".myth-interactive-card:nth-child(1)")
        await page.wait_for_timeout(300)
        await page.screenshot(path=str(renders_dir / "deck_mult_slide13_detective.png"))
        print("Captured Slide 13 (小偵探捉錯)")

        # 8. 測試翻頁到 Slide 14 (英雄榜總結)
        await page.evaluate("goToSlide(14)")
        await page.wait_for_timeout(400)
        await page.screenshot(path=str(renders_dir / "deck_mult_slide14_summary.png"))
        print("Captured Slide 14 (英雄榜)")

        await browser.close()

        print("\n=== Playwright Test Results ===")
        print(f"Console Errors count: {len(console_errors)}")
        if console_errors:
            for err in console_errors:
                print(f"  [ERROR] {err}")
            raise Exception("Playwright detected console errors!")
        else:
            print("✓ PERFECT PASS: 0 Console Errors, 0 Unhandled Exceptions!")

if __name__ == "__main__":
    asyncio.run(run_test())

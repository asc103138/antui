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
        page.on("console", lambda msg: console_errors.append(f"[{msg.type}] {msg.text}") if msg.type == "error" else None)
        page.on("pageerror", lambda err: console_errors.append(str(err)))

        html_path = Path("d:/antui/動畫簡報/社會第二單元/index.html").resolve()
        url = f"file:///{html_path.as_posix()}"
        print(f"Navigating to {url}...")
        await page.goto(url, wait_until="networkidle")

        renders_dir = Path("d:/antui/動畫簡報/社會第二單元/renders")
        renders_dir.mkdir(parents=True, exist_ok=True)

        # 1. 封面截圖 (Slide 1)
        await page.screenshot(path=str(renders_dir / "deck_social_slide1_cover.png"))
        print("✓ Slide 1 Cover captured")

        # 2. Slide 2: 單元架構地圖
        await page.evaluate("goToSlide(2)")
        await page.wait_for_timeout(300)
        await page.screenshot(path=str(renders_dir / "deck_social_slide2_map.png"))
        print("✓ Slide 2 Map captured")

        # 3. Slide 3: 2-1 原住民傳統住屋
        await page.evaluate("goToSlide(3)")
        await page.wait_for_timeout(300)
        await page.screenshot(path=str(renders_dir / "deck_social_slide3_indigenous_house.png"))
        print("✓ Slide 3 Indigenous Houses captured")

        # 4. Slide 4: 2-1 漢人傳統住屋
        await page.evaluate("goToSlide(4)")
        await page.wait_for_timeout(300)
        await page.screenshot(path=str(renders_dir / "deck_social_slide4_han_house.png"))
        print("✓ Slide 4 Han Houses captured")

        # 5. Slide 5: 關鍵解說動畫頁 (205秒 MP4 控制面板)
        await page.evaluate("goToSlide(5)")
        await page.wait_for_timeout(500)
        has_video = await page.is_visible("#main-video-player")
        has_play_btn = await page.is_visible("#btn-play-pause")
        has_seek = await page.is_visible("#video-seek")
        has_time = await page.is_visible("#video-time")
        print(f"Slide 5 Controls: video={has_video}, play={has_play_btn}, seek={has_seek}, time={has_time}")
        assert has_video and has_play_btn and has_seek and has_time, "Slide 5 播放器控制項缺失！"

        # 點擊播放與調整進度
        await page.click("#btn-play-pause")
        await page.wait_for_timeout(600)
        await page.fill("#video-seek", "45")
        await page.evaluate("onSeekChange()")
        await page.wait_for_timeout(400)
        await page.screenshot(path=str(renders_dir / "deck_social_slide5_video_player.png"))
        print("✓ Slide 5 Video Player captured")

        # 6. Slide 6: 建築物理結構解剖
        await page.evaluate("goToSlide(6)")
        await page.wait_for_timeout(400)
        await page.click("#btn-struct-underground")
        await page.wait_for_timeout(300)
        await page.screenshot(path=str(renders_dir / "deck_social_slide6_struct_canvas.png"))
        print("✓ Slide 6 Structural Anatomy captured")

        # 7. Slide 7: 2-2 原住民生活器具
        await page.evaluate("goToSlide(7)")
        await page.wait_for_timeout(300)
        await page.screenshot(path=str(renders_dir / "deck_social_slide7_indigenous_tools.png"))
        print("✓ Slide 7 Indigenous Tools captured")

        # 8. Slide 8: 2-2 漢人生活器具
        await page.evaluate("goToSlide(8)")
        await page.wait_for_timeout(300)
        await page.screenshot(path=str(renders_dir / "deck_social_slide8_han_tools.png"))
        print("✓ Slide 8 Han Tools captured")

        # 9. Slide 9: 器具物理動態演示
        await page.evaluate("goToSlide(9)")
        await page.wait_for_timeout(400)
        await page.click("#btn-mach-winnow")
        await page.wait_for_timeout(300)
        await page.screenshot(path=str(renders_dir / "deck_social_slide9_machine_canvas.png"))
        print("✓ Slide 9 Machine Simulation captured")

        # 10. Slide 10: 跨族群智慧對照
        await page.evaluate("goToSlide(10)")
        await page.wait_for_timeout(300)
        await page.screenshot(path=str(renders_dir / "deck_social_slide10_compare.png"))
        print("✓ Slide 10 Compare Matrix captured")

        # 11. Slide 11: 臺中海線在地情境
        await page.evaluate("goToSlide(11)")
        await page.wait_for_timeout(300)
        await page.screenshot(path=str(renders_dir / "deck_social_slide11_local_coast.png"))
        print("✓ Slide 11 Local Coast captured")

        # 12. Slide 12: 小偵探捉錯互動
        await page.evaluate("goToSlide(12)")
        await page.wait_for_timeout(300)
        await page.click("#quiz-detect-1")
        await page.wait_for_timeout(200)
        await page.screenshot(path=str(renders_dir / "deck_social_slide12_myth_detective.png"))
        print("✓ Slide 12 Detective Myth captured")

        # 13. Slide 13: 隨堂測驗互動
        await page.evaluate("goToSlide(13)")
        await page.wait_for_timeout(400)
        # 點擊正確答案 (選項 B: 防鼠板)
        options = await page.query_selector_all(".quiz-option")
        if len(options) >= 2:
            await options[1].click()
            await page.wait_for_timeout(400)
        await page.screenshot(path=str(renders_dir / "deck_social_slide13_interactive_quiz.png"))
        print("✓ Slide 13 Interactive Quiz captured")

        # 14. Slide 14: SOIL 喚起行動
        await page.evaluate("goToSlide(14)")
        await page.wait_for_timeout(300)
        await page.screenshot(path=str(renders_dir / "deck_social_slide14_soil_cta.png"))
        print("✓ Slide 14 SOIL CTA captured")

        await browser.close()

        print("\n==========================================")
        print(f"Console Errors Count: {len(console_errors)}")
        if console_errors:
            print("Errors encountered:")
            for e in console_errors:
                print("  -", e)
        else:
            print("✓ 0 Console Errors & 0 Unhandled Exceptions Verified!")
        print("==========================================")

        assert len(console_errors) == 0, f"Encountered {len(console_errors)} console errors!"

if __name__ == "__main__":
    asyncio.run(run_test())

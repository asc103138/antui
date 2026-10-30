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

        html_path = Path("d:/antui/動畫簡報/index.html").resolve()
        url = f"file:///{html_path.as_posix()}"
        print(f"Navigating to {url}...")
        await page.goto(url, wait_until="networkidle")

        renders_dir = Path("d:/antui/動畫簡報/renders")
        renders_dir.mkdir(parents=True, exist_ok=True)

        # 1. 封面截圖 (Slide 1)
        await page.screenshot(path=str(renders_dir / "deck_social_slide1_cover.png"))
        print("✓ Slide 1 Cover captured")

        # 2. Slide 2: 單元架構地圖
        await page.evaluate("goToSlide(2)")
        await page.wait_for_timeout(300)
        await page.screenshot(path=str(renders_dir / "deck_social_slide2_map.png"))
        print("✓ Slide 2 Map captured")

        # 3. Slide 3: 2-1 原住民族傳統住屋
        await page.evaluate("goToSlide(3)")
        await page.wait_for_timeout(300)
        await page.screenshot(path=str(renders_dir / "deck_social_slide3_indigenous_house.png"))
        print("✓ Slide 3 Indigenous Houses captured")

        # 4. Slide 4: 會呼吸的房子石板屋
        await page.evaluate("goToSlide(4)")
        await page.wait_for_timeout(300)
        await page.screenshot(path=str(renders_dir / "deck_social_slide4_han_house.png"))
        print("✓ Slide 4 Breathing Slate House captured")

        # 5. Slide 5: 關鍵解說動畫頁 (271秒 MP4 控制面板)
        await page.evaluate("goToSlide(5)")
        await page.wait_for_timeout(500)
        has_video = await page.is_visible("#main-video-player")
        has_play_btn = await page.is_visible("#btn-play-pause")
        has_seek = await page.is_visible("#video-seek")
        has_time = await page.is_visible("#video-time")
        print(f"Slide 5 Controls: video={has_video}, play={has_play_btn}, seek={has_seek}, time={has_time}")
        assert has_video and has_play_btn and has_seek and has_time, "Slide 5 播放器控制項缺失！"

        await page.click("#btn-play-pause")
        await page.wait_for_timeout(500)
        await page.fill("#video-seek", "45")
        await page.evaluate("onSeekChange()")
        await page.wait_for_timeout(400)
        await page.screenshot(path=str(renders_dir / "deck_social_slide5_video_player.png"))
        print("✓ Slide 5 Video Player captured")

        # 6. Slide 6: 漢人傳統住屋（竹管仔厝與土埆厝）
        await page.evaluate("goToSlide(6)")
        await page.wait_for_timeout(300)
        await page.screenshot(path=str(renders_dir / "deck_social_slide6_struct_canvas.png"))
        print("✓ Slide 6 Han Traditional Houses captured")

        # 7. Slide 7: 住屋擴建三部曲（一條龍、單伸手、三合院）
        await page.evaluate("goToSlide(7)")
        await page.wait_for_timeout(300)
        await page.screenshot(path=str(renders_dir / "deck_social_slide7_indigenous_tools.png"))
        print("✓ Slide 7 House Evolution captured")

        # 8. Slide 8: 三合院生活空間情境圖解
        await page.evaluate("goToSlide(8)")
        await page.wait_for_timeout(300)
        await page.screenshot(path=str(renders_dir / "deck_social_slide8_han_tools.png"))
        print("✓ Slide 8 Sanheyuan Living Space captured")

        # 9. Slide 9: 傳統住屋的改變與再生
        await page.evaluate("goToSlide(9)")
        await page.wait_for_timeout(300)
        await page.screenshot(path=str(renders_dir / "deck_social_slide9_machine_canvas.png"))
        print("✓ Slide 9 House Change & Rebirth captured")

        # 10. Slide 10: 原住民族傳統生活器物
        await page.evaluate("goToSlide(10)")
        await page.wait_for_timeout(300)
        await page.screenshot(path=str(renders_dir / "deck_social_slide10_compare.png"))
        print("✓ Slide 10 Indigenous Tools captured")

        # 11. Slide 11: 漢人傳統器物與物盡其用（紅磚灶灰燼悶地瓜）
        await page.evaluate("goToSlide(11)")
        await page.wait_for_timeout(300)
        await page.screenshot(path=str(renders_dir / "deck_social_slide11_local_coast.png"))
        print("✓ Slide 11 Han Utensils & Resourcefulness captured")

        # 12. Slide 12: 生活器物現代風貌與減塑實踐
        await page.evaluate("goToSlide(12)")
        await page.wait_for_timeout(300)
        await page.screenshot(path=str(renders_dir / "deck_social_slide12_myth_detective.png"))
        print("✓ Slide 12 Modern Plastic & Reduction captured")

        # 13. Slide 13: 習作實戰檢討 (一)：住屋篇 P.12-15
        await page.evaluate("goToSlide(13)")
        await page.wait_for_timeout(400)
        await page.evaluate("setWbTab(2)")
        await page.wait_for_timeout(300)
        await page.evaluate("setWbTab(1)")
        await page.evaluate("switchWbImg(1, 'tch')")
        await page.wait_for_timeout(400)
        await page.screenshot(path=str(renders_dir / "deck_social_slide13_interactive_quiz.png"))
        print("✓ Slide 13 Workbook Housing (P.12-15) captured")

        # 14. Slide 14: 習作實戰檢討 (二)：器物與減塑篇 P.16-17
        await page.evaluate("goToSlide(14)")
        await page.wait_for_timeout(400)
        await page.evaluate("setWbPageImg14(17)")
        await page.wait_for_timeout(300)
        await page.evaluate("setWbPageImg14(16)")
        await page.evaluate("switchWbImg14('tch')")
        await page.evaluate("revealP16Table()")
        await page.wait_for_timeout(400)
        await page.screenshot(path=str(renders_dir / "deck_social_slide14_workbook_p16_17.png"))
        print("✓ Slide 14 Dedicated Workbook Utensils & Plastic Reduction (P.16-17) captured")

        # 15. Slide 15: 小探究家與階層圖學習策略
        await page.evaluate("goToSlide(15)")
        await page.wait_for_timeout(300)
        await page.screenshot(path=str(renders_dir / "deck_social_slide15_soil_cta.png"))
        print("✓ Slide 15 Inquiry & Hierarchy Strategy captured")

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

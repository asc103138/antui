#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
使用 Playwright 精準渲染 22 頁 Reveal.js 簡報為 1920x1080 高解析 PNG
確保每一頁的所有 fragment、照片、圖表、文字卡片 100% 完整呈現，絕不留白！
"""

import os
import time
from playwright.sync_api import sync_playwright

OUTPUT_DIR = r"d:\antui\steam成果製作\成果展繳交資料\簡報圖片_1080p"
os.makedirs(OUTPUT_DIR, exist_ok=True)

html_path = os.path.abspath(r"d:\antui\steam成果製作\成果展繳交資料\steam-gigo-balance-deck\index.html")
html_url = "file:///" + html_path.replace("\\", "/")

print("=" * 65)
print("  🎬 使用 Playwright 啟動 Chromium 渲染 22 頁 1080p 實體畫面")
print("=" * 65)

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page(viewport={"width": 1920, "height": 1080}, device_scale_factor=1)
    page.goto(html_url, wait_until="networkidle")
    
    # 確保 Reveal.js 載入完成
    page.wait_for_function("typeof Reveal !== 'undefined' && Reveal.isReady()")
    
    # 強制所有 fragment 預設可視，避免截圖遺漏
    page.evaluate("""() => {
        const style = document.createElement('style');
        style.innerHTML = `
            .reveal .slides section .fragment {
                opacity: 1 !important;
                visibility: visible !important;
                transform: none !important;
            }
        `;
        document.head.appendChild(style);
    }""")
    
    total_slides = page.evaluate("Reveal.getTotalSlides()")
    print(f"  總頁數: {total_slides} 頁")
    
    for i in range(total_slides):
        page.evaluate(f"Reveal.slide({i})")
        time.sleep(0.3) # 等待過渡穩定
        
        # 特殊頁面處理：如果是 S13（對比拉桿），設定拉桿位置在 50%
        if i == 12: # slide 13 (0-indexed 12)
            page.evaluate("""() => {
                const slider = document.getElementById('compareRange');
                const afterLayer = document.getElementById('afterLayer');
                const handle = document.getElementById('sliderHandle');
                if (slider && afterLayer && handle) {
                    slider.value = 50;
                    afterLayer.style.clipPath = 'inset(0 50% 0 0)';
                    handle.style.left = '50%';
                }
            }""")
            time.sleep(0.1)
            
        out_png = os.path.join(OUTPUT_DIR, f"slide_{i+1:02d}.png")
        page.screenshot(path=out_png)
        sz_kb = os.path.getsize(out_png) // 1024
        print(f"  [Slide {i+1:02d}/{total_slides}] 成功渲染: {os.path.basename(out_png)} ({sz_kb} KB)")
        
    browser.close()

print("=" * 65)
print("  🎉 全套 22 頁 1080p 簡報實體截圖全數渲染完成！")
print("=" * 65)

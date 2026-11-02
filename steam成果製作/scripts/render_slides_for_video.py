#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
將 7 頁簡報以 Chrome headless 高解析渲染為 1920x1080 PNG 圖片供影片合成
"""

import os
import subprocess
from PIL import Image

SLIDES_IMG_DIR = r"d:\antui\steam成果製作\成果展繳交資料\簡報圖片_1080p"
os.makedirs(SLIDES_IMG_DIR, exist_ok=True)

html_path = os.path.abspath(r"d:\antui\steam成果製作\成果展繳交資料\臺中市梧棲區中正國小_STEAM成果展_5分鐘現場分享會簡報.html")
chrome_exe = r"C:\Program Files\Google\Chrome\Application\chrome.exe"

print("=" * 65)
print("  🎥 正在使用 Chrome Headless 渲染 7 頁 1920x1080 簡報畫面...")
print("=" * 65)

for i in range(7):
    out_png = os.path.join(SLIDES_IMG_DIR, f"slide_{i+1:02d}.png")
    url = f"file:///{html_path.replace(os.sep, '/')}?slide={i}&hide_ui=1"
    
    cmd = [
        chrome_exe,
        "--headless=new",
        f"--screenshot={out_png}",
        "--window-size=1920,1080",
        "--hide-scrollbars",
        "--force-device-scale-factor=1",
        url
    ]
    subprocess.run(cmd, capture_output=True)
    
    if os.path.exists(out_png):
        with Image.open(out_png) as im:
            print(f"  ✅ Slide {i+1} 渲染成功: {out_png} ({im.size[0]}x{im.size[1]})")
    else:
        print(f"  ❌ Slide {i+1} 渲染失敗！")

print("\n🎉 全部 7 頁 1080p 畫面渲染完成！")

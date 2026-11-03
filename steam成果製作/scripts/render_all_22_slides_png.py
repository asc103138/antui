#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
將 22 頁 Reveal.js 簡報完整渲染為 1920x1080 高解析 PNG 靜態圖庫
"""

import os
import time
import subprocess

SLIDES_IMG_DIR = r"d:\antui\steam成果製作\成果展繳交資料\簡報圖片_1080p"
os.makedirs(SLIDES_IMG_DIR, exist_ok=True)

html_path = os.path.abspath(r"d:\antui\steam成果製作\成果展繳交資料\臺中市梧棲區中正國小_STEAM成果展_5分鐘現場分享會簡報.html")
chrome_exe = r"C:\Program Files\Google\Chrome\Application\chrome.exe"

if not os.path.exists(chrome_exe):
    print("[WARN] Chrome executable not found at default location.")
    exit(0)

print("=" * 65)
print("  🎥 正在使用 Chrome Headless 批次渲染 22 頁 1920x1080 簡報畫面...")
print("=" * 65)

html_url = "file:///" + html_path.replace("\\", "/")

for i in range(22):
    out_png = os.path.join(SLIDES_IMG_DIR, f"slide_{i+1:02d}.png")
    # Reveal.js fragment 全開與精準導航
    url = f"{html_url}#/{i}"
    cmd = [
        chrome_exe,
        "--headless=new",
        f"--screenshot={out_png}",
        "--window-size=1920,1080",
        "--hide-scrollbars",
        "--virtual-time-budget=1200",
        url
    ]
    res = subprocess.run(cmd, capture_output=True)
    if os.path.exists(out_png):
        sz = os.path.getsize(out_png) // 1024
        print(f"  [Slide {i+1:02d}/22] Rendered: {os.path.basename(out_png)} ({sz} KB)")
    else:
        print(f"  [Slide {i+1:02d}/22] FAILED")

print("=" * 65)
print("  ✅ 全套 22 頁 1080p 簡報圖片渲染完畢！")
print("=" * 65)

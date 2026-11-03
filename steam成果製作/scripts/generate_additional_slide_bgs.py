#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
生成全套 22 頁簡報之專屬暗色科技背景圖，確保每一頁皆有專屬深邃科技底圖，絕不缺漏任何一張背景。
"""

import os
import math
from PIL import Image, ImageDraw, ImageFilter

TARGET_DIRS = [
    r"d:\antui\steam成果製作\成果展繳交資料\steam-gigo-balance-deck\images\bgs",
    r"d:\antui\steam成果製作\成果展繳交資料\images\bgs"
]
for d in TARGET_DIRS:
    os.makedirs(d, exist_ok=True)

def create_base_canvas(w=1920, h=1080, bg_rgb=(9, 13, 20)):
    im = Image.new("RGB", (w, h), bg_rgb)
    d = ImageDraw.Draw(im)
    # 細微科技網格
    for y in range(0, h, 60):
        d.line([(0, y), (w, y)], fill=(bg_rgb[0]+6, bg_rgb[1]+8, bg_rgb[2]+12), width=1)
    for x in range(0, w, 60):
        d.line([(x, 0), (x, h)], fill=(bg_rgb[0]+6, bg_rgb[1]+8, bg_rgb[2]+12), width=1)
    return im

def add_glow_spot(im, cx, cy, rx, ry, col_rgba, blur_r=80):
    w, h = im.size
    overlay = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(overlay)
    d.ellipse([(cx - rx, cy - ry), (cx + rx, cy + ry)], fill=col_rgba)
    overlay = overlay.filter(ImageFilter.GaussianBlur(blur_r))
    base = im.convert("RGBA")
    combined = Image.alpha_composite(base, overlay)
    return combined.convert("RGB")

def save_to_all(im, filename):
    for d in TARGET_DIRS:
        p = os.path.join(d, filename)
        im.save(p, quality=92)
    print(f"[OK] Generated {filename}")

# 1. bg_paradigm: 典範轉移對比雙色底圖 (左側冷紅警示，右側青翠科技綠)
im_p = create_base_canvas(bg_rgb=(8, 12, 18))
im_p = add_glow_spot(im_p, 380, 540, 350, 420, (239, 68, 68, 45), blur_r=100)
im_p = add_glow_spot(im_p, 1540, 540, 350, 420, (16, 185, 129, 45), blur_r=100)
im_p = add_glow_spot(im_p, 960, 540, 150, 500, (56, 189, 248, 30), blur_r=70)
d_p = ImageDraw.Draw(im_p)
# 分割線光暈裝飾
d_p.line([(960, 0), (960, 1080)], fill=(79, 195, 247, 80), width=2)
save_to_all(im_p, "bg_paradigm.png")

# 2. bg_chronicle_01: 回憶錄一 萌芽啟動與原型研發 (琥珀金色與藍綠光點交織)
im_c1 = create_base_canvas(bg_rgb=(10, 14, 22))
im_c1 = add_glow_spot(im_c1, 400, 300, 300, 300, (245, 158, 11, 40), blur_r=90)
im_c1 = add_glow_spot(im_c1, 1500, 750, 350, 350, (56, 189, 248, 45), blur_r=90)
d_c1 = ImageDraw.Draw(im_c1)
for i in range(5):
    y = 200 + i * 160
    d_c1.line([(100, y), (1820, y)], fill=(30, 45, 65), width=1)
    d_c1.ellipse([(200 + i*320 - 8, y - 8), (200 + i*320 + 8, y + 8)], fill=(245, 158, 11, 180))
save_to_all(im_c1, "bg_chronicle_01.png")

# 3. bg_chronicle_02: 回憶錄二 鯉魚國小創客交流 (青藍與電路板科技質感)
im_c2 = create_base_canvas(bg_rgb=(9, 15, 24))
im_c2 = add_glow_spot(im_c2, 350, 800, 320, 320, (14, 165, 233, 45), blur_r=90)
im_c2 = add_glow_spot(im_c2, 1450, 320, 360, 360, (99, 102, 241, 40), blur_r=90)
d_c2 = ImageDraw.Draw(im_c2)
# 電路轉折軌跡
for pt_seq in [
    [(150, 200), (450, 200), (550, 300), (850, 300)],
    [(1100, 800), (1350, 800), (1450, 700), (1750, 700)]
]:
    d_c2.line(pt_seq, fill=(56, 189, 248, 90), width=2)
save_to_all(im_c2, "bg_chronicle_02.png")

# 4. bg_chronicle_03: 回憶錄三 入班試教與黑板引導 (深邃鈷藍與白光焦點)
im_c3 = create_base_canvas(bg_rgb=(8, 13, 23))
im_c3 = add_glow_spot(im_c3, 500, 500, 400, 350, (59, 130, 246, 45), blur_r=90)
im_c3 = add_glow_spot(im_c3, 1400, 600, 320, 320, (45, 212, 191, 40), blur_r=85)
d_c3 = ImageDraw.Draw(im_c3)
# 幾何視窗焦點框
d_c3.rectangle([(120, 140), (1800, 940)], outline=(30, 58, 138, 100), width=1)
save_to_all(im_c3, "bg_chronicle_03.png")

# 5. bg_chronicle_04: 回憶錄四 數據成效與科技實測 (翠綠與霓虹脈衝)
im_c4 = create_base_canvas(bg_rgb=(8, 16, 20))
im_c4 = add_glow_spot(im_c4, 400, 650, 350, 350, (16, 185, 129, 45), blur_r=90)
im_c4 = add_glow_spot(im_c4, 1500, 400, 380, 380, (56, 189, 248, 45), blur_r=90)
d_c4 = ImageDraw.Draw(im_c4)
# 數據圖表波動線
pts = [(160 + i*160, int(750 - 180 * math.sin(i*0.7))) for i in range(11)]
d_c4.line(pts, fill=(52, 211, 153, 90), width=2)
save_to_all(im_c4, "bg_chronicle_04.png")

# 6. bg_chronicle_05: 回憶錄五 機關王 8 迴與團隊合影 (霓虹紫與品紅慶典光環)
im_c5 = create_base_canvas(bg_rgb=(13, 10, 24))
im_c5 = add_glow_spot(im_c5, 450, 450, 380, 380, (168, 85, 247, 45), blur_r=95)
im_c5 = add_glow_spot(im_c5, 1450, 650, 360, 360, (236, 72, 153, 40), blur_r=95)
d_c5 = ImageDraw.Draw(im_c5)
# 8 迴同心齒輪光環
for r in [80, 160, 240, 320]:
    d_c5.arc([(960-r, 540-r), (960+r, 540+r)], start=0, end=360, fill=(168, 85, 247, 70), width=1)
save_to_all(im_c5, "bg_chronicle_05.png")

# 7. bg_chronicle_06: 回憶錄六 教案規格藍圖與規準 (極致工程藍圖座標與雙向細目)
im_c6 = create_base_canvas(bg_rgb=(7, 16, 28))
im_c6 = add_glow_spot(im_c6, 960, 540, 500, 400, (6, 182, 212, 40), blur_r=100)
d_c6 = ImageDraw.Draw(im_c6)
# 精密藍圖格線
for y in range(0, 1080, 40):
    d_c6.line([(0, y), (1920, y)], fill=(12, 40, 65), width=1)
for x in range(0, 1920, 40):
    d_c6.line([(0, x), (1920, x)], fill=(12, 40, 65), width=1)
save_to_all(im_c6, "bg_chronicle_06.png")

print("All new slide backgrounds generated successfully!")

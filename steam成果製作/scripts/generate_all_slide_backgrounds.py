#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
生成全套 16:9 簡報暗色科技背景圖，確保每一頁皆有專屬深邃科技底圖
"""

import os
import math
from PIL import Image, ImageDraw, ImageFilter

OUT_DIR = r"d:\antui\steam成果製作\成果展繳交資料\steam-gigo-balance-deck\images\bgs"
os.makedirs(OUT_DIR, exist_ok=True)

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
    od = ImageDraw.Draw(overlay)
    od.ellipse([cx - rx, cy - ry, cx + rx, cy + ry], fill=col_rgba)
    overlay = overlay.filter(ImageFilter.GaussianBlur(blur_r))
    im.paste(overlay, (0, 0), overlay)

# 1. bg_team: 團隊共備網狀連結
im = create_base_canvas(bg_rgb=(10, 15, 24))
add_glow_spot(im, 400, 300, 450, 350, (79, 195, 247, 35), 90)
add_glow_spot(im, 1500, 700, 400, 300, (232, 100, 58, 30), 85)
d = ImageDraw.Draw(im)
# 幾何節點
nodes = [(300, 250), (600, 180), (850, 350), (1400, 200), (1650, 400), (1300, 650), (450, 700)]
for i, n1 in enumerate(nodes):
    for n2 in nodes[i+1:]:
        if math.hypot(n1[0]-n2[0], n1[1]-n2[1]) < 650:
            d.line([n1, n2], fill=(79, 195, 247, 40), width=1)
    d.ellipse([n1[0]-6, n1[1]-6, n1[0]+6, n1[1]+6], fill=(129, 199, 132, 180))
im.save(os.path.join(OUT_DIR, "bg_team.png"), quality=92)

# 2. bg_wordcloud: 思維波紋與文字雲粒子
im = create_base_canvas(bg_rgb=(11, 14, 25))
add_glow_spot(im, 1200, 540, 500, 400, (79, 195, 247, 40), 95)
add_glow_spot(im, 400, 540, 350, 300, (255, 183, 77, 30), 80)
d = ImageDraw.Draw(im)
cx, cy = 1300, 540
for r in [120, 240, 360, 480]:
    d.ellipse([cx-r, cy-r, cx+r, cy+r], outline=(79, 195, 247, 30), width=2)
im.save(os.path.join(OUT_DIR, "bg_wordcloud.png"), quality=92)

# 3. bg_steam: STEAM 跨域幾何線框
im = create_base_canvas(bg_rgb=(12, 16, 26))
add_glow_spot(im, 960, 540, 600, 400, (129, 199, 132, 35), 100)
d = ImageDraw.Draw(im)
for i in range(5):
    angle = i * (2 * math.pi / 5) - math.pi / 2
    x = 960 + 380 * math.cos(angle)
    y = 540 + 380 * math.sin(angle)
    d.line([(960, 540), (x, y)], fill=(255, 183, 77, 45), width=2)
    d.ellipse([x-20, y-20, x+20, y+20], outline=(79, 195, 247, 80), width=3)
im.save(os.path.join(OUT_DIR, "bg_steam.png"), quality=92)

# 4. bg_curriculum: 課綱素養雙向細目柱線
im = create_base_canvas(bg_rgb=(10, 14, 24))
add_glow_spot(im, 480, 540, 450, 400, (79, 195, 247, 35), 90)
add_glow_spot(im, 1440, 540, 450, 400, (232, 100, 58, 30), 90)
d = ImageDraw.Draw(im)
d.line([(960, 100), (960, 980)], fill=(255, 255, 255, 30), width=2)
im.save(os.path.join(OUT_DIR, "bg_curriculum.png"), quality=92)

# 5. bg_roadmap: 階梯式光軌
im = create_base_canvas(bg_rgb=(11, 15, 25))
add_glow_spot(im, 350, 750, 300, 250, (255, 183, 77, 40), 80)
add_glow_spot(im, 960, 540, 300, 250, (79, 195, 247, 40), 80)
add_glow_spot(im, 1570, 330, 300, 250, (129, 199, 132, 45), 80)
d = ImageDraw.Draw(im)
pts = [(200, 800), (500, 800), (750, 580), (1150, 580), (1400, 360), (1750, 360)]
for i in range(len(pts)-1):
    d.line([pts[i], pts[i+1]], fill=(79, 195, 247, 70), width=4)
im.save(os.path.join(OUT_DIR, "bg_roadmap.png"), quality=92)

# 6. bg_assembly: 智高積木結構孔洞藍圖
im = create_base_canvas(bg_rgb=(8, 18, 28))
add_glow_spot(im, 960, 540, 550, 350, (79, 195, 247, 45), 90)
d = ImageDraw.Draw(im)
for gx in range(200, 1750, 80):
    for gy in range(180, 950, 80):
        d.ellipse([gx-8, gy-8, gx+8, gy+8], outline=(79, 195, 247, 30), width=1)
im.save(os.path.join(OUT_DIR, "bg_assembly.png"), quality=92)

# 7. bg_physics: 物理力學力矩天平
im = create_base_canvas(bg_rgb=(10, 18, 26))
add_glow_spot(im, 960, 540, 500, 350, (232, 100, 58, 35), 85)
d = ImageDraw.Draw(im)
d.line([(250, 480), (1670, 480)], fill=(255, 183, 77, 60), width=4)
d.polygon([(960, 480), (910, 580), (1010, 580)], fill=(79, 195, 247, 50))
im.save(os.path.join(OUT_DIR, "bg_physics.png"), quality=92)

# 8. bg_poll: 迷思快問快答同心光環
im = create_base_canvas(bg_rgb=(12, 16, 26))
add_glow_spot(im, 960, 540, 500, 400, (129, 199, 132, 45), 90)
d = ImageDraw.Draw(im)
for r in [180, 320, 460, 600]:
    d.arc([960-r, 540-r, 960+r, 540+r], 45, 315, fill=(129, 199, 132, 35), width=2)
im.save(os.path.join(OUT_DIR, "bg_poll.png"), quality=92)

# 9. bg_math_strategy: 算則微調加減法
im = create_base_canvas(bg_rgb=(11, 17, 27))
add_glow_spot(im, 480, 540, 400, 300, (232, 100, 58, 35), 85)
add_glow_spot(im, 1440, 540, 400, 300, (129, 199, 132, 40), 85)
d = ImageDraw.Draw(im)
# 加號與減號發光幾何
d.rectangle([460, 500, 500, 580], fill=(232, 100, 58, 40))
d.rectangle([420, 520, 540, 560], fill=(232, 100, 58, 40))
d.rectangle([1380, 520, 1500, 560], fill=(129, 199, 132, 40))
im.save(os.path.join(OUT_DIR, "bg_math_strategy.png"), quality=92)

# 10. bg_microbit: 科技體育加速度脈衝波形
im = create_base_canvas(bg_rgb=(8, 16, 25))
add_glow_spot(im, 960, 540, 550, 350, (79, 195, 247, 45), 90)
d = ImageDraw.Draw(im)
# 弦波軌跡
prev = (150, 540)
for px in range(150, 1770, 15):
    py = 540 + int(90 * math.sin((px - 150) * 0.02) * math.sin((px - 150) * 0.005))
    d.line([prev, (px, py)], fill=(79, 195, 247, 80), width=3)
    prev = (px, py)
im.save(os.path.join(OUT_DIR, "bg_microbit.png"), quality=92)

# 11. bg_gm: 機關王連續齒輪與斜面連鎖
im = create_base_canvas(bg_rgb=(14, 16, 26))
add_glow_spot(im, 1300, 540, 500, 400, (255, 183, 77, 40), 90)
d = ImageDraw.Draw(im)
cx, cy = 1400, 540
d.ellipse([cx-180, cy-180, cx+180, cy+180], outline=(255, 183, 77, 45), width=4)
for a in range(0, 360, 30):
    rad = math.radians(a)
    d.line([(cx + 170*math.cos(rad), cy + 170*math.sin(rad)), (cx + 200*math.cos(rad), cy + 200*math.sin(rad))], fill=(255, 183, 77, 50), width=6)
im.save(os.path.join(OUT_DIR, "bg_gm.png"), quality=92)

# 12. bg_chronicle: 歷程回憶錄膠卷微光
im = create_base_canvas(bg_rgb=(10, 15, 24))
add_glow_spot(im, 960, 540, 650, 450, (79, 195, 247, 40), 100)
add_glow_spot(im, 300, 300, 350, 250, (255, 183, 77, 30), 80)
d = ImageDraw.Draw(im)
# 膠卷孔洞線條
for fy in [120, 960]:
    d.line([(100, fy), (1820, fy)], fill=(255, 255, 255, 25), width=2)
    for fx in range(120, 1800, 60):
        d.rounded_rectangle([fx, fy-15, fx+25, fy+15], radius=3, outline=(79, 195, 247, 40), width=1)
im.save(os.path.join(OUT_DIR, "bg_chronicle.png"), quality=92)

print("🎉 Successfully generated all themed slide backgrounds!")

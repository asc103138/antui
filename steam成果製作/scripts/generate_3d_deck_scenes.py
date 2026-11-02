#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
生成拉桿對比專屬 3D 立體渲染場景圖與高畫質科技背景
1. viz_traditional_scale.png: 3D 立體金屬指針彈簧秤（傳統讀數痛點）
2. viz_steam_balance.png: 3D 立體智高積木等臂天平與彩色微調積木（STEAM創客典範）
3. conflict_bg.png: 重力擾動力線背景
4. balance_bg.png: 精密等臂力矩平衡背景
5. ending_bg.png: 未來展望粒子星空背景
"""

import os
import math
from PIL import Image, ImageDraw, ImageFilter, ImageEnhance

OUT_DIR = r"d:\antui\steam成果製作\成果展繳交資料\steam-gigo-balance-deck\images"
os.makedirs(OUT_DIR, exist_ok=True)

# 讀取現有 AI cover_bg 作為色調參考
cover_path = os.path.join(OUT_DIR, "cover_bg.png")
ai_cover = None
if os.path.exists(cover_path):
    try:
        ai_cover = Image.open(cover_path).convert("RGB")
    except Exception:
        ai_cover = None

# ==============================================================================
# 1. 繪製 3D 立體傳統指針彈簧秤 (viz_traditional_scale.png)
# ==============================================================================
def create_3d_traditional_scale():
    w, h = 1200, 800
    im = Image.new("RGBA", (w, h), (15, 20, 32, 255))
    d = ImageDraw.Draw(im)

    # 1.1 冷調壓抑環境背景與幾何網格
    for y in range(0, h, 40):
        d.line([(0, y), (w, y)], fill=(25, 30, 48, 120), width=1)
    for x in range(0, w, 40):
        d.line([(x, 0), (x, h)], fill=(25, 30, 48, 120), width=1)

    # 1.2 散落的枯燥試卷與繁複公式（立體斜角紙張）
    def draw_paper(x, y, pw, ph, angle_deg):
        paper = Image.new("RGBA", (pw, ph), (240, 240, 245, 140))
        pd = ImageDraw.Draw(paper)
        # 模擬繁雜公式線條
        for py in range(15, ph - 15, 12):
            pd.line([(15, py), (pw - 20, py)], fill=(120, 130, 150, 160), width=2)
        rotated = paper.rotate(angle_deg, expand=True, resample=Image.BICUBIC)
        im.paste(rotated, (x, y), rotated)

    draw_paper(150, 520, 260, 160, -12)
    draw_paper(780, 500, 280, 180, 15)
    draw_paper(220, 560, 240, 140, 5)

    # 1.3 秤的底部陰影（橢圓模糊）
    shadow = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    sd = ImageDraw.Draw(shadow)
    sd.ellipse([450, 560, 750, 680], fill=(0, 0, 0, 180))
    shadow = shadow.filter(ImageFilter.GaussianBlur(30))
    im.paste(shadow, (0, 0), shadow)

    # 1.4 立體梯形金屬機身（帶有立體金屬漸層與邊緣反光）
    body_overlay = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    bd = ImageDraw.Draw(body_overlay)
    # 主機身多邊形（正面）
    pts_front = [(500, 320), (700, 320), (740, 600), (460, 600)]
    bd.polygon(pts_front, fill=(40, 45, 65, 255), outline=(70, 80, 110, 255))
    # 側面立體厚度
    pts_side = [(700, 320), (730, 310), (770, 580), (740, 600)]
    bd.polygon(pts_side, fill=(28, 32, 48, 255), outline=(60, 70, 95, 255))

    # 1.5 頂部立體金屬托盤（立體厚度橢圓）
    # 托盤支柱
    bd.rectangle([585, 230, 615, 320], fill=(70, 75, 95, 255), outline=(100, 110, 135, 255))
    # 托盤厚度
    bd.ellipse([420, 205, 780, 265], fill=(50, 55, 75, 255), outline=(90, 100, 125, 255))
    bd.ellipse([420, 195, 780, 255], fill=(95, 105, 130, 255), outline=(140, 155, 185, 255))
    # 托盤內凹陰影
    bd.ellipse([450, 205, 750, 245], fill=(65, 72, 92, 255))

    # 1.6 正面圓形指針錶盤（帶有玻璃反光與密密麻麻的刻度）
    cx, cy = 600, 460
    r = 110
    bd.ellipse([cx - r - 8, cy - r - 8, cx + r + 8, cy + r + 8], fill=(30, 35, 50, 255), outline=(90, 105, 135, 255))
    bd.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(230, 232, 238, 255), outline=(50, 60, 80, 255))

    # 刻度環（密集細刻度，刻畫「傳統看錯」的痛點）
    for i in range(60):
        angle = math.radians(i * 6 - 90)
        is_major = (i % 5 == 0)
        len_tick = 14 if is_major else 7
        color_tick = (180, 30, 30, 255) if (is_major and i % 15 == 0) else (40, 45, 60, 255)
        x1 = cx + (r - 4) * math.cos(angle)
        y1 = cy + (r - 4) * math.sin(angle)
        x2 = cx + (r - 4 - len_tick) * math.cos(angle)
        y2 = cy + (r - 4 - len_tick) * math.sin(angle)
        bd.line([(x1, y1), (x2, y2)], fill=color_tick, width=2 if is_major else 1)

    # 紅色歪斜指針（未歸零，指向偏位）
    ptr_angle = math.radians(-55)
    px = cx + (r - 20) * math.cos(ptr_angle)
    py = cy + (r - 20) * math.sin(ptr_angle)
    bd.line([(cx, cy), (px, py)], fill=(225, 45, 45, 255), width=4)
    bd.ellipse([cx - 8, cy - 8, cx + 8, cy + 8], fill=(40, 45, 60, 255))
    bd.ellipse([cx - 4, cy - 4, cx + 4, cy + 4], fill=(225, 45, 45, 255))

    # 錶盤玻璃反光弧線
    bd.arc([cx - r + 15, cy - r + 15, cx + r - 15, cy + r - 15], 210, 330, fill=(255, 255, 255, 180), width=4)

    # 警告驚嘆標記（浮空發光警示）
    bd.circle = lambda x, y, cr, fill: bd.ellipse([x-cr, y-cr, x+cr, y+cr], fill=fill)
    bd.circle(380, 360, 32, (239, 68, 68, 220))
    bd.rectangle([376, 342, 384, 364], fill=(255, 255, 255, 255))
    bd.circle(380, 374, 4, (255, 255, 255, 255))

    im.paste(body_overlay, (0, 0), body_overlay)

    out_path = os.path.join(OUT_DIR, "viz_traditional_scale.png")
    im.save(out_path, quality=95)
    print(f"✅ Generated 3D Traditional Scale: {out_path}")

# ==============================================================================
# 2. 繪製 3D 立體 STEAM 智高彩色等臂天平 (viz_steam_balance.png)
# ==============================================================================
def create_3d_steam_balance():
    w, h = 1200, 800
    im = Image.new("RGBA", (w, h), (8, 28, 26, 255))
    d = ImageDraw.Draw(im)

    # 2.1 溫暖創客工坊微光背景與透視格線
    for y in range(0, h, 35):
        d.line([(0, y), (w, y)], fill=(16, 60, 50, 100), width=1)
    for x in range(0, w, 35):
        d.line([(x, 0), (x, h)], fill=(16, 60, 50, 100), width=1)

    # 2.2 底部光暈與投影
    glow = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    gd = ImageDraw.Draw(glow)
    gd.ellipse([300, 580, 900, 720], fill=(34, 197, 94, 60))
    gd.ellipse([450, 600, 750, 680], fill=(0, 0, 0, 190))
    glow = glow.filter(ImageFilter.GaussianBlur(35))
    im.paste(glow, (0, 0), glow)

    steam_layer = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    sd = ImageDraw.Draw(steam_layer)

    # 2.3 智高積木梯形立體底座（青藍色 + 模組卡扣孔）
    base_front = [(480, 560), (720, 560), (760, 650), (440, 650)]
    sd.polygon(base_front, fill=(14, 116, 144, 255), outline=(79, 195, 247, 255))
    base_top = [(480, 560), (510, 540), (750, 540), (720, 560)]
    sd.polygon(base_top, fill=(6, 182, 212, 255), outline=(125, 211, 252, 255))
    # 底座圓形孔洞
    for bx in range(480, 720, 45):
        sd.ellipse([bx, 600, bx + 22, 622], fill=(8, 47, 73, 255), outline=(56, 189, 248, 200))

    # 2.4 立體中央支柱與旋轉中軸
    sd.rectangle([580, 240, 620, 560], fill=(2, 132, 199, 255), outline=(56, 189, 248, 255))
    # 軸心立體球體
    sd.ellipse([570, 220, 630, 280], fill=(234, 88, 12, 255), outline=(254, 215, 170, 255))
    sd.ellipse([585, 235, 615, 265], fill=(251, 146, 60, 255))

    # 2.5 對稱等臂橫樑（亮黃/琥珀色立體長條積木，左右各 10 個孔洞）
    beam_front = [(150, 235), (1050, 235), (1050, 275), (150, 275)]
    sd.polygon(beam_front, fill=(245, 158, 11, 255), outline=(254, 240, 138, 255))
    beam_top = [(150, 235), (170, 220), (1070, 220), (1050, 235)]
    sd.polygon(beam_top, fill=(251, 191, 36, 255), outline=(254, 249, 195, 255))
    # 橫樑等距積木孔（左10孔 + 右10孔）
    for k in range(21):
        hx = 180 + k * 42
        if abs(hx - 600) > 25: # 避開中心軸
            sd.ellipse([hx, 245, hx + 18, 265], fill=(120, 53, 15, 255), outline=(253, 230, 138, 200))

    # 2.6 垂直校準指針（居中筆直指向水平基準）
    sd.line([(600, 250), (600, 480)], fill=(34, 197, 94, 255), width=6)
    sd.polygon([(592, 475), (608, 475), (600, 500)], fill=(34, 197, 94, 255))
    # 水平指示基準框
    sd.rounded_rectangle([560, 510, 640, 530], radius=4, fill=(15, 23, 42, 255), outline=(34, 197, 94, 255))
    sd.line([(600, 510), (600, 530)], fill=(34, 197, 94, 255), width=3)

    # 2.7 左右兩側立體懸吊托盤（綠色高質感吊架）
    def draw_pan_and_weights(px, py, is_left=True):
        # 吊線
        sd.line([(px - 70, 275), (px - 100, py)], fill=(74, 222, 128, 255), width=4)
        sd.line([(px + 70, 275), (px + 100, py)], fill=(74, 222, 128, 255), width=4)
        # 托盤
        sd.ellipse([px - 110, py - 10, px + 110, py + 40], fill=(22, 101, 52, 255), outline=(74, 222, 128, 255))
        sd.ellipse([px - 110, py - 20, px + 110, py + 30], fill=(34, 197, 94, 255), outline=(134, 239, 172, 255))
        sd.ellipse([px - 90, py - 15, px + 90, py + 22], fill=(20, 83, 45, 255))

        if is_left:
            # 左盤放待測物：立體橡皮擦（白色與藍色斜角立方體）
            sd.polygon([(px - 35, py - 5), (px + 25, py - 5), (px + 45, py - 35), (px - 15, py - 35)], fill=(226, 232, 240, 255), outline=(148, 163, 184, 255))
            sd.polygon([(px - 35, py - 5), (px + 25, py - 5), (px + 25, py + 15), (px - 35, py + 15)], fill=(59, 130, 246, 255), outline=(37, 99, 235, 255))
            sd.polygon([(px + 25, py - 5), (px + 45, py - 35), (px + 45, py - 15), (px + 25, py + 15)], fill=(29, 78, 216, 255))
        else:
            # 右盤堆疊 6 個立體 5g 彩色小積木（達成完美平衡）
            colors = [
                (234, 179, 8), (239, 68, 68), (59, 130, 246),
                (168, 85, 247), (234, 88, 12), (34, 197, 94)
            ]
            offsets = [(-40, 0), (-10, 0), (20, 0), (-25, -20), (5, -20), (-10, -40)]
            for (ox, oy), col in zip(offsets, colors):
                bx, by = px + ox, py + oy
                sd.polygon([(bx, by), (bx + 24, by), (bx + 24, by + 18), (bx, by + 18)], fill=col, outline=(255, 255, 255, 180))
                sd.polygon([(bx, by), (bx + 10, by - 8), (bx + 34, by - 8), (bx + 24, by)], fill=(min(255, col[0]+40), min(255, col[1]+40), min(255, col[2]+40)))

    draw_pan_and_weights(220, 430, is_left=True)
    draw_pan_and_weights(980, 430, is_left=False)

    # 完美平衡打勾與發光皇冠標誌
    sd.circle = lambda x, y, cr, fill: sd.ellipse([x-cr, y-cr, x+cr, y+cr], fill=fill)
    sd.circle(600, 140, 36, (34, 197, 94, 240))
    # 勾勾
    sd.line([(586, 140), (596, 152), (616, 130)], fill=(255, 255, 255, 255), width=6)

    im.paste(steam_layer, (0, 0), steam_layer)

    out_path = os.path.join(OUT_DIR, "viz_steam_balance.png")
    im.save(out_path, quality=95)
    print(f"✅ Generated 3D STEAM Balance: {out_path}")

# ==============================================================================
# 3. 依據 AI cover_bg 調性渲染高畫質背景 (conflict_bg, balance_bg, ending_bg)
# ==============================================================================
def create_themed_backgrounds():
    w, h = 1920, 1080

    # 3.1 conflict_bg.png: 深紫藍手感擾動力線背景
    im_c = Image.new("RGB", (w, h), (13, 16, 28))
    dc = ImageDraw.Draw(im_c)
    # 動態力線
    for i in range(12):
        y = 200 + i * 60
        dc.arc([100, y - 100, w - 100, y + 100], 190, 350, fill=(232, 100, 58, 70), width=3)
    # 柔和模糊
    overlay_c = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    ocd = ImageDraw.Draw(overlay_c)
    ocd.ellipse([300, 200, 900, 800], fill=(232, 100, 58, 45))
    ocd.ellipse([w - 900, 300, w - 300, 900], fill=(79, 195, 247, 40))
    overlay_c = overlay_c.filter(ImageFilter.GaussianBlur(90))
    im_c.paste(overlay_c, (0, 0), overlay_c)
    im_c.save(os.path.join(OUT_DIR, "conflict_bg.png"), quality=95)
    print("✅ Generated conflict_bg.png")

    # 3.2 balance_bg.png: 精密等臂力矩平衡背景
    im_b = Image.new("RGB", (w, h), (8, 22, 28))
    db = ImageDraw.Draw(im_b)
    # 科技幾何同心圓與精密水平刻線
    cx, cy = w // 2, h // 2
    for r in [200, 350, 500]:
        db.ellipse([cx - r, cy - r, cx + r, cy + r], outline=(79, 195, 247, 25), width=2)
    db.line([(100, cy), (w - 100, cy)], fill=(129, 199, 132, 70), width=3)
    db.line([(cx, 100), (cx, h - 100)], fill=(79, 195, 247, 50), width=2)
    overlay_b = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    obd = ImageDraw.Draw(overlay_b)
    obd.ellipse([cx - 400, cy - 300, cx + 400, cy + 300], fill=(79, 195, 247, 35))
    obd.ellipse([cx - 200, cy - 150, cx + 200, cy + 150], fill=(129, 199, 132, 30))
    overlay_b = overlay_b.filter(ImageFilter.GaussianBlur(80))
    im_b.paste(overlay_b, (0, 0), overlay_b)
    im_b.save(os.path.join(OUT_DIR, "balance_bg.png"), quality=95)
    print("✅ Generated balance_bg.png")

    # 3.3 ending_bg.png: 未來展望粒子星空背景
    im_e = Image.new("RGB", (w, h), (10, 14, 24))
    de = ImageDraw.Draw(im_e)
    # 飄升粒子
    import random
    random.seed(42)
    for _ in range(250):
        px = random.randint(50, w - 50)
        py = random.randint(50, h - 50)
        pr = random.randint(2, 6)
        col = random.choice([(79, 195, 247), (129, 199, 132), (255, 183, 77), (232, 100, 58)])
        de.ellipse([px, py, px + pr, py + pr], fill=col)
    overlay_e = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    oed = ImageDraw.Draw(overlay_e)
    oed.ellipse([w // 2 - 500, 300, w // 2 + 500, 900], fill=(129, 199, 132, 45))
    oed.ellipse([200, 200, 700, 700], fill=(79, 195, 247, 35))
    overlay_e = overlay_e.filter(ImageFilter.GaussianBlur(95))
    im_e.paste(overlay_e, (0, 0), overlay_e)
    im_e.save(os.path.join(OUT_DIR, "ending_bg.png"), quality=95)
    print("✅ Generated ending_bg.png")

if __name__ == "__main__":
    create_3d_traditional_scale()
    create_3d_steam_balance()
    create_themed_backgrounds()
    print("🎉 All 3D and themed background assets successfully created!")

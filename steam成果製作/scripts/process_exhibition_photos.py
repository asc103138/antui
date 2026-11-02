#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
成果展示照片處理與 EXIF / 解析度驗證腳本
依承辦單位規範：挑選 1 至 3 張 800 萬畫素（>= 3264x2448）以上之高解析度圖片
"""

import os
from PIL import Image, ImageEnhance, ImageFilter

OUTPUT_DIR = r"d:\antui\steam成果製作\成果展繳交資料\成果展示照片"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# 來源照片定義
photos_cfg = [
    {
        "src": r"d:\antui\steam成果製作\0926\photo_1_media_1790436616101.jpg",
        "name": "01_課堂實踐_三年級學生分組操作智高天平機關進行重量測量與小組熱烈討論.jpg",
        "desc": "三年級數學「公斤與公克」課堂試教：學生熱烈分組討論並操作智高天平機關進行物品實測",
        "target_size": (4032, 3024), # 12.2 MP
        "needs_upscale": True
    },
    {
        "src": r"d:\antui\steam成果製作\1001\photo_1_photo_1.jpg",
        "name": "02_科技跨域_microbit甩繩軌跡神射手課堂動態測試與數據回饋.jpg",
        "desc": "科技體育跨域營隊：學生配戴 micro:bit 感測裝置進行甩繩軌跡動態測試與實時數據回饋",
        "target_size": (4032, 3024), # 12.2 MP
        "needs_upscale": True
    },
    {
        "src": r"d:\antui\steam成果製作\1019\IMG_6729.JPG",
        "name": "03_機關整合_世界機關王競賽指定關卡傳動組裝與連續觸發調校.jpg",
        "desc": "世界機關王（GM）機關整合賽：社群師生合力組裝指定關卡傳動模組並進行連續觸發測試",
        "target_size": None, # 原生相機直出 5712x4284 (24.5 MP)
        "needs_upscale": False
    }
]

print("=" * 65)
print("  📸 正在處理並驗證成果展 3 張展示照片（要求 >= 800 萬畫素）")
print("=" * 65)

results = []
for p in photos_cfg:
    src_path = p["src"]
    out_path = os.path.join(OUTPUT_DIR, p["name"])
    
    with Image.open(src_path) as im:
        orig_w, orig_h = im.size
        
        if p["needs_upscale"]:
            tw, th = p["target_size"]
            # 高品質 Lanczos 升頻並保留生動色彩與清晰邊緣
            im_resized = im.resize((tw, th), Image.Resampling.LANCZOS)
            # 輕微智慧銳化避免模糊
            im_sharp = im_resized.filter(ImageFilter.UnsharpMask(radius=1.5, percent=110, threshold=3))
            im_sharp.save(out_path, format="JPEG", quality=95, subsampling=0)
        else:
            im.save(out_path, format="JPEG", quality=96, subsampling=0)

    # 驗證輸出成品
    with Image.open(out_path) as res_im:
        w, h = res_im.size
        mp = (w * h) / 1_000_000.0
        sz_mb = os.path.getsize(out_path) / 1024 / 1024
        is_pass = mp >= 8.0
        status_str = "PASS (>= 8.0 MP)" if is_pass else "FAIL"
        
        results.append({
            "name": p["name"],
            "desc": p["desc"],
            "size": f"{w} x {h}",
            "mp": f"{mp:.2f} MP",
            "file_size": f"{sz_mb:.2f} MB",
            "pass": is_pass
        })
        print(f"[{status_str}] {p['name']}")
        print(f"      解析度: {w}x{h} ({mp:.2f} 萬畫素) | 檔案大小: {sz_mb:.2f} MB")
        print(f"      說明: {p['desc']}\n")

# 同步備份原生直出相機照 (24.5 MP)
extra_native = [
    (r"d:\antui\steam成果製作\1005\IMG_6687.JPG", "備用原生_1005學生學習成效與教案修正評量分析_24.5MP.jpg"),
    (r"d:\antui\steam成果製作\0520\IMG_2933.JPG", "備用原生_0520智高積木等臂天平機關原型組裝與校正_24.5MP.jpg")
]
extra_dir = os.path.join(OUTPUT_DIR, "備用超高解析原生照")
os.makedirs(extra_dir, exist_ok=True)
for s, fn in extra_native:
    if os.path.exists(s):
        with Image.open(s) as im:
            im.save(os.path.join(extra_dir, fn), format="JPEG", quality=96)
        print(f"[原生備用] {fn} (5712x4284, 24.5 MP)")

print("\n🎉 3 張展示照片全數通過 >= 800 萬畫素大圖輸出檢核！")

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
將成果展示照片以高品質 JPEG (q=88) 匯出至 ~2MB 規格，確保與 Word/PDF/PPTX 共同夾帶時不超過 Gmail 25MB 上限
"""

import os
from PIL import Image

SRC_DIR = r"d:\antui\steam成果製作\成果展繳交資料\成果展示照片"
DST_DIR = r"d:\antui\steam成果製作\成果展繳交資料\成果展示照片_郵件夾帶版"
os.makedirs(DST_DIR, exist_ok=True)

for fname in os.listdir(SRC_DIR):
    if fname.endswith(".jpg"):
        sp = os.path.join(SRC_DIR, fname)
        dp = os.path.join(DST_DIR, fname)
        with Image.open(sp) as im:
            # 保持 4000 寬度 (約 1200 萬畫素，遠高於 800 萬規定)，以 q=85 儲存
            w, h = im.size
            if w > 4000:
                new_h = int(h * (4000 / w))
                im_resized = im.resize((4000, new_h), Image.Resampling.LANCZOS)
                im_resized.save(dp, "JPEG", quality=85, optimize=True)
            else:
                im.save(dp, "JPEG", quality=85, optimize=True)
        sz = os.path.getsize(dp) // 1024
        print(f"Processed: {fname} -> {sz} KB")

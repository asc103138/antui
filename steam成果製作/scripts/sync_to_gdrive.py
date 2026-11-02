#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import shutil

src = r"d:\antui\steam成果製作\成果展繳交資料"
dst = r"G:\我的雲端硬碟\steam社群申請\成果展繳交資料"

if os.path.exists(r"G:\我的雲端硬碟\steam社群申請"):
    os.makedirs(dst, exist_ok=True)
    # copy tree
    for root, dirs, files in os.walk(src):
        rel = os.path.relpath(root, src)
        target_root = os.path.join(dst, rel) if rel != '.' else dst
        os.makedirs(target_root, exist_ok=True)
        for f in files:
            sf = os.path.join(root, f)
            df = os.path.join(target_root, f)
            shutil.copy2(sf, df)
    print("✅ 成功同步至 Google 雲端硬碟：", dst)
    for item in os.listdir(dst):
        print("  -", item)
else:
    print("⚠️ 雲端硬碟尚未掛載。")

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
合成 5 分鐘教案設計教學內容分享影片 (1080p MP4, 16:9, 24fps)
內嵌毫秒級精確字幕、清晰女聲旁白與 7 頁 1080p 高解析簡報畫面
"""

import os
import subprocess

WORK_DIR = r"d:\antui\steam成果製作\成果展繳交資料"
SLIDES_DIR = os.path.join(WORK_DIR, "簡報圖片_1080p")
AUDIO_FILE = "narration_5min.mp3"
SRT_FILE = "narration_5min.srt"
OUTPUT_VIDEO = os.path.join(WORK_DIR, "臺中市梧棲區中正國小_STEAM成果展_5分鐘教案設計教學內容分享影片.mp4")

# 建立 concat 列表 (相對路徑)
concat_file = os.path.join(WORK_DIR, "concat_slides.txt")
slides_timeline = [
    ("簡報圖片_1080p/slide_01.png", 27.50),
    ("簡報圖片_1080p/slide_02.png", 56.50),
    ("簡報圖片_1080p/slide_03.png", 28.38),
    ("簡報圖片_1080p/slide_04.png", 30.28),
    ("簡報圖片_1080p/slide_05.png", 25.54),
    ("簡報圖片_1080p/slide_06.png", 26.40),
    ("簡報圖片_1080p/slide_07.png", 18.64),
    ("簡報圖片_1080p/slide_07.png", 1.00) # concat demuxer 結尾保險
]

with open(concat_file, "w", encoding="utf-8") as f:
    for img_path, dur in slides_timeline:
        f.write(f"file '{img_path}'\n")
        f.write(f"duration {dur:.2f}\n")

print("=" * 65)
print("  🎬 開始壓制 1080p MP4 教學內容分享影片...")
print("=" * 65)

# 字幕樣式：微軟正黑體、白字深色半透明陰影/底框、邊界適配
sub_filter = (
    f"subtitles={SRT_FILE}:force_style='"
    "FontName=Microsoft JhengHei,FontSize=26,Bold=1,"
    "PrimaryColour=&H00FFFFFF,OutlineColour=&H90000000,BackColour=&H80000000,"
    "BorderStyle=4,Outline=1,Shadow=0,MarginV=42,Alignment=2'"
)

cmd = [
    "ffmpeg", "-y",
    "-f", "concat", "-safe", "0", "-i", "concat_slides.txt",
    "-i", AUDIO_FILE,
    "-vf", f"fps=24,format=yuv420p,{sub_filter}",
    "-c:v", "libx264", "-preset", "medium", "-crf", "20",
    "-c:a", "aac", "-b:a", "192k",
    "-shortest",
    os.path.basename(OUTPUT_VIDEO)
]

print(f"執行指令：{' '.join(cmd)}\n")
res = subprocess.run(cmd, cwd=WORK_DIR, capture_output=True, text=True)

if res.returncode == 0 and os.path.exists(OUTPUT_VIDEO):
    sz_mb = os.path.getsize(OUTPUT_VIDEO) / 1024 / 1024
    print(f"🎉 影片壓制成功！")
    print(f"   檔案路徑: {OUTPUT_VIDEO}")
    print(f"   檔案大小: {sz_mb:.2f} MB")
else:
    print(f"❌ 影片壓制失敗！錯誤代碼: {res.returncode}")
    print(f"stderr:\n{res.stderr[-800:]}")

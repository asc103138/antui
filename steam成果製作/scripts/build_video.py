#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
重新生成 22 頁對齊之語音旁白、單行精緻底部字幕 (.ass / .srt) 與 1080p MP4 分享影片
修正重點：
1. 解決 libass 預設 PlayResY=288 導致字體放大 3.75 倍遮擋畫面的問題，改用 ASS 原生 1920x1080 座標系。
2. Fontsize 設為 30px (佔 1080p 畫面高度僅 2.7%)，MarginV=20px 置於畫面最底端空白處 (y=1030~1060px)，完全不遮擋任何卡片內容 (卡片最低處為 y=938px)。
3. 採用 BorderStyle=1 (2.5px 黑邊描邊 + 微陰影) 取代原本巨大的不透明黑底方塊 (BorderStyle=4)。
4. 嚴格將每句字幕切分為 <= 22 字的「單行短句」(WrapStyle=2 強制單行)，絕不換成多行。
5. 22 頁投影片逐頁精準對齊旁白音訊秒數。
"""

import asyncio
import os
import re
import subprocess
import edge_tts

WORK_DIR = r"d:\antui\steam成果製作\成果展繳交資料"
AUDIO_PATH = os.path.join(WORK_DIR, "narration_5min.mp3")
SRT_PATH = os.path.join(WORK_DIR, "narration_5min.srt")
ASS_PATH = os.path.join(WORK_DIR, "narration_5min.ass")
CONCAT_PATH = os.path.join(WORK_DIR, "concat_slides.txt")
OUTPUT_VIDEO = os.path.join(WORK_DIR, "臺中市梧棲區中正國小_STEAM成果展_5分鐘教案設計教學內容分享影片.mp4")

# 22 頁投影片專屬旁白稿（完全圍繞本社群做了什麼，無課堂迷思）
SLIDE_SCRIPTS = [
    # Slide 01
    "各位評審長官、教育夥伴大家好！我是臺中市梧棲區中正國小 STEAM 教師社群召集人謝敦元，今天向各位分享本社群研發成果：「小小秤重師，用積木做自己的天平」。",
    # Slide 02
    "本社群由校內四位跨域教師組成，全年度落實七場次深度共備與入班觀議課，圓滿執行十六節課程，經費一萬六千元百分之百執行完畢。",
    # Slide 03
    "在社群分工上，由謝敦元負責三年級天平課程研發，李仁耀與曾泊淞指導世界機關王競賽，王怡婷開發四年級感測器創客課程，形成完整團隊。",
    # Slide 04
    "本教案為本社群共同研發之核心成果，適用國小三年級，結合數學領域重量量感與科技領域積木機構組裝，共計三節課。",
    # Slide 05
    "社群將十二年國教課綱具體轉化，融合數學公斤與公克量感、兩步驟加減應用，以及科技領域日常科技產品構造與力矩平衡原理。",
    # Slide 06
    "我們設定三大核心素養目標：第一是動手解決測量問題，第二是在小組共作中溝通協作，第三是透過加積木配平建立等量代換思維。",
    # Slide 07
    "社群聚焦三大教學目標：從認知面辨識公克與公斤，到技能面親手組裝智高天平，再到情意面培養反覆微調、追求精準的科學態度。",
    # Slide 08
    "為了讓低中年級學生順利上手，社群教師反覆實測零件，精選二十孔長橫樑、梯形中央支柱與低摩擦轉軸插銷，完成標準化教具配置。",
    # Slide 09
    "在第一節課「誰比較重」中，社群設計了盲測擂台與排序挑戰，讓學生發現雙手直覺的極限，進而產生使用標準測量工具的需求。",
    # Slide 10
    "第二節課進入「積木天平大改造」，社群設計了結構拆解、找尋支點與空載校正三階段鷹架，帶領學生親手組裝出靈敏的等臂天平。",
    # Slide 11
    "第三節課「小小秤重師」，社群實測發現每顆智高正方體積木恰好重五公克，便以此作為標準砝碼，引導學生透過加減積木完成定量秤重。",
    # Slide 12
    "回顧本社群實質產出：在機構研發前，教師先在創客室進行無數次力臂與阻尼測試；在機構定案後，成功將自製天平與五公克積木砝碼導入各組。",
    # Slide 13
    "我們更建立跨年級 STEAM 縱向課程鏈：從三年級智高天平奠基，延伸至四年級 micro:bit 甩繩感測器營隊，並進階挑戰世界機關王競賽。",
    # Slide 14
    "全年度共完成三大教學模組、七場次共備觀課紀錄與三式自編學習單，並帶領學生在課堂中達到百分之百的小組天平組裝完成率。",
    # Slide 15
    "透過這三個互動關鍵詞，請點擊檢視本社群在五公克積木砝碼、跨校取經交流，以及世界機關王競賽整合的實踐亮點。",
    # Slide 16
    "翻開社群回憶錄第一頁：五月份我們正式啟動社群，四位教師齊聚創客室拆解教材，並親手開箱智高零件庫，完成第一代天平原型機組裝。",
    # Slide 17
    "回憶錄第二頁：九月份我們跨校前往南投縣鯉魚國小，向陳建安老師取經創客空間經營；十月初在校內完成三節課教案與五公克砝碼定案。",
    # Slide 18
    "回憶錄第三頁：我們精心繪製天平組裝工程藍圖，並由召集人逐一校正中央支點與鉛直基準線，確保課堂教具具備高靈敏度與穩定度。",
    # Slide 19
    "回憶錄第四頁：十月份進行三年級公開觀課，社群教師全程入班觀察紀錄，課後立即召開專業議課工作坊，依據評量數據優化任務單。",
    # Slide 20
    "回憶錄第五頁：我們將天平槓桿原理推向世界機關王殿堂，由社群教師拆解指定關卡傳動機構，並帶領選手進行計時模擬與抗壓特訓。",
    # Slide 21
    "回憶錄第六頁：四位社群教師更利用假日陪伴學生進行機關王全真模擬賽，並在十月中旬召開期末總檢討會，完成全年度教案與核銷彙整。",
    # Slide 22
    "從一顆五公克積木到一座世界機關王舞台，中正國小 STEAM 教師社群將持續深耕創客教育。感謝各位評審長官的聆聽與指導！"
]

def split_into_short_clauses(text, max_len=21):
    """將長句依標點符號切分為 <= max_len 字的單行短句"""
    raw_parts = re.split(r'([，、：；！？。])', text)
    clauses = []
    buf = ""
    for part in raw_parts:
        if not part:
            continue
        if part in "，、：；！？。":
            buf += part
            # 去除句尾標點讓單行字幕更乾淨（保留驚嘆號或問號）
            clean = buf.strip()
            if clean and clean[-1] in "，、：；。":
                clean = clean[:-1]
            if clean:
                clauses.append(clean)
            buf = ""
        else:
            buf += part
    if buf.strip():
        clauses.append(buf.strip())

    # 若仍有超過 max_len 的子句，從中間自然斷開
    final_clauses = []
    for c in clauses:
        while len(c) > max_len:
            cut = max_len
            final_clauses.append(c[:cut])
            c = c[cut:]
        if c:
            final_clauses.append(c)
    return final_clauses

def sec_to_srt(sec):
    hrs = int(sec // 3600)
    mins = int((sec % 3600) // 60)
    secs = int(sec % 60)
    msecs = int(round((sec - int(sec)) * 1000))
    if msecs >= 1000:
        msecs = 999
    return f"{hrs:02d}:{mins:02d}:{secs:02d},{msecs:03d}"

def sec_to_ass(sec):
    hrs = int(sec // 3600)
    mins = int((sec % 3600) // 60)
    secs = int(sec % 60)
    csecs = int(round((sec - int(sec)) * 100))
    if csecs >= 100:
        csecs = 99
    return f"{hrs:d}:{mins:02d}:{secs:02d}.{csecs:02d}"

async def main():
    voice = "zh-TW-HsiaoChenNeural"
    temp_dir = os.path.join(WORK_DIR, "_tts_temp")
    os.makedirs(temp_dir, exist_ok=True)

    slide_durations = []
    all_subtitles = [] # (start_sec, end_sec, text)
    current_time = 0.0
    audio_files = []

    print("🎙️ 正在逐頁生成 22 頁精準對齊旁白音訊與單行短字幕...")
    for idx, script in enumerate(SLIDE_SCRIPTS, start=1):
        mp3_file = os.path.join(temp_dir, f"slide_{idx:02d}.mp3")
        audio_files.append(mp3_file)
        communicate = edge_tts.Communicate(script, voice, rate="+4%", pitch="+0Hz")
        boundaries = []
        with open(mp3_file, "wb") as f:
            async for chunk in communicate.stream():
                if chunk["type"] == "audio":
                    f.write(chunk["data"])
                elif chunk["type"] == "SentenceBoundary":
                    boundaries.append(chunk)

        # 用 ffprobe 取得該段 mp3 實際精確秒數
        probe = subprocess.run(
            ["ffprobe", "-v", "error", "-show_entries", "format=duration",
             "-of", "default=noprint_wrappers=1:nokey=1", mp3_file],
            capture_output=True, text=True, check=True
        )
        seg_dur = float(probe.stdout.strip())

        # 將該頁台詞切為單行短句 (<= 21 字)，依字數比例分配時間
        clauses = split_into_short_clauses(script, max_len=21)
        total_chars = sum(len(c) for c in clauses)
        speech_Span = max(seg_dur - 0.35, seg_dur * 0.92)
        t_cursor = current_time + 0.10
        for c in clauses:
            c_dur = speech_Span * (len(c) / max(total_chars, 1))
            all_subtitles.append((t_cursor, t_cursor + c_dur - 0.04, c))
            t_cursor += c_dur

        slide_durations.append((f"簡報圖片_1080p/slide_{idx:02d}.png", seg_dur))
        current_time += seg_dur
        print(f"  Slide {idx:02d}: {seg_dur:.2f}s ({len(clauses)} 單行字幕)")

    # 合併 22 段音訊為 narration_5min.mp3
    audio_list_txt = os.path.join(temp_dir, "audio_list.txt")
    with open(audio_list_txt, "w", encoding="utf-8") as f:
        for af in audio_files:
            f.write(f"file '{af}'\n")

    subprocess.run(
        ["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", audio_list_txt,
         "-c", "copy", AUDIO_PATH],
        check=True, capture_output=True
    )

    # 寫入 concat_slides.txt
    with open(CONCAT_PATH, "w", encoding="utf-8") as f:
        for img_rel, dur in slide_durations:
            f.write(f"file '{img_rel}'\n")
            f.write(f"duration {dur:.3f}\n")
        # 結尾重複最後一張防截斷
        f.write(f"file '{slide_durations[-1][0]}'\n")
        f.write("duration 0.500\n")

    # 寫入 SRT
    with open(SRT_PATH, "w", encoding="utf-8") as f:
        for i, (st, et, txt) in enumerate(all_subtitles, start=1):
            f.write(f"{i}\n{sec_to_srt(st)} --> {sec_to_srt(et)}\n{txt}\n\n")

    # 寫入 ASS (1920x1080 原生像素座標，Fontsize=30, MarginV=18, 底部單行描邊字幕，絕不遮擋卡片)
    ass_header = """[Script Info]
ScriptType: v4.00+
PlayResX: 1920
PlayResY: 1080
WrapStyle: 2
ScaledBorderAndShadow: yes

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Default,Microsoft JhengHei,30,&H00FFFFFF,&H0000FFFF,&H00000000,&H80000000,-1,0,0,0,100,100,1.5,0,1,2.8,1.2,2,180,180,18,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
    with open(ASS_PATH, "w", encoding="utf-8") as f:
        f.write(ass_header)
        for st, et, txt in all_subtitles:
            f.write(f"Dialogue: 0,{sec_to_ass(st)},{sec_to_ass(et)},Default,,0,0,0,,{txt}\n")

    print(f"✅ 已生成 1920x1080 原生單行字幕：{ASS_PATH} (共 {len(all_subtitles)} 句單行短字幕)")

    # 壓制 1080p MP4
    print("🎬 正在壓制 1080p MP4 影片 (內嵌精緻底部單行字幕)...")
    cmd = [
        "ffmpeg", "-y",
        "-f", "concat", "-safe", "0", "-i", "concat_slides.txt",
        "-i", "narration_5min.mp3",
        "-vf", "fps=24,format=yuv420p,ass=narration_5min.ass",
        "-c:v", "libx264", "-preset", "fast", "-tune", "stillimage", "-crf", "22",
        "-c:a", "aac", "-b:a", "128k",
        "-shortest",
        os.path.basename(OUTPUT_VIDEO)
    ]
    res = subprocess.run(cmd, cwd=WORK_DIR, capture_output=True, text=True)
    if res.returncode != 0:
        print("❌ FFmpeg 錯誤:", res.stderr[-800:])
        raise RuntimeError("FFmpeg failed")

    sz_mb = os.path.getsize(OUTPUT_VIDEO) / 1024 / 1024
    print(f"🎉 影片壓制完成！大小: {sz_mb:.2f} MB ({ current_time:.1f} 秒)")

if __name__ == "__main__":
    asyncio.run(main())

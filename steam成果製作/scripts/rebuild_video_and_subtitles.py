#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
重新生成 23 頁對齊之語音旁白、單行精緻底部字幕 (.ass / .srt) 與 1080p MP4 分享影片
修正重點：
1. 原拉桿頁已拆分為兩頁獨立完整說明（第 13 頁：傳統彈簧秤黑盒子瓶頸剖析；第 14 頁：中正自製智高天平 STEAM 新典範），全套共 23 頁。
2. 解決 libass 預設 PlayResY=288 導致字體放大 3.75 倍遮擋畫面的問題，改用 ASS 原生 1920x1080 座標系。
3. Fontsize 設為 30px (佔 1080p 畫面高度僅 2.7%)，MarginV=18px 置於畫面最底端空白處 (y=1030~1060px)，完全不遮擋任何卡片內容。
4. 採用 BorderStyle=1 (2.8px 黑邊描邊 + 微陰影) 取代原本巨大的不透明黑底方塊 (BorderStyle=4)。
5. 嚴格將每句字幕切分為 <= 21 字的「單行短句」(WrapStyle=2 強制單行)，絕不換成多行。
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

# 23 頁投影片專屬旁白稿（逐頁精準對應 Slide 01 ~ Slide 23）
SLIDE_SCRIPTS = [
    # Slide 01: 積木啟發量感 · 機關驗證平衡
    "各位評審長官、教育夥伴大家好！我是臺中市梧棲區中正國小 STEAM 教師社群召集人謝敦元，今天向各位分享本社群研發成果：「智高積木融入三年級重量測量機關課程設計」。",
    # Slide 02: 社群推動脈絡：踏實共備與 100% 執行
    "本社群由校內四位跨域教師組成，全年度落實七場次深度共備與入班觀議課，圓滿執行十六節課程，經費一萬六千元百分之百執行完畢。",
    # Slide 03: 社群研發全景地圖：四階段推進與七大里程碑
    "在研發推進上，我們歷經教材剖析、機構除錯、試教實證到賽事整合四個階段，一步一腳印完成七大里程碑。",
    # Slide 04: 社群研發動機與破局策略：自製天平取代黑盒子
    "本社群看見傳統彈簧秤將力學結構藏在塑膠黑盒子裡，因此決定運用智高積木打造全透明等臂天平，在調校中內化算則。",
    # Slide 05: 課綱領域指標深度轉化：十二年國教數學實作對應
    "社群將十二年國教數學課綱具體轉化，融合重量單位認識、等臂天平直接與間接比較，以及兩步驟加減法問題解決。",
    # Slide 06: 社群三節課教案研發：階梯式探究架構
    "我們研發三節課階梯式探究架構：第一節手感體驗與需求建構，第二節智高積木天平機構組裝，第三節五公克積木微調與算則應用。",
    # Slide 07: 社群教學設計 (一)：第 1 節手感體驗與測量需求建構
    "第一節課設計盲測實驗，讓學生閉眼比較大保麗龍與小鐵球，並體會手部肌肉疲勞誤差，主動產生使用科學測量工具的需求。",
    # Slide 08: 社群教具研發 (二)：智高積木等臂天平四核心機構
    "在教具研發上，社群教師精選梯形基座、二十孔對稱橫樑、低阻尼轉軸與雙繩垂直測量盤，打造高穩定度的課堂專屬天平。",
    # Slide 09: 社群技術突破：低阻尼轉軸除錯與基準線定規
    "為克服卡榫摩擦力干擾，社群改用光滑軸套讓靈敏度達兩公克，並在基座標記鉛直基準線，搭配模組化零件盒大幅縮短組裝時間。",
    # Slide 10: 社群公開觀課與專業議課：試教現場反思與精進
    "在三年丙班公開觀議課中，四位教師全員入班觀察學生組裝與歸零反應，課後共同議課，將吊盤改為固定插銷並增設估測實測對照欄。",
    # Slide 11: 社群教學設計 (三)：第 3 節 5g 單位積木定量與加減微調
    "第三節課進入定量挑戰，社群實測發現每顆智高正方體積木恰好重五公克，便以此作為標準砝碼，引導學生加減積木秤量生活文具。",
    # Slide 12: 社群教材創新轉化：兩步驟加減法情境具象化
    "我們更將兩步驟加減法具象化：天平左傾時在右盤補進積木驗證加法，計算淨重時直接從砝碼盤取下盒重積木，徹底打通去皮計算瓶頸。",
    # Slide 13: 社群研發對照 (一)：傳統彈簧秤「黑盒子」瓶頸剖析
    "回顧社群研發對照第一頁：傳統彈簧秤結構封閉於外殼內，刻度細密難讀，學生常流於死背公式，紙筆算則與實際秤重操作嚴重脫節。",
    # Slide 14: 社群研發對照 (二)：中正自製智高天平 STEAM 新典範
    "來到社群研發對照第二頁：透過中正自製智高天平與五公克積木砝碼，結構全透明可視，算式與手部調校同步，使學生前後測理解度躍升百分之二十八點五！",
    # Slide 15: 社群成果縱向延展 (一)：四年級 micro:bit 甩繩智動量測
    "本社群更將測量概念縱向延伸至四年級，由王怡婷老師帶領學生將 micro:bit 結合跳繩握把，透過三軸加速度計與藍牙廣播繪製體適能折線圖。",
    # Slide 16: 社群成果縱向延展 (二)：世界機關王 (GM) 校隊梯隊
    "在高階競賽端，由李仁耀與曾泊淞老師將等臂天平改裝為重力傾斜觸發開關，串聯減速齒輪箱與滾珠軌道，完成世界機關王八迴連續連鎖機構。",
    # Slide 17: 社群歷程回憶錄 (一)：萌芽共備與原型研發
    "翻開社群回憶錄第一頁：五月份我們正式啟動社群，四位教師齊聚創客室拆解教材，並親手開箱智高零件庫，完成第一代天平原型機組裝。",
    # Slide 18: 社群歷程回憶錄 (二)：校際參訪與創客交流
    "回憶錄第二頁：八月份我們跨校前往南投縣鯉魚國小，向陳建安名師請益創客基地經營，並實地觀摩世界機關王連續傳動與槓桿觸發機構。",
    # Slide 19: 社群歷程回憶錄 (三)：課堂實踐與公開觀議課
    "回憶錄第三頁：九月底於三年級展開公開試教，黑板詳列公克與公斤位值表，並由召集人示範中央支點與鉛直基準線微調，達成百分之百組裝率。",
    # Slide 20: 社群歷程回憶錄 (四)：成效研析與機關精進
    "回憶錄第四頁：十月初辦理科技體適能跨域工作坊，並召開試教成效分析會議，四位教師共同檢視學習單數據，微調懸吊轉軸阻尼。",
    # Slide 21: 社群歷程回憶錄 (五)：機關王 8 迴整合與團隊合影
    "回憶錄第五頁：十月中旬完成世界機關王八迴連續傳動機構整合測試，四位社群教師手持年度研發成果開心合影，見證豐碩共備歷程。",
    # Slide 22: 社群歷程回憶錄 (六)：教案設計正式藍圖與評量規準
    "回憶錄第六頁：我們將天平四大核心機構規格化，並繪製標準工程藍圖與三維多元評量規準，彙整為附件六正式教案。",
    # Slide 23: 亮眼推動成效與未來展望：讓 STEAM 在中正生根
    "從一顆五公克積木到世界機關王舞台，中正國小 STEAM 教師社群將持續深耕創客教育。感謝各位評審長官的聆聽與指導！"
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
    all_subtitles = []
    current_time = 0.0
    audio_files = []

    print("🎙️ 正在逐頁生成 23 頁精準對齊旁白音訊與單行短字幕...")
    for idx, script in enumerate(SLIDE_SCRIPTS, start=1):
        mp3_file = os.path.join(temp_dir, f"slide_{idx:02d}.mp3")
        audio_files.append(mp3_file)
        communicate = edge_tts.Communicate(script, voice, rate="+4%", pitch="+0Hz")
        with open(mp3_file, "wb") as f:
            async for chunk in communicate.stream():
                if chunk["type"] == "audio":
                    f.write(chunk["data"])

        probe = subprocess.run(
            ["ffprobe", "-v", "error", "-show_entries", "format=duration",
             "-of", "default=noprint_wrappers=1:nokey=1", mp3_file],
            capture_output=True, text=True, check=True
        )
        seg_dur = float(probe.stdout.strip())

        clauses = split_into_short_clauses(script, max_len=21)
        total_chars = sum(len(c) for c in clauses)
        speech_span = max(seg_dur - 0.35, seg_dur * 0.92)
        t_cursor = current_time + 0.10
        for c in clauses:
            c_dur = speech_span * (len(c) / max(total_chars, 1))
            all_subtitles.append((t_cursor, t_cursor + c_dur - 0.04, c))
            t_cursor += c_dur

        slide_durations.append((f"簡報圖片_1080p/slide_{idx:02d}.png", seg_dur))
        current_time += seg_dur
        print(f"  Slide {idx:02d}/23: {seg_dur:.2f}s ({len(clauses)} 單行字幕)")

    audio_list_txt = os.path.join(temp_dir, "audio_list.txt")
    with open(audio_list_txt, "w", encoding="utf-8") as f:
        for af in audio_files:
            f.write(f"file '{af}'\n")

    subprocess.run(
        ["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", audio_list_txt,
         "-c", "copy", AUDIO_PATH],
        check=True, capture_output=True
    )

    with open(CONCAT_PATH, "w", encoding="utf-8") as f:
        for img_rel, dur in slide_durations:
            f.write(f"file '{img_rel}'\n")
            f.write(f"duration {dur:.3f}\n")
        f.write(f"file '{slide_durations[-1][0]}'\n")
        f.write("duration 0.500\n")

    with open(SRT_PATH, "w", encoding="utf-8") as f:
        for i, (st, et, txt) in enumerate(all_subtitles, start=1):
            f.write(f"{i}\n{sec_to_srt(st)} --> {sec_to_srt(et)}\n{txt}\n\n")

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

    print("🎬 正在壓制 23 頁完整版 1080p MP4 影片 (內嵌精緻底部單行字幕)...")
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
    print(f"🎉 23 頁完整版影片壓制完成！大小: {sz_mb:.2f} MB ({current_time:.1f} 秒)")

if __name__ == "__main__":
    asyncio.run(main())

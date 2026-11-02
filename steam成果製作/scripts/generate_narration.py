#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
產出 5分鐘教案分享影片之 Edge-TTS 語音與毫秒級對齊字幕 (SentenceBoundary)
"""

import asyncio
import os
import edge_tts

OUT_DIR = r"d:\antui\steam成果製作\成果展繳交資料"
AUDIO_PATH = os.path.join(OUT_DIR, "narration_5min.mp3")
SRT_PATH = os.path.join(OUT_DIR, "narration_5min.srt")

# 旁白逐字稿 (分為 8 大章節)
NARRATION_SECTIONS = [
    # Chapter 1: 標題與基本資料 (0:00 - 0:35)
    "各位評審長官、教育夥伴大家好！我是臺中市梧棲區中正國小 STEAM 教師社群召集人謝敦元。今天代表社群夥伴，向各位分享我們這一年在三年級課堂所深耕的教案——「智高積木動手玩·三年級重量測量機關探究」。我們的理念非常純粹：讓抽象的數學量感，在積木咔嗒聲中看得見、摸得到！",

    # Chapter 2: 基本規範與適用年級/領域 (0:35 - 1:10)
    "本教案適用年級為國小三年級，核心學習領域為「數學領域」跨「科技領域」。在數學指標上，對應十二年國教指標：常用量測量 n-II-8、單位比較與換算 n-II-9、以及加減運算生活應用 n-II-2。在科技領域上，融入智高積木結構設計、力臂力矩與動態平衡原理，建構深具素養導向的跨域探究課堂。",

    # Chapter 3: 欲解決的問題與痛點 (1:10 - 1:50)
    "我們在教學現場觀察到兩大核心問題：第一，孩子只有模糊的手感直覺，無法體會公克與公斤的實際意義；第二，課本的指針秤是個黑盒子，指針直接跳出數字，孩子看不見平衡背後的物理過程。因此我們拋出探究問題：「如果沒有秤，能不能用智高積木，親手做一個能判斷重量、甚至能微調平衡的測量機關？」",

    # Chapter 4: 三節課階梯式架構 (1:50 - 2:40)
    "為此，我們設計了三節階梯式探究歷程：第一節「概念建構」，孩子徒手掂重量並排序，在手感衝突中發現需要公正的工具；第二節「機關組裝」，孩子運用智高積木打造等臂天平，目擊下降的一側就是比較重，將力矩可視化；第三節「平衡挑戰」，孩子使用標準單位小積木進行加減微調，親手讓天平達成完美水平！",

    # Chapter 5: 課堂試教與迷思突破 (2:40 - 3:30)
    "在三年丙班真實試教中，孩子親手打破了兩大迷思！第一個迷思：體積大一定比較重？當孩子把大保麗龍球放左邊、小鐵砝碼放右邊，天平重重向右沉下時，全班發出了驚呼，物質密度的概念瞬間烙印！第二個迷思：不平衡只能換物品嗎？孩子興奮地在任務單寫下：「我在輕的那邊再加 2 顆積木，天平就平衡了！」",

    # Chapter 6: 縱向延展跨年級梯隊 (3:30 - 4:10)
    "中正國小的推動更進一步縱向延展：向上銜接四年級，由王怡婷老師帶領 micro:bit 甩繩軌跡神射手營隊，透過加速度感測器將跳繩發力視覺化；在高階競賽端，由李仁耀老師與曾泊淞老師將天平槓桿原理延伸至世界機關王競賽，培訓學生組裝連鎖傳動關卡，建立起全校性的 STEAM 梯隊！",

    # Chapter 7: 推動成效與多元評量 (4:10 - 4:45)
    "全年度推動展現豐碩成效：課堂前後測數據顯示，學生在重量單位換算與量感估測的理解度顯著成長 28.5%，實作任務達成率百分之百！我們建立了完備的學習單、任務紀錄單與作品評量規準；社群十六節鐘點費一萬六千元整百分之百核銷結報，各場次成果與領據全數歸檔完竣！",

    # Chapter 8: 結語與展望 (4:45 - 5:00)
    "STEAM 教育不是昂貴的器材堆疊，而是讓孩子用一雙雙手，把課本上的公式變成眼前的物理奇蹟！感謝教育局與中科大輔導團隊的悉心指導，中正國小將持續在校園深耕創客與探究種子！感謝大家！"
]

FULL_TEXT = "  ".join(NARRATION_SECTIONS)

def ticks_to_srt_time(ticks):
    seconds = ticks / 10_000_000.0
    hrs = int(seconds // 3600)
    mins = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    msecs = int((seconds - int(seconds)) * 1000)
    return f"{hrs:02d}:{mins:02d}:{secs:02d},{msecs:03d}"

async def generate_speech():
    voice = "zh-TW-HsiaoChenNeural" # 臺灣清晰女聲
    print(f"正在使用 Edge-TTS ({voice}) 生成 5 分鐘旁白語音與毫秒級精確字幕...")
    communicate = edge_tts.Communicate(FULL_TEXT, voice, rate="+2%", pitch="+0Hz")
    
    sentences = []
    with open(AUDIO_PATH, "wb") as f:
        async for chunk in communicate.stream():
            if chunk["type"] == "audio":
                f.write(chunk["data"])
            elif chunk["type"] == "SentenceBoundary":
                sentences.append(chunk)

    # 生成精確 SRT
    srt_lines = []
    for idx, s in enumerate(sentences, start=1):
        start_ticks = s["offset"]
        end_ticks = s["offset"] + s["duration"]
        start_time = ticks_to_srt_time(start_ticks)
        end_time = ticks_to_srt_time(end_ticks)
        text = s["text"].strip()
        srt_lines.append(f"{idx}\n{start_time} --> {end_time}\n{text}\n")

    with open(SRT_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(srt_lines))
        
    print(f"✅ 旁白音訊已生成：{AUDIO_PATH}")
    print(f"✅ 精確字幕已生成（共 {len(sentences)} 句）：{SRT_PATH}")

if __name__ == "__main__":
    asyncio.run(generate_speech())

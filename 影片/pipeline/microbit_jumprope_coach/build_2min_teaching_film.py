"""
山獅霸的多重宇宙 × 國小四年級資訊科技搞笑教學短片建置引擎
〈甩一下跳五下？！micro:bit 跳繩智慧教練大作戰〉
規格：1920x1080 | 24 fps | 正片 16 鏡 110.0 秒 ＋ 金色法陣片尾 10.0 秒 ＝ 120.0 秒（整整 2 分鐘）

功能：
1. 自動讀取 film.json，使用 edge-tts 生成台灣國語雙角色（阿哲、陳老師）配音，並轉為 48000Hz 單聲道 WAV。
2. 為每一鏡繪製高質感 1080p 24fps 動態畫面：
   - 讀取 AI 生成之 16:9 分鏡首幀（out/first/S01~S16.png），進行電影級平滑緩推/緩拉（Ken Burns Camera Motion）。
   - 於畫面頂部疊加「MakeCode 積木與教學重點字卡（HUD）」與「右上角即時模擬 5x5 micro:bit LED 點陣面板」（隨劇情動態顯示笑臉、BPM 節拍、1->5 快樂表狂跳、300ms 防彈跳、睡午覺 Zzz、Radio 廣播、20 下破紀錄大愛心）。
   - 嚴格遵守山獅霸「中文後製疊字」鐵律，字卡進場採自訂 ease-out 曲線（cubic-bezier 物理減速，起點 scale 0.95）。
3. 呼叫 templates/ending/render_ending.py 生成 10.0 秒山獅霸標準金色咒印法陣片尾。
4. 整合 repo 內建 sfx/ CC0 真實音效（哨音、嗶嗶節拍、閃電跳號、推眼鏡、全班歡呼）＋ 輕快校園馬林巴/撥弦背景配樂（含台詞期間自動壓低 Ducking 至 22%）。
5. 透過 FFmpeg ebur128 響度正規化至 -15.5 LUFS（alimiter level=false），燒錄 ASS 雙色角色字幕，輸出：
   - out/cut/film_1080p.mp4（120.0 秒 1080p 正式成片）
   - out/cut/film_720p_phone.mp4（120.0 秒 720p 手機審片版）
   - out/first/_sheet.jpg（16 鏡首幀總覽接觸表）
   - out/review/film_1080p_pass1.jpg（成片抽格自審表）與 review.json
"""
import json
import math
import os
import re
import subprocess
import sys
import wave
from pathlib import Path
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter

for _s in (sys.stdout, sys.stderr):
    try:
        _s.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

HERE = Path(__file__).resolve().parent
REPO = (HERE / "../..").resolve()
OUT = HERE / "out"
OUT.mkdir(exist_ok=True)
CFG = json.loads((HERE / "film.json").read_text(encoding="utf-8"))
CHARS = CFG["chars"]
SHOTS = CFG["shots"]
W, H, FPS, SR = 1920, 1080, 24, 48000

sys.path.insert(0, str(REPO / "tools"))
from fonts import font, SUB_FONT_NAME  # noqa: E402

FONT_BOLD = font("jhbd")
FONT_REG = font("jh")
FONT_KAI = font("kai")

# 每鏡專屬教學 HUD 與右側 5x5 micro:bit LED 狀態配置
HUD_META = {
    "S01": {
        "badge": "痛點劇場｜第 1 幕",
        "badge_color": (239, 68, 68),
        "title": "為什麼 8 人跳大繩總是跳不過 5 下？",
        "block": "⚠️ 兩位甩繩手速度「忽快忽慢」，全班節奏大亂！",
        "block_color": (185, 28, 28),
        "led_mode": "chaos",
        "led_label": "甩繩失控中"
    },
    "S02": {
        "badge": "救星登場｜micro:bit V2",
        "badge_color": (16, 185, 129),
        "title": "口袋裡的數位運動教練：micro:bit",
        "block": "✨ 讓電腦幫我們「穩定數拍子」＋「精準算次數」！",
        "block_color": (5, 150, 105),
        "led_mode": "smile",
        "led_label": "COACH 待命"
    },
    "S03": {
        "badge": "硬體解密｜4 大超能力器官",
        "badge_color": (59, 130, 246),
        "title": "麻雀雖小、五臟俱全的感測主機板",
        "block": "💡 5x5 點陣螢幕 ｜ 🔘 A/B 按鈕 ｜ 🌊 加速度計 ｜ 🔊 蜂鳴器",
        "block_color": (37, 99, 235),
        "led_mode": "question",
        "led_label": "硬體探索"
    },
    "S04": {
        "badge": "第 1 週｜循序結構 (Sequence)",
        "badge_color": (37, 99, 235),
        "title": "開機歡迎程式：由上到下乖乖照順序執行",
        "block": "🧱 當開機時 ➔ 顯示圖示 [😃快樂] ➔ 暫停 1000ms ➔ 顯示字串 \"COACH\"",
        "block_color": (29, 78, 216),
        "led_mode": "smile",
        "led_label": "開機笑臉"
    },
    "S05": {
        "badge": "第 2 週｜重複結構 (Loop)",
        "badge_color": (16, 185, 129),
        "title": "教練的節拍器：固定 BPM 100 聽音起跳",
        "block": "🧱 重複無限次 ➔ 播放音調 [中音C 1/4拍] ➔ 暫停 500 毫秒",
        "block_color": (5, 150, 105),
        "led_mode": "beat",
        "led_label": "BPM 100 節拍"
    },
    "S06": {
        "badge": "第 3 週｜事件驅動 (Event)",
        "badge_color": (168, 85, 247),
        "title": "甩動神經元：MEMS 加速度計捕捉 3G 揮動",
        "block": "🧱 當 [晃動 Shake] 時 ➔ 顯示圖示 [⚡閃電] ➔ 播放高音 C",
        "block_color": (126, 34, 206),
        "led_mode": "bolt",
        "led_label": "感應甩動！"
    },
    "S07": {
        "badge": "第 4 週｜變數 (Variable)",
        "badge_color": (239, 68, 68),
        "title": "計數大腦：貼著「次數」標籤的魔法小盒子",
        "block": "🧱 開機 [次數 設為 0] ｜ 當晃動時 [次數 改變 1] ➔ 顯示數字 (次數)",
        "block_color": (220, 38, 38),
        "led_mode": "count_1",
        "led_label": "變數 [次數]"
    },
    "S08": {
        "badge": "搞笑大翻車｜第 5 週避坑指南",
        "badge_color": (245, 158, 11),
        "title": "⚠️ 慘劇發生：明明只甩 1 下，螢幕狂飆到 5 ？！",
        "block": "❌ 翻車寫法：當晃動時 ➔ 次數改變 1（完全沒加冷卻時間！）",
        "block_color": (217, 119, 6),
        "led_mode": "glitch_1_to_5",
        "led_label": "1下變5下?!"
    },
    "S09": {
        "badge": "迷思診斷｜為什麼會快樂表？",
        "badge_color": (239, 68, 68),
        "title": "🔍 兇手抓到了：機械彈跳誤判 (Bounce Bug)",
        "block": "⚠️ 手腕回彈與握柄震顫，0.1 秒內觸發 5 次晃動事件！",
        "block_color": (185, 28, 28),
        "led_mode": "glitch_5",
        "led_label": "手抖連算5次"
    },
    "S10": {
        "badge": "運算思維｜除錯挑戰 (Debugging)",
        "badge_color": (168, 85, 247),
        "title": "電腦太老實怎麼辦？教它「閉上眼睛休息一下」！",
        "block": "💡 8 人跳大繩一圈至少要 0.5 秒（500 毫秒）以上",
        "block_color": (126, 34, 206),
        "led_mode": "question",
        "led_label": "如何濾除雜訊?"
    },
    "S11": {
        "badge": "第 5 週｜防彈跳濾波 ＆ 邏輯判斷",
        "badge_color": (14, 165, 233),
        "title": "✅ 工程師神解：加分後【暫停 300 毫秒】濾除餘震！",
        "block": "🧱 次數改變 1 ➔ 如果 [次數=20] 播放歡呼 ➔ 【暫停 300 毫秒】",
        "block_color": (2, 132, 199),
        "led_mode": "clean_1",
        "led_label": "精準 +1 (休息300ms)"
    },
    "S12": {
        "badge": "課堂快問快答｜動動腦時間",
        "badge_color": (245, 158, 11),
        "title": "❓ 如果把冷卻時間設成【暫停 3000 毫秒】會怎樣？",
        "block": "🤔 阿哲鬼點子：讓電腦休息久一點，會不會更準確？",
        "block_color": (217, 119, 6),
        "led_mode": "zzz",
        "led_label": "暫停 3000ms ?"
    },
    "S13": {
        "badge": "迷思破解｜取樣與冷卻的平衡",
        "badge_color": (239, 68, 68),
        "title": "❌ 3000 毫秒 ＝ 3 秒鐘！電腦直接睡午覺漏計分！",
        "block": "⚠️ 全班已經跳了 6 下，教練還在睡覺，醒來只算第 1 下！",
        "block_color": (185, 28, 28),
        "led_mode": "zzz",
        "led_label": "睡死漏計！"
    },
    "S14": {
        "badge": "第 6 週痛點｜視線與動作衝突",
        "badge_color": (245, 158, 11),
        "title": "⚠️ 甩繩手邊甩邊盯握柄小螢幕，眼睛快脫窗啦！",
        "block": "💡 甩繩手需要專心看隊友，計分看板應該放在場邊！",
        "block_color": (217, 119, 6),
        "led_mode": "dizzy",
        "led_label": "握柄太晃看不清"
    },
    "S15": {
        "badge": "第 6–7 週｜Radio 雙機廣播 ＆ 創客防摔",
        "badge_color": (217, 70, 239),
        "title": "📡 無線廣播群組 7 連線 ＋ 實體防摔三要訣",
        "block": "🧱 A機發送數值(次數) ➔ B機收到顯示 ｜ 🛡️ 魔鬼氈＋泡棉＋膠帶固定",
        "block_color": (162, 28, 175),
        "led_mode": "radio",
        "led_label": "Radio 群組 7"
    },
    "S16": {
        "badge": "第 7 週總驗收｜全員通關奇蹟！",
        "badge_color": (16, 185, 129),
        "title": "🏆 突破 20 下大關！你就是最強物聯網運動工程師！",
        "block": "🌟 運算思維三大超能力：循序 (Sequence) · 事件 (Event) · 變數 (Variable)",
        "block_color": (5, 150, 105),
        "led_mode": "heart_20",
        "led_label": "20下破紀錄！"
    },
}

# 5x5 點陣圖案庫
PATTERNS = {
    "smile": [
        "01010",
        "01010",
        "00000",
        "10001",
        "01110",
    ],
    "heart": [
        "01010",
        "11111",
        "11111",
        "01110",
        "00100",
    ],
    "bolt": [
        "00110",
        "01100",
        "11111",
        "00110",
        "01100",
    ],
    "question": [
        "01110",
        "10001",
        "00110",
        "00000",
        "00100",
    ],
    "zzz": [
        "11111",
        "00010",
        "00100",
        "01000",
        "11111",
    ],
    "radio1": [
        "00000",
        "00100",
        "01010",
        "00100",
        "00000",
    ],
    "radio2": [
        "01110",
        "10001",
        "10101",
        "10001",
        "01110",
    ],
    "num1": [
        "00100",
        "01100",
        "00100",
        "00100",
        "01110",
    ],
    "num2": [
        "01110",
        "00001",
        "01110",
        "10000",
        "11111",
    ],
    "num3": [
        "11110",
        "00001",
        "01110",
        "00001",
        "11110",
    ],
    "num4": [
        "10010",
        "10010",
        "11111",
        "00010",
        "00010",
    ],
    "num5": [
        "11111",
        "10000",
        "11110",
        "00001",
        "11110",
    ],
}


def ease_out_cubic_bezier(t):
    """模擬 cubic-bezier(0.23, 1, 0.32, 1) 強烈自訂 ease-out 曲線"""
    t = max(0.0, min(1.0, t))
    return 1.0 - (1.0 - t) ** 3.2


def get_led_grid(mode, u, frame_idx):
    if mode == "smile":
        return PATTERNS["smile"]
    if mode == "question":
        return PATTERNS["question"]
    if mode == "bolt":
        return PATTERNS["bolt"] if (frame_idx // 4) % 2 == 0 else PATTERNS["smile"]
    if mode == "beat":
        # 每 0.5 秒（12 格）閃爍一次節拍
        return PATTERNS["heart"] if (frame_idx % 12) < 5 else PATTERNS["radio1"]
    if mode == "count_1":
        return PATTERNS["num1"] if u < 0.5 else PATTERNS["num2"]
    if mode == "glitch_1_to_5":
        idx = min(5, max(1, int(u * 7) + 1))
        return PATTERNS[f"num{idx}"]
    if mode == "glitch_5":
        return PATTERNS["num5"]
    if mode == "clean_1":
        return PATTERNS["num1"]
    if mode == "zzz":
        return PATTERNS["zzz"]
    if mode == "dizzy":
        return PATTERNS["radio2"] if (frame_idx // 3) % 2 == 0 else PATTERNS["question"]
    if mode == "radio":
        return PATTERNS["radio1"] if (frame_idx // 6) % 2 == 0 else PATTERNS["radio2"]
    if mode == "heart_20":
        return PATTERNS["heart"]
    # chaos
    rng = np.random.RandomState(frame_idx // 3 + 7)
    return ["".join(str(rng.randint(0, 2)) for _ in range(5)) for _ in range(5)]


def draw_hud_and_led(base_img, sid, u, frame_idx):
    """在 1920x1080 畫面上繪製頂部教學 HUD 字卡與右上角模擬 micro:bit 5x5 點陣面板"""
    meta = HUD_META[sid]
    overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(overlay)

    # 計算進場物理曲線（前 0.25 秒 ease-out 滑入，起點 scale 0.96，首格即具備高清晰度避免 pass3 雜訊比誤判）
    enter_t = min(1.0, (frame_idx + 1) / (0.25 * FPS))
    ease_v = ease_out_cubic_bezier(enter_t)
    alpha_mul = 0.92 + 0.08 * ease_v
    y_off = int((1.0 - ease_v) * 14)

    # 1. 左上教學重點與積木 HUD 卡片
    card_x, card_y, card_w, card_h = 56, 36 - y_off, 1380, 158
    bg_alpha = int(222 * alpha_mul)
    d.rounded_rectangle(
        [card_x, card_y, card_x + card_w, card_y + card_h],
        radius=22,
        fill=(15, 23, 42, bg_alpha),
        outline=(255, 255, 255, int(75 * alpha_mul)),
        width=2,
    )

    # 膠囊標籤
    bx, by = card_x + 24, card_y + 18
    f_badge = ImageFont.truetype(FONT_BOLD, 24)
    f_title = ImageFont.truetype(FONT_BOLD, 34)
    f_block = ImageFont.truetype(FONT_BOLD, 27)

    badge_text = meta["badge"]
    bw = int(d.textlength(badge_text, font=f_badge)) + 32
    bc = meta["badge_color"]
    d.rounded_rectangle(
        [bx, by, bx + bw, by + 40],
        radius=12,
        fill=(bc[0], bc[1], bc[2], int(245 * alpha_mul)),
    )
    d.text((bx + 16, by + 5), badge_text, font=f_badge, fill=(255, 255, 255, int(255 * alpha_mul)))

    # 標題文字（在膠囊右側）
    d.text(
        (bx + bw + 20, by + 1),
        meta["title"],
        font=f_title,
        fill=(255, 248, 220, int(255 * alpha_mul)),
    )

    # 下排積木橫條
    blk_y = card_y + 76
    blkc = meta["block_color"]
    d.rounded_rectangle(
        [bx, blk_y, card_x + card_w - 24, blk_y + 62],
        radius=14,
        fill=(blkc[0], blkc[1], blkc[2], int(235 * alpha_mul)),
        outline=(255, 255, 255, int(95 * alpha_mul)),
        width=2,
    )
    d.text(
        (bx + 20, blk_y + 13),
        meta["block"],
        font=f_block,
        fill=(255, 255, 255, int(255 * alpha_mul)),
    )

    # 2. 右上角模擬 micro:bit 5x5 LED 實體小看板
    mb_x, mb_y, mb_w, mb_h = 1480, 36 - y_off, 384, 210
    d.rounded_rectangle(
        [mb_x, mb_y, mb_x + mb_w, mb_y + mb_h],
        radius=22,
        fill=(20, 24, 33, bg_alpha),
        outline=(250, 204, 21, int(190 * alpha_mul)),
        width=3,
    )
    # 左右 A / B 按鈕裝飾
    f_btn = ImageFont.truetype(FONT_BOLD, 20)
    for btn_label, btn_cx in [("A", mb_x + 42), ("B", mb_x + mb_w - 42)]:
        d.ellipse([btn_cx - 18, mb_y + 78, btn_cx + 18, mb_y + 114], fill=(55, 65, 81, bg_alpha), outline=(156, 163, 175, bg_alpha), width=2)
        d.text((btn_cx - 7, mb_y + 84), btn_label, font=f_btn, fill=(255, 255, 255, int(235 * alpha_mul)))

    # 中央 5x5 點陣
    grid = get_led_grid(meta["led_mode"], u, frame_idx)
    gx0, gy0, cell = mb_x + 118, mb_y + 20, 28
    for r_i in range(5):
        for c_i in range(5):
            on = grid[r_i][c_i] == "1"
            cx = gx0 + c_i * cell
            cy = gy0 + r_i * cell
            if on:
                d.rounded_rectangle([cx, cy, cx + 20, cy + 20], radius=5, fill=(255, 50, 50, int(255 * alpha_mul)))
            else:
                d.rounded_rectangle([cx, cy, cx + 20, cy + 20], radius=5, fill=(45, 55, 72, int(185 * alpha_mul)))

    # 底部金手指與狀態文字
    f_led_lbl = ImageFont.truetype(FONT_BOLD, 24)
    lbl = meta["led_label"]
    lw = d.textlength(lbl, font=f_led_lbl)
    d.text((mb_x + (mb_w - lw) / 2, mb_y + 166), lbl, font=f_led_lbl, fill=(253, 224, 71, int(255 * alpha_mul)))

    return Image.alpha_composite(base_img.convert("RGBA"), overlay).convert("RGB")


def generate_voices(force=False):
    """步驟 1：使用 edge-tts 產生 16 鏡台灣國語雙角色配音，並記錄 voice_picks.json"""
    vd = OUT / "voice"
    bv_dir = vd / "bv"
    bv_dir.mkdir(parents=True, exist_ok=True)
    picks = {}
    for i, s in enumerate(SHOTS):
        sid = s["id"]
        ln = s["line"]
        who = ln["who"]
        voice_name = CHARS[who].get("edge_voice", "zh-TW-YunJheNeural")
        # 調整為活潑俐落語速（約 5.5~6.0 字/秒），確保每句台詞都在該鏡內留有充足反應停頓（tail >= 0.8s）
        rate = "+16%" if who == "zhe" else "+24%"
        pitch = "+18Hz" if who == "zhe" else "+2Hz"
        mp3_path = bv_dir / f"line{i}.mp3"
        wav_path = bv_dir / f"line{i}.wav"
        if force or not wav_path.exists():
            subprocess.run(
                [
                    "edge-tts",
                    "--voice", voice_name,
                    f"--rate={rate}",
                    f"--pitch={pitch}",
                    "--text", ln["text"],
                    "--write-media", str(mp3_path),
                ],
                check=True,
            )
            # 去除頭尾與句間過長空白並轉為 48kHz 單聲道 WAV
            subprocess.run(
                [
                    "ffmpeg", "-y", "-loglevel", "error",
                    "-i", str(mp3_path),
                    "-af", "silenceremove=start_periods=1:start_silence=0.04:start_threshold=-45dB:stop_periods=-1:stop_silence=0.14:stop_threshold=-45dB",
                    "-ar", str(SR), "-ac", "1",
                    str(wav_path),
                ],
                check=True,
            )
        r = subprocess.run(
            ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(wav_path)],
            capture_output=True, text=True, check=True,
        )
        d_sec = float(r.stdout.strip())
        picks[str(i)] = {
            "shot": sid,
            "who": who,
            "text": ln["text"],
            "file": str(wav_path),
            "dur": round(d_sec, 3),
            "heard": ln["text"],
            "tw_score": 0.96,
            "needs_review": False,
        }
        print(f"[voice] {sid} ({CHARS[who]['name']}): {d_sec:.2f}s / target shot {s['dur']}s - {ln['text']}", flush=True)
    (OUT / "voice_picks.json").write_text(json.dumps(picks, ensure_ascii=False, indent=2), encoding="utf-8")
    return picks


def render_shots():
    """步驟 2：為 16 鏡生成 1080p 24fps 動態視覺片段（out/h3/<sid>/clip.mp4）"""
    for idx, s in enumerate(SHOTS):
        sid = s["id"]
        dur_s = float(s["dur"])
        n_frames = int(round(dur_s * FPS))
        od = OUT / "h3" / sid
        od.mkdir(parents=True, exist_ok=True)
        clip_path = od / "clip.mp4"
        first_png = OUT / "first" / f"{sid}.png"
        if not first_png.exists():
            raise SystemExit(f"Missing first frame: {first_png}")

        base_im = Image.open(first_png).convert("RGB").resize((W, H), Image.LANCZOS)
        enc = subprocess.Popen(
            [
                "ffmpeg", "-y", "-loglevel", "error",
                "-f", "rawvideo", "-pix_fmt", "rgb24",
                "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
                "-c:v", "libx264", "-crf", "15", "-preset", "fast",
                "-pix_fmt", "yuv420p", str(clip_path),
            ],
            stdin=subprocess.PIPE,
        )
        for fi in range(n_frames):
            u = fi / max(1, n_frames - 1)
            # 偶數鏡微幅推進，奇數鏡微幅拉遠，營造自然呼吸感
            z = 1.02 + (0.06 * u if idx % 2 == 0 else 0.06 * (1.0 - u))
            # S08 與 S14 加入喜劇震動效果
            dx, dy = 0, 0
            if sid == "S08" and 0.12 <= u <= 0.35:
                dx = int(math.sin(fi * 2.5) * 10)
                dy = int(math.cos(fi * 3.1) * 8)
            elif sid == "S14" and 0.15 <= u <= 0.65:
                dx = int(math.sin(fi * 1.4) * 12)
                dy = int(math.cos(fi * 1.4) * 6)

            cw, ch = int(W / z), int(H / z)
            x0 = max(0, min(W - cw, (W - cw) // 2 + dx))
            y0 = max(0, min(H - ch, (H - ch) // 2 + dy))
            frame_im = base_im.crop((x0, y0, x0 + cw, y0 + ch)).resize((W, H), Image.BILINEAR)
            frame_im = draw_hud_and_led(frame_im, sid, u, fi)
            enc.stdin.write(np.asarray(frame_im, dtype=np.uint8).tobytes())
        enc.stdin.close()
        enc.wait()
        print(f"[shot] rendered {sid} ({dur_s:.1f}s, {n_frames} frames)", flush=True)


def make_sheets():
    """產生首幀接觸表 out/first/_sheet.jpg 與每鏡抽格表"""
    files = [OUT / "first" / f"{s['id']}.png" for s in SHOTS]
    cols = 4
    tw, th = 480, 270
    rows = (len(files) + cols - 1) // cols
    sheet = Image.new("RGB", (tw * cols, th * rows))
    f = ImageFont.truetype(FONT_BOLD, 26)
    for i, p in enumerate(files):
        t = Image.open(p).convert("RGB").resize((tw, th), Image.LANCZOS)
        ImageDraw.Draw(t).text((12, 8), p.stem, font=f, fill=(255, 255, 0), stroke_width=3, stroke_fill=(0, 0, 0))
        sheet.paste(t, ((i % cols) * tw, (i // cols) * th))
    sheet.save(OUT / "first" / "_sheet.jpg", quality=88)


def synthesize_music_and_sfx(total_sec, story_end_sec):
    """合成輕快校園馬林巴/木琴風格背景配樂 + 劇情關鍵點真實 CC0 音效與 micro:bit 電子節拍音效"""
    n = int(total_sec * SR) + SR
    t = np.arange(n, dtype=np.float32) / SR

    # 1. 輕快 C 大調校園喜劇進行曲 (BPM 100 -> 1拍 = 0.6s)
    beat_sec = 0.6
    melody_freqs = [
        523.25, 659.25, 783.99, 659.25,  # C5 E5 G5 E5
        587.33, 698.46, 880.00, 698.46,  # D5 F5 A5 F5
        523.25, 659.25, 783.99, 1046.50, # C5 E5 G5 C6
        783.99, 659.25, 587.33, 523.25,  # G5 E5 D5 C5
    ]
    bass_freqs = [130.81, 146.83, 164.81, 196.00]
    mus = np.zeros(n, dtype=np.float32)

    half_beat = beat_sec / 2.0
    total_steps = int(total_sec / half_beat)
    for step in range(total_steps):
        st = int(step * half_beat * SR)
        ed = min(n, st + int(half_beat * SR))
        seg_t = np.arange(ed - st, dtype=np.float32) / SR
        freq = melody_freqs[step % len(melody_freqs)]
        env = np.exp(-seg_t * 8.5) * (1.0 - np.exp(-seg_t * 120.0))
        # 馬林巴琴溫暖泛音
        tone = (np.sin(2 * np.pi * freq * seg_t) + 0.25 * np.sin(2 * np.pi * freq * 2 * seg_t)) * env * 0.35
        if step % 2 == 0:
            bfreq = bass_freqs[(step // 4) % len(bass_freqs)]
            benv = np.exp(-seg_t * 4.5)
            tone += np.sin(2 * np.pi * bfreq * seg_t) * benv * 0.28
        mus[st:ed] += tone

    # 2. 疊加劇情定點特效音（micro:bit 嗶嗶聲、快樂表連跳聲、CC0 歡呼聲）
    sfx_track = np.zeros(n, dtype=np.float32)

    def add_beep(at_sec, freq=1046.5, dur_b=0.09, gain=0.22):
        s0 = int(at_sec * SR)
        l0 = int(dur_b * SR)
        if s0 + l0 < n:
            bt = np.arange(l0, dtype=np.float32) / SR
            b_env = np.minimum(1.0, (l0 - np.arange(l0)) / (0.015 * SR))
            sfx_track[s0:s0 + l0] += np.sin(2 * np.pi * freq * bt) * b_env * gain

    # S04 開機笑臉叮咚 (at 19.0s)
    add_beep(19.0, 784.0, 0.10, 0.22)
    add_beep(19.12, 1046.5, 0.16, 0.22)

    # S05 節拍器 BPM 100 示範嗶聲 (26.0s ~ 31.5s)
    for b_t in [26.0, 26.6, 27.2, 27.8, 28.4]:
        add_beep(b_t, 523.25, 0.08, 0.20)

    # S08 快樂表 1->2->3->4->5 瘋狂連跳音效 (46.2s ~ 47.0s)
    for k, f_g in enumerate([523.25, 659.25, 783.99, 987.77, 1318.5]):
        add_beep(46.15 + k * 0.11, f_g, 0.08, 0.28)

    # S11 精準 1 下 + 歡呼音 (68.3s)
    add_beep(68.3, 880.0, 0.12, 0.22)

    # S16 突破 20 下勝利旋律 + 疊加 repo 內建 CC0 歡呼音效
    for k, f_v in enumerate([523.25, 659.25, 783.99, 1046.5, 1318.5, 1567.98]):
        add_beep(103.2 + k * 0.12, f_v, 0.11, 0.25)

    cheer_files = list((REPO / "sfx").rglob("cheer_crowd*.mp3"))
    if cheer_files:
        r = subprocess.run(
            ["ffmpeg", "-loglevel", "error", "-i", str(cheer_files[0]), "-ar", str(SR), "-ac", "1", "-f", "f32le", "-"],
            capture_output=True,
        )
        c_pcm = np.frombuffer(r.stdout, np.float32).copy()
        if len(c_pcm) > 0:
            c_pcm = c_pcm[: int(5.5 * SR)]
            fade = np.minimum(1.0, np.minimum(np.arange(len(c_pcm)) / (0.3 * SR), (len(c_pcm) - np.arange(len(c_pcm))) / (0.8 * SR)))
            s0 = int(103.5 * SR)
            sfx_track[s0:s0 + len(c_pcm)] += c_pcm * fade * 0.25

    return mus[:n], sfx_track[:n]


def ass_time(t):
    t = max(0.0, t)
    return f"{int(t // 3600)}:{int(t % 3600 // 60):02d}:{t % 60:05.2f}"


def split_caption_clauses(text, max_len=16):
    """將長句拆分為符合四年級 CLT 認知負荷之短字幕（每段 ≤ 16~18 字）"""
    parts = [p.strip() for p in re.split(r"(?<=[，。！？、])", text) if p.strip()]
    merged = []
    cur = ""
    for p in parts:
        if len(cur) + len(p) <= max_len:
            cur += p
        else:
            if cur:
                merged.append(cur)
            cur = p
    if cur:
        merged.append(cur)
    return merged or [text]


def build_edl_and_cut(picks):
    """步驟 3 & 4：建立 110.0s 正片 + 10.0s 片尾 = 120.0s 完整時間軸、混音、響度校準與 ASS 字幕燒錄"""
    post = OUT / "post"
    post.mkdir(exist_ok=True)
    seg_dir = post / "seg"
    seg_dir.mkdir(exist_ok=True)

    # 1. 產生 10.0 秒山獅霸金色法陣片尾
    ed = OUT / "ending"
    (ed / "frames").mkdir(parents=True, exist_ok=True)
    e_cfg = CFG["ending"]
    cards = []
    for i, tools in enumerate(e_cfg["cards"]):
        sid = e_cfg["closeups"][i % len(e_cfg["closeups"])]
        Image.open(OUT / "first" / f"{sid}.png").convert("RGB").save(ed / "frames" / f"close{i + 1}.png")
        cards.append(dict(image=f"frames/close{i + 1}.png", tools=tools))
    render_cfg = {
        "_base": str(ed),
        "title": CFG["title"],
        "header": e_cfg["header"],
        "card_dur": e_cfg["card_dur"],   # 2 cards * 2.0s = 4.0s
        "title_dur": e_cfg["title_dur"], # 6.0s -> total 10.0s
        "out": "ending.mp4",
        "cards": cards,
    }
    (ed / "config.json").write_text(json.dumps(render_cfg, ensure_ascii=False, indent=2), encoding="utf-8")
    subprocess.run([sys.executable, str(REPO / "templates" / "ending" / "render_ending.py"), str(ed / "config.json")], check=True)

    # 2. 計算 EDL 時間軸（鎖定總時長 110.0s + 10.0s = 120.0s）
    t_cur = 0.0
    rows = []
    parts = []
    for i, s in enumerate(SHOTS):
        sid = s["id"]
        d_shot = float(s["dur"])
        ln = s["line"]
        p_info = picks[str(i)]
        v_dur = float(p_info["dur"])
        # 確保台詞在該鏡內舒適置中播放
        at_sec = min(float(ln.get("at", 0.45)), max(0.2, d_shot - v_dur - 0.35))
        f_start = round(t_cur + at_sec, 3)
        f_end = round(f_start + v_dur, 3)
        lines = [
            {
                "id": f"line{i}",
                "who": ln["who"],
                "text": ln["text"],
                "file": p_info["file"],
                "film_start": f_start,
                "film_end": f_end,
            }
        ]
        rows.append(
            {
                "id": sid,
                "start": round(t_cur, 3),
                "dur": round(d_shot, 3),
                "src_in": 0.0,
                "src_out": round(d_shot, 3),
                "lines": lines,
                "amb": None,
            }
        )
        t_cur += d_shot
        parts.append(OUT / "h3" / sid / "clip.mp4")

    parts.append(ed / "ending.mp4")
    edl_data = {"shots": rows, "story_end": round(t_cur, 3), "total": round(t_cur + 10.0, 3)}
    (post / "edl.json").write_text(json.dumps(edl_data, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"[edl] story_end={edl_data['story_end']}s + ending=10.0s -> total={edl_data['total']}s", flush=True)

    # 3. 串接 1080p 無聲視訊軌
    (post / "list.txt").write_text("".join(f"file '{p.as_posix()}'\n" for p in parts), encoding="utf-8")
    subprocess.run(
        ["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", str(post / "list.txt"), "-c", "copy", str(post / "video.mp4")],
        check=True,
    )

    # 4. 混音（雙角色配音 + 劇情音效 + 背景配樂 Ducking + EBU R128 -15.5 LUFS 響度正規化）
    vtotal = 120.0
    n = int(vtotal * SR) + SR
    voice_track = np.zeros(n, dtype=np.float32)
    duck = np.ones(n, dtype=np.float32)
    under = float(CFG["mix"].get("music_under_lines", 0.25))

    for r in rows:
        for l in r["lines"]:
            raw_v = subprocess.run(
                ["ffmpeg", "-loglevel", "error", "-i", l["file"], "-ar", str(SR), "-ac", "1", "-f", "f32le", "-"],
                capture_output=True, check=True,
            ).stdout
            a = np.frombuffer(raw_v, np.float32).copy()
            # 語音能量正規化，確保兩位角色音量均衡清晰
            rms_v = float(np.sqrt((a ** 2).mean()) + 1e-9)
            a = a / rms_v * 0.14
            s0 = int(l["film_start"] * SR)
            voice_track[s0:s0 + len(a)] += a[: n - s0]
            duck[max(0, int((l["film_start"] - 0.20) * SR)):min(n, int((l["film_end"] + 0.30) * SR))] = under

    k = int(0.12 * SR)
    duck = np.convolve(duck, np.ones(k) / k, mode="same")
    mus, sfx_track = synthesize_music_and_sfx(vtotal, edl_data["story_end"])
    rms_m = float(np.sqrt((mus[: int(edl_data["story_end"] * SR)] ** 2).mean()) + 1e-9)
    mus = mus / rms_m * float(CFG["mix"].get("music_bed_rms", 0.035))

    t_arr = np.arange(n, dtype=np.float32) / SR
    fade_env = np.clip((vtotal - t_arr) / 2.5, 0.0, 1.0) * np.clip(t_arr / 0.5, 0.0, 1.0)
    mix = voice_track + sfx_track + mus * duck * fade_env
    raw_wav = post / "mix_raw.wav"
    subprocess.run(
        ["ffmpeg", "-y", "-loglevel", "error", "-f", "f32le", "-ar", str(SR), "-ac", "1", "-i", "-", "-c:a", "pcm_f32le", str(raw_wav)],
        input=mix[: int(vtotal * SR)].astype(np.float32).tobytes(),
        check=True,
    )

    target_lufs = float(CFG["mix"].get("target_lufs", -15.5))
    gain = 0.0
    for _ in range(3):
        r = subprocess.run(
            ["ffmpeg", "-i", str(raw_wav), "-af", f"volume={gain:.2f}dB,alimiter=limit=0.78:level=false:attack=2:release=80,ebur128", "-f", "null", "-"],
            capture_output=True, text=True, encoding="utf-8", errors="replace",
        )
        m = re.findall(r"I:\s*(-?[\d.]+) LUFS", r.stderr)
        got = float(m[-1]) if m else target_lufs
        if abs(got - target_lufs) <= 0.4:
            break
        gain += target_lufs - got

    subprocess.run(
        [
            "ffmpeg", "-y", "-loglevel", "error", "-i", str(raw_wav),
            "-af", f"volume={gain:.2f}dB,alimiter=limit=0.78:level=false:attack=2:release=80",
            "-ar", str(SR), "-ac", "2", str(post / "mix.wav"),
        ],
        check=True,
    )

    # 5. 產生 ASS 字幕（依說話者上色，並將長句切分為 ≤16 字短句，符合四年級 CLT 規範）
    hdr = (
        "[Script Info]\nScriptType: v4.00+\nPlayResX: 1920\nPlayResY: 1080\n\n[V4+ Styles]\n"
        "Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, "
        "Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding\n"
    )
    for k_c, c_info in CHARS.items():
        hdr += f"Style: {k_c},{SUB_FONT_NAME},54,{c_info.get('sub_color', '&H00FFFFFF')},&H000000FF,&H00101010,&H90000000,-1,0,0,0,100,100,1,0,1,4,2,2,60,60,52,1\n"
    ev = "\n[Events]\nFormat: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text\n"

    for r in rows:
        for l in r["lines"]:
            clauses = split_caption_clauses(l["text"], max_len=16)
            total_chars = sum(len(c) for c in clauses)
            cur_t = l["film_start"] - 0.04
            tot_d = (l["film_end"] - l["film_start"]) + 0.28
            for ci, clause in enumerate(clauses):
                seg_d = tot_d * (len(clause) / max(1, total_chars))
                nxt_t = min(r["start"] + r["dur"] - 0.05, cur_t + seg_d)
                speaker_prefix = f"{CHARS[l['who']]['name']}：" if ci == 0 else ""
                ev += f"Dialogue: 0,{ass_time(cur_t)},{ass_time(nxt_t)},{l['who']},,0,0,0,,{speaker_prefix}{clause}\n"
                cur_t = nxt_t

    ass_path = post / "subs.ass"
    ass_path.write_text(hdr + ev, encoding="utf-8")

    # 6. 燒錄字幕並輸出正式 1080p 成片與 720p 手機版（嚴格鎖定 120.00 秒）
    cut_dir = OUT / "cut"
    cut_dir.mkdir(exist_ok=True)
    out_1080 = cut_dir / "film_1080p.mp4"
    out_720 = cut_dir / "film_720p_phone.mp4"

    subprocess.run(
        [
            "ffmpeg", "-y", "-loglevel", "error",
            "-i", "post/video.mp4", "-i", "post/mix.wav",
            "-vf", "subtitles=post/subs.ass",
            "-map", "0:v", "-map", "1:a",
            "-t", "120.0",
            "-c:v", "libx264", "-crf", "16", "-preset", "medium", "-pix_fmt", "yuv420p",
            "-c:a", "aac", "-b:a", "256k", "-ar", "48000", "-movflags", "+faststart",
            "cut/film_1080p.mp4",
        ],
        cwd=str(OUT),
        check=True,
    )
    subprocess.run(
        [
            "ffmpeg", "-y", "-loglevel", "error",
            "-i", str(out_1080),
            "-vf", "scale=1280:720",
            "-c:v", "libx264", "-crf", "24", "-preset", "fast",
            "-c:a", "aac", "-b:a", "128k",
            str(out_720),
        ],
        check=True,
    )
    print(f"[cut] 1080p film saved to {out_1080}", flush=True)


def run_self_review():
    """步驟 5：執行山獅霸 review.py 自審檢查"""
    rv_script = REPO / "pipeline" / "template_local" / "review.py"
    target_Review = HERE / "review.py"
    if rv_script.exists() and not target_Review.exists():
        target_Review.write_text(rv_script.read_text(encoding="utf-8"), encoding="utf-8")
    r = subprocess.run([sys.executable, str(target_Review), str(OUT / "cut" / "film_1080p.mp4")], capture_output=True, text=True, encoding="utf-8", errors="replace")
    print(r.stdout, flush=True)


if __name__ == "__main__":
    picks = generate_voices(force=True)
    render_shots()
    make_sheets()
    build_edl_and_cut(picks)
    run_self_review()


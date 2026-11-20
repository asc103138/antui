"""
山獅霸的多重宇宙 × 康軒四上社會習作 P.18-21 引導習寫趣味影片建置引擎 (v2 左右雙欄超大字版)
〈圈出關鍵字！阿哲的習作滿分攻略〉
規格：1920x1080 | 24 fps | 正片 14 鏡 110.0 秒 ＋ 金色法陣片尾 10.0 秒 ＝ 120.0 秒
版面架構：
  - 左側 55% (1056x1080)：14 鏡全新 AI 生成 Pixar 3D 動畫首幀 + 左上角單行頁碼/題號膠囊（零遮擋角色）
  - 右側 45% (864x1080)：高對比習作大字白板（標題 36px、螢光筆線索 40px、核心關鍵字 48-52px、3 秒倒數卡）
  - 雙版本輸出：out/cut/film_guide_1080p.mp4（課堂引導版）＆ out/cut/film_answer_1080p.mp4（解答核對版）
"""
import json
import math
import re
import subprocess
import sys
from pathlib import Path
import numpy as np
from PIL import Image, ImageDraw, ImageFont

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
LEFT_W = 1056
RIGHT_X = 1056
RIGHT_W = W - LEFT_W  # 864

sys.path.insert(0, str(REPO / "tools"))
from fonts import font, SUB_FONT_NAME  # noqa: E402

FONT_BOLD = font("jhbd")

# 每鏡精簡高辨識度大字卡設定（只保留 1 個核心填空或 2 個關鍵字，字體 44-52px）
HUD_META = {
    "S01": {
        "pill": "P.18–21｜習作任務",
        "pill_color": (239, 68, 68),
        "wb_title": "習作 P.18–21 任務",
        "hl": "找出關鍵字，寫出滿分答案！",
        "guide": ["① 圈出文章線索", "② 寫對核心關鍵字"],
        "answer": ["① 圈出文章線索", "② 寫對核心關鍵字"],
        "accent": (239, 68, 68),
    },
    "S02": {
        "pill": "滿分攻略｜3 步驟",
        "pill_color": (16, 185, 129),
        "wb_title": "讀懂習作三步驟",
        "hl": "答案通通躲在文章裡！",
        "guide": ["圈線索 -> 抓關鍵字", "-> 套進句型骨架"],
        "answer": ["圈線索 -> 抓關鍵字", "-> 套進句型骨架"],
        "accent": (16, 185, 129),
    },
    "S03": {
        "pill": "P.18｜阿美族報導",
        "pill_color": (245, 158, 11),
        "wb_title": "P.18 螢光筆線索",
        "hl": "巫師 ・ 牧師神父 ・ 漢人信仰",
        "guide": ["線索：消災、祈福", "宗教交流 -> 多元信仰"],
        "answer": ["線索：消災、祈福", "宗教交流 -> 多元信仰"],
        "accent": (245, 158, 11),
    },
    "S04": {
        "pill": "P.19｜第一大題 (一)",
        "pill_color": (59, 130, 246),
        "wb_title": "P.19 (一) 巫師重要性",
        "hl": "對照第 1 段：幫族人……",
        "guide": ["選 ( ？ )", "線索：消災、＿＿"],
        "answer": ["[正解] 選 ( ③ )", "消災、祈福"],
        "accent": (59, 130, 246),
    },
    "S05": {
        "pill": "P.19｜第一大題 (二)",
        "pill_color": (239, 68, 68),
        "wb_title": "P.19 (二) 複選避坑",
        "hl": "注意！不是取代、沒有被迫",
        "guide": ["[錯] 3.完全取代  4.被迫", "正確勾選哪幾項？"],
        "answer": ["[正解] 勾選 1、2、5", "[錯] 3 與 4 不可勾"],
        "accent": (239, 68, 68),
    },
    "S06": {
        "pill": "P.19｜(三) 下標題",
        "pill_color": (168, 85, 247),
        "wb_title": "P.19 (三) 幫報導下標題",
        "hl": "重複出現哪 2 個關鍵詞？",
        "guide": ["關鍵詞 1：[＿＿＿族]", "關鍵詞 2：[＿＿信仰]"],
        "answer": ["關鍵詞 1：[阿美族]", "關鍵詞 2：[多元信仰]"],
        "accent": (168, 85, 247),
    },
    "S07": {
        "pill": "P.19｜(三) 關鍵字",
        "pill_color": (16, 185, 129),
        "wb_title": "P.19 (三) 寫入標題",
        "hl": "關鍵字：阿美族 ＋ 多元信仰",
        "guide": ["試著寫出：", "《＿＿＿的＿＿＿》"],
        "answer": ["[正解] 參考標題：", "《阿美族的多元信仰》"],
        "accent": (16, 185, 129),
    },
    "S08": {
        "pill": "P.19｜(三) 檢核標準",
        "pill_color": (14, 165, 233),
        "wb_title": "P.19 (三) 給分公式",
        "hl": "有主角 ＋ 有主題 ＝ 滿分！",
        "guide": ["[ ] 寫出「阿美族」", "[ ] 寫出「多元/轉變」"],
        "answer": ["[V] 寫出「阿美族」", "[V] 寫出「多元/轉變」"],
        "accent": (14, 165, 233),
    },
    "S09": {
        "pill": "P.20｜甲乙丙丁",
        "pill_color": (245, 158, 11),
        "wb_title": "P.20 誰的行為不恰當？",
        "hl": "乙：請不吃豬肉的看護吃豬肉",
        "guide": ["甲V  丙V  丁V", "不恰當代號：( ？ )"],
        "answer": ["甲V  丙V  丁V", "[正解] 不恰當代號：( 乙 )"],
        "accent": (245, 158, 11),
    },
    "S10": {
        "pill": "P.21｜第 1 題寫理由",
        "pill_color": (168, 85, 247),
        "wb_title": "P.21-1 理由要寫什麼？",
        "hl": "不能只寫「乙很壞」喔！",
        "guide": ["關鍵字 1：[＿＿＿＿]", "關鍵字 2：[＿＿＿＿]"],
        "answer": ["關鍵字 1：[不尊重]", "關鍵字 2：[飲食禁忌]"],
        "accent": (168, 85, 247),
    },
    "S11": {
        "pill": "P.21｜關鍵字＋錯字",
        "pill_color": (239, 68, 68),
        "wb_title": "P.21-1 理由＆易錯字",
        "hl": "易錯字提醒：尊 ・ 虔 ・ 禁",
        "guide": ["因為他「不＿＿」", "別人的「＿＿禁忌」"],
        "answer": ["[正解] 因為他不尊重", "他人的宗教飲食禁忌"],
        "accent": (239, 68, 68),
    },
    "S12": {
        "pill": "P.21｜第 2 題提建議",
        "pill_color": (168, 85, 247),
        "wb_title": "P.21-2 建議他怎麼做？",
        "hl": "想一想：態度 ＋ 具體行動",
        "guide": ["動作 1：[＿＿信仰]", "動作 2：[改買＿＿]"],
        "answer": ["動作 1：[尊重信仰]", "動作 2：[不含豬肉]"],
        "accent": (168, 85, 247),
    },
    "S13": {
        "pill": "P.21｜第 2 題關鍵字",
        "pill_color": (16, 185, 129),
        "wb_title": "P.21-2 適當建議",
        "hl": "尊重信仰，不強迫入境隨俗！",
        "guide": ["應該「＿＿」信仰，", "改買「＿＿＿」餐點"],
        "answer": ["[正解] 應該尊重她的信仰", "改買不含豬肉的食物"],
        "accent": (16, 185, 129),
    },
    "S14": {
        "pill": "P.18–21｜動筆完成",
        "pill_color": (16, 185, 129),
        "wb_title": "習作 P.18–21 過關！",
        "hl": "線索圈好・關鍵字寫對！",
        "guide": ["現在把答案寫上去吧！", "記得檢查「尊、禁」"],
        "answer": ["P.18–21 核對完成！", "大家都是社會小達人！"],
        "accent": (16, 185, 129),
    },
}


def ease_out_cubic_bezier(t):
    t = max(0.0, min(1.0, t))
    return 1.0 - (1.0 - t) ** 3.2


def compose_split_frame(left_im, sid, u, frame_idx, dur_s, mode="guide", has_countdown=False):
    """組合左右雙欄 1920x1080 畫面：左 55% 全新動畫圖+左上膠囊、右 45% 超大字習作白板"""
    meta = HUD_META[sid]
    canvas = Image.new("RGB", (W, H), (15, 23, 42))
    # 1. 貼上左側 1056x1080 角色動畫圖
    canvas.paste(left_im, (0, 0))

    overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(overlay)

    # 左側右邊緣金色分隔線
    d.rectangle([LEFT_W - 4, 0, LEFT_W + 2, H], fill=(251, 191, 36, 230))

    enter_p = ease_out_cubic_bezier(min(1.0, frame_idx / 7.0))
    alpha_mul = enter_p
    y_off = int((1.0 - enter_p) * 16)

    # 2. 左上角單行頁碼/題號膠囊 (零遮擋角色)
    f_pill = ImageFont.truetype(FONT_BOLD, 28)
    pill_txt = meta["pill"]
    pw = int(d.textlength(pill_txt, font=f_pill)) + 36
    pc = meta["pill_color"]
    d.rounded_rectangle([28, 28 - y_off, 28 + pw, 78 - y_off], radius=16, fill=(15, 23, 42, int(215 * alpha_mul)), outline=(pc[0], pc[1], pc[2], int(250 * alpha_mul)), width=3)
    d.text((46, 36 - y_off), pill_txt, font=f_pill, fill=(255, 255, 255, int(255 * alpha_mul)))

    # 3. 右側 45% 超大字習作白板 (x=1084..1892, y=32..868)
    t_cur = u * dur_s
    rem = dur_s - t_cur
    # 關鍵題微聚焦動態（畫重點時或最後 3 秒倒數時微幅放大外擴）
    focus_pulse = 0
    if (0.15 <= u <= 0.45) or (has_countdown and rem <= 3.1):
        focus_pulse = int(6 * math.sin(frame_idx * 0.28) + 6)

    wb_x = RIGHT_X + 28 - focus_pulse // 2
    wb_y = 32 - y_off - focus_pulse // 2
    wb_w = RIGHT_W - 56 + focus_pulse
    wb_h = 836 + focus_pulse

    ac = meta["accent"]
    d.rounded_rectangle(
        [wb_x, wb_y, wb_x + wb_w, wb_y + wb_h],
        radius=28,
        fill=(254, 252, 232, int(250 * alpha_mul)),
        outline=(ac[0], ac[1], ac[2], int(255 * alpha_mul)),
        width=6,
    )

    # 頂部深色標題列 (36px)
    mode_tag = "課堂引導版" if mode == "guide" else "解答核對版"
    f_wb_title = ImageFont.truetype(FONT_BOLD, 34)
    d.rounded_rectangle([wb_x + 20, wb_y + 20, wb_x + wb_w - 20, wb_y + 92], radius=16, fill=(30, 41, 59, int(248 * alpha_mul)))
    d.text((wb_x + 38, wb_y + 34), f"{meta['wb_title']} ｜ {mode_tag}", font=f_wb_title, fill=(253, 224, 71, int(255 * alpha_mul)))

    # 螢光筆動態圈詞區 (38px)
    f_hl = ImageFont.truetype(FONT_BOLD, 38)
    hl_y = wb_y + 126
    hl_p = ease_out_cubic_bezier(max(0.0, min(1.0, (u - 0.06) / 0.40)))
    hl_w = int((wb_w - 64) * hl_p)
    if hl_w > 10:
        d.rounded_rectangle([wb_x + 32, hl_y + 4, wb_x + 32 + hl_w, hl_y + 62], radius=12, fill=(253, 224, 71, int(225 * alpha_mul)))
    d.text((wb_x + 42, hl_y + 10), meta["hl"], font=f_hl, fill=(120, 53, 15, int(255 * alpha_mul)))

    # 超大字填空 / 關鍵字卡片區 (48px!! 最多 2 條，教室後排超清楚)
    f_big = ImageFont.truetype(FONT_BOLD, 48)
    lines = meta["guide"] if mode == "guide" else meta["answer"]
    for idx_l, ltxt in enumerate(lines[:2]):
        ly = wb_y + 236 + idx_l * 195
        box_fill = (255, 255, 255, int(250 * alpha_mul))
        box_out = (148, 163, 184, int(220 * alpha_mul))
        txt_col = (15, 23, 42, int(255 * alpha_mul))
        if mode == "answer" and "[V]" in ltxt:
            box_fill = (236, 253, 245, int(250 * alpha_mul))
            box_out = (16, 185, 129, int(250 * alpha_mul))
            txt_col = (4, 120, 87, int(255 * alpha_mul))
        elif "[X]" in ltxt:
            box_fill = (254, 242, 242, int(250 * alpha_mul))
            box_out = (239, 68, 68, int(250 * alpha_mul))
            txt_col = (185, 28, 28, int(255 * alpha_mul))

        d.rounded_rectangle(
            [wb_x + 28, ly, wb_x + wb_w - 28, ly + 150],
            radius=20,
            fill=box_fill,
            outline=box_out,
            width=4,
        )
        tw = d.textlength(ltxt, font=f_big)
        tx = wb_x + max(42, (wb_w - tw) / 2)
        d.text((tx, ly + 46), ltxt, font=f_big, fill=txt_col)

    # 4. 3 秒課堂思考倒數提示卡 (白板下方專屬區 y=675..810，字體 40px)
    if has_countdown and rem <= 3.1:
        sec_num = max(1, min(3, int(math.ceil(rem))))
        cd_x, cd_y, cd_w, cd_h = wb_x + 28, wb_y + 650, wb_w - 56, 140
        d.rounded_rectangle(
            [cd_x, cd_y, cd_x + cd_w, cd_y + cd_h],
            radius=24,
            fill=(109, 40, 217, 248),
            outline=(253, 224, 71, 255),
            width=5,
        )
        f_cd = ImageFont.truetype(FONT_BOLD, 42)
        cd_txt = f"思考倒數：{sec_num} 秒"
        cd_tw = d.textlength(cd_txt, font=f_cd)
        d.text((cd_x + (cd_w - cd_tw) / 2, cd_y + 42), cd_txt, font=f_cd, fill=(255, 255, 255, 255))

    return Image.alpha_composite(canvas.convert("RGBA"), overlay).convert("RGB")


def render_shots_for_mode(mode):
    """步驟 2：渲染左右雙欄 1080p 24fps 視訊"""
    for idx, s in enumerate(SHOTS):
        sid = s["id"]
        dur_s = float(s["dur"])
        n_frames = int(round(dur_s * FPS))
        od = OUT / f"h3_{mode}" / sid
        od.mkdir(parents=True, exist_ok=True)
        clip_path = od / "clip.mp4"
        first_png = OUT / "first" / f"{sid}.png"
        # 裁切/縮放至填滿左側 1056x1080
        src = Image.open(first_png).convert("RGB")
        sw, sh = src.size
        scale = max(LEFT_W / sw, H / sh)
        rw, rh = int(sw * scale), int(sh * scale)
        src_fit = src.resize((rw, rh), Image.LANCZOS)
        left_base = src_fit.crop(((rw - LEFT_W) // 2, (rh - H) // 2, (rw - LEFT_W) // 2 + LEFT_W, (rh - H) // 2 + H))

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
            z = 1.02 + (0.06 * u if idx % 2 == 0 else 0.06 * (1.0 - u))
            cw, ch = int(LEFT_W / z), int(H / z)
            x0, y0 = (LEFT_W - cw) // 2, (H - ch) // 2
            left_frame = left_base.crop((x0, y0, x0 + cw, y0 + ch)).resize((LEFT_W, H), Image.BILINEAR)
            frame_im = compose_split_frame(left_frame, sid, u, fi, dur_s, mode=mode, has_countdown=bool(s.get("countdown")))
            enc.stdin.write(np.asarray(frame_im, dtype=np.uint8).tobytes())
        enc.stdin.close()
        enc.wait()
        print(f"[shot:{mode}] rendered {sid} ({dur_s:.1f}s)", flush=True)


def make_sheets():
    files = [OUT / "first" / f"{s['id']}.png" for s in SHOTS]
    cols = 4
    tw, th = 360, 360
    rows = (len(files) + cols - 1) // cols
    sheet = Image.new("RGB", (tw * cols, th * rows))
    f = ImageFont.truetype(FONT_BOLD, 28)
    for i, p in enumerate(files):
        t = Image.open(p).convert("RGB").resize((tw, th), Image.LANCZOS)
        ImageDraw.Draw(t).text((12, 8), p.stem, font=f, fill=(255, 255, 0), stroke_width=3, stroke_fill=(0, 0, 0))
        sheet.paste(t, ((i % cols) * tw, (i // cols) * th))
    sheet.save(OUT / "first" / "_sheet.jpg", quality=88)


def package_mode(mode, vtotal=120.0):
    post = OUT / "post"
    ed = OUT / "ending"
    parts = [OUT / f"h3_{mode}" / s["id"] / "clip.mp4" for s in SHOTS] + [ed / "ending.mp4"]
    (post / f"list_{mode}.txt").write_text("".join(f"file '{p.as_posix()}'\n" for p in parts), encoding="utf-8")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", str(post / f"list_{mode}.txt"), "-c", "copy", str(post / f"video_{mode}.mp4")], check=True)

    cut_dir = OUT / "cut"
    cut_dir.mkdir(exist_ok=True)
    out_1080 = cut_dir / f"film_{mode}_1080p.mp4"
    subprocess.run(
        [
            "ffmpeg", "-y", "-loglevel", "error",
            "-i", f"post/video_{mode}.mp4", "-i", "post/mix.wav",
            "-vf", "subtitles=post/subs.ass",
            "-map", "0:v", "-map", "1:a", "-t", f"{vtotal:.1f}",
            "-c:v", "libx264", "-crf", "16", "-preset", "medium", "-pix_fmt", "yuv420p",
            "-c:a", "aac", "-b:a", "256k", "-ar", "48000", "-movflags", "+faststart",
            f"cut/film_{mode}_1080p.mp4",
        ],
        cwd=str(OUT),
        check=True,
    )
    print(f"[cut] saved {out_1080}", flush=True)


def run_self_review(target_mp4):
    target_review = HERE / "review.py"
    r = subprocess.run([sys.executable, str(target_review), str(target_mp4)], capture_output=True, text=True, encoding="utf-8", errors="replace")
    print(r.stdout, flush=True)


if __name__ == "__main__":
    make_sheets()
    for m in ("guide", "answer"):
        render_shots_for_mode(m)
        package_mode(m, 120.0)
    run_self_review(OUT / "cut" / "film_guide_1080p.mp4")
    run_self_review(OUT / "cut" / "film_answer_1080p.mp4")

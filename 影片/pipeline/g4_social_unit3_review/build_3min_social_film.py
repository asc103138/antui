"""
山獅霸的多重宇宙 × 康軒版國小四年級上學期社會科第三單元總複習短片建置引擎
〈阿哲的時空大冒險！家鄉的傳統信仰與老街〉
規格：1920x1080 | 24 fps | 正片 22 鏡 170.0 秒 ＋ 金色法陣片尾 10.0 秒 ＝ 180.0 秒（整整 3 分鐘）
"""
import json
import math
import re
import subprocess
import sys
import wave
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

sys.path.insert(0, str(REPO / "tools"))
from fonts import font, SUB_FONT_NAME  # noqa: E402

FONT_BOLD = font("jhbd")
FONT_REG = font("jh")
FONT_KAI = font("kai")

# 每鏡專屬教學 HUD 與右側「社會筆記小卡」配置
HUD_META = {
    "S01": {
        "badge": "考前大作戰｜第 3 單元",
        "badge_color": (239, 68, 68),
        "title": "家鄉的傳統信仰與老街，真的那麼簡單嗎？",
        "block": "⚠️ 阿哲自信滿滿，準備迎接陳老師的突襲考題！",
        "block_color": (185, 28, 28),
        "card_title": "單元兩大主題",
        "card_lines": ["1. 信仰與生活", "2. 老街與生活", "目標：100 分！"],
        "card_accent": (248, 113, 113),
    },
    "S02": {
        "badge": "單元首頁｜臺中大甲",
        "badge_color": (14, 165, 233),
        "title": "大甲特色：鐵砧山、媽祖繞境與三大特產",
        "block": "💡 大甲三特產：芋頭 ＋ 奶油酥餅 ＋ 大甲草帽",
        "block_color": (3, 105, 161),
        "card_title": "臺中大甲小檔案",
        "card_lines": ["信仰：媽祖繞境", "地標：鐵砧山", "特產：芋頭/酥餅/草帽"],
        "card_accent": (56, 189, 248),
    },
    "S03": {
        "badge": "時空啟動｜紅白遙控器",
        "badge_color": (168, 85, 247),
        "title": "答錯啦！啟動實地複習大冒險",
        "block": "✨ 跟陳老師一起穿越時空，親眼看懂社會課本！",
        "block_color": (126, 34, 206),
        "card_title": "時空旅行出發",
        "card_lines": ["第 1 站：原住民族", "第 2 站：漢人信仰", "第 3 站：家鄉老街"],
        "card_accent": (192, 132, 252),
    },
    "S04": {
        "badge": "3-1｜原住民族祭典",
        "badge_color": (16, 185, 129),
        "title": "排灣族五年祭 ＆ 鄒族戰祭",
        "block": "🙏 祭典目的：表達對祖靈／神靈的敬畏，並祈求保佑",
        "block_color": (5, 150, 105),
        "card_title": "代表祭典筆記",
        "card_lines": ["排灣族：五年祭 (臺東達仁)", "鄒族：戰祭 (嘉義阿里山)", "團結族人・追念祖先"],
        "card_accent": (52, 211, 153),
    },
    "S05": {
        "badge": "破除迷思｜彩虹橋傳說",
        "badge_color": (245, 158, 11),
        "title": "五年祭不是放假！祖靈信仰如何影響生活？",
        "block": "🌈 泰雅族「彩虹橋傳說」：遵守祖先訓誡、努力生活",
        "block_color": (217, 119, 6),
        "card_title": "常見迷思破解",
        "card_lines": ["❌ 五年放假一次", "✅ 祖靈探訪子孫", "❤️ 感謝與追念祖先"],
        "card_accent": (251, 191, 36),
    },
    "S06": {
        "badge": "3-1｜泰雅族彩虹橋",
        "badge_color": (16, 185, 129),
        "title": "學會生活技能、成為正當有用的人",
        "block": "🏹 男生學打獵 ｜ 🧶 女生學織布 ➔ 過世後通過彩虹橋與祖靈相聚",
        "block_color": (5, 150, 105),
        "card_title": "彩虹橋約定",
        "card_lines": ["男生：認真學打獵", "女生：熟練織布技巧", "不讓族人挨餓受凍"],
        "card_accent": (52, 211, 153),
    },
    "S07": {
        "badge": "3-1｜外來文化交流",
        "badge_color": (59, 130, 246),
        "title": "桃園復興高遶教堂：宗教交流的見證",
        "block": "⛪ 改建歷程：竹子 ➔ 土磚(土埆) ➔ 方石 ➔ 鋼筋水泥",
        "block_color": (37, 99, 235),
        "card_title": "多元信仰交流",
        "card_lines": ["阿美族：巫師消災祈福", "基督教/天主教傳入", "高遶教堂：4 次改建"],
        "card_accent": (96, 165, 250),
    },
    "S08": {
        "badge": "迷思大考驗｜漢人神明",
        "badge_color": (239, 68, 68),
        "title": "土地公和媽祖，到底誰管農田、誰管航海？",
        "block": "⚠️ 警報！阿哲好像把兩位神明的職責記反囉！",
        "block_color": (185, 28, 28),
        "card_title": "神明配對題",
        "card_lines": ["土地公 ➔ ???", "媽祖 ➔ ???", "小心別選反啦！"],
        "card_accent": (248, 113, 113),
    },
    "S09": {
        "badge": "3-1｜漢人傳統信仰",
        "badge_color": (245, 158, 11),
        "title": "認識漢人兩大常見神明稱號與職責",
        "block": "🌾 土地公(福德正神)：護農田村莊 ｜ ⛵ 媽祖(天上聖母)：保航海平安",
        "block_color": (180, 83, 9),
        "card_title": "必考神明對照",
        "card_lines": ["土地公＝福德正神", "  (臺灣最常見廟宇)", "媽祖＝天上聖母"],
        "card_accent": (251, 191, 36),
    },
    "S10": {
        "badge": "3-1｜廟宇功能與環保",
        "badge_color": (16, 185, 129),
        "title": "廟宇是信仰中心，廟前廣場更是聚會好地方",
        "block": "🙏 現代環保新觀念：減少燒香、雙手合掌一樣虔誠！",
        "block_color": (5, 150, 105),
        "card_title": "廟宇三大作用",
        "card_lines": ["1. 當地信仰中心", "2. 休閒聚會廣場", "3. 辦慶典聯絡感情"],
        "card_accent": (52, 211, 153),
    },
    "S11": {
        "badge": "習作必考陷阱｜尊重包容",
        "badge_color": (239, 68, 68),
        "title": "請不能吃豬肉的外籍看護吃香腸便當？",
        "block": "❌ 錯誤示範！不能強迫他人「入境隨俗」違反信仰禁忌",
        "block_color": (185, 28, 28),
        "card_title": "習作情境判斷",
        "card_lines": ["外籍看護不吃豬肉", "強迫吃＝不尊重！", "應該替她換別的餐點"],
        "card_accent": (248, 113, 113),
    },
    "S12": {
        "badge": "3-1｜信仰與現代生活",
        "badge_color": (59, 130, 246),
        "title": "修身養性、行善助人，尊重與包容不同信仰",
        "block": "🤝 尊重實踐：週日要禮拜改約週六打球、等親友禱告再開動",
        "block_color": (37, 99, 235),
        "card_title": "尊重與包容三招",
        "card_lines": ["1. 尊重飲食禁忌", "2. 配合禮拜改約打球", "3. 等飯前禱告再開動"],
        "card_accent": (96, 165, 250),
    },
    "S13": {
        "badge": "3-2｜老街建築解密",
        "badge_color": (217, 119, 6),
        "title": "為什麼老街的房子都有長長的走廊？",
        "block": "🏠 街屋設計（如金門金城老街）：前面設「騎樓」供行人遮陽避雨",
        "block_color": (180, 83, 9),
        "card_title": "街屋秘密探索",
        "card_lines": ["店面：朝向街道", "走廊：騎樓遮陽避雨", "後面/樓上：住哪裡？"],
        "card_accent": (251, 191, 36),
    },
    "S14": {
        "badge": "3-2｜老街的起源與空間",
        "badge_color": (16, 185, 129),
        "title": "廟宇附近形成市集 ➔ 演變成熱鬧老街",
        "block": "🏪 空間分配：前店（做生意＋騎樓）｜ 後方與樓上（商家起居作息）",
        "block_color": (5, 150, 105),
        "card_title": "老街發展公式",
        "card_lines": ["廟宇人群聚集", "➔ 市集 / 商店街", "➔ 前店後住家街屋"],
        "card_accent": (52, 211, 153),
    },
    "S15": {
        "badge": "3-2｜老街轉變 ① ②",
        "badge_color": (14, 165, 233),
        "title": "現代老街的三種轉變（沒落 vs 新舊並存）",
        "block": "📍 臺南橋南老街：港口淤積而沒落 ｜ 📍 臺中南屯老街：老店與新店並存",
        "block_color": (3, 105, 161),
        "card_title": "老街轉變 1 & 2",
        "card_lines": ["① 沒落轉住宅：", "   臺南橋南 (港口淤積)", "② 新舊並存：臺中南屯"],
        "card_accent": (56, 189, 248),
    },
    "S16": {
        "badge": "3-2｜老街轉變 ③ 觀光",
        "badge_color": (168, 85, 247),
        "title": "保留原本建築風貌，變身熱門觀光老街！",
        "block": "📸 彰化鹿港(閩南建築) ｜ 新北三峽(金牛角/藍染) ｜ 雲林西螺(洋樓/醬油)",
        "block_color": (126, 34, 206),
        "card_title": "觀光老街代表",
        "card_lines": ["鹿港：閩南式建築", "三峽：祖師廟/金牛角", "西螺：洋樓/米糕/醬油"],
        "card_accent": (192, 132, 252),
    },
    "S17": {
        "badge": "3-2｜街道多元風貌",
        "badge_color": (236, 72, 153),
        "title": "觀光街與異國街：家鄉街道越來越豐富",
        "block": "🌏 花蓮火車站麻糬街 ｜ 臺北北平西路「印尼街」(薑黃飯/服飾雜貨)",
        "block_color": (190, 24, 93),
        "card_title": "多元風貌原因",
        "card_lines": ["工商業發達・觀光發展", "新住民與國際移工增加", "臺北北平西路＝印尼街"],
        "card_accent": (244, 114, 182),
    },
    "S18": {
        "badge": "學習方法｜小探究家",
        "badge_color": (245, 158, 11),
        "title": "老街資料這麼多，怎麼整理才不會眼花？",
        "block": "🤔 課本第 68–69 頁教你用「四步驟」＋「T 表／T 圖」做報告！",
        "block_color": (217, 119, 6),
        "card_title": "老街報告卡關了？",
        "card_lines": ["地址？建築？美食？", "資料太亂怎麼辦？", "交給小探究家四步驟！"],
        "card_accent": (251, 191, 36),
    },
    "S19": {
        "badge": "3-2｜小探究家 4 步驟",
        "badge_color": (16, 185, 129),
        "title": "探究老街四步驟：一學就會的整理術",
        "block": "① 發現問題 ➔ ② 蒐集資料 ➔ ③ T表整理分析 ➔ ④ 行動省思",
        "block_color": (5, 150, 105),
        "card_title": "探究四步驟",
        "card_lines": ["1. 發現問題", "2. 蒐集資料", "3. 整理分析 (T表/T圖)", "4. 行動省思"],
        "card_accent": (52, 211, 153),
    },
    "S20": {
        "badge": "總複習｜黃金記憶口訣",
        "badge_color": (59, 130, 246),
        "title": "四句口訣秒殺康軒四上社會第三單元！",
        "block": "🎵 原漢信仰要尊重｜廟口市集變老街｜騎樓前店後住家｜多元文化在家鄉",
        "block_color": (29, 78, 216),
        "card_title": "考前必背四句",
        "card_lines": ["1. 原漢信仰要尊重", "2. 廟口市集變老街", "3. 騎樓前店後住家", "4. 多元文化在家鄉"],
        "card_accent": (96, 165, 250),
    },
    "S21": {
        "badge": "首尾呼應｜大甲三特產",
        "badge_color": (16, 185, 129),
        "title": "答對了！送你大甲芋頭酥、奶油酥餅與草帽",
        "block": "🎁 還記得開場的大甲三大特產嗎？芋頭、酥餅、草帽全到位！",
        "block_color": (5, 150, 105),
        "card_title": "通關獎勵解鎖",
        "card_lines": ["✅ 芋頭 (芋頭酥)", "✅ 酥餅 (奶油酥餅)", "✅ 大甲草帽"],
        "card_accent": (52, 211, 153),
    },
    "S22": {
        "badge": "全劇終｜考 100 分再吃！",
        "badge_color": (239, 68, 68),
        "title": "想偷吃芋頭酥？考完試一百分再說！",
        "block": "🎉 祝大家四上社會第三單元複習順利，考試 100 分！",
        "block_color": (185, 28, 28),
        "card_title": "下次見！",
        "card_lines": ["第三單元複習完成", "記得複習課本 p.52-69", "我們考場見！"],
        "card_accent": (248, 113, 113),
    },
}


def ease_out_cubic_bezier(t):
    """模擬 cubic-bezier(0.23, 1, 0.32, 1) 強烈自訂 ease-out 曲線"""
    t = max(0.0, min(1.0, t))
    return 1.0 - (1.0 - t) ** 3.2


def draw_hud_and_note_card(base_img, sid, u, frame_idx):
    """繪製頂部教學重點 HUD 字卡與右側「社會筆記小卡」（嚴守 Emil Kowalski 進場規範：起點 scale 0.95 + ease-out）"""
    meta = HUD_META[sid]
    overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(overlay)

    # 進場動畫 0.28 秒（約 7 格）：從 opacity 0 + scale 0.95 平滑減速到位
    enter_p = ease_out_cubic_bezier(min(1.0, frame_idx / 7.0))
    alpha_mul = enter_p
    y_off = int((1.0 - enter_p) * 18)

    # 1. 頂部教學 HUD 卡片 (x=48..1430, y=36..196)
    card_x, card_y, card_w, card_h = 48, 36 - y_off, 1382, 160
    bg_alpha = int(218 * alpha_mul)
    border_alpha = int(230 * alpha_mul)
    d.rounded_rectangle(
        [card_x, card_y, card_x + card_w, card_y + card_h],
        radius=22,
        fill=(15, 23, 42, bg_alpha),
        outline=(255, 255, 255, int(65 * alpha_mul)),
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

    # 標題文字
    d.text(
        (bx + bw + 20, by + 1),
        meta["title"],
        font=f_title,
        fill=(255, 248, 220, int(255 * alpha_mul)),
    )

    # 下排考點橫條
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

    # 2. 右上角「社會筆記小卡」(x=1460..1872, y=36..238)
    nc_x, nc_y, nc_w, nc_h = 1460, 36 - y_off, 412, 202
    ac = meta["card_accent"]
    d.rounded_rectangle(
        [nc_x, nc_y, nc_x + nc_w, nc_y + nc_h],
        radius=22,
        fill=(15, 23, 42, bg_alpha),
        outline=(ac[0], ac[1], ac[2], border_alpha),
        width=3,
    )
    # 筆記卡標題列
    d.rounded_rectangle(
        [nc_x + 14, nc_y + 14, nc_x + nc_w - 14, nc_y + 56],
        radius=12,
        fill=(ac[0], ac[1], ac[2], int(55 * alpha_mul)),
    )
    f_nc_title = ImageFont.truetype(FONT_BOLD, 25)
    f_nc_line = ImageFont.truetype(FONT_BOLD, 24)
    tw = d.textlength(meta["card_title"], font=f_nc_title)
    d.text(
        (nc_x + (nc_w - tw) / 2, nc_y + 20),
        meta["card_title"],
        font=f_nc_title,
        fill=(ac[0], ac[1], ac[2], int(255 * alpha_mul)),
    )
    for idx_l, line_txt in enumerate(meta["card_lines"][:3]):
        ly = nc_y + 70 + idx_l * 40
        d.text(
            (nc_x + 24, ly),
            line_txt,
            font=f_nc_line,
            fill=(248, 250, 252, int(255 * alpha_mul)),
        )

    return Image.alpha_composite(base_img.convert("RGBA"), overlay).convert("RGB")


def generate_voices(force=False):
    """步驟 1：使用 Windows OneCore 台灣國語雙角色語音 (Zhiwei 調高音高飾阿哲、Yating 飾陳老師)，並自動微調語速以確保 0 截斷"""
    vd = OUT / "voice"
    bv_dir = vd / "bv"
    bv_dir.mkdir(parents=True, exist_ok=True)
    ps_script = HERE / "tts_onecore.ps1"
    picks = {}
    for i, s in enumerate(SHOTS):
        sid = s["id"]
        who = s["who"]
        voice_match = "Zhiwei" if who == "zhe" else "Yating"
        raw_wav = bv_dir / f"line{i}_raw.wav"
        wav_path = bv_dir / f"line{i}.wav"
        if force or not wav_path.exists():
            subprocess.run(
                [
                    "powershell", "-ExecutionPolicy", "Bypass", "-File", str(ps_script),
                    "-Text", s["text"],
                    "-VoiceMatch", voice_match,
                    "-OutWav", str(raw_wav),
                ],
                check=True,
                stdout=subprocess.DEVNULL,
            )
            # 阿哲：音高 +15% (10歲男童) + 語速 1.05；陳老師：自然女聲語速 1.22
            if who == "zhe":
                af = "silenceremove=start_periods=1:start_silence=0.04:start_threshold=-45dB:stop_periods=-1:stop_silence=0.10:stop_threshold=-45dB,asetrate=16000*1.15,aresample=48000,atempo=1.06"
            else:
                af = "silenceremove=start_periods=1:start_silence=0.04:start_threshold=-45dB:stop_periods=-1:stop_silence=0.10:stop_threshold=-45dB,atempo=1.22"
            subprocess.run(
                [
                    "ffmpeg", "-y", "-loglevel", "error",
                    "-i", str(raw_wav),
                    "-af", af,
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
        # 若台詞比鏡頭可容納空間長，自動微加速確保不截斷
        max_allow = float(s["dur"]) - 0.55
        if d_sec > max_allow:
            spd = min(1.28, (d_sec / max_allow) * 1.03)
            tmp_wav = bv_dir / f"line{i}_fast.wav"
            subprocess.run(
                ["ffmpeg", "-y", "-loglevel", "error", "-i", str(wav_path), "-af", f"atempo={spd:.3f}", str(tmp_wav)],
                check=True,
            )
            tmp_wav.replace(wav_path)
            r2 = subprocess.run(
                ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(wav_path)],
                capture_output=True, text=True, check=True,
            )
            d_sec = float(r2.stdout.strip())

        picks[str(i)] = {
            "shot": sid,
            "who": who,
            "text": s["text"],
            "file": str(wav_path),
            "dur": round(d_sec, 3),
        }
        print(f"[voice] {sid} ({CHARS[who]['name']}): {d_sec:.2f}s / shot {s['dur']}s", flush=True)
    (OUT / "voice_picks.json").write_text(json.dumps(picks, ensure_ascii=False, indent=2), encoding="utf-8")
    return picks


def render_shots():
    """步驟 2：為 22 鏡生成 1080p 24fps 動態視覺片段（Ken Burns 緩推/緩拉 + HUD + 筆記小卡）"""
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
            z = 1.02 + (0.06 * u if idx % 2 == 0 else 0.06 * (1.0 - u))
            dx, dy = 0, 0
            # S03 時空傳送震動 & S18 昏倒震動
            if sid in ("S03", "S18") and 0.15 <= u <= 0.45:
                dx = int(math.sin(fi * 2.2) * 8)
                dy = int(math.cos(fi * 2.8) * 6)

            cw, ch = int(W / z), int(H / z)
            x0 = max(0, min(W - cw, (W - cw) // 2 + dx))
            y0 = max(0, min(H - ch, (H - ch) // 2 + dy))
            frame_im = base_im.crop((x0, y0, x0 + cw, y0 + ch)).resize((W, H), Image.BILINEAR)
            frame_im = draw_hud_and_note_card(frame_im, sid, u, fi)
            enc.stdin.write(np.asarray(frame_im, dtype=np.uint8).tobytes())
        enc.stdin.close()
        enc.wait()
        print(f"[shot] rendered {sid} ({dur_s:.1f}s, {n_frames} frames)", flush=True)


def make_sheets():
    """產生 22 鏡首幀總覽接觸表 out/first/_sheet.jpg"""
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


def load_sfx(rel_path, target_len=None, vol=0.22):
    p = REPO / "sfx" / rel_path
    if not p.exists():
        return np.zeros(0, dtype=np.float32)
    raw = subprocess.run(
        ["ffmpeg", "-loglevel", "error", "-i", str(p), "-ar", str(SR), "-ac", "1", "-f", "f32le", "-"],
        capture_output=True, check=True,
    ).stdout
    a = np.frombuffer(raw, np.float32).copy()
    if target_len is not None and len(a) > target_len:
        a = a[:target_len]
    mx = float(np.max(np.abs(a)) + 1e-9)
    return a / mx * vol


def synthesize_music_and_sfx(total_sec, story_end_sec, shot_starts):
    """合成輕快冒險木琴背景配樂 + CC0 真實音效"""
    n = int(total_sec * SR) + SR
    t = np.arange(n, dtype=np.float32) / SR

    # 1. 輕快 C 大調校園冒險進行曲 (BPM 108 -> 1拍 = 0.555s)
    beat_sec = 0.555
    melody_freqs = [
        523.25, 659.25, 783.99, 659.25,
        587.33, 698.46, 880.00, 698.46,
        659.25, 783.99, 1046.5, 880.00,
        783.99, 659.25, 587.33, 523.25,
    ]
    mus = np.zeros(n, dtype=np.float32)
    num_beats = int(story_end_sec / beat_sec) + 2
    for bi in range(num_beats):
        t0 = bi * beat_sec
        s0 = int(t0 * SR)
        dur_n = int(0.42 * SR)
        if s0 + dur_n >= n:
            break
        f0 = melody_freqs[bi % len(melody_freqs)]
        tt = np.arange(dur_n, dtype=np.float32) / SR
        env = np.exp(-tt * 7.0) * np.minimum(1.0, tt / 0.008)
        note = 0.7 * np.sin(2 * math.pi * f0 * tt) + 0.25 * np.sin(2 * math.pi * f0 * 2 * tt)
        mus[s0:s0 + dur_n] += note * env * 0.32
        if bi % 2 == 0:
            bass_f = 261.63 if (bi // 4) % 2 == 0 else 196.00
            mus[s0:s0 + dur_n] += np.sin(2 * math.pi * bass_f * tt) * np.exp(-tt * 5.0) * 0.16

    # 片尾 10 秒溫暖和弦
    es0 = int(story_end_sec * SR)
    et = np.arange(n - es0, dtype=np.float32) / SR
    pad = (
        np.sin(2 * math.pi * 261.63 * et)
        + np.sin(2 * math.pi * 329.63 * et)
        + np.sin(2 * math.pi * 392.00 * et)
    ) * 0.12 * np.minimum(1.0, et / 0.6)
    mus[es0:] += pad

    # 2. 音效軌
    sfx = np.zeros(n, dtype=np.float32)

    def add_sfx(arr, t_sec):
        idx0 = int(t_sec * SR)
        if 0 <= idx0 < n and len(arr) > 0:
            m = min(len(arr), n - idx0)
            sfx[idx0:idx0 + m] += arr[:m]

    def add_beep(freq, t_sec, dur=0.14, amp=0.16):
        idx0 = int(t_sec * SR)
        ln = int(dur * SR)
        if 0 <= idx0 < n - ln:
            tt = np.arange(ln, dtype=np.float32) / SR
            env = np.exp(-tt * 14.0) * np.minimum(1.0, tt / 0.005)
            sfx[idx0:idx0 + ln] += np.sin(2 * math.pi * freq * tt) * env * amp

    # 時空傳送音效 (S03, S13, S22) & 警報/錯誤音效 (S08, S11) & 翻書 (S18) & 歡呼 (S20, S21)
    add_beep(880, shot_starts["S03"] + 0.15, 0.12, 0.15)
    add_beep(1174, shot_starts["S03"] + 0.28, 0.18, 0.15)
    add_beep(330, shot_starts["S08"] + 4.8, 0.22, 0.16)
    add_beep(293, shot_starts["S11"] + 0.2, 0.20, 0.15)
    add_beep(1046, shot_starts["S13"] + 0.1, 0.15, 0.15)
    add_sfx(load_sfx("翻頁/flip_book_1.wav", int(1.0 * SR), 0.16), shot_starts["S18"] + 0.2)
    add_sfx(load_sfx("歡呼/kids_cheer_1.wav", int(2.2 * SR), 0.18), shot_starts["S20"] + 5.2)
    add_beep(523, shot_starts["S22"] + 3.2, 0.12, 0.14)
    add_beep(784, shot_starts["S22"] + 3.35, 0.18, 0.14)

    return mus, sfx


def ass_time(t):
    t = max(0.0, t)
    return f"{int(t // 3600)}:{int(t % 3600 // 60):02d}:{t % 60:05.2f}"


def split_caption_clauses(text, max_len=16):
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
    """步驟 3 & 4：建立 170.0s 正片 + 10.0s 片尾 = 180.0s 完整時間軸、混音、響度校準與 ASS 字幕燒錄"""
    post = OUT / "post"
    post.mkdir(exist_ok=True)

    # 1. 產生 10.0 秒山獅霸金色法陣片尾
    ed = OUT / "ending"
    (ed / "frames").mkdir(parents=True, exist_ok=True)
    closeups = ["S01", "S20"]
    cards_tools = [
        [["Google Gemini", "劇本與三階審查"], ["Windows OneCore", "台灣國語雙角色配音"]],
        [["AI 圖像生成", "16:9 無字首幀"], ["FFmpeg + PIL", "1080p 動態合成"]],
    ]
    cards = []
    for i, tools in enumerate(cards_tools):
        sid = closeups[i % len(closeups)]
        Image.open(OUT / "first" / f"{sid}.png").convert("RGB").save(ed / "frames" / f"close{i + 1}.png")
        cards.append(dict(image=f"frames/close{i + 1}.png", tools=tools))
    render_cfg = {
        "_base": str(ed),
        "title": CFG["title"],
        "header": "康軒四上社會第三單元｜本片由以下 AI 工具協作完成",
        "card_dur": 2.0,
        "title_dur": 6.0,
        "out": "ending.mp4",
        "cards": cards,
    }
    (ed / "config.json").write_text(json.dumps(render_cfg, ensure_ascii=False, indent=2), encoding="utf-8")
    subprocess.run([sys.executable, str(REPO / "templates" / "ending" / "render_ending.py"), str(ed / "config.json")], check=True)

    # 2. 計算 EDL 時間軸（170.0s + 10.0s = 180.0s）
    t_cur = 0.0
    rows = []
    parts = []
    shot_starts = {}
    for i, s in enumerate(SHOTS):
        sid = s["id"]
        d_shot = float(s["dur"])
        shot_starts[sid] = t_cur
        p_info = picks[str(i)]
        v_dur = float(p_info["dur"])
        at_sec = min(float(s.get("at", 0.4)), max(0.15, d_shot - v_dur - 0.3))
        f_start = round(t_cur + at_sec, 3)
        f_end = round(f_start + v_dur, 3)
        lines = [
            {
                "id": f"line{i}",
                "who": s["who"],
                "text": s["text"],
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
    vtotal = round(t_cur + 10.0, 3)
    edl_data = {"shots": rows, "story_end": round(t_cur, 3), "total": vtotal}
    (post / "edl.json").write_text(json.dumps(edl_data, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"[edl] story_end={edl_data['story_end']}s + ending=10.0s -> total={vtotal}s", flush=True)

    # 3. 串接 1080p 無聲視訊軌
    (post / "list.txt").write_text("".join(f"file '{p.as_posix()}'\n" for p in parts), encoding="utf-8")
    subprocess.run(
        ["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", str(post / "list.txt"), "-c", "copy", str(post / "video.mp4")],
        check=True,
    )

    # 4. 混音
    n = int(vtotal * SR) + SR
    voice_track = np.zeros(n, dtype=np.float32)
    duck = np.ones(n, dtype=np.float32)
    under = float(CFG["mix"].get("music_under_lines", 0.22))

    for r in rows:
        for l in r["lines"]:
            raw_v = subprocess.run(
                ["ffmpeg", "-loglevel", "error", "-i", l["file"], "-ar", str(SR), "-ac", "1", "-f", "f32le", "-"],
                capture_output=True, check=True,
            ).stdout
            a = np.frombuffer(raw_v, np.float32).copy()
            rms_v = float(np.sqrt((a ** 2).mean()) + 1e-9)
            a = a / rms_v * 0.14
            s0 = int(l["film_start"] * SR)
            voice_track[s0:s0 + len(a)] += a[: n - s0]
            duck[max(0, int((l["film_start"] - 0.20) * SR)):min(n, int((l["film_end"] + 0.30) * SR))] = under

    k = int(0.12 * SR)
    duck = np.convolve(duck, np.ones(k) / k, mode="same")
    mus, sfx_track = synthesize_music_and_sfx(vtotal, edl_data["story_end"], shot_starts)
    rms_m = float(np.sqrt((mus[: int(edl_data["story_end"] * SR)] ** 2).mean()) + 1e-9)
    mus = mus / rms_m * float(CFG["mix"].get("music_bed_rms", 0.032))

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

    # 5. 產生 ASS 字幕
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
            tot_d = (l["film_end"] - l["film_start"]) + 0.24
            for ci, clause in enumerate(clauses):
                seg_d = tot_d * (len(clause) / max(1, total_chars))
                nxt_t = min(r["start"] + r["dur"] - 0.05, cur_t + seg_d)
                speaker_prefix = f"{CHARS[l['who']]['name']}：" if ci == 0 else ""
                ev += f"Dialogue: 0,{ass_time(cur_t)},{ass_time(nxt_t)},{l['who']},,0,0,0,,{speaker_prefix}{clause}\n"
                cur_t = nxt_t

    ass_path = post / "subs.ass"
    ass_path.write_text(hdr + ev, encoding="utf-8")

    # 6. 燒錄字幕並輸出 1080p 與 720p
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
            "-t", f"{vtotal:.1f}",
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
    target_review = HERE / "review.py"
    if rv_script.exists() and not target_review.exists():
        target_review.write_text(rv_script.read_text(encoding="utf-8"), encoding="utf-8")
    r = subprocess.run([sys.executable, str(target_review), str(OUT / "cut" / "film_1080p.mp4")], capture_output=True, text=True, encoding="utf-8", errors="replace")
    print(r.stdout, flush=True)
    if r.stderr:
        print(r.stderr, flush=True)


if __name__ == "__main__":
    picks_file = OUT / "voice_picks.json"
    if picks_file.exists():
        picks = json.loads(picks_file.read_text(encoding="utf-8"))
    else:
        picks = generate_voices(force=False)
    if not (OUT / "h3" / "S22" / "clip.mp4").exists():
        render_shots()
    if not (OUT / "first" / "_sheet.jpg").exists():
        make_sheets()
    build_edl_and_cut(picks)
    run_self_review()

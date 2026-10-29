import os
import sys
import subprocess
from PIL import Image, ImageDraw, ImageFont

FONT_PATH = "C:/Windows/Fonts/msjhbd.ttc"
if not os.path.exists(FONT_PATH):
    FONT_PATH = "C:/Windows/Fonts/msjh.ttc"

def get_font(size):
    return ImageFont.truetype(FONT_PATH, size)

FPS = 30
TOTAL_DURATION = 205.32
TOTAL_FRAMES = int(TOTAL_DURATION * FPS)

SCENES = [
    {
        "start": 0.0,
        "end": 15.0,
        "kicker": "國小四年級社會 · 第二單元 (康軒版)",
        "title": "走進時光隧道 · 家鄉的傳統住屋與器具",
        "subtitle": "解鎖早期臺灣先民就地取材與適應環境的生活大智慧",
        "subtitles": [
            (0.0, 7.5, "歡迎來到四年級社會時光探險隊！"),
            (7.5, 15.0, "今天我們要穿越時空，解鎖早期臺灣先民的居住與生活大智慧。")
        ],
        "cards": [
            {"title": "2-1 傳統住屋", "desc": "原住民（石板屋、地下屋、防鼠穀倉）\n漢人（三合院、土埆厝、街屋騎樓）", "accent": "#38BDF8"},
            {"title": "2-2 傳統生活器具", "desc": "原住民（木臼杵、百步蛇陶壺、竹編魚筌）\n漢人（紅磚大灶、雙扇石磨、手搖風鼓、防蟻菜櫥）", "accent": "#F59E0B"}
        ]
    },
    {
        "start": 15.0,
        "end": 50.0,
        "kicker": "2-1 傳統住屋篇 (原住民)",
        "title": "原住民族的智慧建築：因地制宜與大自然共處",
        "subtitle": "就地取材黑灰石板、開挖地下避強風、高腳防鼠守護糧食",
        "subtitles": [
            (15.0, 20.0, "首先進入二之一：傳統住屋篇。"),
            (20.0, 26.0, "住屋的樣貌，反映了先民就地取材與適應氣候的超凡智慧。"),
            (26.0, 31.0, "原住民依據生活環境，發展出因地制宜的經典建築："),
            (31.0, 39.0, "排灣族與魯凱族運用板岩頁岩堆疊出冬暖夏涼的石板屋，防風抗震。"),
            (39.0, 45.0, "蘭嶼達悟族開挖地下屋避強風，地面搭配通風涼台。"),
            (45.0, 50.0, "泰雅族以竹木建屋，並設計帶防鼠板的高腳穀倉阻擋鼠患！")
        ],
        "cards": [
            {"title": "排灣/魯凱【石板屋】", "desc": "• 取材山林頁岩與板岩層層咬合\n• 建築低矮冬暖夏涼，抵抗颱風地震\n• 門楣飾百步蛇圖騰象徵祖靈守護", "accent": "#38BDF8"},
            {"title": "達悟族【半穴居地下屋】", "desc": "• 主屋向下開挖，深入地底避強風\n• 抵擋夏季颱風與冬季狂暴東北季風\n• 地面上設高架涼台通風乘涼", "accent": "#10B981"},
            {"title": "泰雅/太魯閣【防鼠高腳穀倉】", "desc": "• 柱體高高挑起，阻隔潮濕地氣\n• 柱頂套設圓形防鼠木板卡死攀爬路徑\n• 妥善儲藏保護全家人的珍貴小米", "accent": "#F59E0B"}
        ]
    },
    {
        "start": 50.0,
        "end": 95.0,
        "kicker": "2-1 傳統住屋篇 (漢人)",
        "title": "漢人先民的傳統住屋：家族禮法與市街人情",
        "subtitle": "三合院長幼尊卑、土埆厝隔熱保暖、騎樓亭仔腳遮陽避雨",
        "subtitles": [
            (50.0, 57.0, "而漢人先民的傳統住屋，同樣凝聚了深刻的家族禮法與環境智慧："),
            (57.0, 66.0, "最具代表性的三合院，由正身與左右護龍圍繞，前有大埕曬穀聚會。"),
            (66.0, 73.0, "正身中央是神明廳，彰顯尊卑長幼有序的倫理孝道。"),
            (73.0, 83.0, "早期就地取土混合稻草牛糞製成土埆厝，冬暖夏涼但最怕大雨水浸。"),
            (83.0, 95.0, "市街興起後，街屋前店後住，開闢騎樓亭仔腳供行人避雨，充滿人情味！")
        ],
        "cards": [
            {"title": "倫理空間【三合院】", "desc": "• 正身中央為神明廳供奉祖先\n• 左右護龍長幼分居，左尊右卑\n• 門前寬闊大埕曬稻穀與宗族聚會", "accent": "#EF4444"},
            {"title": "就地取材【土埆厝】", "desc": "• 稻草、米糠、泥土與牛糞壓製土埆磚\n• 泥土熱傳導慢，室內冬暖夏涼\n• 基座常墊卵石防水浸泡崩塌", "accent": "#F59E0B"},
            {"title": "市街溫情【街屋與騎樓】", "desc": "• 臨街商業街屋，前為店鋪後為住家\n• 留出騎樓（亭仔腳）讓過路人遮陽避雨\n• 狹長格局搭配天井採光通風", "accent": "#38BDF8"}
        ]
    },
    {
        "start": 95.0,
        "end": 140.0,
        "kicker": "2-2 傳統生活器具篇 (原住民)",
        "title": "原住民族的生活巧思：凝聚族群與生存智慧",
        "subtitle": "木臼木杵合力搗小米、百步蛇陶壺貴族傳家、竹編魚筌單向倒刺陷阱",
        "subtitles": [
            (95.0, 101.0, "接著進入二之二：傳統生活器具篇。"),
            (101.0, 107.0, "先民沒有現代電器與塑膠，一切器具全靠雙手與自然材料打造。"),
            (107.0, 114.0, "排灣族與魯凱族木臼長杵，逢年過節全村搗小米打麻糬，象徵團結；"),
            (114.0, 122.0, "手工雕刻百步蛇圖騰的陶壺，更是貴族家族代代相傳的傳家珍寶；"),
            (122.0, 140.0, "溪流捕魚使用的竹編魚筌具備單向倒刺，魚蝦游入無法脫逃，是神奇物理陷阱！")
        ],
        "cards": [
            {"title": "團結共作【木臼與木杵】", "desc": "• 原木鑿空成臼，配雙頭長木杵\n• 慶典時多人節奏合作搗小米麻糬\n• 凝聚部落情感與家族勞動記憶", "accent": "#10B981"},
            {"title": "貴族傳家【排灣/魯凱陶壺】", "desc": "• 壺身細緻雕刻百步蛇與太陽紋\n• 貴族與頭目傳承之信物與重要聘禮\n• 象徵祖靈祝福，神聖不可侵犯", "accent": "#F59E0B"},
            {"title": "物理陷阱【竹編魚筌】", "desc": "• 喇叭口形竹編，逆著溪流擺放\n• 內層倒鬚（倒刺）設計進得去出不來\n• 善用流體物理與魚類逆游習性", "accent": "#38BDF8"}
        ]
    },
    {
        "start": 140.0,
        "end": 190.0,
        "kicker": "2-2 傳統生活器具篇 (漢人)",
        "title": "漢人農家日常器具：勞動與廚房的智慧巧思",
        "subtitle": "柴火大灶炊粿、雙扇石磨出米漿、風鼓篩分飽滿穀粒、水盤防蟻菜櫥",
        "subtitles": [
            (140.0, 147.0, "漢人傳統農村廚房裡，更是處處藏著智慧："),
            (147.0, 155.0, "紅磚大灶燒柴煮飯炒菜，大鐵鍋還能蒸炊年糕菜包；"),
            (155.0, 164.0, "雙扇石磨利用逆時針旋轉碾磨，將浸泡的在來米磨成雪白米漿做粿；"),
            (164.0, 175.0, "收割稻穀時，手搖風鼓吹出氣流，吹走乾癟草屑留下飽滿稻穀；"),
            (175.0, 190.0, "竹篾菜罩通風防蒼蠅，菜櫥腳下墊注水防蟻陶盤阻斷螞蟻攀爬！")
        ],
        "cards": [
            {"title": "廚房心臟【紅磚大灶】", "desc": "• 灶口填柴生火，大鐵鍋導熱迅速均勻\n• 炊煮三餐、蒸炊年糕菜包、燒熱水\n• 灶上有灶君爺像，寄託家宅平安", "accent": "#EF4444"},
            {"title": "逆轉碾磨【雙扇石磨】", "desc": "• 上下兩片厚重石輪，上扇進料逆轉旋轉\n• 磨齒咬合細細碾磨在來米與黃豆\n• 磨出雪白米漿與豆漿做粿做粄", "accent": "#38BDF8"},
            {"title": "重力風力【手搖風鼓】", "desc": "• 手搖把帶動內部木製扇葉吹風\n• 飽滿實穀重直接下落，乾癟穀與屑隨風飛出\n• 物理流體比重篩分法效率極高", "accent": "#F59E0B"},
            {"title": "生活防疫【菜罩與防蟻菜櫥】", "desc": "• 竹篾編織圓形菜罩通風透氣防蒼蠅\n• 菜櫥四腳下置陶製防蟻水盤（隔水斷路）\n• 純天然物理防護無化學毒素", "accent": "#10B981"}
        ]
    },
    {
        "start": 190.0,
        "end": 205.32,
        "kicker": "學習總結 · 核心素養",
        "title": "就地取材 · 因地制宜 · 人與自然和諧共存",
        "subtitle": "原住民與漢人共同演繹的臺灣家鄉文化瑰寶",
        "subtitles": [
            (190.0, 198.0, "從住屋到器具，無論原住民還是漢人，都用雙手與大地和諧共處。"),
            (198.0, 205.32, "珍惜家鄉的文化瑰寶，我們下次時光探險再見！")
        ],
        "cards": [
            {"title": "環境適應智慧", "desc": "取之於自然（石板、竹木、泥土、黃藤），適應氣候颱風與地形", "accent": "#38BDF8"},
            {"title": "族群倫理與共榮", "desc": "部落搗米團結、三合院長幼有序、市街騎樓互助人情味", "accent": "#F59E0B"},
            {"title": "傳承家鄉珍寶", "desc": "用心觀察身邊的老物件與古老聚落，讓文化活在生活中！", "accent": "#10B981"}
        ]
    }
]

def render_frame(t):
    scene = None
    for s in SCENES:
        if s["start"] <= t <= s["end"]:
            scene = s
            break
    if scene is None:
        scene = SCENES[-1]

    img = Image.new("RGB", (1920, 1080), (10, 15, 29))
    draw = ImageDraw.Draw(img)

    # 頂部光暈
    draw.ellipse([460, -100, 1460, 300], fill=(17, 30, 60))

    # 頂部 Kicker 與標題
    font_kicker = get_font(26)
    font_title = get_font(46)
    font_sub = get_font(24)

    draw.text((100, 50), scene["kicker"], font=font_kicker, fill=(56, 189, 248))
    draw.text((100, 92), scene["title"], font=font_title, fill=(248, 250, 252))
    draw.text((100, 155), scene["subtitle"], font=font_sub, fill=(148, 163, 184))

    # 右上角時間標籤
    mins = int(t // 60)
    secs = int(t % 60)
    tot_mins = int(TOTAL_DURATION // 60)
    tot_secs = int(TOTAL_DURATION % 60)
    time_str = f"{mins:02d}:{secs:02d} / {tot_mins:02d}:{tot_secs:02d}"
    draw.text((1650, 60), time_str, font=get_font(24), fill=(148, 163, 184))

    # 繪製卡片
    cards = scene["cards"]
    num_cards = len(cards)
    left_margin = 100
    top_pos = 220
    card_h = 580
    avail_w = 1920 - 200
    gap = 24
    card_w = int((avail_w - (num_cards - 1) * gap) / num_cards)

    font_ctitle = get_font(28)
    font_cdesc = get_font(21)

    for i, c in enumerate(cards):
        cx = left_margin + i * (card_w + gap)
        # 背景
        draw.rounded_rectangle([cx, top_pos, cx + card_w, top_pos + card_h], radius=16, fill=(17, 26, 48), outline=(30, 45, 80), width=2)
        # 標題飾條
        accent_hex = c["accent"]
        r = int(accent_hex[1:3], 16)
        g = int(accent_hex[3:5], 16)
        b = int(accent_hex[5:7], 16)
        draw.rounded_rectangle([cx + 20, top_pos + 20, cx + card_w - 20, top_pos + 80], radius=10, fill=(r//4, g//4, b//4), outline=(r, g, b), width=2)
        draw.text((cx + 35, top_pos + 32), c["title"], font=font_ctitle, fill=(255, 255, 255))

        # 內容換行繪製
        lines = c["desc"].split("\n")
        y_text = top_pos + 110
        for l in lines:
            draw.text((cx + 25, y_text), l, font=font_cdesc, fill=(203, 213, 225))
            y_text += 40

    # 底部字幕
    cur_sub = ""
    for s_st, s_ed, s_text in scene["subtitles"]:
        if s_st <= t <= s_ed:
            cur_sub = s_text
            break
    if not cur_sub and scene["subtitles"]:
        cur_sub = scene["subtitles"][-1][2]

    # 字幕條背景
    draw.rounded_rectangle([100, 840, 1820, 940], radius=12, fill=(12, 19, 36), outline=(40, 60, 100), width=2)
    font_sub_big = get_font(34)
    # 文字置中
    bbox = draw.textbbox((0, 0), cur_sub, font=font_sub_big)
    tw = bbox[2] - bbox[0]
    draw.text((960 - tw // 2, 866), cur_sub, font=font_sub_big, fill=(254, 240, 138))

    # 底部進度條
    progress_w = int((t / TOTAL_DURATION) * 1920)
    draw.rectangle([0, 1068, 1920, 1080], fill=(20, 30, 50))
    draw.rectangle([0, 1068, progress_w, 1080], fill=(56, 189, 248))

    return img.tobytes()

def main():
    out_mp4 = "social_explainer_125s.mp4"
    audio_file = "social_explainer_tts.mp3"

    print(f"Rendering {TOTAL_FRAMES} frames ({TOTAL_DURATION}s @ {FPS}fps) to {out_mp4}...")

    cmd = [
        "ffmpeg", "-y",
        "-f", "rawvideo",
        "-vcodec", "rawvideo",
        "-s", "1920x1080",
        "-pix_fmt", "rgb24",
        "-r", str(FPS),
        "-i", "-",
        "-i", audio_file,
        "-c:v", "libx264",
        "-pix_fmt", "yuv420p",
        "-preset", "ultrafast",
        "-crf", "23",
        "-c:a", "aac",
        "-b:a", "192k",
        "-shortest",
        out_mp4
    ]

    proc = subprocess.Popen(cmd, stdin=subprocess.PIPE)

    report_interval = FPS * 10
    for frame_idx in range(TOTAL_FRAMES):
        t = frame_idx / FPS
        raw_bytes = render_frame(t)
        proc.stdin.write(raw_bytes)
        if frame_idx % report_interval == 0:
            pct = (frame_idx / TOTAL_FRAMES) * 100
            print(f"Progress: {frame_idx}/{TOTAL_FRAMES} frames ({pct:.1f}%)")

    proc.stdin.close()
    proc.wait()
    print("Render completed successfully!")

if __name__ == "__main__":
    main()

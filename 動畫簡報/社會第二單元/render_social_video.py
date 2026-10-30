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
TOTAL_DURATION = 271.85
TOTAL_FRAMES = int(TOTAL_DURATION * FPS)

# 100% 對齊微軟 Edge-TTS (zh-TW-HsiaoChenNeural) 毫秒級時間戳記與康軒四上真實教材
SUBTITLES = [
    (0.10, 3.86, "歡迎來到四年級社會時光探險隊！"),
    (3.81, 8.63, "今天我們要穿越時空，走進康軒版四上第二單元："),
    (8.63, 16.73, "家鄉的傳統住屋與生活器具，解鎖早期臺灣先民就地取材與適應環境的生活大智慧。"),
    (16.73, 20.61, "首先進入二之一：傳統住屋篇。"),
    (20.61, 26.01, "住屋的樣貌，反映了先民就地取材與適應氣候的智慧。"),
    (26.01, 31.37, "原住民依據生活環境，發展出因地制宜的經典建築："),
    (31.36, 35.48, "排灣族與魯凱族運用山林裡的板岩和頁岩，"),
    (35.48, 39.81, "層層咬合堆疊出石板屋，屋頂縫隙通風排煙，"),
    (39.81, 45.01, "煙燻還能形成保護防蟲防腐，冬暖夏涼且抗強颱地震，"),
    (45.01, 48.48, "更獲世界建築文物保護基金會守護。"),
    (48.48, 53.73, "蘭嶼達悟族為了避開夏季狂暴颱風，將主屋向下開挖，"),
    (53.73, 59.43, "深入地底建成半地下屋，地面上則搭配高架涼台通風休憩，"),
    (59.43, 62.49, "周圍鋪設鵝卵石水溝迅速排水。"),
    (62.49, 70.00, "泰雅族則就地取材竹木搭建家屋，通風防潮，適應山區濕潤多雨的氣候。"),
    (70.00, 76.82, "而漢人先民的傳統住屋，同樣凝聚了深刻的就地取材與家族倫理智慧："),
    (76.82, 83.80, "早期雲林麥寮常見竹管仔厝，用竹子作樑柱編竹夾泥，輕巧柔韌；"),
    (83.80, 88.39, "新北深坑則有土埆厝，以石塊奠定堅固基礎，"),
    (88.39, 93.21, "再用泥土混合稻草米糠壓製土埆磚，冬暖夏涼。"),
    (93.21, 98.32, "隨著家族人口增加，漢人住屋依生活需求擴建："),
    (98.33, 103.19, "從單列的一條龍，擴展為一正身一護龍的單伸手，"),
    (103.19, 106.51, "再擴建為一正身兩護龍的三合院。"),
    (106.51, 112.77, "三合院正身中央是神明廳，用來祭拜祖先神明與接待客人；"),
    (112.77, 119.49, "長輩居住在左廂房，晚輩居於右廂房，體現長幼尊卑的宗法倫理；"),
    (119.49, 125.39, "左右護龍設有廚房大灶炊煮，農具間靠近牛棚豬舍便利勞作，"),
    (125.39, 132.39, "門前寬闊的稻埕用來曬穀、聚會與遊戲，屋後則種植防風竹林遮擋強風。"),
    (132.39, 136.67, "現代住屋雖然多演變為鋼筋混凝土大樓公寓，"),
    (136.67, 143.31, "但老舊古厝透過活化轉型為特色民宿，更在祭祖節慶時吸引家族返鄉，"),
    (143.31, 144.81, "延續文化傳承。"),
    (144.81, 149.15, "接著進入二之二：傳統生活器具篇。"),
    (149.15, 155.97, "早期先民沒有現代電器與塑膠，一切器具全靠雙手與自然材料打造。"),
    (155.97, 160.26, "原住民在飲食與勞動中展現驚人巧思："),
    (160.26, 167.16, "木臼與長木杵整根原木鑿空，節奏合作搗小米脫殼，凝聚部落情感；"),
    (167.16, 173.75, "排灣族的百步蛇陶壺，更是貴族階級世代相傳的神聖傳家寶與聘禮；"),
    (173.75, 178.55, "耐高溫的阿美族陶鍋，用來炊煮野菜與熱湯；"),
    (178.55, 184.80, "排灣族雙人連杯，宴客時兩人並肩同飲，象徵深厚情誼；"),
    (184.80, 190.72, "阿美族更善用檳榔葉鞘折疊成食器，竹籤固定後耐火耐熱，"),
    (190.72, 193.23, "是天然環保的智慧食器；"),
    (193.23, 197.99, "溪流捕魚使用的竹編魚筌具備喇叭口與單向倒刺，"),
    (197.99, 202.97, "魚蝦順流游入便無法折返脫逃，是神奇的物理陷阱！"),
    (202.97, 208.61, "漢人農村廚房裡，同樣處處展現物盡其用的先民智慧："),
    (208.61, 216.00, "紅磚大灶以柴火高溫蒸粿炊飯，熄火後還能利用木柴餘溫灰燼燜熟香甜地瓜，"),
    (216.00, 221.21, "最後把富含鉀質的木柴灰燼拌入菜園土壤當天然肥料，"),
    (221.21, 224.69, "既防蟲害又肥沃土地，絲毫不浪費；"),
    (224.69, 231.79, "通風防蠅的木製菜櫥、堅固的木水桶與木砧板，陪伴了無數農家歲月。"),
    (231.80, 238.73, "到了現代，塑膠器具雖然輕便便宜，卻不易分解造成環境沉重負擔；"),
    (238.72, 244.50, "臺灣海岸淨灘統計中，寶特瓶更高居海洋廢棄物第一名！"),
    (244.50, 250.19, "透過自備環保餐具與提袋，我們能從日常落實源頭減塑。"),
    (250.19, 254.23, "在小探究家單元中，我們更能運用階層圖，"),
    (254.23, 261.46, "將斗笠、桌罩等日常生活類，與布農族藤編背簍等工作生產類器具分門別類，"),
    (261.46, 264.23, "掌握生活器具的原料與功能！"),
    (264.23, 271.85, "珍惜家鄉的傳統住屋與器具智慧，人與環境共好，我們下次時光探險再見！")
]

SCENES = [
    {
        "start": 0.0,
        "end": 16.73,
        "kicker": "國小四年級社會 · 第二單元 (康軒版)",
        "title": "走進時光隧道 · 家鄉的傳統住屋與生活器具",
        "subtitle": "解鎖早期臺灣先民就地取材與適應環境的生活大智慧 (課本 P.32-33)",
        "cards": [
            {"title": "2-1 傳統住屋與生活", "desc": "• 原住民族：石板屋、地下屋、木竹屋\n• 漢人先民：竹管仔厝、土埆厝、三合院\n• 因地制宜適應氣候，宗法倫理與家族傳承", "accent": "#38BDF8"},
            {"title": "2-2 器物與生活", "desc": "• 原住民族：木臼杵、陶壺、陶鍋、連杯、魚筌\n• 漢人先民：紅磚大灶、灰燼燜地瓜、肥料、菜櫥\n• 就地取材物盡其用，現代減塑永續實踐", "accent": "#F59E0B"}
        ]
    },
    {
        "start": 16.73,
        "end": 70.00,
        "kicker": "2-1 傳統住屋篇 (原住民族智慧建築)",
        "title": "原住民族的傳統住屋：因地制宜與自然共處",
        "subtitle": "就地取材黑灰板岩、開挖半地下避強風、竹木搭建通風防潮 (課本 P.34-35)",
        "cards": [
            {"title": "排灣/魯凱【石板屋】", "desc": "• 取材山林頁岩與板岩層層咬合堆疊\n• 屋頂石板縫隙通風排煙，防蟲防腐\n• 冬暖夏涼抵抗颱風地震，WMF守護遺產", "accent": "#38BDF8"},
            {"title": "達悟族【半地下屋】", "desc": "• 主屋向下開挖深入地底，避開夏季強颱\n• 平緩斜屋頂引導強風滑過，防風阻力低\n• 地面高架涼台通風休憩，深溝鵝卵石防澇", "accent": "#10B981"},
            {"title": "泰雅族【木竹傳統屋】", "desc": "• 就地取材竹子與木材建構家屋\n• 竹木縫隙良好通風，排除多餘濕氣\n• 適應多雨山林氣候，體現就地取材智慧", "accent": "#F59E0B"}
        ]
    },
    {
        "start": 70.00,
        "end": 144.81,
        "kicker": "2-1 傳統住屋篇 (漢人傳統住屋與空間格局)",
        "title": "漢人先民的傳統住屋：家族禮法與擴建智慧",
        "subtitle": "竹管土埆就地取材、擴建三部曲、合院空間倫理與文化傳承 (課本 P.36-41)",
        "cards": [
            {"title": "就地取材【竹管厝與土埆厝】", "desc": "• 麥寮竹管厝：竹柱竹樑編竹夾泥，輕巧柔韌\n• 深坑土埆厝：石塊基底，泥土混稻草壓磚\n• 隔熱保暖冬暖夏涼，反映環境材料適應", "accent": "#F59E0B"},
            {"title": "空間禮法【合院生活空間】", "desc": "• 擴建三部曲：一條龍 ➔ 單伸手 ➔ 三合院\n• 正廳神明祖先居中，長輩居左廂房左尊右卑\n• 大灶廚房炊煮、農具間、稻埕曬穀、防風竹林", "accent": "#EF4444"},
            {"title": "住屋再生【古厝活化傳承】", "desc": "• 傳統合院演變為現代鋼筋混凝土大樓公寓\n• 老舊古厝活化轉型為特色民宿文化休閒體驗\n• 逢年過節祭祖團聚，凝聚宗族延續文化根基", "accent": "#38BDF8"}
        ]
    },
    {
        "start": 144.81,
        "end": 202.97,
        "kicker": "2-2 傳統生活器具篇 (原住民族生活巧思)",
        "title": "原住民族傳統生活器具：族群凝聚與生存智慧",
        "subtitle": "木臼木杵合作舂米、神聖百步蛇陶壺、阿美葉鞘食器與竹編魚筌 (課本 P.42-43)",
        "cards": [
            {"title": "部落凝聚【木臼木杵與連杯】", "desc": "• 原木鑿空成臼，眾人節奏合作搗小米脫殼\n• 雙人雕刻木連杯並肩同飲，象徵真摯友誼\n• 凝聚部落深厚情感與家族互助記憶", "accent": "#10B981"},
            {"title": "祖靈神聖【陶壺、陶鍋與葉鞘】", "desc": "• 排灣百步蛇陶壺，貴族階級世代相傳聘禮\n• 阿美族耐火陶鍋，炊煮野菜鮮美熱湯\n• 檳榔葉鞘折疊食器，天然耐熱環保巧思", "accent": "#F59E0B"},
            {"title": "物理陷阱【竹編魚筌】", "desc": "• 喇叭口形竹編錐形陷阱，逆著溪流擺放\n• 內層單向倒刺（倒鬚）設計進得去出不來\n• 善用魚蝦逆游習性，純天然物理捕撈巧思", "accent": "#38BDF8"}
        ]
    },
    {
        "start": 202.97,
        "end": 250.19,
        "kicker": "2-2 傳統生活器具篇 (漢人日常器物與現代減塑)",
        "title": "漢人家鄉生活器具：物盡其用與現代減塑實踐",
        "subtitle": "柴火大灶、灰燼燜地瓜做肥料、透氣菜櫥與生活源頭減塑 (課本 P.44-47)",
        "cards": [
            {"title": "物盡其用【紅磚大灶與草木灰】", "desc": "• 紅磚大灶大鐵鍋，柴火高溫蒸粿炊飯\n• 餘溫柴灰燜烤地瓜，毫不浪費熱能源\n• 富鉀草木灰拌入菜園天然施肥防蟲害", "accent": "#EF4444"},
            {"title": "日常智慧【木製菜櫥水桶】", "desc": "• 木製菜櫥紗網透氣通風，防蒼蠅塵土\n• 實木水桶、木砧板堅固耐用陪伴歲月\n• 先民取材天然竹木，容易自然分解環境友善", "accent": "#10B981"},
            {"title": "現代減塑【海洋廢棄物實證】", "desc": "• 現代塑膠輕便便宜，但百年難自然分解\n• 臺灣淨灘統計：寶特瓶第一、吸管、免洗餐具\n• 自備環保杯袋與餐具，從日常生活源頭減塑", "accent": "#38BDF8"}
        ]
    },
    {
        "start": 250.19,
        "end": 271.85,
        "kicker": "學習專題 · 小探究家階層圖 (課本 P.48-51)",
        "title": "小探究家思維策略 · 階層圖分門別類",
        "subtitle": "生活器具分門別類、因地制宜物盡其用、人與自然共榮",
        "cards": [
            {"title": "階層圖【日常生活類】", "desc": "• 斗笠：竹篾編織，遮陽擋雨通風透氣\n• 桌罩：竹篾編織，覆蓋飯菜防蠅透氣\n• 掌握器具原料、用途與生活使用場合", "accent": "#38BDF8"},
            {"title": "階層圖【工作生產類】", "desc": "• 布農族藤編背簍：黃藤編織，雙肩背負\n• 上山採集與收穫搬運農作物，堅韌耐重\n• 善用材料物理工程特性，減輕勞作負擔", "accent": "#F59E0B"},
            {"title": "人與自然【永續傳承】", "desc": "• 因地制宜就地取材，順應風土氣候\n• 物盡其用不浪費，源頭減塑愛護地球\n• 傳承家鄉先民生活大智慧，文化永續共榮", "accent": "#10B981"}
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

    # 頂部柔和微光暈
    draw.ellipse([460, -100, 1460, 300], fill=(17, 30, 60))

    # 頂部 Kicker 與標題
    font_kicker = get_font(26)
    font_title = get_font(44)
    font_sub = get_font(23)

    draw.text((100, 48), scene["kicker"], font=font_kicker, fill=(56, 189, 248))
    draw.text((100, 88), scene["title"], font=font_title, fill=(248, 250, 252))
    draw.text((100, 150), scene["subtitle"], font=font_sub, fill=(148, 163, 184))

    # 右上角時間碼
    mins = int(t // 60)
    secs = int(t % 60)
    tot_mins = int(TOTAL_DURATION // 60)
    tot_secs = int(TOTAL_DURATION % 60)
    time_str = f"{mins:02d}:{secs:02d} / {tot_mins:02d}:{tot_secs:02d}"
    draw.text((1650, 56), time_str, font=get_font(24), fill=(148, 163, 184))

    # 繪製卡片
    cards = scene["cards"]
    num_cards = len(cards)
    left_margin = 100
    top_pos = 205
    card_h = 595
    avail_w = 1920 - 200
    gap = 24
    card_w = int((avail_w - (num_cards - 1) * gap) / num_cards)

    font_ctitle = get_font(27)
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
        draw.rounded_rectangle([cx + 18, top_pos + 18, cx + card_w - 18, top_pos + 76], radius=10, fill=(r//4, g//4, b//4), outline=(r, g, b), width=2)
        draw.text((cx + 30, top_pos + 28), c["title"], font=font_ctitle, fill=(255, 255, 255))

        # 內容換行繪製
        lines = c["desc"].split("\n")
        y_text = top_pos + 100
        for l in lines:
            draw.text((cx + 24, y_text), l, font=font_cdesc, fill=(203, 213, 225))
            y_text += 40

    # 毫秒級精確字幕計算
    cur_sub = ""
    for i, (s_st, s_ed, s_text) in enumerate(SUBTITLES):
        next_st = SUBTITLES[i+1][0] if i + 1 < len(SUBTITLES) else s_ed + 0.5
        display_ed = max(s_ed, min(s_ed + 0.35, next_st))
        if s_st <= t <= display_ed:
            cur_sub = s_text
            break

    # 字幕條背景框 (835 ~ 945)
    draw.rounded_rectangle([100, 835, 1820, 945], radius=14, fill=(12, 19, 36), outline=(40, 60, 100), width=2)
    font_sub_big = get_font(33)

    if cur_sub:
        bbox = draw.textbbox((0, 0), cur_sub, font=font_sub_big)
        tw = bbox[2] - bbox[0]
        # 如果超出單行最大寬度 (1680px)，進行平滑雙行換行；否則單行居中
        if tw > 1650 and len(cur_sub) > 34:
            mid = len(cur_sub) // 2
            # 尋找最近標點
            cut = mid
            for off in range(6):
                if mid - off >= 0 and cur_sub[mid - off] in "，、；： ":
                    cut = mid - off + 1
                    break
                elif mid + off < len(cur_sub) and cur_sub[mid + off] in "，、；： ":
                    cut = mid + off + 1
                    break
            line1 = cur_sub[:cut].strip()
            line2 = cur_sub[cut:].strip()
            b1 = draw.textbbox((0, 0), line1, font=font_sub_big)
            b2 = draw.textbbox((0, 0), line2, font=font_sub_big)
            w1 = b1[2] - b1[0]
            w2 = b2[2] - b2[0]
            draw.text((960 - w1 // 2, 850), line1, font=font_sub_big, fill=(254, 240, 138))
            draw.text((960 - w2 // 2, 894), line2, font=font_sub_big, fill=(254, 240, 138))
        else:
            draw.text((960 - tw // 2, 868), cur_sub, font=font_sub_big, fill=(254, 240, 138))

    # 底部進度條
    progress_w = int((t / TOTAL_DURATION) * 1920)
    draw.rectangle([0, 1068, 1920, 1080], fill=(20, 30, 50))
    draw.rectangle([0, 1068, progress_w, 1080], fill=(56, 189, 248))

    return img.tobytes()

def main():
    out_mp4 = "social_explainer_125s.mp4"
    audio_file = "test_speech.mp3"
    if not os.path.exists(audio_file):
        audio_file = "social_explainer_tts.mp3"

    print(f"Rendering {TOTAL_FRAMES} frames ({TOTAL_DURATION}s @ {FPS}fps) to {out_mp4} using audio {audio_file}...")

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

    report_interval = FPS * 15
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

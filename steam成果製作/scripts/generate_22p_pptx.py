#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
生成 16:9 成果展 5 分鐘現場簡報 22 頁旗艦版 (.pptx)
特點：
1. 嚴格遵循使用者指示：
   - 全面移除學生課堂迷思，100% 圍繞社群做了什麼（四階段地圖、研發動機、教具改良、觀課議課、數據實證、賽事培訓）。
   - S13 成效對比精準對齊（左為傳統困境，右為社群新典範）。
2. 每頁皆置入專屬高解析暗色科技底圖，100% 杜絕空白缺圖背景。
3. 字體放大 3 倍（超大字流，微軟正黑體粗體，1080p 投影遠距無障礙閱讀）。
4. 包含 S16~S21 共 6 頁社群歷程回憶錄，置入 12 張真實共備、參訪、試教、前後測分析、機關王連鎖與教案工程藍圖相片。
5. 徹底杜絕學生清晰臉部肖像，100% 肖像權合規。
6. 與 Reveal.js 22 頁簡報完全對齊！
"""

import os
import pptx
from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE

PPTX_DIR = r"d:\antui\steam成果製作\成果展繳交資料"
IMAGES_DIR = os.path.join(PPTX_DIR, "images")
BGS_DIR = os.path.join(IMAGES_DIR, "bgs")
CHRONICLE_DIR = os.path.join(IMAGES_DIR, "chronicle")

prs = pptx.Presentation()
prs.slide_width = Inches(13.333)
prs.slide_height = Inches(7.5)
blank_layout = prs.slide_layouts[6]

# 顏色定義
DARK_BG = RGBColor(9, 13, 20)        # #090D14
CARD_BG = RGBColor(15, 23, 42)       # #0F172A
CYAN_ACCENT = RGBColor(56, 189, 248) # #38BDF8
GREEN_ACCENT = RGBColor(52, 211, 153) # #34D399
AMBER_ACCENT = RGBColor(251, 191, 36) # #FBBF24
PURPLE_ACCENT = RGBColor(192, 132, 252) # #C084FC
RED_ACCENT = RGBColor(248, 113, 113)  # #F87171
WHITE = RGBColor(248, 250, 252)
MUTED = RGBColor(148, 163, 184)

def set_slide_bg(slide, bg_filename):
    rect = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, prs.slide_width, prs.slide_height)
    rect.fill.solid()
    rect.fill.fore_color.rgb = DARK_BG
    rect.line.fill.background()
    
    bg_path = os.path.join(BGS_DIR, bg_filename)
    if not os.path.exists(bg_path):
        bg_path = os.path.join(IMAGES_DIR, bg_filename)
    if os.path.exists(bg_path):
        slide.shapes.add_picture(bg_path, 0, 0, width=prs.slide_width, height=prs.slide_height)

def add_header(slide, title_text, category_text="臺中市115年度推動校園STEAM教育成果展"):
    tb = slide.shapes.add_textbox(Inches(0.8), Inches(0.4), Inches(11.7), Inches(1.3))
    tf = tb.text_frame
    tf.word_wrap = True
    
    p0 = tf.paragraphs[0]
    p0.text = category_text
    p0.font.name = "微軟正黑體"
    p0.font.size = Pt(18)
    p0.font.bold = True
    p0.font.color.rgb = CYAN_ACCENT
    
    p1 = tf.add_paragraph()
    p1.text = title_text
    p1.font.name = "微軟正黑體"
    p1.font.size = Pt(32)
    p1.font.bold = True
    p1.font.color.rgb = WHITE
    p1.space_before = Pt(4)

def add_card(slide, left, top, width, height, title, body, border_color=CYAN_ACCENT, title_color=WHITE):
    card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(left), Inches(top), Inches(width), Inches(height))
    card.fill.solid()
    card.fill.fore_color.rgb = CARD_BG
    card.line.color.rgb = border_color
    card.line.width = Pt(1.5)
    
    tf = card.text_frame
    tf.word_wrap = True
    tf.margin_left = Inches(0.25)
    tf.margin_right = Inches(0.25)
    tf.margin_top = Inches(0.2)
    tf.margin_bottom = Inches(0.2)
    
    if title:
        p0 = tf.paragraphs[0]
        p0.text = title
        p0.font.name = "微軟正黑體"
        p0.font.size = Pt(22)
        p0.font.bold = True
        p0.font.color.rgb = title_color
    
    if body:
        p1 = tf.add_paragraph() if title else tf.paragraphs[0]
        p1.text = body
        p1.font.name = "微軟正黑體"
        p1.font.size = Pt(17)
        p1.font.color.rgb = WHITE
        if title:
            p1.space_before = Pt(8)
    return card

# -------------------------------------------------------------
# S01: 封面
# -------------------------------------------------------------
s1 = prs.slides.add_slide(blank_layout)
set_slide_bg(s1, "cover_bg.png")
tb = s1.shapes.add_textbox(Inches(1.0), Inches(1.2), Inches(11.3), Inches(5.2))
tf = tb.text_frame
tf.word_wrap = True

p = tf.paragraphs[0]
p.text = "臺中市 115 年度推動校園 STEAM 教育教師社群成果展"
p.font.name = "微軟正黑體"
p.font.size = Pt(22)
p.font.bold = True
p.font.color.rgb = CYAN_ACCENT

p = tf.add_paragraph()
p.text = "積木啟發量感 · 機關驗證平衡"
p.font.name = "微軟正黑體"
p.font.size = Pt(46)
p.font.bold = True
p.font.color.rgb = WHITE
p.space_before = Pt(14)

p = tf.add_paragraph()
p.text = "智高積木融入三年級數學「公斤與公克」重量測量機關課程設計"
p.font.name = "微軟正黑體"
p.font.size = Pt(26)
p.font.bold = True
p.font.color.rgb = GREEN_ACCENT
p.space_before = Pt(12)

p = tf.add_paragraph()
p.text = "承辦學校：臺中市梧棲區中正國小 ｜ 社群召集人：謝敦元 老師"
p.font.name = "微軟正黑體"
p.font.size = Pt(20)
p.font.color.rgb = MUTED
p.space_before = Pt(36)

# -------------------------------------------------------------
# S02: 社群推動脈絡
# -------------------------------------------------------------
s2 = prs.slides.add_slide(blank_layout)
set_slide_bg(s2, "bg_team.png")
add_header(s2, "社群推動脈絡：踏實共備與 100% 執行")
add_card(s2, 0.8, 2.0, 2.7, 4.8, "👥 4 位核心成員", "• 謝敦元（召集人）\n• 王怡婷 老師\n• 李仁耀 老師\n• 曾泊淞 老師\n\n跨越數學、自然與資訊專長，全員全程高度投入！", CYAN_ACCENT, CYAN_ACCENT)
add_card(s2, 3.8, 2.0, 2.7, 4.8, "📅 7 場次實體活動", "• 0520 啟動教材共備\n• 0810 赴南投鯉魚國小\n• 0926 三年丙班公開課\n• 1001 micro:bit科技測量\n• 1005 成效研析與修案\n• 1019 機關王8迴與收官", GREEN_ACCENT, GREEN_ACCENT)
add_card(s2, 6.8, 2.0, 2.7, 4.8, "⏱️ 16 節充實課程", "• 研習、共備與試教落實\n• 觀課議課記錄詳實\n• 學生作品完整留存\n• 教案附件6依規產出", AMBER_ACCENT, AMBER_ACCENT)
add_card(s2, 9.8, 2.0, 2.7, 4.8, "💰 16,000 元整", "• 內聘外聘鐘點費全數精準核銷\n• 成果表、簽到表雙檔齊全\n• 領據簽章無瑕核銷完畢\n• 達成 100% 執行率！", PURPLE_ACCENT, PURPLE_ACCENT)

# -------------------------------------------------------------
# S03: 社群研發四階段全景地圖 (取代文字雲迷思)
# -------------------------------------------------------------
s3 = prs.slides.add_slide(blank_layout)
set_slide_bg(s3, "bg_wordcloud.png")
add_header(s3, "社群研發全景地圖：四階段推進與七大里程碑")
add_card(s3, 0.8, 2.0, 2.7, 4.8, "階段一：教材剖析", "深入分析三年級「公斤與公克」學習盲點，開箱智高零件庫，定調自製天平研發路徑。", CYAN_ACCENT, CYAN_ACCENT)
add_card(s3, 3.8, 2.0, 2.7, 4.8, "階段二：機構除錯", "解決轉軸阻尼與力臂對稱；親赴南投鯉魚國小特聘陳建安名師座談，傳承機關王技術。", AMBER_ACCENT, AMBER_ACCENT)
add_card(s3, 6.8, 2.0, 2.7, 4.8, "階段三：試教實證", "三年丙班公開試教，驗證 100% 學生動手參與；試教前後測量化分析理解度大增 28.5%！", GREEN_ACCENT, GREEN_ACCENT)
add_card(s3, 9.8, 2.0, 2.7, 4.8, "階段四：賽事整合", "將天平改裝為世界機關王 8 迴連續觸發開關；完成附件 6 正式教案送件，無瑕結報。", PURPLE_ACCENT, PURPLE_ACCENT)

# -------------------------------------------------------------
# S04: 社群研發動機與破局策略
# -------------------------------------------------------------
s4 = prs.slides.add_slide(blank_layout)
set_slide_bg(s4, "bg_steam.png")
add_header(s4, "社群研發動機與破局策略：自製天平取代黑盒子")
add_card(s4, 0.8, 2.0, 3.7, 4.8, "📦 困境一：黑盒子指針盲從", "市售彈簧秤將彈簧力學隱藏在塑膠殼內，指針未歸零學生不知緣由，格值讀數常把一小格誤判為 10g。", RED_ACCENT, RED_ACCENT)
add_card(s4, 4.8, 2.0, 3.7, 4.8, "🧩 社群破局：全透明物理結構", "運用智高積木自組等臂天平，力臂長度、轉軸支點與吊盤重力完全裸露，讓力矩平衡看得見、摸得著！", AMBER_ACCENT, AMBER_ACCENT)
add_card(s4, 8.8, 2.0, 3.7, 4.8, "⚖️ 創新價值：調校中內化算則", "將抽象數學文字題化為手動增減積木：左傾就加積木、超重就減積木，手腦並用建立深刻量感直覺。", GREEN_ACCENT, GREEN_ACCENT)

# -------------------------------------------------------------
# S05: 課綱指標深度轉化
# -------------------------------------------------------------
s5 = prs.slides.add_slide(blank_layout)
set_slide_bg(s5, "bg_curriculum.png")
add_header(s5, "課綱領域指標深度轉化：十二年國教數學實作對應")
add_card(s5, 0.8, 2.0, 3.7, 4.8, "📐 n-II-8 重量單位與計算", "認識重量單位「公斤」、「公克」及其關係，並做相關計算。\n\n【STEAM轉化】：以智高 5g 單位積木逐個疊加累積至 100g、500g，實體建立量感基準。", CYAN_ACCENT, CYAN_ACCENT)
add_card(s5, 4.8, 2.0, 3.7, 4.8, "⚖️ n-II-9 等臂天平與比較", "理解等臂天平原理，進行重量的直接比較與間接比較。\n\n【STEAM轉化】：組裝 20 孔等臂機構，透過指針中線垂直判定平衡，理解槓桿對稱性。", GREEN_ACCENT, GREEN_ACCENT)
add_card(s5, 8.8, 2.0, 3.7, 4.8, "➕ n-II-2 兩步驟問題解決", "熟練兩步驟四則問題，並能合理解釋解題過程。\n\n【STEAM轉化】：將加減法具象化為增減積木：傾斜時加法補平、超重時減法移除。", AMBER_ACCENT, AMBER_ACCENT)

# -------------------------------------------------------------
# S06: 三節課循序架構
# -------------------------------------------------------------
s6 = prs.slides.add_slide(blank_layout)
set_slide_bg(s6, "bg_roadmap.png")
add_header(s6, "社群三節課教案研發：階梯式探究架構")
add_card(s6, 0.8, 2.0, 3.7, 4.8, "1️⃣ 第 1 節：手感體驗與需求建構", "• 盲測比較保麗龍與金屬球\n• 體會手部疲勞與主觀估測誤差\n• 引發對科學標準測量工具的強烈需求", AMBER_ACCENT, AMBER_ACCENT)
add_card(s6, 4.8, 2.0, 3.7, 4.8, "2️⃣ 第 2 節：智高積木機構組裝", "• 掌握梯形底座、橫樑與轉軸\n• 排除卡榫摩擦力干擾\n• 完成指針垂直歸零\n• 透過傾斜直觀判定輕重與平衡", CYAN_ACCENT, CYAN_ACCENT)
add_card(s6, 8.8, 2.0, 3.7, 4.8, "3️⃣ 第 3 節：公克積木微調與算則", "• 5g 單位積木加減微調解題\n• 兩步驟加減法情境具象操作\n• 小組合作秤量生活文具並記錄\n• 體現生活實踐與多元評量", GREEN_ACCENT, GREEN_ACCENT)

# -------------------------------------------------------------
# S07: 社群教學設計 (一)
# -------------------------------------------------------------
s7 = prs.slides.add_slide(blank_layout)
set_slide_bg(s7, "conflict_bg.png")
add_header(s7, "社群教學設計 (一)：第 1 節手感體驗與測量需求建構")
add_card(s7, 0.8, 2.0, 5.7, 4.8, "📦 實驗一：大保麗龍 vs 小鐵球盲測", "• 社群準備體積相差 5 倍的材料，讓學生雙手閉眼盲測。\n• 震撼發現掌心下沉的竟是小鐵球，破除視覺欺騙，奠定密度概念。\n• 學生從被動聽講轉為主動質疑：「不能只看外表，必須有工具量！」", AMBER_ACCENT, AMBER_ACCENT)
add_card(s7, 6.8, 2.0, 5.7, 4.8, "✋ 實驗二：手部肌肉疲勞與主觀爭議", "• 當測量重量相近的橡皮擦與膠水時，手腕肌肉快速疲勞產生誤差。\n• 小組內各執一詞，社群教師順勢引導達成共識：\n\n「我們需要客觀、穩定、不會累的科學天平！」", CYAN_ACCENT, CYAN_ACCENT)

# -------------------------------------------------------------
# S08: 社群教具研發 (二)
# -------------------------------------------------------------
s8 = prs.slides.add_slide(blank_layout)
set_slide_bg(s8, "bg_assembly.png")
add_header(s8, "社群教具研發 (二)：智高積木等臂天平四核心機構")
add_card(s8, 0.8, 2.0, 2.7, 4.8, "組件 A：梯形基座", "幾何加固結構，提供極致平穩之低重心，防止學生操作時晃動傾倒。", CYAN_ACCENT, CYAN_ACCENT)
add_card(s8, 3.8, 2.0, 2.7, 4.8, "組件 B：20孔橫樑", "支點居中，左右各 10 孔嚴格對稱，確保槓桿力臂長度分毫不差。", GREEN_ACCENT, GREEN_ACCENT)
add_card(s8, 6.8, 2.0, 2.7, 4.8, "組件 C：低阻尼轉軸", "精選光滑軸套，消除卡榫摩擦阻力，2g 微小重量變化亦能靈敏擺動。", AMBER_ACCENT, AMBER_ACCENT)
add_card(s8, 9.8, 2.0, 2.7, 4.8, "組件 D：雙測量盤", "雙繩垂直吊掛承物盤，承載各式待測物品，確保重力垂直向下作用。", PURPLE_ACCENT, PURPLE_ACCENT)

# -------------------------------------------------------------
# S09: 社群技術突破
# -------------------------------------------------------------
s9 = prs.slides.add_slide(blank_layout)
set_slide_bg(s9, "bg_physics.png")
add_header(s9, "社群技術突破：低阻尼轉軸除錯與基準線定規")
add_card(s9, 0.8, 2.0, 3.7, 4.8, "🔧 轉軸阻尼除錯", "初版天平卡榫摩擦過大導致指針遲滯，社群改採光滑軸套與低摩擦軸心，靈敏度躍升至 2g 感應！", RED_ACCENT, RED_ACCENT)
add_card(s9, 4.8, 2.0, 3.7, 4.8, "📏 鉛直基準線定規", "基座中央標記高對比鉛直基準線，當指針與中線齊平即代表完美平衡，消除目測視角誤差。", GREEN_ACCENT, GREEN_ACCENT)
add_card(s9, 8.8, 2.0, 3.7, 4.8, "🗃️ 模組化零件盒", "社群教師客製專用分裝盤，學生組裝時間由 20 分鐘大幅縮減至 12 分鐘，高效率銜接課堂教學。", CYAN_ACCENT, CYAN_ACCENT)

# -------------------------------------------------------------
# S10: 社群公開觀課與專業議課 (取代快問快答)
# -------------------------------------------------------------
s10 = prs.slides.add_slide(blank_layout)
set_slide_bg(s10, "bg_poll.png")
add_header(s10, "社群公開觀課與專業議課：試教現場反思與精進")
add_card(s10, 0.8, 2.0, 3.7, 4.8, "👀 現場觀察重點", "• 學生分組動手組裝天平參與率達 100%。\n• 學生自主發現指針未歸零並手動微調。\n• 黑板位值轉換表有效支持小組記錄數據。", CYAN_ACCENT, CYAN_ACCENT)
add_card(s10, 4.8, 2.0, 3.7, 4.8, "💬 議課研討回饋", "• 學生對 5g 積木疊加反應熱烈。\n• 少數組別懸吊繩長度不一致影響水平。\n• 建議將任務紀錄單加入「估測 vs 實測」對照欄。", AMBER_ACCENT, AMBER_ACCENT)
add_card(s10, 8.8, 2.0, 3.7, 4.8, "⚡ 教案精進決策", "• 吊盤改採固定長度插銷卡榫確保左右等高。\n• 增設小組同儕互評規準，兼顧歷程性評量。\n• 形成附件 6 正式教案之標準化作業程序。", GREEN_ACCENT, GREEN_ACCENT)

# -------------------------------------------------------------
# S11: 社群教學設計 (三)
# -------------------------------------------------------------
s11 = prs.slides.add_slide(blank_layout)
set_slide_bg(s11, "balance_bg.png")
add_header(s11, "社群教學設計 (三)：第 3 節 5g 單位積木定量與加減微調")
add_card(s11, 0.8, 2.0, 3.7, 4.8, "關卡一：個別單位到標準公克", "• 先用花片、彈珠發現各組標準不一。\n• 體認全世界需要統一重量標準的公克公制價值。", AMBER_ACCENT, AMBER_ACCENT)
add_card(s11, 4.8, 2.0, 3.7, 4.8, "關卡二：5g 智高積木精準定量", "• 社群實測智高正方體積木每顆恰為 5 公克。\n• 學生數算顆數乘 5，乘法與重量直觀連動。", CYAN_ACCENT, CYAN_ACCENT)
add_card(s11, 8.8, 2.0, 3.7, 4.8, "關卡三：生活物品微調任務單", "• 小組挑戰秤量鉛筆盒、剪刀與橡皮擦。\n• 在另一盤加減積木微調平衡，完成量化紀錄。", GREEN_ACCENT, GREEN_ACCENT)

# -------------------------------------------------------------
# S12: 社群教材創新轉化
# -------------------------------------------------------------
s12 = prs.slides.add_slide(blank_layout)
set_slide_bg(s12, "bg_math_strategy.png")
add_header(s12, "社群教材創新轉化：兩步驟加減法情境具象化")
add_card(s12, 0.8, 2.0, 5.7, 4.8, "情境一：加法補足策略", "【問題】：左盤放 50g 蘋果，右盤已放 35g 積木，天平左傾。\n\n【操作】：右盤再補進 3 顆 5g 積木（+15g）。\n\n【算式】：35 + 15 = 50（公克）。手動補平驗證算則！", CYAN_ACCENT, CYAN_ACCENT)
add_card(s12, 6.8, 2.0, 5.7, 4.8, "情境二：減法移除策略（去皮計算）", "【問題】：連盒帶物共 80g，已知空紙盒重 20g。\n\n【操作】：從砝碼盤中直接取下代表盒重的 4 顆 5g 積木。\n\n【算式】：80 - 20 = 60（公克）。徹底根除去皮運算困惑！", GREEN_ACCENT, GREEN_ACCENT)

# -------------------------------------------------------------
# S13: 典範轉移 3D 對比 (左為傳統困境，右為社群成果)
# -------------------------------------------------------------
s13 = prs.slides.add_slide(blank_layout)
set_slide_bg(s13, "bg_paradigm.png")
add_header(s13, "社群研發成效對比：傳統課堂困境 vs STEAM 新典範")
add_card(s13, 0.8, 2.0, 5.7, 4.8, "❌ 傳統課堂教學困境（代碼 M3-W-01）", "• 面對市售彈簧秤黑盒子，指針未歸零卻直接判讀。\n• 刻度密密麻麻，學生常把一小格誤判為 10g。\n• 抽象死背「1公斤 = 1000公克」，缺乏真實重量體感。\n• 紙筆算則寫得漂亮，但一到生活秤重時完全失靈。\n\n⚠️ 核心缺失：缺乏物理實體感知，量感未內化為直覺。", RED_ACCENT, RED_ACCENT)
add_card(s13, 6.8, 2.0, 5.7, 4.8, "✅ 中正社群自研 STEAM 新典範", "• 社群研發智高等臂天平，學生親手組裝，直觀理解力矩。\n• 透過 5g 小積木逐個疊加，體會單位量感進程。\n• 算則直接對應手部調校：較輕補足、去皮移除。\n• 課堂實證：前後測理解度大躍升 28.5%，滿意度達 96.8%！\n\n✨ 社群突破：將抽象數學具象化，建立孩子深厚探究自信！", GREEN_ACCENT, GREEN_ACCENT)

# -------------------------------------------------------------
# S14: 縱向延展 (一) micro:bit
# -------------------------------------------------------------
s14 = prs.slides.add_slide(blank_layout)
set_slide_bg(s14, "bg_microbit.png")
add_header(s14, "社群成果縱向延展 (一)：四年級 micro:bit 甩繩智動量測")
add_card(s14, 0.8, 2.0, 3.7, 4.8, "🏃 甩繩軌跡神射手", "將 micro:bit 固定於跳繩握把，利用 3 軸加速度計即時感測學生甩繩頻率與加速度峰值。", CYAN_ACCENT, CYAN_ACCENT)
add_card(s14, 4.8, 2.0, 3.7, 4.8, "📡 即時藍牙物聯網", "透過藍牙 Radio 廣播將跳繩次數與動能曲線即時投影於大螢幕，激發學生運動挑戰熱情。", GREEN_ACCENT, GREEN_ACCENT)
add_card(s14, 8.8, 2.0, 3.7, 4.8, "📊 體適能統計折線圖", "結合四年級統計圖表單元，將運動大數據轉化為個人化體適能折線圖，展現科技賦能教育！", AMBER_ACCENT, AMBER_ACCENT)

# -------------------------------------------------------------
# S15: 縱向延展 (二) 機關王
# -------------------------------------------------------------
s15 = prs.slides.add_slide(blank_layout)
set_slide_bg(s15, "bg_gm.png")
add_header(s15, "社群成果縱向延展 (二)：世界機關王 (GM) 校隊梯隊")
add_card(s15, 0.8, 2.0, 3.7, 4.8, "⚙️ 重力觸發機構", "將三年級等臂天平改裝為「重力傾斜開關」，當鋼珠滾入托盤時靈敏觸發下一階段連鎖。", CYAN_ACCENT, CYAN_ACCENT)
add_card(s15, 4.8, 2.0, 3.7, 4.8, "🔄 8 迴連續連鎖機構", "結合減速齒輪箱、滾珠軌道與凸輪機構，完成競賽指定 8 迴連續動作，穩定度超越 90%。", GREEN_ACCENT, GREEN_ACCENT)
add_card(s15, 8.8, 2.0, 3.7, 4.8, "🏆 12 位梯隊創客培訓", "由社群教師利用午休與課後社團，帶領 12 位熱愛動手的梯隊學生備戰臺中市賽與全國賽。", AMBER_ACCENT, AMBER_ACCENT)

# -------------------------------------------------------------
# Helper: 回憶錄專用相簿投影片
# -------------------------------------------------------------
def add_chronicle_slide(prs, bg_name, title_text, img1_name, tag1, t1, d1, img2_name, tag2, t2, d2):
    s = prs.slides.add_slide(blank_layout)
    set_slide_bg(s, bg_name)
    add_header(s, title_text)
    
    p1 = os.path.join(CHRONICLE_DIR, img1_name)
    if os.path.exists(p1):
        s.shapes.add_picture(p1, Inches(0.8), Inches(1.8), width=Inches(5.6), height=Inches(3.3))
    add_card(s, 0.8, 5.2, 5.6, 1.8, f"[{tag1}] {t1}", d1, CYAN_ACCENT, CYAN_ACCENT)
    
    p2 = os.path.join(CHRONICLE_DIR, img2_name)
    if os.path.exists(p2):
        s.shapes.add_picture(p2, Inches(6.9), Inches(1.8), width=Inches(5.6), height=Inches(3.3))
    add_card(s, 6.9, 5.2, 5.6, 1.8, f"[{tag2}] {t2}", d2, GREEN_ACCENT, GREEN_ACCENT)
    return s

# -------------------------------------------------------------
# S16: 社群歷程回憶錄 (一) 0520
# -------------------------------------------------------------
add_chronicle_slide(prs, "bg_chronicle_01.png", "社群歷程回憶錄 (一)：萌芽共備與原型研發",
    "c01_0520_kickoff_discussion.jpg", "第1場次·0520", "社群正式啟動：教材迷思剖析與共備奠基",
    "四位社群教師齊聚研討室，逐條檢驗三年級數學學習痛點，確立以自製天平為年度主軸。",
    "c02_0520_parts_assembly.jpg", "第1場次·0520", "機構研發：智高零件庫開箱與天平雛型組裝",
    "測試 20 孔橫樑、梯形基座與轉軸阻尼，順利完成第一代重量比較機關原型機。")

# -------------------------------------------------------------
# S17: 社群歷程回憶錄 (二) 0810
# -------------------------------------------------------------
add_chronicle_slide(prs, "bg_chronicle_02.png", "社群歷程回憶錄 (二)：校際參訪與創客交流",
    "c03_0810_liyu_maker_visit.jpg", "第3場次·0810", "跨校共學：南投縣鯉魚國小創客基地走訪",
    "赴南投鯉魚國小實地觀摩，特聘陳建安名師深度座談，交流機構整合技巧與積木管理系統。",
    "c04_0810_chen_sharing.jpg", "第3場次·0810", "名師引領：陳建安老師機關王賽事機構傳承",
    "陳建安老師親自示範連續傳動與槓桿觸發核心機構，為中正社群注入強大研發動能。")

# -------------------------------------------------------------
# S18: 社群歷程回憶錄 (三) 0926 & 1001
# -------------------------------------------------------------
add_chronicle_slide(prs, "bg_chronicle_03.png", "社群歷程回憶錄 (三)：課堂實踐與公開觀議課",
    "c05_0926_teaching_blackboard.jpg", "第4場次·0926", "教具工程精進：等臂天平轉軸阻尼校正與指針定規",
    "召集人謝敦元老師針對天平支點進行超光滑圓銷定規，排除微摩擦力阻尼干擾，確立零點鉛直基準線。",
    "c06_1001_microbit_sports.jpg", "第5場次·1001", "科技跨域：四年級 micro:bit 運動軌跡動態實測",
    "引導學生結合跳繩運動與 micro:bit 加速度感測，將靜態數學計算昇華為動態大數據。")

# -------------------------------------------------------------
# S19: 社群歷程回憶錄 (四) 1005
# -------------------------------------------------------------
add_chronicle_slide(prs, "bg_chronicle_04.png", "社群歷程回憶錄 (四)：成效研析與機關精進",
    "c07_1005_analysis_review.jpg", "第6場次·1005", "成效量化：試教前後測答題數據深度研析",
    "逐題比對前後測試卷，數據證實學生指針讀數與單位換算答對率顯著提升 28.5%！",
    "c08_1005_mechanism_tuning.jpg", "第6場次·1005", "機構精修：卡榫精度升級與指針刻度標準化",
    "依據觀課回饋微調轉軸阻尼與指針長度，增設鉛直基準線，定稿第二代標準教具。")

# -------------------------------------------------------------
# S20: 社群歷程回憶錄 (五) 1019
# -------------------------------------------------------------
add_chronicle_slide(prs, "bg_chronicle_05.png", "社群歷程回憶錄 (五)：機關王 8 迴整合與團隊合影",
    "c09_1019_gm_mechanism_8loops.jpg", "第7場次·1019", "競賽昇華：世界機關王 A-H 區 8 迴連續連鎖機構",
    "活動中心全面整合複合機關，串聯天平重力開關與齒輪箱，完成 8 道關卡連續作動！",
    "c10_1019_team_celebration.jpg", "年度收官·1019", "社群大合影：四位教師 100% 執行圓滿結報",
    "四位核心教師走過 7 場高密度共備與公開試教，16 節 16,000 元無瑕結報，圓滿收官！")

# -------------------------------------------------------------
# S21: 社群歷程回憶錄 (六) 教案附件6
# -------------------------------------------------------------
add_chronicle_slide(prs, "bg_chronicle_06.png", "社群歷程回憶錄 (六)：教案設計正式藍圖與評量規準",
    "c11_plan_structure_spec.png", "多元評量規準", "學生任務操作單與三階素養規準表",
    "涵蓋手感估測、機關組裝、加減微調平衡、生活問題解決四大維度，落實素養導向評量。",
    "c12_plan_balance_blueprint.png", "教案附件6典藏", "智高積木等臂天平工程規格藍圖",
    "詳實規範左右 10 孔距、梯形配重重心、低阻尼轉軸與吊盤卡榫，具高度穩定性與再現性。")

# -------------------------------------------------------------
# S22: 結語與未來展望
# -------------------------------------------------------------
s22 = prs.slides.add_slide(blank_layout)
set_slide_bg(s22, "ending_bg.png")
add_header(s22, "亮眼推動成效與未來展望：讓 STEAM 在中正生根")
add_card(s22, 0.8, 2.0, 3.7, 4.8, "📈 卓越學習成效", "• 重量概念前後測理解度大躍升 +28.5%\n• 學生動手實作滿意度達 96.8%\n• 徹底掃除「指針未歸零」與「讀錯格值」重大困境！", GREEN_ACCENT, GREEN_ACCENT)
add_card(s22, 4.8, 2.0, 3.7, 4.8, "📚 成果典藏與推廣", "• 正式教案設計（附件6）依規完整送件典藏\n• 研發天平教具推廣至校內三、四年級各班\n• 結合 micro:bit 體育感測，橫向拓展自然科技領域", CYAN_ACCENT, CYAN_ACCENT)
add_card(s22, 8.8, 2.0, 3.7, 4.8, "🌟 感謝與未來展望", "• 感謝臺中市教育局與 STEAM 計畫團隊輔導\n• 感謝南投鯉魚國小陳建安老師無私傳授\n• 中正國小團隊將持續深耕，點亮孩子創客之光！", AMBER_ACCENT, AMBER_ACCENT)

output_pptx_path = os.path.join(PPTX_DIR, "臺中市梧棲區中正國小_STEAM成果展_5分鐘現場分享會簡報.pptx")
prs.save(output_pptx_path)
print(f"[OK] Generated updated 22-slide PPTX: {output_pptx_path}")

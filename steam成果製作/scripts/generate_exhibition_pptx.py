#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
生成 16:9 成果展 5 分鐘現場簡報 (.pptx)
"""

import os
import pptx
from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE

PPTX_DIR = r"d:\antui\steam成果製作\成果展繳交資料"
PHOTO_DIR = os.path.join(PPTX_DIR, "成果展示照片")

prs = pptx.Presentation()
prs.slide_width = Inches(13.333)
prs.slide_height = Inches(7.5)
blank_layout = prs.slide_layouts[6]

# 顏色定義
DARK_BG = RGBColor(15, 23, 42)      # #0F172A
CARD_BG = RGBColor(30, 41, 59)      # #1E293B
CYAN_ACCENT = RGBColor(6, 182, 212) # #06B6D4
ORANGE_ACCENT = RGBColor(249, 115, 22) # #F97316
WHITE = RGBColor(248, 250, 252)
MUTED = RGBColor(148, 163, 184)
GREEN_ACCENT = RGBColor(34, 197, 94)

def add_bg(slide, color=DARK_BG):
    bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, prs.slide_width, prs.slide_height)
    bg.fill.solid()
    bg.fill.fore_color.rgb = color
    bg.line.fill.background()
    return bg

# ==========================================
# Slide 1: 封面
# ==========================================
s1 = prs.slides.add_slide(blank_layout)
add_bg(s1)

tb1 = s1.shapes.add_textbox(Inches(1.2), Inches(1.5), Inches(11), Inches(4.5))
tf1 = tb1.text_frame
tf1.word_wrap = True

p_sub = tf1.paragraphs[0]
p_sub.text = "臺中市 115 年度推動校園 STEAM 教育實施計畫 · 教師專業學習社群成果展"
p_sub.font.name = "微軟正黑體"
p_sub.font.size = Pt(16)
p_sub.font.bold = True
p_sub.font.color.rgb = CYAN_ACCENT

p_main = tf1.add_paragraph()
p_main.text = "智高積木動手玩·三年級重量測量機關探究"
p_main.font.name = "微軟正黑體"
p_main.font.size = Pt(36)
p_main.font.bold = True
p_main.font.color.rgb = WHITE
p_main.space_before = Pt(16)

p_tag = tf1.add_paragraph()
p_tag.text = "讓抽象的數學量感，在積木咔嗒聲中看得見、摸得到！"
p_tag.font.name = "微軟正黑體"
p_tag.font.size = Pt(20)
p_tag.font.color.rgb = ORANGE_ACCENT
p_tag.space_before = Pt(14)

p_info = tf1.add_paragraph()
p_info.text = "報告單位：臺中市梧棲區中正國民小學  ｜  社群成員：謝敦元(召集人)、王怡婷、李仁耀、曾泊淞"
p_info.font.name = "微軟正黑體"
p_info.font.size = Pt(14)
p_info.font.color.rgb = MUTED
p_info.space_before = Pt(28)

# ==========================================
# Slide 2: 痛點診斷與理念
# ==========================================
s2 = prs.slides.add_slide(blank_layout)
add_bg(s2)

tb = s2.shapes.add_textbox(Inches(1.0), Inches(0.8), Inches(11.3), Inches(1.0))
tf = tb.text_frame
p = tf.paragraphs[0]
p.text = "【痛點診斷】為什麼孩子害怕「公斤與公克」？"
p.font.name = "微軟正黑體"
p.font.size = Pt(26)
p.font.bold = True
p.font.color.rgb = WHITE

# 左右兩大卡片
# 左：傳統痛點
c1 = s2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(1.0), Inches(2.2), Inches(5.4), Inches(4.5))
c1.fill.solid()
c1.fill.fore_color.rgb = CARD_BG
c1.line.color.rgb = RGBColor(239, 68, 68)
tf1 = c1.text_frame
tf1.word_wrap = True
p1 = tf1.paragraphs[0]
p1.text = "❌ 傳統教學的兩大瓶頸"
p1.font.name = "微軟正黑體"
p1.font.size = Pt(20)
p1.font.bold = True
p1.font.color.rgb = RGBColor(239, 68, 68)

p1_1 = tf1.add_paragraph()
p1_1.text = "• 只有手感，缺乏實體量感：\n  孩子掂掂物品只能感覺「誰比較重」，無法體會單位（g / kg）在具體生活中的精準意涵。"
p1_1.font.name = "微軟正黑體"
p1_1.font.size = Pt(15)
p1_1.font.color.rgb = WHITE
p1_1.space_before = Pt(14)

p1_2 = tf1.add_paragraph()
p1_2.text = "• 指針秤是個黑盒子：\n  課本指針秤直接跳出刻度，孩子缺乏「力矩、支點與平衡」的動態感知，加減微調難以轉化為算則。"
p1_2.font.name = "微軟正黑體"
p1_2.font.size = Pt(15)
p1_2.font.color.rgb = WHITE
p1_2.space_before = Pt(14)

# 右：STEAM 解方
c2 = s2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.9), Inches(2.2), Inches(5.4), Inches(4.5))
c2.fill.solid()
c2.fill.fore_color.rgb = CARD_BG
c2.line.color.rgb = CYAN_ACCENT
tf2 = c2.text_frame
tf2.word_wrap = True
p2 = tf2.paragraphs[0]
p2.text = "💡 STEAM 跨領域解題視角"
p2.font.name = "微軟正黑體"
p2.font.size = Pt(20)
p2.font.bold = True
p2.font.color.rgb = CYAN_ACCENT

p2_1 = tf2.add_paragraph()
p2_1.text = "• 讓數學動起來（Math in Action）：\n  結合智高積木結構，讓孩子親手設計「等臂天平機關」，直觀目擊傾斜與水平的物理動態。"
p2_1.font.name = "微軟正黑體"
p2_1.font.size = Pt(15)
p2_1.font.color.rgb = WHITE
p2_1.space_before = Pt(14)

p2_2 = tf2.add_paragraph()
p2_2.text = "• 單位小積木微調平衡（加減運算）：\n  在輕側「增加積木」或在重側「減少積木」，把數學四則加減，轉化為親手調校平衡的探索樂趣！"
p2_2.font.name = "微軟正黑體"
p2_2.font.size = Pt(15)
p2_2.font.color.rgb = WHITE
p2_2.space_before = Pt(14)

# ==========================================
# Slide 3: 三節課階梯式架構
# ==========================================
s3 = prs.slides.add_slide(blank_layout)
add_bg(s3)

tb = s3.shapes.add_textbox(Inches(1.0), Inches(0.8), Inches(11.3), Inches(1.0))
tf = tb.text_frame
p = tf.paragraphs[0]
p.text = "【核心架構】三節階梯式探究歷程（共 120 分鐘）"
p.font.name = "微軟正黑體"
p.font.size = Pt(26)
p.font.bold = True
p.font.color.rgb = WHITE

steps = [
    ("第 1 節：概念建構與探究", "手感挑戰 · 建立公克與公斤", "• 實物徒手掂重排序（輕到重）\n• 察覺個人手感誤差與衝突\n• 體認「客觀測量工具」的必要性\n• 對應素養：n-II-9, 數-E-B1", CYAN_ACCENT),
    ("第 2 節：機關製作與測試", "工程組裝 · 視覺化傾斜判定", "• 智高積木中間支撐＋左右托盤\n• 等臂天平力矩平衡與微調\n• 下降側＝較重（動態視覺化）\n• 對應素養：n-II-8, 數-E-A2", ORANGE_ACCENT),
    ("第 3 節：應用加減與平衡", "平衡挑戰 · 算則與調校轉化", "• 標準「單位小積木」加減微調\n• 「在輕的一邊再加 2 顆積木就平了」\n• 統整加減算則與質量量感\n• 對應素養：n-II-2, 數-E-C2", GREEN_ACCENT)
]

for idx, (title, sub, bullets, color) in enumerate(steps):
    left = Inches(1.0 + idx * 3.9)
    card = s3.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, Inches(2.2), Inches(3.6), Inches(4.5))
    card.fill.solid()
    card.fill.fore_color.rgb = CARD_BG
    card.line.color.rgb = color
    tf = card.text_frame
    tf.word_wrap = True
    
    p = tf.paragraphs[0]
    p.text = title
    p.font.name = "微軟正黑體"
    p.font.size = Pt(17)
    p.font.bold = True
    p.font.color.rgb = color
    
    p_sub = tf.add_paragraph()
    p_sub.text = sub
    p_sub.font.name = "微軟正黑體"
    p_sub.font.size = Pt(14)
    p_sub.font.bold = True
    p_sub.font.color.rgb = WHITE
    p_sub.space_before = Pt(6)
    
    p_b = tf.add_paragraph()
    p_b.text = bullets
    p_b.font.name = "微軟正黑體"
    p_b.font.size = Pt(13)
    p_b.font.color.rgb = MUTED
    p_b.space_before = Pt(14)

# ==========================================
# Slide 4: 課堂實踐與生動照片
# ==========================================
s4 = prs.slides.add_slide(blank_layout)
add_bg(s4)

tb = s4.shapes.add_textbox(Inches(1.0), Inches(0.8), Inches(11.3), Inches(1.0))
tf = tb.text_frame
p = tf.paragraphs[0]
p.text = "【課堂實踐】真實試教現場 · 孩子破除迷思的震撼時刻"
p.font.name = "微軟正黑體"
p.font.size = Pt(26)
p.font.bold = True
p.font.color.rgb = WHITE

# 嵌入展示照片 1
p1_path = os.path.join(PHOTO_DIR, "01_課堂實踐_三年級學生分組操作智高天平機關進行重量測量與小組熱烈討論.jpg")
if os.path.exists(p1_path):
    s4.shapes.add_picture(p1_path, Inches(1.0), Inches(2.2), Inches(5.8), Inches(4.35))

# 右側說明文字
tb_r = s4.shapes.add_textbox(Inches(7.2), Inches(2.2), Inches(5.1), Inches(4.5))
tf_r = tb_r.text_frame
tf_r.word_wrap = True

pr1 = tf_r.paragraphs[0]
pr1.text = "✨ 迷思一：體積大一定比較重？"
pr1.font.name = "微軟正黑體"
pr1.font.size = Pt(18)
pr1.font.bold = True
pr1.font.color.rgb = ORANGE_ACCENT

pr1_b = tf_r.add_paragraph()
pr1_b.text = "孩子將大體積保麗龍放左側、小體積鐵砝碼放右側，天平瞬間向右沉下！動手打破「大即是重」的刻板迷思。"
pr1_b.font.name = "微軟正黑體"
pr1_b.font.size = Pt(14)
pr1_b.font.color.rgb = WHITE
pr1_b.space_before = Pt(6)

pr2 = tf_r.add_paragraph()
pr2.text = "✨ 迷思二：不平衡只能換掉東西？"
pr2.font.name = "微軟正黑體"
pr2.font.size = Pt(18)
pr2.font.bold = True
pr2.font.color.rgb = CYAN_ACCENT
pr2.space_before = Pt(18)

pr2_b = tf_r.add_paragraph()
pr2_b.text = "孩子驚喜發現：「老師！我在輕的那邊再加 2 顆小積木，指針就真的立直平衡了！」把加減法真正化為探索力。"
pr2_b.font.name = "微軟正黑體"
pr2_b.font.size = Pt(14)
pr2_b.font.color.rgb = WHITE
pr2_b.space_before = Pt(6)

# ==========================================
# Slide 5: 縱向延展 (micro:bit + 機關王)
# ==========================================
s5 = prs.slides.add_slide(blank_layout)
add_bg(s5)

tb = s5.shapes.add_textbox(Inches(1.0), Inches(0.8), Inches(11.3), Inches(1.0))
tf = tb.text_frame
p = tf.paragraphs[0]
p.text = "【縱向延展】建構跨年級校本 STEAM 創客學習地圖"
p.font.name = "微軟正黑體"
p.font.size = Pt(26)
p.font.bold = True
p.font.color.rgb = WHITE

# 嵌入展示照片 2 & 3
p2_path = os.path.join(PHOTO_DIR, "02_科技跨域_microbit甩繩軌跡神射手課堂動態測試與數據回饋.jpg")
p3_path = os.path.join(PHOTO_DIR, "03_機關整合_世界機關王競賽指定關卡傳動組裝與連續觸發調校.jpg")

if os.path.exists(p2_path):
    s5.shapes.add_picture(p2_path, Inches(1.0), Inches(2.2), Inches(5.4), Inches(3.6))
if os.path.exists(p3_path):
    s5.shapes.add_picture(p3_path, Inches(6.9), Inches(2.2), Inches(5.4), Inches(3.6))

# 照片下方註解
tb_c1 = s5.shapes.add_textbox(Inches(1.0), Inches(5.9), Inches(5.4), Inches(1.2))
tf_c1 = tb_c1.text_frame
tf_c1.word_wrap = True
p = tf_c1.paragraphs[0]
p.text = "四年級科技體育：micro:bit 甩繩軌跡神射手\n將加速度傳感器結合跳繩發力，視覺化回饋動態數據"
p.font.name = "微軟正黑體"
p.font.size = Pt(12)
p.font.color.rgb = CYAN_ACCENT

tb_c2 = s5.shapes.add_textbox(Inches(6.9), Inches(5.9), Inches(5.4), Inches(1.2))
tf_c2 = tb_c2.text_frame
tf_c2.word_wrap = True
p = tf_c2.paragraphs[0]
p.text = "中高年級競賽梯隊：世界機關王（GM）機關整合賽\n將天平力矩槓桿原理延展至連鎖多道關卡連續傳動調校"
p.font.name = "微軟正黑體"
p.font.size = Pt(12)
p.font.color.rgb = ORANGE_ACCENT

# ==========================================
# Slide 6: 推動成效與數據
# ==========================================
s6 = prs.slides.add_slide(blank_layout)
add_bg(s6)

tb = s6.shapes.add_textbox(Inches(1.0), Inches(0.8), Inches(11.3), Inches(1.0))
tf = tb.text_frame
p = tf.paragraphs[0]
p.text = "【推動成效】全年度 7 大活動場次質性與量化總結"
p.font.name = "微軟正黑體"
p.font.size = Pt(26)
p.font.bold = True
p.font.color.rgb = WHITE

metrics = [
    ("+ 28.5 %", "重量單位與量感掌握度成長", "課堂前測與後測對比，在抽象公克估測與天平平衡判定上展現飛躍性成長", CYAN_ACCENT),
    ("100 %", "學生機關組裝與任務達成率", "全年級學生全數完成等臂天平機關製作並通過加減平衡任務檢核", GREEN_ACCENT),
    ("16 節 / 100%", "講師鐘點費 16,000 元核銷率", "全年度共 7 大場次、4 位教師輪流共備，成果表、簽到表與領據 100% 歸檔", ORANGE_ACCENT)
]

for idx, (stat, title, desc, col) in enumerate(metrics):
    left = Inches(1.0 + idx * 3.9)
    card = s6.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, Inches(2.2), Inches(3.6), Inches(4.5))
    card.fill.solid()
    card.fill.fore_color.rgb = CARD_BG
    card.line.color.rgb = col
    tf = card.text_frame
    tf.word_wrap = True
    
    p = tf.paragraphs[0]
    p.text = stat
    p.font.name = "Arial Black"
    p.font.size = Pt(32)
    p.font.bold = True
    p.font.color.rgb = col
    p.alignment = PP_ALIGN.CENTER
    
    p_t = tf.add_paragraph()
    p_t.text = title
    p_t.font.name = "微軟正黑體"
    p_t.font.size = Pt(15)
    p_t.font.bold = True
    p_t.font.color.rgb = WHITE
    p_t.alignment = PP_ALIGN.CENTER
    p_t.space_before = Pt(8)
    
    p_d = tf.add_paragraph()
    p_d.text = desc
    p_d.font.name = "微軟正黑體"
    p_d.font.size = Pt(13)
    p_d.font.color.rgb = MUTED
    p_d.space_before = Pt(16)

# ==========================================
# Slide 7: 結語與致謝
# ==========================================
s7 = prs.slides.add_slide(blank_layout)
add_bg(s7)

tb = s7.shapes.add_textbox(Inches(1.5), Inches(1.8), Inches(10.3), Inches(4.5))
tf = tb.text_frame
tf.word_wrap = True

p = tf.paragraphs[0]
p.text = "「STEAM 教育不是昂貴的器材堆疊，\n而是讓孩子用一雙雙手，把課本上的公式變成眼前的物理奇蹟！」"
p.font.name = "微軟正黑體"
p.font.size = Pt(28)
p.font.bold = True
p.font.color.rgb = CYAN_ACCENT
p.alignment = PP_ALIGN.CENTER

p2 = tf.add_paragraph()
p2.text = "感謝 臺中市政府教育局 ✕ 國立臺中科技大學 推動校園 STEAM 教育實施計畫團隊"
p2.font.name = "微軟正黑體"
p2.font.size = Pt(18)
p2.font.color.rgb = WHITE
p2.alignment = PP_ALIGN.CENTER
p2.space_before = Pt(32)

p3 = tf.add_paragraph()
p3.text = "中正國小將持續在校園播下創客與探究的種子 · 敬請長官前輩不吝指教！"
p3.font.name = "微軟正黑體"
p3.font.size = Pt(16)
p3.font.color.rgb = MUTED
p3.alignment = PP_ALIGN.CENTER
p3.space_before = Pt(16)

out_pptx = os.path.join(PPTX_DIR, "臺中市梧棲區中正國小_STEAM成果展_5分鐘現場分享會簡報.pptx")
prs.save(out_pptx)
print(f"🎉 成果展 16:9 現場分享會簡報 (.pptx) 已成功產出：{os.path.basename(out_pptx)}")

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
生成 16:9 成果展 5 分鐘現場簡報 16 頁精裝版 (.pptx)
字體放大 3 倍 · 徹底移除學生照片（無肖像權風險）
與 Reveal.js 16 頁簡報完全對齊
"""

import os
import pptx
from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE

PPTX_DIR = r"d:\antui\steam成果製作\成果展繳交資料"

prs = pptx.Presentation()
prs.slide_width = Inches(13.333)
prs.slide_height = Inches(7.5)
blank_layout = prs.slide_layouts[6]

# 顏色定義
DARK_BG = RGBColor(9, 13, 20)        # #090D14
CARD_BG = RGBColor(15, 23, 42)       # #0F172A
CYAN_ACCENT = RGBColor(79, 195, 247) # #4FC3F7
ORANGE_ACCENT = RGBColor(232, 100, 58) # #E8643A
GREEN_ACCENT = RGBColor(129, 199, 132) # #81C784
AMBER_ACCENT = RGBColor(255, 183, 77)  # #FFB74D
WHITE = RGBColor(248, 250, 252)
MUTED = RGBColor(148, 163, 184)
RED_ACCENT = RGBColor(239, 68, 68)

def add_bg(slide, color=DARK_BG):
    bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, prs.slide_width, prs.slide_height)
    bg.fill.solid()
    bg.fill.fore_color.rgb = color
    bg.line.fill.background()
    return bg

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
    p1.space_before = Pt(6)

# -------------------------------------------------------------
# S01: 封面 (大字)
# -------------------------------------------------------------
s1 = prs.slides.add_slide(blank_layout)
add_bg(s1)
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
p.space_before = Pt(16)

p = tf.add_paragraph()
p.text = "智高積木融入三年級數學「公斤與公克」重量測量機關課程"
p.font.name = "微軟正黑體"
p.font.size = Pt(26)
p.font.bold = True
p.font.color.rgb = ORANGE_ACCENT
p.space_before = Pt(14)

p = tf.add_paragraph()
p.text = "發表人：臺中市梧棲區中正國小 謝敦元 老師 (召集人)\n社群成員：王怡婷、李仁耀、曾泊淞 老師"
p.font.name = "微軟正黑體"
p.font.size = Pt(20)
p.font.color.rgb = MUTED
p.space_before = Pt(30)

# -------------------------------------------------------------
# S02: 社群推動背景與無瑕成果 (大字)
# -------------------------------------------------------------
s2 = prs.slides.add_slide(blank_layout)
add_bg(s2)
add_header(s2, "社群推動脈絡：踏實共備與 100% 執行")

cards_data = [
    ("① 4人核心陣容", "謝敦元、王怡婷、李仁耀、曾泊淞老師跨領域深度共備。"),
    ("② 7場高密研習", "自5月至10月扎實推進，公開觀議課100%按進度完成。"),
    ("③ 16,000元結報", "16節講師鐘點費全數如期執行、正楷手簽領據無瑕核銷。"),
    ("④ 跨校外聘深化", "特聘南投鯉魚國小陳建安老師指導，引進機關王機構經驗。")
]
for i, (title, desc) in enumerate(cards_data):
    left = Inches(0.8 + i * 2.95)
    card = s2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, Inches(2.0), Inches(2.8), Inches(4.7))
    card.fill.solid()
    card.fill.fore_color.rgb = CARD_BG
    card.line.color.rgb = CYAN_ACCENT
    card.line.width = Pt(2)
    tf = card.text_frame
    tf.word_wrap = True
    p0 = tf.paragraphs[0]
    p0.text = title
    p0.font.name = "微軟正黑體"
    p0.font.size = Pt(24)
    p0.font.bold = True
    p0.font.color.rgb = CYAN_ACCENT
    p1 = tf.add_paragraph()
    p1.text = desc
    p1.font.name = "微軟正黑體"
    p1.font.size = Pt(20)
    p1.font.color.rgb = WHITE
    p1.space_before = Pt(14)

# -------------------------------------------------------------
# S03: 現場互動提問（文字雲） (大字)
# -------------------------------------------------------------
s3 = prs.slides.add_slide(blank_layout)
add_bg(s3)
add_header(s3, "現場互動提問：提到國小「重量測量」，學生最常卡在哪？")
c = s3.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(2.0), Inches(11.7), Inches(4.7))
c.fill.solid()
c.fill.fore_color.rgb = CARD_BG
c.line.color.rgb = AMBER_ACCENT
c.line.width = Pt(2)
tf = c.text_frame
tf.word_wrap = True
p = tf.paragraphs[0]
p.text = "【現場即時反思文字雲】三大痛點高頻集中："
p.font.name = "微軟正黑體"
p.font.size = Pt(28)
p.font.bold = True
p.font.color.rgb = AMBER_ACCENT

items = [
    ("🚨 痛點一：刻度指針黑盒子", "彈簧秤未歸零就讀數，大格小格混淆（誤把100g中的一小格當成10g）。"),
    ("🚨 痛點二：手感經驗與生活斷層", "死背「1公斤=1000公克」，卻無法體會 1 公斤拿在手上到底多重。"),
    ("🚨 痛點三：直覺迷思難撼動", "堅信「體積大就一定重、體積小就一定輕」，被外觀強烈誤導。")
]
for t, d in items:
    p = tf.add_paragraph()
    p.text = f"{t} —— {d}"
    p.font.name = "微軟正黑體"
    p.font.size = Pt(22)
    p.font.color.rgb = WHITE
    p.space_before = Pt(16)

# -------------------------------------------------------------
# S04: STEAM 跨領域核心解法 (大字)
# -------------------------------------------------------------
s4 = prs.slides.add_slide(blank_layout)
add_bg(s4)
add_header(s4, "教學痛點轉化：STEAM 跨領域核心解法")
s4_cards = [
    ("S & E 物理結構解密", "親手組裝等臂支點、降低摩擦力，讓孩子直接看見力矩與重力下沉的物理本質。"),
    ("T 機關靈敏度調校", "利用智高積木微調滑塊與指針歸零機關，體驗工程師面對誤差時的校準思維。"),
    ("M 數學加減真實化", "將「公斤與公克」的抽象加減法，化為左盤放物、右盤累加單位積木的直觀運算體驗。")
]
for i, (t, d) in enumerate(s4_cards):
    left = Inches(0.8 + i * 3.95)
    card = s4.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, Inches(2.0), Inches(3.8), Inches(4.7))
    card.fill.solid()
    card.fill.fore_color.rgb = CARD_BG
    card.line.color.rgb = ORANGE_ACCENT if i==0 else (CYAN_ACCENT if i==1 else GREEN_ACCENT)
    card.line.width = Pt(2)
    tf = card.text_frame
    tf.word_wrap = True
    p0 = tf.paragraphs[0]
    p0.text = t
    p0.font.name = "微軟正黑體"
    p0.font.size = Pt(26)
    p0.font.bold = True
    p0.font.color.rgb = card.line.color.rgb
    p1 = tf.add_paragraph()
    p1.text = d
    p1.font.name = "微軟正黑體"
    p1.font.size = Pt(21)
    p1.font.color.rgb = WHITE
    p1.space_before = Pt(16)

# -------------------------------------------------------------
# S05: 課綱素養對齊 (大字雙欄)
# -------------------------------------------------------------
s5 = prs.slides.add_slide(blank_layout)
add_bg(s5)
add_header(s5, "課程核心依據：十二年國教數學領域指標對齊")
for i, (col_title, col_color, bullets) in enumerate([
    ("🎯 學習內容對齊 (Content Standards)", CYAN_ACCENT, [
        "n-II-8 重量測量：認識重量單位「公斤」與「公克」，使用天平與秤進行實測與估測。",
        "n-II-9 單位關係換算：理解 1 公斤 = 1000 公克，並進行單位間化聚與比較。",
        "n-II-2 兩步驟加減計算：在具體情境中解決包含公斤與公克的加減應用問題。"
    ]),
    ("🌟 STEAM 核心素養轉化", ORANGE_ACCENT, [
        "數-E-A1 具備量感：建立實體重量手感，破除「體積大就一定重」的直覺迷思。",
        "科-E-B2 科技操作：熟練運用智高積木完成對稱力臂與承重托盤組裝。",
        "自-E-C2 團隊探究：小組合作進行平衡校準、數據記錄與多元策略分享。"
    ])
]):
    left = Inches(0.8 + i * 5.95)
    c = s5.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, Inches(2.0), Inches(5.8), Inches(4.7))
    c.fill.solid()
    c.fill.fore_color.rgb = CARD_BG
    c.line.color.rgb = col_color
    c.line.width = Pt(2)
    tf = c.text_frame
    tf.word_wrap = True
    p0 = tf.paragraphs[0]
    p0.text = col_title
    p0.font.name = "微軟正黑體"
    p0.font.size = Pt(24)
    p0.font.bold = True
    p0.font.color.rgb = col_color
    for b in bullets:
        p = tf.add_paragraph()
        p.text = "• " + b
        p.font.name = "微軟正黑體"
        p.font.size = Pt(20)
        p.font.color.rgb = WHITE
        p.space_before = Pt(12)

# -------------------------------------------------------------
# S06: 階梯式三節探究地圖 (大字)
# -------------------------------------------------------------
s6 = prs.slides.add_slide(blank_layout)
add_bg(s6)
add_header(s6, "三節課循序進階架構：階梯式探究地圖")
s6_data = [
    ("第1節：手感衝突與需求", AMBER_ACCENT, "徒手掂重排序 ➔ 發現組員排序完全相反 ➔ 察覺人體感知盲區 ➔ 萌生製作客觀天平的需求。"),
    ("第2節：智高天平組裝", CYAN_ACCENT, "等臂力臂搭建 ➔ 支點低阻力轉軸調校 ➔ 雙托盤平衡懸吊 ➔ 指針歸零動態驗證。"),
    ("第3節：加減微調挑戰", GREEN_ACCENT, "單位小積木作為非標準砝碼 ➔ 加法累加與減法扣除 ➔ 數學算則與天平水平完美閉環。")
]
for i, (t, col, d) in enumerate(s6_data):
    left = Inches(0.8 + i * 3.95)
    card = s6.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, Inches(2.0), Inches(3.8), Inches(4.7))
    card.fill.solid()
    card.fill.fore_color.rgb = CARD_BG
    card.line.color.rgb = col
    card.line.width = Pt(2)
    tf = card.text_frame
    tf.word_wrap = True
    p0 = tf.paragraphs[0]
    p0.text = t
    p0.font.name = "微軟正黑體"
    p0.font.size = Pt(26)
    p0.font.bold = True
    p0.font.color.rgb = col
    p1 = tf.add_paragraph()
    p1.text = d
    p1.font.name = "微軟正黑體"
    p1.font.size = Pt(21)
    p1.font.color.rgb = WHITE
    p1.space_before = Pt(16)

# -------------------------------------------------------------
# S07: 第 1 節實踐：手感估測與認知衝突 (大字雙欄)
# -------------------------------------------------------------
s7 = prs.slides.add_slide(blank_layout)
add_bg(s7)
add_header(s7, "第 1 節課堂實踐：徒手掂重引爆認知衝突")
c1 = s7.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(2.0), Inches(5.8), Inches(4.7))
c1.fill.solid()
c1.fill.fore_color.rgb = CARD_BG
c1.line.color.rgb = AMBER_ACCENT
c1.line.width = Pt(2)
tf1 = c1.text_frame
tf1.word_wrap = True
p0 = tf1.paragraphs[0]
p0.text = "🔥 課堂實況：主觀手感大混亂"
p0.font.name = "微軟正黑體"
p0.font.size = Pt(26)
p0.font.bold = True
p0.font.color.rgb = AMBER_ACCENT
p1 = tf1.add_paragraph()
p1.text = "課堂給予大小外觀相異物品（保麗龍球、木積木、鐵鎖、水瓶）。\n學生徒手掂重排序時，全班出現高達 6 種完全不同的排序結果！\n\n孩子們開始激烈討論，深刻體會到：\n「人手的肌肉記憶是有誤差的，我們需要一個公正客觀的工具！」"
p1.font.name = "微軟正黑體"
p1.font.size = Pt(21)
p1.font.color.rgb = WHITE
p1.space_before = Pt(14)

c2 = s7.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.8), Inches(2.0), Inches(5.7), Inches(4.7))
c2.fill.solid()
c2.fill.fore_color.rgb = CARD_BG
c2.line.color.rgb = CYAN_ACCENT
c2.line.width = Pt(2)
tf2 = c2.text_frame
tf2.word_wrap = True
p0 = tf2.paragraphs[0]
p0.text = "💡 STEAM 探究起點：自主提問"
p0.font.name = "微軟正黑體"
p0.font.size = Pt(26)
p0.font.bold = True
p0.font.color.rgb = CYAN_ACCENT
p1 = tf2.add_paragraph()
p1.text = "學生自主歸納出三大工具需求：\n\n1. 必須有支點：兩邊長度要完全一樣長（等臂概念）。\n2. 托盤自由晃動：兩側不能卡住，要能上下自由傾斜。\n3. 水平指針回饋：中間要有指針，明確指示何時「剛好一樣重」。"
p1.font.name = "微軟正黑體"
p1.font.size = Pt(21)
p1.font.color.rgb = WHITE
p1.space_before = Pt(14)

# -------------------------------------------------------------
# S08: 第 2 節實踐：智高天平四核心組件 (大字)
# -------------------------------------------------------------
s8 = prs.slides.add_slide(blank_layout)
add_bg(s8)
add_header(s8, "第 2 節課堂實踐：智高積木四核心組件組裝")
parts = [
    ("① 梯形寬底座", "多孔長條與配重三角架，提供低重心扎實底盤，防止翻覆。"),
    ("② 對稱等臂橫樑", "左右各數 10 個積木孔，嚴格維持左力臂 = 右力臂，力矩對等。"),
    ("③ 零摩擦中心轉軸", "光滑圓軸連接中孔，保留微隙降低摩擦阻尼，提升擺盪靈敏度。"),
    ("④ 懸吊托盤與指針", "下方垂直垂懸指針，搭配底座刻度基準線，是否水平一目了然！")
]
for i, (t, d) in enumerate(parts):
    left = Inches(0.8 + i * 2.95)
    card = s8.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, Inches(2.0), Inches(2.8), Inches(4.7))
    card.fill.solid()
    card.fill.fore_color.rgb = CARD_BG
    card.line.color.rgb = CYAN_ACCENT
    card.line.width = Pt(2)
    tf = card.text_frame
    tf.word_wrap = True
    p0 = tf.paragraphs[0]
    p0.text = t
    p0.font.name = "微軟正黑體"
    p0.font.size = Pt(24)
    p0.font.bold = True
    p0.font.color.rgb = CYAN_ACCENT
    p1 = tf.add_paragraph()
    p1.text = d
    p1.font.name = "微軟正黑體"
    p1.font.size = Pt(20)
    p1.font.color.rgb = WHITE
    p1.space_before = Pt(14)

# -------------------------------------------------------------
# S09: 物理力學視覺化（無人物肖像·純機構架構大字）
# -------------------------------------------------------------
s9 = prs.slides.add_slide(blank_layout)
add_bg(s9)
add_header(s9, "物理機制解析：天平傾斜與指針判定規則")
c1 = s9.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(2.0), Inches(5.8), Inches(4.7))
c1.fill.solid()
c1.fill.fore_color.rgb = CARD_BG
c1.line.color.rgb = ORANGE_ACCENT
c1.line.width = Pt(2)
tf = c1.text_frame
tf.word_wrap = True
p0 = tf.paragraphs[0]
p0.text = "⚖️ 傾斜動態的力學語言"
p0.font.name = "微軟正黑體"
p0.font.size = Pt(26)
p0.font.bold = True
p0.font.color.rgb = ORANGE_ACCENT
p1 = tf.add_paragraph()
p1.text = "• 左盤下沉：左邊物品重力大於右邊，力矩不平衡。\n• 右盤下沉：右邊物品重力勝出。\n• 指針居中（水平）：兩側重力恰好相等，達成力矩平衡。\n• 微調滑塊：利用橫樑上的微調積木消除結構微小公差。"
p1.font.name = "微軟正黑體"
p1.font.size = Pt(21)
p1.font.color.rgb = WHITE
p1.space_before = Pt(14)

c2 = s9.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.8), Inches(2.0), Inches(5.7), Inches(4.7))
c2.fill.solid()
c2.fill.fore_color.rgb = CARD_BG
c2.line.color.rgb = CYAN_ACCENT
c2.line.width = Pt(2)
tf2 = c2.text_frame
tf2.word_wrap = True
p0 = tf2.paragraphs[0]
p0.text = "📐 等臂天平力學平衡判定"
p0.font.name = "微軟正黑體"
p0.font.size = Pt(26)
p0.font.bold = True
p0.font.color.rgb = CYAN_ACCENT
p1 = tf2.add_paragraph()
p1.text = "【核心工程參數對稱性】：\n• 左力臂 L1 = 右力臂 L2 = 10 孔距\n• 轉軸中心阻尼極小化，靈敏擺盪\n• 垂直垂懸指針對準底座中心基準刻度\n• 下降側＝較重側，指針偏移直觀判讀"
p1.font.name = "微軟正黑體"
p1.font.size = Pt(21)
p1.font.color.rgb = WHITE
p1.space_before = Pt(14)

# -------------------------------------------------------------
# S10: 課堂迷思快問快答（單選投票） (大字)
# -------------------------------------------------------------
s10 = prs.slides.add_slide(blank_layout)
add_bg(s10)
add_header(s10, "課堂迷思快問快答：破除「體積大就一定重」")
c = s10.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(2.0), Inches(11.7), Inches(4.7))
c.fill.solid()
c.fill.fore_color.rgb = CARD_BG
c.line.color.rgb = GREEN_ACCENT
c.line.width = Pt(2)
tf = c.text_frame
tf.word_wrap = True
p = tf.paragraphs[0]
p.text = "【快問快答】等臂天平左放 100g 保麗龍大球，右放 100g 實心鐵砝碼，結果會如何？"
p.font.name = "微軟正黑體"
p.font.size = Pt(26)
p.font.bold = True
p.font.color.rgb = AMBER_ACCENT

opts = [
    ("A. 左盤下沉（保麗龍球體積很大，向下壓的力量大）", "直覺迷思 ❌"),
    ("B. 右盤下沉（鐵塊感覺密度很高，所以特別沉）", "直覺迷思 ❌"),
    ("C. 兩盤水平平衡（質量同為 100g，力矩相等）", "正確解答 ✅ (現場 76% 答對)"),
    ("D. 天平會不停隨機亂晃，無法判定", "錯誤概念 ❌")
]
for o, stat in opts:
    p = tf.add_paragraph()
    p.text = f"{o} —— 【{stat}】"
    p.font.name = "微軟正黑體"
    p.font.size = Pt(22)
    p.font.color.rgb = GREEN_ACCENT if "✅" in stat else WHITE
    p.space_before = Pt(14)

# -------------------------------------------------------------
# S11: 第 3 節實踐：加減微調平衡挑戰 (大字雙欄)
# -------------------------------------------------------------
s11 = prs.slides.add_slide(blank_layout)
add_bg(s11)
add_header(s11, "第 3 節課堂實踐：單位積木與加減微調挑戰")
for i, (t, col, d) in enumerate([
    ("🧱 非標準單位到標準單位", CYAN_ACCENT, "先以每個重 5 公克的智高黃色小單位積木作為「非標準砝碼」。\n左盤放橡皮擦，右盤一個一個加入小積木：\n「1個、2個...加到第 6 個時天平剛好水平！」\n➔ 橡皮擦重量 = 6 個小積木 ✕ 5g = 30 公克！"),
    ("🧮 算則的真實反饋", GREEN_ACCENT, "如果右盤放了 8 個積木導致右邊下沉？\n孩子會主動說：「右邊太重了，要減去 2 個積木！」\n減法（扣除）與加法（累加）不再是冷冰冰的符號，而是讓天平重返水平的魔法操作。")
]):
    left = Inches(0.8 + i * 5.95)
    c = s11.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, Inches(2.0), Inches(5.8), Inches(4.7))
    c.fill.solid()
    c.fill.fore_color.rgb = CARD_BG
    c.line.color.rgb = col
    c.line.width = Pt(2)
    tf = c.text_frame
    tf.word_wrap = True
    p0 = tf.paragraphs[0]
    p0.text = t
    p0.font.name = "微軟正黑體"
    p0.font.size = Pt(26)
    p0.font.bold = True
    p0.font.color.rgb = col
    p1 = tf.add_paragraph()
    p1.text = d
    p1.font.name = "微軟正黑體"
    p1.font.size = Pt(21)
    p1.font.color.rgb = WHITE
    p1.space_before = Pt(14)

# -------------------------------------------------------------
# S12: 算則微調實驗：不平衡時怎麼辦？ (大字雙欄)
# -------------------------------------------------------------
s12 = prs.slides.add_slide(blank_layout)
add_bg(s12)
add_header(s12, "課堂深度探究：兩步驟加減法情境具象化")
for i, (t, col, d) in enumerate([
    ("策略 A：較輕側「補足差額」（加法思維）", ORANGE_ACCENT, "左盤放 120g 物品，右盤放 100g 砝碼 ➔ 右側翹起（較輕）。\n\n• 數學算式：120 - 100 = 20g\n• 具體動作：在右盤加放 20g 單位積木，天平回正！"),
    ("策略 B：較重側「移除多餘」（減法思維）", GREEN_ACCENT, "兩側原本各放 150g 平衡，左盤額外滑入 30g 零件 ➔ 左側下沉。\n\n• 數學算式：180 - 30 = 150g\n• 具體動作：將左盤額外 30g 移出，指針立刻回歸水平！")
]):
    left = Inches(0.8 + i * 5.95)
    c = s12.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, Inches(2.0), Inches(5.8), Inches(4.7))
    c.fill.solid()
    c.fill.fore_color.rgb = CARD_BG
    c.line.color.rgb = col
    c.line.width = Pt(2)
    tf = c.text_frame
    tf.word_wrap = True
    p0 = tf.paragraphs[0]
    p0.text = t
    p0.font.name = "微軟正黑體"
    p0.font.size = Pt(26)
    p0.font.bold = True
    p0.font.color.rgb = col
    p1 = tf.add_paragraph()
    p1.text = d
    p1.font.name = "微軟正黑體"
    p1.font.size = Pt(21)
    p1.font.color.rgb = WHITE
    p1.space_before = Pt(14)

# -------------------------------------------------------------
# S13: 課堂變革滑桿對比 (大字雙欄)
# -------------------------------------------------------------
s13 = prs.slides.add_slide(blank_layout)
add_bg(s13)
add_header(s13, "教學典範轉移：傳統讀秤 vs STEAM 動手調校")
c1 = s13.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(2.0), Inches(5.8), Inches(4.7))
c1.fill.solid()
c1.fill.fore_color.rgb = CARD_BG
c1.line.color.rgb = RED_ACCENT
c1.line.width = Pt(2)
tf1 = c1.text_frame
tf1.word_wrap = True
p = tf1.paragraphs[0]
p.text = "❌ 傳統課堂痛點"
p.font.name = "微軟正黑體"
p.font.size = Pt(26)
p.font.bold = True
p.font.color.rgb = RED_ACCENT
p = tf1.add_paragraph()
p.text = "• 學生面對彈簧秤，指針未歸零直接判讀。\n• 刻度密密麻麻，學生常把一小格看錯。\n• 抽象死背「1公斤=1000公克」，無法感知實體量感。\n• 算式寫得漂亮，日常生活稱重時完全失靈。"
p.font.name = "微軟正黑體"
p.font.size = Pt(21)
p.font.color.rgb = WHITE
p.space_before = Pt(12)

c2 = s13.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.8), Inches(2.0), Inches(5.7), Inches(4.7))
c2.fill.solid()
c2.fill.fore_color.rgb = CARD_BG
c2.line.color.rgb = GREEN_ACCENT
c2.line.width = Pt(2)
tf2 = c2.text_frame
tf2.word_wrap = True
p = tf2.paragraphs[0]
p.text = "✅ STEAM 動手調校新典範"
p.font.name = "微軟正黑體"
p.font.size = Pt(26)
p.font.bold = True
p.font.color.rgb = GREEN_ACCENT
p = tf2.add_paragraph()
p.text = "• 親手組裝等臂力臂，徹底理解指針歸零的關鍵。\n• 透過 5g 小積木逐個疊加，體會非標準到標準單位。\n• 算則直接轉化為動作：較輕則加、較重則減。\n• 建立深厚體感量感，課堂充滿主動探究與歡呼！"
p.font.name = "微軟正黑體"
p.font.size = Pt(21)
p.font.color.rgb = WHITE
p.space_before = Pt(12)

# -------------------------------------------------------------
# S14: 縱向延展 (一)：四年級 micro:bit 科技體育 (無人物·純架構大字)
# -------------------------------------------------------------
s14 = prs.slides.add_slide(blank_layout)
add_bg(s14)
add_header(s14, "社群成果縱向延展 (一)：四年級 micro:bit 甩繩智慧教練")
c1 = s14.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(2.0), Inches(5.8), Inches(4.7))
c1.fill.solid()
c1.fill.fore_color.rgb = CARD_BG
c1.line.color.rgb = CYAN_ACCENT
c1.line.width = Pt(2)
tf = c1.text_frame
tf.word_wrap = True
p0 = tf.paragraphs[0]
p0.text = "🏃‍♂️ 甩繩軌跡神射手：數據驅動體育"
p0.font.name = "微軟正黑體"
p0.font.size = Pt(26)
p0.font.bold = True
p0.font.color.rgb = CYAN_ACCENT
p1 = tf.add_paragraph()
p1.text = "• 加速度感測：將 micro:bit 封裝於大跳繩握把，即時捕捉三軸加速度向量。\n• 離心力與節奏演算法：每甩動一圈自動濾波計數，無線廣播即時傳輸。\n• 大螢幕即時回饋：體育課 8 人跳繩現場看見甩繩穩定度數據，破除運動傷害盲點！"
p1.font.name = "微軟正黑體"
p1.font.size = Pt(21)
p1.font.color.rgb = WHITE
p1.space_before = Pt(14)

c2 = s14.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.8), Inches(2.0), Inches(5.7), Inches(4.7))
c2.fill.solid()
c2.fill.fore_color.rgb = CARD_BG
c2.line.color.rgb = CYAN_ACCENT
c2.line.width = Pt(2)
tf2 = c2.text_frame
tf2.word_wrap = True
p0 = tf2.paragraphs[0]
p0.text = "📡 系統拓撲與數據傳輸架構"
p0.font.name = "微軟正黑體"
p0.font.size = Pt(26)
p0.font.bold = True
p0.font.color.rgb = CYAN_ACCENT
p1 = tf2.add_paragraph()
p1.text = "【前端感測】：握把微處理器 (3-Axis Accelerometer)\n          ⬇ 無線廣播 (Radio Broadcast 2.4GHz)\n【中端網關】：接收終端 (Edge Filtering Algorithm)\n          ⬇ 即時數據管道 (Real-time Stream)\n【後端展示】：體育館大螢幕 (即時波形與轉速)"
p1.font.name = "微軟正黑體"
p1.font.size = Pt(20)
p1.font.color.rgb = WHITE
p1.space_before = Pt(14)

# -------------------------------------------------------------
# S15: 縱向延展 (二)：世界機關王 (GM) 校隊梯隊 (無人物·純機構大字)
# -------------------------------------------------------------
s15 = prs.slides.add_slide(blank_layout)
add_bg(s15)
add_header(s15, "社群成果縱向延展 (二)：世界機關王 (GM) 校隊梯隊")
c1 = s15.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(2.0), Inches(5.8), Inches(4.7))
c1.fill.solid()
c1.fill.fore_color.rgb = CARD_BG
c1.line.color.rgb = AMBER_ACCENT
c1.line.width = Pt(2)
tf = c1.text_frame
tf.word_wrap = True
p0 = tf.paragraphs[0]
p0.text = "⚙️ 複合機關整合工藝"
p0.font.name = "微軟正黑體"
p0.font.size = Pt(26)
p0.font.bold = True
p0.font.color.rgb = AMBER_ACCENT
p1 = tf.add_paragraph()
p1.text = "• 斜面重力位能：金屬球沿軌道滾動加速累積動能。\n• 天平觸發開關：球體滾入天平托盤，力矩失衡下沉，精準扣動下一道骨牌連鎖。\n• 齒輪降速組：結合減速齒輪箱傳遞強大扭力，完成連鎖關卡 100% 穩定觸發！"
p1.font.name = "微軟正黑體"
p1.font.size = Pt(21)
p1.font.color.rgb = WHITE
p1.space_before = Pt(14)

c2 = s15.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.8), Inches(2.0), Inches(5.7), Inches(4.7))
c2.fill.solid()
c2.fill.fore_color.rgb = CARD_BG
c2.line.color.rgb = AMBER_ACCENT
c2.line.width = Pt(2)
tf2 = c2.text_frame
tf2.word_wrap = True
p0 = tf2.paragraphs[0]
p0.text = "🔗 三重連續連鎖機關拓撲"
p0.font.name = "微軟正黑體"
p0.font.size = Pt(26)
p0.font.bold = True
p0.font.color.rgb = AMBER_ACCENT
p1 = tf2.add_paragraph()
p1.text = "【關卡 1】：斜面重力位能釋放 ➔ 金屬球加速滾動\n          ⬇ 撞擊觸發\n【關卡 2】：等臂天平微型開關 ➔ 槓桿失衡下沉釋放\n          ⬇ 骨牌骨牌效應\n【關卡 3】：多級減速齒輪箱 ➔ 大扭力帶動終點機關"
p1.font.name = "微軟正黑體"
p1.font.size = Pt(20)
p1.font.color.rgb = WHITE
p1.space_before = Pt(14)

# -------------------------------------------------------------
# S16: 推動成效、評量規準與未來展望 (大字)
# -------------------------------------------------------------
s16 = prs.slides.add_slide(blank_layout)
add_bg(s16)
add_header(s16, "亮眼推動成效與未來展望：讓 STEAM 在中正生根")
cards_end = [
    ("理解度提升 +28.5%", GREEN_ACCENT, "前後測顯示，學生在重量單位換算與天平平衡概念題型，答對率由 63.2% 躍升至 91.7%！"),
    ("組裝任務 100% 達成", CYAN_ACCENT, "全年級各組均能自主完成智高天平組裝與指針歸零調校，展現卓越之動手實踐自信心。"),
    ("持續跨年級深耕", ORANGE_ACCENT, "社群教案無私公開分享於全校課發會，持續拓展至中高年級物理、科技與體育跨域課程。")
]
for i, (t, col, d) in enumerate(cards_end):
    left = Inches(0.8 + i * 3.95)
    card = s16.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, Inches(2.0), Inches(3.8), Inches(4.7))
    card.fill.solid()
    card.fill.fore_color.rgb = CARD_BG
    card.line.color.rgb = col
    card.line.width = Pt(2)
    tf = card.text_frame
    tf.word_wrap = True
    p0 = tf.paragraphs[0]
    p0.text = t
    p0.font.name = "微軟正黑體"
    p0.font.size = Pt(26)
    p0.font.bold = True
    p0.font.color.rgb = col
    p1 = tf.add_paragraph()
    p1.text = d
    p1.font.name = "微軟正黑體"
    p1.font.size = Pt(21)
    p1.font.color.rgb = WHITE
    p1.space_before = Pt(16)

# 儲存
out_pptx = os.path.join(PPTX_DIR, "臺中市梧棲區中正國小_STEAM成果展_5分鐘現場分享會簡報.pptx")
prs.save(out_pptx)
print(f"Successfully generated 16-slide PPTX (Large font, No photos): {out_pptx}")

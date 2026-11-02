#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
將 5分鐘發表逐字講稿 與 成果展一頁精華備忘單 轉換為精美可編輯 .docx
"""

import os
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import parse_xml, OxmlElement
from docx.oxml.ns import nsdecls, qn

DOC_DIR = r"d:\antui\steam成果製作\成果展繳交資料"

def set_cell_background(cell, color_hex):
    tcPr = cell._tc.get_or_add_tcPr()
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{color_hex}"/>')
    tcPr.append(shd)

def set_cell_margins(cell, top=120, bottom=120, left=150, right=150):
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = parse_xml(f'<w:tcMar {nsdecls("w")}><w:top w:w="{top}" w:type="dxa"/><w:bottom w:w="{bottom}" w:type="dxa"/><w:left w:w="{left}" w:type="dxa"/><w:right w:w="{right}" w:type="dxa"/></w:tcMar>')
    tcPr.append(tcMar)

def create_script_docx():
    doc = docx.Document()
    # 邊界 2 cm
    for s in doc.sections:
        s.top_margin = Inches(0.8)
        s.bottom_margin = Inches(0.8)
        s.left_margin = Inches(0.8)
        s.right_margin = Inches(0.8)

    # 標題
    p_top = doc.add_paragraph()
    r_top = p_top.add_run("臺中市梧棲區中正國民小學 115年度STEAM教師專業學習社群")
    r_top.font.name = "微軟正黑體"
    r_top.font.size = Pt(11)
    r_top.font.color.rgb = RGBColor(100, 116, 139)

    p_title = doc.add_paragraph()
    r_title = p_title.add_run("成果展 5 分鐘現場發表逐字講稿（含每分鐘計時標記）")
    r_title.font.name = "微軟正黑體"
    r_title.font.size = Pt(18)
    r_title.bold = True
    r_title.font.color.rgb = RGBColor(15, 23, 42)

    # 基本資訊卡片
    t_info = doc.add_table(rows=2, cols=2)
    t_info.alignment = WD_TABLE_ALIGNMENT.CENTER
    info_data = [
        [("發表學校 / 發表人", "臺中市梧棲區中正國小 ／ 謝敦元 老師（召集人）"), ("社群夥伴", "王怡婷 老師、李仁耀 老師、曾泊淞 老師")],
        [("教案主題", "智高積木動手玩·三年級重量測量機關探究"), ("發表時長規範", "嚴格控制於 4分45秒 ～ 4分55秒（上限 5 分鐘）")]
    ]
    for r_idx, row in enumerate(info_data):
        for c_idx, (label, val) in enumerate(row):
            cell = t_info.cell(r_idx, c_idx)
            set_cell_background(cell, "F8FAFC")
            set_cell_margins(cell, 100, 100, 140, 140)
            p = cell.paragraphs[0]
            p.paragraph_format.space_after = Pt(2)
            r1 = p.add_run(f"{label}：")
            r1.font.name = "微軟正黑體"
            r1.font.size = Pt(9.5)
            r1.bold = True
            r1.font.color.rgb = RGBColor(71, 85, 105)
            r2 = p.add_run(val)
            r2.font.name = "微軟正黑體"
            r2.font.size = Pt(9.5)
            r2.font.color.rgb = RGBColor(15, 23, 42)
            r2.bold = ("4分45秒" in val or "謝敦元" in val)

    doc.add_paragraph().paragraph_format.space_after = Pt(6)

    # 各分段逐字稿
    sections_data = [
        ("【0:00 - 0:35】Slide 1 封面引言：從手感直覺到精準測量（~110 字）",
         "[投影片：Slide 1 封面]",
         "各位評審長官、教育局長官、以及現場所有致力於 STEAM 教育的教育夥伴們，大家早安！我是臺中市梧棲區中正國小 STEAM 教師社群召集人謝敦元。今天非常榮幸代表我們社群的四位老師，向各位分享我們這一年在中正國小三年級課堂所深耕的跨領域教案——「智高積木動手玩·三年級重量測量機關探究」。我們的核心理念非常純粹：「讓抽象的數學量感，在積木咔嗒聲中看得見、摸得到！」"),

        ("【0:35 - 1:15】Slide 2 痛點診斷與設計理念：為什麼要做天平？（~130 字）",
         "[按鍵換頁 ➜ Slide 2 痛點診斷與理念]",
         "各位老師在教三年級數學「公斤與公克」時，是否常發現孩子看著課本上的傳統指針秤，指針轉了半圈，孩子眼神卻是一片茫然？傳統教學常陷入兩個困境：第一，孩子只有模糊的「手感直覺」，缺乏對重量單位的實體量感；第二，指針秤是個黑盒子，孩子看不見「力矩與平衡」的內部動態。於是我們社群就在思考：「如果沒有秤，孩子能不能用智高積木，親手打造一個能判斷重量、甚至能微調平衡的測量機關？」這正是我們將數學「常用量測量」與科技領域「結構機關」深度融合的起點！"),

        ("【1:15 - 2:05】Slide 3 教案核心架構：三節階梯式探究歷程（~145 字）",
         "[按鍵換頁 ➜ Slide 3 三節課階梯式架構]",
         "依據 108 課綱核心素養，我們規劃了紮實的三節階梯式教學：\n• 第一節：概念建構與手感挑戰。孩子從徒手掂重量、將物品由輕到重排序，在不同人手感差異的衝突中，自主察覺「單憑手感是不準確的，我們需要公正的測量工具」。\n• 第二節：智高天平機關組裝。孩子化身小小工程師，運用支點、力臂與左右托盤組裝等臂天平。看著托盤「下降的一邊就是比較重」，孩子瞬間掌握了力的直觀視覺化。\n• 第三節：平衡挑戰與加減微調。這是全堂高潮！我們給孩子「小積木」作為標準加減單位。左邊重了怎麼辦？孩子學會在右邊加小積木，把抽象的數學加減法，轉化為親手調校平衡的真實體驗。"),

        ("【2:05 - 2:55】Slide 4 課堂試教與迷思突破：孩子眼裡的光（~145 字）",
         "[按鍵換頁 ➜ Slide 4 課堂實踐與迷思破除]",
         "（請看大螢幕照片）這是在三年丙班真實試教的感人一幕。孩子在操作中自發破除了兩大關鍵迷思：\n• 迷思一：「體積大就一定比較重嗎？」當孩子把拳頭大的保麗龍球放左邊、小小的金屬鐵砝碼放右邊，天平重重往右沉下的那刻，全班發出了驚呼，物質密度的概念在動手實證中深刻烙印！\n• 迷思二：「天平不平衡只能換物品嗎？」孩子在任務單上記錄：「我在輕的那邊再加 2 顆小積木，天平就剛好水平了！」數學的加減算則在孩子手指間自然流動，這就是最具素養感的學習！"),

        ("【2:55 - 3:45】Slide 5 縱向延展：從微型天平到世界機關王（~140 字）",
         "[按鍵換頁 ➜ Slide 5 縱向延展與多元場次]",
         "我們中正國小的社群推動絕不僅止於單一教案，而是串連起完整的科學與科技脈絡：\n• 向上延伸至四年級——王怡婷老師帶領的「micro:bit 甩繩軌跡神射手」，結合科技與體育，讓孩子在跳繩時透過加速度感測器即時看見發力數據；\n• 在高階競賽端——李仁耀老師與曾泊淞老師將天平槓桿原理延伸至「世界機關王（GM）機關整合賽」，帶領學生設計連鎖傳動機構。從課堂基礎到競賽梯隊，建構起校本 STEAM 梯隊！"),

        ("【3:45 - 4:25】Slide 6 質性量化成效與多元評量規準（~130 字）",
         "[按鍵換頁 ➜ Slide 6 推動成效與數據]",
         "回顧全年度 7 大活動場次，我們達成了三大成果：\n1. 量化成效顯著：課堂前後測數據顯示，學生在重量單位換算與量感估測的理解度大幅成長 28.5%，實作任務完成率達 100%。\n2. 評量工具完備：我們設計了完整的「學習單、任務操作紀錄單、機關作品評量規準」，兼顧歷程性與總結性評量。\n3. 行政財務 100% 執行：社群 16 節鐘點費 16,000 元整全數執行結報，經費執行率 100%，成果電子檔與領據正本已全數完成備查。"),

        ("【4:25 - 4:55】Slide 7 結語與未來展望：在積木聲中點燃科學夢（~90 字）",
         "[按鍵換頁 ➜ Slide 7 結語與致謝]",
         "最後，我們想以這句話總結中正國小的努力：「STEAM 教育不是昂貴的器材堆疊，而是讓孩子用一雙雙手，把課本上的公式變成眼前的物理奇蹟！」感謝臺中市政府教育局與推動校園 STEAM 計畫團隊的全力支持與悉心輔導，中正國小將持續在校園播下創客與探究的種子。以上是中正國小的報告，謝謝各位長官與老師的聆聽，敬請不吝指教！")
    ]

    for title, action, content in sections_data:
        h = doc.add_paragraph()
        h.paragraph_format.space_before = Pt(8)
        h.paragraph_format.space_after = Pt(2)
        r_h = h.add_run(title)
        r_h.font.name = "微軟正黑體"
        r_h.font.size = Pt(12)
        r_h.bold = True
        r_h.font.color.rgb = RGBColor(14, 116, 144)

        p_act = doc.add_paragraph()
        p_act.paragraph_format.space_after = Pt(4)
        r_act = p_act.add_run(action)
        r_act.font.name = "微軟正黑體"
        r_act.font.size = Pt(10)
        r_act.bold = True
        r_act.font.color.rgb = RGBColor(194, 65, 12)

        # 內文框
        tbl = doc.add_table(rows=1, cols=1)
        tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
        c = tbl.cell(0, 0)
        set_cell_background(c, "F1F5F9")
        set_cell_margins(c, 100, 100, 140, 140)
        p_c = c.paragraphs[0]
        p_c.paragraph_format.line_spacing = 1.25
        p_c.paragraph_format.space_after = Pt(0)
        r_c = p_c.add_run(content)
        r_c.font.name = "微軟正黑體"
        r_c.font.size = Pt(10.5)
        r_c.font.color.rgb = RGBColor(30, 41, 59)

        doc.add_paragraph().paragraph_format.space_after = Pt(4)

    out_docx = os.path.join(DOC_DIR, "臺中市梧棲區中正國小_STEAM成果展_5分鐘發表逐字講稿(含計時標記).docx")
    doc.save(out_docx)
    print(f"✅ 已成功產出逐字講稿 Word 檔：{os.path.basename(out_docx)}")

create_script_docx()

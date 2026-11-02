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

def set_cell_margins(cell, top=100, bottom=100, left=130, right=130):
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = parse_xml(f'<w:tcMar {nsdecls("w")}><w:top w:w="{top}" w:type="dxa"/><w:bottom w:w="{bottom}" w:type="dxa"/><w:left w:w="{left}" w:type="dxa"/><w:right w:w="{right}" w:type="dxa"/></w:tcMar>')
    tcPr.append(tcMar)

def create_cheatsheet_docx():
    doc = docx.Document()
    for s in doc.sections:
        s.top_margin = Inches(0.5)
        s.bottom_margin = Inches(0.5)
        s.left_margin = Inches(0.6)
        s.right_margin = Inches(0.6)

    # 標頭
    p_h = doc.add_paragraph()
    p_h.paragraph_format.space_after = Pt(2)
    r_h = p_h.add_run("臺中市梧棲區中正國小 115年度STEAM教師社群成果展")
    r_h.font.name = "微軟正黑體"
    r_h.font.size = Pt(10)
    r_h.font.color.rgb = RGBColor(100, 116, 139)

    p_t = doc.add_paragraph()
    p_t.paragraph_format.space_after = Pt(6)
    r_t = p_t.add_run("【一頁精華備忘單 · One-Page Cheat Sheet】")
    r_t.font.name = "微軟正黑體"
    r_t.font.size = Pt(16)
    r_t.bold = True
    r_t.font.color.rgb = RGBColor(15, 23, 42)

    # 一、基本身分表
    doc.add_paragraph().paragraph_format.space_after = Pt(1)
    p_s1 = doc.add_paragraph()
    p_s1.paragraph_format.space_after = Pt(3)
    r_s1 = p_s1.add_run("📌 一、 基本身分與核心資訊速查")
    r_s1.font.name = "微軟正黑體"
    r_s1.font.size = Pt(11)
    r_s1.bold = True
    r_s1.font.color.rgb = RGBColor(14, 116, 144)

    t1 = doc.add_table(rows=5, cols=2)
    t1.alignment = WD_TABLE_ALIGNMENT.CENTER
    d1 = [
        ("學校與社群", "臺中市梧棲區中正國民小學 —— 115年度推動校園STEAM教育教師專業學習社群"),
        ("社群成員", "謝敦元 老師（召集人／發表人）、王怡婷 老師、李仁耀 老師、曾泊淞 老師（名單完全無異動）"),
        ("核心教案", "智高積木融入三年級數學「公斤與公克」重量測量機關課程設計（附件6）"),
        ("跨域範疇", "數學領域（n-II-8 重量測量、n-II-9 單位比較、n-II-2 加減運算） ✕ 科技領域（機構設計）"),
        ("全案經費", "核定 16 節 × 1,000 元 ＝ 16,000 元整（預算執行率 100%，結餘款 0 元，領據正本已掛號寄達）")
    ]
    for r_i, (k, v) in enumerate(d1):
        c0 = t1.cell(r_i, 0)
        c1 = t1.cell(r_i, 1)
        c0.width = Inches(1.5)
        c1.width = Inches(5.6)
        set_cell_background(c0, "F8FAFC")
        set_cell_background(c1, "FFFFFF")
        set_cell_margins(c0, 60, 60, 100, 100)
        set_cell_margins(c1, 60, 60, 100, 100)
        p0 = c0.paragraphs[0]
        p0.paragraph_format.space_after = Pt(0)
        r0 = p0.add_run(k)
        r0.font.name = "微軟正黑體"
        r0.font.size = Pt(9)
        r0.bold = True
        r0.font.color.rgb = RGBColor(51, 65, 85)
        p1 = c1.paragraphs[0]
        p1.paragraph_format.space_after = Pt(0)
        r1 = p1.add_run(v)
        r1.font.name = "微軟正黑體"
        r1.font.size = Pt(9)
        r1.font.color.rgb = RGBColor(15, 23, 42)

    # 二、發表計時表
    p_s2 = doc.add_paragraph()
    p_s2.paragraph_format.space_before = Pt(6)
    p_s2.paragraph_format.space_after = Pt(3)
    r_s2 = p_s2.add_run("⏱️ 二、 5 分鐘發表計時節奏與換頁提詞")
    r_s2.font.name = "微軟正黑體"
    r_s2.font.size = Pt(11)
    r_s2.bold = True
    r_s2.font.color.rgb = RGBColor(14, 116, 144)

    t2 = doc.add_table(rows=8, cols=4)
    t2.alignment = WD_TABLE_ALIGNMENT.CENTER
    headers2 = ["時間碼", "投影片頁面", "發表重點", "口頭金句 / 提示動作"]
    for c_i, h_txt in enumerate(headers2):
        c = t2.cell(0, c_i)
        set_cell_background(c, "E2E8F0")
        set_cell_margins(c, 80, 80, 100, 100)
        p = c.paragraphs[0]
        p.paragraph_format.space_after = Pt(0)
        r = p.add_run(h_txt)
        r.font.name = "微軟正黑體"
        r.font.size = Pt(9)
        r.bold = True
        r.font.color.rgb = RGBColor(15, 23, 42)

    d2 = [
        ("0:00 - 0:35", "Slide 1 封面", "引言、夥伴、核心理念", "「讓抽象的數學量感，在積木咔嗒聲中看得見、摸得到！」"),
        ("0:35 - 1:15", "Slide 2 痛點理念", "傳統指針秤抽象、手感不準", "「如果沒有秤，孩子能不能自己做一個重量測量機關？」"),
        ("1:15 - 2:05", "Slide 3 三節架構", "1.手感估測 ➜ 2.機關 ➜ 3.平衡", "階梯式探究：支點力矩 ➜ 傾斜判定 ➜ 小積木微調平衡"),
        ("2:05 - 2:55", "Slide 4 課堂實踐", "破除兩大迷思（體積 vs 平衡）", "「老師，我再加2顆積木，它就真的平了！」（手指比平衡）"),
        ("2:55 - 3:45", "Slide 5 縱向延展", "四年級甩繩 ✕ 世界機關王梯隊", "科技體育（視覺化加速度）＋ 競賽梯隊連鎖機關整合"),
        ("3:45 - 4:25", "Slide 6 成效數據", "前後測理解度 +28.5%，評量完備", "量化 28.5% 躍升、實作 100% 達成、行政經費 100% 結算"),
        ("4:25 - 4:55", "Slide 7 結語致謝", "總結展望，感謝指導單位", "「把課本公式變成物理奇蹟！」敬請長官前輩不吝指教")
    ]
    for r_i, row in enumerate(d2, start=1):
        bg = "FFFFFF" if r_i % 2 == 1 else "F8FAFC"
        for c_i, val in enumerate(row):
            c = t2.cell(r_i, c_i)
            set_cell_background(c, bg)
            set_cell_margins(c, 50, 50, 80, 80)
            p = c.paragraphs[0]
            p.paragraph_format.space_after = Pt(0)
            r = p.add_run(val)
            r.font.name = "微軟正黑體"
            r.font.size = Pt(8.5)
            r.font.color.rgb = RGBColor(15, 23, 42)
            if c_i == 0:
                r.bold = True
                r.font.color.rgb = RGBColor(194, 65, 12)

    # 三、常見 Q&A 備答
    p_s3 = doc.add_paragraph()
    p_s3.paragraph_format.space_before = Pt(6)
    p_s3.paragraph_format.space_after = Pt(3)
    r_s3 = p_s3.add_run("💡 三、 評審與現場常見 Q&A 備答錦囊（30 秒精準回覆）")
    r_s3.font.name = "微軟正黑體"
    r_s3.font.size = Pt(11)
    r_s3.bold = True
    r_s3.font.color.rgb = RGBColor(14, 116, 144)

    qa_list = [
        ("Q1：智高積木零件繁多，在一般普通班教室實施時，會不會容易遺失或造成課堂混亂？",
         "A1 答題點：我們採用「模組化零件盒」＋「小組四人分工機制（A取料、B組裝、C測試、D記錄）」。每組僅發放指定之結構桿件與托盤扣件，課堂收整嚴格執行「清點歸位打卡單」，試教班級 40 分鐘內收整完畢且零件零遺失，具備高度在常態班級複製推廣的普及性！"),
        ("Q2：學生玩積木玩得很開心，但如何證明孩子真的學會了數學「公斤與公克」概念？",
         "A2 答題點：我們設計了三重評量規準：第一是課堂前測與後測（概念理解提升 28.5%）；第二是「任務操作紀錄單」，孩子必須記錄左右物品名稱、下降側判斷，並用「加減幾顆單位積木」寫出算式證明平衡；第三是孩子能用日常語言清楚說明「質量密度」與「手感 vs 工具」之差別，學習扎實深根。"),
        ("Q3：這套 STEAM 社群成果未來在學校是否有永續延續與推展的規劃？",
         "A3 答題點：已納入中正國小校本彈性課程發展計畫！三年級以本套「公斤與公克重量機關」為起點，四年級銜接王怡婷老師的「micro:bit 體育感測」，中高年級由李仁耀老師與曾泊淞老師對接「世界機關王校隊社團」，形成校內跨年級縱向連貫的 STEAM 科學實作學習地圖！")
    ]
    for q, a in qa_list:
        p_qa = doc.add_paragraph()
        p_qa.paragraph_format.space_after = Pt(1)
        r_q = p_qa.add_run(f"❓ {q}\n")
        r_q.font.name = "微軟正黑體"
        r_q.font.size = Pt(8.5)
        r_q.bold = True
        r_q.font.color.rgb = RGBColor(15, 23, 42)
        r_a = p_qa.add_run(f"👉 {a}")
        r_a.font.name = "微軟正黑體"
        r_a.font.size = Pt(8.5)
        r_a.font.color.rgb = RGBColor(71, 85, 105)

    out_docx = os.path.join(DOC_DIR, "臺中市梧棲區中正國小_STEAM成果展_一頁精華備忘單(CheatSheet).docx")
    doc.save(out_docx)
    print(f"✅ 已成功產出備忘單 Word 檔：{os.path.basename(out_docx)}")

create_cheatsheet_docx()

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
將 16 頁版 5分鐘發表逐字講稿 轉換為精美可編輯 .docx 與 .pdf
"""

import os
import re
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import parse_xml
from docx.oxml.ns import nsdecls

DOC_DIR = r"d:\antui\steam成果製作\成果展繳交資料"
MD_PATH = os.path.join(DOC_DIR, "5分鐘發表逐字講稿_含計時標記.md")

def set_cell_background(cell, color_hex):
    tcPr = cell._tc.get_or_add_tcPr()
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{color_hex}"/>')
    tcPr.append(shd)

def set_cell_margins(cell, top=100, bottom=100, left=140, right=140):
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = parse_xml(f'<w:tcMar {nsdecls("w")}><w:top w:w="{top}" w:type="dxa"/><w:bottom w:w="{bottom}" w:type="dxa"/><w:left w:w="{left}" w:type="dxa"/><w:right w:w="{right}" w:type="dxa"/></w:tcMar>')
    tcPr.append(tcMar)

def create_script_docx():
    doc = docx.Document()
    for s in doc.sections:
        s.top_margin = Inches(0.8)
        s.bottom_margin = Inches(0.8)
        s.left_margin = Inches(0.8)
        s.right_margin = Inches(0.8)

    # 頂部小字
    p_top = doc.add_paragraph()
    r_top = p_top.add_run("臺中市梧棲區中正國民小學 115年度STEAM教師專業學習社群")
    r_top.font.name = "微軟正黑體"
    r_top.font.size = Pt(11)
    r_top.font.color.rgb = RGBColor(100, 116, 139)

    # 主標題
    p_title = doc.add_paragraph()
    r_title = p_title.add_run("成果展 5 分鐘現場發表逐字講稿（16 頁精裝版 · 含每頁計時標記）")
    r_title.font.name = "微軟正黑體"
    r_title.font.size = Pt(18)
    r_title.bold = True
    r_title.font.color.rgb = RGBColor(15, 23, 42)

    # 基本資訊卡片
    t_info = doc.add_table(rows=2, cols=2)
    t_info.alignment = WD_TABLE_ALIGNMENT.CENTER
    info_data = [
        [("發表學校 / 發表人", "臺中市梧棲區中正國小 ／ 謝敦元 老師（召集人）"), ("社群夥伴", "王怡婷 老師、李仁耀 老師、曾泊淞 老師")],
        [("教案主題", "積木啟發量感 · 機關驗證平衡（16 頁精實簡報）"), ("發表時長規範", "嚴格控制於 4分45秒 ～ 4分55秒（上限 5 分鐘，每頁約18秒）")]
    ]
    for r_idx, row in enumerate(info_data):
        for c_idx, (label, val) in enumerate(row):
            cell = t_info.cell(r_idx, c_idx)
            set_cell_background(cell, "F8FAFC")
            set_cell_margins(cell, 80, 80, 120, 120)
            p = cell.paragraphs[0]
            p.paragraph_format.line_spacing = 1.2
            r_l = p.add_run(f"【{label}】\n")
            r_l.font.name = "微軟正黑體"
            r_l.font.size = Pt(9.5)
            r_l.font.color.rgb = RGBColor(100, 116, 139)
            r_l.bold = True
            r_v = p.add_run(val)
            r_v.font.name = "微軟正黑體"
            r_v.font.size = Pt(10.5)
            r_v.font.color.rgb = RGBColor(15, 23, 42)

    doc.add_paragraph().paragraph_format.space_after = Pt(8)

    # 讀取 MD 檔案內容
    with open(MD_PATH, 'r', encoding='utf-8') as f:
        md_text = f.read()

    # 解析各 Slide 區塊
    sections = re.findall(r'###\s*【(.*?)】\s*(Slide \d+.*?)\n> \*\*\[(.*?)\]\*\*\n>\s*\n(.*?)(?=\n---\n|\Z)', md_text, re.DOTALL)

    for time_mark, slide_title, action, content in sections:
        clean_content = "\n".join([line.strip()[2:] if line.strip().startswith('>') else line.strip() for line in content.strip().splitlines() if line.strip() and not line.strip().startswith('> **[')])
        clean_content = clean_content.replace('**', '')

        h = doc.add_paragraph()
        h.paragraph_format.space_before = Pt(8)
        h.paragraph_format.space_after = Pt(2)
        r_h = h.add_run(f"【{time_mark}】{slide_title}")
        r_h.font.name = "微軟正黑體"
        r_h.font.size = Pt(12)
        r_h.bold = True
        r_h.font.color.rgb = RGBColor(14, 116, 144)

        p_act = doc.add_paragraph()
        p_act.paragraph_format.space_after = Pt(4)
        r_act = p_act.add_run(f"[{action}]")
        r_act.font.name = "微軟正黑體"
        r_act.font.size = Pt(10)
        r_act.bold = True
        r_act.font.color.rgb = RGBColor(194, 65, 12)

        # 內文框
        tbl = doc.add_table(rows=1, cols=1)
        tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
        c = tbl.cell(0, 0)
        set_cell_background(c, "F1F5F9")
        set_cell_margins(c, 80, 80, 120, 120)
        p_c = c.paragraphs[0]
        p_c.paragraph_format.line_spacing = 1.25
        p_c.paragraph_format.space_after = Pt(0)
        r_c = p_c.add_run(clean_content)
        r_c.font.name = "微軟正黑體"
        r_c.font.size = Pt(10)
        r_c.font.color.rgb = RGBColor(30, 41, 59)

        doc.add_paragraph().paragraph_format.space_after = Pt(2)

    out_docx = os.path.join(DOC_DIR, "臺中市梧棲區中正國小_STEAM成果展_5分鐘發表逐字講稿(含計時標記).docx")
    doc.save(out_docx)
    print(f"✅ 已成功產出 16 頁版逐字講稿 Word 檔：{os.path.basename(out_docx)}")

    # 轉為 PDF
    try:
        import comtypes.client
        word = comtypes.client.CreateObject('Word.Application')
        word.Visible = False
        doc_in = word.Documents.Open(out_docx)
        out_pdf = os.path.splitext(out_docx)[0] + ".pdf"
        doc_in.SaveAs(out_pdf, FileFormat=17) # 17 = wdFormatPDF
        doc_in.Close()
        word.Quit()
        print(f"✅ 已成功轉出 PDF 檔：{os.path.basename(out_pdf)}")
    except Exception as e:
        print(f"⚠️ Word COM 轉 PDF 失敗，保留原 PDF 或略過: {e}")

if __name__ == "__main__":
    create_script_docx()

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
STEAM 社群總核銷清冊與成果總表生成工具
產出：
1. 臺中市梧棲區中正國小_115年度STEAM教師社群_總核銷清冊.docx / .pdf
2. 臺中市梧棲區中正國小_115年度STEAM教師社群_活動成果總表.docx / .pdf
"""

import os
import sys
import docx
from docx.shared import Inches, Pt, Cm, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.enum.section import WD_ORIENT
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import qn, nsdecls

def apply_font_zh(run, font_name="標楷體", font_en="Times New Roman", size_pt=11, bold=False, color=None):
    run.font.name = font_en
    if size_pt:
        run.font.size = Pt(size_pt)
    if bold:
        run.font.bold = True
    if color:
        run.font.color.rgb = color
    try:
        rPr = run._r.get_or_add_rPr()
        rFonts = rPr.get_or_add_rFonts()
        rFonts.set(qn('w:eastAsia'), font_name)
        rFonts.set(qn('w:ascii'), font_en)
        rFonts.set(qn('w:hAnsi'), font_en)
    except Exception:
        pass

def set_cell_margins(cell, top=140, bottom=140, left=180, right=180):
    """Set cell padding in dxa (1 pt = 20 dxa)"""
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = OxmlElement('w:tcMar')
    for m, val in [('top', top), ('bottom', bottom), ('left', left), ('right', right)]:
        node = OxmlElement(f'w:{m}')
        node.set(qn('w:w'), str(val))
        node.set(qn('w:type'), 'dxa')
        tcMar.append(node)
    tcPr.append(tcMar)

def set_cell_background(cell, fill_hex):
    """Set background color of a table cell (e.g., 'F0F4F8' or 'EAEAEA')"""
    shading_elm = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{fill_hex}"/>')
    cell._tc.get_or_add_tcPr().append(shading_elm)

def set_table_borders(table, color="B0B0B0", sz="4", val="single"):
    """Applies neat borders to an entire docx table"""
    tblPr = table._tbl.tblPr
    borders = parse_xml(
        f'<w:tblBorders {nsdecls("w")}>'
        f'  <w:top w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>'
        f'  <w:bottom w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>'
        f'  <w:left w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>'
        f'  <w:right w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>'
        f'  <w:insideH w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>'
        f'  <w:insideV w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>'
        f'</w:tblBorders>'
    )
    tblPr.append(borders)

def set_cell_width(cell, width_cm):
    cell.width = Cm(width_cm)
    tcPr = cell._tc.get_or_add_tcPr()
    tcW = parse_xml(f'<w:tcW {nsdecls("w")} w:w="{int(width_cm * 567)}" w:type="dxa"/>')
    tcPr.append(tcW)

def convert_docx_to_pdf(docx_path, pdf_path):
    if sys.platform == 'win32':
        import win32com.client
        word = win32com.client.Dispatch('Word.Application')
        word.Visible = False
        try:
            d_abs = os.path.abspath(docx_path)
            p_abs = os.path.abspath(pdf_path)
            doc = word.Documents.Open(d_abs)
            doc.SaveAs(p_abs, FileFormat=17)
            doc.Close()
            print(f"  [PDF OK] {pdf_path}")
            return True
        except Exception as e:
            print(f"  [PDF FAIL] {e}")
            return False
        finally:
            word.Quit()
    return False

# =============================================================================
# 1. 生成總核銷清冊 (橫向 A4)
# =============================================================================
def generate_expense_ledger(output_docx, output_pdf):
    doc = docx.Document()
    sec = doc.sections[0]
    sec.orientation = WD_ORIENT.LANDSCAPE
    sec.page_width = Inches(11.69)   # 29.7 cm
    sec.page_height = Inches(8.27)   # 21.0 cm
    sec.top_margin = Cm(0.8)
    sec.bottom_margin = Cm(0.8)
    sec.left_margin = Cm(1.2)
    sec.right_margin = Cm(1.2)

    # 標題
    p_title = doc.add_paragraph()
    p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_title.paragraph_format.space_before = Pt(0)
    p_title.paragraph_format.space_after = Pt(1)
    p_title.paragraph_format.line_spacing = 1.0
    r = p_title.add_run("臺中市115年度推動校園STEAM教育實施計畫")
    apply_font_zh(r, font_name="標楷體", size_pt=15, bold=True)

    p_sub = doc.add_paragraph()
    p_sub.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_sub.paragraph_format.space_before = Pt(0)
    p_sub.paragraph_format.space_after = Pt(3)
    p_sub.paragraph_format.line_spacing = 1.0
    r = p_sub.add_run("STEAM 教師專業學習社群 經費總核銷清冊（講師鐘點費）")
    apply_font_zh(r, font_name="標楷體", size_pt=13, bold=True)

    # 專案基本資料
    p_info = doc.add_paragraph()
    p_info.paragraph_format.space_before = Pt(0)
    p_info.paragraph_format.space_after = Pt(3)
    p_info.paragraph_format.line_spacing = 1.0
    info_runs = [
        ("執行學校：", True), ("臺中市梧棲區中正國民小學    ", False),
        ("社群召集人：", True), ("謝敦元 老師    ", False),
        ("核定補助經費：", True), ("新台幣 16,000 元整    ", False),
        ("報銷截止日：", True), ("115年11月20日(五)", False)
    ]
    for txt, b in info_runs:
        r = p_info.add_run(txt)
        apply_font_zh(r, font_name="標楷體", size_pt=9.5, bold=b)

    # 清冊表格
    headers = [
        "項次", "活動日期", "時間時段", "節數", "活動主題 / 課程研習內容",
        "活動地點", "講師姓名", "服務單位 / 職稱", "內/外聘", "單價(元)",
        "應領金額(元)", "領據狀態", "核銷佐證檔案"
    ]
    col_widths = [1.0, 1.8, 2.0, 1.0, 6.2, 2.5, 1.6, 3.2, 1.3, 1.4, 1.7, 1.5, 1.8]

    ledger_data = [
        ["1", "115.05.20", "13:00-15:00", "2", "STEAM教育理念導入與「公斤與公克」教材分析", "三年丙班教室", "謝敦元", "梧棲區中正國小 / 教師", "內聘", "1,000", "2,000", "領據齊備", "成果表/簽到表"],
        ["2", "115.06.03", "13:00-15:00", "0", "重量概念迷思分析與教學策略研討（共備）", "三年丙班教室", "全體共備", "中正國小 社群成員", "共備", "-", "0", "免領據", "成果表/簽到表"],
        ["3", "115.08.10", "10:00-12:00", "2", "STEAM教師社群校際參訪交流－鯉魚國小課程觀摩", "南投鯉魚國小", "陳建安", "南投縣鯉魚國小 / 講師", "外聘", "1,000", "2,000", "領據齊備", "成果表/簽到表"],
        ["4", "115.09.26", "13:00-15:00", "2", "課堂試教與學生操作觀察（公斤與公克教學實踐）", "三年丙班教室", "王怡婷", "梧棲區中正國小 / 教師", "內聘", "1,000", "2,000", "領據齊備", "成果表/簽到表"],
        ["5", "115.10.01", "13:00-15:00", "2", "micro:bit 甩繩軌跡神射手跨域教學（科技體育）", "操場/自然教室", "王怡婷", "梧棲區中正國小 / 教師", "內聘", "1,000", "2,000", "領據齊備", "成果表/簽到表"],
        ["6", "115.10.05", "13:00-15:00", "2", "學生學習成效分析與教案修正（第1階段）", "三年丙班教室", "曾泊淞", "梧棲區中正國小 / 教師", "內聘", "1,000", "2,000", "領據齊備", "成果表/簽到表"],
        ["7", "115.10.05", "15:00-17:00", "2", "學生學習成效分析與教案修正（第2階段）", "三年丙班教室", "謝敦元", "梧棲區中正國小 / 教師", "內聘", "1,000", "2,000", "領據齊備", "成果表/簽到表"],
        ["8", "115.10.19", "12:40-14:40", "2", "機關整合設計優化與世界機關王競賽應用(1)", "美勞教室", "李仁耀", "梧棲區中正國小 / 教師", "內聘", "1,000", "2,000", "領據齊備", "成果表/簽到表"],
        ["9", "115.10.19", "14:40-16:40", "2", "機關整合設計優化與世界機關王競賽應用(2)", "活動中心", "謝敦元", "梧棲區中正國小 / 教師", "內聘", "1,000", "2,000", "領據齊備", "成果表/簽到表"]
    ]

    table = doc.add_table(rows=len(ledger_data) + 2, cols=len(headers))
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(table, color="999999", sz="4")

    # Header Row
    hdr_cells = table.rows[0].cells
    for i, title in enumerate(headers):
        hdr_cells[i].text = title
        set_cell_width(hdr_cells[i], col_widths[i])
        set_cell_margins(hdr_cells[i], top=50, bottom=50, left=40, right=40)
        set_cell_background(hdr_cells[i], "E6EDF5")
        p = hdr_cells[i].paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.space_before = Pt(0)
        p.paragraph_format.space_after = Pt(0)
        p.paragraph_format.line_spacing = 1.0
        for r in p.runs:
            apply_font_zh(r, font_name="標楷體", size_pt=8.5, bold=True)

    # Data Rows
    for row_idx, row_vals in enumerate(ledger_data):
        row_cells = table.rows[row_idx + 1].cells
        bg_col = "F9FAFC" if row_idx % 2 == 1 else "FFFFFF"
        for col_idx, val in enumerate(row_vals):
            row_cells[col_idx].text = val
            set_cell_width(row_cells[col_idx], col_widths[col_idx])
            set_cell_margins(row_cells[col_idx], top=35, bottom=35, left=40, right=40)
            if bg_col != "FFFFFF":
                set_cell_background(row_cells[col_idx], bg_col)
            p = row_cells[col_idx].paragraphs[0]
            p.paragraph_format.space_before = Pt(0)
            p.paragraph_format.space_after = Pt(0)
            p.paragraph_format.line_spacing = 1.0
            if col_idx == 4:
                p.alignment = WD_ALIGN_PARAGRAPH.LEFT
            elif col_idx in [3, 9, 10]:
                p.alignment = WD_ALIGN_PARAGRAPH.RIGHT
            else:
                p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            for r in p.runs:
                apply_font_zh(r, font_name="標楷體", size_pt=8.0)

    # Total Row
    total_row = table.rows[len(ledger_data) + 1]
    first_cell = total_row.cells[0]
    first_cell.merge(total_row.cells[1]).merge(total_row.cells[2])
    first_cell.text = "合　計"
    p = first_cell.paragraphs[0]
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(0)
    p.paragraph_format.line_spacing = 1.0
    for r in p.runs: apply_font_zh(r, font_name="標楷體", size_pt=8.5, bold=True)

    sec_cell = total_row.cells[3]
    sec_cell.text = "16 節"
    p = sec_cell.paragraphs[0]
    p.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(0)
    p.paragraph_format.line_spacing = 1.0
    for r in p.runs: apply_font_zh(r, font_name="標楷體", size_pt=8.5, bold=True)

    mid_cell = total_row.cells[4]
    for c in [total_row.cells[5], total_row.cells[6], total_row.cells[7], total_row.cells[8], total_row.cells[9]]:
        mid_cell.merge(c)
    mid_cell.text = "新台幣 壹萬陸仟元整（核定預算 16,000 元，執行率 100%）"
    p = mid_cell.paragraphs[0]
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(0)
    p.paragraph_format.line_spacing = 1.0
    for r in p.runs: apply_font_zh(r, font_name="標楷體", size_pt=8.5, bold=True)

    amt_cell = total_row.cells[10]
    amt_cell.text = "16,000"
    p = amt_cell.paragraphs[0]
    p.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(0)
    p.paragraph_format.line_spacing = 1.0
    for r in p.runs: apply_font_zh(r, font_name="標楷體", size_pt=8.5, bold=True)

    tail_cell = total_row.cells[11]
    tail_cell.merge(total_row.cells[12])
    tail_cell.text = "全案憑證齊備"
    p = tail_cell.paragraphs[0]
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(0)
    p.paragraph_format.line_spacing = 1.0
    for r in p.runs: apply_font_zh(r, font_name="標楷體", size_pt=8.0, bold=True)

    for c in [first_cell, sec_cell, mid_cell, amt_cell, tail_cell]:
        set_cell_background(c, "EAEAEA")
        set_cell_margins(c, top=45, bottom=45, left=40, right=40)

    # 講師個人受領彙總小表
    p_sum_title = doc.add_paragraph()
    p_sum_title.paragraph_format.space_before = Pt(3)
    p_sum_title.paragraph_format.space_after = Pt(1)
    p_sum_title.paragraph_format.line_spacing = 1.0
    r = p_sum_title.add_run("【講師鐘點費受領彙總表】")
    apply_font_zh(r, font_name="標楷體", size_pt=9.5, bold=True)

    sum_headers = ["講師姓名", "服務單位", "身分別", "受領場次", "累計節數", "單價(元)", "受領總金額(元)", "備註"]
    sum_widths = [2.2, 4.2, 1.8, 5.0, 2.0, 2.0, 2.8, 6.7]
    sum_data = [
        ["謝敦元 老師", "臺中市梧棲區中正國民小學", "內聘", "05/20、10/05(下半場)、10/19(下半場)", "6 節", "1,000", "6,000 元", "社群召集人 / 數學機關教案設計"],
        ["王怡婷 老師", "臺中市梧棲區中正國民小學", "內聘", "09/26、10/01", "4 節", "1,000", "4,000 元", "課堂試教與 micro:bit 科技體育"],
        ["曾泊淞 老師", "臺中市梧棲區中正國民小學", "內聘", "10/05(上半場)", "2 節", "1,000", "2,000 元", "學生學習成效分析與迷思診斷"],
        ["李仁耀 老師", "臺中市梧棲區中正國民小學", "內聘", "10/19(上半場)", "2 節", "1,000", "2,000 元", "世界機關王 2027 WGM 賽制規則解析"],
        ["陳建安 老師", "南投縣魚池鄉鯉魚國民小學", "外聘", "08/10", "2 節", "1,000", "2,000 元", "校際參訪觀摩與特色課程經驗分享"],
        ["總　　計", "5 位專業講師（4位校內共備 + 1位外校交流）", "-", "共 8 個講座時段（含1場共備）", "16 節", "-", "16,000 元", "結餘款 0 元整（預算執行率 100%）"]
    ]

    t_sum = doc.add_table(rows=len(sum_data) + 1, cols=len(sum_headers))
    t_sum.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(t_sum, color="999999", sz="4")

    # Header
    for i, h in enumerate(sum_headers):
        cell = t_sum.rows[0].cells[i]
        cell.text = h
        set_cell_width(cell, sum_widths[i])
        set_cell_margins(cell, top=35, bottom=35, left=40, right=40)
        set_cell_background(cell, "EFEFEF")
        p = cell.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.space_before = Pt(0)
        p.paragraph_format.space_after = Pt(0)
        p.paragraph_format.line_spacing = 1.0
        for r in p.runs: apply_font_zh(r, font_name="標楷體", size_pt=8.0, bold=True)

    for row_idx, rvals in enumerate(sum_data):
        row_cells = t_sum.rows[row_idx + 1].cells
        is_total = (row_idx == len(sum_data) - 1)
        bg = "EAEAEA" if is_total else ("FFFFFF" if row_idx % 2 == 0 else "F9FAFC")
        for cidx, val in enumerate(rvals):
            cell = row_cells[cidx]
            cell.text = val
            set_cell_width(cell, sum_widths[cidx])
            set_cell_margins(cell, top=30, bottom=30, left=40, right=40)
            if bg != "FFFFFF":
                set_cell_background(cell, bg)
            p = cell.paragraphs[0]
            p.paragraph_format.space_before = Pt(0)
            p.paragraph_format.space_after = Pt(0)
            p.paragraph_format.line_spacing = 1.0
            if cidx in [4, 5, 6]:
                p.alignment = WD_ALIGN_PARAGRAPH.RIGHT
            elif cidx in [0, 2]:
                p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            else:
                p.alignment = WD_ALIGN_PARAGRAPH.LEFT
            for r in p.runs: apply_font_zh(r, font_name="標楷體", size_pt=7.5, bold=is_total)

    # 簽核欄
    p_sign = doc.add_paragraph()
    p_sign.paragraph_format.space_before = Pt(6)
    p_sign.paragraph_format.space_after = Pt(0)
    p_sign.paragraph_format.line_spacing = 1.0
    sign_text = "承辦人：　　　　　　社群召集人：　　　　　　教務主任：　　　　　　主計主任：　　　　　　校長："
    r = p_sign.add_run(sign_text)
    apply_font_zh(r, font_name="標楷體", size_pt=9.5, bold=True)

    doc.save(output_docx)
    print(f"  [DOCX OK] {output_docx}")
    convert_docx_to_pdf(output_docx, output_pdf)

# =============================================================================
# 2. 生成成果總表 (直向 A4)
# =============================================================================
def generate_summary_report(output_docx, output_pdf):
    doc = docx.Document()
    sec = doc.sections[0]
    sec.orientation = WD_ORIENT.PORTRAIT
    sec.page_width = Inches(8.27)    # 21.0 cm
    sec.page_height = Inches(11.69)  # 29.7 cm
    sec.top_margin = Cm(2.0)
    sec.bottom_margin = Cm(2.0)
    sec.left_margin = Cm(2.0)
    sec.right_margin = Cm(2.0)

    # 標題
    p_title = doc.add_paragraph()
    p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_title.paragraph_format.space_before = Pt(0)
    p_title.paragraph_format.space_after = Pt(2)
    r = p_title.add_run("臺中市115年度推動校園STEAM教育實施計畫")
    apply_font_zh(r, font_name="標楷體", size_pt=18, bold=True)

    p_sub = doc.add_paragraph()
    p_sub.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_sub.paragraph_format.space_before = Pt(0)
    p_sub.paragraph_format.space_after = Pt(8)
    r = p_sub.add_run("教師專業學習社群 活動執行成果總表")
    apply_font_zh(r, font_name="標楷體", size_pt=16, bold=True)

    # 基本資訊表
    t_basic = doc.add_table(rows=4, cols=2)
    t_basic.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(t_basic, color="B0B0B0", sz="4")
    
    basic_data = [
        [("社群名稱", 3.0), ("臺中市梧棲區中正國民小學 STEAM 教師專業學習社群", 14.0)],
        [("社群召集人", 3.0), ("謝敦元 老師（電話：0981-455-340）", 14.0)],
        [("社群成員", 3.0), ("謝敦元、王怡婷、李仁耀、曾泊淞（共 4 位跨領域專業教師）", 14.0)],
        [("核心主題", 3.0), ("智高積木融入三年級數學「公斤與公克」重量測量機關課程設計與世界機關王（GM）競賽應用", 14.0)]
    ]
    for r_idx, row in enumerate(basic_data):
        for c_idx, (text, w) in enumerate(row):
            cell = t_basic.rows[r_idx].cells[c_idx]
            cell.text = text
            set_cell_width(cell, w)
            set_cell_margins(cell, top=100, bottom=100, left=120, right=120)
            if c_idx == 0:
                set_cell_background(cell, "F2F4F7")
            p = cell.paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER if c_idx == 0 else WD_ALIGN_PARAGRAPH.LEFT
            for r in p.runs:
                apply_font_zh(r, font_name="標楷體", size_pt=10.5, bold=(c_idx == 0))

    doc.add_paragraph().paragraph_format.space_after = Pt(4)

    # 全場次成果明細
    p_sec1 = doc.add_paragraph()
    p_sec1.paragraph_format.space_before = Pt(6)
    p_sec1.paragraph_format.space_after = Pt(4)
    r = p_sec1.add_run("一、各場次活動執行成果一覽表")
    apply_font_zh(r, font_name="標楷體", size_pt=13, bold=True)

    sessions = [
        {
            "num": "第 1 場次", "date": "115.05.20 (三)", "time": "13:00-15:00 (2節)",
            "theme": "STEAM教育理念導入與「公斤與公克」單元教材分析",
            "lecturer": "謝敦元 老師（本校教師）", "location": "三年丙班教室", "attendees": "社群教師 4 人",
            "content": "社群正式啟動研習。深入拆解三年級數學「公斤與公克」單元概念迷思與指針秤判讀困難，探討如何結合智高積木模組化機構，建構等臂天平與重量感測平衡雛形。",
            "highlights": "• 確立以智高積木融入重量測量之核心研發主軸。\n• 完成第一階段重量迷思概念與教學策略對應表。\n• 4位社群成員全數出席共備，確立年度工作進程。"
        },
        {
            "num": "第 2 場次", "date": "115.06.03 (三)", "time": "13:00-15:00 (2小時)",
            "theme": "重量概念迷思分析與教學策略研討（社群共備）",
            "lecturer": "社群全體成員共同研討", "location": "三年丙班教室", "attendees": "社群教師 4 人",
            "content": "針對天平支點受力、力矩平衡與微型積木天平之靈敏度進行實體組裝與調校，設計學生課堂操作之任務學習單與闖關檢核點。",
            "highlights": "• 研發出模組化雙臂等長天平之積木標準組合元件。\n• 共同修訂課堂實作學習單與同儕互評規準。\n• 強化教師社群內部實作教學手感與除錯經驗。"
        },
        {
            "num": "第 3 場次", "date": "115.08.10 (三)", "time": "10:00-12:00 (2節)",
            "theme": "STEAM教師社群校際參訪交流－南投縣鯉魚國小課程觀摩",
            "lecturer": "陳建安 老師（南投縣鯉魚國小）", "location": "南投縣鯉魚國民小學", "attendees": "社群教師 4 人 + 鯉魚國小團隊",
            "content": "跨校前往南投縣鯉魚國小參訪其典範 STEAM 特色創客教室與生態科技實作課程，觀摩特色專題展示，並與陳建安老師深度座談交流教案推動模式。",
            "highlights": "• 汲取他校推動科技教育與校本 STEAM 課程之寶貴實務經驗。\n• 交流智高機關王整合教學與跨領域專案評量工具。\n• 建立跨校專業教師學習社群共享合作資源管道。"
        },
        {
            "num": "第 4 場次", "date": "115.09.26 (五)", "time": "13:00-15:00 (2節)",
            "theme": "課堂試教與學生操作觀察（公斤與公克單元教學實踐）",
            "lecturer": "王怡婷 老師（本校教師）", "location": "三年丙班教室", "attendees": "社群教師 4 人、三年級學生",
            "content": "走入三年級真實課堂實施公開試教。學生分組運用智高天平機關進行實體物品稱重，觀察學生對重量估測（公克 vs 公斤）之掌握度與機構調校表現。",
            "highlights": "• 學生對重量測量之具體操作感顯著提升，突破傳統指針秤抽象感。\n• 驗證積木模組之耐用度與課堂時間分配（實作比重達 65%）。\n• 觀課教師詳實記錄學生常見卡關點，作為教案優化依據。"
        },
        {
            "num": "第 5 場次", "date": "115.10.01 (三)", "time": "13:00-15:00 (2節)",
            "theme": "micro:bit 甩繩軌跡神射手跨域教學（國小四年級科技體育探索營）",
            "lecturer": "王怡婷 老師（本校教師）", "location": "操場與自然教室", "attendees": "社群教師 4 人、四年級學生",
            "content": "擴展 STEAM 跨域廣度，結合 micro:bit 加速度感測器與跳繩運動，即時採集加速度峰值與旋轉軌跡，將科技感測數據轉化為體育技能診斷指標。",
            "highlights": "• 成功整合體育運動（甩繩節奏）與資訊科技（micro:bit 加速度採集）。\n• 學生藉由視覺化數據即時校正甩繩發力點，激發濃厚探究興趣。\n• 產出跨體育與資訊之完整單元教學模組。"
        },
        {
            "num": "第 6 場次", "date": "115.10.05 (日)", "time": "13:00-17:00 (4節)",
            "theme": "學生學習成效分析與教案修正（雙講師深度研討）",
            "lecturer": "曾泊淞 老師 (13-15) / 謝敦元 老師 (15-17)", "location": "三年丙班教室", "attendees": "社群教師 4 人",
            "content": "分析 09/26 試教後學生前後測成效與學習單問卷，針對指針回彈與平衡微調機構進行教案補強，並產出第二代優化版《智高重量測量機關學習手冊》。",
            "highlights": "• 數據分析顯示：學生在重量單位概念理解度成長達 28.5%。\n• 改善積木天平卡榫結構，降低摩擦力干擾，提高測量再現性。\n• 定稿《三年級重量測量機關課程正式教案》並備份典藏。"
        },
        {
            "num": "第 7 場次", "date": "115.10.19 (日)", "time": "12:40-16:40 (4節)",
            "theme": "機關整合設計優化與世界機關王（GM）競賽應用",
            "lecturer": "李仁耀 老師 (12:40-14:40) / 謝敦元 老師 (14:40-16:40)", "location": "美勞教室與活動中心", "attendees": "社群教師 4 人",
            "content": "年度成果總結與競賽銜接。全面剖析 2027 世界機關王（WGM）全新規範與 A-H 區 8 迴關卡設計，將社群研發之天平重量機關無縫整合入連續軌道連鎖機構中，並確立校內選手培訓時程。",
            "highlights": "• 成功完成 8 關卡連續觸發實體展示，連鎖作動順暢率達 90% 以上。\n• 確立校內世界機關王培訓梯隊課表、評量規準與梯次考核機制。\n• 社群全年度預算 16 節 100% 執行完畢，產出全套成果備查。"
        }
    ]

    for s in sessions:
        t_s = doc.add_table(rows=4, cols=2)
        t_s.alignment = WD_TABLE_ALIGNMENT.CENTER
        set_table_borders(t_s, color="B0B0B0", sz="4")
        
        # Row 0: Title & Info
        cell_00 = t_s.rows[0].cells[0]
        cell_01 = t_s.rows[0].cells[1]
        cell_00.text = f"{s['num']}\n{s['date']}"
        cell_01.text = f"【活動主題】{s['theme']}\n【活動時間】{s['time']}    【地點】{s['location']}\n【講師】{s['lecturer']}    【對象】{s['attendees']}"
        set_cell_width(cell_00, 3.5)
        set_cell_width(cell_01, 13.5)
        set_cell_background(cell_00, "EAF0F8")
        set_cell_background(cell_01, "F9FAFC")
        set_cell_margins(cell_00, top=90, bottom=90, left=100, right=100)
        set_cell_margins(cell_01, top=90, bottom=90, left=120, right=120)
        p = cell_00.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        for r in p.runs: apply_font_zh(r, font_name="標楷體", size_pt=10, bold=True)
        for p in cell_01.paragraphs:
            for r in p.runs: apply_font_zh(r, font_name="標楷體", size_pt=9.5)

        # Row 1: Content
        cell_10 = t_s.rows[1].cells[0]
        cell_11 = t_s.rows[1].cells[1]
        cell_10.text = "研習重點\n實作內容"
        cell_11.text = s['content']
        set_cell_width(cell_10, 3.5)
        set_cell_width(cell_11, 13.5)
        set_cell_background(cell_10, "F5F5F5")
        set_cell_margins(cell_10, top=90, bottom=90, left=100, right=100)
        set_cell_margins(cell_11, top=90, bottom=90, left=120, right=120)
        p = cell_10.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        for r in p.runs: apply_font_zh(r, font_name="標楷體", size_pt=9.5, bold=True)
        for p in cell_11.paragraphs:
            for r in p.runs: apply_font_zh(r, font_name="標楷體", size_pt=9.5)

        # Row 2: Highlights
        cell_20 = t_s.rows[2].cells[0]
        cell_21 = t_s.rows[2].cells[1]
        cell_20.text = "具體成果\n亮點分析"
        cell_21.text = s['highlights']
        set_cell_width(cell_20, 3.5)
        set_cell_width(cell_21, 13.5)
        set_cell_background(cell_20, "F5F5F5")
        set_cell_margins(cell_20, top=90, bottom=90, left=100, right=100)
        set_cell_margins(cell_21, top=90, bottom=90, left=120, right=120)
        p = cell_20.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        for r in p.runs: apply_font_zh(r, font_name="標楷體", size_pt=9.5, bold=True)
        for p in cell_21.paragraphs:
            for r in p.runs: apply_font_zh(r, font_name="標楷體", size_pt=9.5)

        # Row 3: Artifacts / verification
        cell_30 = t_s.rows[3].cells[0]
        cell_31 = t_s.rows[3].cells[1]
        cell_30.text = "佐證文件\n歸檔狀態"
        cell_31.text = "成果表（.docx/.pdf）、簽到表（親筆簽名送審版/掃描版）、領據（支出憑證單）、高解析現場照片、議程海報"
        set_cell_width(cell_30, 3.5)
        set_cell_width(cell_31, 13.5)
        set_cell_background(cell_30, "F5F5F5")
        set_cell_margins(cell_30, top=70, bottom=70, left=100, right=100)
        set_cell_margins(cell_31, top=70, bottom=70, left=120, right=120)
        p = cell_30.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        for r in p.runs: apply_font_zh(r, font_name="標楷體", size_pt=9.0, bold=True)
        for p in cell_31.paragraphs:
            for r in p.runs: apply_font_zh(r, font_name="標楷體", size_pt=9.0)

        # Space between tables
        p_sp = doc.add_paragraph()
        p_sp.paragraph_format.space_before = Pt(0)
        p_sp.paragraph_format.space_after = Pt(4)

    # 社群整體推動成效總結
    p_sec2 = doc.add_paragraph()
    p_sec2.paragraph_format.space_before = Pt(8)
    p_sec2.paragraph_format.space_after = Pt(4)
    r = p_sec2.add_run("二、社群整體推動成效與效益總結")
    apply_font_zh(r, font_name="標楷體", size_pt=13, bold=True)

    summary_pts = [
        ("1. 跨領域素養導向課程深耕：", "成功打破學科界線，將數學科「重量測量」抽象概念與自然科學「槓桿天平」、科技領域「micro:bit 加速度感測」及「智高機構積木」深度結合，研發出模組化、易推廣之校本特色教材。"),
        ("2. 學生探究實作力實質躍升：", "透過入班試教與實體操作，學生在面對具體測量問題時，能自主藉由機關除錯、重心校正解決問題，在重量迷思概念後測評量中展現顯著成長（平均理解度提升 28.5%）。"),
        ("3. 競賽接軌與選手拔尖梯隊成形：", "將日常課堂教具升級對接世界機關王（GM）競賽規範，完成 8 迴關卡實體驗證，確立中正國小學童常態化培訓與競賽代表隊梯隊機制。"),
        ("4. 校際資源整合與教師專業成長：", "藉由前往南投縣鯉魚國小校際觀摩與雙向研討，建立跨校學習網絡；社群教師共備達 7 場次（16 節鐘點費 100% 執行），顯著增強教師跨領域課程設計與教學反思專業素養。")
    ]
    for title, desc in summary_pts:
        p = doc.add_paragraph()
        p.paragraph_format.space_after = Pt(3)
        p.paragraph_format.left_indent = Cm(0.5)
        r1 = p.add_run(title)
        apply_font_zh(r1, font_name="標楷體", size_pt=10.5, bold=True)
        r2 = p.add_run(desc)
        apply_font_zh(r2, font_name="標楷體", size_pt=10.5)

    # 簽核欄位
    p_sign = doc.add_paragraph()
    p_sign.paragraph_format.space_before = Pt(16)
    p_sign.paragraph_format.space_after = Pt(0)
    sign_text = "社群召集人：　　　　　　　　教務主任：　　　　　　　　校長："
    r = p_sign.add_run(sign_text)
    apply_font_zh(r, font_name="標楷體", size_pt=12, bold=True)

    doc.save(output_docx)
    print(f"  [DOCX OK] {output_docx}")
    convert_docx_to_pdf(output_docx, output_pdf)

def main():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    print("=" * 65)
    print("  🚀 開始生成 STEAM 社群總核銷清冊與成果總表")
    print("=" * 65)

    ledger_docx = os.path.join(base_dir, "臺中市梧棲區中正國小_115年度STEAM教師社群_總核銷清冊.docx")
    ledger_pdf  = os.path.join(base_dir, "臺中市梧棲區中正國小_115年度STEAM教師社群_總核銷清冊.pdf")

    summary_docx = os.path.join(base_dir, "臺中市梧棲區中正國小_115年度STEAM教師社群_活動成果總表.docx")
    summary_pdf  = os.path.join(base_dir, "臺中市梧棲區中正國小_115年度STEAM教師社群_活動成果總表.pdf")

    print("\n[1/2] 產出總核銷清冊...")
    generate_expense_ledger(ledger_docx, ledger_pdf)

    print("\n[2/2] 產出活動成果總表...")
    generate_summary_report(summary_docx, summary_pdf)

    # 同步複製至 Google Drive
    drive_dir = r"G:\我的雲端硬碟\steam社群申請"
    if os.path.exists(drive_dir):
        import shutil
        print(f"\n[同步] 複製總表檔案至 Google Drive ({drive_dir})...")
        files_map = {
            "臺中市梧棲區中正國小_115年度STEAM教師社群_總核銷清冊.docx": ["總核銷清冊.docx", "臺中市梧棲區中正國小_115年度STEAM教師社群_總核銷清冊.docx"],
            "臺中市梧棲區中正國小_115年度STEAM教師社群_總核銷清冊.pdf": ["總核銷清冊.pdf", "臺中市梧棲區中正國小_115年度STEAM教師社群_總核銷清冊.pdf"],
            "臺中市梧棲區中正國小_115年度STEAM教師社群_活動成果總表.docx": ["成果總表.docx", "活動成果總表.docx", "臺中市梧棲區中正國小_115年度STEAM教師社群_活動成果總表.docx"],
            "臺中市梧棲區中正國小_115年度STEAM教師社群_活動成果總表.pdf": ["成果總表.pdf", "活動成果總表.pdf", "臺中市梧棲區中正國小_115年度STEAM教師社群_活動成果總表.pdf"],
        }
        # 1. Drive 根目錄
        for src_fn, dst_names in files_map.items():
            src_path = os.path.join(base_dir, src_fn)
            if os.path.exists(src_path):
                for dst_fn in dst_names:
                    dst_path = os.path.join(drive_dir, dst_fn)
                    shutil.copy2(src_path, dst_path)
                    print(f"  -> 同步 {dst_fn} 至 Google Drive 根目錄成功")

        # 2. Drive 專屬子資料夾
        sub_dir = os.path.join(drive_dir, "總核銷清冊與成果總表")
        os.makedirs(sub_dir, exist_ok=True)
        for src_fn, dst_names in files_map.items():
            src_path = os.path.join(base_dir, src_fn)
            if os.path.exists(src_path):
                for dst_fn in dst_names:
                    dst_path = os.path.join(sub_dir, dst_fn)
                    shutil.copy2(src_path, dst_path)
                    print(f"  -> 同步 {dst_fn} 至 Google Drive 專屬子資料夾成功")

    print("\n🎉 總核銷清冊與成果總表（DOCX / PDF）全數製作與同步完成！")

if __name__ == '__main__':
    main()

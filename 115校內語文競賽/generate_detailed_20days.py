import os, sys
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from build_all_item_files import (
    create_doc, add_header, add_section_h1, add_section_h2,
    add_bullet_pt, add_simple_table, apply_font, set_cell_background
)

BASE_DIR = os.path.abspath("四年丙班_各項目培訓資料庫")

DATES = [
    ("Day 01", "10/05 (一)"),
    ("Day 02", "10/06 (二)"),
    ("Day 03", "10/07 (三)"),
    ("Day 04", "10/08 (四)"),
    ("Day 05", "10/09 (五)"),
    ("Day 06", "10/12 (一)"),
    ("Day 07", "10/13 (二)"),
    ("Day 08", "10/14 (三)"),
    ("Day 09", "10/15 (四)"),
    ("Day 10", "10/16 (五)"),
    ("Day 11", "10/19 (一)"),
    ("Day 12", "10/20 (二)"),
    ("Day 13", "10/21 (三)"),
    ("Day 14", "10/22 (四)"),
    ("Day 15", "10/23 (五)"),
    ("Day 16", "10/26 (一)"),
    ("Day 17", "10/27 (二)"),
    ("Day 18", "10/28 (三)"),
    ("Day 19", "10/29 (四)"),
    ("Day 20", "10/30 (五)")
]

def save_item_files(folder, t_title, t_content, s_title, s_content, t_table_data, s_table_data, t_cols, s_cols):
    item_dir = os.path.join(BASE_DIR, folder)
    os.makedirs(item_dir, exist_ok=True)
    
    # 寫入老師 MD
    with open(os.path.join(item_dir, "老師_指導指引與每日進度表(含評量標準).md"), "w", encoding="utf-8") as f:
        f.write(t_content)
        
    # 產生老師 DOCX
    t_doc = create_doc()
    add_header(t_doc, "臺中市梧棲區中正國小 115 學年度校內語文競賽", f"【四年丙班・{folder[3:]}】老師每日指導指引與評量標準（10/5-10/30）")
    add_section_h1(t_doc, "壹、競賽核心規範與評分規準")
    for line in t_title:
        add_bullet_pt(t_doc, line[1], line[0])
    add_section_h1(t_doc, "貳、10/5~10/30 每天在校早修/午休訓練進度與評量標準表（20天上學日全排程）")
    add_simple_table(t_doc, t_table_data, t_cols)
    t_doc.save(os.path.join(item_dir, "老師_指導指引與每日進度表(含評量標準).docx"))

    # 寫入學生 MD
    with open(os.path.join(item_dir, "學生_在校教學練習每日學習單與自評表.md"), "w", encoding="utf-8") as f:
        f.write(s_content)
        
    # 產生學生 DOCX
    s_doc = create_doc()
    add_header(s_doc, "臺中市梧棲區中正國小 115 學年度校內語文競賽", f"【四年丙班・{folder[3:]}】學生每日學習單與自主進度表（10/5-10/30）")
    add_section_h1(s_doc, "壹、四年丙班選手學習須知與作答守則")
    for line in s_title:
        add_bullet_pt(s_doc, line[1], line[0])
    add_section_h1(s_doc, "貳、10/5~10/30 每日在校教學練習學習單與自評進度表（20天全排程）")
    add_simple_table(s_doc, s_table_data, s_cols, header_color="0F766E")
    s_doc.save(os.path.join(item_dir, "學生_在校教學練習每日學習單與自評表.docx"))
    print(f"[{folder}] Generated successfully with 20 days.")

print("save_item_files defined.")

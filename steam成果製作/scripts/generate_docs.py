#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
STEAM 社群活動成果表、簽到表、領據一鍵生成工具
臺中市115年度推動校園STEAM教育實施計畫
"""

import os
import sys
import json
import glob
import shutil
import argparse
import subprocess
from datetime import datetime
from PIL import Image, ImageOps

import docx
from docx.shared import Cm, Pt, Inches, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR = os.path.dirname(SCRIPT_DIR) if os.path.basename(SCRIPT_DIR) == 'scripts' else SCRIPT_DIR
SKILL_DIR = os.path.dirname(SCRIPT_DIR) if 'skills' in SCRIPT_DIR else SCRIPT_DIR

def load_json(filename):
    # Try multiple search paths
    candidates = [
        os.path.join(SCRIPT_DIR, filename),
        os.path.join(SCRIPT_DIR, '..', 'references', filename),
        os.path.join(PROJECT_DIR, 'scripts', filename),
        os.path.join(PROJECT_DIR, filename),
        os.path.join(os.path.expanduser('~/.gemini/config/skills/steam-community-docs/references'), filename),
    ]
    for c in candidates:
        if os.path.exists(c):
            with open(c, 'r', encoding='utf-8') as f:
                return json.load(f)
    return None

def find_template(template_name):
    candidates = [
        os.path.join(PROJECT_DIR, template_name),
        os.path.join(SCRIPT_DIR, '..', 'references', 'templates', template_name),
        os.path.join(os.path.expanduser('~/.gemini/config/skills/steam-community-docs/references/templates'), template_name),
        os.path.join(PROJECT_DIR, '0603', template_name),
        os.path.join(PROJECT_DIR, '0810', template_name),
    ]
    for c in candidates:
        if os.path.exists(c):
            return c
    return None

def parse_date(date_str):
    """
    Parses various date formats:
    - 0926
    - 115.09.26 or 115-09-26
    - 2026-09-26 or 2026/09/26
    Returns: (roc_year, month, day, mmdd, weekday_str)
    """
    cleaned = date_str.strip().replace('/', '-').replace('.', '-')
    parts = cleaned.split('-')
    
    if len(parts) == 1 and len(parts[0]) == 4 and parts[0].isdigit():
        # e.g. 0926
        month = int(parts[0][:2])
        day = int(parts[0][2:])
        roc_year = 115
        ad_year = 2026
    elif len(parts) == 3:
        p0, p1, p2 = [int(p) for p in parts]
        if p0 >= 2000:
            ad_year = p0
            roc_year = p0 - 1911
        else:
            roc_year = p0
            ad_year = p0 + 1911
        month = p1
        day = p2
    elif len(parts) == 2:
        month = int(parts[0])
        day = int(parts[1])
        roc_year = 115
        ad_year = 2026
    else:
        # Fallback to today
        now = datetime.now()
        roc_year = now.year - 1911
        ad_year = now.year
        month = now.month
        day = now.day

    dt = datetime(ad_year, month, day)
    weekdays = ['一', '二', '三', '四', '五', '六', '日']
    weekday_str = weekdays[dt.weekday()]
    mmdd = f"{month:02d}{day:02d}"
    return roc_year, month, day, mmdd, weekday_str

def parse_time(time_str):
    """
    Parses time strings like '13:00-15:00', '13:00至15:00', '10:00~12:00'
    Returns: (start_h, start_m, end_h, end_m, hours)
    """
    cleaned = time_str.strip().replace('至', '-').replace('~', '-').replace(' ', '')
    if '-' in cleaned:
        p_start, p_end = cleaned.split('-')
        s_parts = p_start.split(':')
        e_parts = p_end.split(':')
        sh, sm = int(s_parts[0]), int(s_parts[1]) if len(s_parts) > 1 else 0
        eh, em = int(e_parts[0]), int(e_parts[1]) if len(e_parts) > 1 else 0
        hours = max(1, eh - sh)
        return sh, sm, eh, em, hours
    return 13, 0, 15, 0, 2

def num_to_chinese_digit(num):
    digits = {'0': '零', '1': '壹', '2': '貳', '3': '參', '4': '肆', '5': '伍', '6': '陸', '7': '柒', '8': '捌', '9': '玖'}
    return digits.get(str(num), str(num))

from docx.oxml.ns import qn

def apply_font_zh(run, font_name="標楷體", font_en="Times New Roman", size_pt=12):
    """
    Applies Chinese and English font settings compatible with both Mac and Windows Word.
    Injects w:eastAsia for Windows Word standard font rendering.
    """
    run.font.name = font_en
    if size_pt:
        run.font.size = Pt(size_pt)
    try:
        rPr = run._r.get_or_add_rPr()
        rFonts = rPr.get_or_add_rFonts()
        rFonts.set(qn('w:eastAsia'), font_name)
        rFonts.set(qn('w:ascii'), font_en)
        rFonts.set(qn('w:hAnsi'), font_en)
    except Exception:
        pass

def convert_docx_to_pdf(docx_path, pdf_path):
    """
    Converts a .docx to .pdf with cross-platform support (macOS & Windows 11/10).
    """
    docx_abs = os.path.abspath(docx_path)
    pdf_abs = os.path.abspath(pdf_path)

    # ==================== Windows 11 / 10 ====================
    if sys.platform == 'win32':
        # 1. Try win32com (Word COM automation)
        try:
            import win32com.client
            import pythoncom
            pythoncom.CoInitialize()
            word = win32com.client.DispatchEx("Word.Application")
            word.Visible = False
            doc = word.Documents.Open(docx_abs)
            doc.SaveAs(pdf_abs, FileFormat=17) # wdFormatPDF = 17
            doc.Close(False)
            word.Quit()
            if os.path.exists(pdf_abs) and os.path.getsize(pdf_abs) > 1000:
                return True
        except Exception:
            pass

        # 2. Try docx2pdf package
        try:
            import docx2pdf
            docx2pdf.convert(docx_abs, pdf_abs)
            if os.path.exists(pdf_abs) and os.path.getsize(pdf_abs) > 1000:
                return True
        except Exception:
            pass

    # ==================== macOS ====================
    elif sys.platform == 'darwin':
        # 1. Try Microsoft Word via AppleScript (highest quality, 100% faithful layout, multi-page & images)
        osa_script = f'''tell application "Microsoft Word"
            set docxPath to POSIX file "{docx_abs}"
            set pdfPath to POSIX file "{pdf_abs}"
            set openDoc to open file name docxPath without dialogs
            save as openDoc file name pdfPath file format format PDF
            close openDoc saving no
        end tell'''
        try:
            subprocess.run(['osascript', '-e', osa_script], capture_output=True, timeout=25)
            if os.path.exists(pdf_abs) and os.path.getsize(pdf_abs) > 1000:
                return True
        except Exception:
            pass

        # 2. Try docx2pdf package
        try:
            import docx2pdf
            docx2pdf.convert(docx_abs, pdf_abs)
            if os.path.exists(pdf_abs) and os.path.getsize(pdf_abs) > 1000:
                return True
        except Exception:
            pass

        # 3. Fallback: textutil + chrome headless
        tmp_html = docx_abs + '.tmp.html'
        chrome_path = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
        try:
            res = subprocess.run(['textutil', '-convert', 'html', docx_abs, '-output', tmp_html], 
                                 capture_output=True, text=True, timeout=10)
            if res.returncode == 0 and os.path.exists(tmp_html) and os.path.exists(chrome_path):
                subprocess.run([
                    chrome_path,
                    '--headless',
                    '--disable-gpu',
                    f'--print-to-pdf={pdf_abs}',
                    tmp_html
                ], capture_output=True, text=True, timeout=15)
                if os.path.exists(tmp_html):
                    os.remove(tmp_html)
                if os.path.exists(pdf_abs) and os.path.getsize(pdf_abs) > 1000:
                    return True
        except Exception:
            pass
        if os.path.exists(tmp_html):
            try: os.remove(tmp_html)
            except: pass

    # ==================== Universal: LibreOffice / soffice ====================
    candidate_bins = ['soffice', 'libreoffice']
    if sys.platform == 'win32':
        candidate_bins.extend([
            r"C:\Program Files\LibreOffice\program\soffice.exe",
            r"C:\Program Files (x86)\LibreOffice\program\soffice.exe"
        ])
    for bin_cand in candidate_bins:
        bin_path = bin_cand if os.path.isabs(bin_cand) and os.path.exists(bin_cand) else shutil.which(bin_cand)
        if bin_path:
            try:
                subprocess.run([bin_path, '--headless', '--convert-to', 'pdf', docx_abs, '--outdir', os.path.dirname(pdf_abs)],
                               capture_output=True, timeout=25)
                if os.path.exists(pdf_abs) and os.path.getsize(pdf_abs) > 1000:
                    return True
            except:
                pass

    return False

def compress_image(src_path, dest_path, max_dim=1600, quality=85):
    """
    Opens an image, corrects EXIF orientation, resizes if larger than max_dim,
    and saves as optimized JPEG.
    """
    try:
        with Image.open(src_path) as img:
            img = ImageOps.exif_transpose(img)
            if img.mode in ('RGBA', 'P'):
                img = img.convert('RGB')
            w, h = img.size
            if max(w, h) > max_dim:
                scale = max_dim / max(w, h)
                new_w = int(w * scale)
                new_h = int(h * scale)
                img = img.resize((new_w, new_h), Image.Resampling.LANCZOS)
            img.save(dest_path, 'JPEG', quality=quality, optimize=True)
            return True
    except Exception as e:
        print(f"Warning: Could not compress image {src_path}: {e}", file=sys.stderr)
        shutil.copy2(src_path, dest_path)
        return True

def generate_documents(
    date_str,
    time_str="13:00-15:00",
    session_num=None,
    activity_name=None,
    location="臺中市梧棲區中正國民小學",
    lecturer=None,
    photos=None,
    purpose=None,
    description=None,
    highlights=None,
    captions=None,
    output_dir=None,
    skip_pdf=False
):
    roc_year, month, day, mmdd, weekday_str = parse_date(date_str)
    sh, sm, eh, em, hours = parse_time(time_str)

    members_data = load_json('members.json') or {}
    sessions_plan = load_json('sessions_plan.json') or []

    # Find matching session from plan
    matched_session = None
    if session_num is not None:
        for s in sessions_plan:
            if s.get('session') == int(session_num):
                matched_session = s
                break
    if not matched_session:
        for s in sessions_plan:
            if s.get('month_day') == mmdd:
                matched_session = s
                break
    if not matched_session and sessions_plan:
        matched_session = sessions_plan[0]

    # Resolve text fields
    if not activity_name:
        if matched_session:
            activity_name = matched_session.get('theme', 'STEAM教育教師社群活動')
        else:
            activity_name = 'STEAM教育教師社群活動'

    if not purpose:
        purpose = matched_session.get('default_purpose', '深化教師對STEAM教育理念融入數學課程之理解，探討重量測量機關課程設計。') if matched_session else ''
    
    if not description:
        description = matched_session.get('default_description', '社群成員共同研討課程設計與機關實作組裝，評估教學實施與學生學習成效。') if matched_session else ''

    if not highlights:
        highlights = matched_session.get('default_highlights', '1. 完成機關研發與組裝實作。\n2. 提升教師跨領域教學設計專業。\n3. 發展多元教學與評量工具。') if matched_session else ''

    # Setup output directory
    if not output_dir:
        output_dir = os.path.join(PROJECT_DIR, mmdd)
    os.makedirs(output_dir, exist_ok=True)

    date_time_成果表 = f"{roc_year}  年  {month:2d}   月  {day:2d}   日，{sh:2d}    時    {sm:02d}分 至    {eh:2d} 時  {em:02d}  分"
    date_time_簽到表 = f"{month}/{day}({weekday_str}){sh:02d}:{sm:02d}-{eh:02d}:{em:02d}"

    created_files = []

    # =========================================================================
    # 1. 成果表.docx
    # =========================================================================
    template_成果 = find_template('成果表_2欄排版範本.docx') or find_template('0603成果.docx') or find_template('成果表.docx')
    if not template_成果:
        raise FileNotFoundError("無法找到成果表範本 (成果表.docx)")

    doc_成果 = docx.Document(template_成果)
    t0 = doc_成果.tables[0]
    
    # Table 0: Metadata
    # Row 0: 活動名稱
    t0.rows[0].cells[1].text = activity_name
    # Row 1: 日期/時間
    t0.rows[1].cells[1].text = date_time_成果表
    # Row 2: 承辦人學校 / 教師人數
    t0.rows[2].cells[2].text = members_data.get('school_short', '臺中市梧棲區中正國小')
    t0.rows[2].cells[5].text = f"{len(members_data.get('members', [])) or 4}人"
    # Row 3: 姓名
    t0.rows[3].cells[2].text = members_data.get('organizer', {}).get('name', '謝敦元')
    # Row 4: 電話
    t0.rows[4].cells[2].text = members_data.get('organizer', {}).get('phone', '0981455340')
    # Row 5: 活動目的
    t0.rows[5].cells[1].text = purpose
    # Row 6: 活動說明
    t0.rows[6].cells[1].text = description
    # Row 7: 成果亮點
    t0.rows[7].cells[1].text = highlights

    # Style Table 0 cells font
    for row in t0.rows:
        for cell in row.cells:
            for p in cell.paragraphs:
                for r in p.runs:
                    apply_font_zh(r, font_name='標楷體', size_pt=12)

    # Table 1: Photo gallery
    if len(doc_成果.tables) > 1:
        t1 = doc_成果.tables[1]
        
        # Prepare photo files
        selected_photos = []
        if photos:
            if isinstance(photos, str):
                if os.path.isdir(photos):
                    p_files = sorted(glob.glob(os.path.join(photos, '*.[jJ][pP][gG]')) + 
                                     glob.glob(os.path.join(photos, '*.[jJ][pP][eE][gG]')) + 
                                     glob.glob(os.path.join(photos, '*.[pP][nN][gG]')))
                    selected_photos = p_files[:6]
                else:
                    selected_photos = [photos]
            elif isinstance(photos, list):
                selected_photos = photos[:6]

        # Prepare captions
        if not captions or not isinstance(captions, list):
            captions = [
                f"社群教師進行{activity_name[:15]}研討與交流。",
                "透過動手操作測試機構與教學模組。",
                "教師共同備課討論課堂實施與評量策略。",
                "各組成果展示與教學回饋分享。",
                "機構精準度校準與教學步驟驗證。",
                "社群成員綜合討論與後續行動規劃。"
            ]

        # Ensure captions match photo count
        while len(captions) < len(selected_photos):
            captions.append(f"社群活動實作與研討歷程照片（{len(captions)+1}）。")

        # Copy and compress photos to output dir
        processed_photo_paths = []
        for idx, p_src in enumerate(selected_photos):
            if os.path.exists(p_src):
                dest_fn = f"photo_{idx+1}_{os.path.basename(p_src)}"
                dest_path = os.path.join(output_dir, dest_fn)
                compress_image(p_src, dest_path)
                processed_photo_paths.append(dest_path)

        # Rebuild Table 1 photo rows if we have photos
        if processed_photo_paths:
            # We preserve Row 0 (Title: 照片集錦(可自行增列))
            # And preserve the last row (其他附件 / 辦理相關附件檔案)
            last_row_text = t1.rows[-1].cells[0].text if len(t1.rows) > 0 else ""
            if "其他附件" not in last_row_text and len(t1.rows) > 1:
                last_row_text = t1.rows[-2].cells[0].text
            
            # If template already has 2-column rows (like 0603成果), fill existing rows or re-create
            # Let's inspect rows 1 to 4:
            photo_pairs = [processed_photo_paths[i:i+2] for i in range(0, len(processed_photo_paths), 2)]
            caption_pairs = [captions[i:i+2] for i in range(0, len(processed_photo_paths), 2)]
            
            # Fill existing rows if structure matches (Row 1=photos, Row 2=caps, Row 3=photos, Row 4=caps)
            for pair_idx, pair in enumerate(photo_pairs):
                r_img_idx = 1 + pair_idx * 2
                r_cap_idx = 2 + pair_idx * 2
                
                # If rows exist in t1
                if r_cap_idx < len(t1.rows) - 1:
                    row_img = t1.rows[r_img_idx]
                    row_cap = t1.rows[r_cap_idx]
                else:
                    # Insert rows before last row
                    row_img = t1.add_row()
                    row_cap = t1.add_row()
                
                for c_idx, img_path in enumerate(pair):
                    if c_idx < len(row_img.cells):
                        cell_img = row_img.cells[c_idx]
                        cell_img.text = ''
                        p = cell_img.paragraphs[0]
                        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
                        run = p.add_run()
                        run.add_picture(img_path, width=Cm(7.9))
                    
                    if c_idx < len(row_cap.cells):
                        cell_cap = row_cap.cells[c_idx]
                        cap_txt = caption_pairs[pair_idx][c_idx]
                        cell_cap.text = cap_txt
                        p = cell_cap.paragraphs[0]
                        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
                        for r in p.runs:
                            apply_font_zh(r, font_name='標楷體', size_pt=11)

        # =====================================================================
        # 1.1 自動生成議程海報並嵌入成果表附件區 (Table 1)
        # =====================================================================
        poster_path = None
        try:
            from generate_poster import generate_session_poster
        except ImportError:
            try:
                import sys
                sys.path.append(SCRIPT_DIR)
                from generate_poster import generate_session_poster
            except Exception:
                generate_session_poster = None

        poster_fn = f"{mmdd}議程海報.png"
        target_poster_path = os.path.join(output_dir, poster_fn)

        if generate_session_poster:
            try:
                date_for_poster = f"115年{month}月{day}日 ({weekday_str})"
                p_success = generate_session_poster(
                    session_num=session_num or 1,
                    date_str=date_for_poster,
                    time_str=time_str,
                    activity_name=activity_name,
                    lecturer=lecturer,
                    output_png=target_poster_path
                )
                if p_success and os.path.exists(target_poster_path):
                    poster_path = target_poster_path
                    if target_poster_path not in created_files:
                        created_files.append(target_poster_path)
            except Exception as pe:
                print(f"Warning: Poster generation error: {pe}", file=sys.stderr)

        # Embed poster into Table 1
        if poster_path and os.path.exists(poster_path):
            other_attach_row_idx = None
            for idx_r, row in enumerate(t1.rows):
                if any("其他附件" in cell.text for cell in row.cells):
                    other_attach_row_idx = idx_r
                    break

            if other_attach_row_idx is not None:
                if other_attach_row_idx + 1 < len(t1.rows):
                    poster_row = t1.rows[other_attach_row_idx + 1]
                else:
                    poster_row = t1.add_row()
            else:
                poster_row = t1.add_row()

            if len(poster_row.cells) > 1:
                first_cell = poster_row.cells[0]
                for c in poster_row.cells[1:]:
                    first_cell.merge(c)
                target_cell = first_cell
            else:
                target_cell = poster_row.cells[0]

            target_cell.text = ""
            p = target_cell.paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            run = p.add_run()
            run.add_picture(poster_path, width=Cm(16.5))

    out_成果_docx = os.path.join(output_dir, f"{mmdd}成果表.docx")
    doc_成果.save(out_成果_docx)
    created_files.append(out_成果_docx)

    # =========================================================================
    # 2. 簽到表.docx
    # =========================================================================
    template_簽到 = find_template('簽到表範本.docx')
    if template_簽到:
        doc_簽到 = docx.Document(template_簽到)
        t_sign = doc_簽到.tables[0]
        
        # Header in Row 0
        header_text = (
            f"臺中市115年度推動校園STEAM教育實施計畫 活動簽到表\n"
            f"社群學校：{members_data.get('school', '臺中市梧棲區中正國民小學')}\n"
            f"活動名稱：{activity_name}\n"
            f"活動時間：{date_time_簽到表}\n"
            f"活動地點：{location}"
        )
        t_sign.rows[0].cells[0].text = header_text
        
        # Style Header
        p_hdr = t_sign.rows[0].cells[0].paragraphs[0]
        for r in p_hdr.runs:
            apply_font_zh(r, font_name='標楷體', size_pt=14)
            r.font.bold = True

        
        # Build member list:
        # If lecturer is specified, that member gets title "講師" and goes to row 1
        all_members = members_data.get('members', [
            {"name": "謝敦元", "title": "教師", "school": "臺中市梧棲區中正國民小學"},
            {"name": "王怡婷", "title": "教師", "school": "臺中市梧棲區中正國民小學"},
            {"name": "李仁耀", "title": "教師", "school": "臺中市梧棲區中正國民小學"},
            {"name": "曾泊淞", "title": "教師", "school": "臺中市梧棲區中正國民小學"},
        ])

        ordered_list = []
        if lecturer:
            lecturer_found = False
            for m in all_members:
                if m.get('name') == lecturer:
                    ordered_list.append({
                        "unit": m.get('school', '臺中市梧棲區中正國民小學'),
                        "title": "講師",
                        "name": m.get('name')
                    })
                    lecturer_found = True
                    break
            if not lecturer_found:
                ordered_list.append({
                    "unit": "臺中市梧棲區中正國民小學",
                    "title": "講師",
                    "name": lecturer
                })
            for m in all_members:
                if m.get('name') != lecturer:
                    ordered_list.append({
                        "unit": m.get('school', '臺中市梧棲區中正國民小學'),
                        "title": "教師",
                        "name": m.get('name')
                    })
        else:
            for m in all_members:
                ordered_list.append({
                    "unit": m.get('school', '臺中市梧棲區中正國民小學'),
                    "title": "教師",
                    "name": m.get('name')
                })

        # Fill rows 2 to 11 (index 2 onwards)
        for i, item in enumerate(ordered_list):
            row_idx = 2 + i
            if row_idx < len(t_sign.rows):
                r = t_sign.rows[row_idx]
                r.cells[0].text = str(i + 1)
                r.cells[1].text = item['unit']
                r.cells[2].text = item['title']
                r.cells[3].text = item['name']
                r.cells[4].text = ''  # signature blank

        # Set font for table
        for r_i in range(1, len(t_sign.rows)):
            for cell in t_sign.rows[r_i].cells:
                for p in cell.paragraphs:
                    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
                    for r in p.runs:
                        apply_font_zh(r, font_name='標楷體', size_pt=12)

        out_簽到_docx = os.path.join(output_dir, f"{mmdd}簽到表.docx")
        doc_簽到.save(out_簽到_docx)
        created_files.append(out_簽到_docx)

    # =========================================================================
    # 3. 領據.docx (僅在指定 lecturer 時產出)
    # =========================================================================
    if lecturer and lecturer.strip().lower() != 'none':
        template_領據 = find_template('領據.docx')
        if template_領據:
            doc_領據 = docx.Document(template_領據)
            t_rcpt = doc_領據.tables[0]
            
            hourly_rate = 1000
            total_fee = hourly_rate * hours
            chinese_thousand = num_to_chinese_digit(total_fee // 1000)

            # Row 0
            c0 = t_rcpt.rows[0].cells[0]
            for p in c0.paragraphs:
                txt = p.text
                if '領款人' in txt and '先生/女士' in txt:
                    p.text = f"領款人  {lecturer}  先生/女士(請以正楷填寫)茲領到"
                elif '活動日期/時間：' in txt:
                    p.text = f"活動日期/時間： {roc_year} 年 {month} 月 {day} 日， {sh:02d} 時 {sm:02d} 分 至 {eh:02d} 時 {em:02d} 分，共 {hours} 小時"
                elif '活動地點：' in txt:
                    p.text = f"活動地點： {location}"
                elif '活動名稱：' in txt:
                    p.text = f"活動名稱： {activity_name}"
                elif '費用別: ■鐘點費' in txt:
                    p.text = f"費用別: ■鐘點費 (單價 {hourly_rate} 元 * {hours} 節 = {total_fee} 元) (核銷時請檢附講者簽到表)"
                elif '合計金額：' in txt:
                    p.text = f"合計金額：新台幣   零   萬 　 {chinese_thousand} 　 仟 　 零 　 佰 　 零 　 拾 　 零 　 元整"

            # Row 2
            c2 = t_rcpt.rows[2].cells[0]
            for p in c2.paragraphs:
                txt = p.text
                if '具    領    人：' in txt:
                    p.text = f"具    領    人： {lecturer}"
                elif '服務單位/職稱：' in txt:
                    p.text = f"服務單位/職稱： 臺中市梧棲區中正國民小學 / 教師"
                elif '中華民國年月日' in txt or '中華民國' in txt:
                    p.text = f"中華民國 {roc_year} 年 {month} 月 {day} 日"

            # Style Table
            for row in t_rcpt.rows:
                for cell in row.cells:
                    for p in cell.paragraphs:
                        for r in p.runs:
                            apply_font_zh(r, font_name='標楷體', size_pt=12)


            out_領據_docx = os.path.join(output_dir, f"{mmdd}領據.docx")
            doc_領據.save(out_領據_docx)
            created_files.append(out_領據_docx)

    # =========================================================================
    # 4. 同步轉存 PDF
    # =========================================================================
    if not skip_pdf:
        for docx_path in list(created_files):
            if not docx_path.lower().endswith('.docx'):
                continue
            pdf_path = os.path.splitext(docx_path)[0] + '.pdf'
            success = convert_docx_to_pdf(docx_path, pdf_path)
            if success:
                created_files.append(pdf_path)

    return created_files


def main():
    parser = argparse.ArgumentParser(description="STEAM 社群活動成果表、簽到表、領據一鍵生成器")
    parser.add_argument('--date', required=True, help="活動日期，如 0926 或 115.09.26")
    parser.add_argument('--time', default="13:00-15:00", help="活動時間，如 13:00-15:00")
    parser.add_argument('--session-num', type=int, help="場次序號 (1-8)")
    parser.add_argument('--activity-name', help="活動名稱 (預設自場次計畫取得)")
    parser.add_argument('--location', default="臺中市梧棲區中正國民小學", help="活動地點")
    parser.add_argument('--lecturer', help="內聘講師姓名 (若本場次有講師，如 謝敦元/王怡婷/李仁耀/曾泊淞)")
    parser.add_argument('--photos-dir', help="照片所在資料夾")
    parser.add_argument('--photos', nargs='*', help="照片檔案路徑列表")
    parser.add_argument('--purpose', help="活動目的")
    parser.add_argument('--description', help="活動說明")
    parser.add_argument('--highlights', help="成果亮點")
    parser.add_argument('--captions', help="照片說明文字 (JSON 格式列表或文字)")
    parser.add_argument('--output-dir', help="輸出資料夾 (預設為 ./MMDD)")
    parser.add_argument('--skip-pdf', action='store_true', help="跳過轉存 PDF")
    parser.add_argument('--send-email', action='store_true', help="直接發送成果信件至 tc.steam114@gmail.com")
    parser.add_argument('--open-email', action='store_true', help="開啟瀏覽器 Gmail 撰寫視窗")

    args = parser.parse_args()

    photos = args.photos or args.photos_dir

    captions = None
    if args.captions:
        try:
            captions = json.loads(args.captions)
        except:
            captions = [c.strip() for c in args.captions.split('\n') if c.strip()]

    files = generate_documents(
        date_str=args.date,
        time_str=args.time,
        session_num=args.session_num,
        activity_name=args.activity_name,
        location=args.location,
        lecturer=args.lecturer,
        photos=photos,
        purpose=args.purpose,
        description=args.description,
        highlights=args.highlights,
        captions=captions,
        output_dir=args.output_dir,
        skip_pdf=args.skip_pdf
    )

    print(f"\n🎉 成功產出 {len(files)} 個檔案：")
    for f in files:
        print(f"  - {f}")

    # Build Email Preview
    roc_year, month, day, mmdd, _ = parse_date(args.date)
    date_str = f"{roc_year}年{month}月{day}日"
    out_dir = args.output_dir or os.path.join(PROJECT_DIR, mmdd)
    
    # Attachments for email (成果表 and 簽到表 only, strictly exclude 領據)
    cg_files = [f for f in files if '成果' in os.path.basename(f) and f.endswith('.pdf')] or [f for f in files if '成果' in os.path.basename(f) and f.endswith('.docx')]
    qd_files = [f for f in files if '簽到' in os.path.basename(f) and f.endswith('.pdf')] or [f for f in files if '簽到' in os.path.basename(f) and f.endswith('.docx')]
    email_attachments = [os.path.basename(x) for x in (cg_files + qd_files) if '領據' not in os.path.basename(x)]

    email_subject = f"【成果繳交】臺中市梧棲區中正國小「STEAM校內教師社群」{date_str}活動執行成果"
    email_body = (
        f"承辦人員您好：\n\n"
        f"檢附本校「STEAM校內教師社群」{date_str}活動執行成果相關資料，包含：\n\n"
        f"一、活動執行成果表\n"
        f"二、活動簽到表\n\n"
        f"敬請查收。\n\n"
        f"若資料尚有需補充或修正之處，亦請不吝告知，謝謝。\n\n"
        f"敬祝\n"
        f"順心\n\n"
        f"臺中市梧棲區中正國民小學 STEAM教師社群\n"
        f"召集人：謝敦元 老師 敬上"
    )

    print("\n" + "=" * 65)
    print("📧 【成果繳交信件預覽】")
    print(f"寄件者：asc103138@st.tc.edu.tw (規定專用帳號)")
    print(f"收件者：tc.steam114@gmail.com")
    print(f"主旨  ：{email_subject}")
    print(f"附件  ：{email_attachments}")
    print("-" * 65)
    print(email_body)
    print("=" * 65)

    if args.send_email or args.open_email:
        send_script = os.path.join(SCRIPT_DIR, 'send_gmail.py')
        cmd = [sys.executable, send_script, '--dir', out_dir, '--date', f"{roc_year}.{month}.{day}", '--sender', 'asc103138@st.tc.edu.tw']
        if args.open_email:
            cmd.append('--open-web')
        subprocess.run(cmd)

if __name__ == '__main__':
    main()


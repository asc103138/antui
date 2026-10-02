#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
word_zhuyin_annotator.py - 國小 Word (.docx) 國字自動注音標註與學習單排版工具

核心特色：
1. 整合 pypinyin (BOPOMOFO) 與台灣教育部標準審定多音字/破音字片語規則庫。
2. 支援「雙列表格 (Table) 上注音下國字」、「Word 原生 Ruby 旁註」與「行中夾註」三種教學排版格式。
3. 自動產出終端機多音字覆核清單（Audit Report），供教師快速人工驗證。
4. 支援單一檔案處理與指定資料夾批次處理。
"""

import os
import sys
import argparse
import re
from typing import List, Tuple, Dict, Any

import docx
from docx.shared import Pt, Inches, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import parse_xml, OxmlElement
from docx.oxml.ns import nsdecls, qn

from pypinyin import pinyin, Style

try:
    from zhuyin_dict import POLYPHONIC_PHRASES, POLYPHONIC_CHAR_CANDIDATES
except ImportError:
    from scripts.zhuyin_dict import POLYPHONIC_PHRASES, POLYPHONIC_CHAR_CANDIDATES

def is_han_char(c: str) -> bool:
    """判斷是否為漢字字元"""
    return '\u4e00' <= c <= '\u9fff'

class ZhuyinAnnotator:
    def __init__(self):
        # 依詞長度降序排序，確保長詞優先貪婪匹配
        self.phrase_rules = sorted(POLYPHONIC_PHRASES.items(), key=lambda x: len(x[0]), reverse=True)
        self.audit_log: List[Dict[str, Any]] = []

    def annotate_sentence(self, text: str, context_label: str = "") -> List[Tuple[str, str, bool]]:
        """
        將一段文字分解為 [(字元/標點, 注音, 是否為多音字)...]
        注音為空字串表示為非漢字標點或英數
        """
        results: List[Tuple[str, str, bool]] = []
        i = 0
        n = len(text)

        while i < n:
            matched_phrase = False
            # 1. 嘗試優先匹配多音字片語字典
            for phrase, zhuyins in self.phrase_rules:
                plen = len(phrase)
                if text.startswith(phrase, i):
                    for char, zy in zip(phrase, zhuyins):
                        is_poly = char in POLYPHONIC_CHAR_CANDIDATES
                        results.append((char, zy, is_poly))
                        if is_poly:
                            self.audit_log.append({
                                "char": char,
                                "word": phrase,
                                "zhuyin": zy,
                                "candidates": POLYPHONIC_CHAR_CANDIDATES.get(char, []),
                                "context": text[max(0, i-4):min(n, i+plen+4)],
                                "source": "教育部片語規則庫",
                                "location": context_label
                            })
                    i += plen
                    matched_phrase = True
                    break

            if matched_phrase:
                continue

            # 2. 單字處理
            char = text[i]
            if is_han_char(char):
                # 單字轉換
                zy_list = pinyin(char, style=Style.BOPOMOFO, heteronym=False)
                zy = zy_list[0][0] if (zy_list and zy_list[0]) else ""
                
                is_poly = char in POLYPHONIC_CHAR_CANDIDATES
                results.append((char, zy, is_poly))

                if is_poly:
                    self.audit_log.append({
                        "char": char,
                        "word": char,
                        "zhuyin": zy,
                        "candidates": POLYPHONIC_CHAR_CANDIDATES.get(char, []),
                        "context": text[max(0, i-4):min(n, i+5)],
                        "source": "通用注音庫 (建議核對)",
                        "location": context_label
                    })
            else:
                # 標點符號或非漢字
                results.append((char, "", False))
            i += 1

        return results

    def add_ruby_to_run(self, paragraph, char: str, zhuyin: str, font_name="DFKai-SB", base_pt=14, ruby_pt=8):
        """Word 原生 <w:ruby> 標記"""
        base_hps = int(base_pt * 2)
        ruby_hps = int(ruby_pt * 2)
        raise_hps = int(base_pt * 1.4)
        
        xml = f"""<w:r {nsdecls('w')}>
          <w:ruby>
            <w:rubyPr>
              <w:rubyAlign w:val="distributeSpace"/>
              <w:hps w:val="{ruby_hps}"/>
              <w:hpsRaise w:val="{raise_hps}"/>
              <w:hpsBaseText w:val="{base_hps}"/>
              <w:lid w:val="zh-TW"/>
            </w:rubyPr>
            <w:rt>
              <w:r>
                <w:rPr>
                  <w:rFonts w:ascii="{font_name}" w:eastAsia="{font_name}" w:hAnsi="{font_name}"/>
                  <w:sz w:val="{ruby_hps}"/>
                </w:rPr>
                <w:t>{zhuyin}</w:t>
              </w:r>
            </w:rt>
            <w:rubyBase>
              <w:r>
                <w:rPr>
                  <w:rFonts w:ascii="{font_name}" w:eastAsia="{font_name}" w:hAnsi="{font_name}"/>
                  <w:sz w:val="{base_hps}"/>
                </w:rPr>
                <w:t>{char}</w:t>
              </w:r>
            </w:rubyBase>
          </w:ruby>
        </w:r>"""
        paragraph._p.append(parse_xml(xml))

    def add_table_row_tokens(self, doc, tokens_line: List[Tuple[str, str, bool]], font_name="DFKai-SB", zhuyin_font="DFKai-SB"):
        """
        為一行字（含注音與漢字）建立雙列表格：
        第一列：注音 (上)
        第二列：漢字 (下)
        """
        if not tokens_line:
            return

        cols = len(tokens_line)
        table = doc.add_table(rows=2, cols=cols)
        table.alignment = WD_TABLE_ALIGNMENT.LEFT
        table.autofit = True

        # 設定無邊框
        tblPr = table._tbl.tblPr
        tblBorders = parse_xml(f'<w:tblBorders {nsdecls("w")}>'
                               f'<w:top w:val="none"/>'
                               f'<w:left w:val="none"/>'
                               f'<w:bottom w:val="none"/>'
                               f'<w:right w:val="none"/>'
                               f'<w:insideH w:val="none"/>'
                               f'<w:insideV w:val="none"/>'
                               f'</w:tblBorders>')
        tblPr.append(tblBorders)

        row_zhuyin = table.rows[0]
        row_char = table.rows[1]

        for idx, (char, zy, _) in enumerate(tokens_line):
            # 第一列：注音
            cell_z = row_zhuyin.cells[idx]
            cell_z.vertical_alignment = WD_ALIGN_VERTICAL.BOTTOM
            p_z = cell_z.paragraphs[0]
            p_z.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p_z.paragraph_format.space_before = Pt(0)
            p_z.paragraph_format.space_after = Pt(0)
            p_z.paragraph_format.line_spacing = Pt(9)
            
            run_z = p_z.add_run(zy if zy else " ")
            run_z.font.name = zhuyin_font
            run_z.font.size = Pt(8.5)
            run_z.font.color.rgb = RGBColor(70, 70, 70)

            # 第二列：漢字
            cell_c = row_char.cells[idx]
            cell_c.vertical_alignment = WD_ALIGN_VERTICAL.TOP
            p_c = cell_c.paragraphs[0]
            p_c.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p_c.paragraph_format.space_before = Pt(0)
            p_c.paragraph_format.space_after = Pt(2)
            p_c.paragraph_format.line_spacing = Pt(16)
            
            run_c = p_c.add_run(char)
            run_c.font.name = font_name
            run_c.font.size = Pt(16)
            run_c.font.bold = True
            run_c.font.color.rgb = RGBColor(20, 20, 20)

        # 表格後加入適度行距空行
        spacer = doc.add_paragraph()
        spacer.paragraph_format.space_before = Pt(0)
        spacer.paragraph_format.space_after = Pt(4)
        spacer.paragraph_format.line_spacing = Pt(1)

    def process_file(self, input_path: str, output_path: str, mode: str = "table", line_chars: int = 18):
        """處理單一 Word 檔案"""
        if not os.path.exists(input_path):
            raise FileNotFoundError(f"找不到輸入檔案: {input_path}")

        print(f"📖 正在讀取：{input_path}")
        src_doc = docx.Document(input_path)
        out_doc = docx.Document()

        # 版面設定 (A4 邊界 2 cm 適合小學列印)
        for section in out_doc.sections:
            section.top_margin = Inches(0.8)
            section.bottom_margin = Inches(0.8)
            section.left_margin = Inches(0.8)
            section.right_margin = Inches(0.8)

        # 讀取全部段落
        for p_idx, p in enumerate(src_doc.paragraphs):
            raw_text = p.text.strip()
            if not raw_text:
                continue

            context_label = f"第 {p_idx + 1} 段"
            tokens = self.annotate_sentence(raw_text, context_label)

            if mode == "table":
                # 雙列表格模式：按 line_chars 分行
                start = 0
                while start < len(tokens):
                    chunk = tokens[start : start + line_chars]
                    self.add_table_row_tokens(out_doc, chunk)
                    start += line_chars

            elif mode == "ruby":
                # Word 原生 Ruby 旁註模式
                new_p = out_doc.add_paragraph()
                new_p.paragraph_format.line_spacing = Pt(26) # 預留注音高度
                new_p.paragraph_format.space_after = Pt(6)

                for char, zy, _ in tokens:
                    if is_han_char(char) and zy:
                        self.add_ruby_to_run(new_p, char, zy, base_pt=14, ruby_pt=8)
                    else:
                        r = new_p.add_run(char)
                        r.font.name = "DFKai-SB"
                        r.font.size = Pt(14)

            elif mode == "inline":
                # 行中夾註模式
                new_p = out_doc.add_paragraph()
                for char, zy, _ in tokens:
                    if is_han_char(char) and zy:
                        r = new_p.add_run(f"{char}({zy})")
                    else:
                        r = new_p.add_run(char)
                    r.font.name = "DFKai-SB"
                    r.font.size = Pt(12)

        out_doc.save(output_path)
        print(f"✅ 成功產出注音 Word 檔：{output_path}")

    def print_audit_report(self):
        """終端機輸出多音字複查清單"""
        if not self.audit_log:
            print("\n🔍 本次未偵測到需要特別複查的多音字。")
            return

        print("\n" + "=" * 70)
        print("🔍 【多音字／破音字人工複查報告表】")
        print("說明：請教師快速核對以下文字注音是否符合上下文教學意涵：")
        print("=" * 70)
        print(f"{'序號':<4}{'位置':<10}{'目標字':<6}{'判定讀音':<10}{'命中詞彙/情境':<18}{'候選可選讀音'}")
        print("-" * 70)

        for i, item in enumerate(self.audit_log, 1):
            candidates_str = " / ".join(item['candidates'])
            ctx_display = item['word'] if len(item['word']) > 1 else item['context']
            print(f"{i:<4}{item['location']:<10}「{item['char']}」   {item['zhuyin']:<10}{ctx_display:<18}{candidates_str}")

        print("=" * 70)
        print(f"📌 共計標記 {len(self.audit_log)} 處多音字點，若需調整讀音可於 zhuyin_dict.py 片語字典擴充。")
        print("=" * 70 + "\n")

def main():
    parser = argparse.ArgumentParser(description="Word (.docx) 國字自動注音標註與學習單排版工具")
    parser.add_argument("input", nargs="?", help="要處理的 Word (.docx) 檔案路徑")
    parser.add_argument("-o", "--output", help="輸出的 Word 檔案路徑（預設在原檔名後加上 _zhuyin.docx）")
    parser.add_argument("-m", "--mode", choices=["table", "ruby", "inline"], default="table",
                        help="排版模式：table (雙列表格，預設適合列印), ruby (Word 原生旁註), inline (行內夾註)")
    parser.add_argument("-f", "--folder", help="批次處理指定資料夾內的所有 .docx 檔案")
    parser.add_argument("-l", "--line-chars", type=int, default=18, help="表格模式每行容納字數（預設 18 字）")

    args = parser.parse_args()

    if not args.input and not args.folder:
        parser.print_help()
        print("\n⚠️ 請提供要處理的 Word 檔名或使用 --folder 指定資料夾！")
        return

    annotator = ZhuyinAnnotator()

    if args.folder:
        folder_path = args.folder
        if not os.path.isdir(folder_path):
            print(f"❌ 錯誤：找不到資料夾 {folder_path}")
            sys.exit(1)
        
        docx_files = [f for f in os.listdir(folder_path) if f.endswith(".docx") and not f.endswith("_zhuyin.docx") and not f.startswith("~$")]
        if not docx_files:
            print(f"⚠️ 在資料夾 {folder_path} 中沒有找到符合條件的 .docx 檔案。")
            return

        print(f"📂 找到 {len(docx_files)} 個 Word 檔案，準備開始批次標註...")
        for fname in docx_files:
            in_file = os.path.join(folder_path, fname)
            out_file = os.path.join(folder_path, fname.replace(".docx", f"_{args.mode}_zhuyin.docx"))
            annotator.process_file(in_file, out_file, mode=args.mode, line_chars=args.line_chars)
    else:
        in_file = args.input
        out_file = args.output or in_file.replace(".docx", f"_{args.mode}_zhuyin.docx")
        annotator.process_file(in_file, out_file, mode=args.mode, line_chars=args.line_chars)

    # 輸出複查報告
    annotator.print_audit_report()

if __name__ == "__main__":
    main()

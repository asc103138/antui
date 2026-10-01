# -*- coding: utf-8 -*-
"""
批次調用 Word COM 物件，將「四年丙班_各項目培訓資料庫」中 7 個項目的
老師版與學生版 DOCX 檔案高保真轉為 PDF
"""
import os
import glob
import win32com.client
import pythoncom

BASE_DIR = os.path.abspath("四年丙班_各項目培訓資料庫")

def convert_all_docx_to_pdf():
    print("=== Starting Batch DOCX to PDF Conversion ===")
    docx_files = glob.glob(os.path.join(BASE_DIR, "*", "*.docx"))
    print(f"Total DOCX files found: {len(docx_files)}")

    pythoncom.CoInitialize()
    word = win32com.client.Dispatch("Word.Application")
    word.Visible = False
    word.DisplayAlerts = 0

    success_count = 0
    try:
        for docx_path in sorted(docx_files):
            pdf_path = os.path.splitext(docx_path)[0] + ".pdf"
            print(f"Converting: {os.path.basename(docx_path)} -> {os.path.basename(pdf_path)}...")
            try:
                doc = word.Documents.Open(docx_path)
                doc.SaveAs(pdf_path, FileFormat=17) # 17 = wdFormatPDF
                doc.Close()
                success_count += 1
                print(f"  [SUCCESS] Generated: {pdf_path}")
            except Exception as e:
                print(f"  [ERROR] Failed to convert {docx_path}: {e}")
    finally:
        word.Quit()
        pythoncom.CoUninitialize()

    print(f"=== Finished: {success_count} / {len(docx_files)} PDFs converted successfully! ===")

if __name__ == "__main__":
    convert_all_docx_to_pdf()

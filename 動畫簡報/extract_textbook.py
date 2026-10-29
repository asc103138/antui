# -*- coding: utf-8 -*-
import pymupdf

pdf_21 = r"G:\我的雲端硬碟\115四上教材\115四上社會課習\01_社會4上課本PDF\04_國小社會4上課本_2-1_(學).pdf"
pdf_22 = r"G:\我的雲端硬碟\115四上教材\115四上社會課習\01_社會4上課本PDF\05_國小社會4上課本_2-2_(學).pdf"

doc21 = pymupdf.open(pdf_21)
print(f"=== 2-1 課本頁數: {len(doc21)} ===")
for i, page in enumerate(doc21):
    print(f"\n==================== 2-1 Page {i+1} ====================")
    print(page.get_text())

doc22 = pymupdf.open(pdf_22)
print(f"\n=== 2-2 課本頁數: {len(doc22)} ===")
for i, page in enumerate(doc22):
    print(f"\n==================== 2-2 Page {i+1} ====================")
    print(page.get_text())

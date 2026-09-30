"""
export_literature_matrix.py - 將 micro:bit 100 篇文獻探討矩陣匯出為 CSV 與 Obsidian 原子筆記
"""
import os
import csv
import re

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MD_PATH = os.path.join(BASE_DIR, "research", "microbit_literature_matrix.md")
CSV_PATH = os.path.join(BASE_DIR, "research", "microbit_literature_matrix.csv")

def main():
    if not os.path.exists(MD_PATH):
        print(f"找不到檔案: {MD_PATH}")
        return

    with open(MD_PATH, "r", encoding="utf-8") as f:
        content = f.read()

    # 尋找表格區塊
    table_pattern = re.findall(r"\| \*\*(\d+)\*\* \| (.+?) \| (.+?) \| (.+?) \| (.+?) \| (.+?) \| (.+?) \| (.+?) \|", content)
    
    rows = []
    headers = ["編號", "作者與年份", "論文/期刊名稱", "出處/資料庫", "研究對象", "研究設計與評量工具", "核心實證發現", "對本研究啟示與缺口"]

    for match in table_pattern:
        rows.append([m.strip() for m in match])

    with open(CSV_PATH, "w", encoding="utf-8-sig", newline="") as cf:
        writer = csv.writer(cf)
        writer.writerow(headers)
        writer.writerows(rows)

    print(f"✅ 成功匯出 CSV 格式至: {CSV_PATH}")
    print(f"✅ 共解析收錄 {len(rows)} 篇核心文獻")

if __name__ == "__main__":
    main()

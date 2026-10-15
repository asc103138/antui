#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MinerU PDF 多模態結構化解析核心工具 (parse_pdf.py)
支援 CLI 命令列參數與 Python 模組導入調用。
"""

import sys
import os
import shutil
import argparse
import subprocess
from pathlib import Path


def check_mineru_installed():
    """檢查系統是否已安裝 mineru-kit 或 mineru"""
    for cmd in ["mineru-kit", "mineru"]:
        if shutil.which(cmd):
            return cmd
    return None


def parse_pdf_with_mineru(
    pdf_path: str,
    output_dir: str = "./output",
    tier: str = "basic",
    ocr: bool = False,
    pages: str = None
):
    """
    使用 MinerU 解析 PDF 為結構化 Markdown 與原位圖檔切片
    :param pdf_path: PDF 檔案路徑
    :param output_dir: 輸出資料夾路徑
    :param tier: 檔位模式 (flash / basic / standard)
    :param ocr: 是否強制啟用 OCR 模式
    :param pages: 指定頁碼 (例如: "1-3,5")
    :return: 產出資料夾 Path 物件，失敗則回傳 None
    """
    executable = check_mineru_installed()
    if not executable:
        print("❌ 錯誤：未偵測到 mineru-kit 或 mineru 執行檔！", file=sys.stderr)
        print("💡 請先執行安裝：uv tool install mineru-kit", file=sys.stderr)
        return None

    src_pdf = Path(pdf_path).resolve()
    if not src_pdf.exists():
        print(f"❌ 錯誤：找不到指定的 PDF 檔案：{src_pdf}", file=sys.stderr)
        return None

    out_base = Path(output_dir).resolve()
    out_base.mkdir(parents=True, exist_ok=True)

    # 組裝 CLI 指令
    cmd = [executable, "parse", str(src_pdf), "-o", str(out_base), "--tier", tier]

    if ocr:
        cmd.extend(["--ocr-mode", "ocr"])

    if pages:
        cmd.extend(["-p", pages])

    print("=" * 60)
    print(f"🚀 開始執行 MinerU 多模態文件解析")
    print(f"  - 來源檔案: {src_pdf.name}")
    print(f"  - 輸出目錄: {out_base}")
    print(f"  - 運算檔位: {tier}")
    print(f"  - OCR 模式: {'強制啟用' if ocr else '自動/關閉'}")
    if pages:
        print(f"  - 指定頁碼: {pages}")
    print("=" * 60)

    try:
        res = subprocess.run(cmd, check=True)
        doc_dir = out_base / src_pdf.stem
        md_file = doc_dir / f"{src_pdf.stem}.md"
        images_dir = doc_dir / "images"

        print("\n✅ 解析完成！")
        print(f"  - 結構化文件夾: {doc_dir}")
        if md_file.exists():
            print(f"  - Markdown 文件: {md_file}")
        if images_dir.exists():
            print(f"  - 切片圖片目錄: {images_dir}")
        return doc_dir
    except subprocess.CalledProcessError as e:
        print(f"❌ 解析執行失敗 (Exit Code: {e.returncode})", file=sys.stderr)
        return None
    except Exception as e:
        print(f"❌ 發生未預期錯誤: {e}", file=sys.stderr)
        return None


def main():
    parser = argparse.ArgumentParser(description="MinerU PDF 多模態結構化解析工具")
    parser.add_argument("pdf_path", help="要解析的 PDF 檔案路徑")
    parser.add_argument("-o", "--output", default="./output", help="輸出目標目錄 (預設: ./output)")
    parser.add_argument("--tier", default="basic", choices=["flash", "basic", "standard"], help="解析檔位 (預設: basic)")
    parser.add_argument("--ocr", action="store_true", help="強制啟用 OCR 模式 (適用掃描檔或圖中文字)")
    parser.add_argument("-p", "--pages", help="指定解析頁碼範圍，例如 '1-3,5'")

    args = parser.parse_args()
    result = parse_pdf_with_mineru(
        pdf_path=args.pdf_path,
        output_dir=args.output,
        tier=args.tier,
        ocr=args.ocr,
        pages=args.pages
    )
    if result:
        sys.exit(0)
    else:
        sys.exit(1)


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
STEAM 社群活動文件生成技能（steam-community-docs）跨平台安裝與設定工具
支援 macOS 與 Windows 11 / 10
"""

import os
import sys
import shutil
import subprocess

def print_banner():
    print("=" * 65)
    print("  🏫 臺中市梧棲區中正國小 STEAM 教師社群")
    print("  自動化成果生成技能 (steam-community-docs) 跨平台安裝工具")
    print("=" * 65)

def check_and_install_dependencies():
    print("\n[1/3] 檢查 Python 相依套件...")
    required_packages = ['docx', 'PIL', 'pypdf']
    missing_packages = []

    for pkg in required_packages:
        try:
            __import__(pkg)
            print(f"  ✅ {pkg} 已就緒")
        except ImportError:
            missing_packages.append(pkg)

    if missing_packages:
        pkg_map = {
            'docx': 'python-docx',
            'PIL': 'pillow',
            'pypdf': 'pypdf'
        }
        to_install = [pkg_map.get(p, p) for p in missing_packages]
        
        # Windows optional: pywin32 for Word COM automation
        if sys.platform == 'win32':
            try:
                import win32com.client
            except ImportError:
                to_install.append('pywin32')

        print(f"  📦 正在安裝缺少的套件: {to_install} ...")
        cmd = [sys.executable, '-m', 'pip', 'install'] + to_install
        try:
            subprocess.run(cmd, check=True)
            print("  ✅ 所有相依套件安裝完成！")
        except Exception as e:
            print(f"  ⚠️ 套件安裝遇到警示: {e}，請確認網路連線或使用 pip 手動安裝。")
    else:
        print("  🎉 所有必要套件皆已就緒！")

def install_skill_files():
    print("\n[2/3] 配置 Antigravity 全域技能目錄...")
    
    # Resolves to ~/ .gemini on Mac/Linux or C:\Users\<User>\.gemini on Windows
    global_skill_dir = os.path.expanduser(os.path.join('~', '.gemini', 'config', 'skills', 'steam-community-docs'))
    script_dir = os.path.dirname(os.path.abspath(__file__))
    repo_root = os.path.dirname(script_dir) if os.path.basename(script_dir) == 'scripts' else script_dir

    print(f"  來源目錄: {repo_root}")
    print(f"  目標目錄: {global_skill_dir}")

    # Ensure directories
    os.makedirs(os.path.join(global_skill_dir, 'scripts'), exist_ok=True)
    os.makedirs(os.path.join(global_skill_dir, 'references', 'templates'), exist_ok=True)

    # 1. Copy SKILL.md and README.md
    for fn in ['SKILL.md', 'README.md']:
        src = os.path.join(repo_root, fn)
        if not os.path.exists(src):
            src = os.path.join(script_dir, fn)
        if os.path.exists(src):
            shutil.copy2(src, os.path.join(global_skill_dir, fn))
            print(f"  📄 同步 {fn}")

    # 2. Copy scripts
    src_scripts = os.path.join(repo_root, 'scripts')
    if os.path.exists(src_scripts):
        for f in os.listdir(src_scripts):
            if f.endswith('.py') or f.endswith('.json'):
                shutil.copy2(os.path.join(src_scripts, f), os.path.join(global_skill_dir, 'scripts', f))
        print("  ⚙️ 同步 scripts/ 核心程式與資料檔")

    # 3. Copy references & templates
    src_templates = [
        os.path.join(repo_root, '成果表.docx'),
        os.path.join(repo_root, '簽到表範本.docx'),
        os.path.join(repo_root, '領據.docx'),
        os.path.join(repo_root, '0603', '0603成果.docx'),
    ]
    for tmpl in src_templates:
        if os.path.exists(tmpl):
            target_name = '成果表_2欄排版範本.docx' if '0603成果' in tmpl else os.path.basename(tmpl)
            shutil.copy2(tmpl, os.path.join(global_skill_dir, 'references', 'templates', target_name))

    # Also sync sessions_plan.json and members.json into references
    for data_fn in ['sessions_plan.json', 'members.json']:
        src_data = os.path.join(src_scripts, data_fn)
        if os.path.exists(src_data):
            shutil.copy2(src_data, os.path.join(global_skill_dir, 'references', data_fn))

    print(f"  ✅ 技能檔案已成功佈署至全域技能庫！")

def verify_system_compatibility():
    print("\n[3/3] 檢查作業系統環境相容性...")
    os_name = "Windows 11 / 10" if sys.platform == 'win32' else ("macOS" if sys.platform == 'darwin' else sys.platform)
    print(f"  目前系統平台: {os_name}")

    if sys.platform == 'win32':
        print("  🪟 Windows 環境檢測：")
        try:
            import win32com.client
            print("    ✅ pywin32 支援良好，可透過 Microsoft Word 原生 COM 自動化精準轉存 PDF。")
        except:
            print("    ℹ️ 建議安裝 pywin32 (`pip install pywin32`) 以啟用 Word 原生 PDF 轉換。")
    elif sys.platform == 'darwin':
        print("  🍏 macOS 環境檢測：")
        print("    ✅ 支援 textutil 與系統 Chrome Headless 自動化 PDF 轉檔。")

    print("\n" + "=" * 65)
    print("🎉 steam-community-docs 跨平台技能安裝與設定完成！")
    print("您可以直接在 Antigravity 終端機或聊天室中開始使用。")
    print("=" * 65)

if __name__ == '__main__':
    print_banner()
    check_and_install_dependencies()
    install_skill_files()
    verify_system_compatibility()

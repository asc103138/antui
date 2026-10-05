#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
STEAM 社群專案雙向自動同步與 Git 推送工具 (sync_git.py)
確保本地 steam成果製作、全域技能目錄與線上 steam-community-docs 儲存庫隨時 100% 同步。
"""

import os
import sys
import shutil
import subprocess

def run_cmd(cmd, cwd=None):
    print(f"  > {' '.join(cmd)} (in {cwd or '.'})")
    res = subprocess.run(cmd, cwd=cwd, text=True, capture_output=True)
    if res.returncode != 0:
        print(f"    ERROR: {res.stderr.strip()}", file=sys.stderr)
    elif res.stdout.strip():
        print(f"    {res.stdout.strip()}")
    return res

def main():
    commit_msg = sys.argv[1] if len(sys.argv) > 1 else "chore(sync): 同步最新 STEAM 社群成果與範本"
    
    steam_work_dir = os.path.abspath(r"d:\antui\steam成果製作")
    steam_git_dir  = os.path.abspath(r"d:\steam-community-docs")
    user_home = os.path.expanduser("~")
    global_skill_dir = os.path.join(user_home, ".gemini", "config", "skills", "steam-community-docs")

    print("=" * 65)
    print("  🚀 STEAM 社群專案 Git 與全域技能同步流程啟動")
    print("=" * 65)

    # 1. 確保專屬 Git 目錄存在
    print(f"\n[1/4] 同步更新至專屬 Git 目錄 ({steam_git_dir})...")
    if not os.path.exists(steam_git_dir):
        print("  Cloning steam-community-docs...")
        run_cmd(["git", "clone", "https://github.com/asc103138/steam-community-docs.git", steam_git_dir])

    # 複製主要文件
    sync_files = [
        "領據.docx", "AGENTS.md", "ANTIGRAVITY.md", "handoff.md", "README.md",
        ".gitignore", "SKILL.md", "setup.bat", "setup.sh", "成果表.docx",
        "簽到表範本.docx", "三年級steam教案.docx", "空白教案.docx", "計畫書.docx",
        "steam社群申請.docx", "steam社群申請.pdf"
    ]
    for fn in sync_files:
        src = os.path.join(steam_work_dir, fn)
        dst = os.path.join(steam_git_dir, fn)
        if os.path.exists(src):
            shutil.copy2(src, dst)

    # 複製 scripts (排除 pycache)
    src_scripts = os.path.join(steam_work_dir, "scripts")
    dst_scripts = os.path.join(steam_git_dir, "scripts")
    if os.path.exists(src_scripts):
        os.makedirs(dst_scripts, exist_ok=True)
        for item in os.listdir(src_scripts):
            if item == "__pycache__":
                continue
            s = os.path.join(src_scripts, item)
            d = os.path.join(dst_scripts, item)
            if os.path.isfile(s):
                shutil.copy2(s, d)
            elif os.path.isdir(s):
                shutil.copytree(s, d, dirs_exist_ok=True)

    # 複製 references
    src_ref = os.path.join(steam_work_dir, "references")
    dst_ref = os.path.join(steam_git_dir, "references")
    if os.path.exists(src_ref):
        shutil.copytree(src_ref, dst_ref, dirs_exist_ok=True)

    # 複製 rdq
    src_rdq = os.path.join(steam_work_dir, "rdq")
    dst_rdq = os.path.join(steam_git_dir, "rdq")
    if os.path.exists(src_rdq):
        shutil.copytree(src_rdq, dst_rdq, dirs_exist_ok=True)

    print("  ✅ 檔案同步至專屬 Git 目錄完成！")

    # 2. 同步至全域技能模組
    print(f"\n[2/4] 同步更新至全域技能模組 ({global_skill_dir})...")
    if os.path.exists(global_skill_dir):
        # 範本
        t_src = os.path.join(steam_work_dir, "references", "templates", "領據.docx")
        t_dst = os.path.join(global_skill_dir, "references", "templates", "領據.docx")
        if os.path.exists(t_src):
            os.makedirs(os.path.dirname(t_dst), exist_ok=True)
            shutil.copy2(t_src, t_dst)
        
        # 產檔腳本
        g_src = os.path.join(steam_work_dir, "scripts", "generate_docs.py")
        g_dst = os.path.join(global_skill_dir, "scripts", "generate_docs.py")
        if os.path.exists(g_src):
            shutil.copy2(g_src, g_dst)

        # 郵件腳本
        m_src = os.path.join(steam_work_dir, "scripts", "send_gmail.py")
        m_dst = os.path.join(global_skill_dir, "scripts", "send_gmail.py")
        if os.path.exists(m_src):
            shutil.copy2(m_src, m_dst)

        print("  ✅ 全域技能模組同步完成！")

    # 3. 提交並推送至 steam-community-docs 線上遠端儲存庫
    print(f"\n[3/4] 提交並推送到 GitHub (asc103138/steam-community-docs)...")
    run_cmd(["git", "add", "-A"], cwd=steam_git_dir)
    st = subprocess.run(["git", "status", "--porcelain"], cwd=steam_git_dir, text=True, capture_output=True)
    if st.stdout.strip():
        run_cmd(["git", "commit", "-m", commit_msg], cwd=steam_git_dir)
        p_res = run_cmd(["git", "push", "origin", "main"], cwd=steam_git_dir)
        if p_res.returncode == 0:
            print("  ✅ 成功推送到 asc103138/steam-community-docs！")
    else:
        print("  ℹ️ steam-community-docs 已是最新狀態，無需重複提交。")

    # 4. 同步父倉庫 antui
    print(f"\n[4/4] 檢查父儲存庫 (asc103138/antui)...")
    antui_dir = r"d:\antui"
    run_cmd(["git", "add", "steam成果製作"], cwd=antui_dir)
    st_antui = subprocess.run(["git", "status", "--porcelain"], cwd=antui_dir, text=True, capture_output=True)
    if st_antui.stdout.strip():
        run_cmd(["git", "commit", "-m", commit_msg], cwd=antui_dir)
        p_antui = run_cmd(["git", "push", "origin", "main"], cwd=antui_dir)
        if p_antui.returncode == 0:
            print("  ✅ 成功同步至 asc103138/antui！")
    else:
        print("  ℹ️ antui 父儲存庫已是最新狀態。")

    print("\n🎉 所有儲存庫與全域模組皆已 100% 同步完成！")

if __name__ == '__main__':
    main()

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MinerU 專案多端自動同步與 Git 推送工具 (sync_git.py)
確保本地 pdf技能 工作目錄、專屬 Git 目錄 (d:\antigravity-mineru)、全域技能目錄 (20-mineru)
與線上 GitHub 儲存庫 (asc103138/antigravity-mineru) 保持同步。
"""

import os
import sys
import shutil
import subprocess
from pathlib import Path


def run_cmd(cmd, cwd=None):
    cmd_str = " ".join(cmd) if isinstance(cmd, list) else cmd
    print(f"  > {cmd_str} (in {cwd or '.'})")
    res = subprocess.run(cmd, cwd=cwd, text=True, capture_output=True, shell=isinstance(cmd, str))
    if res.returncode != 0:
        if res.stderr.strip():
            print(f"    ERROR: {res.stderr.strip()}", file=sys.stderr)
    elif res.stdout.strip():
        print(f"    {res.stdout.strip()}")
    return res


def main():
    commit_msg = sys.argv[1] if len(sys.argv) > 1 else "chore(sync): 同步最新 MinerU 技能與文件解析工具"

    work_dir = Path(r"d:\antui\pdf技能").resolve()
    git_dir = Path(r"d:\antigravity-mineru").resolve()
    user_home = Path.home()
    global_skill_dir = user_home / ".gemini" / "config" / "skills" / "20-mineru"

    print("=" * 65)
    print("  🚀 Antigravity MinerU 專案 Git 與全域技能同步流程啟動")
    print("=" * 65)

    # 1. 確保專屬 Git 目錄存在與初始化
    print(f"\n[1/4] 檢查專屬 Git 目錄 ({git_dir})...")
    git_dir.mkdir(parents=True, exist_ok=True)

    git_dot_dir = git_dir / ".git"
    if not git_dot_dir.exists():
        print("  初始化本地 Git 儲存庫...")
        run_cmd(["git", "init"], cwd=str(git_dir))
        run_cmd(["git", "branch", "-M", "main"], cwd=str(git_dir))
        run_cmd(["git", "remote", "add", "origin", "https://github.com/asc103138/antigravity-mineru.git"], cwd=str(git_dir))

    # 2. 複製主要專案檔案至專屬 Git 目錄
    print(f"\n[2/4] 同步工作檔案至專屬 Git 目錄...")
    sync_files = ["AGENTS.md", "ANTIGRAVITY.md", "handoff.md", "README.md", ".gitignore", "SKILL.md"]
    for fn in sync_files:
        src = work_dir / fn
        dst = git_dir / fn
        if src.exists():
            shutil.copy2(src, dst)
            print(f"  ✓ 已同步: {fn}")

    # 同步 scripts 目錄
    src_scripts = work_dir / "scripts"
    dst_scripts = git_dir / "scripts"
    if src_scripts.exists():
        dst_scripts.mkdir(parents=True, exist_ok=True)
        for item in src_scripts.iterdir():
            if item.is_file() and item.name != "__pycache__":
                shutil.copy2(item, dst_scripts / item.name)
                print(f"  ✓ 已同步腳本: scripts/{item.name}")

    # 3. 同步至全域技能目錄
    print(f"\n[3/4] 同步更新至全域技能目錄 ({global_skill_dir})...")
    if global_skill_dir.exists():
        skill_src = work_dir / "SKILL.md"
        if skill_src.exists():
            shutil.copy2(skill_src, global_skill_dir / "SKILL.md")
            print("  ✓ 全域 20-mineru/SKILL.md 已更新")
    else:
        global_skill_dir.mkdir(parents=True, exist_ok=True)
        shutil.copy2(work_dir / "SKILL.md", global_skill_dir / "SKILL.md")
        print("  ✓ 已建立全域技能目錄並同步 SKILL.md")

    # 4. Git Commit & Push
    print(f"\n[4/4] 執行 Git Commit 與推送至 GitHub...")
    run_cmd(["git", "add", "."], cwd=str(git_dir))
    status_res = run_cmd(["git", "status", "--porcelain"], cwd=str(git_dir))
    if not status_res.stdout.strip():
        print("  ℹ️ 專屬 Git 目錄無新增變更，跳過 commit。")
    else:
        run_cmd(["git", "commit", "-m", commit_msg], cwd=str(git_dir))

    push_res = run_cmd(["git", "push", "-u", "origin", "main"], cwd=str(git_dir))
    if push_res.returncode == 0:
        print("  🎉 專案已成功推送至線上 GitHub: https://github.com/asc103138/antigravity-mineru")
    else:
        print("  ⚠️ Git 推送遇到問題，請確認網路或遠端權限。")

    print("\n" + "=" * 65)
    print("  ✨ 同步完成！")
    print("=" * 65)


if __name__ == "__main__":
    main()

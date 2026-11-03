#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
自動將 22 頁 STEAM 成果展互動簡報部署至 GitHub Pages
1. 獨立儲存庫：https://asc103138.github.io/steam-gigo-balance-deck/
2. 專案主儲存庫：https://asc103138.github.io/steam-community-docs/成果展繳交資料/steam-gigo-balance-deck/
"""

import os
import shutil
import subprocess

SRC_DECK = r"d:\antui\steam成果製作\成果展繳交資料\steam-gigo-balance-deck"
DEPLOY_DIR = r"d:\steam-gigo-balance-deck"
REPO_FULL = "asc103138/steam-gigo-balance-deck"

print("=" * 65)
print("  🚀 啟動 GitHub Pages 網頁簡報自動部署流程")
print("=" * 65)

# 1. 準備部署目錄
if os.path.exists(DEPLOY_DIR):
    for item in os.listdir(DEPLOY_DIR):
        if item == ".git":
            continue
        p = os.path.join(DEPLOY_DIR, item)
        if os.path.isdir(p):
            shutil.rmtree(p)
        else:
            os.remove(p)
else:
    os.makedirs(DEPLOY_DIR, exist_ok=True)

# 複製簡報檔案 (index.html + images/)
for item in os.listdir(SRC_DECK):
    if item == ".git":
        continue
    s = os.path.join(SRC_DECK, item)
    d = os.path.join(DEPLOY_DIR, item)
    if os.path.isdir(s):
        shutil.copytree(s, d)
    else:
        shutil.copy2(s, d)

# 加入 .nojekyll 確保靜態資源不被 Jekyll 過濾
with open(os.path.join(DEPLOY_DIR, ".nojekyll"), "w", encoding="utf-8") as f:
    f.write("")

print("  ✅ 簡報靜態檔案已同步至:", DEPLOY_DIR)

# 2. 初始化 Git 並推送至 asc103138/steam-gigo-balance-deck
if not os.path.exists(os.path.join(DEPLOY_DIR, ".git")):
    subprocess.run(["git", "init", "-b", "main"], cwd=DEPLOY_DIR, check=True)
    subprocess.run(["git", "config", "user.name", "謝敦元"], cwd=DEPLOY_DIR, check=True)
    subprocess.run(["git", "config", "user.email", "305822202+asc103138@users.noreply.github.com"], cwd=DEPLOY_DIR, check=True)

subprocess.run(["git", "add", "-A"], cwd=DEPLOY_DIR, check=True)
status = subprocess.run(["git", "status", "--porcelain"], cwd=DEPLOY_DIR, capture_output=True, text=True).stdout.strip()
if status:
    subprocess.run(["git", "commit", "-m", "deploy: 臺中市梧棲區中正國小115年度STEAM教師社群成果展22頁互動簡報"], cwd=DEPLOY_DIR, check=True)

# 檢查遠端 repo 是否已存在
check_repo = subprocess.run(["gh", "repo", "view", REPO_FULL], capture_output=True, text=True)
if check_repo.returncode != 0:
    print(f"  📦 建立全新 GitHub 公開儲存庫: {REPO_FULL}")
    subprocess.run([
        "gh", "repo", "create", REPO_FULL,
        "--public",
        "--source=.",
        "--push",
        "--description", "臺中市梧棲區中正國小 115年度STEAM教師社群成果展 22頁互動簡報（積木啟發量感·機關驗證平衡）"
    ], cwd=DEPLOY_DIR, check=True)
else:
    # 確保 remote origin 存在並推送
    remotes = subprocess.run(["git", "remote"], cwd=DEPLOY_DIR, capture_output=True, text=True).stdout.split()
    if "origin" not in remotes:
        subprocess.run(["git", "remote", "add", "origin", f"https://github.com/{REPO_FULL}.git"], cwd=DEPLOY_DIR, check=True)
    subprocess.run(["git", "push", "-u", "origin", "main", "--force"], cwd=DEPLOY_DIR, check=True)

# 3. 啟用 GitHub Pages (steam-gigo-balance-deck)
print("  🌐 設定 GitHub Pages (asc103138/steam-gigo-balance-deck)...")
pages_check = subprocess.run(["gh", "api", f"repos/{REPO_FULL}/pages"], capture_output=True, text=True)
if pages_check.returncode != 0:
    subprocess.run([
        "gh", "api", f"repos/{REPO_FULL}/pages",
        "--method", "POST",
        "-f", "source[branch]=main",
        "-f", "source[path]=/"
    ], check=True)
    print("  ✅ 已成功開啟 asc103138/steam-gigo-balance-deck GitHub Pages！")
else:
    print("  ✅ asc103138/steam-gigo-balance-deck GitHub Pages 已處於啟用狀態！")

# 4. 同步開啟主儲存庫 asc103138/steam-community-docs 之 GitHub Pages
MAIN_REPO = "asc103138/steam-community-docs"
main_pages_check = subprocess.run(["gh", "api", f"repos/{MAIN_REPO}/pages"], capture_output=True, text=True)
if main_pages_check.returncode != 0:
    subprocess.run([
        "gh", "api", f"repos/{MAIN_REPO}/pages",
        "--method", "POST",
        "-f", "source[branch]=main",
        "-f", "source[path]=/"
    ], check=False)
    print("  ✅ 已同步開啟 asc103138/steam-community-docs GitHub Pages！")

print("\n🎉 部署完成！")
print(f"🔗 簡報專屬網址：https://asc103138.github.io/steam-gigo-balance-deck/")
print(f"📦 GitHub 儲存庫：https://github.com/{REPO_FULL}")

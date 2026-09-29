#!/usr/bin/env bash
# macOS & Linux setup script for steam-community-docs skill

set -e

echo "================================================================="
echo "  臺中市梧棲區中正國小 STEAM 教師社群"
echo "  自動化成果生成技能 (steam-community-docs) - macOS / Linux 安裝"
echo "================================================================="
echo ""

if ! command -v python3 &> /dev/null; then
    echo "[錯誤] 找不到 python3，請先安裝 Python 3。"
    exit 1
fi

python3 scripts/install_skill.py
echo ""
echo "[成功] 技能已完成設定！"

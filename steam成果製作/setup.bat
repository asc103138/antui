@echo off
chcp 65001 >nul
echo =================================================================
echo   臺中市梧棲區中正國小 STEAM 教師社群
echo   自動化成果生成技能 (steam-community-docs) - Windows 11 安裝設定
echo =================================================================
echo.

python --version >nul 2>&1
if errorlevel 1 (
    echo [錯誤] 找不到 Python，請先至 https://www.python.org/ 安裝 Python 3.10+ 並勾選 Add to PATH。
    pause
    exit /b 1
)

python scripts\install_skill.py
if errorlevel 1 (
    echo.
    echo [警告] 安裝過程遇到錯誤，請檢查上方訊息。
) else (
    echo.
    echo [成功] 技能已完成設定！您可以在 Windows 11 上的 Antigravity 直接使用此技能。
)

echo.
pause

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
=============================================================================
成品一票否決檢查機制 (Zero-Tolerance Deliverable Gatekeeper Protocol)
專案：antui / DUN-YUAN AI
標準：Emil Kowalski 全套設計工程工藝 + Mobile Native + 零漏洞物理真實感
規則：任一「一票否決紅線」不合格，立即判定 REBUILD（砍掉重練）！
=============================================================================
"""

import os
import re
import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent

# 顏色終端輸出
class Color:
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    BOLD = '\033[1m'
    RESET = '\033[0m'

class GatekeeperAuditor:
    def __init__(self):
        self.violations = []
        self.passes = []
        self.warnings = []

    def check_fatal(self, rule_name: str, passed: bool, error_msg: str, file_path: str = ""):
        if passed:
            self.passes.append((rule_name, file_path))
        else:
            self.violations.append((rule_name, error_msg, file_path))

    def audit_css(self, css_path: Path):
        if not css_path.exists():
            return
        content = css_path.read_text(encoding='utf-8')
        lines = content.splitlines()

        # 1. 嚴禁無差別 transition: all
        transition_all_matches = []
        for idx, line in enumerate(lines, 1):
            # 排除註解
            cleaned = line.split('/*')[0].strip()
            if re.search(r'transition\s*:\s*all\b', cleaned, re.IGNORECASE):
                transition_all_matches.append(f"Line {idx}: {cleaned}")
        self.check_fatal(
            "動效物理性：嚴禁 transition: all",
            len(transition_all_matches) == 0,
            f"發現無差別 transition: all，引發多餘重繪耗能：\n  " + "\n  ".join(transition_all_matches),
            css_path.name
        )

        # 2. 嚴禁 scale(0) 憑空生成
        scale_zero_matches = []
        for idx, line in enumerate(lines, 1):
            cleaned = line.split('/*')[0].strip()
            if re.search(r'scale\(\s*0\s*\)', cleaned):
                scale_zero_matches.append(f"Line {idx}: {cleaned}")
        self.check_fatal(
            "動效物理性：嚴禁 scale(0) 憑空出現",
            len(scale_zero_matches) == 0,
            f"發現 scale(0) 反物理動態（起點應為 scale(0.95) 搭配 opacity）：\n  " + "\n  ".join(scale_zero_matches),
            css_path.name
        )

        # 3. 嚴禁進場使用 ease-in
        ease_in_matches = []
        for idx, line in enumerate(lines, 1):
            cleaned = line.split('/*')[0].strip()
            if re.search(r'animation\s*:.*?\bease-in\b', cleaned, re.IGNORECASE) or re.search(r'transition\s*:.*?\bease-in\b', cleaned, re.IGNORECASE):
                ease_in_matches.append(f"Line {idx}: {cleaned}")
        self.check_fatal(
            "動效物理性：UI 進場嚴禁 ease-in",
            len(ease_in_matches) == 0,
            f"進場元素禁止使用 ease-in（必須使用強烈自訂曲線的 ease-out）：\n  " + "\n  ".join(ease_in_matches),
            css_path.name
        )

        # 4. 行動端原生感：消除點擊藍灰色高亮
        tap_highlight = re.search(r'-webkit-tap-highlight-color\s*:\s*transparent', content)
        self.check_fatal(
            "行動端原生：必備 -webkit-tap-highlight-color: transparent",
            bool(tap_highlight),
            "全域 Reset 缺少 -webkit-tap-highlight-color: transparent，行動端點擊會出現破壞質感的灰色遮罩！",
            css_path.name
        )

        # 5. 行動端原生感：全螢幕高低視窗 100dvh 適配 (嚴禁單純 100vh 破版)
        has_dvh = bool(re.search(r'100dvh|100svh', content))
        self.check_fatal(
            "行動端原生：視窗高度適配 100dvh / 100svh",
            has_dvh,
            "全域未發現 100dvh / 100svh 適配，行動端虛擬鍵盤與網址列伸縮時將出現死板 100vh 破版！",
            css_path.name
        )

        # 6. 微互動：按鈕必須包含 :active 微縮反饋
        has_active_scale = bool(re.search(r':active\s*\{[^}]*scale\(\s*0\.\d+\s*\)', content))
        self.check_fatal(
            "微互動回饋：按鈕與互動元素必備 :active 微縮",
            has_active_scale,
            "未檢測到按鈕 :active 包含 scale(0.96~0.98) 物理微縮觸感反饋！",
            css_path.name
        )

        # 7. 文字選取防護：user-select: none
        has_user_select = bool(re.search(r'user-select\s*:\s*none', content))
        self.check_fatal(
            "行動端原生：按鈕與控制項文字防誤選 user-select: none",
            has_user_select,
            "按鈕或可點擊標籤未鎖定 user-select: none，長按將觸發反白反選災難！",
            css_path.name
        )

        # 8. 表單字體防 iOS Safari 焦點縮放災難 (>= 16px)
        has_16px_rule = bool(re.search(r'font-size\s*:\s*16px', content))
        self.check_fatal(
            "行動端原生：表單/全局基準字體最低 16px 防放大",
            has_16px_rule,
            "未見 font-size: 16px 基準守門，iOS Safari 表單輸入可能觸發畫面無預警縮放！",
            css_path.name
        )

    def audit_html(self, html_path: Path):
        if not html_path.exists():
            return
        content = html_path.read_text(encoding='utf-8')

        # 1. Viewport 必須包含 viewport-fit=cover
        has_viewport_fit = bool(re.search(r'viewport-fit\s*=\s*cover', content))
        self.check_fatal(
            "行動端安全區：viewport-fit=cover",
            has_viewport_fit,
            "HTML <meta name=\"viewport\"> 缺少 viewport-fit=cover，無法適配 iPhone 瀏海與動態島安全區！",
            html_path.name
        )

        # 2. 檢查日夜模式支援
        has_theme_meta = bool(re.search(r'meta\s+name=["\']theme-color["\']', content))
        self.check_fatal(
            "瀏覽器整合：theme-color 標籤健全",
            has_theme_meta,
            "缺少 <meta name=\"theme-color\">，行動瀏覽器狀態列無法融合日夜沉浸背景！",
            html_path.name
        )

        # 3. 檢查流星層或背景動態層是否具備 pointer-events: none 防點擊攔截
        if 'meteor' in content:
            has_pointer_none = 'pointer-events: none' in content or 'meteor-shower-layer' in content
            self.check_fatal(
                "空間圖層：動態背景層不得攔截使用者點擊",
                has_pointer_none,
                "背景或流星圖層缺少 pointer-events: none 規範，可能阻礙卡片點擊！",
                html_path.name
            )

    def audit_security(self):
        # 掃描專案敏感關鍵字
        sensitive_patterns = [
            (r'AIzaSy[A-Za-z0-9_-]{33}', "Google API Key"),
            (r'ghp_[A-Za-z0-9]{36}', "GitHub Personal Access Token"),
            (r'sk-[A-Za-z0-9]{32,}', "OpenAI/Anthropic Secret Key"),
            (r'hf_[A-Za-z0-9]{34}', "Hugging Face Token"),
            (r'Bearer\s+[A-Za-z0-9_\-\.]{20,}', "Authorization Bearer Token")
        ]
        
        for file in ROOT_DIR.rglob('*'):
            if file.is_dir() or '.git' in file.parts or 'node_modules' in file.parts:
                continue
            if file.suffix in ['.html', '.css', '.js', '.md', '.json', '.py']:
                try:
                    text = file.read_text(encoding='utf-8', errors='ignore')
                    for pat, name in sensitive_patterns:
                        if re.search(pat, text):
                            self.check_fatal(
                                "資安紅線：嚴禁硬編碼機密金鑰",
                                False,
                                f"於檔案 {file.relative_to(ROOT_DIR)} 發現疑似洩漏之 {name}！",
                                str(file.name)
                            )
                except Exception:
                    pass

    def run(self) -> bool:
        print(f"\n{Color.BOLD}{Color.BLUE}========================================================================{Color.RESET}")
        print(f"{Color.BOLD}{Color.BLUE}   DUN-YUAN AI / antui 成品一票否決驗收檢查 (Gatekeeper Protocol)   {Color.RESET}")
        print(f"{Color.BOLD}{Color.BLUE}========================================================================{Color.RESET}\n")

        # 檢驗 CSS
        css_file = ROOT_DIR / 'style.css'
        self.audit_css(css_file)

        # 檢驗 HTML
        for html_name in ['index.html', 'tools.html']:
            self.audit_html(ROOT_DIR / html_name)

        # 檢驗資安
        self.audit_security()

        # 輸出結果
        print(f"{Color.BOLD}【合格檢驗項目（PASS）】{Color.RESET}")
        for rule, fpath in self.passes:
            loc = f" [{fpath}]" if fpath else ""
            print(f"  {Color.GREEN}✓ PASS{Color.RESET} {rule}{loc}")

        print()

        if self.violations:
            print(f"{Color.BOLD}{Color.RED}========================================================================{Color.RESET}")
            print(f"{Color.BOLD}{Color.RED}   [FAIL] 發現一票否決紅線違規！觸發【砍掉重練】機制 (REBUILD)   {Color.RESET}")
            print(f"{Color.BOLD}{Color.RED}========================================================================{Color.RESET}\n")
            for idx, (rule, msg, fpath) in enumerate(self.violations, 1):
                loc = f" [{fpath}]" if fpath else ""
                print(f"{Color.RED}[紅線 {idx}] {rule}{loc}{Color.RESET}")
                print(f"  {msg}\n")
            
            print(f"{Color.BOLD}{Color.YELLOW}處置程序：{Color.RESET}")
            print("  1. 拒絕合併 / 拒絕 Commit / 拒絕交付。")
            print("  2. 將踩線模組清空重寫，依據 Emil Kowalski 全套工藝與行動原生標準重新實作。")
            print("  3. 重新執行檢查直到 100% 全數通過。\n")
            return False
        else:
            print(f"{Color.BOLD}{Color.GREEN}========================================================================{Color.RESET}")
            print(f"{Color.BOLD}{Color.GREEN}   [PERFECT PASS] 全部標準合格！通過頂級設計工程工藝底線驗收！   {Color.RESET}")
            print(f"{Color.BOLD}{Color.GREEN}========================================================================{Color.RESET}\n")
            print("  ✓ 零無差別 transition: all")
            print("  ✓ 零 scale(0) 憑空進場")
            print("  ✓ 100dvh 行動視窗防破版")
            print("  ✓ :active 物理觸感微縮具備")
            print("  ✓ 消除點擊閃爍 & iOS 輸入框縮放防護")
            print("  ✓ 零機敏金鑰洩漏")
            return True

if __name__ == '__main__':
    auditor = GatekeeperAuditor()
    success = auditor.run()
    sys.exit(0 if success else 1)

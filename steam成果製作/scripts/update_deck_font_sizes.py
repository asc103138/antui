#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
精準更新 scripts/build_22p_reveal_deck.py 中的字體大小
1. 全局字體大幅升級：
   - reveal h1: 84px
   - reveal h2: 56px
   - reveal h3: 38px
   - lead-text: 34px
   - deck-footer: 20px
2. 回憶錄卡片字體升級：
   - tag-session: 24px
   - title: 36px
   - desc: 28px
   - 圖片高度微調為 330px 留出充裕排版空間
3. 所有卡片內文從 20px/22px 全面提升至 28px~30px
4. 對比滑桿文字升級至 30px，標題 40px
"""

import re

with open('scripts/build_22p_reveal_deck.py', 'r', encoding='utf-8') as f:
    text = f.read()

# 1. 替換 CSS 中的基礎字體設定
text = text.replace("font-size: 26px;\n      line-height: 1.6;", "font-size: 30px;\n      line-height: 1.6;")
text = text.replace("font-size: 68px;", "font-size: 84px;")
text = text.replace("font-size: 48px;", "font-size: 56px;")
text = text.replace("font-size: 32px;\n      line-height: 1.35;", "font-size: 38px;\n      line-height: 1.35;")
text = text.replace("font-size: 28px !important;\n      color: #e2e8f0 !important;", "font-size: 34px !important;\n      color: #e2e8f0 !important;")
text = text.replace("font-size: 20px;\n      font-weight: 700;\n      letter-spacing: 0.05em;", "font-size: 24px;\n      font-weight: 700;\n      letter-spacing: 0.05em;")
text = text.replace("height: 360px;\n      object-fit: cover;", "height: 330px;\n      object-fit: cover;")
text = text.replace("font-size: 18px;\n      font-weight: 700;\n      color: #ffffff;\n      background: var(--primary);", "font-size: 24px;\n      font-weight: 700;\n      color: #ffffff;\n      background: var(--primary);")
text = text.replace("font-size: 28px;\n      font-weight: 800;\n      color: #ffffff;\n      margin-bottom: 10px;", "font-size: 36px;\n      font-weight: 800;\n      color: #ffffff;\n      margin-bottom: 12px;")
text = text.replace("font-size: 22px;\n      line-height: 1.6;\n      color: #cbd5e1;", "font-size: 28px;\n      line-height: 1.55;\n      color: #e2e8f0;")
text = text.replace("font-size: 16px;\n      color: #64748b;", "font-size: 20px;\n      color: #94a3b8;")

# 2. 替換各頁面 HTML 內的 inline font-size
# 封面
text = text.replace('style="font-size:22px; margin-bottom:24px;"', 'style="font-size:28px; margin-bottom:24px;"')
text = text.replace('style="font-size:38px; color:#e0f2fe; font-weight:600; margin-bottom:48px;"', 'style="font-size:46px; color:#e0f2fe; font-weight:700; margin-bottom:44px;"')
text = text.replace('style="font-size:26px; color:#f8fafc; font-weight:700;"', 'style="font-size:32px; color:#f8fafc; font-weight:700;"')
text = text.replace('style="color:#38bdf8; font-size:26px;"', 'style="color:#38bdf8; font-size:32px;"')

# 替換通用的卡片字體
text = text.replace('font-size:44px; margin-bottom:12px;', 'font-size:56px; margin-bottom:10px;')
text = text.replace('font-size:44px; margin-bottom:10px;', 'font-size:54px; margin-bottom:10px;')
text = text.replace('font-size:40px; margin-bottom:12px;', 'font-size:52px; margin-bottom:10px;')

# 數字大標
text = text.replace('font-size:32px; margin-bottom:8px;', 'font-size:38px; margin-bottom:8px;')
text = text.replace('font-size:32px; margin-bottom:12px;', 'font-size:40px; margin-bottom:12px;')

# 內文段落
text = text.replace('style="font-size:22px; color:#cbd5e1; margin:0;"', 'style="font-size:28px; color:#e2e8f0; line-height:1.55; margin:0;"')
text = text.replace('style="font-size:20px; color:#cbd5e1; margin:0;"', 'style="font-size:28px; color:#e2e8f0; line-height:1.55; margin:0;"')
text = text.replace('style="font-size:22px; color:#cbd5e1;"', 'style="font-size:28px; color:#e2e8f0; line-height:1.55;"')
text = text.replace('style="font-size:24px; color:#e2e8f0; line-height:1.7;"', 'style="font-size:30px; color:#f1f5f9; line-height:1.6;"')
text = text.replace('style="color:#34d399; font-weight:800; font-size:26px;"', 'style="color:#34d399; font-weight:800; font-size:34px;"')

# S13 對比頁
text = text.replace('style="font-size:24px; line-height:1.6; color:#e2e8f0; margin:0;"', 'style="font-size:28px; line-height:1.55; color:#f1f5f9; margin:0;"')
text = text.replace('style="font-size:24px; line-height:1.6; color:#ecfdf5; margin:0;"', 'style="font-size:28px; line-height:1.55; color:#ecfdf5; margin:0;"')
text = text.replace('font-size:22px; font-weight:700;', 'font-size:28px; font-weight:800;')
text = text.replace('font-size:24px; color:#94a3b8; font-weight:700;', 'font-size:30px; color:#94a3b8; font-weight:700;')

# S22 結尾
text = text.replace('style="font-size:32px; font-weight:800; color:#ffffff; background:rgba(15,23,42,0.85); padding:14px 44px;', 'style="font-size:38px; font-weight:800; color:#ffffff; background:rgba(15,23,42,0.85); padding:16px 52px;')

with open('scripts/build_22p_reveal_deck.py', 'w', encoding='utf-8') as f:
    f.write(text)

print("Successfully updated scripts/build_22p_reveal_deck.py with enlarged font sizes!")

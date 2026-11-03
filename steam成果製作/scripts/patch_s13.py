#!/usr/bin/env python3
# -*- coding: utf-8 -*-
with open('scripts/build_22p_reveal_deck.py', 'r', encoding='utf-8') as f:
    text = f.read()

# 微調 S13 卡片文字與高度
text = text.replace('height: 560px;', 'height: 580px;')
text = text.replace('max-width: 700px;', 'max-width: 740px;')
text = text.replace('padding: 20px 28px;', 'padding: 16px 24px;')

# 精煉文字
old_before_text = """              <div style="color:#f87171; font-weight:800; font-size:40px; margin-bottom:12px;">❌ 傳統課堂教學困境（代碼 M3-W-01）</div>
              <p style="font-size:28px; line-height:1.55; color:#f1f5f9; margin:0;">
                • 面對市售彈簧秤黑盒子，指針未歸零卻直接判讀。<br>
                • 刻度密密麻麻，學生常把「1大格100g、5小格」誤算為一小格 10g。<br>
                • 抽象死背「1公斤 = 1000公克」，缺乏真實重量體感。<br>
                • 紙筆算則寫得漂亮，但一到真實生活買水果或稱重時完全失靈。
              </p>
              <div style="color:#fca5a5; margin-top:14px; font-size:28px; font-weight:800;">
                ⚠️ 核心缺失：缺乏物理實體感知，量感未內化為直覺。
              </div>"""

new_before_text = """              <div style="color:#f87171; font-weight:800; font-size:36px; margin-bottom:8px;">❌ 傳統課堂教學困境（代碼 M3-W-01）</div>
              <p style="font-size:26px; line-height:1.45; color:#f1f5f9; margin:0;">
                • 市售彈簧秤黑盒子，指針未歸零卻直接判讀。<br>
                • 刻度密密麻麻，常把「1大格100g、5小格」誤算為一格10g。<br>
                • 抽象死背「1公斤=1000公克」，缺乏真實重量手感。<br>
                • 紙筆算則寫得漂亮，但生活實測秤重時完全失靈。
              </p>
              <div style="color:#fca5a5; margin-top:10px; font-size:26px; font-weight:800;">
                ⚠️ 核心缺失：缺乏實體物理感知，量感未內化為直覺。
              </div>"""

old_after_text = """              <div style="color:#34d399; font-weight:800; font-size:40px; margin-bottom:12px;">✅ 中正社群自研 STEAM 新典範</div>
              <p style="font-size:28px; line-height:1.55; color:#ecfdf5; margin:0;">
                • 社群研發智高等臂天平，學生親手組裝，直觀理解歸零與力矩。<br>
                • 透過 5g 小積木逐個疊加，體會非標準到標準單位進程。<br>
                • 算則直接對應手部調校：較輕補積木（加法）、去皮拿積木（減法）。<br>
                • 課堂實證：前後測理解度大躍升 28.5%，滿意度達 96.8%！
              </p>
              <div style="color:#a7f3d0; margin-top:14px; font-size:28px; font-weight:800;">
                ✨ 社群突破：將抽象數學具象化，建立孩子深厚探究自信！
              </div>"""

new_after_text = """              <div style="color:#34d399; font-weight:800; font-size:36px; margin-bottom:8px;">✅ 中正社群自研 STEAM 新典範</div>
              <p style="font-size:26px; line-height:1.45; color:#ecfdf5; margin:0;">
                • 自研智高等臂天平，親手組裝直觀理解歸零與力矩。<br>
                • 透過 5g 積木逐個累加，體會非標準到標準單位進程。<br>
                • 算則對應手部調校：較輕補積木（加法）、去皮減積木（減法）。<br>
                • 課堂實證：前後測理解度躍升 28.5%，滿意度達 96.8%！
              </p>
              <div style="color:#a7f3d0; margin-top:10px; font-size:26px; font-weight:800;">
                ✨ 社群突破：將抽象數學具象化，建立深厚探究自信！
              </div>"""

if old_before_text in text:
    text = text.replace(old_before_text, new_before_text)
if old_after_text in text:
    text = text.replace(old_after_text, new_after_text)

with open('scripts/build_22p_reveal_deck.py', 'w', encoding='utf-8') as f:
    f.write(text)

print("Updated S13 card in build_22p_reveal_deck.py!")

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
將原本合併於單頁的「拉桿對照頁 (S13)」拆分為兩頁獨立、完整且清晰的大字版投影片：
- 第 13 頁：社群研發對照 (一)：傳統彈簧秤「黑盒子」瓶頸剖析 (搭配完整未裁切之 viz_traditional_scale.png)
- 第 14 頁：社群研發對照 (二)：中正自製智高天平 STEAM 新典範 (搭配完整未裁切之 viz_steam_balance.png)
同步更新 HTML 簡報 (build_22p_reveal_deck.py) 與 PPTX 簡報 (generate_22p_pptx.py) 為 23 頁完整版。
"""

import re

# 1. 更新 build_22p_reveal_deck.py
with open("scripts/build_22p_reveal_deck.py", "r", encoding="utf-8") as f:
    deck_code = f.read()

pattern = re.compile(
    r"<!-- S13: 典範轉移 3D 拉桿.*?<!-- S14: 縱向延展 \(一\) micro:bit -->",
    re.DOTALL
)

replacement_slides = """<!-- S13: 社群研發對照 (一)：傳統彈簧秤黑盒子瓶頸剖析 (獨立單頁完整說明) -->
      <section data-background-image="images/bgs/bg_paradigm.png"
               data-background-opacity="0.32"
               data-background-size="cover">
        <h2>社群研發對照 (一)：傳統彈簧秤「黑盒子」瓶頸剖析</h2>
        <p class="lead-text">
          本社群於第一場次共備時，深入剖析傳統秤重教學為何難以建立真實量感：
        </p>

        <div class="grid-2" style="align-items: stretch;">
          <div class="glass-card" style="border-top: 6px solid #ef4444; display:flex; flex-direction:column; justify-content:space-between;">
            <img src="images/viz_traditional_scale.png" alt="傳統彈簧秤黑盒子剖析"
                 style="width:100%; height:410px; object-fit:cover; border-radius:14px; border:2px solid rgba(248,113,113,0.45); margin-bottom:16px;" />
            <div style="font-size:26px; font-weight:700; color:#fca5a5; text-align:center; background:rgba(239,68,68,0.15); padding:10px 16px; border-radius:10px;">
              📦 傳統教具瓶頸：彈簧結構封閉於外殼內，學生僅能被動判讀指針
            </div>
          </div>

          <div class="glass-card" style="border-left: 6px solid #ef4444; display:flex; flex-direction:column; justify-content:space-between;">
            <div>
              <h3 style="color:#f87171; font-size:36px; margin-bottom:16px;">🔍 社群共備診斷之四大教學痛點</h3>
              <p style="font-size:28px; line-height:1.62; color:#f1f5f9; margin:0;">
                • <strong>黑盒子效應</strong>：市售彈簧秤內部力學結構封閉，指針未歸零學生卻直接讀數。<br>
                • <strong>刻度判讀挫折</strong>：面對「1大格100g、5小格」細密刻度，常誤算為一格 10g。<br>
                • <strong>抽象死背公式</strong>：僅靠紙筆背誦「1公斤＝1000公克」，缺乏真實重量體感。<br>
                • <strong>算則操作脫節</strong>：紙筆加減法會算，但實際秤重配平與去皮時卻無從下手。
              </p>
            </div>
            <div style="color:#fecaca; margin-top:18px; font-size:27px; font-weight:800; background:rgba(239,68,68,0.18); padding:12px 18px; border-radius:12px;">
              💡 社群研發共識：必須開發「結構全透明、可親手加減配平」的實體教具！
            </div>
          </div>
        </div>
      </section>

      <!-- S14: 社群研發對照 (二)：中正自製智高天平 STEAM 新典範 (獨立單頁完整說明) -->
      <section data-background-image="images/bgs/bg_paradigm.png"
               data-background-opacity="0.32"
               data-background-size="cover">
        <h2>社群研發對照 (二)：中正自製智高天平 STEAM 新典範</h2>
        <p class="lead-text">
          本社群以自製 20 孔等臂天平與 5g 標準積木砝碼，實現具體可感的量感教學：
        </p>

        <div class="grid-2" style="align-items: stretch;">
          <div class="glass-card" style="border-top: 6px solid #10b981; display:flex; flex-direction:column; justify-content:space-between;">
            <img src="images/viz_steam_balance.png" alt="中正社群自研智高積木等臂天平"
                 style="width:100%; height:410px; object-fit:cover; border-radius:14px; border:2px solid rgba(52,211,153,0.45); margin-bottom:16px;" />
            <div style="font-size:26px; font-weight:700; color:#a7f3d0; text-align:center; background:rgba(16,185,129,0.15); padding:10px 16px; border-radius:10px;">
              ⚖️ 本社群自研教具：20孔等臂橫樑、鉛直基準線與 5g 積木砝碼全透明可視
            </div>
          </div>

          <div class="glass-card" style="border-left: 6px solid #10b981; display:flex; flex-direction:column; justify-content:space-between;">
            <div>
              <h3 style="color:#34d399; font-size:36px; margin-bottom:16px;">✅ 中正社群自研 STEAM 四大突破</h3>
              <p style="font-size:28px; line-height:1.62; color:#ecfdf5; margin:0;">
                • <strong>結構透明可視</strong>：親手組裝智高等臂天平，直觀理解支點、力臂與歸零原理。<br>
                • <strong>5g 積木定量</strong>：透過每顆 5g 智高積木逐一累加，體會非標準到標準公克進程。<br>
                • <strong>手腦合一算則</strong>：較輕補積木（加法）、去皮減積木（減法），算式與動作同步。<br>
                • <strong>試教實證躍升</strong>：前後測理解度顯著成長 28.5%，課堂學習滿意度達 96.8%！
              </p>
            </div>
            <div style="color:#a7f3d0; margin-top:18px; font-size:27px; font-weight:800; background:rgba(16,185,129,0.18); padding:12px 18px; border-radius:12px;">
              ✨ 社群核心價值：將抽象數學公式具象化，建立孩子深厚探究自信！
            </div>
          </div>
        </div>
      </section>

      <!-- S15: 縱向延展 (一) micro:bit -->"""

assert pattern.search(deck_code), "Pattern not found in build_22p_reveal_deck.py"
deck_code = pattern.sub(replacement_slides, deck_code)

with open("scripts/build_22p_reveal_deck.py", "w", encoding="utf-8") as f:
    f.write(deck_code)

print("✅ Updated build_22p_reveal_deck.py to 23 slides (split S13 slider into S13 + S14)!")

# 2. 更新 generate_22p_pptx.py
with open("scripts/generate_22p_pptx.py", "r", encoding="utf-8") as f:
    pptx_code = f.read()

old_s13_pptx = """# -------------------------------------------------------------
# S13: 典範轉移 3D 對比 (左為傳統困境，右為社群成果)
# -------------------------------------------------------------
s13 = prs.slides.add_slide(blank_layout)
set_slide_bg(s13, "bg_paradigm.png")
add_header(s13, "社群研發成效對比：傳統課堂困境 vs STEAM 新典範")
add_card(s13, 0.8, 2.0, 5.7, 4.8, "❌ 傳統課堂教學困境（代碼 M3-W-01）", "• 面對市售彈簧秤黑盒子，指針未歸零卻直接判讀。\\n• 刻度密密麻麻，學生常把一小格誤判為 10g。\\n• 抽象死背「1公斤 = 1000公克」，缺乏真實重量體感。\\n• 紙筆算則寫得漂亮，但一到生活秤重時完全失靈。\\n\\n⚠️ 核心缺失：缺乏物理實體感知，量感未內化為直覺。", RED_ACCENT, RED_ACCENT)
add_card(s13, 6.8, 2.0, 5.7, 4.8, "✅ 中正社群自研 STEAM 新典範", "• 社群研發智高等臂天平，學生親手組裝，直觀理解力矩。\\n• 透過 5g 小積木逐個疊加，體會單位量感進程。\\n• 算則直接對應手部調校：較輕補足、去皮移除。\\n• 課堂實證：前後測理解度大躍升 28.5%，滿意度達 96.8%！\\n\\n✨ 社群突破：將抽象數學具象化，建立孩子深厚探究自信！", GREEN_ACCENT, GREEN_ACCENT)"""

new_s13_s14_pptx = """# -------------------------------------------------------------
# S13: 社群研發對照 (一)：傳統彈簧秤黑盒子瓶頸剖析
# -------------------------------------------------------------
s13 = prs.slides.add_slide(blank_layout)
set_slide_bg(s13, "bg_paradigm.png")
add_header(s13, "社群研發對照 (一)：傳統彈簧秤「黑盒子」瓶頸剖析")
p_trad = os.path.join(IMG_DIR, "viz_traditional_scale.png")
if os.path.exists(p_trad):
    s13.shapes.add_picture(p_trad, Inches(0.8), Inches(2.0), width=Inches(5.6), height=Inches(3.6))
add_card(s13, 0.8, 5.7, 5.6, 1.1, "📦 傳統教具瓶頸", "彈簧結構封閉於外殼內，學生僅能被動判讀指針", RED_ACCENT, RED_ACCENT)
add_card(s13, 6.8, 2.0, 5.7, 4.8, "🔍 社群共備診斷之四大教學痛點", "• 黑盒子效應：內部力學結構封閉，指針未歸零卻直接讀數。\\n• 刻度判讀挫折：面對細密刻度常誤算為一格 10g。\\n• 抽象死背公式：僅靠紙筆背誦「1公斤=1000公克」。\\n• 算則操作脫節：紙筆加減會算，實際配平與去皮無從下手。\\n\\n💡 社群共識：必須開發結構全透明、可親手配平之教具！", RED_ACCENT, RED_ACCENT)

# -------------------------------------------------------------
# S14: 社群研發對照 (二)：中正自製智高天平 STEAM 新典範
# -------------------------------------------------------------
s14_new = prs.slides.add_slide(blank_layout)
set_slide_bg(s14_new, "bg_paradigm.png")
add_header(s14_new, "社群研發對照 (二)：中正自製智高天平 STEAM 新典範")
p_steam = os.path.join(IMG_DIR, "viz_steam_balance.png")
if os.path.exists(p_steam):
    s14_new.shapes.add_picture(p_steam, Inches(0.8), Inches(2.0), width=Inches(5.6), height=Inches(3.6))
add_card(s14_new, 0.8, 5.7, 5.6, 1.1, "⚖️ 本社群自研教具", "20孔等臂橫樑、鉛直基準線與 5g 積木砝碼全透明可視", GREEN_ACCENT, GREEN_ACCENT)
add_card(s14_new, 6.8, 2.0, 5.7, 4.8, "✅ 中正社群自研 STEAM 四大突破", "• 結構透明可視：親手組裝等臂天平，直觀理解支點與歸零。\\n• 5g 積木定量：每顆 5g 積木逐一累加，體會標準公克進程。\\n• 手腦合一算則：較輕補積木（加）、去皮減積木（減）。\\n• 試教實證躍升：前後測理解度成長 28.5%，滿意度 96.8%！\\n\\n✨ 社群價值：將抽象數學公式具象化，建立深厚探究自信！", GREEN_ACCENT, GREEN_ACCENT)"""

if old_s13_pptx in pptx_code:
    pptx_code = pptx_code.replace(old_s13_pptx, new_s13_s14_pptx)
    with open("scripts/generate_22p_pptx.py", "w", encoding="utf-8") as f:
        f.write(pptx_code)
    print("✅ Updated generate_22p_pptx.py to 23 slides!")
else:
    print("⚠️ Notice: old_s13_pptx pattern check needed in generate_22p_pptx.py")

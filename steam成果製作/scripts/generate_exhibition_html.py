#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
生成符合 Emil Kowalski 設計工程標準的 16:9 現代化網頁簡報 (成果展現場分享會簡報.html)
"""

import os
import base64

HTML_DIR = r"d:\antui\steam成果製作\成果展繳交資料"
PHOTO_DIR = os.path.join(HTML_DIR, "成果展示照片")

def get_base64_img(filename):
    p = os.path.join(PHOTO_DIR, filename)
    if os.path.exists(p):
        with open(p, "rb") as f:
            return f"data:image/jpeg;base64,{base64.b64encode(f.read()).decode('utf-8')}"
    return ""

img1_b64 = get_base64_img("01_課堂實踐_三年級學生分組操作智高天平機關進行重量測量與小組熱烈討論.jpg")
img2_b64 = get_base64_img("02_科技跨域_microbit甩繩軌跡神射手課堂動態測試與數據回饋.jpg")
img3_b64 = get_base64_img("03_機關整合_世界機關王競賽指定關卡傳動組裝與連續觸發調校.jpg")

html_content = f'''<!DOCTYPE html>
<html lang="zh-TW">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0, viewport-fit=cover">
  <meta name="theme-color" content="#0F172A">
  <title>中正國小 115年度STEAM成果展 5分鐘分享會簡報</title>
  <style>
    :root {{
      --bg: #0F172A;
      --card-bg: rgba(30, 41, 59, 0.7);
      --card-border: rgba(148, 163, 184, 0.15);
      --text: #F8FAFC;
      --text-muted: #94A3B8;
      --cyan: #06B6D4;
      --orange: #F97316;
      --green: #22C55E;
      --red: #EF4444;
      --ease-out: cubic-bezier(0.16, 1, 0.3, 1);
      --ease-drawer: cubic-bezier(0.32, 0.72, 0, 1);
    }}

    [data-theme="light"] {{
      --bg: #F8FAFC;
      --card-bg: rgba(255, 255, 255, 0.9);
      --card-border: rgba(203, 213, 225, 0.8);
      --text: #0F172A;
      --text-muted: #64748B;
      --cyan: #0891B2;
      --orange: #EA580C;
      --green: #16A34A;
      --red: #DC2626;
    }}

    * {{
      box-sizing: border-box;
      margin: 0;
      padding: 0;
      -webkit-tap-highlight-color: transparent;
    }}

    body {{
      font-family: -apple-system, BlinkMacSystemFont, "PingFang TC", "Noto Sans TC", "Microsoft JhengHei", sans-serif;
      background-color: var(--bg);
      color: var(--text);
      overflow: hidden;
      height: 100dvh;
      width: 100vw;
      user-select: none;
      transition: background-color 200ms var(--ease-out), color 200ms var(--ease-out);
    }}

    /* 頂部進度條 */
    .progress-bar-track {{
      position: fixed;
      top: 0;
      left: 0;
      width: 100vw;
      height: 4px;
      background: rgba(255, 255, 255, 0.1);
      z-index: 100;
    }}
    .progress-bar-fill {{
      height: 100%;
      background: linear-gradient(90deg, var(--cyan), var(--orange));
      width: 14.28%;
      transition: width 240ms var(--ease-out);
    }}

    /* 投影片舞台容器 */
    .deck-container {{
      position: relative;
      width: 100vw;
      height: 100dvh;
      display: flex;
      align-items: center;
      justify-content: center;
      padding: 3vh 3vw 6vh;
    }}

    .slide {{
      position: absolute;
      width: min(94vw, 1360px);
      height: min(84dvh, 765px);
      aspect-ratio: 16 / 9;
      background: var(--card-bg);
      border: 1px solid var(--card-border);
      border-radius: 20px;
      padding: 40px 50px;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      backdrop-filter: blur(16px);
      opacity: 0;
      transform: scale(0.96) translateY(12px);
      pointer-events: none;
      transition: opacity 280ms var(--ease-out), transform 280ms var(--ease-out);
    }}

    .slide.active {{
      opacity: 1;
      transform: scale(1) translateY(0);
      pointer-events: auto;
    }}

    /* 標題與標籤 */
    .slide-badge {{
      display: inline-flex;
      align-items: center;
      gap: 6px;
      font-size: 14px;
      font-weight: 700;
      color: var(--cyan);
      text-transform: uppercase;
      letter-spacing: 1px;
      margin-bottom: 8px;
    }}

    .slide-title {{
      font-size: clamp(24px, 2.8vw, 36px);
      font-weight: 800;
      color: var(--text);
      line-height: 1.25;
      margin-bottom: 24px;
    }}

    /* Slide 1 封面特化 */
    .cover-body {{
      display: flex;
      flex-direction: column;
      justify-content: center;
      height: 100%;
      gap: 16px;
    }}
    .cover-headline {{
      font-size: clamp(32px, 4.2vw, 56px);
      font-weight: 900;
      line-height: 1.15;
      background: linear-gradient(135deg, var(--text) 30%, var(--cyan) 100%);
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
    }}
    .cover-tagline {{
      font-size: clamp(18px, 2vw, 26px);
      font-weight: 700;
      color: var(--orange);
    }}
    .cover-meta {{
      font-size: 16px;
      color: var(--text-muted);
      margin-top: 20px;
      display: flex;
      gap: 24px;
      flex-wrap: wrap;
    }}

    /* 雙卡 / 三卡 柵格 */
    .grid-2 {{
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 24px;
      height: 100%;
    }}
    .grid-3 {{
      display: grid;
      grid-template-columns: 1fr 1fr 1fr;
      gap: 20px;
      height: 100%;
    }}

    .sub-card {{
      background: rgba(255, 255, 255, 0.04);
      border: 1px solid var(--card-border);
      border-radius: 14px;
      padding: 24px;
      display: flex;
      flex-direction: column;
      gap: 12px;
      transition: border-color 150ms var(--ease-out);
    }}
    .sub-card.danger {{
      border-color: rgba(239, 68, 68, 0.4);
    }}
    .sub-card.success {{
      border-color: rgba(6, 182, 212, 0.5);
    }}
    .sub-card h3 {{
      font-size: 20px;
      font-weight: 800;
      color: var(--text);
    }}
    .sub-card p, .sub-card li {{
      font-size: 15px;
      line-height: 1.6;
      color: var(--text-muted);
      list-style-position: inside;
    }}

    /* 圖文版型 */
    .media-grid {{
      display: grid;
      grid-template-columns: 1.1fr 0.9fr;
      gap: 28px;
      align-items: center;
      height: 100%;
    }}
    .slide-img-frame {{
      width: 100%;
      height: 100%;
      max-height: 440px;
      border-radius: 14px;
      overflow: hidden;
      border: 1px solid var(--card-border);
      box-shadow: 0 12px 32px rgba(0, 0, 0, 0.3);
    }}
    .slide-img-frame img {{
      width: 100%;
      height: 100%;
      object-fit: cover;
      display: block;
    }}

    /* 數字大卡片 */
    .metric-value {{
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
      font-size: clamp(36px, 4vw, 54px);
      font-weight: 900;
      color: var(--cyan);
      line-height: 1;
    }}
    .metric-card {{
      background: rgba(255, 255, 255, 0.03);
      border: 1px solid var(--card-border);
      border-radius: 16px;
      padding: 24px;
      text-align: center;
      display: flex;
      flex-direction: column;
      justify-content: center;
      gap: 10px;
    }}

    /* 底部控制工具列 */
    .toolbar {{
      position: fixed;
      bottom: 12px;
      left: 50%;
      transform: translateX(-50%);
      display: flex;
      align-items: center;
      gap: 12px;
      background: rgba(15, 23, 42, 0.85);
      border: 1px solid var(--card-border);
      padding: 6px 16px;
      border-radius: 40px;
      backdrop-filter: blur(12px);
      z-index: 100;
    }}
    .toolbar-btn {{
      background: none;
      border: none;
      color: var(--text);
      cursor: pointer;
      font-size: 14px;
      padding: 6px 10px;
      border-radius: 8px;
      display: flex;
      align-items: center;
      gap: 6px;
      font-weight: 600;
      transition: background 150ms var(--ease-out), transform 80ms var(--ease-out);
    }}
    .toolbar-btn:active {{
      transform: scale(0.97);
    }}
    .toolbar-btn:hover {{
      background: rgba(255, 255, 255, 0.08);
    }}
    .timer-display {{
      font-family: monospace;
      font-size: 15px;
      font-weight: 700;
      color: var(--cyan);
      padding: 0 8px;
      border-left: 1px solid var(--card-border);
      border-right: 1px solid var(--card-border);
    }}

    /* 講者備忘提詞抽屜 */
    .notes-drawer {{
      position: fixed;
      right: 20px;
      bottom: 70px;
      width: min(420px, 90vw);
      background: rgba(15, 23, 42, 0.95);
      border: 1px solid var(--cyan);
      border-radius: 16px;
      padding: 20px;
      box-shadow: 0 16px 40px rgba(0, 0, 0, 0.5);
      backdrop-filter: blur(16px);
      z-index: 99;
      transform: translateY(20px) scale(0.96);
      opacity: 0;
      pointer-events: none;
      transition: transform 240ms var(--ease-drawer), opacity 240ms var(--ease-drawer);
    }}
    .notes-drawer.open {{
      transform: translateY(0) scale(1);
      opacity: 1;
      pointer-events: auto;
    }}
    .notes-title {{
      font-size: 14px;
      font-weight: 800;
      color: var(--cyan);
      margin-bottom: 8px;
      display: flex;
      justify-content: space-between;
    }}
    .notes-text {{
      font-size: 14px;
      line-height: 1.6;
      color: #E2E8F0;
      max-height: 240px;
      overflow-y: auto;
    }}
  </style>
</head>
<body>

  <!-- 頂部進度條 -->
  <div class="progress-bar-track">
    <div class="progress-bar-fill" id="progressBar"></div>
  </div>

  <div class="deck-container">
    <!-- Slide 1: 封面 -->
    <section class="slide active" id="slide-1" data-notes="【0:00-0:35 引言】各位長官好，我是中正國小謝敦元。今天代表社群分享「智高積木動手玩·三年級重量測量機關探究」。核心理念：讓數學量感在積木聲中看得見、摸得到！">
      <div>
        <div class="slide-badge">臺中市 115 年度推動校園 STEAM 教育計畫 · 社群成果展</div>
      </div>
      <div class="cover-body">
        <h1 class="cover-headline">智高積木動手玩·三年級重量測量機關探究</h1>
        <div class="cover-tagline">讓抽象的數學量感，在積木咔嗒聲中看得見、摸得到！</div>
        <div class="cover-meta">
          <div>🏫 <b>發表學校：</b>臺中市梧棲區中正國民小學</div>
          <div>👥 <b>社群團隊：</b>謝敦元(召集人)、王怡婷、李仁耀、曾泊淞</div>
          <div>⏱️ <b>限時規範：</b>5 分鐘現場精華報告</div>
        </div>
      </div>
      <div style="font-size: 13px; color: var(--text-muted);">按鍵 [方向鍵 →] 進入下一頁 ｜ [T] 切換主題 ｜ [N] 開啟講者提詞</div>
    </section>

    <!-- Slide 2: 痛點與理念 -->
    <section class="slide" id="slide-2" data-notes="【0:35-1:15 痛點】三年級教公斤與公克，孩子只看課本指針秤常一臉茫然。手感不準、指針秤是黑盒子。我們思考：孩子能不能用智高積木親手打造等臂天平？">
      <div>
        <div class="slide-badge">痛點診斷 ✕ STEAM 解決方案</div>
        <h2 class="slide-title">為什麼孩子害怕「公斤與公克」？</h2>
      </div>
      <div class="grid-2">
        <div class="sub-card danger">
          <h3 style="color: var(--red);">❌ 傳統教學的兩大瓶頸</h3>
          <p>• <b>只有手感，缺乏實體量感：</b>孩子單憑手掂物品只能模糊感覺誰輕誰重，難以體會「公克(g)」與「公斤(kg)」在生活中的精準差距。</p>
          <p>• <b>傳統指針秤是個黑盒子：</b>課本指針直接跳出刻度，孩子看不見「支點、力臂與力矩」的物理過程，加減微調難以轉化為算則。</p>
        </div>
        <div class="sub-card success">
          <h3 style="color: var(--cyan);">💡 STEAM 跨領域創新解方</h3>
          <p>• <b>讓數學動起來（Math in Action）：</b>結合智高積木結構，讓學生親手組裝「等臂天平機關」，直觀目擊傾斜與平衡的物理過程。</p>
          <p>• <b>單位小積木微調（加減算則實證）：</b>在輕的一邊增加小積木，把抽象的加減法轉化為親手調校平衡的探索樂趣！</p>
        </div>
      </div>
      <div style="font-size: 13px; color: var(--text-muted);">核心轉化：從「被動讀秤」躍升為「主動調校平衡」</div>
    </section>

    <!-- Slide 3: 三節課架構 -->
    <section class="slide" id="slide-3" data-notes="【1:15-2:05 架構】三節課階梯探究：第1節手感挑戰建立需求；第2節積木天平組裝，下降側＝較重；第3節加減微調小積木達到平衡。">
      <div>
        <div class="slide-badge">核心教案設計（附件6）</div>
        <h2 class="slide-title">三節階梯式探究歷程（共 120 分鐘）</h2>
      </div>
      <div class="grid-3">
        <div class="sub-card" style="border-color: rgba(6, 182, 212, 0.4);">
          <h3 style="color: var(--cyan);">第 1 節：概念與探究</h3>
          <p><b>手感挑戰 · 建立量感</b></p>
          <p>• 實物徒手掂重與排序<br>• 察覺個人手感誤差衝突<br>• 體認公正測量工具之必要<br>• 對應素養：n-II-9, 數-E-B1</p>
        </div>
        <div class="sub-card" style="border-color: rgba(249, 115, 22, 0.4);">
          <h3 style="color: var(--orange);">第 2 節：機關製作</h3>
          <p><b>工程組裝 · 傾斜判定</b></p>
          <p>• 智高積木天平支撐＋托盤<br>• 等臂力矩調校與靈敏度<br>• 下降側＝較重（動態視覺化）<br>• 對應素養：n-II-8, 數-E-A2</p>
        </div>
        <div class="sub-card" style="border-color: rgba(34, 197, 94, 0.4);">
          <h3 style="color: var(--green);">第 3 節：加減平衡</h3>
          <p><b>平衡挑戰 · 算則轉化</b></p>
          <p>• 標準單位小積木加減微調<br>• 「在輕側再加2顆就平了」<br>• 統整加減算則與物理量感<br>• 對應素養：n-II-2, 數-E-C2</p>
        </div>
      </div>
      <div style="font-size: 13px; color: var(--text-muted);">三維度螺旋式學習：概念 ➜ 操作 ➜ 算則轉化</div>
    </section>

    <!-- Slide 4: 課堂實踐與照片 -->
    <section class="slide" id="slide-4" data-notes="【2:05-2:55 實踐】三年丙班真實試教。破除迷思一：體積大不等於重（保麗龍 vs 鐵砝碼）；迷思二：天平偏了可在輕側加積木微調。孩子眼睛發光！">
      <div>
        <div class="slide-badge">真實課堂試教實踐</div>
        <h2 class="slide-title">課堂實踐 · 孩子破除迷思的震撼時刻</h2>
      </div>
      <div class="media-grid">
        <div class="slide-img-frame">
          <img src="{img1_b64}" alt="課堂實踐現場">
        </div>
        <div style="display: flex; flex-direction: column; gap: 16px;">
          <div class="sub-card">
            <h3 style="color: var(--orange);">✨ 迷思一：體積大就一定比較重？</h3>
            <p>孩子將拳頭大的保麗龍放左邊、小金屬鐵砝碼放右邊，天平重重向右沉下！動手打破「大即是重」的迷思，深刻體會材質密度的概念。</p>
          </div>
          <div class="sub-card">
            <h3 style="color: var(--cyan);">✨ 迷思二：天平不平只能換物品？</h3>
            <p>孩子在任務紀錄單興奮寫下：「老師！我在輕的那邊再加 2 顆小積木，指針就立直平衡了！」把四則加減在手指間化為具體證據。</p>
          </div>
        </div>
      </div>
      <div style="font-size: 13px; color: var(--text-muted);">教學實錄：115.09.26 三年丙班公開試教實踐</div>
    </section>

    <!-- Slide 5: 縱向延展 -->
    <section class="slide" id="slide-5" data-notes="【2:55-3:45 延展】縱向延伸：四年級 micro:bit 甩繩軌跡神射手（科技體育）；高階競賽端：世界機關王梯隊培育（連鎖傳動機構）。">
      <div>
        <div class="slide-badge">校本創客學習地圖</div>
        <h2 class="slide-title">縱向延展 · 跨年級科技與競賽梯隊</h2>
      </div>
      <div class="grid-2">
        <div style="display: flex; flex-direction: column; gap: 10px;">
          <div class="slide-img-frame" style="max-height: 300px;">
            <img src="{img2_b64}" alt="micro:bit 甩繩軌跡神射手">
          </div>
          <h3 style="color: var(--cyan); font-size: 18px;">四年級科技體育：micro:bit 甩繩軌跡</h3>
          <p style="font-size: 14px; color: var(--text-muted);">配戴微型加速度感測器跳繩，視覺化回饋動態發力數據。</p>
        </div>
        <div style="display: flex; flex-direction: column; gap: 10px;">
          <div class="slide-img-frame" style="max-height: 300px;">
            <img src="{img3_b64}" alt="世界機關王競賽指定關卡">
          </div>
          <h3 style="color: var(--orange); font-size: 18px;">中高年級競賽：世界機關王（GM）機關整合</h3>
          <p style="font-size: 14px; color: var(--text-muted);">將天平力矩槓桿原理延展至多道連鎖關卡連續傳動調校。</p>
        </div>
      </div>
      <div style="font-size: 13px; color: var(--text-muted);">從課堂素養扎根，延伸至科技體育與國際級機關競賽</div>
    </section>

    <!-- Slide 6: 成效與數據 -->
    <section class="slide" id="slide-6" data-notes="【3:45-4:25 成效】前後測理解度成長 28.5%，組裝任務 100% 達成；全案 16 節 16,000 元 100% 執行結報，領據成果全數歸檔。">
      <div>
        <div class="slide-badge">全案推動總結</div>
        <h2 class="slide-title">質性與量化推動成效總結</h2>
      </div>
      <div class="grid-3">
        <div class="metric-card" style="border-color: rgba(6, 182, 212, 0.4);">
          <div class="metric-value">+ 28.5%</div>
          <h3 style="font-size: 17px; color: var(--text);">單位概念理解度成長</h3>
          <p style="font-size: 14px; color: var(--text-muted);">課堂前後測數據對比，在公克與公斤換算及天平平衡判定上展現顯著提升。</p>
        </div>
        <div class="metric-card" style="border-color: rgba(34, 197, 94, 0.4);">
          <div class="metric-value" style="color: var(--green);">100 %</div>
          <h3 style="font-size: 17px; color: var(--text);">任務達成與參與率</h3>
          <p style="font-size: 14px; color: var(--text-muted);">全年級試教班級學生全數完成等臂天平機關製作並通過加減微調檢核。</p>
        </div>
        <div class="metric-card" style="border-color: rgba(249, 115, 22, 0.4);">
          <div class="metric-value" style="color: var(--orange);">16節 / 100%</div>
          <h3 style="font-size: 17px; color: var(--text);">鐘點費與行政核銷率</h3>
          <p style="font-size: 14px; color: var(--text-muted);">全年度 7 大活動場次共備研討，16,000 元整經費結報完竣，領據正本已寄達。</p>
        </div>
      </div>
      <div style="font-size: 13px; color: var(--text-muted);">完備三重評量規準：學習單 ＋ 任務紀錄單 ＋ 機關作品評量</div>
    </section>

    <!-- Slide 7: 結語致謝 -->
    <section class="slide" id="slide-7" data-notes="【4:25-4:55 結語】結語：STEAM 不是昂貴器材堆疊，而是讓孩子用雙手把課本公式變成物理奇蹟！感謝教育局與承辦團隊，中正國小謝謝大家！">
      <div>
        <div class="slide-badge">未來展望與致謝</div>
      </div>
      <div style="display: flex; flex-direction: column; align-items: center; justify-content: center; height: 100%; text-align: center; gap: 24px;">
        <h2 style="font-size: clamp(26px, 3.2vw, 42px); line-height: 1.4; color: var(--cyan); font-weight: 900; max-width: 900px;">
          「STEAM 教育不是昂貴的器材堆疊，<br>而是讓孩子用一雙雙手，把課本上的公式變成眼前的物理奇蹟！」
        </h2>
        <div style="font-size: 18px; color: var(--text); font-weight: 600;">
          感謝 臺中市政府教育局 ✕ 國立臺中科技大學 推動校園 STEAM 教育計畫團隊
        </div>
        <div style="font-size: 16px; color: var(--text-muted);">
          臺中市梧棲區中正國民小學 STEAM 教師專業學習社群 敬上
        </div>
      </div>
      <div style="font-size: 13px; color: var(--text-muted); text-align: center;">報告完畢 · 敬請長官前輩不吝指教！</div>
    </section>
  </div>

  <!-- 底部懸浮控制列 -->
  <div class="toolbar">
    <button class="toolbar-btn" id="prevBtn" title="上一頁 (←)">◀ 上一頁</button>
    <div style="font-size: 14px; font-weight: 700;" id="pageIndicator">1 / 7</div>
    <button class="toolbar-btn" id="nextBtn" title="下一頁 (→)">下一頁 ▶</button>
    <div class="timer-display" id="timer">00:00</div>
    <button class="toolbar-btn" id="timerBtn" title="開始/暫停計時">⏱️ 計時</button>
    <button class="toolbar-btn" id="notesBtn" title="講者提詞 (N)">📝 提詞</button>
    <button class="toolbar-btn" id="themeBtn" title="日夜切換 (T)">🌓 主題</button>
    <button class="toolbar-btn" id="fsBtn" title="全螢幕 (F)">⛶ 全螢幕</button>
  </div>

  <!-- 講者提詞懸浮窗 -->
  <div class="notes-drawer" id="notesDrawer">
    <div class="notes-title">
      <span>🎤 講者計時提詞 (5分鐘節奏)</span>
      <span style="cursor: pointer;" id="closeNotes">✕</span>
    </div>
    <div class="notes-text" id="notesContent"></div>
  </div>

  <script>
    const slides = document.querySelectorAll('.slide');
    const totalSlides = slides.length;
    let currentSlide = 0;

    const progressBar = document.getElementById('progressBar');
    const pageIndicator = document.getElementById('pageIndicator');
    const notesDrawer = document.getElementById('notesDrawer');
    const notesContent = document.getElementById('notesContent');
    const timerEl = document.getElementById('timer');
    const timerBtn = document.getElementById('timerBtn');

    // 計時器狀態
    let timerSec = 0;
    let timerInterval = null;

    function formatTime(sec) {{
      const m = String(Math.floor(sec / 60)).padStart(2, '0');
      const s = String(sec % 60).padStart(2, '0');
      return `${{m}}:${{s}}`;
    }}

    function toggleTimer() {{
      if (timerInterval) {{
        clearInterval(timerInterval);
        timerInterval = null;
        timerBtn.textContent = '⏱️ 繼續';
      }} else {{
        timerInterval = setInterval(() => {{
          timerSec++;
          timerEl.textContent = formatTime(timerSec);
          if (timerSec >= 270 && timerSec < 300) {{
            timerEl.style.color = 'var(--orange)';
          }} else if (timerSec >= 300) {{
            timerEl.style.color = 'var(--red)';
          }}
        }}, 1000);
        timerBtn.textContent = '⏸️ 暫停';
      }}
    }}

    function showSlide(index) {{
      if (index < 0 || index >= totalSlides) return;
      slides[currentSlide].classList.remove('active');
      currentSlide = index;
      slides[currentSlide].classList.add('active');

      // 更新進度條與頁碼
      const pct = ((currentSlide + 1) / totalSlides) * 100;
      progressBar.style.width = pct + '%';
      pageIndicator.textContent = `${{currentSlide + 1}} / ${{totalSlides}}`;

      // 更新講者提詞
      const note = slides[currentSlide].getAttribute('data-notes') || '無備忘';
      notesContent.textContent = note;
    }}

    document.getElementById('prevBtn').addEventListener('click', () => showSlide(currentSlide - 1));
    document.getElementById('nextBtn').addEventListener('click', () => showSlide(currentSlide + 1));
    timerBtn.addEventListener('click', toggleTimer);

    document.getElementById('notesBtn').addEventListener('click', () => {{
      notesDrawer.classList.toggle('open');
    }});
    document.getElementById('closeNotes').addEventListener('click', () => {{
      notesDrawer.classList.remove('open');
    }});

    // 主題切換 (T)
    document.getElementById('themeBtn').addEventListener('click', () => {{
      const current = document.documentElement.getAttribute('data-theme');
      const next = current === 'light' ? 'dark' : 'light';
      document.documentElement.setAttribute('data-theme', next);
    }});

    // 全螢幕切換 (F)
    document.getElementById('fsBtn').addEventListener('click', () => {{
      if (!document.fullscreenElement) {{
        document.documentElement.requestFullscreen().catch(() => {{}});
      }} else {{
        document.exitFullscreen();
      }}
    }});

    // 鍵盤導航
    window.addEventListener('keydown', (e) => {{
      if (e.key === 'ArrowRight' || e.key === ' ' || e.key === 'PageDown') {{
        e.preventDefault();
        showSlide(currentSlide + 1);
      }} else if (e.key === 'ArrowLeft' || e.key === 'PageUp') {{
        e.preventDefault();
        showSlide(currentSlide - 1);
      }} else if (e.key === 'f' || e.key === 'F') {{
        document.getElementById('fsBtn').click();
      }} else if (e.key === 't' || e.key === 'T') {{
        document.getElementById('themeBtn').click();
      }} else if (e.key === 'n' || e.key === 'N') {{
        document.getElementById('notesBtn').click();
      }}
    }});

    // 初始化
    const urlParams = new URLSearchParams(window.location.search);
    const slideParam = parseInt(urlParams.get('slide') || '0', 10);
    if (urlParams.get('hide_ui') === '1') {{
      const tb = document.querySelector('.toolbar');
      const pb = document.querySelector('.progress-bar-track');
      if (tb) tb.style.display = 'none';
      if (pb) pb.style.display = 'none';
    }}
    showSlide(slideParam);
  </script>
</body>
</html>
'''

out_html = os.path.join(HTML_DIR, "臺中市梧棲區中正國小_STEAM成果展_5分鐘現場分享會簡報.html")
with open(out_html, "w", encoding="utf-8") as f:
    f.write(html_content)

print(f"🎉 成果展 16:9 現代化網頁簡報 (.html) 已成功產出：{os.path.basename(out_html)}")

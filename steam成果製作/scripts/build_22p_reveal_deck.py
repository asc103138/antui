#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
生成全套 22 頁 Reveal.js 成果展現場簡報 HTML (steam-gigo-balance-deck/index.html 及成果展繳交資料根目錄)
特色：
1. 嚴格符合 Emil Kowalski 全套設計工程工藝標準（零 transition:all、零 scale(0)、:active 微縮、100dvh、字體 >= 16px）。
2. 每頁字體放大 3 倍（h1: 68px, h2: 48px, p: 26px, card-h3: 32px, text: 24px），1920x1080 遠距大螢幕超清晰。
3. 全 22 頁皆具備高解析深邃暗色科技背景底圖，100% 杜絕空白無圖背景。
4. S13 3D 拉桿對比頁具備雙色科技底圖與立體玻璃擬態場景。
5. S16~S21 設置 6 頁專屬「社群歷程回憶錄」相簿，完整收錄 0520、0810、0926、1001、1005、1019 歷次成果及教案附件6工程規格圖與評量表。
6. 100% 規避學生臉部肖像權風險（僅呈現教師共備、板書、教具特寫與教師團隊合影）。
"""

import os
import re

OUTPUT_PATHS = [
    r"d:\antui\steam成果製作\成果展繳交資料\steam-gigo-balance-deck\index.html",
    r"d:\antui\steam成果製作\成果展繳交資料\臺中市梧棲區中正國小_STEAM成果展_5分鐘現場分享會簡報.html"
]

html_template = """<!doctype html>
<html lang="zh-TW">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no, viewport-fit=cover" />
  <meta name="theme-color" content="#090d14" />
  <title>臺中市梧棲區中正國小 - 115年度STEAM教師社群成果展（22頁旗艦版）</title>

  <!-- Reveal.js CDN -->
  <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/reveal.js@4.6.1/dist/reveal.css" />
  <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/reveal.js@4.6.1/dist/theme/black.css" id="theme" />

  <!-- Google Fonts: Noto Sans TC -->
  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
  <link href="https://fonts.googleapis.com/css2?family=Noto+Sans+TC:wght@400;500;700;800;900&family=JetBrains+Mono:wght@600;700&display=swap" rel="stylesheet" />

  <style>
    :root {
      --primary: #0284c7;
      --primary-light: #38bdf8;
      --primary-glow: rgba(56, 189, 248, 0.35);
      --accent: #f59e0b;
      --accent2: #4fc3f7;
      --accent3: #ec4899;
      --success: #10b981;
      --warn: #fb923c;
      --danger: #ef4444;
      --bg-dark: #090d14;
      --card-bg: rgba(15, 23, 42, 0.88);
      --card-border: rgba(56, 189, 248, 0.28);
      --text-main: #f8fafc;
      --text-muted: #94a3b8;
      --font-family: 'Noto Sans TC', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
    }

    * {
      box-sizing: border-box;
      -webkit-tap-highlight-color: transparent;
    }

    body, html {
      margin: 0;
      padding: 0;
      width: 100%;
      height: 100%;
      min-height: 100dvh;
      background-color: var(--bg-dark);
      font-family: var(--font-family);
      color: var(--text-main);
      overflow: hidden;
    }

    .reveal {
      font-family: var(--font-family);
      font-size: 26px;
      line-height: 1.6;
      color: var(--text-main);
    }

    .reveal h1, .reveal h2, .reveal h3, .reveal h4 {
      font-family: var(--font-family);
      font-weight: 800;
      letter-spacing: -0.02em;
      color: #ffffff;
      text-transform: none;
      margin-bottom: 20px;
    }

    .reveal h1 {
      font-size: 68px;
      line-height: 1.25;
      text-shadow: 0 4px 24px rgba(0, 0, 0, 0.8);
    }

    .reveal h2 {
      font-size: 48px;
      line-height: 1.3;
      color: var(--primary-light);
      margin-bottom: 24px;
      text-shadow: 0 3px 18px rgba(0, 0, 0, 0.7);
    }

    .reveal h3 {
      font-size: 32px;
      line-height: 1.35;
      color: #e2e8f0;
      margin-bottom: 12px;
    }

    .reveal p {
      font-size: 26px;
      line-height: 1.65;
      color: #cbd5e1;
      margin-bottom: 20px;
    }

    .lead-text {
      font-size: 28px !important;
      color: #e2e8f0 !important;
      font-weight: 500;
      margin-top: -8px !important;
      margin-bottom: 24px !important;
    }

    /* 卡片風格（Emil Kowalski 物理層級） */
    .glass-card {
      background: var(--card-bg);
      backdrop-filter: blur(16px);
      -webkit-backdrop-filter: blur(16px);
      border: 1px solid var(--card-border);
      border-radius: 20px;
      padding: 28px 32px;
      box-shadow: 0 12px 36px rgba(0, 0, 0, 0.55), 0 0 0 1px rgba(255, 255, 255, 0.05);
      transition: transform 0.25s cubic-bezier(0.23, 1, 0.32, 1), box-shadow 0.25s cubic-bezier(0.23, 1, 0.32, 1), border-color 0.25s cubic-bezier(0.23, 1, 0.32, 1);
      text-align: left;
    }

    .glass-card:hover {
      transform: translateY(-4px);
      border-color: rgba(56, 189, 248, 0.6);
      box-shadow: 0 18px 44px rgba(0, 0, 0, 0.65), 0 0 24px var(--primary-glow);
    }

    .glass-card:active {
      transform: scale(0.97);
    }

    .grid-2 {
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 32px;
      width: 100%;
      margin-top: 16px;
    }

    .grid-3 {
      display: grid;
      grid-template-columns: repeat(3, 1fr);
      gap: 28px;
      width: 100%;
      margin-top: 16px;
    }

    .grid-4 {
      display: grid;
      grid-template-columns: repeat(4, 1fr);
      gap: 24px;
      width: 100%;
      margin-top: 16px;
    }

    /* 徽章 Badge */
    .badge-pill {
      display: inline-block;
      padding: 6px 16px;
      border-radius: 9999px;
      font-size: 20px;
      font-weight: 700;
      letter-spacing: 0.05em;
      text-transform: uppercase;
      user-select: none;
    }

    .badge-cyan {
      background: rgba(56, 189, 248, 0.18);
      color: #38bdf8;
      border: 1px solid rgba(56, 189, 248, 0.4);
    }

    .badge-green {
      background: rgba(16, 185, 129, 0.18);
      color: #34d399;
      border: 1px solid rgba(16, 185, 129, 0.4);
    }

    .badge-amber {
      background: rgba(245, 158, 11, 0.18);
      color: #fbbf24;
      border: 1px solid rgba(245, 158, 11, 0.4);
    }

    .badge-purple {
      background: rgba(168, 85, 247, 0.18);
      color: #c084fc;
      border: 1px solid rgba(168, 85, 247, 0.4);
    }

    /* 回憶錄相簿專屬樣式 */
    .chronicle-grid {
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 36px;
      width: 100%;
      margin-top: 10px;
    }

    .photo-album-card {
      background: rgba(15, 23, 42, 0.88);
      backdrop-filter: blur(14px);
      -webkit-backdrop-filter: blur(14px);
      border: 1px solid rgba(56, 189, 248, 0.32);
      border-radius: 20px;
      overflow: hidden;
      box-shadow: 0 16px 40px rgba(0, 0, 0, 0.65);
      display: flex;
      flex-direction: column;
      transition: transform 0.25s cubic-bezier(0.23, 1, 0.32, 1), box-shadow 0.25s cubic-bezier(0.23, 1, 0.32, 1);
      text-align: left;
    }

    .photo-album-card:hover {
      transform: translateY(-4px);
      box-shadow: 0 20px 48px rgba(0, 0, 0, 0.75), 0 0 24px rgba(56, 189, 248, 0.4);
    }

    .photo-album-card:active {
      transform: scale(0.98);
    }

    .photo-album-card img {
      width: 100%;
      height: 360px;
      object-fit: cover;
      display: block;
      border-bottom: 2px solid rgba(56, 189, 248, 0.3);
    }

    .photo-album-card .caption {
      padding: 22px 26px 26px;
      flex: 1;
    }

    .photo-album-card .tag-session {
      display: inline-block;
      padding: 4px 14px;
      border-radius: 6px;
      font-size: 18px;
      font-weight: 700;
      color: #ffffff;
      background: var(--primary);
      margin-bottom: 10px;
    }

    .photo-album-card .title {
      font-size: 28px;
      font-weight: 800;
      color: #ffffff;
      margin-bottom: 10px;
      line-height: 1.35;
    }

    .photo-album-card .desc {
      font-size: 22px;
      line-height: 1.6;
      color: #cbd5e1;
    }

    /* 3D 比較滑桿元件 */
    .slider-box {
      position: relative;
      height: 520px;
      border-radius: 20px;
      overflow: hidden;
      border: 2px solid rgba(79, 195, 247, 0.4);
      background: #090d14;
      margin-top: 14px;
      box-shadow: 0 16px 40px rgba(0, 0, 0, 0.7);
    }

    .slider-layer {
      position: absolute;
      inset: 0;
      padding: 30px;
      box-sizing: border-box;
      text-align: left;
      font-size: 26px;
      line-height: 1.7;
      overflow-y: auto;
      display: flex;
      align-items: center;
    }

    .slider-layer.before {
      background: #111522 url('images/viz_traditional_scale.png') center/cover no-repeat;
      color: #e0e7ff;
    }

    .slider-layer.after {
      background: #07221d url('images/viz_steam_balance.png') center/cover no-repeat;
      color: #ecfdf5;
      clip-path: inset(0 100% 0 0);
    }

    .slider-glass-card {
      background: rgba(15, 23, 42, 0.88);
      backdrop-filter: blur(14px);
      border-radius: 16px;
      padding: 24px 30px;
      max-width: 680px;
      box-shadow: 0 12px 32px rgba(0, 0, 0, 0.65);
    }

    .slider-glass-card.before {
      border: 1px solid rgba(248, 113, 113, 0.35);
      border-left: 6px solid #ef4444;
    }

    .slider-glass-card.after {
      border: 1px solid rgba(52, 211, 153, 0.35);
      border-left: 6px solid #10b981;
    }

    .slider-divider {
      position: absolute;
      top: 0;
      left: 0;
      width: 4px;
      height: 100%;
      background: linear-gradient(to bottom, transparent, #4fc3f7, #81c784, transparent);
      box-shadow: 0 0 20px #4fc3f7;
      pointer-events: none;
    }

    .slider-ctrl {
      width: 80%;
      margin: 16px auto 0;
      display: block;
      accent-color: #38bdf8;
      height: 10px;
      border-radius: 5px;
      cursor: ew-resize;
    }

    /* 互動文字雲 */
    .cloud-tag {
      display: inline-block;
      margin: 10px 14px;
      padding: 10px 22px;
      border-radius: 14px;
      background: rgba(30, 41, 59, 0.85);
      border: 1px solid rgba(56, 189, 248, 0.3);
      color: #e2e8f0;
      transition: transform 0.2s cubic-bezier(0.23, 1, 0.32, 1), background-color 0.2s cubic-bezier(0.23, 1, 0.32, 1);
      user-select: none;
    }

    .cloud-tag:hover {
      transform: scale(1.06);
      background: rgba(56, 189, 248, 0.25);
      border-color: #38bdf8;
    }

    .cloud-tag:active {
      transform: scale(0.97);
    }

    /* 投票選項按鈕 */
    .poll-btn {
      width: 100%;
      background: rgba(15, 23, 42, 0.85);
      border: 2px solid rgba(56, 189, 248, 0.3);
      border-radius: 16px;
      padding: 18px 24px;
      color: #ffffff;
      font-size: 26px;
      font-weight: 700;
      text-align: left;
      cursor: pointer;
      display: flex;
      justify-content: space-between;
      align-items: center;
      transition: transform 0.2s cubic-bezier(0.23, 1, 0.32, 1), border-color 0.2s cubic-bezier(0.23, 1, 0.32, 1), background 0.2s cubic-bezier(0.23, 1, 0.32, 1);
      user-select: none;
    }

    .poll-btn:hover {
      border-color: #38bdf8;
      background: rgba(56, 189, 248, 0.15);
      transform: translateX(6px);
    }

    .poll-btn:active {
      transform: scale(0.97);
    }

    .poll-btn.correct {
      border-color: #10b981;
      background: rgba(16, 185, 129, 0.2);
    }

    /* 數學策略流程節點 */
    .strategy-node {
      background: rgba(15, 23, 42, 0.9);
      border-radius: 16px;
      padding: 20px 24px;
      border: 1px solid rgba(56, 189, 248, 0.3);
      position: relative;
    }

    /* 課綱表格 */
    .spec-table {
      width: 100%;
      border-collapse: separate;
      border-spacing: 0;
      border-radius: 16px;
      overflow: hidden;
      border: 1px solid rgba(56, 189, 248, 0.35);
      background: rgba(15, 23, 42, 0.85);
      margin-top: 16px;
    }

    .spec-table th, .spec-table td {
      padding: 18px 22px;
      text-align: left;
      font-size: 24px;
    }

    .spec-table th {
      background: rgba(56, 189, 248, 0.15);
      color: #38bdf8;
      font-weight: 800;
      border-bottom: 2px solid rgba(56, 189, 248, 0.3);
    }

    .spec-table td {
      border-bottom: 1px solid rgba(255, 255, 255, 0.08);
      color: #e2e8f0;
    }

    .spec-table tr:last-child td {
      border-bottom: none;
    }

    /* 頁碼導航提示 */
    .deck-footer {
      position: fixed;
      bottom: 14px;
      left: 24px;
      right: 24px;
      display: flex;
      justify-content: space-between;
      align-items: center;
      font-size: 16px;
      color: #64748b;
      pointer-events: none;
      z-index: 100;
    }
  </style>
</head>

<body>
  <div class="reveal">
    <div class="slides">

      <!-- S01: 封面 -->
      <section data-background-image="images/cover_bg.png"
               data-background-opacity="0.36"
               data-background-size="cover">
        <div style="margin-top:40px;">
          <span class="badge-pill badge-cyan" style="font-size:22px; margin-bottom:24px;">
            臺中市 115 年度推動校園 STEAM 教育實施計畫成果展
          </span>
          <h1 style="margin-top:20px; margin-bottom:24px;">
            積木啟發量感 · 機關驗證平衡
          </h1>
          <h2 style="font-size:38px; color:#e0f2fe; font-weight:600; margin-bottom:48px;">
            智高積木融入三年級數學「公斤與公克」重量測量機關課程設計
          </h2>

          <div style="display:inline-flex; align-items:center; gap:20px; background:rgba(15,23,42,0.85); padding:16px 36px; border-radius:9999px; border:1px solid rgba(56,189,248,0.4); box-shadow:0 12px 30px rgba(0,0,0,0.6);">
            <span style="font-size:26px; color:#f8fafc; font-weight:700;">承辦學校：臺中市梧棲區中正國小</span>
            <span style="color:#38bdf8; font-size:26px;">｜</span>
            <span style="font-size:26px; color:#f8fafc; font-weight:700;">社群召集人：謝敦元 老師</span>
          </div>
        </div>
      </section>

      <!-- S02: 社群推動脈絡 -->
      <section data-background-image="images/bgs/bg_team.png"
               data-background-opacity="0.32"
               data-background-size="cover">
        <h2>社群推動脈絡：踏實共備與 100% 執行</h2>
        <p class="lead-text">
          由校內數學、自然與資訊專長教師跨域組成，歷經 7 場次高密度共備與入班實踐：
        </p>

        <div class="grid-4">
          <div class="glass-card">
            <div style="font-size:44px; margin-bottom:12px;">👥</div>
            <div style="color:#38bdf8; font-weight:800; font-size:32px; margin-bottom:8px;">4 位核心教師</div>
            <p style="font-size:22px; color:#cbd5e1; margin:0;">
              召集人謝敦元、李仁耀、曾泊淞、王怡婷，專長涵蓋國小數學、創客機械與資訊科技。
            </p>
          </div>

          <div class="glass-card">
            <div style="font-size:44px; margin-bottom:12px;">📅</div>
            <div style="color:#34d399; font-weight:800; font-size:32px; margin-bottom:8px;">7 場研習與觀課</div>
            <p style="font-size:22px; color:#cbd5e1; margin:0;">
              從教材迷思剖析、跨校赴南投鯉魚國小創客參訪、公開試教到前後測成效研討。
            </p>
          </div>

          <div class="glass-card">
            <div style="font-size:44px; margin-bottom:12px;">⏱️</div>
            <div style="color:#fbbf24; font-weight:800; font-size:32px; margin-bottom:8px;">16 節充實課程</div>
            <p style="font-size:22px; color:#cbd5e1; margin:0;">
              每場次落實 2~3 節深度共備研討與實體機構除錯，課堂公開試教完整記錄。
            </p>
          </div>

          <div class="glass-card">
            <div style="font-size:44px; margin-bottom:12px;">💰</div>
            <div style="color:#c084fc; font-weight:800; font-size:32px; margin-bottom:8px;">16,000 元整</div>
            <p style="font-size:22px; color:#cbd5e1; margin:0;">
              全案鐘點費 16 節 16,000 元 100% 執行核銷完畢，成果表、簽到表與領據全備齊。
            </p>
          </div>
        </div>
      </section>

      <!-- S03: 現場互動提問 (文字雲) -->
      <section data-background-image="images/bgs/bg_wordcloud.png"
               data-background-opacity="0.32"
               data-background-size="cover">
        <h2>現場互動提問：提到國小「重量測量」，學生最常卡在哪？</h2>
        <p class="lead-text">
          請現場各位教育夥伴與評審委員回想日常課堂，點擊下方高頻困境：
        </p>

        <div style="margin-top:24px; padding:24px; background:rgba(15,23,42,0.85); border-radius:20px; border:1px solid rgba(56,189,248,0.3);">
          <div class="cloud-tag" style="font-size:36px; color:#f87171; border-color:#f87171;">
            🔥 彈簧秤指針未歸零 (32%)
          </div>
          <div class="cloud-tag" style="font-size:40px; color:#38bdf8; font-weight:800; border-color:#38bdf8;">
            ⭐ 刻度格值看錯 (38%)
          </div>
          <div class="cloud-tag" style="font-size:32px; color:#fbbf24; border-color:#fbbf24;">
            ⚠️ 公斤與公克換算障礙 (24%)
          </div>
          <br />
          <div class="cloud-tag" style="font-size:34px; color:#34d399; border-color:#34d399;">
            💡 誤認「體積大一定重」 (29%)
          </div>
          <div class="cloud-tag" style="font-size:30px; color:#c084fc; border-color:#c084fc;">
            📦 缺乏實體量感直覺 (27%)
          </div>
          <div class="cloud-tag" style="font-size:28px; color:#94a3b8; border-color:#94a3b8;">
            📝 兩步驟加減解題機械化 (21%)
          </div>
        </div>

        <div style="margin-top:28px; font-size:24px; color:#cbd5e1; font-weight:500;">
          👉 這些痛點的根源：傳統課堂依賴「市售黑盒子彈簧秤」，學生只看讀數，缺少<span style="color:#38bdf8; font-weight:700;">「物理結構支撐」</span>與<span style="color:#34d399; font-weight:700;">「手動調校過程」</span>！
        </div>
      </section>

      <!-- S04: 教學痛點診斷 -->
      <section data-background-image="images/bgs/bg_steam.png"
               data-background-opacity="0.32"
               data-background-size="cover">
        <h2>教學痛點診斷：從「黑盒子讀數」到「物理具象」</h2>
        <p class="lead-text">
          依據南一版三年級上學期第六單元教材分析，拆解傳統教學三大壁壘：
        </p>

        <div class="grid-3">
          <div class="glass-card" style="border-left:6px solid #ef4444;">
            <div style="font-size:40px; margin-bottom:12px;">❌</div>
            <h3 style="color:#f87171;">痛點一：刻度密麻與未歸零</h3>
            <p style="font-size:22px; color:#cbd5e1; margin:0;">
              市售彈簧秤 1 大格 100g 內含 5 小格，學生常直覺誤認一小格為 10g；且指針未調零便直接判讀，誤差累積。
            </p>
          </div>

          <div class="glass-card" style="border-left:6px solid #f59e0b;">
            <div style="font-size:40px; margin-bottom:12px;">⚡</div>
            <h3 style="color:#fbbf24;">痛點二：抽象單位換算障礙</h3>
            <p style="font-size:22px; color:#cbd5e1; margin:0;">
              「1 公斤 = 1000 公克」淪為數字背誦，學生面對 2 公斤 50 公克常誤寫成 2500 公克，欠缺體感重量基準。
            </p>
          </div>

          <div class="glass-card" style="border-left:6px solid #38bdf8;">
            <div style="font-size:40px; margin-bottom:12px;">🔄</div>
            <h3 style="color:#38bdf8;">痛點三：生活應用與算則脫節</h3>
            <p style="font-size:22px; color:#cbd5e1; margin:0;">
              課本兩步驟加減題目（如裝箱去皮、兩物補平）缺乏具象操作，學生只能死套公式，無法連結真實生活情境。
            </p>
          </div>
        </div>
      </section>

      <!-- S05: 課綱指標對齊 -->
      <section data-background-image="images/bgs/bg_curriculum.png"
               data-background-opacity="0.32"
               data-background-size="cover">
        <h2>課程核心依據：十二年國教數學領域指標對齊</h2>
        <p class="lead-text">
          緊密扣合課綱學習表現與學習內容，落實跨領域素養導向設計：
        </p>

        <table class="spec-table">
          <thead>
            <tr>
              <th style="width:20%;">課綱代碼</th>
              <th style="width:38%;">學習內容 / 表現條目</th>
              <th style="width:42%;">智高積木 STEAM 課程轉化重點</th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td style="color:#38bdf8; font-weight:800; font-family:'JetBrains Mono';">n-II-8</td>
              <td>認識重量單位「公斤」、「公克」及其關係，並做相關計算。</td>
              <td>以智高 5g 單位積木為基底，透過逐個疊加累積至 100g、500g，實體建立量感基準。</td>
            </tr>
            <tr>
              <td style="color:#34d399; font-weight:800; font-family:'JetBrains Mono';">n-II-9</td>
              <td>理解等臂天平原理，進行重量的直接比較與間接比較。</td>
              <td>動手組裝 20 孔等臂機構，透過指針中線垂直判定平衡，理解槓桿力矩對稱性。</td>
            </tr>
            <tr>
              <td style="color:#fbbf24; font-weight:800; font-family:'JetBrains Mono';">n-II-2</td>
              <td>熟練兩步驟四則問題，並能合理解釋解題過程。</td>
              <td>將加減法具象化為天平增減積木：傾斜時「加法補平」或「減法移除」，化抽象為操作。</td>
            </tr>
          </tbody>
        </table>
      </section>

      <!-- S06: 三節課循序架構 -->
      <section data-background-image="images/bgs/bg_roadmap.png"
               data-background-opacity="0.32"
               data-background-size="cover">
        <h2>三節課循序進階架構：階梯式探究地圖</h2>
        <p class="lead-text">
          設計由感官到結構、再由結構到數理計量的完整學習進程：
        </p>

        <div class="grid-3">
          <div class="glass-card">
            <span class="badge-pill badge-amber">第 1 節 ｜ 40 min</span>
            <h3 style="color:#fbbf24; margin-top:14px;">手感掂重引爆認知衝突</h3>
            <p style="font-size:22px; color:#cbd5e1;">
              • 盲測比較保麗龍與金屬球。<br>
              • 破除「體積大一定重」的直覺謬誤。<br>
              • 體會手部疲勞誤差，引出對精準測量工具的渴望。
            </p>
          </div>

          <div class="glass-card">
            <span class="badge-pill badge-cyan">第 2 節 ｜ 40 min</span>
            <h3 style="color:#38bdf8; margin-top:14px;">智高積木等臂機構組裝</h3>
            <p style="font-size:22px; color:#cbd5e1;">
              • 掌握梯形底座、對稱橫樑與低阻尼轉軸。<br>
              • 解決卡榫摩擦力問題，完成指針歸零。<br>
              • 透過指針傾斜直觀辨識輕重與水平平衡。
            </p>
          </div>

          <div class="glass-card">
            <span class="badge-pill badge-green">第 3 節 ｜ 40 min</span>
            <h3 style="color:#34d399; margin-top:14px;">公克積木微調與生活應用</h3>
            <p style="font-size:22px; color:#cbd5e1;">
              • 5g 單位積木加減微調解題。<br>
              • 兩步驟加減法情境具象操作實證。<br>
              • 小組合作秤量文具、玩具等生活物品並記錄。
            </p>
          </div>
        </div>
      </section>

      <!-- S07: 第 1 節課堂實踐 -->
      <section data-background-image="images/conflict_bg.png"
               data-background-opacity="0.32"
               data-background-size="cover">
        <h2>第 1 節課堂實踐：徒手掂重引爆認知衝突</h2>
        <p class="lead-text">
          利用「視覺體積」與「真實重量」的巨大落差，製造強烈教學鷹架：
        </p>

        <div class="grid-2">
          <div class="glass-card" style="border-left:6px solid #fb923c;">
            <h3 style="color:#fb923c;">📦 認知衝突實驗：大保麗龍 vs 小鐵球</h3>
            <p style="font-size:24px; color:#e2e8f0; line-height:1.7;">
              • 學生單憑雙眼觀察，92% 直覺猜測體積大 5 倍的保麗龍方塊較重。<br>
              • 當雙手捧起閉眼盲測時，震撼發現掌心下沉的反而是小小金屬球！<br>
              • 瞬間瓦解「大 = 重」的直覺迷思，課堂討論氣氛瞬間點燃。
            </p>
          </div>

          <div class="glass-card" style="border-left:6px solid #38bdf8;">
            <h3 style="color:#38bdf8;">✋ 雙手掂重限制：感官疲勞與主觀爭議</h3>
            <p style="font-size:24px; color:#e2e8f0; line-height:1.7;">
              • 兩件物品重量相近時（如 85g 橡皮擦 vs 90g 膠水），組內同學互換手感各執一詞。<br>
              • 手腕肌肉快速疲勞導致估測失真，全班一致達成共識：<br>
              <span style="color:#34d399; font-weight:800; font-size:26px;">「我們需要客觀、穩定、不會累的科學測量工具！」</span>
            </p>
          </div>
        </div>
      </section>

      <!-- S08: 第 2 節課堂實踐 -->
      <section data-background-image="images/bgs/bg_assembly.png"
               data-background-opacity="0.32"
               data-background-size="cover">
        <h2>第 2 節課堂實踐：智高積木四核心組件組裝</h2>
        <p class="lead-text">
          工程設計歷程（EDP）：拆解結構細節，化身小小工程師：
        </p>

        <div class="grid-4">
          <div class="glass-card">
            <span class="badge-pill badge-cyan">組件 A</span>
            <h3 style="color:#38bdf8; margin-top:10px;">穩固梯形基座</h3>
            <p style="font-size:22px; color:#cbd5e1;">
              三角形與梯形幾何加固，提供極致平穩低重心，避免量測時傾倒。
            </p>
          </div>

          <div class="glass-card">
            <span class="badge-pill badge-green">組件 B</span>
            <h3 style="color:#34d399; margin-top:10px;">20 孔對稱橫樑</h3>
            <p style="font-size:22px; color:#cbd5e1;">
              支點居中，左右各 10 孔完全對稱，確保槓桿力臂長度分毫不差。
            </p>
          </div>

          <div class="glass-card">
            <span class="badge-pill badge-amber">組件 C</span>
            <h3 style="color:#fbbf24; margin-top:10px;">低阻尼轉軸</h3>
            <p style="font-size:22px; color:#cbd5e1;">
              嚴選光滑軸套，消除卡榫摩擦力，讓微小 2g 重量變化也能靈敏擺動。
            </p>
          </div>

          <div class="glass-card">
            <span class="badge-pill badge-purple">組件 D</span>
            <h3 style="color:#c084fc; margin-top:10px;">懸吊測量盤</h3>
            <p style="font-size:22px; color:#cbd5e1;">
              雙繩垂直吊掛承物盤，承載各式生活待測物，確保重力垂直向下。
            </p>
          </div>
        </div>
      </section>

      <!-- S09: 物理機制解析 -->
      <section data-background-image="images/bgs/bg_physics.png"
               data-background-opacity="0.32"
               data-background-size="cover">
        <h2>物理機制解析：天平傾斜與指針判定規則</h2>
        <p class="lead-text">
          手動調校零點，建立清楚直觀的力學視覺辨識語言：
        </p>

        <div class="grid-3">
          <div class="glass-card" style="text-align:center;">
            <div style="font-size:52px; margin-bottom:10px;">↙️</div>
            <h3 style="color:#f87171;">左盤下沉 · 指針偏右</h3>
            <p style="font-size:24px; color:#e2e8f0; font-weight:700;">左邊物體較重 (Left > Right)</p>
            <p style="font-size:20px; color:#cbd5e1;">重力力矩較大，需在右盤追加砝碼或減少左盤重量。</p>
          </div>

          <div class="glass-card" style="text-align:center; border:2px solid #10b981; box-shadow:0 0 24px rgba(16,185,129,0.3);">
            <div style="font-size:52px; margin-bottom:10px;">⚖️</div>
            <h3 style="color:#34d399;">指針鉛直 · 兩端齊平</h3>
            <p style="font-size:24px; color:#a7f3d0; font-weight:700;">達成完美平衡 (Left = Right)</p>
            <p style="font-size:20px; color:#cbd5e1;">力矩完美對稱抵消，此時兩側物品重量完全相等。</p>
          </div>

          <div class="glass-card" style="text-align:center;">
            <div style="font-size:52px; margin-bottom:10px;">↘️</div>
            <h3 style="color:#60a5fa;">右盤下沉 · 指針偏左</h3>
            <p style="font-size:24px; color:#e2e8f0; font-weight:700;">右邊物體較重 (Right > Left)</p>
            <p style="font-size:20px; color:#cbd5e1;">右側力矩過大，需在左盤追加單位積木直至鉛直平衡。</p>
          </div>
        </div>
      </section>

      <!-- S10: 課堂迷思快問快答 -->
      <section data-background-image="images/bgs/bg_poll.png"
               data-background-opacity="0.32"
               data-background-size="cover">
        <h2>課堂迷思快問快答：破除「體積大就一定重」</h2>
        <p class="lead-text">
          課堂即時互動環節，檢驗學生對體積與質量概念的釐清：
        </p>

        <div style="max-width:960px; margin:0 auto; text-align:left;">
          <div style="background:rgba(30,41,59,0.9); padding:24px 30px; border-radius:18px; margin-bottom:24px; border-left:6px solid #38bdf8;">
            <span style="font-size:28px; font-weight:800; color:#ffffff;">
              ❓ 課堂快問：若天平左邊放「大棉花團」、右邊放「小金屬塊」，指針鉛直平衡，兩者誰重？
            </span>
          </div>

          <div style="display:flex; flex-direction:column; gap:16px;">
            <div class="poll-btn" onclick="this.classList.toggle('correct')">
              <span>A. 棉花團體積大很多，所以棉花較重</span>
              <span style="color:#94a3b8; font-size:22px;">課前 38% 學生誤選</span>
            </div>

            <div class="poll-btn correct">
              <span>B. 指針垂直中線，兩者重量完全一樣重！ ✅</span>
              <span style="color:#34d399; font-weight:800; font-size:22px;">課後 98% 學生正解！</span>
            </div>

            <div class="poll-btn">
              <span>C. 金屬密度大，所以一定是小金屬塊比較重</span>
              <span style="color:#94a3b8; font-size:22px;">課前 18% 學生誤選</span>
            </div>
          </div>
        </div>
      </section>

      <!-- S11: 第 3 節課堂實踐 -->
      <section data-background-image="images/balance_bg.png"
               data-background-opacity="0.32"
               data-background-size="cover">
        <h2>第 3 節課堂實踐：單位積木與加減微調挑戰</h2>
        <p class="lead-text">
          引導學生從「非標準單位」邁向「標準公克單位」的認知跳躍：
        </p>

        <div class="grid-3">
          <div class="glass-card">
            <span class="badge-pill badge-amber">關卡一</span>
            <h3 style="color:#fbbf24; margin-top:12px;">個別單位到公克標準</h3>
            <p style="font-size:22px; color:#cbd5e1;">
              • 先用花片、彈珠當單位，發現每組花片重量不一。<br>
              • 深刻體會「全世界需要統一標準」的公克制度重要性。
            </p>
          </div>

          <div class="glass-card">
            <span class="badge-pill badge-cyan">關卡二</span>
            <h3 style="color:#38bdf8; margin-top:12px;">5g 智高積木精準定量</h3>
            <p style="font-size:22px; color:#cbd5e1;">
              • 標準智高正方體積木每顆恰為 5 公克。<br>
              • 學生數算顆數乘 5，直觀連結乘法倍數與重量數值。
            </p>
          </div>

          <div class="glass-card">
            <span class="badge-pill badge-green">關卡三</span>
            <h3 style="color:#34d399; margin-top:12px;">加減微調平衡挑戰</h3>
            <p style="font-size:22px; color:#cbd5e1;">
              • 小組挑戰秤量鉛筆盒，在另一盤加減微調。<br>
              • 算式與指針即時連動，成功完成課堂任務單。
            </p>
          </div>
        </div>
      </section>

      <!-- S12: 課堂深度探究 -->
      <section data-background-image="images/bgs/bg_math_strategy.png"
               data-background-opacity="0.32"
               data-background-size="cover">
        <h2>課堂深度探究：兩步驟加減法情境具象化</h2>
        <p class="lead-text">
          將數學課本抽象文字題，轉化為看得見、摸得著的動態操作：
        </p>

        <div class="grid-2">
          <div class="glass-card" style="border-left:6px solid #38bdf8;">
            <div class="badge-pill badge-cyan" style="margin-bottom:12px;">情境一：加法補足策略</div>
            <h3 style="color:#38bdf8;">左盤放 50g 蘋果，右盤已放 35g 積木</h3>
            <p style="font-size:24px; color:#e2e8f0; line-height:1.7;">
              • 現象：天平左傾，指針偏右。<br>
              • 思考：要使指針歸零平衡，右盤還需要加多少公克？<br>
              • 操作：右盤再補進 3 顆 5g 積木（+15g）。<br>
              • 算式：35 + 15 = 50（公克）。手動補平驗證算則！
            </p>
          </div>

          <div class="glass-card" style="border-left:6px solid #34d399;">
            <div class="badge-pill badge-green" style="margin-bottom:12px;">情境二：減法移除策略</div>
            <h3 style="color:#34d399;">扣除包裝盒皮重（去皮計算）</h3>
            <p style="font-size:24px; color:#e2e8f0; line-height:1.7;">
              • 現象：連盒帶物共 80g，已知空紙盒重 20g。<br>
              • 思考：內容物真正重量是多少？<br>
              • 操作：從天平砝碼盤中直接取下代表盒重的 4 顆 5g 積木。<br>
              • 算式：80 - 20 = 60（公克）。徹底根除學生對去皮運算的困惑！
            </p>
          </div>
        </div>
      </section>

      <!-- S13: 典範轉移 3D 拉桿 -->
      <section data-background-image="images/bgs/bg_paradigm.png"
               data-background-opacity="0.32"
               data-background-size="cover">
        <h2>教學典範轉移：傳統讀秤 vs STEAM 動手調校</h2>
        <p class="lead-text">
          拖動下方滑桿，對照傳統教學困境與 STEAM 跨域實作的巨大轉變：
        </p>

        <div class="slider-box">
          <div class="slider-layer before">
            <div class="slider-glass-card before">
              <div style="color:#f87171; font-weight:800; font-size:32px; margin-bottom:12px;">❌ 傳統課堂痛點（代碼 M3-W-01）</div>
              <p style="font-size:24px; line-height:1.6; color:#e2e8f0; margin:0;">
                • 面對市售彈簧秤，指針未歸零卻直接判讀。<br>
                • 刻度密密麻麻，學生常把「1大格100g、5小格」誤算為一小格 10g。<br>
                • 抽象死背「1公斤 = 1000公克」，卻無法直觀感受 1 公斤到底多重。<br>
                • 算式寫得漂亮，但一到真實生活買水果或稱重時完全失靈。
              </p>
              <div style="color:#fca5a5; margin-top:14px; font-size:22px; font-weight:700;">
                ⚠️ 缺失：缺乏物理實體感知，量感沒有真正內化為直覺。
              </div>
            </div>
          </div>

          <div class="slider-layer after" id="viz-after">
            <div class="slider-glass-card after">
              <div style="color:#34d399; font-weight:800; font-size:32px; margin-bottom:12px;">✅ STEAM 動手調校新典範</div>
              <p style="font-size:24px; line-height:1.6; color:#ecfdf5; margin:0;">
                • 親手組裝等臂力臂，徹底理解為什麼指針歸零如此關鍵。<br>
                • 透過 5g 小積木的逐個疊加，深刻體會非標準單位到標準單位的進程。<br>
                • 算則直接轉化為手部動作：較輕就「加法補足」、較重就「減法移除」。<br>
                • 建立深厚體感量感，課堂充滿主動除錯與興奮歡呼聲！
              </p>
              <div style="color:#a7f3d0; margin-top:14px; font-size:22px; font-weight:700;">
                ✨ 成果：前後測理解度大躍進，小組合作與探究自信心爆棚！
              </div>
            </div>
          </div>

          <div class="slider-divider" id="viz-divider"></div>
        </div>

        <input type="range" min="0" max="100" value="0" class="slider-ctrl" id="viz-slider" />
        <div style="display:flex; justify-content:space-between; width:80%; margin:8px auto 0; font-size:24px; color:#cbd5e1; font-weight:700;">
          <span>👈 拖曳查看【傳統教學痛點】</span>
          <span>拖曳查看【STEAM 動手典範】 👉</span>
        </div>
      </section>

      <!-- S14: 縱向延展 (一) micro:bit -->
      <section data-background-image="images/bgs/bg_microbit.png"
               data-background-opacity="0.32"
               data-background-size="cover">
        <h2>社群成果縱向延展 (一)：四年級 micro:bit 甩繩智動量測</h2>
        <p class="lead-text">
          將重量與感測概念無縫銜接至四年級跨域科技與體育健康課程：
        </p>

        <div class="grid-3">
          <div class="glass-card">
            <div style="font-size:44px; margin-bottom:10px;">🏃</div>
            <h3 style="color:#38bdf8;">體育跨域：甩繩軌跡神射手</h3>
            <p style="font-size:22px; color:#cbd5e1;">
              將 micro:bit 晶片固定於跳繩握把，利用內建 3 軸加速度計即時感測學生甩繩頻率與加速度峰值。
            </p>
          </div>

          <div class="glass-card">
            <div style="font-size:44px; margin-bottom:10px;">📡</div>
            <h3 style="color:#34d399;">物聯網傳輸：即時數據回饋</h3>
            <p style="font-size:22px; color:#cbd5e1;">
              透過藍牙 Radio 廣播將跳繩次數與動能曲線即時投影於大螢幕，激發學生運動自主挑戰慾望。
            </p>
          </div>

          <div class="glass-card">
            <div style="font-size:44px; margin-bottom:10px;">📊</div>
            <h3 style="color:#fbbf24;">數學統計：次數折線圖繪製</h3>
            <p style="font-size:22px; color:#cbd5e1;">
              結合四年級統計圖表單元，將運動大數據轉化為個人化體適能折線圖，完美展現科技賦能教育價值。
            </p>
          </div>
        </div>
      </section>

      <!-- S15: 縱向延展 (二) 機關王 -->
      <section data-background-image="images/bgs/bg_gm.png"
               data-background-opacity="0.32"
               data-background-size="cover">
        <h2>社群成果縱向延展 (二)：世界機關王 (GM) 校隊梯隊</h2>
        <p class="lead-text">
          將微型天平槓桿原理，昇華為大型競賽連續連鎖動態關卡：
        </p>

        <div class="grid-3">
          <div class="glass-card">
            <div style="font-size:44px; margin-bottom:10px;">⚙️</div>
            <h3 style="color:#38bdf8;">機構整合：重力觸發關卡</h3>
            <p style="font-size:22px; color:#cbd5e1;">
              將三年級所學等臂天平改裝為「重力傾斜開關」，當鋼珠滾入托盤時觸發下一階段連鎖機構。
            </p>
          </div>

          <div class="glass-card">
            <div style="font-size:44px; margin-bottom:10px;">🔄</div>
            <h3 style="color:#34d399;">8 迴連鎖：複合齒輪傳動</h3>
            <p style="font-size:22px; color:#cbd5e1;">
              結合減速齒輪箱、滾珠軌道與凸輪機構，完成世界機關王競賽指定之 8 迴連續動作，穩定度達 90% 以上。
            </p>
          </div>

          <div class="glass-card">
            <div style="font-size:44px; margin-bottom:10px;">🏆</div>
            <h3 style="color:#fbbf24;">校隊培訓：高階創客小組</h3>
            <p style="font-size:22px; color:#cbd5e1;">
              由社群教師利用午休與社團時間，帶領 12 位熱愛動手的梯隊學生備戰臺中市賽與全國賽。
            </p>
          </div>
        </div>
      </section>

      <!-- S16: 社群歷程回憶錄 (一) -->
      <section data-background-image="images/bgs/bg_chronicle_01.png"
               data-background-opacity="0.32"
               data-background-size="cover">
        <h2>社群歷程回憶錄 (一)：萌芽共備與原型研發</h2>
        <p class="lead-text">
          記錄中正國小社群教師全員從零開始共備、拆解迷思的踏實足跡：
        </p>

        <div class="chronicle-grid">
          <div class="photo-album-card fragment">
            <img src="images/chronicle/c01_0520_kickoff_discussion.jpg" alt="0520啟動共備" />
            <div class="caption">
              <span class="tag-session">第 1 場次 ｜ 115.05.20</span>
              <div class="title">社群正式啟動：教材迷思剖析與共備奠基</div>
              <div class="desc">
                四位社群教師齊聚創客研討室，逐條檢驗三年級數學「公斤與公克」學習痛點，開箱智高積木零件庫，確立以自製天平機關為核心的年度研發主軸。
              </div>
            </div>
          </div>

          <div class="photo-album-card fragment">
            <img src="images/chronicle/c02_0520_parts_assembly.jpg" alt="0520原型組裝" />
            <div class="caption">
              <span class="tag-session" style="background:var(--accent);">第 1 場次 ｜ 115.05.20</span>
              <div class="title">機構研發：智高零件庫開箱與天平雛型組裝</div>
              <div class="desc">
                親手測試 20 孔橫樑、梯形基座與轉軸阻尼，克服卡榫摩擦力干擾，順利完成第一代重量比較機關原型機，奠定後續入班試教之硬體基礎。
              </div>
            </div>
          </div>
        </div>
      </section>

      <!-- S17: 社群歷程回憶錄 (二) -->
      <section data-background-image="images/bgs/bg_chronicle_02.png"
               data-background-opacity="0.32"
               data-background-size="cover">
        <h2>社群歷程回憶錄 (二)：校際參訪與創客交流</h2>
        <p class="lead-text">
          社群走出校園跨校取經，向世界機關王指導名師深度請益：
        </p>

        <div class="chronicle-grid">
          <div class="photo-album-card fragment">
            <img src="images/chronicle/c03_0810_liyu_maker_visit.jpg" alt="0810鯉魚國小參訪" />
            <div class="caption">
              <span class="tag-session" style="background:var(--warn);">第 3 場次 ｜ 115.08.10</span>
              <div class="title">跨校共學：南投縣鯉魚國小創客基地走訪</div>
              <div class="desc">
                社群團隊赴南投鯉魚國小實地觀摩，特聘陳建安老師深度座談，交流機構整合技巧、積木材料管理系統與競賽訓練梯隊之實戰經驗。
              </div>
            </div>
          </div>

          <div class="photo-album-card fragment">
            <img src="images/chronicle/c04_0810_chen_sharing.jpg" alt="0810名師分享" />
            <div class="caption">
              <span class="tag-session" style="background:#0284c7;">第 3 場次 ｜ 115.08.10</span>
              <div class="title">名師引領：陳建安老師機關王賽事機構傳承</div>
              <div class="desc">
                陳建安老師親自示範連續傳動與槓桿觸發核心機構，為中正社群注入強大研發動能，並將競賽技術成功降轉為國小三年級課堂適用之天平教具。
              </div>
            </div>
          </div>
        </div>
      </section>

      <!-- S18: 社群歷程回憶錄 (三) -->
      <section data-background-image="images/bgs/bg_chronicle_03.png"
               data-background-opacity="0.32"
               data-background-size="cover">
        <h2>社群歷程回憶錄 (三)：課堂實踐與公開觀議課</h2>
        <p class="lead-text">
          真實走入教學現場公開試教，以嚴謹板書架構與科技實測雙軌並進：
        </p>

        <div class="chronicle-grid">
          <div class="photo-album-card fragment">
            <img src="images/chronicle/c05_0926_teaching_blackboard.jpg" alt="0926入班試教板書" />
            <div class="caption">
              <span class="tag-session" style="background:var(--success);">第 4 場次 ｜ 115.09.26</span>
              <div class="title">入班公開課：三年丙班黑板板書架構與量感階梯</div>
              <div class="desc">
                在三年丙班進行公開觀議課，板書清楚標註公斤與公克位值轉換表，全班學生動手操作等臂天平，實作參與度高達 100%，觀課教師詳實記錄反思。
              </div>
            </div>
          </div>

          <div class="photo-album-card fragment">
            <img src="images/chronicle/c06_1001_microbit_sports.jpg" alt="1001科技跨域" />
            <div class="caption">
              <span class="tag-session" style="background:#06b6d4;">第 5 場次 ｜ 115.10.01</span>
              <div class="title">科技跨域：四年級 micro:bit 運動軌跡動態實測</div>
              <div class="desc">
                李仁耀老師引導學生將 micro:bit 結合跳繩運動，在操場與體育館即時串流加速度數值，將靜態數學計算昇華為動態感測體適能大數據。
              </div>
            </div>
          </div>
        </div>
      </section>

      <!-- S19: 社群歷程回憶錄 (四) -->
      <section data-background-image="images/bgs/bg_chronicle_04.png"
               data-background-opacity="0.32"
               data-background-size="cover">
        <h2>社群歷程回憶錄 (四)：成效研析與機關精進</h2>
        <p class="lead-text">
          秉持嚴謹科學實證精神，以前後測量化數據引導教具與教案反覆優化：
        </p>

        <div class="chronicle-grid">
          <div class="photo-album-card fragment">
            <img src="images/chronicle/c07_1005_analysis_review.jpg" alt="1005成效分析" />
            <div class="caption">
              <span class="tag-session" style="background:var(--accent);">第 6 場次 ｜ 115.10.05</span>
              <div class="title">成效量化：試教前後測答題數據深度研析</div>
              <div class="desc">
                曾泊淞與謝敦元老師接力主持，逐題比對試教前後測卷。數據證實學生在「指針讀數」與「單位換算」答對率提升 28.5%，學習成效極為顯著。
              </div>
            </div>
          </div>

          <div class="photo-album-card fragment">
            <img src="images/chronicle/c08_1005_mechanism_tuning.jpg" alt="1005機構精修" />
            <div class="caption">
              <span class="tag-session" style="background:#3b82f6;">第 6 場次 ｜ 115.10.05</span>
              <div class="title">機構精修：卡榫精度升級與指針刻度標準化</div>
              <div class="desc">
                依據觀課回饋，針對積木轉軸阻尼與指針長度進行微調改良，增設清晰的「零點鉛直基準線」，定稿最適合國小學童操作之第二代標準教具。
              </div>
            </div>
          </div>
        </div>
      </section>

      <!-- S20: 社群歷程回憶錄 (五) -->
      <section data-background-image="images/bgs/bg_chronicle_05.png"
               data-background-opacity="0.32"
               data-background-size="cover">
        <h2>社群歷程回憶錄 (五)：機關王 8 迴整合與團隊合影</h2>
        <p class="lead-text">
          將課堂微型天平無縫昇華為世界機關王 8 迴連鎖關卡，完美收官：
        </p>

        <div class="chronicle-grid">
          <div class="photo-album-card fragment">
            <img src="images/chronicle/c09_1019_gm_mechanism_8loops.jpg" alt="1019機關王8迴" />
            <div class="caption">
              <span class="tag-session" style="background:#a855f7;">第 7 場次 ｜ 115.10.19</span>
              <div class="title">競賽昇華：世界機關王 A-H 區 8 迴連續連鎖機構</div>
              <div class="desc">
                在活動中心全面整合複合機關，串聯天平重力傾斜開關與減速齒輪箱，完成 8 道關卡連續作動，實體驗證連鎖觸發順暢率超越 90%！
              </div>
            </div>
          </div>

          <div class="photo-album-card fragment">
            <img src="images/chronicle/c10_1019_team_celebration.jpg" alt="1019團隊大合影" />
            <div class="caption">
              <span class="tag-session" style="background:#ec4899;">年度完美收官 ｜ 115.10.19</span>
              <div class="title">社群大合影：四位教師 100% 執行圓滿結報</div>
              <div class="desc">
                謝敦元、李仁耀、曾泊淞、王怡婷四位老師攜手走過 7 場高密度共備與公開試教，16 節課程 16,000 元整無瑕結報，展現中正教育熱忱！
              </div>
            </div>
          </div>
        </div>
      </section>

      <!-- S21: 社群歷程回憶錄 (六) -->
      <section data-background-image="images/bgs/bg_chronicle_06.png"
               data-background-opacity="0.32"
               data-background-size="cover">
        <h2>社群歷程回憶錄 (六)：教案設計正式藍圖與評量規準</h2>
        <p class="lead-text">
          依教育局規定完整繳交之附件 6 正式教案設計，內嵌標準工程藍圖：
        </p>

        <div class="chronicle-grid">
          <div class="photo-album-card fragment">
            <img src="images/chronicle/c11_plan_structure_spec.png" alt="教案藍圖" />
            <div class="caption">
              <span class="tag-session" style="background:var(--accent2);">教案附件 6 典藏</span>
              <div class="title">智高積木等臂天平工程規格藍圖</div>
              <div class="desc">
                詳實規範左右等臂 10 孔距、梯形配重重心、低阻尼轉軸與懸吊托盤卡榫結構，確保跨校與全年級推廣時具備高度組裝穩定性與測量再現性。
              </div>
            </div>
          </div>

          <div class="photo-album-card fragment">
            <img src="images/chronicle/c12_plan_balance_blueprint.png" alt="評量規準" />
            <div class="caption">
              <span class="tag-session" style="background:var(--success);">多元評量規準</span>
              <div class="title">學生任務操作單與三階素養規準表</div>
              <div class="desc">
                涵蓋「手感估測、機關組裝、加減微調平衡、生活問題解決」四大維度，搭配同儕互評與量規，兼顧歷程性與總結性學習成就感。
              </div>
            </div>
          </div>
        </div>
      </section>

      <!-- S22: 結語與未來展望 -->
      <section data-background-image="images/ending_bg.png"
               data-background-opacity="0.36"
               data-background-size="cover">
        <h2>亮眼推動成效與未來展望：讓 STEAM 在中正生根</h2>
        <p class="lead-text">
          扎實研究、入班實證、永續傳承，建立中正國小特色課程品牌：
        </p>

        <div class="grid-3">
          <div class="glass-card" style="border-top:6px solid #10b981;">
            <div style="font-size:44px; margin-bottom:10px;">📈</div>
            <h3 style="color:#34d399;">卓越學習成效</h3>
            <p style="font-size:22px; color:#cbd5e1;">
              • 重量概念前後測理解度大躍升 <strong style="color:#34d399;">+28.5%</strong>。<br>
              • 學生動手實作滿意度達 <strong style="color:#38bdf8;">96.8%</strong>。<br>
              • 徹底掃除「指針未歸零」與「讀錯格值」重大迷思！
            </p>
          </div>

          <div class="glass-card" style="border-top:6px solid #38bdf8;">
            <div style="font-size:44px; margin-bottom:10px;">📚</div>
            <h3 style="color:#38bdf8;">成果典藏與推廣</h3>
            <p style="font-size:22px; color:#cbd5e1;">
              • 正式教案設計（附件6）已依規完整送件典藏。<br>
              • 研發之天平教具模組推廣至校內三、四年級各班。<br>
              • 結合 micro:bit 體育感測，橫向拓展自然與科技領域。
            </p>
          </div>

          <div class="glass-card" style="border-top:6px solid #f59e0b;">
            <div style="font-size:44px; margin-bottom:10px;">🌟</div>
            <h3 style="color:#fbbf24;">感謝與未來展望</h3>
            <p style="font-size:22px; color:#cbd5e1;">
              • 感謝臺中市教育局與 STEAM 計畫團隊的全力輔導。<br>
              • 感謝南投鯉魚國小陳建安老師的無私經驗傳授。<br>
              • 中正國小團隊將持續深耕，點亮每位孩子的創客之光！
            </p>
          </div>
        </div>

        <div style="margin-top:36px;">
          <span style="font-size:32px; font-weight:800; color:#ffffff; background:rgba(15,23,42,0.85); padding:14px 44px; border-radius:9999px; border:1px solid rgba(56,189,248,0.4);">
            🎉 感謝聆聽 · 敬請指教 ｜ 梧棲中正國小 STEAM 教師社群
          </span>
        </div>
      </section>

    </div>
  </div>

  <div class="deck-footer">
    <span>臺中市梧棲區中正國小 ｜ 115年度STEAM教師社群成果展</span>
    <span>使用方向鍵 [←] [→] 或 [Space] 換頁 ｜ 按 [ESC] 總覽</span>
  </div>

  <!-- Reveal.js JS -->
  <script src="https://cdn.jsdelivr.net/npm/reveal.js@4.6.1/dist/reveal.js"></script>
  <script>
    Reveal.initialize({
      width: 1920,
      height: 1080,
      margin: 0.04,
      minScale: 0.2,
      maxScale: 2.0,
      controls: true,
      progress: true,
      center: true,
      hash: true,
      transition: 'slide',
      backgroundTransition: 'fade',
      transitionSpeed: 'default'
    });

    // S13 互動對比滑桿即時控制
    const slider = document.getElementById('viz-slider');
    const afterLayer = document.getElementById('viz-after');
    const divider = document.getElementById('viz-divider');

    if (slider && afterLayer && divider) {
      function updateSlider(val) {
        afterLayer.style.clipPath = `inset(0 0 0 ${val}%)`;
        divider.style.left = `${val}%`;
      }
      slider.addEventListener('input', (e) => {
        updateSlider(e.target.value);
      });
      // 初始設為 50% 完美展示對比兩端
      slider.value = 50;
      updateSlider(50);
    }
  </script>
</body>
</html>
"""

for path in OUTPUT_PATHS:
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(html_template)
    print(f"[OK] Written 22-slide Reveal deck to: {path}")

print("All 22-slide Reveal HTML decks generated successfully!")

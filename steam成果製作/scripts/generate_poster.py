#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
STEAM 社群活動議程海報自動生成器
根據活動場次、日期、時間、主題、議程與照片，自動產出高品質 A4 直式活動海報 (PNG)
支援 macOS 與 Windows 11 / 10
"""

import os
import sys
import base64
import argparse
import subprocess
import shutil

if hasattr(sys.stdout, 'reconfigure'):
    try:
        sys.stdout.reconfigure(encoding='utf-8')
        sys.stderr.reconfigure(encoding='utf-8')
    except Exception:
        pass

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR = os.path.dirname(SCRIPT_DIR) if os.path.basename(SCRIPT_DIR) == 'scripts' else SCRIPT_DIR

def img_to_base64(path):
    if path and os.path.exists(path):
        try:
            with open(path, 'rb') as f:
                data = f.read()
            ext = os.path.splitext(path)[1].lower().replace('.', '')
            if ext == 'jpg': ext = 'jpeg'
            return f"data:image/{ext};base64,{base64.b64encode(data).decode('utf-8')}"
        except Exception:
            pass
    return ""

def generate_poster_html(
    session_num=6,
    theme="STEAM跨域教學實踐與課堂試教",
    subtheme="數位載具融入與學生操作觀察",
    tagline="從教案研發到課堂實踐，打造以學生為中心的智慧學習課堂！",
    date_str="115年9月26日 (六)",
    time_str="13:00 - 15:00",
    location="臺中市梧棲區中正國民小學",
    lecturer="王怡婷 老師",
    target="本校STEAM教師社群成員與觀課教師",
    agenda=None,
    objectives=None,
    hero_image_path=None
):
    if not agenda:
        agenda = [
            ("13:00 - 13:15", "說課與觀課重點說明"),
            ("13:15 - 13:55", "課堂試教公開授課（王怡婷 老師）"),
            ("13:55 - 14:35", "學生載具操作觀察與歷程紀錄"),
            ("14:35 - 15:00", "議課交流與教案優化研討")
        ]

    if not objectives:
        objectives = [
            "深化教師科技融入素養導向教學之實踐知能。",
            "觀察學生運用數位載具進行學習任務之操作表現。",
            "蒐集真實課堂實證回饋，作為教案修訂依據。",
            "促進社群教師觀課與議課專業對話，共同成長。"
        ]

    # Convert hero image to base64
    b64_hero = ""
    if hero_image_path and os.path.exists(hero_image_path):
        b64_hero = img_to_base64(hero_image_path)
    else:
        # Fallback candidate search
        default_candidates = [
            os.path.join(PROJECT_DIR, 'references', 'assets', 'steam_hero_default.jpg'),
            os.path.join(os.path.expanduser('~/.gemini/config/skills/steam-community-docs/references/assets'), 'steam_hero_default.jpg')
        ]
        for c in default_candidates:
            if os.path.exists(c):
                b64_hero = img_to_base64(c)
                break

    agenda_rows_html = "".join([
        f"<tr><td class='time-col'>{t}</td><td class='desc-col'>{d}</td></tr>"
        for t, d in agenda
    ])

    obj_items_html = "".join([
        f"<li class='obj-item'><span class='check-icon'>✔</span><span>{obj}</span></li>"
        for obj in objectives
    ])

    hero_html = ""
    if b64_hero:
        hero_html = f"""
        <div class="hero-card">
          <img class="hero-img" src="{b64_hero}" alt="STEAM 主題意象視覺圖" />
          <div class="hero-badge">AI 跨領域教學意象設計</div>
        </div>
        """

    html = f"""<!DOCTYPE html>
<html lang="zh-TW">
<head>
<meta charset="utf-8">
<title>STEAM 社群活動海報</title>
<style>
  * {{ box-sizing: border-box; margin: 0; padding: 0; }}
  body {{
    width: 1080px;
    height: 1528px;
    font-family: 'PingFang TC', 'Microsoft JhengHei', 'Noto Sans TC', sans-serif;
    background: #f4f6fa;
    color: #1e293b;
    position: relative;
    overflow: hidden;
    padding: 36px 40px;
  }}

  /* Background decorative shapes */
  .bg-circle-1 {{
    position: absolute; width: 450px; height: 450px;
    background: radial-gradient(circle, rgba(59, 130, 246, 0.12) 0%, rgba(244, 246, 250, 0) 70%);
    top: -100px; right: -80px; border-radius: 50%; z-index: 0;
  }}
  .bg-circle-2 {{
    position: absolute; width: 400px; height: 400px;
    background: radial-gradient(circle, rgba(245, 158, 11, 0.1) 0%, rgba(244, 246, 250, 0) 70%);
    bottom: 50px; left: -100px; border-radius: 50%; z-index: 0;
  }}

  .content-wrapper {{ position: relative; z-index: 1; height: 100%; display: flex; flex-direction: column; justify-content: space-between; }}

  /* Top Banner */
  .top-badge-row {{ text-align: center; margin-bottom: 8px; }}
  .top-badge {{
    display: inline-block;
    background: #1e3a8a;
    color: #ffffff;
    font-size: 20px;
    font-weight: 700;
    padding: 8px 32px;
    border-radius: 30px;
    letter-spacing: 2px;
    box-shadow: 0 4px 10px rgba(30, 58, 138, 0.25);
  }}

  .main-title {{
    text-align: center;
    font-size: 44px;
    font-weight: 900;
    color: #0f172a;
    line-height: 1.25;
    margin-top: 10px;
    letter-spacing: 1px;
  }}
  .main-title span.hl {{ color: #2563eb; }}

  .sub-title {{
    text-align: center;
    font-size: 28px;
    font-weight: 700;
    color: #475569;
    margin-top: 6px;
    letter-spacing: 1px;
  }}

  .tagline-banner {{
    background: linear-gradient(90deg, #f59e0b, #fbbf24);
    color: #78350f;
    text-align: center;
    font-size: 21px;
    font-weight: 800;
    padding: 10px 20px;
    border-radius: 12px;
    margin: 16px auto 20px auto;
    width: 92%;
    box-shadow: 0 3px 8px rgba(245, 158, 11, 0.2);
  }}

  /* Hero Illustration Section */
  .hero-card {{
    position: relative;
    width: 1000px;
    height: 400px;
    margin: 14px auto 18px auto;
    background: #ffffff;
    border-radius: 20px;
    padding: 8px;
    box-shadow: 0 10px 25px rgba(30, 58, 138, 0.15);
    border: 1px solid #cbd5e1;
    overflow: hidden;
  }}
  .hero-img {{
    width: 100%;
    height: 100%;
    object-fit: cover;
    border-radius: 14px;
    display: block;
  }}
  .hero-badge {{
    position: absolute;
    bottom: 18px;
    right: 20px;
    background: rgba(15, 23, 42, 0.75);
    backdrop-filter: blur(8px);
    color: #ffffff;
    font-size: 14px;
    font-weight: 700;
    padding: 6px 16px;
    border-radius: 20px;
    letter-spacing: 1px;
    border: 1px solid rgba(255, 255, 255, 0.3);
  }}

  /* Middle Grid */
  .grid-two-col {{
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 22px;
    margin-bottom: 20px;
  }}

  .card {{
    background: #ffffff;
    border-radius: 18px;
    padding: 22px 24px;
    box-shadow: 0 6px 16px rgba(0, 0, 0, 0.05);
    border: 1px solid #e2e8f0;
  }}

  .card-header {{
    display: flex;
    align-items: center;
    gap: 10px;
    font-size: 22px;
    font-weight: 800;
    margin-bottom: 16px;
    padding-bottom: 8px;
    border-bottom: 2px solid #f1f5f9;
  }}
  .card-header.blue {{ color: #1d4ed8; border-color: #bfdbfe; }}
  .card-header.amber {{ color: #b45309; border-color: #fde68a; }}
  .card-header.emerald {{ color: #047857; border-color: #a7f3d0; }}

  /* Info list */
  .info-list {{ list-style: none; }}
  .info-item {{
    display: flex;
    margin-bottom: 12px;
    font-size: 18px;
    line-height: 1.4;
  }}
  .info-label {{
    font-weight: 700;
    color: #64748b;
    min-width: 90px;
  }}
  .info-val {{
    font-weight: 800;
    color: #0f172a;
  }}

  /* Objectives list */
  .obj-list {{ list-style: none; }}
  .obj-item {{
    display: flex;
    align-items: flex-start;
    gap: 10px;
    font-size: 17px;
    line-height: 1.45;
    margin-bottom: 12px;
    color: #334155;
    font-weight: 600;
  }}
  .check-icon {{
    background: #10b981;
    color: white;
    width: 22px;
    height: 22px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 13px;
    flex-shrink: 0;
    margin-top: 2px;
  }}

  /* Agenda Table */
  .agenda-table {{
    width: 100%;
    border-collapse: collapse;
    font-size: 17px;
  }}
  .agenda-table td {{
    padding: 10px 12px;
    border-bottom: 1px dashed #cbd5e1;
  }}
  .time-col {{
    font-weight: 800;
    color: #2563eb;
    white-space: nowrap;
    width: 140px;
  }}
  .desc-col {{
    font-weight: 700;
    color: #1e293b;
  }}

  /* Slogan & Footer */
  .slogan-row {{
    text-align: center;
    font-size: 26px;
    font-weight: 900;
    color: #1e3a8a;
    letter-spacing: 3px;
    margin: 10px 0;
  }}

  .footer-row {{
    background: #0f172a;
    color: #e2e8f0;
    text-align: center;
    font-size: 17px;
    font-weight: 600;
    padding: 12px 20px;
    border-radius: 12px;
    letter-spacing: 1px;
  }}
</style>
</head>
<body>
  <div class="bg-circle-1"></div>
  <div class="bg-circle-2"></div>
  
  <div class="content-wrapper">
    <!-- Top Area -->
    <div>
      <div class="top-badge-row">
        <div class="top-badge">✨ STEAM 校內教師社群活動 第 {session_num} 場 ✨</div>
      </div>
      <h1 class="main-title"><span class="hl">{theme[:15]}</span>{theme[15:] if len(theme)>15 else ""}</h1>
      <div class="sub-title">⚙️ {subtheme} ⚙️</div>
      <div class="tagline-banner">💡 {tagline}</div>
      {hero_html}
    </div>

    <!-- Middle Grid -->
    <div class="grid-two-col">
      <!-- Card 1: 活動資訊 -->
      <div class="card">
        <div class="card-header blue">📅 活動基本資訊</div>
        <ul class="info-list">
          <li class="info-item"><span class="info-label">活動日期：</span><span class="info-val">{date_str}</span></li>
          <li class="info-item"><span class="info-label">活動時間：</span><span class="info-val">{time_str}</span></li>
          <li class="info-item"><span class="info-label">活動地點：</span><span class="info-val">{location}</span></li>
          <li class="info-item"><span class="info-label">主講講師：</span><span class="info-val">{lecturer}</span></li>
          <li class="info-item"><span class="info-label">參與對象：</span><span class="info-val">{target}</span></li>
        </ul>
      </div>

      <!-- Card 2: 活動目標 -->
      <div class="card">
        <div class="card-header emerald">🎯 活動核心目標</div>
        <ul class="obj-list">
          {obj_items_html}
        </ul>
      </div>
    </div>

    <!-- Bottom Agenda Table -->
    <div class="card" style="margin-bottom: 14px;">
      <div class="card-header amber">⏰ 活動詳細議程</div>
      <table class="agenda-table">
        <tbody>
          {agenda_rows_html}
        </tbody>
      </table>
    </div>

    <!-- Slogan & Footer -->
    <div>
      <div class="slogan-row">🌟 一起玩・一起學・一起創造無限可能！ 🌟</div>
      <div class="footer-row">主辦單位：臺中市梧棲區中正國民小學 ｜ 協辦單位：STEAM教師社群</div>
    </div>
  </div>
</body>
</html>"""
    return html

def render_html_to_png(html_content, output_png):
    tmp_html = output_png + ".tmp.html"
    with open(tmp_html, 'w', encoding='utf-8') as f:
        f.write(html_content)

    # Find Chrome or Edge
    browser_bin = None
    if sys.platform == 'darwin':
        c_path = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
        if os.path.exists(c_path):
            browser_bin = c_path
    elif sys.platform == 'win32':
        candidates = [
            r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
            r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
            r"C:\Program Files\Google\Chrome\Application\chrome.exe",
            r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
        ]
        for c in candidates:
            if os.path.exists(c):
                browser_bin = c
                break
    
    if not browser_bin:
        for b in ['google-chrome', 'chromium', 'msedge']:
            if shutil.which(b):
                browser_bin = shutil.which(b)
                break

    if browser_bin:
        cmd = [
            browser_bin,
            '--headless',
            '--disable-gpu',
            f'--screenshot={output_png}',
            '--window-size=1080,1528',
            tmp_html
        ]
        try:
            subprocess.run(cmd, capture_output=True, timeout=15)
            if os.path.exists(tmp_html):
                os.remove(tmp_html)
            if os.path.exists(output_png) and os.path.getsize(output_png) > 1000:
                return True
        except Exception as e:
            print(f"Warning: Browser screenshot failed: {e}", file=sys.stderr)

    if os.path.exists(tmp_html):
        try: os.remove(tmp_html)
        except: pass
    return False

# Presets for 8 Sessions
SESSION_PRESETS = {
    1: {
        "theme": "社群運作規劃與STEAM課程跨域整合初探",
        "subtheme": "年度發展目標定錨與教學資源盤點",
        "lecturer": "謝敦元",
        "agenda": [
            ("13:00 - 13:20", "社群年度計畫說明與共識凝聚"),
            ("13:20 - 14:10", "STEAM 跨域理念與國內外教案案例分析"),
            ("14:10 - 14:40", "校內智高積木與教學硬體設備盤點"),
            ("14:40 - 15:00", "學期工作分配與後續場次期程規劃")
        ],
        "objectives": [
            "凝聚社群成員對 STEAM 跨領域教育之核心理念共識。",
            "完成校內積木模組與跨域教學器材資源盤點。",
            "確立全年度 8 場次備課與公開觀課研討時程。"
        ]
    },
    2: {
        "theme": "智高積木機械原理拆解與結構分析",
        "subtheme": "槓桿、齒輪比與天平機構組裝實作",
        "lecturer": "王怡婷",
        "agenda": [
            ("13:00 - 13:20", "力學原理與積木機構組裝邏輯解析"),
            ("13:20 - 14:20", "齒輪傳動與槓桿天平機構動手實作"),
            ("14:20 - 14:45", "支點、力臂與平衡靈敏度實測調校"),
            ("14:45 - 15:00", "機構組裝常見難點與學生學習鷹架探討")
        ],
        "objectives": [
            "掌握智高積木多向度接頭與力學機構之工程特性。",
            "動手完成雙盤等臂天平原型機關組裝與校正。",
            "探討數學重量概念融入實體機關之實施瓶頸與解方。"
        ]
    },
    3: {
        "theme": "三年級數學「公斤與公克」素養導向教案設計",
        "subtheme": "數學重量感量概念與 STEAM 機構整合",
        "lecturer": "李仁耀",
        "agenda": [
            ("13:00 - 13:30", "課綱「公斤與公克」學習重點與迷思概念分析"),
            ("13:30 - 14:20", "秤重機關融入數學課堂教學流程設計"),
            ("14:20 - 14:45", "學習單設計與學生感量操作任務研發"),
            ("14:45 - 15:00", "跨領域教學目標檢核與評量指標研擬")
        ],
        "objectives": [
            "連結國小三年級數學課綱與 STEAM 工程實作歷程。",
            "研發兼具感量體驗與精準測量之整合式學習單。",
            "擬定多元學習評量向度，兼顧數學概念與動手能力。"
        ]
    },
    4: {
        "theme": "世界機關王（GM）整合賽題目研討與機構串接",
        "subtheme": "骨牌、滾珠與多層關卡機關設計",
        "lecturer": "曾泊淞",
        "agenda": [
            ("13:00 - 13:30", "世界機關王競賽規則與評分規準解析"),
            ("13:30 - 14:20", "骨牌效應、斜坡滾球與彈跳機關實作"),
            ("14:20 - 14:45", "多重關卡動能傳遞連動測試與穩定度調校"),
            ("14:45 - 15:00", "機關王創思解題教學引導策略交流")
        ],
        "objectives": [
            "理解競賽型連鎖機關之能量轉換與傳遞原理。",
            "實作三種以上連鎖機關模組並驗證觸發穩定度。",
            "規劃學生參與校內外科學創思競賽之培訓架構。"
        ]
    },
    5: {
        "theme": "動態機關穩定度調校與科學探究實作",
        "subtheme": "重力位能與動能轉換機制優化",
        "lecturer": "謝敦元",
        "agenda": [
            ("13:00 - 13:20", "機關失敗成因分析與科學探究變因控制"),
            ("13:20 - 14:20", "軌道摩擦力、角度與釋放高度對比實驗"),
            ("14:20 - 14:45", "機關結構補強與防卡彈優化實作"),
            ("14:45 - 15:00", "課堂故障排除（Troubleshooting）教學法研討")
        ],
        "objectives": [
            "深化科學探究之公平測試與變因控制實踐知能。",
            "掌握機關運動摩擦阻抗最小化之結構校準要領。",
            "培養引導學生面對操作失敗時的除錯與心理韌性。"
        ]
    },
    6: {
        "theme": "STEAM 跨域教學實踐與課堂試教觀課",
        "subtheme": "數位載具融入與學生操作歷程觀察",
        "lecturer": "王怡婷",
        "agenda": [
            ("13:00 - 13:15", "說課與觀課重點指標說明"),
            ("13:15 - 13:55", "公開課課堂實踐與學生分組操作"),
            ("13:55 - 14:35", "數位載具歷程紀錄與課堂反思回饋"),
            ("14:35 - 15:00", "議課交流與教學流程調整研議")
        ],
        "objectives": [
            "實踐科技融入素養導向教學之課堂公開課。",
            "觀察學生運用數位載具進行學習任務之操作表現。",
            "蒐集真實課堂實證回饋，作為教案修訂依據。"
        ]
    },
    7: {
        "theme": "課堂試教議課回饋與教案精進修正",
        "subtheme": "學習成效評量與教學鷹架優化",
        "lecturer": "李仁耀",
        "agenda": [
            ("13:00 - 13:30", "試教課堂學生學習成效與作品分析"),
            ("13:30 - 14:20", "教案操作步驟修正與教學時間節奏調校"),
            ("14:20 - 14:45", "差異化教學策略與低成就學生鷹架規劃"),
            ("14:45 - 15:00", "正式版教學手冊與引導指引編寫分工")
        ],
        "objectives": [
            "根據實作回饋精修公斤公克測量機關教案與評量單。",
            "建立針對操作學習困難學生之補救鷹架指引。",
            "產出具體可移轉、易推廣之校本跨域教案規格書。"
        ]
    },
    8: {
        "theme": "社群成果彙整、推廣發表與跨校分享",
        "subtheme": "成果冊編纂與推動成效總結",
        "lecturer": "曾泊淞",
        "agenda": [
            ("13:00 - 13:30", "年度研發教案與機關模組完整回顧"),
            ("13:30 - 14:20", "社群活動成果彙整與檔案製作分工"),
            ("14:20 - 14:45", "校內教師晨會與跨校教學推廣形式討論"),
            ("14:45 - 15:00", "下一年度 STEAM 社群深化目標前瞻交流")
        ],
        "objectives": [
            "綜整全年度社群研發之教學資源與學生作品集錦。",
            "完成 115 年度校園 STEAM 教育推動結案與成果手冊。",
            "深化校內外教師專業學習社群網絡與持續發展動能。"
        ]
    }
}

def generate_session_poster(session_num, date_str, time_str, activity_name, lecturer, photo_paths=None, output_png=None, hero_image_path=None):
    """
    High-level API to generate session poster PNG.
    Uses AI generated hero illustration image, completely omitting activity photos.
    """
    preset = SESSION_PRESETS.get(session_num, SESSION_PRESETS[1])
    theme = activity_name if activity_name else preset["theme"]
    subtheme = preset["subtheme"]
    lec_str = f"{lecturer} 老師" if lecturer and not lecturer.endswith("老師") else (f"{preset['lecturer']} 老師" if not lecturer else lecturer)
    agenda = preset["agenda"]
    objectives = preset["objectives"]

    # If hero_image_path not explicitly provided, look for default
    if not hero_image_path:
        default_candidates = [
            os.path.join(os.path.dirname(output_png) if output_png else '.', '0926海報視覺圖.jpg'),
            os.path.join(PROJECT_DIR, 'references', 'assets', 'steam_hero_default.jpg'),
            os.path.join(os.path.expanduser('~/.gemini/config/skills/steam-community-docs/references/assets'), 'steam_hero_default.jpg'),
        ]
        for c in default_candidates:
            if os.path.exists(c):
                hero_image_path = c
                break

    html = generate_poster_html(
        session_num=session_num or 1,
        theme=theme,
        subtheme=subtheme,
        date_str=date_str,
        time_str=time_str,
        location="臺中市梧棲區中正國民小學",
        lecturer=lec_str,
        agenda=agenda,
        objectives=objectives,
        hero_image_path=hero_image_path
    )

    return render_html_to_png(html, output_png)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="STEAM 社群活動海報生成工具 (AI 主題視覺版)")
    parser.add_argument('--session-num', type=int, default=6)
    parser.add_argument('--theme', default=None)
    parser.add_argument('--subtheme', default=None)
    parser.add_argument('--date', default="115年9月26日 (六)")
    parser.add_argument('--time', default="13:00 - 15:00")
    parser.add_argument('--location', default="臺中市梧棲區中正國民小學")
    parser.add_argument('--lecturer', default=None)
    parser.add_argument('--hero-image', default=None, help="Gemini 生成的 AI 主題視覺圖路徑")
    parser.add_argument('--output', required=True, help="輸出 PNG 路徑")

    args = parser.parse_args()

    s_num = args.session_num or 6
    preset = SESSION_PRESETS.get(s_num, SESSION_PRESETS[1])
    theme = args.theme or preset["theme"]
    subtheme = args.subtheme or preset["subtheme"]
    lecturer = args.lecturer or preset["lecturer"]

    html = generate_poster_html(
        session_num=s_num,
        theme=theme,
        subtheme=subtheme,
        date_str=args.date,
        time_str=args.time,
        location=args.location,
        lecturer=lecturer if lecturer.endswith("老師") else f"{lecturer} 老師",
        agenda=preset["agenda"],
        objectives=preset["objectives"],
        hero_image_path=args.hero_image
    )

    success = render_html_to_png(html, args.output)
    if success:
        print(f"✅ 議程海報生成成功：{args.output}")
    else:
        print(f"❌ 議程海報生成失敗")



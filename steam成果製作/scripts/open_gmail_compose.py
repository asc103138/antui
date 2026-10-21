#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
一鍵開啟瀏覽器 Gmail 官方撰寫視窗與附件資料夾
解決教育局 @st.tc.edu.tw 網域透過 SMTP 寄送時遭 Google 阻擋 (Message blocked) 的問題。
"""

import os
import sys
import subprocess
import urllib.parse
import webbrowser

PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

recipient = 'tc.steam114@gmail.com'
subject = '【核銷寄件通知】臺中市梧棲區中正國小「115年度STEAM校內教師社群」全案講師領據紙本正本寄出通知'

body = """「115年度推動校園STEAM教育實施計畫」承辦團隊 您好：

感謝貴團隊對校園 STEAM 教育推動的悉心指導與全力支持！

本校辦理臺中市「115年度推動校園STEAM教育實施計畫」——STEAM校內教師專業學習社群，全年度共 7 大活動場次已全數圓滿執行完畢，先前各場次之「活動執行成果表」與「簽到表」電子檔均已依規寄交備查。

為辦理全案經費結報核銷，本校已於今日（115年10月21日）將全案之「講師鐘點費領款收據正本（國立臺中科技大學支出憑證單）」共 8 份親筆簽名正本，備妥並以郵局掛號郵寄至承辦單位，特以此信先行通知備查。

檢附全案核銷講師領據與經費明細如下：

【全案經費執行總結】
• 核定補助經費：新台幣 16,000 元整（講師鐘點費 16 節 × 1,000 元）
• 累計執行節数：16 節（預算執行率 100%，結餘款 0 元整）
• 領款收據正本：共計 8 份（如下列清單）

【掛號郵寄之領款收據清單（共 8 份）】
1. 115.05.20（13:00-15:00）：謝敦元 老師（內聘 2 節，金額 2,000 元）
2. 115.08.10（10:00-12:00）：陳建安 老師（外聘／南投縣鯉魚國小 2 節，金額 2,000 元）
3. 115.09.26（13:00-15:00）：王怡婷 老師（內聘 2 節，金額 2,000 元）
4. 115.10.01（13:00-15:00）：王怡婷 老師（內聘 2 節，金額 2,000 元）
5. 115.10.05（13:00-15:00）：曾泊淞 老師（內聘 2 節，金額 2,000 元）
6. 115.10.05（15:00-17:00）：謝敦元 老師（內聘 2 節，金額 2,000 元）
7. 115.10.19（12:40-14:40）：李仁耀 老師（內聘 2 節，金額 2,000 元）
8. 115.10.19（14:40-16:40）：謝敦元 老師（內聘 2 節，金額 2,000 元）
（註：115.06.03 為社群全體共備研討，不支領鐘點費 0 元，免附領據）

隨信夾帶電子檔供承辦團隊先行核對：
一、臺中市梧棲區中正國小_115年度STEAM教師社群_總核銷清冊.pdf（單頁橫向）
二、臺中市梧棲區中正國小_115年度STEAM教師社群_活動成果總表.pdf（直向三頁）

紙本掛號郵件寄出後，若有需要進一步補件或核對之處，懇請不吝隨時指教，謝謝您！

敬祝
研安

臺中市梧棲區中正國民小學 STEAM教師專業學習社群
社群召集人：謝敦元 老師
聯絡電話：0981-455-340 / 04-26560844
學校地址：435057 臺中市梧棲區中央路二段15號"""

def main():
    print("=" * 65)
    print("  🌐 正在啟動瀏覽器官方 Gmail 撰寫模式 (安全認證防阻擋)")
    print("=" * 65)

    # 1. 複製內文到剪貼簿 (PowerShell)
    try:
        # Write body to temp utf-8 file to avoid command line escape issues
        tmp_txt = os.path.join(PROJECT_DIR, 'scripts', 'temp_email_body.txt')
        with open(tmp_txt, 'w', encoding='utf-8') as f:
            f.write(body)
        subprocess.run(['powershell', '-Command', f"Get-Content -Path '{tmp_txt}' -Raw -Encoding UTF8 | Set-Clipboard"], check=True)
        if os.path.exists(tmp_txt):
            os.remove(tmp_txt)
        print("✅ 完整信件內文已自動複製到您的 Windows 剪貼簿 (隨時可 Ctrl+V 貼上)")
    except Exception as e:
        print(f"⚠️ 剪貼簿複製提示：{e}")

    # 2. 開啟檔案總管資料夾 (方便拖曳附件)
    try:
        if sys.platform == 'win32':
            os.startfile(PROJECT_DIR)
            print(f"✅ 已為您開啟附件資料夾：{PROJECT_DIR}")
    except Exception as e:
        print(f"⚠️ 開啟資料夾提示：{e}")

    # 3. 開啟瀏覽器 Gmail Compose 網頁 (鎖定官方帳號)
    user_email = 'asc103138@st.tc.edu.tw'
    encoded_to = urllib.parse.quote(recipient)
    encoded_su = urllib.parse.quote(subject)
    encoded_body = urllib.parse.quote(body)
    
    compose_url = f"https://mail.google.com/mail/u/{urllib.parse.quote(user_email)}/?view=cm&fs=1&to={encoded_to}&su={encoded_su}&body={encoded_body}"
    print(f"🌐 正在以瀏覽器開啟 Gmail 撰寫視窗 (鎖定帳號：{user_email})...")
    webbrowser.open(compose_url)

    print("\n" + "=" * 65)
    print("📌 寄件 3 步驟快速指引：")
    print("1. 瀏覽器視窗開啟後，請確認右上角為您的教育局帳號（asc103138@st.tc.edu.tw）。")
    print("2. 檢查內文（若部分瀏覽器截斷長網址，直接在內文按 Ctrl+V 即可貼上完整排版內文）。")
    print("3. 將剛才開啟的資料夾中的 2 份 PDF（總核銷清冊.pdf 與 活動成果總表.pdf）拖曳至 Gmail 視窗。")
    print("4. 點擊「傳送」，走 Google 官方網頁連線，保證 100% 成功送達，絕不被封鎖！")
    print("=" * 65)

if __name__ == '__main__':
    main()

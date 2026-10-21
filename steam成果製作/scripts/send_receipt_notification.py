#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
發送全案領據郵寄寄出通知信件
收件人：tc.steam114@gmail.com
寄件人：asc103138@st.tc.edu.tw (信封來源自動映射 asc103138@tc.edu.tw 通過 SPF 驗證)
附件：
1. 臺中市梧棲區中正國小_115年度STEAM教師社群_總核銷清冊.pdf
2. 臺中市梧棲區中正國小_115年度STEAM教師社群_活動成果總表.pdf
"""

import os
import sys
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from email.utils import formatdate, make_msgid
from email.header import Header

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR = os.path.dirname(SCRIPT_DIR)
sys.path.append(SCRIPT_DIR)

from send_gmail import get_gmail_config, REQUIRED_SENDER, DEFAULT_RECIPIENT, send_via_smtp

def send_notification():
    cfg = get_gmail_config()
    sender = REQUIRED_SENDER
    app_pwd = cfg.get('app_password')

    if not app_pwd:
        print("ERROR: 未取得 GMAIL_APP_PASSWORD！", file=sys.stderr)
        sys.exit(1)

    recipient = DEFAULT_RECIPIENT
    subject = "【核銷寄件通知】臺中市梧棲區中正國小「115年度STEAM校內教師社群」全案講師領據紙本正本寄出通知"

    body = """「115年度推動校園STEAM教育實施計畫」承辦團隊 您好：

感謝貴團隊對校園 STEAM 教育推動的悉心指導與全力支持！

本校辦理臺中市「115年度推動校園STEAM教育實施計畫」——STEAM校內教師專業學習社群，全年度共 7 大活動場次已全數圓滿執行完畢，先前各場次之「活動執行成果表」與「簽到表」電子檔均已依規寄交備查。

為辦理全案經費結報核銷，本校已於今日（115年10月21日）將全案之「講師鐘點費領款收據正本（國立臺中科技大學支出憑證單）」共 8 份親筆簽名正本，備妥並以郵局掛號郵寄至承辦單位，特以此信先行通知備查。

檢附全案核銷講師領據與經費明細如下：

【全案經費執行總結】
• 核定補助經費：新台幣 16,000 元整（講師鐘點費 16 節 × 1,000 元）
• 累計執行節數：16 節（預算執行率 100%，結餘款 0 元整）
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

    attachments = [
        os.path.join(PROJECT_DIR, "臺中市梧棲區中正國小_115年度STEAM教師社群_總核銷清冊.pdf"),
        os.path.join(PROJECT_DIR, "臺中市梧棲區中正國小_115年度STEAM教師社群_活動成果總表.pdf")
    ]

    print("=" * 65)
    print("  📨 準備發送全案領據寄出通知信件")
    print("=" * 65)
    print(f"寄件人：{sender} (信封來源自動映射至 tc.edu.tw 通過 SPF)")
    print(f"收件人：{recipient}")
    print(f"主旨  ：{subject}")
    print("附件清單：")
    for att in attachments:
        exists = os.path.exists(att)
        sz = os.path.getsize(att) if exists else 0
        print(f"  - {os.path.basename(att)} ({sz} bytes, 存在: {exists})")

    # 執行合規發送
    success = send_via_smtp(
        sender=sender,
        app_password=app_pwd,
        recipient=recipient,
        subject=subject,
        body=body,
        attachment_paths=attachments
    )
    if success:
        print("🎉 郵件已成功寄出！")

if __name__ == '__main__':
    send_notification()

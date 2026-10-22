#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
發送 STEAM 社群教案設計繳交與成果展參展回信
收件人：tc.steam114@gmail.com (張莉崢 助理)
寄件人：asc103138@st.tc.edu.tw (信封來源自動映射 asc103138@tc.edu.tw 通過 SPF 驗證)
附件：
1. 臺中市梧棲區中正國小_115年度STEAM教師社群_教案設計(附件6).docx
2. 臺中市梧棲區中正國小_115年度STEAM教師社群_教案設計(附件6).pdf
"""

import os
import sys
import shutil
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

def send_reply():
    cfg = get_gmail_config()
    sender = REQUIRED_SENDER
    app_pwd = cfg.get('app_password')

    if not app_pwd:
        print("ERROR: 未取得 GMAIL_APP_PASSWORD！", file=sys.stderr)
        sys.exit(1)

    recipient = DEFAULT_RECIPIENT
    subject = "Re:【STEAM教師社群】臺中市梧棲區中正國小——教案設計繳交與12月成果展參展回覆"

    body = """推動校園 STEAM 教育實施計畫團隊、張莉崢 助理 您好：

感謝張助理的溫暖來信與即時回覆！

有關全案講師鐘點費領款收據正本（支出憑證單共 8 份），本校已於昨日以郵局掛號寄出，掛號郵件送達後，再煩請貴團隊惠予查收與核對。

另外，針對來信提醒之「教案設計繳交（附件6）」與「12月成果展」，本校社群回覆如下：

一、 教案設計提早繳交（檢附附件6）：
本校 STEAM 教師社群本年度深耕之跨領域主題為智高積木融入三年級數學——「公斤與公克」重量測量機關課程設計（數學領域 ✕ 科技領域，共 3 節），相關教案設計與課堂實踐已完整編撰完成。
為利貴團隊提早彙整，特隨信提前檢附符合規定之「教案設計（附件6）」電子檔（包含 Word 可編輯檔與 PDF 檔各 1 份），敬請查收備查。若有任何需增補或微調之處，懇請隨時不吝指導！

二、 配合參與 12 月成果展：
本校 STEAM 社群團隊非常期待並將全力配合參與預計於 12 月辦理之校園 STEAM 教育成果展，屆時將展示本校研發之社群教案設計作品與學生積木機關成果。後續我們將密切留意貴團隊於 10 月底至 11 月初發布之成果展期程與相關公告公文。

再次感謝張助理與承辦團隊全年度對本校社群推動歷程的悉心協助與大力支持！

敬祝
教安

臺中市梧棲區中正國民小學 STEAM教師專業學習社群
社群召集人：謝敦元 老師
聯絡電話：0981-455-340 / 04-26560844
學校地址：435057 臺中市梧棲區中央路二段15號"""

    # 準備規範命名之附件
    raw_docx = os.path.join(PROJECT_DIR, "三年級steam教案.docx")
    raw_pdf  = os.path.join(PROJECT_DIR, "三年級steam教案.pdf")

    att_docx = os.path.join(PROJECT_DIR, "臺中市梧棲區中正國小_115年度STEAM教師社群_教案設計(附件6).docx")
    att_pdf  = os.path.join(PROJECT_DIR, "臺中市梧棲區中正國小_115年度STEAM教師社群_教案設計(附件6).pdf")

    if os.path.exists(raw_docx) and not os.path.exists(att_docx):
        shutil.copy2(raw_docx, att_docx)
    if os.path.exists(raw_pdf) and not os.path.exists(att_pdf):
        shutil.copy2(raw_pdf, att_pdf)

    attachments = [att_docx, att_pdf]

    print("=" * 65)
    print("  📨 準備發送教案繳交與成果展參展回信")
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
    send_reply()

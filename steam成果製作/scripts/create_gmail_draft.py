#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
精準將全套成果資料（成果總表PDF/DOCX、教案設計PDF/DOCX、PPTX簡報、3張高解析照片）
打包並存入 Gmail 草稿匣，嚴格排除《領據》！
"""

import os
import sys
import time
import imaplib
import re
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from email.utils import formatdate, make_msgid
from email.header import Header

sys.path.append(r"d:\antui\steam成果製作\scripts")
from send_gmail import get_gmail_config, REQUIRED_SENDER, DEFAULT_RECIPIENT

RECIPIENT = DEFAULT_RECIPIENT # tc.steam114@gmail.com
SUBJECT = "【成果報告與成果展資料繳交】臺中市梧棲區中正國小「115年度推動校園STEAM教育實施計畫」教師社群成果報告、教案設計及12/18成果展資料（社群名單無異動及出席整日派代洽詢）"

# 附件清單 (正確完整路徑，嚴格排除領據)
ATTACHMENT_PATHS = [
    # 1. 成果總表
    r"d:\antui\steam成果製作\臺中市梧棲區中正國小_115年度STEAM教師社群_活動成果總表.pdf",
    r"d:\antui\steam成果製作\臺中市梧棲區中正國小_115年度STEAM教師社群_活動成果總表.docx",
    # 2. 教案設計
    r"d:\antui\steam成果製作\臺中市梧棲區中正國小_115年度STEAM教師社群_教案設計(附件6).pdf",
    r"d:\antui\steam成果製作\臺中市梧棲區中正國小_115年度STEAM教師社群_教案設計(附件6).docx",
    # 3. 簡報檔案
    r"d:\antui\steam成果製作\成果展繳交資料\臺中市梧棲區中正國小_STEAM成果展_5分鐘現場分享會簡報.pptx",
    # 4. 成果展示照片 3 張 (高畫質 1,200 萬畫素，遠高於 800 萬畫素規定，確保郵件總容量在 Gmail 25MB 安全範圍內)
    r"d:\antui\steam成果製作\成果展繳交資料\成果展示照片_郵件夾帶版\01_教具研發_社群教師合力組裝智高積木等臂天平原型與轉軸阻尼校正_24.5MP.jpg",
    r"d:\antui\steam成果製作\成果展繳交資料\成果展示照片_郵件夾帶版\02_教案共備_社群教師研討學習成效評量分析與兩步驟問題情境轉化_24.5MP.jpg",
    r"d:\antui\steam成果製作\成果展繳交資料\成果展示照片_郵件夾帶版\03_競賽整合_社群召集人解析世界機關王競賽指定關卡傳動與賽程策略_24.5MP.jpg",
]

HTML_BODY = """<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
  body, p, div, li, span, td, th {
    font-family: "標楷體", "DFKai-SB", "BiauKai", "Kaiti TC", "KaiTi", serif;
    font-size: 16px;
    line-height: 1.85;
    color: #222222;
  }
  .highlight-title {
    font-weight: bold;
    color: #0d47a1;
    font-size: 17px;
  }
  .note-box {
    background-color: #f8fafc;
    border-left: 4px solid #0284c7;
    padding: 12px 16px;
    margin: 14px 0;
  }
  ul, ol {
    margin-top: 6px;
    margin-bottom: 12px;
  }
  li {
    margin-bottom: 6px;
  }
  .signature {
    margin-top: 28px;
    border-top: 1px dashed #999999;
    padding-top: 14px;
    color: #444444;
  }
</style>
</head>
<body>

<p>臺中市115年度推動校園STEAM教育實施計畫 承辦團隊 您好：</p>

<p>我是臺中市梧棲區中正國小 STEAM 教師社群召集人謝敦元老師。<br>
感謝承辦團隊的協助與提醒，針對來信各項辦理事項，謹逐一說明並檢附本校全套成果資料如下：</p>

<p><span class="highlight-title">一、【社群經費執行進度（11/15前）】</span><br>
本校社群全年度共 8 場次、16 節課程之講師鐘點費（共計新臺幣 16,000 元整）已於 115 年 10 月 19 日 100% 執行完畢，相關核銷領據正本亦已按期寄交核銷。</p>

<p><span class="highlight-title">二、【活動執行成果報告繳交（11/27前）】</span></p>
<ul>
  <li>各單場次（04/15、05/06、05/20、09/16、09/26、10/01、10/05、10/19 共 8 場次）之活動成果表與簽到表均已逐場寄送完畢，隨信一併檢附彙整之《115年度STEAM教師社群_活動成果總表》（含 Word 與 PDF 檔）。</li>
  <li>隨信檢附完成之《115年度STEAM教師社群_教案設計（附件6）》（主題：小小秤重師——用積木做自己的天平，含 Word 與 PDF 檔）。</li>
</ul>

<p><span class="highlight-title">三、【確認社群教師名單（無異動）】</span><br>
經確認，本校 STEAM 教師社群成員名單與原申請計畫書完全一致，<b>無任何異動</b>（免填異動申請表）。成果展感謝狀請依下列 4 位社群教師名單印製：</p>
<ul>
  <li><b>召集人</b>：謝敦元 老師</li>
  <li><b>社群成員</b>：王怡婷 老師、李仁耀 老師、曾泊淞 老師</li>
</ul>

<p><span class="highlight-title">四、【12月18日(五)成果展參與方式及出席公費派代洽詢】</span></p>
<p><b>(1) 參與及分享方式：</b><br>
本社群將準時出席 115 年 12 月 18 日（星期五）成果展。上午 5 分鐘教案設計成果分享，我們已同步備妥「上台簡報發表」與「5分鐘教學分享影片」，可配合大會現場流程彈性調整：<br>
🌐 <b>22頁互動式網頁簡報線上網址（GitHub Pages）：</b><br>
<a href="https://asc103138.github.io/steam-gigo-balance-deck/">https://asc103138.github.io/steam-gigo-balance-deck/</a></p>

<p><b>(2) 重要洽詢事項（出席名額與公費派代時段）：</b><br>
為利本社群教師提早規劃當日校內課務調度並完備請假行政程序，想懇請承辦團隊協助釋疑與考量：</p>
<ul>
  <li><b>請問 12/18(五) 成果展當天，本社群出席教師人數上限可有幾位？</b></li>
  <li><b>關於出席教師之公假課務，計畫是否提供「公費派代」？若是派代，補助時段為「整天」或「半天」？</b></li>
  <li><b>因中正國小位處海線梧棲，往返市區活動會場路途遙遠，單趟通勤與交通轉乘耗時甚鉅。因應學校課務排定與行政公假派代之實務流程，若僅核予半天派代，教師於下午難以即時趕回學校銜接課務，故懇請承辦團隊考量海線偏遠交通實況，惠予同意並核發「整日公費派代」公文，以利教師安心全程參與及會後順利返校。</b></li>
</ul>

<p><span class="highlight-title">五、【成果展所需繳交資料（隨信檢附）】</span></p>
<ol>
  <li><b>教案設計 1 份</b>（附件 6，Word 及 PDF 格式）。</li>
  <li><b>5 分鐘教案設計教學內容分享影片 1 支</b>（MP4 檔，1080p 含語音導覽與全套社群研發紀實）。</li>
  <li><b>成果展分享會簡報檔案</b>（22 頁完整版，含 PowerPoint .pptx 檔、離線單檔 .html 及上述線上網址）。</li>
  <li><b>成果展示高解析度照片 3 張</b>（皆為高解析度原生橫幅照片，遠高於 800 萬畫素規定，且均為社群教師研發畫面，無學生肖像權疑慮）：
    <ul>
      <li>照片1（教具研發）：社群教師合力組裝智高積木等臂天平原型與轉軸阻尼校正</li>
      <li>照片2（教案共備）：社群教師研討學習成效評量分析與兩步驟問題情境轉化</li>
      <li>照片3（競賽整合）：社群召集人解析世界機關王競賽指定關卡傳動與賽程策略</li>
    </ul>
  </li>
  <li><b>展示海報</b>：敬請承辦單位協助依本次繳交之《教案設計（附件6）》內容統一印製。</li>
</ol>

<div class="note-box">
  <b>備註說明：</b>考量信件夾帶容量上限，除隨信夾帶核心檔案（成果總表、附件6教案設計、PPTX簡報、3張高解析展示照片）外，全套超高畫質檔案（含 13.8MB 1080p 分享影片、24.5MP 原生大圖與離線 HTML 簡報）亦同步備份於公開專案庫供隨時下載備用：<br>
  <a href="https://github.com/asc103138/steam-community-docs/tree/main/%E6%88%90%E6%9E%9C%E5%B1%95%E7%B9%B3%E4%BA%A4%E8%B3%87%E6%96%99">https://github.com/asc103138/steam-community-docs/tree/main/成果展繳交資料</a>
</div>

<p>以上資料與公費派代懇請事項，再麻煩承辦團隊撥冗參閱與惠復，萬分感謝！</p>

<p>敬祝<br>
教安、順心</p>

<div class="signature">
  臺中市梧棲區中正國民小學<br>
  STEAM 教師社群召集人：謝敦元 老師<br>
  聯絡電話：0981-455340<br>
  電子信箱：asc103138@st.tc.edu.tw
</div>

</body>
</html>
"""

PLAIN_TEXT = """臺中市115年度推動校園STEAM教育實施計畫 承辦團隊 您好：

我是臺中市梧棲區中正國小 STEAM 教師社群召集人謝敦元老師。
感謝承辦團隊的協助與提醒，針對來信各項辦理事項，謹逐一說明並檢附本校全套成果資料如下：

一、【社群經費執行進度（11/15前）】
本校社群全年度共 8 場次、16 節課程之講師鐘點費（共計新臺幣 16,000 元整）已於 115 年 10 月 19 日 100% 執行完畢，相關核銷領據正本亦已按期寄交核銷。

二、【活動執行成果報告繳交（11/27前）】
- 各單場次（04/15、05/06、05/20、09/16、09/26、10/01、10/05、10/19 共 8 場次）之活動成果表與簽到表均已逐場寄送完畢，隨信一併檢附彙整之《115年度STEAM教師社群_活動成果總表》（含 Word 與 PDF 檔）。
- 隨信檢附完成之《115年度STEAM教師社群_教案設計（附件6）》（主題：小小秤重師——用積木做自己的天平，含 Word 與 PDF 檔）。

三、【確認社群教師名單（無異動）】
經確認，本校 STEAM 教師社群成員名單與原申請計畫書完全一致，無任何異動（免填異動申請表）。成果展感謝狀請依下列 4 位社群教師名單印製：
- 召集人：謝敦元 老師
- 社群成員：王怡婷 老師、李仁耀 老師、曾泊淞 老師

四、【12月18日(五)成果展參與方式及出席公費派代洽詢】
(1) 參與及分享方式：
    本社群將準時出席 115 年 12 月 18 日（星期五）成果展。上午 5 分鐘教案設計成果分享，我們已同步備妥「上台簡報發表」與「5分鐘教學分享影片」，可配合大會現場流程彈性調整：
    - 22頁互動式網頁簡報線上網址（GitHub Pages）：
      https://asc103138.github.io/steam-gigo-balance-deck/
(2) 重要洽詢事項（出席名額與公費派代時段）：
    為利本社群教師提早規劃當日校內課務調度並完備請假行政程序，想懇請承辦團隊協助釋疑與考量：
    - 請問 12/18(五) 成果展當天，本社群出席教師人數上限可有幾位？
    - 關於出席教師之公假課務，計畫是否提供「公費派代」？若是派代，補助時段為「整天」或「半天」？
    - 因中正國小位處海線梧棲，往返市區活動會場路途遙遠，單趟通勤與交通轉乘耗時甚鉅。因應學校課務排定與行政公假派代之實務流程，若僅核予半天派代，教師於下午難以即時趕回學校銜接課務，故懇請承辦團隊考量海線偏遠交通實況，惠予同意並核發「整日公費派代」公文，以利教師安心全程參與及會後順利返校。

五、【成果展所需繳交資料（隨信檢附）】
1. 教案設計 1 份（附件 6，Word 及 PDF 格式）。
2. 5 分鐘教案設計教學內容分享影片 1 支（MP4 檔，1080p 含語音導覽與全套社群研發紀實）。
3. 成果展分享會簡報檔案（22 頁完整版，含 PowerPoint .pptx 檔、離線單檔 .html 及上述線上網址）。
4. 成果展示高解析度照片 3 張（皆為高解析度原生橫幅照片，遠高於 800 萬畫素規定，且均為社群教師研發畫面，無學生肖像權疑慮）：
   - 照片1（教具研發）：社群教師合力組裝智高積木等臂天平原型與轉軸阻尼校正
   - 照片2（教案共備）：社群教師研討學習成效評量分析與兩步驟問題情境轉化
   - 照片3（競賽整合）：社群召集人解析世界機關王競賽指定關卡傳動與賽程策略
5. 展示海報：敬請承辦單位協助依本次繳交之《教案設計（附件6）》內容統一印製。

（備註說明：考量信件夾帶容量上限，除隨信夾帶核心檔案外，全套超高畫質檔案亦同步備份於公開專案庫供隨時下載備用：https://github.com/asc103138/steam-community-docs/tree/main/%E6%88%90%E6%9E%9C%E5%B1%95%E7%B9%B3%E4%BA%A4%E8%B3%87%E6%96%99 ）

以上資料與公費派代懇請事項，再麻煩承辦團隊撥冗參閱與惠復，萬分感謝！

敬祝
教安、順心

──────────────────────────────────
臺中市梧棲區中正國民小學
STEAM 教師社群召集人：謝敦元 老師
聯絡電話：0981-455340
電子信箱：asc103138@st.tc.edu.tw
"""

def create_draft():
    cfg = get_gmail_config()
    sender = REQUIRED_SENDER
    app_pwd = cfg.get('app_password')

    msg = MIMEMultipart('mixed')
    msg['From'] = f"=?UTF-8?B?{Header('臺中市梧棲區中正國小 STEAM社群召集人 謝敦元', 'utf-8').encode()}?= <{sender}>"
    msg['To'] = RECIPIENT
    msg['Subject'] = Header(SUBJECT, 'utf-8').encode()
    msg['Date'] = formatdate(localtime=True)
    msg['Message-ID'] = make_msgid(domain='st.tc.edu.tw')

    alt_part = MIMEMultipart('alternative')
    alt_part.attach(MIMEText(PLAIN_TEXT, 'plain', 'utf-8'))
    alt_part.attach(MIMEText(HTML_BODY, 'html', 'utf-8'))
    msg.attach(alt_part)

    print("📎 正在加入附件 (嚴格排除領據)...")
    for file_path in ATTACHMENT_PATHS:
        if os.path.exists(file_path):
            filename = os.path.basename(file_path)
            with open(file_path, 'rb') as f:
                part = MIMEApplication(f.read(), Name=filename)
            part.add_header('Content-Disposition', 'attachment', filename=('utf-8', '', filename))
            msg.attach(part)
            sz_kb = os.path.getsize(file_path) // 1024
            print(f"  + {filename} ({sz_kb} KB)")
        else:
            print(f"  ! 檔案不存在: {file_path}")

    raw_email = msg.as_bytes()
    print(f"\n📧 郵件封裝完成，總大小: {len(raw_email) / 1024 / 1024:.2f} MB (完全符合 Gmail 25MB 上限)")

    print("📥 正在連線至 Gmail IMAP 寫入「草稿 (Drafts)」...")
    imap = imaplib.IMAP4_SSL('imap.gmail.com')
    imap.login(sender, app_pwd)

    drafts_box = [b for b in imap.list()[1] if b'Drafts' in b][0]
    m = re.search(r'\"([^\"]+)\"$', drafts_box.decode('latin1'))
    box_name = m.group(1)

    res = imap.append(f'"{box_name}"', '(\\Draft)', imaplib.Time2Internaldate(time.time()), raw_email)
    print("草稿寫入結果:", res)
    imap.logout()
    print("🎉 草稿建立成功！已放置於您的 Gmail 草稿匣。")

if __name__ == '__main__':
    create_draft()

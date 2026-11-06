#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
檢查 Gmail 寄件備份 (Sent Mail) 確認信件是否已成功發送給 tc.steam114@gmail.com
"""

import sys
import re
import imaplib

sys.path.append(r"d:\antui\steam成果製作\scripts")
from send_gmail import get_gmail_config

cfg = get_gmail_config()
imap = imaplib.IMAP4_SSL('imap.gmail.com')
imap.login(cfg['sender'], cfg['app_password'])

sent_boxes = [b for b in imap.list()[1] if b'Sent' in b]
if sent_boxes:
    box_name = re.search(r'\"([^\"]+)\"$', sent_boxes[0].decode('latin1')).group(1)
    imap.select(f'"{box_name}"')
    res, msg_ids = imap.search(None, 'ALL')
    id_list = msg_ids[0].split()
    print(f"寄件備份總數: {len(id_list)}")
    if id_list:
        latest_id = id_list[-1]
        res, data = imap.fetch(latest_id, '(BODY[HEADER.FIELDS (SUBJECT TO DATE FROM)])')
        header_text = data[0][1].decode('utf-8', errors='ignore')
        print("最新寄出郵件標頭:\n" + header_text)

imap.logout()

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
檢查最新寄出信件的附件名稱，嚴格確認是否有領據
"""

import sys
import re
import imaplib
import email
from email.header import decode_header

sys.path.append(r"d:\antui\steam成果製作\scripts")
from send_gmail import get_gmail_config

cfg = get_gmail_config()
imap = imaplib.IMAP4_SSL('imap.gmail.com')
imap.login(cfg['sender'], cfg['app_password'])

sent_boxes = [b for b in imap.list()[1] if b'Sent' in b]
box_name = re.search(r'\"([^\"]+)\"$', sent_boxes[0].decode('latin1')).group(1)
imap.select(f'"{box_name}"')
res, msg_ids = imap.search(None, 'ALL')
latest_id = msg_ids[0].split()[-1]

res, data = imap.fetch(latest_id, '(RFC822)')
raw_email = data[0][1]
msg = email.message_from_bytes(raw_email)

print("=== 最新寄出信件檢查報告 ===")
print("寄件日期:", msg.get('Date'))
print("收件人:", msg.get('To'))
print("主旨:", msg.get('Subject'))

attachments = []
for part in msg.walk():
    fn = part.get_filename()
    if fn:
        decoded_pieces = decode_header(fn)
        filename = ""
        for piece, encoding in decoded_pieces:
            if isinstance(piece, bytes):
                filename += piece.decode(encoding or 'utf-8', errors='ignore')
            else:
                filename += piece
        attachments.append(filename)

print(f"\n📎 成功夾帶附件數量: {len(attachments)} 個")
has_receipt = False
for a in attachments:
    print(f"  ✓ {a}")
    if "領據" in a or "清冊" in a:
        has_receipt = True

if has_receipt:
    print("❌ 警告：附件中含有內部報銷檔案！")
else:
    print("✅ 嚴格合規：絕無夾帶內部報銷之《領據》與《清冊》！")

imap.logout()

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
測試 IMAP 儲存草稿功能
"""

import imaplib
import re
import os
import sys

sys.path.append(r"d:\antui\steam成果製作\scripts")
from send_gmail import get_gmail_config

cfg = get_gmail_config()
imap = imaplib.IMAP4_SSL('imap.gmail.com')
imap.login(cfg['sender'], cfg['app_password'])

drafts_box = [b for b in imap.list()[1] if b'Drafts' in b][0]
m = re.search(r'\"([^\"]+)\"$', drafts_box.decode('latin1'))
box_name = m.group(1)
print("Drafts box name:", box_name)

res, data = imap.select(f'"{box_name}"')
print("Select result:", res, data)
imap.logout()

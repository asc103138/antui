import imaplib
import email
import sys
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(SCRIPT_DIR)
from send_gmail import get_gmail_config, REQUIRED_SENDER

cfg = get_gmail_config()
user = REQUIRED_SENDER
pwd = cfg.get('app_password').replace(' ', '')

mail = imaplib.IMAP4_SSL('imap.gmail.com')
mail.login(user, pwd)
mail.select('INBOX')

status, messages = mail.search(None, 'FROM', '"mailer-daemon"')
print('Bounce messages count:', len(messages[0].split()))
if messages[0].split():
    latest_id = messages[0].split()[-1]
    res, msg_data = mail.fetch(latest_id, '(RFC822)')
    msg = email.message_from_bytes(msg_data[0][1])
    print('Subject:', msg['Subject'])
    print('Date:', msg['Date'])
    
    body_text = ''
    if msg.is_multipart():
        for part in msg.walk():
            ctype = part.get_content_type()
            cdisp = str(part.get('Content-Disposition'))
            if ctype == 'text/plain' and 'attachment' not in cdisp:
                body_text += part.get_payload(decode=True).decode('utf-8', errors='ignore')
    else:
        body_text = msg.get_payload(decode=True).decode('utf-8', errors='ignore')
    print('--- Bounce Body ---')
    print(body_text[:2000])

mail.logout()

import imaplib, email, os, sys
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(SCRIPT_DIR)
from send_gmail import get_gmail_config, REQUIRED_SENDER

cfg = get_gmail_config()
mail = imaplib.IMAP4_SSL('imap.gmail.com')
mail.login(REQUIRED_SENDER, cfg.get('app_password').replace(' ', ''))
mail.select('INBOX')

status, messages = mail.search(None, 'FROM', '"mailer-daemon"')
for msg_id in messages[0].split():
    res, msg_data = mail.fetch(msg_id, '(RFC822)')
    msg = email.message_from_bytes(msg_data[0][1])
    print(msg_id.decode(), 'Subject:', msg['Subject'], 'Date:', msg['Date'])
mail.logout()

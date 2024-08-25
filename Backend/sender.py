import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import os

import config

def sendMail():
    message = MIMEMultipart()
    message['From'] = config.FROM_ADRESS
    message['To'] = config.TO_ADRESS
    message['Subject'] = config.SUBJECT
    message.attach(MIMEText(config.BODY, 'plain'))
    attachmentPath = config.FINAL_WORD_FILENAME
    filename = os.path.basename(attachmentPath)
    with open(attachmentPath, 'rb') as attachment :
        part = MIMEBase('application', 'octet-stream')
        part.set_payload(attachment.read())
    encoders.encode_base64(part)
    part.add_header('Content-Disposition', f'attachment; filename={filename}')
    message.attach(part)
    try:
        with smtplib.SMTP_SSL(config.SMTP, config.PORT) as server:
            server.login(config.FROM_ADRESS, config.MAIL_PASSWORD)
            server.send_message(message)
    except Exception as e:
        print(f"Erreur lors de l'envoie du mail : {e}")
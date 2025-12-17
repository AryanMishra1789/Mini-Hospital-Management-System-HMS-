import os
import json
import smtplib
from email.message import EmailMessage

SMTP_HOST = os.getenv('SMTP_HOST', 'smtp.gmail.com')
SMTP_PORT = int(os.getenv('SMTP_PORT', '587'))
SMTP_USER = os.getenv('SMTP_USER')
SMTP_PASS = os.getenv('SMTP_PASS')


def send_email(event, context):
    """Lambda handler for sending emails.
    
    Expects a JSON body with keys:
      - action: SIGNUP_WELCOME | BOOKING_CONFIRMATION
      - to: recipient email
      - subject: optional subject
      - body: optional HTML/text body
    """
    try:
        body = event.get('body')
        if isinstance(body, str):
            data = json.loads(body)
        else:
            data = body or {}

        action = data.get('action')
        to = data.get('to')
        subject = data.get('subject') or f'HMS: {action}'
        content = data.get('body') or ''

        msg = EmailMessage()
        msg['Subject'] = subject
        msg['From'] = SMTP_USER
        msg['To'] = to
        msg.set_content(content)

        with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as smtp:
            smtp.ehlo()
            smtp.starttls()
            smtp.login(SMTP_USER, SMTP_PASS)
            smtp.send_message(msg)

        return {'statusCode': 200, 'body': json.dumps({'status': 'sent'})}
    except Exception as e:
        return {'statusCode': 500, 'body': json.dumps({'error': str(e)})}

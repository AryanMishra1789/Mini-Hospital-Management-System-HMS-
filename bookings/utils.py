import os
import json
import logging
import requests

logger = logging.getLogger(__name__)


def send_email_notification(action: str, to_email: str, subject: str = None, body: str = None):
    """Send a notification to the serverless email endpoint.
    
    Looks for `SERVERLESS_EMAIL_URL` in env, falls back to http://localhost:3000/send
    """
    url = os.getenv('SERVERLESS_EMAIL_URL', 'http://localhost:3000/send')
    payload = {
        'action': action,
        'to': to_email,
        'subject': subject or f'HMS: {action}',
        'body': body or '',
    }
    headers = {'Content-Type': 'application/json'}
    try:
        resp = requests.post(url, data=json.dumps(payload), headers=headers, timeout=5)
        resp.raise_for_status()
        return resp.json() if resp.text else {}
    except Exception as exc:
        logger.exception('Failed sending email notification')
        return {'error': str(exc)}

import email
import email.policy
from email.message import EmailMessage
from typing import Dict, Any

def parse_raw_email(raw_content: str | bytes) -> Dict[str, Any]:
    """
    Parses a raw email (string or bytes) into a structured dictionary.
    """
    if isinstance(raw_content, str):
        msg = email.message_from_string(raw_content, policy=email.policy.default)
    else:
        msg = email.message_from_bytes(raw_content, policy=email.policy.default)
    
    return _extract_email_info(msg)

def _extract_email_info(msg: EmailMessage) -> Dict[str, Any]:
    """
    Extracts headers, body, and attachments from parsed email message.
    """
    # Extract headers
    headers = {k: v for k, v in msg.items()}
    
    # Extract structural info
    subject = msg.get('Subject', '')
    sender = msg.get('From', '')
    recipient = msg.get('To', '')
    date = msg.get('Date', '')
    
    # Extract body and attachments
    body = ""
    attachments = []
    
    if msg.is_multipart():
        for part in msg.walk():
            content_type = part.get_content_type()
            content_disposition = str(part.get('Content-Disposition'))
            
            if 'attachment' in content_disposition:
                filename = part.get_filename()
                if filename:
                    attachments.append({
                        'filename': filename,
                        'content_type': content_type,
                        'size': len(part.get_payload())
                    })
            elif content_type in ('text/plain', 'text/html'):
                try:
                    payload = part.get_payload(decode=True)
                    if payload:
                        body += payload.decode('utf-8', errors='ignore') + "\n"
                except Exception:
                    pass
    else:
        try:
            payload = msg.get_payload(decode=True)
            if payload:
                body = payload.decode('utf-8', errors='ignore')
        except Exception:
            body = msg.get_payload()
            
    return {
        'headers': headers,
        'subject': subject,
        'sender': sender,
        'recipient': recipient,
        'date': date,
        'body': body,
        'attachments': attachments
    }

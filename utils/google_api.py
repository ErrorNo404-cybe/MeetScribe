from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
import base64
from email.mime.text import MIMEText

SCOPES = ['https://www.googleapis.com/auth/gmail.send']

def get_gmail_service(creds_dict):
    creds = Credentials.from_authorized_user_info(creds_dict, SCOPES)
    return build('gmail', 'v1', credentials=creds)

def send_email(service, to, subject, body):
    message = MIMEText(body)
    message['to'] = to
    message['subject'] = subject
    raw = base64.urlsafe_b64encode(message.as_string().encode()).decode()
    service.users().messages().send(userId='me', body={'raw': raw}).execute()
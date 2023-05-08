import os
import sys

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

SCOPES = ['https://www.googleapis.com/auth/drive.readonly']

def get_drive_service():
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json()) 
    service = build("drive", "v3", credentials=creds)
    return service

def get_file_contents(service, file_id):
    file = service.files().get(fileId = file_id).execute()
    if file['mimeType'] == "application/vnd.google-apps.document":
        content = service.files().export(fileId=file_id, mimeType='text/html').execute()
        print(content.decode('utf-8'))
    elif file['mimeType'] == "application/vnd.google-apps.spreadsheet":
        content = service.files().export(fileId=file_id, mimeType='text/csv').execute()
        print(content.decode('utf-8'))

if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise Exception("Usage: get-contents.py VERSION_FILE_PATH")
    version_file_path = sys.argv[1]
    file_id = os.path.splitext(os.path.basename(version_file_path))[0]
    service = get_drive_service()
    get_file_contents(service, file_id)


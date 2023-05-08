import os
import sys

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

SCOPES = ['https://www.googleapis.com/auth/drive.metadata.readonly']

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

def get_file_versions(service, folder_id):
    query = f"'{folder_id}' in parents and trashed = false"
    while True:
        results = service.files().list(q=query, fields="nextPageToken, files(id, name, mimeType, version)").execute()
        files = results.get("files", [])

        if not files:
            print("No files found.")
        else:
            for file in files:
                if file["mimeType"] == "application/vnd.google-apps.folder":
                    get_file_versions(service, file["id"])
                elif file["mimeType"] in ["application/vnd.google-apps.document", "application/vnd.google-apps.spreadsheet"]:
                    revision = service.revisions().get(fileId=file["id"], revisionId='head').execute()
                    revision_id = revision['id']
                    extension = {
                        'application/vnd.google-apps.document': 'google-docs-version',
                        'application/vnd.google-apps.spreadsheet': 'google-sheets-version'
                    }[file['mimeType']]
                    path = f"out/versions/{file['id']}.{extension}"
                    revision_on_disk = ""
                    if os.path.exists(path):
                        with open(path, 'r') as reader:
                            revision_on_disk = reader.read()
                    if revision_on_disk != revision_id:
                        with open(path, 'w') as writer:
                            writer.write(revision_id)
                        print(f"Writing {file['id']} ({file['name']} | {file['mimeType']}): {revision_id}")
                    else:
                        print(f"Skipping {file['id']} ({file['name']} | {file['mimeType']}) - current version matches")
                else:
                    print(f"Skipping {file['id']} ({file['name']} | {file['mimeType']}) - unsupported mime type")
        
        page_token = results.get('nextPageToken', None)
        if page_token is None:
            break

if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise Exception("Usage: get-versions.py YOUR_FOLDER_ID")
    folder_id = sys.argv[1]
    service = get_drive_service()
    get_file_versions(service, folder_id)

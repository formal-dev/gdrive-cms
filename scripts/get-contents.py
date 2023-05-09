import os
import sys

from utils.drive_authentication import get_drive_service

def get_file_contents(service, file_id):
    file = service.files().get(fileId = file_id).execute()
    if file['mimeType'] == "application/vnd.google-apps.document":
        # TODO - switch to using zip exports so we can handle images more cleanly
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


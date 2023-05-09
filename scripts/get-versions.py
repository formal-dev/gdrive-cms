import os
import sys

from utils.drive_authentication import get_drive_service

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

from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload, MediaIoBaseDownload
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow

from pathlib import Path

PARENT = Path("/home/mohamed/Documents/Stuff/Drive")

# Define the required Google Drive API scopes
SCOPES = ['https://www.googleapis.com/auth/drive']


def authenticate():
    """Authenticate and return the Google Drive service."""
    creds = None
    token_path = "token.json"

    # Load existing credentials if available
    if Path(token_path).exists():
        creds = Credentials.from_authorized_user_file(token_path, SCOPES)

    # If credentials are not valid, perform OAuth authentication
    if not creds or not creds.valid:
        flow = InstalledAppFlow.from_client_secrets_file(
            "credentials.json", SCOPES)
        creds = flow.run_local_server(port=0)
        # Save credentials for future use
        with open(token_path, "w") as token:
            token.write(creds.to_json())

    return build("drive", "v3", credentials=creds)


def list_files_in_folder(service, folder_id):
    """List all files in a specified Google Drive folder."""
    query = f"'{folder_id}' in parents and trashed=false"
    results = service.files().list(q=query, fields="files(id, name)").execute()
    files = results.get("files", [])

    if not files:
        print("No files found.")
        return []

    return [
        file['name']
        for file in files
    ]
    # print(f"ID : {file['id']}")
    # print(f"Name: {file['name']}")


def upload_file(service, file_path, folder_id):
    """Upload a file to a specific Google Drive folder."""
    file_name = file_path.name

    file_metadata = {
        "name": file_name,
        "parents": [folder_id]  # Set the target folder
    }

    media = MediaFileUpload(f"{file_path}", resumable=True)
    uploaded_file = service.files().create(
        body=file_metadata, media_body=media, fields="id").execute()

    print(
        f"File '{file_name}' uploaded successfully. File ID: {uploaded_file['id']}")


def download_file(service, file_id, file_name, save_path=""):
    """Download a file from Google Drive and save it locally."""
    request = service.files().get_media(fileId=file_id)
    file_path = Path(save_path, file_name)

    with open(file_path, "wb") as file:
        downloader = MediaIoBaseDownload(file, request)
        done = False
        while not done:
            status, done = downloader.next_chunk()
            print(
                f"Downloading {file_name}... {int(status.progress() * 100)}%")

    print(f"File '{file_name}' downloaded successfully to '{file_path}'.")


if __name__ == "__main__":
    service = authenticate()
    print("Connected !")
    # Replace with the actual folder ID
    print("Files listed !")
    # Upload a file
    # Replace with the actual file path
    dir_path = "/home/mohamed/Documents/Drive"

    nb = 1
    folder_id = "1AdtI_xSZUopHgLolKt-UJi7DJPGc4NO3"
    while nb:
        nb = 0
        files = list_files_in_folder(service, folder_id)
        for file_path in Path(f"{dir_path}/Files").rglob("*"):
            if file_path.is_dir():
                continue
            if file_path.name in files:
                file_path.unlink()
                continue
            upload_file(service, file_path, folder_id)
            nb += 1

    nb = 1
    folder_id = "1wFUlLRl7XDv1iYJCCfW_MqvnBdco2R3V"
    while nb:
        nb = 0
        files = list_files_in_folder(service, folder_id)
        for file_path in Path(f"{dir_path}/Images").rglob("*"):
            if file_path.is_dir():
                continue
            if file_path.name in files:
                file_path.unlink()
                continue
            upload_file(service, file_path, folder_id)
            nb += 1

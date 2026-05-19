import os
import webbrowser
import tkinter as tk
from tkinter import filedialog
import subprocess

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

SCOPES = ["https://www.googleapis.com/auth/drive.file"]
GOOGLE_SLIDES_MIME = "application/vnd.google-apps.presentation"


def get_drive_service():
    creds = None
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
            creds = flow.run_local_server(port=0)
        with open("token.json", "w") as f:
            f.write(creds.to_json())
    return build("drive", "v3", credentials=creds)


def pick_files():
    try:
        result = subprocess.run(
            [
                "zenity", "--file-selection",
                "--multiple",
                "--separator=|",
                "--title=Select PowerPoint files",
                "--file-filter=PowerPoint files | *.ppt *.pptx",
                "--file-filter=All files | *",
            ],
            capture_output=True, text=True, check=True,
        )
        return result.stdout.strip().split("|")
    except subprocess.CalledProcessError:
        return []  # user hit cancel
def upload_as_slides(service, path):
    name = os.path.splitext(os.path.basename(path))[0]
    metadata = {"name": name, "mimeType": GOOGLE_SLIDES_MIME}
    media = MediaFileUpload(
        path,
        mimetype="application/vnd.openxmlformats-officedocument.presentationml.presentation",
        resumable=True,
    )
    file = service.files().create(
        body=metadata, media_body=media, fields="id, webViewLink"
    ).execute()
    return file["webViewLink"]


def main():
    files = pick_files()
    if not files:
        print("No files selected.")
        return

    service = get_drive_service()
    for path in files:
        print(f"Uploading: {path}")
        try:
            link = upload_as_slides(service, path)
            print(f"  -> {link}")
            webbrowser.open_new_tab(link)
        except Exception as e:
            print(f"  Failed: {e}")


if __name__ == "__main__":
    main()

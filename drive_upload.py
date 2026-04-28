from pydrive2.auth import GoogleAuth
from pydrive2.drive import GoogleDrive
import os

def upload_to_drive(file_path):
    gauth = GoogleAuth()

    # 👇 IMPORTANT LINE (force correct path)
    gauth.LoadClientConfigFile("client_secrets.json")

    gauth.LocalWebserverAuth()

    drive = GoogleDrive(gauth)

    file = drive.CreateFile({'title': os.path.basename(file_path)})
    file.SetContentFile(file_path)
    file.Upload()

    print("Uploaded to Google Drive")

    return file['id']
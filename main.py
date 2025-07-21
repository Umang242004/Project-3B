import os
import json
import gspread
import requests
from google.oauth2.service_account import Credentials
from datetime import datetime, timedelta
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload
import io

# Setup credentials
creds_dict = json.loads(os.environ["GOOGLE_CREDENTIALS_JSON"])
creds = Credentials.from_service_account_info(creds_dict, scopes=[
    "https://www.googleapis.com/auth/drive",
    "https://www.googleapis.com/auth/spreadsheets"
])
gc = gspread.authorize(creds)

# Sheet & Drive
sheet_id = os.environ["SHEET_ID"]
drive_folder_id = os.environ["DRIVE_FOLDER_ID"]
upload_url = os.environ["UPLOAD_ENDPOINT"]
sheet = gc.open_by_key(sheet_id).sheet1

# Step 1: Get 50 unscheduled videos
records = sheet.get_all_records()
pending = [row for row in records if row['Status'].strip().lower() == 'pending'][:50]

# Step 2: Fetch videos from Drive
service = build('drive', 'v3', credentials=creds)
videos = []

for idx, row in enumerate(pending):
    filename = row['Video Name']
    caption = row['Caption']
    query = f"'{drive_folder_id}' in parents and name='{filename}'"
    results = service.files().list(q=query, fields="files(id, name)").execute()
    items = results.get('files', [])

    if not items:
        print(f"File {filename} not found.")
        continue

    file_id = items[0]['id']
    request = service.files().get_media(fileId=file_id)
    fh = io.BytesIO()
    downloader = MediaIoBaseDownload(fh, request)
    done = False
    while not done:
        _, done = downloader.next_chunk()

    video_bytes = fh.getvalue()

    # Prepare for upload
    videos.append({
        "filename": filename,
        "caption": caption,
        "index": idx,
        "content": video_bytes.hex()
    })

# Step 3: Send to upload server
payload = json.dumps({"videos": videos})
response = requests.post(upload_url, data=payload, headers={'Content-Type': 'application/json'})
print(response.status_code, response.text)

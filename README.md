
# Instagram Reels Uploader (Cloud-Based)

This is a fully automated, cloud-based uploader for Instagram Reels using GitHub Actions + Fly.io + Google Sheets.

## 🔧 Setup Instructions

1. Set up secrets in GitHub:
   - `GOOGLE_CREDENTIALS_JSON`: Your service account JSON
   - `SHEET_ID`: Your Google Sheet ID
   - `DRIVE_FOLDER_ID`: Folder where your videos are
   - `UPLOAD_ENDPOINT`: Your Fly.io deployed endpoint

2. Deploy Fly.io:
   - Install Fly.io CLI
   - `fly launch`
   - `fly deploy`

3. Update Google Sheet with:
   - Video Name, Caption, Status (Pending)

The script schedules 5 videos/day at 9AM, 12PM, 3PM, 6PM, 9PM over 10 days.

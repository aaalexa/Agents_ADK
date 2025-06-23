#!/usr/bin/env python3
"""
Google OAuth Setup Script for Calendar, Sheets, and Drive

This script helps you set up OAuth 2.0 credentials for integration with
Google Calendar, Google Sheets, and Google Drive.
"""

import os
from pathlib import Path
from fastapi import APIRouter
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# Scopes for Calendar, Sheets, and Drive
SCOPES = [
    "https://www.googleapis.com/auth/calendar",
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

# Paths
TOKEN_PATH = Path(os.path.expanduser("~/.credentials/google_token.json"))
CREDENTIALS_PATH = Path("credentials.json")


def setup_oauth():
    """Set up OAuth 2.0 and test Google API connections"""
    # print("\n=== Google OAuth Setup ===\n")

    if not CREDENTIALS_PATH.exists():
        # print(f"Error: {CREDENTIALS_PATH} not found!")
        # print("\nTo set up Google API integration:")
        # print("1. Go to https://console.cloud.google.com/")
        # print("2. Create/select a project")
        # print("3. Enable Calendar, Sheets, and Drive APIs")
        # print("4. Create OAuth 2.0 credentials (Desktop app)")
        # print("5. Download and save as 'credentials.json' here")
        return False

    # print(f"Found credentials.json. Setting up OAuth flow...")

    try:
        # Run OAuth flow
        flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_PATH, SCOPES)
        creds = flow.run_local_server(port=8000)

        # Save credentials
        TOKEN_PATH.parent.mkdir(parents=True, exist_ok=True)
        TOKEN_PATH.write_text(creds.to_json())

        # print(f"\n✅ Credentials saved to: {TOKEN_PATH}")

        # Test Calendar API
        # print("\n🔁 Testing Google Calendar...")
        calendar_service = build("calendar", "v3", credentials=creds)
        calendars = calendar_service.calendarList().list().execute().get("items", [])
        # if calendars:
        #     print(f"✅ Found {len(calendars)} calendars:")
        #     for calendar in calendars:
        #         print(f"  - {calendar['summary']} ({calendar['id']})")
        # else:
        #     print("⚠️ No calendars found.")

        # Test Sheets API
        # print("\n🔁 Testing Google Sheets...")
        sheets_service = build("sheets", "v4", credentials=creds)
        # You can replace this with your own sheet ID to test
        # print("✅ Google Sheets API is ready.")

        # Test Drive API
        # print("\n🔁 Testing Google Drive...")
        drive_service = build("drive", "v3", credentials=creds)
        files = drive_service.files().list(pageSize=5).execute().get("files", [])
        # print(f"✅ Google Drive connected. {len(files)} files found:")
        # for f in files:
        #     print(f"  - {f['name']} ({f['id']})")

        # print("\n🎉 OAuth setup complete! All services are connected.")
        return True

    except Exception as e:
        # print(f"\n❌ Error during setup: {str(e)}")
        return False


if __name__ == "__main__":
    setup_oauth()

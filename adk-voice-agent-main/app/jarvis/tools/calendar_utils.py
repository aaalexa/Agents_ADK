"""
Utility functions for Google Calendar integration.
"""

import json
import os
from datetime import datetime
from pathlib import Path

import dateparser
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# Define scopes needed for Google Calendar
SCOPES = ["https://www.googleapis.com/auth/calendar"]

# Path for token storage
# TOKEN_PATH = Path(os.path.expanduser("~/.credentials/calendar_token.json"))
# CREDENTIALS_PATH = Path("credentials.json")


# def get_calendar_service():
#     """
#     Authenticate and create a Google Calendar service object.

#     Returns:
#         A Google Calendar service object or None if authentication fails
#     """
#     creds = None

#     # Check if token exists and is valid
#     if TOKEN_PATH.exists():
#         creds = Credentials.from_authorized_user_info(
#             json.loads(TOKEN_PATH.read_text()), SCOPES
#         )

#     # If credentials don't exist or are invalid, refresh or get new ones
#     if not creds or not creds.valid:
#         if creds and creds.expired and creds.refresh_token:
#             creds.refresh(Request())
#         else:
#             if not CREDENTIALS_PATH.exists():
#                 print(
#                     f"Error: {CREDENTIALS_PATH} not found. Please follow setup instructions."
#                 )
#                 return None

#             flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_PATH, SCOPES)
#             creds = flow.run_local_server(port=0)

#         # Save the credentials for the next run
#         TOKEN_PATH.parent.mkdir(parents=True, exist_ok=True)
#         TOKEN_PATH.write_text(creds.to_json())

#     # Create and return the Calendar service
#     return build("calendar", "v3", credentials=creds)


def get_calendar_service(access_token, refresh_token=None, client_id=None, client_secret=None):
    """
    Crea el servicio de Google Calendar usando el token recibido desde Django.
    """
    creds = Credentials(
        token=access_token,
        refresh_token=refresh_token,
        token_uri="https://oauth2.googleapis.com/token",
        client_id=client_id,
        client_secret=client_secret,
        scopes=SCOPES,
    )
    return build("calendar", "v3", credentials=creds)

def format_event_time(event_time):
    """
    Format an event time into a human-readable string.

    Args:
        event_time (dict): The event time dictionary from Google Calendar API

    Returns:
        str: A human-readable time string
    """
    if "dateTime" in event_time:
        # This is a datetime event
        dt = datetime.fromisoformat(event_time["dateTime"].replace("Z", "+00:00"))
        return dt.strftime("%Y-%m-%d %I:%M %p")
    elif "date" in event_time:
        # This is an all-day event
        return f"{event_time['date']} (All day)"
    return "Unknown time format"


def parse_datetime(datetime_str):
    """
    Parse a datetime string into a timezone-aware datetime object using dateparser.

    Args:
        datetime_str (str): A string representing a date and time

    Returns:
        datetime: A timezone-aware datetime object or None if parsing fails
    """
    # Primer intento con formatos conocidos
    formats = [
        "%Y-%m-%d %H:%M",
        "%Y-%m-%d %I:%M %p",
        "%Y-%m-%d",
        "%m/%d/%Y %H:%M",
        "%m/%d/%Y %I:%M %p",
        "%m/%d/%Y",
        "%B %d, %Y %H:%M",
        "%B %d, %Y %I:%M %p",
        "%B %d, %Y",
    ]
    for fmt in formats:
        try:
            dt = datetime.strptime(datetime_str, fmt)
            return dateparser.parse(dt.isoformat(), settings={"RETURN_AS_TIMEZONE_AWARE": True})
        except ValueError:
            continue

    # Segundo intento: dejar que dateparser lo maneje
    return dateparser.parse(datetime_str, settings={"RETURN_AS_TIMEZONE_AWARE": True})


def get_current_time() -> dict:
    """
    Get the current time and date

    Returns:
        dict: A dictionary with the current time and formatted date
    """
    now = datetime.now()
    formatted_date = now.strftime("%m-%d-%Y")
    return {
        "current_time": now.strftime("%Y-%m-%d %H:%M:%S"),
        "formatted_date": formatted_date,
    }

import os
import re
import datetime
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import subprocess
import argparse
import logging
import pytz

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/calendar']

# Configure logging
logging.basicConfig(filename='calendar_event_creator.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

def get_google_calendar_service(credentials_path, token_path):
    """Gets the Google Calendar API service object."""
    creds = None
    if os.path.exists(token_path):
        creds = Credentials.from_authorized_user_file(token_path, SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                credentials_path, SCOPES)
            creds = flow.run_local_server(port=0)
        with open(token_path, 'w') as token:
            token.write(creds.to_json())

    service = build('calendar', 'v3', credentials=creds)
    logging.info("Successfully authenticated with Google Calendar API.")
    return service

def find_markdown_files_with_ripgrep(directory, pattern):
    """Finds markdown files using ripgrep based on the given pattern."""
    try:
        result = subprocess.run(['rg', '-l', '-g', '*.md', pattern, directory], capture_output=True, text=True, check=True)
        markdown_files = result.stdout.strip().split('\n')
        logging.info(f"Found {len(markdown_files)} markdown files matching the pattern.")
        return markdown_files
    except subprocess.CalledProcessError as e:
        logging.error(f"Error running ripgrep: {e}")
        return []

def parse_markdown_file(filepath, timezone):
    """Parses a markdown file for date, time, and event text."""
    pattern = r"\(?\@\[\[(\d{8})\]\] (\d{2}:\d{2})\) (.*)"
    events = []

    with open(filepath, 'r') as f:
        for line in f:
            match = re.search(pattern, line)
            if match:
                date_str, time_str, text = match.groups()
                try:
                    # Parse the date and time string into a naive datetime object
                    event_datetime_naive = datetime.datetime.strptime(f"{date_str} {time_str}", "%Y%m%d %H:%M")

                    # Localize the naive datetime object to the specified timezone
                    event_datetime = timezone.localize(event_datetime_naive)

                    events.append((event_datetime, text))
                    logging.info(f"Found event in {filepath}: {event_datetime} - {text}")
                except ValueError:
                    logging.error(f"Error parsing date/time in line: {line.strip()}")

    return events

def get_existing_events(service, timeMin, timeMax):
    """Retrieves existing events from the Google Calendar within a specific time range."""
    events_result = service.events().list(calendarId='primary', timeMin=timeMin, timeMax=timeMax,
                                        singleEvents=True, orderBy='startTime').execute()
    events = events_result.get('items', [])

    existing_events = {}
    for event in events:
        start = event['start'].get('dateTime', event['start'].get('date'))
        existing_events[event['summary']] = start

    logging.info(f"Found {len(existing_events)} existing events in the specified time range.")
    return existing_events

def create_calendar_event(service, event_datetime, event_text, existing_events, timezone):
    """Creates a Google Calendar event if it doesn't already exist."""

    # Format the event_datetime to ISO 8601 format with timezone offset
    event_datetime_str = event_datetime.isoformat()

    # Check if the event already exists
    if event_text in existing_events and existing_events[event_text] == event_datetime_str:
        logging.info(f"Event '{event_text}' at '{event_datetime_str}' already exists. Skipping.")
        return

    event = {
        'summary': event_text,
        'start': {
            'dateTime': event_datetime_str,
            'timeZone': timezone.zone,
        },
        'end': {
            'dateTime': (event_datetime + datetime.timedelta(hours=1)).isoformat(),
            'timeZone': timezone.zone,
        },
    }

    try:
        event = service.events().insert(calendarId='primary', body=event).execute()
        logging.info(f"Event created: {event.get('htmlLink')}")
    except HttpError as error:
        logging.error(f"An error occurred: {error}")

def main():
    """Main function to scan directory and create calendar events."""
    parser = argparse.ArgumentParser(description="Scan a directory for markdown files and create Google Calendar events.")
    parser.add_argument("-d", "--directory", required=True, help="The directory to scan for markdown files.")
    parser.add_argument("-c", "--credentials", required=True, help="Path to the credentials.json file.")
    parser.add_argument("-tz", "--timezone", required=True, help="The timezone to use for parsing dates and creating events (e.g., America/New_York).")
    parser.add_argument("-t", "--token", required=False, default="token.json", help="Path to the token.json file (default: token.json).")

    args = parser.parse_args()
    directory_to_scan = args.directory
    credentials_path = args.credentials
    timezone_str = args.timezone
    token_path = args.token

    # Validate the timezone
    try:
        timezone = pytz.timezone(timezone_str)
    except pytz.UnknownTimeZoneError:
        logging.error(f"Invalid timezone: {timezone_str}")
        print(f"Invalid timezone: {timezone_str}")
        return

    service = get_google_calendar_service(credentials_path, token_path)

    # Define the pattern to search for in markdown files
    event_pattern = r"\(?\@\[\[\d{8}\]\] \d{2}:\d{2}\) .*"

    # Set time range for retrieving existing events
    now = datetime.datetime.now(timezone)  # Use timezone-aware datetime
    timeMin = now.isoformat()
    timeMax = (now + datetime.timedelta(days=30)).isoformat()

    # Get existing events within the time range
    existing_events = get_existing_events(service, timeMin, timeMax)

    # Use ripgrep to find markdown files containing the event pattern
    markdown_files = find_markdown_files_with_ripgrep(directory_to_scan, event_pattern)

    for filepath in markdown_files:
        events = parse_markdown_file(filepath, timezone)
        for event_datetime, event_text in events:
            create_calendar_event(service, event_datetime, event_text, existing_events, timezone)

if __name__ == '__main__':
    main()



## Abstract 

This script for syncing your reminders in markdown files (i.e in obsidian reminder plugin) with your google calendar. 
The remind file format:
```
(@[[20240101]] 00:00) Text for event 
```
This is going to google calendar at 2024.01.01 00:00 with the event text "Text for event"

![image](https://github.com/user-attachments/assets/20b209b6-38bb-42e1-aff9-db38d299113b)
![image](https://github.com/user-attachments/assets/f369f0b2-04fc-4c97-9cd9-90af12ed3990)

## Obtaining credentials for google calendar 

1. Create google project:
   - Open Google Cloud Project and API Setup
   - Create a Project:
   - Go to the Google Cloud Console.
   - Create a new project (e.g., "CalendarEventCreator").
   
2. Enable Google Calendar API:
   - In your project, navigate to "APIs & Services" > "Library."
   - Search for "Google Calendar API" and enable it.

3. Create Credentials:
   - Go to "APIs & Services" > "Credentials."
   - Click "Create credentials" and choose "OAuth client ID."
   - Application type: Choose "Desktop app"
   - Name: Give it a name (e.g., "Calendar Script").
   - Click "Create."
   - Download the JSON file containing your credentials (it will have a name like client_secret_xxxx.json). Rename it to credentials.json and place it in the same directory as your script.

## Installation 

- Git clone this repo: `git clone https://github.com/caerry/markdown-notes-reminder-gcalendar`
- May sure you use python 3.9+, create venv and pip install:
- `python3 -m venv venv`
- `source venv/bin/activate`
- `pip install -r requirements.txt`

## Configuration 
- Edit parameters in ./google-remind-sync.sh

## Setupping cronjob for the script 

- `crontab -e`
- `0 * * * * /path/to/your/google-remind-sync.sh >> /path/to/your/cron.log 2>&1`


For example, getting my crontab -l:

```
0 * * * * /home/astrocat/Downloads/sync-notes-reminders-gcalendar.sh >> /home/astrocat/Downloads/calendar_event_creator.log 2>&1
```

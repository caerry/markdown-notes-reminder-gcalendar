
## Abstract 

This script for syncing your reminders in markdown files (i.e in obsidian reminder plugin) with your google calendar. 
The remind file format:
```
(@[[20240101]] 00:00) Text for event 
```
This is going to google calendar at 2024.01.01 00:00 with the event text "Text for event"

![obsidian-editor-example.jpeg](300)
![gcalendar-example.jpeg](300)

## Obtaining credentials for google calendar 

## Installation 

- Git clone this repo: `git clone ...`
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

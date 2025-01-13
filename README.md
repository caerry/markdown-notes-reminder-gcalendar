

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

## Abstract 

This script for syncing your reminders in markdown files (i.e in obsidian reminder plugin) with your google calendar. 
The remind file format:
```
(@[[20240101]] 00:00) Text for event 
```
This is going to google calendar at 2024.01.01 00:00 with the event text "Text for event"

![https://github.com/caerry/markdown-notes-reminder-gcalendar/blob/main/obsidian-editor-example.jpeg?raw=true](300)
![https://github.com/caerry/markdown-notes-reminder-gcalendar/blob/main/gcalendar-example.jpeg?raw=true](300)


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

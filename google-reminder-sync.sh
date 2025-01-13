#!/bin/bash

# --- Configuration ---
# Path to your project directory
PROJECT_DIR="/home/astrocat/Downloads/sync-notes-reminders-gcalendar"

# Name of your virtual environment
VENV_NAME="venv"  

# Path to the Python script
SCRIPT_PATH="${PROJECT_DIR}/calendar-event-creator.py"

# Path to the credentials.json file
CREDENTIALS_PATH="${PROJECT_DIR}/credentials.json"

# Token from google auth
TOKEN_PATH="${PROJECT_DIR}/token.json" 

# Directory to scan for markdown files
DIRECTORY_TO_SCAN="/home/astrocat/repo/exocortex/journal"

# Timezone
TIMEZONE="Europe/Moscow" 

# --- Script ---

# Activate the virtual environment
source "${PROJECT_DIR}/${VENV_NAME}/bin/activate"

# Run the Python script with arguments
python "$SCRIPT_PATH" -d "$DIRECTORY_TO_SCAN" -c "$CREDENTIALS_PATH" -tz "$TIMEZONE" -t "$TOKEN_PATH"

# Deactivate the virtual environment (optional)
deactivate

echo "Calendar event creation script executed at $(date)"

"""
Google Sheets integration for personal notes.
Stores user notes linked to GATE topics.
"""

import gspread
from oauth2client.service_account import ServiceAccountCredentials
import logging
import os
from datetime import datetime
from dotenv import load_dotenv

load_dotenv(override=True)

logger = logging.getLogger(__name__)

# Configuration
GOOGLE_SHEETS_JSON = os.getenv("GOOGLE_SHEETS_JSON", "service_account.json")
GOOGLE_SHEET_NAME = os.getenv("GOOGLE_SHEET_NAME", "AntigravityNotes")

# Valid topics
VALID_TOPICS = ["SM", "FM", "SA", "RCC", "STEEL", "GEO", "ENV", "TRANS", "HYDRO", "CONST"]


def get_client():
    """Authenticate with Google Sheets."""
    try:
        if not os.path.exists(GOOGLE_SHEETS_JSON):
            logger.warning(f"Google Sheets JSON not found: {GOOGLE_SHEETS_JSON}")
            return None
        
        scope = [
            'https://spreadsheets.google.com/feeds',
            'https://www.googleapis.com/auth/drive'
        ]
        creds = ServiceAccountCredentials.from_json_keyfile_name(GOOGLE_SHEETS_JSON, scope)
        client = gspread.authorize(creds)
        return client
    except Exception as e:
        logger.error(f"Google Sheets Auth Error: {e}")
        return None


def _get_or_create_sheet(client):
    """Get the Notes worksheet, create if doesn't exist."""
    try:
        spreadsheet = client.open(GOOGLE_SHEET_NAME)
        try:
            sheet = spreadsheet.worksheet("Notes")
        except gspread.WorksheetNotFound:
            sheet = spreadsheet.add_worksheet(title="Notes", rows="1000", cols="10")
            # Add header
            sheet.append_row(["Timestamp", "UserID", "Username", "Topic", "Note"])
        return sheet
    except Exception as e:
        logger.error(f"Failed to get/create sheet: {e}")
        return None


def add_note(user_id: int, username: str, topic: str, note: str) -> bool:
    """
    Add a note linked to a topic.
    
    Args:
        user_id: Telegram user ID
        username: Telegram username
        topic: Topic code (SM, FM, etc.)
        note: The note content
    
    Returns:
        True if successful, False otherwise
    """
    client = get_client()
    if not client:
        return False
    
    try:
        sheet = _get_or_create_sheet(client)
        if not sheet:
            return False
        
        topic = topic.upper()
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        sheet.append_row([timestamp, str(user_id), username, topic, note])
        logger.info(f"Note added: {username} - {topic}")
        return True
    except Exception as e:
        logger.error(f"Failed to add note: {e}")
        return False


def get_notes(user_id: int, topic: str = None) -> list:
    """
    Get notes for a user, optionally filtered by topic.
    
    Args:
        user_id: Telegram user ID
        topic: Optional topic filter
    
    Returns:
        List of note dicts with 'topic' and 'note' keys
    """
    client = get_client()
    if not client:
        return []
    
    try:
        sheet = _get_or_create_sheet(client)
        if not sheet:
            return []
        
        records = sheet.get_all_records()
        user_notes = []
        
        for record in records:
            # Match user ID
            if str(record.get('UserID', '')) == str(user_id):
                # Filter by topic if specified
                if topic:
                    if record.get('Topic', '').upper() == topic.upper():
                        user_notes.append({
                            'topic': record.get('Topic', ''),
                            'note': record.get('Note', ''),
                            'timestamp': record.get('Timestamp', '')
                        })
                else:
                    user_notes.append({
                        'topic': record.get('Topic', ''),
                        'note': record.get('Note', ''),
                        'timestamp': record.get('Timestamp', '')
                    })
        
        return user_notes
    except Exception as e:
        logger.error(f"Failed to get notes: {e}")
        return []


def get_random_note_for_topic(topic: str) -> dict:
    """
    Get a random note for a topic (for scheduled reminders).
    
    Args:
        topic: Topic code
    
    Returns:
        Dict with 'username', 'note' or empty dict
    """
    import random
    
    client = get_client()
    if not client:
        return {}
    
    try:
        sheet = _get_or_create_sheet(client)
        if not sheet:
            return {}
        
        records = sheet.get_all_records()
        topic_notes = [r for r in records if r.get('Topic', '').upper() == topic.upper()]
        
        if topic_notes:
            note = random.choice(topic_notes)
            return {
                'username': note.get('Username', 'Anonymous'),
                'note': note.get('Note', '')
            }
        return {}
    except Exception as e:
        logger.error(f"Failed to get random note: {e}")
        return {}


def is_valid_topic(topic: str) -> bool:
    """Check if a topic code is valid."""
    return topic.upper() in VALID_TOPICS


def get_topic_full_name(code: str) -> str:
    """Get full topic name from code."""
    names = {
        "SM": "Soil Mechanics",
        "FM": "Fluid Mechanics",
        "SA": "Structural Analysis",
        "RCC": "Reinforced Concrete Design",
        "STEEL": "Steel Structures",
        "GEO": "Geomatics / Surveying",
        "ENV": "Environmental Engineering",
        "TRANS": "Transportation Engineering",
        "HYDRO": "Hydrology & Irrigation",
        "CONST": "Construction Management"
    }
    return names.get(code.upper(), code)

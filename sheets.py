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


# --- User Stats Persistence ---

def _get_stats_sheet(client):
    """Get the UserStats worksheet, create if doesn't exist."""
    try:
        spreadsheet = client.open(GOOGLE_SHEET_NAME)
        try:
            sheet = spreadsheet.worksheet("UserStats")
        except gspread.WorksheetNotFound:
            sheet = spreadsheet.add_worksheet(title="UserStats", rows="1000", cols="10")
            sheet.append_row(["UserID", "Correct", "Incorrect", "Total", "Streak", "LastAnswerDate", "WeeklyCorrect", "WeeklyTotal"])
        return sheet
    except Exception as e:
        logger.error(f"Failed to get/create UserStats sheet: {e}")
        return None


def save_user_stats(user_id: int, stats: dict) -> bool:
    """Save user stats to Google Sheets."""
    client = get_client()
    if not client:
        return False
    
    try:
        sheet = _get_stats_sheet(client)
        if not sheet:
            return False
        
        # Find existing row for user
        try:
            cell = sheet.find(str(user_id))
            row = cell.row
            # Update existing row
            sheet.update(f"A{row}:H{row}", [[
                str(user_id),
                stats.get("correct", 0),
                stats.get("incorrect", 0),
                stats.get("total", 0),
                stats.get("streak", 0),
                stats.get("last_answer_date", ""),
                stats.get("weekly_correct", 0),
                stats.get("weekly_total", 0)
            ]])
        except gspread.exceptions.CellNotFound:
            # Add new row
            sheet.append_row([
                str(user_id),
                stats.get("correct", 0),
                stats.get("incorrect", 0),
                stats.get("total", 0),
                stats.get("streak", 0),
                stats.get("last_answer_date", ""),
                stats.get("weekly_correct", 0),
                stats.get("weekly_total", 0)
            ])
        
        return True
    except Exception as e:
        logger.error(f"Failed to save user stats: {e}")
        return False


def load_user_stats(user_id: int) -> dict:
    """Load user stats from Google Sheets."""
    client = get_client()
    if not client:
        return {}
    
    try:
        sheet = _get_stats_sheet(client)
        if not sheet:
            return {}
        
        try:
            cell = sheet.find(str(user_id))
            row = sheet.row_values(cell.row)
            return {
                "correct": int(row[1]) if len(row) > 1 and row[1] else 0,
                "incorrect": int(row[2]) if len(row) > 2 and row[2] else 0,
                "total": int(row[3]) if len(row) > 3 and row[3] else 0,
                "streak": int(row[4]) if len(row) > 4 and row[4] else 0,
                "last_answer_date": row[5] if len(row) > 5 else None,
                "weekly_correct": int(row[6]) if len(row) > 6 and row[6] else 0,
                "weekly_total": int(row[7]) if len(row) > 7 and row[7] else 0
            }
        except gspread.exceptions.CellNotFound:
            return {}
    except Exception as e:
        logger.error(f"Failed to load user stats: {e}")
        return {}


# --- Leaderboard Persistence ---

def _get_leaderboard_sheet(client):
    """Get the Leaderboard worksheet, create if doesn't exist."""
    try:
        spreadsheet = client.open(GOOGLE_SHEET_NAME)
        try:
            sheet = spreadsheet.worksheet("Leaderboard")
        except gspread.WorksheetNotFound:
            sheet = spreadsheet.add_worksheet(title="Leaderboard", rows="500", cols="6")
            sheet.append_row(["UserID", "Username", "Correct", "Total", "Score"])
        return sheet
    except Exception as e:
        logger.error(f"Failed to get/create Leaderboard sheet: {e}")
        return None


def save_leaderboard_entry(user_id: int, username: str, correct: int, total: int, score: int) -> bool:
    """Save leaderboard entry to Google Sheets."""
    client = get_client()
    if not client:
        return False
    
    try:
        sheet = _get_leaderboard_sheet(client)
        if not sheet:
            return False
        
        try:
            cell = sheet.find(str(user_id))
            row = cell.row
            sheet.update(f"A{row}:E{row}", [[str(user_id), username, correct, total, score]])
        except gspread.exceptions.CellNotFound:
            sheet.append_row([str(user_id), username, correct, total, score])
        
        return True
    except Exception as e:
        logger.error(f"Failed to save leaderboard: {e}")
        return False


def load_leaderboard() -> dict:
    """Load full leaderboard from Google Sheets."""
    client = get_client()
    if not client:
        return {}
    
    try:
        sheet = _get_leaderboard_sheet(client)
        if not sheet:
            return {}
        
        records = sheet.get_all_records()
        leaderboard = {}
        for r in records:
            if r.get("UserID"):
                leaderboard[int(r["UserID"])] = {
                    "name": r.get("Username", "Anonymous"),
                    "correct": int(r.get("Correct", 0)),
                    "total": int(r.get("Total", 0)),
                    "score": int(r.get("Score", 0))
                }
        return leaderboard
    except Exception as e:
        logger.error(f"Failed to load leaderboard: {e}")
        return {}

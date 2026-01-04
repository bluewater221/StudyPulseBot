import gspread
from oauth2client.service_account import ServiceAccountCredentials
import os
import json
from dotenv import load_dotenv

def inspect_study_sheet():
    load_dotenv(r"c:\Users\rajrc\Projects\GitHub\antigravity_bot\.env")
    creds_file = r"c:\Users\rajrc\Projects\GitHub\antigravity_bot\service_account.json"
    sheet_name = os.getenv("GOOGLE_SHEET_NAME", "AntigravityNotes")
    
    if not os.path.exists(creds_file):
        print(f"❌ Credentials file not found: {creds_file}")
        return

    try:
        scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
        creds = ServiceAccountCredentials.from_json_keyfile_name(creds_file, scope)
        client = gspread.authorize(creds)
        
        print(f"🔍 Attempting to open '{sheet_name}'...")
        sh = client.open(sheet_name)
        print(f"✅ Successfully opened: '{sh.title}'")
        
        worksheets = sh.worksheets()
        print(f"📋 Worksheets found: {len(worksheets)}")
        
        for ws in worksheets:
            rows = ws.get_all_values()
            print(f" - '{ws.title}': {len(rows)} rows")
            if len(rows) > 0:
                print(f"   Header/First row: {rows[0]}")
            if len(rows) > 1:
                print(f"   Last data row: {rows[-1]}")
            
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    inspect_study_sheet()

from google.oauth2.service_account import Credentials
import gspread
from config import load_config

CONFIG = load_config()
PILOT_HEADERS = ['pilot_id', 'name', 'skills', 'certifications', 'location', 'status', 'current_assignment', 'available_from']

# Setup Google Sheets
scope = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]
creds = Credentials.from_service_account_file(CONFIG['credentials_file'], scopes=scope)
gsheet_client = gspread.authorize(creds)

def get_pilots():
    try:
        sheet = gsheet_client.open_by_key(CONFIG['pilot_sheet_id']).sheet1
        return sheet.get_all_records(), sheet
    except:
        return [], None

def update_pilot_status(pilot_name, new_status, sheet=None):
    pilots, sheet = get_pilots() if not sheet else ([], sheet)
    if not sheet:
        return False, "Cannot connect to sheet"
    try:
        for i, p in enumerate(pilots, start=2):
            if p['name'].lower() == pilot_name.lower():
                sheet.update_cell(i, 6, new_status)
                return True, f"Updated {pilot_name} to {new_status}"
        return False, f"Pilot {pilot_name} not found"
    except Exception as e:
        return False, str(e)

def is_available_today(pilot):
    from dateutil import parser
    from datetime import date
    status = str(pilot.get('status', '')).strip()
    if status not in ['Available', 'Standby']:
        return False
    avail_date_str = str(pilot.get('available_from', '')).strip()
    if not avail_date_str or avail_date_str in ['–', '-', 'None', '', 'Immediate']:
        return True
    try:
        avail_date = parser.parse(avail_date_str).date()
        return avail_date <= date.today()
    except:
        return True

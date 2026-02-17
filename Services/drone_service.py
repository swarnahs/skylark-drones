from google.oauth2.service_account import Credentials
import gspread
from config import load_config

CONFIG = load_config()
DRONE_HEADERS = ['drone_id', 'model', 'capabilities', 'status', 'location', 'current_assignment', 'maintenance_due']

# Setup Google Sheets
scope = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]
creds = Credentials.from_service_account_file(CONFIG['credentials_file'], scopes=scope)
gsheet_client = gspread.authorize(creds)

def get_drones():
    try:
        sheet = gsheet_client.open_by_key(CONFIG['drone_sheet_id']).sheet1
        return sheet.get_all_records(), sheet
    except:
        return [], None

def update_drone_status(drone_id, new_status, sheet=None):
    drones, sheet = get_drones() if not sheet else ([], sheet)
    if not sheet:
        return False, "Cannot connect to sheet"
    try:
        for i, d in enumerate(drones, start=2):
            if str(d.get('drone_id', '')).upper() == drone_id.upper():
                sheet.update_cell(i, 4, new_status)
                return True, f"Updated {drone_id} to {new_status}"
        return False, f"Drone {drone_id} not found"
    except Exception as e:
        return False, str(e)

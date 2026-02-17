import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd

# ------------------- Google Sheets Connection -------------------
def connect_sheets():
    scope = [
        "https://spreadsheets.google.com/feeds",
        "https://www.googleapis.com/auth/drive"
    ]
    creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)
    client = gspread.authorize(creds)
    return client

# ------------------- Read Sheet -------------------
def read_sheet(sheet_name):
    client = connect_sheets()
    sheet = client.open(sheet_name).sheet1
    data = sheet.get_all_records()
    return pd.DataFrame(data)

# ------------------- Update Pilot Status -------------------
def update_pilot_status(sheet_name, pilot_name, new_status):
    client = connect_sheets()
    sheet = client.open(sheet_name).sheet1
    records = sheet.get_all_records()

    for i, row in enumerate(records, start=2):  # gspread is 1-indexed, headers on row 1
        if str(row.get('name', '')).strip().lower() == pilot_name.lower():
            sheet.update_cell(i, 6, new_status)  # Assuming status is column 6
            return True
    return False

# ------------------- Update Drone Status -------------------
def update_drone_status(sheet_name, drone_id, new_status):
    client = connect_sheets()
    sheet = client.open(sheet_name).sheet1
    records = sheet.get_all_records()

    for i, row in enumerate(records, start=2):
        if str(row.get('drone_id', '')).strip().upper() == drone_id.upper():
            sheet.update_cell(i, 4, new_status)  # Assuming status is column 4
            return True
    return False

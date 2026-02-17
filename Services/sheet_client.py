import gspread
from oauth2client.service_account import ServiceAccountCredentials

SCOPE = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
CREDS_FILE = "service_account.json"  # your service account JSON

creds = ServiceAccountCredentials.from_json_keyfile_name(CREDS_FILE, SCOPE)
client = gspread.authorize(creds)

# Correct sheet IDs
PILOT_SHEET_ID = "10jtVgImDYkaxvEkFH1t_cPeISDk1wNCL-xlxIf0vTyU"
DRONE_SHEET_ID = "1jT8eWxcCj0-44Yri31gloBEA4Y_zC198gpdTBebZacI"
MISSION_SHEET_ID = "1Dcv0_jo4TV9Uvpwplqen79Qw6lGPS2PzSkxqOM6Ies0"

def connect_sheet(sheet_id):
    return client.open_by_key(sheet_id).sheet1

pilot_sheet = connect_sheet(PILOT_SHEET_ID)
drone_sheet = connect_sheet(DRONE_SHEET_ID)
mission_sheet = connect_sheet(MISSION_SHEET_ID)


print(pilot_sheet.get_all_records())
print(drone_sheet.get_all_records())
print(mission_sheet.get_all_records())

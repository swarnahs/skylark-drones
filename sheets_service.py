import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd

def connect_sheets():
    scope = [
        "https://spreadsheets.google.com/feeds",
        "https://www.googleapis.com/auth/drive"
    ]

    creds = ServiceAccountCredentials.from_json_keyfile_name(
        "credentials.json", scope)

    client = gspread.authorize(creds)
    return client


def read_sheet(sheet_name):
    client = connect_sheets()
    sheet = client.open(sheet_name).sheet1
    data = sheet.get_all_records()
    return pd.DataFrame(data)

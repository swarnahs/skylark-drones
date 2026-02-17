import os
import json

def load_config():
    """Load configuration from environment or config.json"""
    config = {
        'pilot_sheet_id': os.getenv('PILOT_SHEET_ID', '10jtVgImDYkaxvEkFH1t_cPeISDk1wNCL-xlxIf0vTyU'),
        'drone_sheet_id': os.getenv('DRONE_SHEET_ID', '1VlqJCLuPXYlC8aKzyMQmw2sTwa-AcLJod07E0-g49oY'),
        'credentials_file': os.getenv('CREDENTIALS_FILE', 'credentials.json'),
        'gemini_api_key': os.getenv('GEMINI_API_KEY', 'GEMINI_SECRET_KEY')
    }
    
    try:
        with open('config.json', 'r') as f:
            file_config = json.load(f)
            config.update({k: v for k, v in file_config.items() if v})
    except:
        pass
    
    return config

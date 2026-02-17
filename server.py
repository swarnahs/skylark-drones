from flask import Flask, request, jsonify
from flask_cors import CORS
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd
import requests
from datetime import datetime

app = Flask(__name__)
CORS(app)

# ==============================
# CONFIG
# ==============================
GOOGLE_SHEET_NAME = "DroneOperations"   # Change to your sheet name
SERVICE_ACCOUNT_FILE = "Credentials.json"

OLLAMA_URL = "http://localhost:11434/api/generate"
OLLAMA_MODEL = "mistral"

# ==============================
# GOOGLE SHEETS CONNECTION
# ==============================
scope = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/drive"
]

creds = ServiceAccountCredentials.from_json_keyfile_name(
    SERVICE_ACCOUNT_FILE, scope
)
client = gspread.authorize(creds)
spreadsheet = client.open(GOOGLE_SHEET_NAME)


# ==============================
# LOAD DATA FUNCTIONS
# ==============================
def load_sheet(sheet_name):
    sheet = spreadsheet.worksheet(sheet_name)
    data = sheet.get_all_records()
    return pd.DataFrame(data)


def load_all_data():
    pilots = load_sheet("Pilots")
    drones = load_sheet("Drones")
    missions = load_sheet("Missions")
    return pilots, drones, missions


# ==============================
# FILTER HELPERS
# ==============================
today = datetime.today().strftime("%Y-%m-%d")

def available_pilots(df):
    return df[
        (df["status"] == "Available") &
        (df["available_from"] <= today)
    ]

def available_drones(df):
    return df[df["status"] == "Available"]


# ==============================
# OLLAMA CALL
# ==============================
def ask_ollama(prompt):
    payload = {
        "model": OLLAMA_MODEL,
        "prompt": prompt,
        "stream": False
    }
    response = requests.post(OLLAMA_URL, json=payload)
    return response.json()["response"]


# ==============================
# INTENT ROUTER
# ==============================
@app.route("/chat", methods=["POST"])
def chat():
    user_message = request.json.get("message", "").lower()

    pilots, drones, missions = load_all_data()

    # ==========================
    # GREETING
    # ==========================
    if user_message in ["hi", "hello", "hey"]:
        return jsonify({
            "answer": "Hello! I am your Drone Operations Assistant. Ask me about pilots, drones, or missions."
        })

    # ==========================
    # PILOT LIST
    # ==========================
    if "available pilots" in user_message:
        ap = available_pilots(pilots)
        return jsonify({"data": ap.to_dict(orient="records")})

    if "all pilots" in user_message or "pilot list" in user_message:
        return jsonify({"data": pilots.to_dict(orient="records")})

    # ==========================
    # DRONE LIST
    # ==========================
    if "available drones" in user_message:
        ad = available_drones(drones)
        return jsonify({"data": ad.to_dict(orient="records")})

    if "all drones" in user_message or "drone list" in user_message:
        return jsonify({"data": drones.to_dict(orient="records")})

    # ==========================
    # MISSIONS
    # ==========================
    if "mission" in user_message or "project" in user_message:
        return jsonify({"data": missions.to_dict(orient="records")})

    # ==========================
    # SPECIFIC PILOT INFO
    # ==========================
    for _, p in pilots.iterrows():
        name = p["name"].lower()
        if name in user_message:

            if "certification" in user_message:
                return jsonify({
                    "answer": f"{p['name']} certifications: {p['certifications']}"
                })

            if "skill" in user_message:
                return jsonify({
                    "answer": f"{p['name']} skills: {p['skills']}"
                })

            if "location" in user_message:
                return jsonify({
                    "answer": f"{p['name']} is located in {p['location']}"
                })

            if "rate" in user_message or "cost" in user_message:
                return jsonify({
                    "answer": f"{p['name']} daily rate: ₹{p['daily_rate_inr']}"
                })

    # ==========================
    # SPECIFIC DRONE INFO
    # ==========================
    for _, d in drones.iterrows():
        drone_id = d["drone_id"].lower()
        if drone_id.lower() in user_message:

            if "status" in user_message:
                return jsonify({
                    "answer": f"{d['drone_id']} status: {d['status']}"
                })

            if "capability" in user_message:
                return jsonify({
                    "answer": f"{d['drone_id']} capabilities: {d['capabilities']}"
                })

            if "location" in user_message:
                return jsonify({
                    "answer": f"{d['drone_id']} location: {d['location']}"
                })

    # ==========================
    # LLM FALLBACK (SMART CONTEXT)
    # ==========================
    context = f"""
You are a Drone Operations AI Assistant.

Available Pilots:
{available_pilots(pilots)[['name','location','skills','certifications']].to_string(index=False)}

Available Drones:
{available_drones(drones)[['drone_id','location','capabilities']].to_string(index=False)}

Active Missions:
{missions[['project_id','location','required_skills','priority']].to_string(index=False)}

User Question:
{user_message}

Provide a short operational recommendation.
"""

    llm_response = ask_ollama(context)

    return jsonify({"answer": llm_response})


# ==============================
# RUN
# ==============================
if __name__ == "__main__":
    app.run(port=5000, debug=True)

import streamlit as st
import pandas as pd
from sheets_service import read_sheet, update_pilot_status

# Optional AI Layer
try:
    from openai import OpenAI
    client = OpenAI(api_key=st.secrets.get("OPENAI_API_KEY", ""))
except:
    client = None

st.set_page_config(page_title="Skylark Drone Coordinator", layout="wide")

st.title("🚁 Skylark Drone Operations Coordinator AI")

# ==============================
# LOAD DATA
# ==============================

@st.cache_data
def load_data():
    pilots = read_sheet("pilot_roster")
    drones = read_sheet("drone_fleet")
    missions = read_sheet("missions")
    return pilots, drones, missions

pilots_df, drones_df, missions_df = load_data()

# ==============================
# 1️⃣ PILOT FILTERING
# ==============================

st.header("🔍 Pilot Roster Management")

col1, col2, col3 = st.columns(3)

with col1:
    skill_filter = st.text_input("Filter by Skill")

with col2:
    status_filter = st.selectbox("Filter by Status", 
        ["All", "Available", "On Leave", "Unavailable"])

with col3:
    location_filter = st.text_input("Filter by Location")

filtered_pilots = pilots_df.copy()

if skill_filter:
    filtered_pilots = filtered_pilots[
        filtered_pilots["skills"].str.contains(skill_filter, case=False, na=False)
    ]

if status_filter != "All":
    filtered_pilots = filtered_pilots[
        filtered_pilots["status"] == status_filter
    ]

if location_filter:
    filtered_pilots = filtered_pilots[
        filtered_pilots["current location"].str.contains(location_filter, case=False, na=False)
    ]

st.dataframe(filtered_pilots, use_container_width=True)

# ==============================
# 2️⃣ UPDATE PILOT STATUS (2-WAY SYNC)
# ==============================

st.subheader("✏️ Update Pilot Status")

pilot_names = pilots_df["name"].tolist()

selected_pilot = st.selectbox("Select Pilot", pilot_names)
new_status = st.selectbox("New Status", ["Available", "On Leave", "Unavailable"])

if st.button("Update Status"):
    update_pilot_status("pilot_roster", selected_pilot, new_status)
    st.success("✅ Pilot status updated in Google Sheet!")
    st.cache_data.clear()

# ==============================
# 3️⃣ ASSIGNMENT MATCHING
# ==============================

st.header("🛰 Mission Assignment")

mission_ids = missions_df["project id"].tolist()
selected_mission = st.selectbox("Select Mission", mission_ids)

if st.button("Find Suitable Pilots"):

    mission = missions_df[missions_df["project id"] == selected_mission].iloc[0]

    required_skill = mission["required skills"]
    mission_location = mission["locations"]
    mission_budget = mission["budget"]

    suitable = pilots_df[
        (pilots_df["skills"].str.contains(required_skill, case=False, na=False)) &
        (pilots_df["status"] == "Available")
    ]

    if suitable.empty:
        st.warning("⚠ No suitable pilots found.")
    else:
        st.success("Matching Pilots:")
        st.dataframe(suitable)

        # Conflict detection
        st.subheader("⚠ Conflict Detection")

        for index, pilot in suitable.iterrows():
            conflicts = []

            if pilot["current location"] != mission_location:
                conflicts.append("Location mismatch")

            estimated_cost = pilot["daily rate"] * mission["duration"]

            if estimated_cost > mission_budget:
                conflicts.append("Budget Overrun")

            if conflicts:
                st.write(f"Pilot: {pilot['name']} → ❌ {conflicts}")
            else:
                st.write(f"Pilot: {pilot['name']} → ✅ No conflicts")

# ==============================
# 4️⃣ DRONE WEATHER CHECK
# ==============================

st.header("🚁 Drone Matching")

weather = missions_df[
    missions_df["project id"] == selected_mission
].iloc[0]["weather"]

available_drones = drones_df[drones_df["status"] == "Available"]

compatible_drones = []

for index, drone in available_drones.iterrows():

    if weather == "Rainy":
        if "IP43" in drone["capabilities"]:
            compatible_drones.append(drone)
    else:
        compatible_drones.append(drone)

if compatible_drones:
    st.dataframe(pd.DataFrame(compatible_drones))
else:
    st.warning("⚠ No weather-compatible drones available.")

# ==============================
# 5️⃣ CONVERSATIONAL AI LAYER
# ==============================

st.header("💬 Ask Drone Coordinator AI")

user_query = st.chat_input("Ask about pilots, missions, drones...")

if user_query:

    if client:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a drone operations coordinator assistant."},
                {"role": "user", "content": user_query}
            ]
        )
        st.write(response.choices[0].message.content)
    else:
        st.warning("AI layer not configured (OpenAI key missing).")

import streamlit as st
import requests
import pandas as pd

# ---------------------
# CONFIGURATION
# ---------------------
API_URL = "http://localhost:5000/api"  # Flask backend URL

st.set_page_config(page_title="Drone Operations", layout="wide")
st.title("Skylark Drone Operations Dashboard 🚁")

# ---------------------
# FETCH DATA
# ---------------------
@st.cache_data(ttl=30)
def get_pilots():
    r = requests.get(f"{API_URL}/tables")
    if r.status_code == 200:
        return r.json().get('pilots_html', '')
    return ""

@st.cache_data(ttl=30)
def get_drones():
    r = requests.get(f"{API_URL}/tables")
    if r.status_code == 200:
        return r.json().get('drones_html', '')
    return ""

# ---------------------
# DISPLAY TABLES
# ---------------------
st.subheader("Pilots")
pilots_html = get_pilots()
st.markdown(pilots_html, unsafe_allow_html=True)

st.subheader("Drones")
drones_html = get_drones()
st.markdown(drones_html, unsafe_allow_html=True)

# ---------------------
# CHAT / COMMAND SECTION
# ---------------------
st.subheader("Command Center")

user_input = st.text_input("Enter command / query:")

if st.button("Send"):
    if user_input:
        try:
            payload = {"message": user_input}
            r = requests.post(f"{API_URL}/chat", json=payload)
            if r.status_code == 200:
                resp = r.json()
                st.markdown(f"**Response:** {resp.get('content', 'No response')}")
            else:
                st.error("Backend error. Try again.")
        except Exception as e:
            st.error(f"Error: {e}")

import streamlit as st
from sheets_service import read_sheet

st.title("🚁 Skylark Drone Coordinator")

if st.button("Load Pilot Roster"):
    df = read_sheet("pilot_roster")
    st.dataframe(df)

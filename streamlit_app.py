import streamlit as st
import requests

st.title("Drone Operations AI")

user_input = st.text_input("Enter your request")

if st.button("Send"):
    res = requests.post(
        "http://localhost:5000/chat",
        json={"message": user_input}
    )
    st.write(res.json()["response"])

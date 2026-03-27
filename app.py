import streamlit as st
from modules.auth import show_auth_page, logout

st.set_page_config(
    page_title="VidLoop AI",
    page_icon="🎬",
    layout="centered"
)

# ── Session guard ──────────────────────────────────────────────
# If no user in session → show auth page
# If user exists → show main app (we'll build this tomorrow)

if "user" not in st.session_state:
    show_auth_page()
    st.stop()  # Don't render anything below this line

# ── Logged-in area ─────────────────────────────────────────────
st.sidebar.write(f"{st.session_state['user'].email}")
if st.sidebar.button("Logout"):
    logout()

# Temporary placeholder — we'll replace this on Day 3
st.title("VidLoop AI")
st.success("You're logged in! Onboarding comes tomorrow.")
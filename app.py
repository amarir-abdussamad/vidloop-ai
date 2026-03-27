import streamlit as st
from modules.auth import show_auth_page, logout
from modules.onboarding import has_completed_onboarding, show_onboarding_page

st.set_page_config(
    page_title="VidLoop AI",
    page_icon="🎬",
    layout="centered"
)

# ── Step 1: Auth guard ─────────────────────────────────────────
if "user" not in st.session_state:
    show_auth_page()
    st.stop()

# ── Step 2: Onboarding guard ───────────────────────────────────
user_id = st.session_state["user"].id

# Check session state first (faster), then Supabase (on fresh load)
if not st.session_state.get("onboarding_complete"):
    if not has_completed_onboarding(user_id):
        show_onboarding_page()
        st.stop()
    else:
        st.session_state["onboarding_complete"] = True

# ── Step 3: Main app ───────────────────────────────────────────
st.sidebar.write(f"{st.session_state['user'].email}")
if st.sidebar.button("Logout"):
    logout()

# Temporary placeholder — we'll replace this on Day 4
st.title("VidLoop AI")
st.success("Onboarding complete! YouTube URL input comes tomorrow.")
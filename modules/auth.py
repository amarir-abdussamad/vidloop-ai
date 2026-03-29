import streamlit as st
from utils.supabase_client import get_supabase_client

supabase = get_supabase_client()


def show_auth_page():
    """Render the full login/signup UI. Called from app.py when no session exists."""

    st.title("🎬 VidLoop AI")
    st.subheader("Your AI-powered YouTube co-pilot")
    st.divider()

    tab_login, tab_signup = st.tabs(["Login", "Sign Up"])

    with tab_login:
        _render_login()

    with tab_signup:
        _render_signup()

def _render_login():
    st.subheader("Welcome back")

    with st.form("login_form"):
        email = st.text_input("Email", key="login_email")
        password = st.text_input("Password", type="password", key="login_password")
        submitted = st.form_submit_button("Login", use_container_width=True)

    if submitted:
        if not email or not password:
            st.warning("Please fill in both fields.")
            return
        try:
            response = supabase.auth.sign_in_with_password({
                "email": email,
                "password": password
            })
            st.session_state["user"] = response.user
            st.session_state["session"] = response.session
            st.rerun()
        except Exception as e:
            st.error(f"Login failed: {e}")

def _render_signup():
    st.subheader("Create your free account")

    with st.form("signup_form"):
        email = st.text_input("Email", key="signup_email")
        password = st.text_input("Password (min 6 chars)", type="password", key="signup_password")
        submitted = st.form_submit_button("Create Account", use_container_width=True)

    if submitted:
        if not email or not password:
            st.warning("Please fill in both fields.")
            return
        if len(password) < 6:
            st.warning("Password must be at least 6 characters.")
            return
        try:
            supabase.auth.sign_up({
                "email": email,
                "password": password
            })
            st.success("Account created! Please log in.")
        except Exception as e:
            st.error(f"Signup failed: {e}")

def logout():
    """Call this from anywhere to log the user out."""
    supabase.auth.sign_out()
    st.session_state.clear()
    st.rerun()

def restore_session():
    """
    Called on every app load. Tries to restore the Supabase session
    so the user doesn't have to log in again after a refresh.
    """
    if "user" in st.session_state:
        return  # Already have a session, nothing to do

    try:
        response = supabase.auth.get_session()
        if response and response.session and response.session.user:
            st.session_state["user"] = response.session.user
            st.session_state["session"] = response.session
    except Exception:
        pass  # No session found — user will see login page
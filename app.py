import streamlit as st
from modules.auth import show_auth_page, logout
from modules.onboarding import has_completed_onboarding, show_onboarding_page, get_user_profile
from modules.youtube_fetcher import process_youtube_url

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

if not st.session_state.get("onboarding_complete"):
    if not has_completed_onboarding(user_id):
        show_onboarding_page()
        st.stop()
    else:
        st.session_state["onboarding_complete"] = True

# ── Step 3: Load user profile into session (once) ─────────────
if "user_profile" not in st.session_state:
    st.session_state["user_profile"] = get_user_profile(user_id)

# ── Sidebar ────────────────────────────────────────────────────
st.sidebar.title("VidLoop AI")
st.sidebar.write(f"{st.session_state['user'].email}")
profile = st.session_state["user_profile"]
if profile:
    st.sidebar.write(f"Niche: {profile.get('niche', 'N/A')}")
    st.sidebar.write(f"Subscribers: {profile.get('subscribers', 'N/A'):,}")
if st.sidebar.button("Logout"):
    logout()

# ── Main Page ──────────────────────────────────────────────────
st.title("VidLoop AI")
st.subheader("Paste your YouTube video URL to get started")
st.divider()

url = st.text_input(
    "YouTube Video URL",
    placeholder="https://www.youtube.com/watch?v=...",
)

if st.button("Analyze Video", use_container_width=True):
    if not url:
        st.warning("Please paste a YouTube URL first.")
    else:
        with st.spinner("Fetching video data and transcript..."):
            result = process_youtube_url(url)

        if "error" in result:
            st.error(result["error"])
        else:
            # Save to session state for the next step (AI generation)
            st.session_state["video_data"] = result
            st.success(f"Got it! **{result['title']}**")

            # Debug display — we'll replace this with AI output on Day 6
            with st.expander("Raw data (debug view)"):
                st.write(f"**Channel:** {result['channel_title']}")
                st.write(f"**Views:** {result['view_count']:,}")
                st.write(f"**Likes:** {result['like_count']:,}")
                st.write(f"**Transcript source:** {result['transcript_source']}")
                st.write(f"**Transcript preview:** {result['transcript'][:300]}...")
import streamlit as st
import time
from modules.auth import show_auth_page, logout, restore_session
from modules.onboarding import has_completed_onboarding, show_onboarding_page, get_user_profile
from modules.youtube_fetcher import process_youtube_url
from modules.rate_limiter import check_rate_limit, increment_usage
from modules.ai_generator import generate_content
from modules.results import show_results
from config import APP_ICON, APP_NAME

st.set_page_config(
    page_title=APP_NAME,
    page_icon=APP_ICON,
    layout="centered"
)

restore_session()

# ── Auth guard ─────────────────────────────────────────────────
if "user" not in st.session_state:
    show_auth_page()
    st.stop()

# ── Onboarding guard ───────────────────────────────────────────
user_id = st.session_state["user"].id

if not st.session_state.get("onboarding_complete"):
    if not has_completed_onboarding(user_id):
        show_onboarding_page()
        st.stop()
    else:
        st.session_state["onboarding_complete"] = True

# ── Load user profile ──────────────────────────────────────────
if "user_profile" not in st.session_state:
    st.session_state["user_profile"] = get_user_profile(user_id)

# ── Sidebar ────────────────────────────────────────────────────
st.sidebar.title("VidLoop AI")
st.sidebar.write(f"{st.session_state['user'].email}")
profile = st.session_state["user_profile"]

# FIX: read tier from profile instead of hardcoding "free"
tier = profile.get("tier", "free") if profile else "free"

if profile:
    st.sidebar.write(f"{profile.get('niche', 'N/A')}")
    st.sidebar.write(f"{profile.get('subscribers', 0):,} subscribers")

allowed, used, limit = check_rate_limit(user_id, tier)
st.sidebar.divider()
st.sidebar.write(f"Generations: {used}/{limit} this month")
if not allowed:
    st.sidebar.error("Limit reached — upgrade to Pro!")

if st.sidebar.button("Logout"):
    logout()

# ── Main Page ──────────────────────────────────────────────────
st.title("VidLoop AI")
st.subheader("Paste your YouTube video URL to get started")
st.divider()

with st.form("analyze_form"):
    url = st.text_input(
        "🔗 YouTube Video URL",
        placeholder="https://www.youtube.com/watch?v=...",
    )
    language = st.selectbox(
        "🌍 Output language:",
        ["Auto-detect", "English", "Arabic", "French", "Spanish", "German"]
    )
    submitted = st.form_submit_button("🚀 Analyze Video", use_container_width=True)

if submitted:
    if not url:
        st.warning("Please paste a YouTube URL first.")
        st.stop()

    # ── Rate limit check ───────────────────────────────────────
    allowed, used, limit = check_rate_limit(user_id, tier)
    if not allowed:
        st.error(f"You've used all {limit} free generations this month. Upgrade to Pro for unlimited access!")
        st.stop()

    # ── Cooldown check ─────────────────────────────────────────────
    last_analysis = st.session_state.get("last_analysis_time")
    if last_analysis:
        elapsed = time.time() - last_analysis
        remaining = int(60 - elapsed)
        if remaining > 0:
            st.warning(f"Please wait {remaining} seconds before analyzing another video.")
            st.stop()

    # ── Step 1: Fetch video ────────────────────────────────────
    with st.spinner("Fetching video data and transcript..."):
        video_data = process_youtube_url(url)

    if "error" in video_data:
        st.error(video_data["error"])
        st.stop()

    st.success(f"Got it! **{video_data['title']}**")

    # ── Step 2: Generate AI content ────────────────────────────
    with st.spinner("AI is generating your titles, descriptions, and thumbnail concepts..."):
        ai_result = generate_content(
            user_profile=st.session_state["user_profile"],
            video_data=video_data,
            language=language
        )

    if "error" in ai_result:
        st.error(ai_result["error"])
        st.stop()

    # ── Step 3: Save + track usage ─────────────────────────────
    st.session_state["video_data"] = video_data
    st.session_state["ai_result"] = ai_result
    increment_usage(user_id, tier)
    st.session_state["last_analysis_time"] = time.time()

# FIX: show results outside the `if submitted:` block so they
# survive reruns (e.g. when user clicks a copy button)
if "ai_result" in st.session_state and "video_data" in st.session_state:
    show_results(st.session_state["ai_result"], st.session_state["video_data"])
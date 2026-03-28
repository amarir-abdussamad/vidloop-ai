import streamlit as st
from modules.auth import show_auth_page, logout
from modules.onboarding import has_completed_onboarding, show_onboarding_page, get_user_profile
from modules.youtube_fetcher import process_youtube_url
from modules.rate_limiter import check_rate_limit, increment_usage
from modules.ai_generator import generate_content
from modules.results import show_results

st.set_page_config(
    page_title="VidLoop AI",
    page_icon="🎬",
    layout="centered"
)

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
tier = "free"

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

url = st.text_input(
    "YouTube Video URL",
    placeholder="https://www.youtube.com/watch?v=...",
)

if st.button("Analyze Video", use_container_width=True):
    if not url:
        st.warning("Please paste a YouTube URL first.")
        st.stop()

    # ── Rate limit check ───────────────────────────────────────
    allowed, used, limit = check_rate_limit(user_id, tier)
    if not allowed:
        st.error(f"You've used all {limit} free generations this month. Upgrade to Pro for unlimited access!")
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
            video_data=video_data
        )

    if "error" in ai_result:
        st.error(ai_result["error"])
        st.stop()

    # ── Step 3: Save + track usage ─────────────────────────────
    st.session_state["video_data"] = video_data
    st.session_state["ai_result"] = ai_result
    increment_usage(user_id, tier)

    # ── Step 4: Show results ───────────────────────────────────
    show_results(ai_result, video_data)
import streamlit as st
from modules.auth import show_auth_page, logout
from modules.onboarding import has_completed_onboarding, show_onboarding_page, get_user_profile
from modules.youtube_fetcher import process_youtube_url
from modules.rate_limiter import check_rate_limit, increment_usage
from modules.ai_generator import generate_content

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
tier = "free"  # hardcoded for now — will come from DB in v1.5
if profile:
    st.sidebar.write(f"Niche: {profile.get('niche', 'N/A')}")
    st.sidebar.write(f"Subscribers: {profile.get('subscribers', 'N/A'):,}")

# ── Rate limit display in sidebar ─────────────────────────────
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

    # ── Fetch video data ───────────────────────────────────────
    with st.spinner("Fetching video data and transcript..."):
        result = process_youtube_url(url)

    if "error" in result:
        st.error(result["error"])
        st.stop()

    # ── Save to session + increment usage ──────────────────────
    st.session_state["video_data"] = result
    increment_usage(user_id, tier)

    st.success(f"Got it! **{result['title']}**")

    # ── AI Generation ──────────────────────────────────────────
    with st.spinner("AI is analyzing your video and generating content..."):
        ai_result = generate_content(
            user_profile=st.session_state["user_profile"],
            video_data=result
        )

    if "error" in ai_result:
        st.error(ai_result["error"])
        st.stop()

    # Save AI results to session for results page (Day 7)
    st.session_state["ai_result"] = ai_result

    # ── Temporary debug display ────────────────────────────────
    st.divider()
    st.subheader("AI Output (debug view)")

    st.markdown("**Titles:**")
    for i, title in enumerate(ai_result.get("titles", []), 1):
        st.write(f"{i}. {title}")

    st.markdown("**Descriptions:**")
    for i, desc in enumerate(ai_result.get("descriptions", []), 1):
        with st.expander(f"Description {i}"):
            st.write(desc)

    st.markdown("**Thumbnail Concepts:**")
    for i, concept in enumerate(ai_result.get("thumbnail_concepts", []), 1):
        with st.expander(f"Concept {i}"):
            st.write(concept)
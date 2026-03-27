import streamlit as st
from utils.supabase_client import get_supabase_client

supabase = get_supabase_client()


def has_completed_onboarding(user_id: str) -> bool:
    """Check if a row exists in user_profiles for this user."""
    try:
        response = (
            supabase.table("user_profiles")
            .select("id")
            .eq("id", user_id)
            .execute()
        )
        return len(response.data) > 0
    except Exception as e:
        return False
    

def get_user_profile(user_id: str) -> dict:
    """Fetch the full onboarding profile for a user."""
    try:
        response = (
            supabase.table("user_profiles")
            .select("*")
            .eq("id", user_id)
            .single()
            .execute()
        )
        return response.data
    except Exception:
        return {}
    

def show_onboarding_page():
    """Render the onboarding form. Called from app.py on first login."""

    st.title("Welcome to VidLoop AI!")
    st.subheader("Let's set up your creator profile — takes 60 seconds")
    st.info("These answers help us personalize every title, description, and thumbnail idea we generate for you.")
    st.divider()

    # ── Question 1 ─────────────────────────────────────────────
    subscribers = st.number_input(
        "How many subscribers do you have?",
        min_value=0,
        max_value=100_000_000,
        step=100,
        help="Your current YouTube subscriber count"
    )

    # ── Question 2 ─────────────────────────────────────────────
    niche = st.selectbox(
        "What is your main content niche?",
        options=[
            "Tech Reviews",
            "Gaming",
            "Finance & Business",
            "Education & Tutorials",
            "Vlogs & Lifestyle",
            "Health & Fitness",
            "Food & Cooking",
            "Travel",
            "Comedy & Entertainment",
            "News & Politics",
            "Science",
            "Sports",
            "Music",
            "Other"
        ]
    )

    # ── Question 3 ─────────────────────────────────────────────
    best_video_url = st.text_input(
        "URL of your highest-viewed video ever",
        placeholder="https://www.youtube.com/watch?v=...",
        help="This helps us understand what works for your audience"
    )

    # ── Question 4 ─────────────────────────────────────────────
    worst_video_url = st.text_input(
        "URL of your lowest-viewed video in the last 90 days",
        placeholder="https://www.youtube.com/watch?v=...",
        help="This helps us understand what to avoid"
    )

    # ── Question 5 ─────────────────────────────────────────────
    style_preferences = st.multiselect(
        "What title styles do you prefer? (pick all that apply)",
        options=[
            "Curiosity hooks (e.g. 'Why nobody talks about...')",
            "Number titles (e.g. '7 Ways to...')",
            "How-to titles (e.g. 'How I...')",
            "Controversial/Bold (e.g. 'I was WRONG about...')",
            "Story-driven (e.g. 'I tried X for 30 days...')",
            "Dark humor",
            "Minimalist / Clean",
            "Emotional (e.g. 'This changed my life...')"
        ]
    )

    st.divider()

    if st.button("Save My Profile & Start", use_container_width=True):
        # ── Validation ──────────────────────────────────────────
        if not best_video_url or not worst_video_url:
            st.warning("Please fill in both video URLs.")
            return
        if not best_video_url.startswith("https://www.youtube.com") and \
           not best_video_url.startswith("https://youtu.be"):
            st.warning("Best video URL doesn't look like a YouTube link.")
            return
        if not worst_video_url.startswith("https://www.youtube.com") and \
           not worst_video_url.startswith("https://youtu.be"):
            st.warning("Worst video URL doesn't look like a YouTube link.")
            return

        # ── Save to Supabase ────────────────────────────────────
        user_id = st.session_state["user"].id
        style_str = ", ".join(style_preferences) if style_preferences else "No preference"

        try:
            supabase.table("user_profiles").insert({
                "id": user_id,
                "subscribers": int(subscribers),
                "niche": niche,
                "best_video_url": best_video_url,
                "worst_video_url": worst_video_url,
                "style_preferences": style_str
            }).execute()

            st.session_state["onboarding_complete"] = True
            st.success("Profile saved! Let's go!")
            st.rerun()

        except Exception as e:
            st.error(f"Failed to save profile: {e}")
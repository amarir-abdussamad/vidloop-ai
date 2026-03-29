import streamlit as st


def show_results(ai_result: dict, video_data: dict):
    """Render the full results page with copy buttons everywhere."""

    st.divider()

    # ── Video summary header ───────────────────────────────────
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Views", f"{video_data.get('view_count', 0):,}")
    with col2:
        st.metric("Likes", f"{video_data.get('like_count', 0):,}")
    with col3:
        st.metric("Transcript", video_data.get("transcript_source", "N/A"))

    with st.expander("📜 View full transcript used by AI"):
        st.write(video_data.get("transcript", "No transcript available"))

    st.divider()

    # ── 3 Tabs ─────────────────────────────────────────────────
    tab_titles, tab_descriptions, tab_thumbnails = st.tabs([
        "📝 Titles (5)",
        "📄 Descriptions (2)",
        "🖼️ Thumbnail Concepts (3)"
    ])

    # ── Tab 1: Titles ──────────────────────────────────────────
    with tab_titles:
        st.subheader("5 Click-Worthy Titles")
        st.caption("Click the copy button next to any title 👇")
        st.divider()
        titles = ai_result.get("titles", [])
        for i, title in enumerate(titles, 1):
            st.markdown(f"**{i}.**")
            st.code(title, language=None)

    # ── Tab 2: Descriptions ────────────────────────────────────
    with tab_descriptions:
        st.subheader("2 Full YouTube Descriptions")
        st.caption()
        st.divider()
        descriptions = ai_result.get("descriptions", [])
        for i, desc in enumerate(descriptions, 1):
            st.markdown(f"**Description {i}**")
            st.code(desc, language=None)
            st.divider()

    # ── Tab 3: Thumbnail Concepts ──────────────────────────────
    with tab_thumbnails:
        st.subheader("3 Thumbnail Concepts")
        st.caption("Paste these straight into Midjourney, Flux, or Canva")
        st.divider()
        concepts = ai_result.get("thumbnail_concepts", [])
        for i, concept in enumerate(concepts, 1):
            with st.expander(f"Concept {i} 🖼️", expanded=(i == 1)):
                st.code(concept, language=None)
import streamlit as st


def show_results(ai_result: dict, video_data: dict):
    """
    Render the full results page with 3 tabs:
    Titles | Descriptions | Thumbnail Concepts
    Each item has a copy button.
    """

    st.divider()

    # ── Video summary header ───────────────────────────────────
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Views", f"{video_data.get('view_count', 0):,}")
    with col2:
        st.metric("Likes", f"{video_data.get('like_count', 0):,}")
    with col3:
        st.metric("Transcript", video_data.get("transcript_source", "N/A"))
    with st.expander("📄 View transcript used by AI"):
        st.write(video_data.get("transcript", "No transcript available"))

    st.divider()

    # ── 3 Tabs ─────────────────────────────────────────────────
    tab_titles, tab_descriptions, tab_thumbnails = st.tabs([
        "Titles (10)",
        "Descriptions (3)",
        "Thumbnail Concepts (5)"
    ])

    # ── Tab 1: Titles ──────────────────────────────────────────
    with tab_titles:
        st.subheader("10 Click-Worthy Titles")
        st.caption("Pick your favorite and A/B test it against your current title.")
        st.divider()

        titles = ai_result.get("titles", [])
        if not titles:
            st.warning("No titles were generated. Try again.")
        else:
            for i, title in enumerate(titles, 1):
                col_text, col_btn = st.columns([5, 1])
                with col_text:
                    st.markdown(f"**{i}.** {title}")
                with col_btn:
                    st.code(title, language=None)

    # ── Tab 2: Descriptions ────────────────────────────────────
    with tab_descriptions:
        st.subheader("3 Full YouTube Descriptions")
        st.caption("Each description includes a hook, key points, CTA, and hashtags.")
        st.divider()

        descriptions = ai_result.get("descriptions", [])
        if not descriptions:
            st.warning("No descriptions were generated. Try again.")
        else:
            for i, desc in enumerate(descriptions, 1):
                st.markdown(f"#### Description {i}")
                st.text_area(
                    label=f"desc_{i}",
                    value=desc,
                    height=200,
                    label_visibility="collapsed",
                    key=f"desc_area_{i}"
                )
                st.divider()

    # ── Tab 3: Thumbnail Concepts ──────────────────────────────
    with tab_thumbnails:
        st.subheader("5 Thumbnail Concepts")
        st.caption("Hand these descriptions to a designer or paste into Midjourney/Flux.")
        st.divider()

        concepts = ai_result.get("thumbnail_concepts", [])
        if not concepts:
            st.warning("No thumbnail concepts were generated. Try again.")
        else:
            for i, concept in enumerate(concepts, 1):
                with st.expander(f"Concept {i}", expanded=(i == 1)):
                    st.write(concept)
                    st.code(concept, language=None)
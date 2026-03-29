def build_prompt(user_profile: dict, video_data: dict) -> str:
    tags = ", ".join(video_data.get("tags", [])) or "None"
    style = user_profile.get("style_preferences", "No preference")
    transcript = video_data.get("transcript", "")

    return f"""
You are an expert YouTube content strategist.

=== LANGUAGE RULE — THIS IS THE MOST IMPORTANT RULE ===
1. First, detect the language of the VIDEO TRANSCRIPT above.
2. You MUST write 100% of your entire output in that EXACT same language.
3. Zero mixing allowed. If the transcript is in Hindi → output in Hindi only.
   If the transcript is in German → output in German only.
   If the transcript is in Arabic (Darija or MSA) → output in Arabic only.
   If the transcript is in English → output in English only.
4. Brand names, technical terms, and single words that appeared in the transcript are allowed to stay as they are.
   Everything else must be in the detected language.

=== CREATOR PROFILE ===
- Niche: {user_profile.get("niche", "Unknown")}
- Subscribers: {user_profile.get("subscribers", "Unknown"):,}
- Style preferences: {style}

=== VIDEO TRANSCRIPT (THIS IS THE SOURCE OF TRUTH) ===
{transcript}

=== VIDEO METADATA (use only for context) ===
- Current title: {video_data.get("title", "Unknown")}
- Channel: {video_data.get("channel_title", "Unknown")}
- Views: {video_data.get("view_count", 0):,}
- Likes: {video_data.get("like_count", 0):,}
- Current tags: {tags}

YOUR TASK (strictly follow the language rule above):

1. TITLES: Write exactly 5 YouTube titles in the detected language only.
   - Base every title on specific moments from the transcript.
   - Minimum 6 words per title.
   - Make them highly clickable.
   - Match the creator's style preferences.
   - Number them 1-5.

2. DESCRIPTIONS: Write exactly 2 full YouTube descriptions in the detected language only.
   - 150-200 words each.
   - Include hook, key points from transcript, CTA, and hashtags.
   - Number them 1-2.

3. THUMBNAIL_CONCEPTS: Write exactly 3 thumbnail concepts in the detected language only.
   - Describe visual layout, colors, facial expression, overlay text.
   - Based on specific transcript moments.
   - Number them 1-3.

FORMATTING (do not add any extra text):
TITLES:
DESCRIPTIONS:
THUMBNAIL_CONCEPTS:
"""
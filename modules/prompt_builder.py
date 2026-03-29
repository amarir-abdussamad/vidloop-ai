def build_prompt(user_profile: dict, video_data: dict) -> str:
    tags = ", ".join(video_data.get("tags", [])) or "None"
    style = user_profile.get("style_preferences", "No preference")
    transcript = video_data.get("transcript", "")

    return f"""
You are an expert YouTube content strategist.

=== LANGUAGE RULE — THIS IS THE MOST IMPORTANT RULE ===
1. First, detect the language of the VIDEO TRANSCRIPT above.
2. You MUST write 100% of your entire output in that EXACT same language.
3. Zero mixing allowed.
4. Brand names, technical terms, and single words that appeared in the transcript may stay as they are.
   Everything else must be in the detected language.

=== STEP 1 — BEFORE WRITING ANYTHING, ANALYZE THE VIDEO ===
Extract these 4 things from the transcript and metadata:
1. TOPIC: What is this video specifically about? (1 short sentence)
2. TONE: What is the emotional mood? Choose EXACTLY ONE from this list:
   - 😂 Comedy/Humor → use jokes, exaggeration, funny hooks
   - 😱 Shocking/Controversial → use curiosity, disbelief, "I can't believe..."
   - 🎓 Educational → use "how to", "learn", "discover", numbers
   - 😢 Emotional/Inspirational → use story-driven, empathy, transformation
   - 🔥 Motivational → use challenge, achievement, energy
   - 😎 Lifestyle/Vlog → use personal, casual, relatable
   - 🎮 Entertainment → use fun, excitement, reaction
   - 💰 Finance/Business → use numbers, results, growth
   - 😨 Horror/Dark → use fear, suspense, mystery
   - 🌍 Adventure/Travel → use discovery, experience, places
3. AUDIENCE: Who is watching this? (age group + main interests)
4. HOOK: What is the most surprising or interesting moment in the transcript?

=== STEP 2 — USE THE 4 POINTS ABOVE ===
- Every title, description, and thumbnail concept MUST match the detected TONE.
- Never mix tones. If it's a comedy video → keep everything funny.
- If it's finance → keep it professional with numbers and results.
- Use appropriate emojis naturally in titles and descriptions to make them more engaging (1-2 emojis max per title, a few in descriptions).

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

YOUR TASK (strictly follow STEP 1, STEP 2 and the language rule):

1. TITLES: Write exactly 5 YouTube titles.
   - Base every title on specific moments from the transcript.
   - Minimum 6 words per title.
   - Highly clickable + match the detected TONE + add 1-2 emojis.
   - Match creator style preferences.
   - Number them 1-5.

2. DESCRIPTIONS: Write exactly 2 full YouTube descriptions.
   - 150-200 words each.
   - Include hook, key points from transcript, CTA, hashtags.
   - Match the detected TONE + use emojis naturally.
   - Number them 1-2.

3. THUMBNAIL_CONCEPTS: Write exactly 3 thumbnail concepts.
   - Describe visual layout, colors, facial expression, overlay text.
   - Based on specific transcript moments and the detected TONE.
   - Number them 1-3.

FORMATTING (do not add any extra text):
TITLES:
DESCRIPTIONS:
THUMBNAIL_CONCEPTS:
"""
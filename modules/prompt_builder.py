def build_prompt(user_profile: dict, video_data: dict) -> str:
    """
    Combine the user's creator profile + video data into one
    powerful, personalized prompt for the LLM.
    """

    # Format tags nicely
    tags = ", ".join(video_data.get("tags", [])) or "None"

    # Format style preferences
    style = user_profile.get("style_preferences", "No preference")

    return f"""
You are an expert YouTube content strategist with 10+ years of experience helping creators grow.

CREATOR PROFILE:
- Niche: {user_profile.get("niche", "Unknown")}
- Subscribers: {user_profile.get("subscribers", "Unknown"):,}
- Style preferences: {style}
- Best performing video: {user_profile.get("best_video_url", "Unknown")}
- Worst performing video: {user_profile.get("worst_video_url", "Unknown")}

VIDEO BEING ANALYZED:
- Title: {video_data.get("title", "Unknown")}
- Channel: {video_data.get("channel_title", "Unknown")}
- Views: {video_data.get("view_count", 0):,}
- Likes: {video_data.get("like_count", 0):,}
- Current tags: {tags}
- Current description snippet: {video_data.get("description", "")[:300]}

VIDEO TRANSCRIPT (first 8000 chars):
{video_data.get("transcript", "")}

YOUR TASKS:
Based on the transcript and creator profile above, generate the following:

1. TITLES: Write exactly 10 YouTube titles optimized for high CTR.
   - Match the creator's style preferences
   - Use curiosity, numbers, or emotional hooks
   - Keep each title under 70 characters
   - Number them 1-10

2. DESCRIPTIONS: Write exactly 3 full YouTube descriptions.
   - Each description: 150-200 words
   - Include: hook sentence, key points from video, CTA, relevant hashtags
   - Number them 1-3

3. THUMBNAIL_CONCEPTS: Write exactly 5 thumbnail concept ideas.
   - Each concept: describe the visual layout, colors, facial expression, and overlay text
   - Make them specific enough to hand to a designer
   - Number them 1-5

IMPORTANT FORMATTING RULES:
- Use EXACTLY these section headers (in caps): TITLES:, DESCRIPTIONS:, THUMBNAIL_CONCEPTS:
- Do not add any intro or outro text
- Start directly with TITLES:
"""
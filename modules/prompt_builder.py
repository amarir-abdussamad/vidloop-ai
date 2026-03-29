def build_analysis_prompt(video_data: dict) -> str:
    transcript = video_data.get("transcript", "")

    return f"""
Analyze this YouTube video.

TRANSCRIPT:
{transcript}

Return ONLY valid JSON:

{{
  "language": "",
  "topic": "",
  "tone": "",
  "hook": ""
}}
"""


def build_generation_prompt(user_profile: dict, video_data: dict, analysis: dict) -> str:
    tags = ", ".join(video_data.get("tags", [])) or "None"

    return f"""
You are a YouTube content expert.

VIDEO ANALYSIS:
- Language: {analysis.get("language")}
- Topic: {analysis.get("topic")}
- Tone: {analysis.get("tone")}
- Hook: {analysis.get("hook")}

CREATOR PROFILE:
- Niche: {user_profile.get("niche", "")}
- Subscribers: {user_profile.get("subscribers", 0)}
- Style: {user_profile.get("style_preferences", "")}

VIDEO CONTEXT:
- Current title: {video_data.get("title", "")}
- Channel: {video_data.get("channel_title", "")}
- Tags: {tags}

RULES:
- Use ONLY {analysis.get("language")}
- Keep tone consistent
- Make content engaging and clickable
- Use emojis naturally (optional)

Return ONLY valid JSON:

{{
  "titles": ["", "", "", "", ""],
  "descriptions": ["", ""],
  "thumbnail_concepts": ["", "", ""]
}}
"""
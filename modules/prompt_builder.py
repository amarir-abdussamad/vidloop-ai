def build_prompt(user_profile: dict, video_data: dict) -> str:

    tags = ", ".join(video_data.get("tags", [])) or "None"
    style = user_profile.get("style_preferences", "No preference")
    transcript = video_data.get("transcript", "")

    return f"""
You are an expert YouTube content strategist with 10+ years of experience.

CREATOR PROFILE:
- Niche: {user_profile.get("niche", "Unknown")}
- Subscribers: {user_profile.get("subscribers", "Unknown"):,}
- Style preferences: {style}

VIDEO TRANSCRIPT (this is the SOURCE OF TRUTH — base everything on this):
{transcript}

VIDEO METADATA (secondary context only):
- Current title: {video_data.get("title", "Unknown")}
- Channel: {video_data.get("channel_title", "Unknown")}
- Views: {video_data.get("view_count", 0):,}
- Likes: {video_data.get("like_count", 0):,}
- Current tags: {tags}

YOUR TASKS:

⚠️ LANGUAGE RULE — MOST IMPORTANT:
Detect the language of the transcript.
Write 100% of your output in that exact same language.
Zero English words allowed if the transcript is Arabic.
Zero Arabic words allowed if the transcript is English.
Not even brand names, technical terms, or hashtags should break this rule.

⚠️ CRITICAL RULE: You MUST base all output on the actual VIDEO TRANSCRIPT above.
Do NOT generate generic titles. Every title, description, and concept must reflect
the SPECIFIC topics, stories, moments, and details found in the transcript.
If the transcript is in Arabic, generate output in Arabic. English → English. Etc.

- CRITICAL: Write titles and descriptions and thumbnail concepts in ONE language only — the same language as the transcript
- Do NOT mix English words into Arabic titles
- If the transcript is in Arabic (Darija or MSA), every single word in every title, description, and thumbnail concept must be Arabic

1. TITLES: Write exactly 5 YouTube titles.
   - FIRST read the transcript carefully and identify: the main topic, key moments, surprising facts, conflicts, results, or stories
   - THEN build each title around one of those specific extracted points
   - A title must be a complete meaningful phrase — minimum 6 words
   - NEVER write 2-3 word titles — those are thumbnail words not titles
   - Every title must make someone who hasn't watched the video curious enough to click
   - Use formats like: "How X led to Y", "Why X is changing Y", "X things about Y that Z", "The truth about X that nobody talks about"
   - Apply these formats in whatever language the transcript is in
   - Match creator style preferences: {style}
   - Number them 1-5

2. DESCRIPTIONS: Write exactly 2 full YouTube descriptions.
   - Each MUST mention specific points, moments, or insights from the transcript
   - Include: hook, key points, CTA, relevant hashtags
   - 150-200 words each
   - Number them 1-2

3. THUMBNAIL_CONCEPTS: Write exactly 3 thumbnail concepts.
   - Each MUST be based on a specific moment or topic from the transcript
   - Describe: visual layout, colors, facial expression, overlay text
   - Specific enough to hand to a designer
   - Number them 1-3

FORMATTING RULES:
- Use EXACTLY these headers: TITLES:, DESCRIPTIONS:, THUMBNAIL_CONCEPTS:
- Start directly with TITLES: — no intro text
"""
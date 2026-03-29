import streamlit as st
from groq import Groq
from modules.prompt_builder import build_prompt


def generate_content(user_profile: dict, video_data: dict, language: str = "Auto-detect") -> dict:
    """
    Send the built prompt to Groq LLaMA 3.3 70B and parse the response
    into a structured dict with titles, descriptions, and thumbnail concepts.

    Returns:
        {
            "titles": [...],           # list of 10 strings
            "descriptions": [...],     # list of 3 strings
            "thumbnail_concepts": [...] # list of 5 strings
        }
    Or a dict with an "error" key if something went wrong.
    """
    try:
        client = Groq(api_key=st.secrets["GROQ_API_KEY"])
        prompt = build_prompt(user_profile, video_data, language)

        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.8,      # slightly creative but not random
            max_tokens=4000,      # enough for all 3 sections
        )

        raw = response.choices[0].message.content
        return _parse_response(raw)

    except Exception as e:
        return {"error": f"AI generation failed: {e}"}
    
def _parse_response(raw: str) -> dict:
    """
    Parse the raw LLM response into structured lists.
    Splits on the three section headers: TITLES:, DESCRIPTIONS:, THUMBNAIL_CONCEPTS:
    """
    try:
        # Split into 3 sections
        parts = raw.split("DESCRIPTIONS:")
        titles_raw = parts[0].replace("TITLES:", "").strip()
        rest = parts[1] if len(parts) > 1 else ""

        parts2 = rest.split("THUMBNAIL_CONCEPTS:")
        descriptions_raw = parts2[0].strip()
        thumbnails_raw = parts2[1].strip() if len(parts2) > 1 else ""

        return {
            "titles": _parse_numbered_list(titles_raw),
            "descriptions": _parse_numbered_list(descriptions_raw),
            "thumbnail_concepts": _parse_numbered_list(thumbnails_raw),
            "raw": raw  # keep raw for debugging
        }

    except Exception as e:
        return {"error": f"Parsing failed: {e}", "raw": raw}
    
def _parse_numbered_list(text: str) -> list[str]:
    """
    Convert a numbered list like:
        1. First item
        2. Second item
    Into a Python list: ["First item", "Second item"]
    """
    lines = text.strip().split("\n")
    items = []
    current = ""

    for line in lines:
        line = line.strip()
        if not line:
            if current:
                items.append(current.strip())
                current = ""
            continue

        # Check if line starts a new numbered item
        import re
        if re.match(r"^\d+[\.\)]\s+", line):
            if current:
                items.append(current.strip())
            current = re.sub(r"^\d+[\.\)]\s+", "", line)
        else:
            # Continuation of previous item
            current += " " + line

    if current:
        items.append(current.strip())

    return [item for item in items if item]
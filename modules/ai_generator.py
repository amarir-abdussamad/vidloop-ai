import streamlit as st
from groq import Groq
import json
from modules.prompt_builder import (
    build_analysis_prompt,
    build_generation_prompt
)


def safe_json_loads(text: str):
    try:
        return json.loads(text)
    except:
        import re
        match = re.search(r"\{.*\}", text, re.DOTALL)
        if match:
            try:
                return json.loads(match.group())
            except:
                return None
        return None


def generate_content(user_profile: dict, video_data: dict) -> dict:
    try:
        client = Groq(api_key=st.secrets["GROQ_API_KEY"])

        # -------------------
        # 🧠 STEP 1: ANALYSIS
        # -------------------
        analysis_prompt = build_analysis_prompt(video_data)

        analysis_res = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": analysis_prompt}],
            temperature=0.3,
        )

        analysis_raw = analysis_res.choices[0].message.content.strip()
        analysis = safe_json_loads(analysis_raw)

        if not analysis:
            return {"error": "Analysis parsing failed", "raw": analysis_raw}

        # -------------------
        # ✨ STEP 2: GENERATION
        # -------------------
        gen_prompt = build_generation_prompt(user_profile, video_data, analysis)

        gen_res = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": gen_prompt}],
            temperature=0.6,
        )

        gen_raw = gen_res.choices[0].message.content.strip()
        result = safe_json_loads(gen_raw)

        if not result:
            return {"error": "Generation parsing failed", "raw": gen_raw}

        return {
            "titles": result.get("titles", []),
            "descriptions": result.get("descriptions", []),
            "thumbnail_concepts": result.get("thumbnail_concepts", []),
            "analysis": analysis
        }

    except Exception as e:
        return {"error": f"AI generation failed: {e}"}
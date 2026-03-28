import re
import streamlit as st
from googleapiclient.discovery import build
from youtube_transcript_api import YouTubeTranscriptApi
from groq import Groq


def extract_video_id(url: str) -> str | None:
    patterns = [
        r"(?:v=)([a-zA-Z0-9_-]{11})",
        r"(?:youtu\.be/)([a-zA-Z0-9_-]{11})",
        r"(?:shorts/)([a-zA-Z0-9_-]{11})"
    ]
    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)
    return None


def fetch_video_metadata(video_id: str) -> dict:
    try:
        youtube = build(
            "youtube", "v3",
            developerKey=st.secrets["YOUTUBE_API_KEY"]
        )
        response = youtube.videos().list(
            part="snippet,statistics",
            id=video_id
        ).execute()

        if not response["items"]:
            return {"error": "Video not found. It may be private or deleted."}

        item = response["items"][0]
        snippet = item["snippet"]
        stats = item["statistics"]

        return {
            "title": snippet.get("title", ""),
            "description": snippet.get("description", "")[:500],
            "tags": snippet.get("tags", [])[:10],
            "channel_title": snippet.get("channelTitle", ""),
            "view_count": int(stats.get("viewCount", 0)),
            "like_count": int(stats.get("likeCount", 0)),
        }
    except Exception as e:
        return {"error": f"Failed to fetch metadata: {e}"}


def fetch_transcript_from_captions(video_id: str) -> str | None:
    try:
        api = YouTubeTranscriptApi()

        # List all available transcripts for this video
        transcript_list = api.list(video_id)

        # Grab the first available one — any language
        transcript = next(iter(transcript_list))
        data = transcript.fetch()
        full_text = " ".join([entry.text for entry in data])
        return full_text.strip()

    except Exception as e:
        st.warning(f"Caption error: {e}")
        return None


def process_youtube_url(url: str) -> dict:
    video_id = extract_video_id(url)
    if not video_id:
        return {"error": "❌ Could not extract a video ID from this URL."}

    metadata = fetch_video_metadata(video_id)
    if "error" in metadata:
        return metadata

    transcript = fetch_transcript_from_captions(video_id)

    if not transcript:
        return {"error": "❌ No captions found for this video. Try a video with captions enabled."}

    return {
        "video_id": video_id,
        "title": metadata["title"],
        "description": metadata["description"],
        "tags": metadata["tags"],
        "channel_title": metadata["channel_title"],
        "view_count": metadata["view_count"],
        "like_count": metadata["like_count"],
        "transcript": transcript[:8000],
        "transcript_source": "YouTube Captions"
    }
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
    import yt_dlp
    import os
    import tempfile

    try:
        with tempfile.TemporaryDirectory() as tmpdir:
            ydl_opts = {
                "quiet": True,
                "no_warnings": True,
                "skip_download": True,        # don't download video
                "writeautomaticsub": True,     # get auto-generated subs
                "writesubtitles": True,        # get manual subs too
                "subtitlesformat": "vtt",      # vtt format
                "subtitleslangs": ["all"],
                "outtmpl": os.path.join(tmpdir, "sub"),
            }

            url = f"https://www.youtube.com/watch?v={video_id}"

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=True)

            # Find the downloaded subtitle file
            for f in os.listdir(tmpdir):
                if f.endswith(".vtt"):
                    with open(os.path.join(tmpdir, f), "r", encoding="utf-8") as file:
                        vtt_content = file.read()
                    return _parse_vtt(vtt_content)

            return None

    except Exception as e:
        st.warning(f"Caption error: {e}")
        return None


def _parse_vtt(vtt: str) -> str:
    """Strip VTT timestamps and formatting, return plain text."""
    import re
    lines = vtt.split("\n")
    text_lines = []
    for line in lines:
        line = line.strip()
        # Skip empty lines, WEBVTT header, timestamps, and NOTE lines
        if not line:
            continue
        if line.startswith("WEBVTT") or line.startswith("NOTE") or line.startswith("Kind:") or line.startswith("Language:"):
            continue
        if re.match(r"^\d{2}:\d{2}", line):  # timestamp line
            continue
        if re.match(r"^\d+$", line):  # sequence number
            continue
        # Remove HTML tags like <c>, </c>, <00:00:00.000>
        line = re.sub(r"<[^>]+>", "", line)
        if line:
            text_lines.append(line)

    # Remove duplicate consecutive lines (VTT often repeats)
    cleaned = []
    for line in text_lines:
        if not cleaned or line != cleaned[-1]:
            cleaned.append(line)

    return " ".join(cleaned).strip()


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
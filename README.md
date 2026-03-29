# VidLoop AI 🎬

> **The AI co-pilot that watches your YouTube videos, generates click-worthy titles, descriptions, and thumbnail concepts — personalized to your channel.**

![Python](https://img.shields.io/badge/Python-3.10+-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-1.x-red)
![Supabase](https://img.shields.io/badge/Supabase-PostgreSQL-green)
![Groq](https://img.shields.io/badge/Groq-LLaMA_3.3_70B-orange)
![License](https://img.shields.io/badge/License-MIT-purple)

---

## 🚀 Live Demo

**[vidloop-ai.streamlit.app](https://vidloop-ai.streamlit.app)**

---

## 📖 What is VidLoop AI?

VidLoop AI solves a real pain for YouTubers: spending hours writing titles, descriptions, and brainstorming thumbnail ideas — with no guarantee they'll perform well.

You paste a YouTube URL → the AI reads the full transcript → instantly generates personalized titles, descriptions, and thumbnail concepts based on your channel's niche, style, and audience.

**What makes it different:** Every output is personalized to your creator profile — not generic suggestions that could apply to any channel.

---

## ✨ Features (MVP v1.0)

- 🔐 **Secure Auth** — Email signup/login via Supabase Auth
- 📋 **Creator Onboarding** — 5-question profile that personalizes every AI output
- 🔗 **YouTube URL Input** — Paste any public YouTube video URL
- 📝 **Auto Transcription** — Fetches captions in any language automatically
- 🤖 **AI Generation** — 5 titles, 2 descriptions, 3 thumbnail concepts via LLaMA 3.3 70B
- 🌍 **Multi-language Output** — Auto-detect or choose English, Arabic, French, Spanish, German
- 🎭 **Tone Matching** — AI detects video mood (comedy, educational, horror...) and matches it
- 📊 **Usage Tracking** — Free tier: 30 generations/month with 60s cooldown
- 📋 **Copy Buttons** — One-click copy for every generated output

---

## 🛠️ Tech Stack

| Layer | Tool |
|---|---|
| Frontend + Backend | Streamlit (Python) |
| Database + Auth | Supabase (PostgreSQL) |
| AI / LLM | Groq API — LLaMA 3.3 70B |
| Transcription | youtube-transcript-api |
| YouTube Metadata | YouTube Data API v3 |
| Deployment | Streamlit Cloud |

---

## 📁 Project Structure

```
vidloop-ai/
├── app.py                      # Entry point + routing
├── config.py                   # Tier limits + constants
├── requirements.txt
├── packages.txt                # System dependencies (ffmpeg)
├── .streamlit/
│   └── secrets.toml            # API keys (gitignored)
├── modules/
│   ├── auth.py                 # Login / signup / logout
│   ├── onboarding.py           # Creator profile form
│   ├── youtube_fetcher.py      # Metadata + transcript fetching
│   ├── prompt_builder.py       # Personalized prompt construction
│   ├── ai_generator.py         # Groq API call + response parsing
│   ├── rate_limiter.py         # Per-user monthly limits
│   └── results.py              # Tabbed results UI
└── utils/
    └── supabase_client.py      # Singleton DB connection
```

---

## ⚡ Quick Start (Local)

### 1. Clone the repo
```bash
git clone https://github.com/YOUR_USERNAME/vidloop-ai.git
cd vidloop-ai
```

### 2. Create virtual environment
```bash
python -m venv venv
source venv/bin/activate  # Mac/Linux
venv\Scripts\activate     # Windows
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Set up secrets
Create `.streamlit/secrets.toml`:
```toml
SUPABASE_URL = "https://your-project.supabase.co"
SUPABASE_KEY = "your-anon-key"
GROQ_API_KEY = "your-groq-key"
YOUTUBE_API_KEY = "your-youtube-api-key"
```

### 5. Set up Supabase
Run the SQL in `supabase/schema.sql` in your Supabase SQL Editor.

### 6. Run the app
```bash
streamlit run app.py
```

---

## 🔑 API Keys You Need

| Key | Where to get it | Cost |
|---|---|---|
| `SUPABASE_URL` + `SUPABASE_KEY` | [supabase.com](https://supabase.com) | Free |
| `GROQ_API_KEY` | [console.groq.com](https://console.groq.com) | Free |
| `YOUTUBE_API_KEY` | [console.cloud.google.com](https://console.cloud.google.com) | Free (10K units/day) |

---

## 💰 Pricing Tiers

| Tier | Price | Generations/month |
|---|---|---|
| Free | $0 | 30 |
| Pro | Coming soon | Unlimited |

---

## 🗺️ Roadmap

- **v1.0** ✅ — URL input → transcription → AI titles/descriptions/thumbnails
- **v1.1** — 7-day performance review loop + free regeneration
- **v1.2** — ML personalization engine (learns from your results)
- **v2.0** — Cross-platform repurposing (Reels, TikTok, LinkedIn, X)
- **v2.5** — Thumbnail image generation inside the app

---

## 🤝 Contributing

This project is open source and contributions are welcome!

1. Fork the repo
2. Create a feature branch: `git checkout -b feature/your-feature`
3. Commit your changes: `git commit -m "✨ Add: your feature"`
4. Push and open a PR

---

## 📬 Contact

- **Creator:** Abdessamad AMARIR (Morocco 🇲🇦)
- **X / Twitter:** [@Abdu_amarir](https://x.com/Abdu_amarir)
- **Live app:** [vidloop-ai.streamlit.app](https://vidloop-ai.streamlit.app)

---

## 📄 License

MIT License — free to use, modify, and distribute.

---
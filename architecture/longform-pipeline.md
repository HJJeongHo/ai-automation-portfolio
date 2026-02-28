# YouTube Longform Pipeline — Architecture Deep Dive

## Overview

Fully automated 7-stage pipeline producing publish-ready YouTube videos on finance and tech topics. Zero manual intervention from topic selection to YouTube upload.

**Channel:** @TheMoneyPlaybooks
**Output:** 13+ videos produced
**Avg. Production Time:** ~15 minutes per video

## Pipeline Stages

### Stage 1 — Topic Research
- Claude analyzes trending finance/tech signals
- Generates video concepts with target keywords and angles
- Deduplication check against PostgreSQL to avoid repeat topics

### Stage 2 — Script Generation (Claude Opus)
- 1,500–3,000 word scripts with hook-driven intros
- Section-based structure with clear transitions
- Data points and statistics woven into narrative
- SRT subtitle file auto-generated
- Affiliate mention points strategically placed

### Stage 3 — Text-to-Speech
- OpenAI TTS (nova voice, 1.15x speed)
- Background music mixed at 12% volume
- Consistent voice identity across all videos

### Stage 4 — Stock Footage (Pexels API)
- Context-aware search queries derived from script sections
- HD video clips matched to narration segments
- Automatic downloading and caching

### Stage 5 — Video Composition (FFmpeg)
- Fast cuts (3–5 second segments) for retention
- Ken Burns zoompan effects
- Section crossfade transitions
- SFX (whoosh, ding, impact) at section breaks
- Text overlay for key statistics
- Multi-track audio mixing (narration + BGM + SFX)

### Stage 6 — Thumbnail Generation
- DALL-E 3 background generation matching video topic
- Bold typography with key statistics overlay
- Modern layout designed for click-through rate

### Stage 7 — YouTube Upload (API v3)
- Optimized title, description, tags
- Affiliate links auto-inserted in description
- Category: Education (27)
- Automatic playlist assignment (Finance or Tech)
- Telegram notification on success/failure

## Architecture Diagram

```
topic_researcher ──▶ script_generator ──▶ voice_generator
                                               │
    stock_fetcher ──▶ video_composer ◀──────────┘
                          │
                   thumbnail_generator
                          │
                    youtube_uploader
                          │
                   telegram_notifier
```

## Design Decisions

| Decision | Rationale |
|----------|-----------|
| Fast cuts (3-5s) | Prevents viewer drop-off; validated by retention data |
| SFX at section breaks | Improves perceived production quality at negligible cost |
| PostgreSQL tracking | Enables deduplication, analytics, and audit trails |
| Telegram alerts | Hands-off operation with instant failure notification |
| Model routing | Opus for scripts (quality), Sonnet for metadata (cost) |

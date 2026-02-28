# Multilingual Shorts Factory — Architecture Deep Dive

## Overview

Batch production system for short-form video content across multiple languages and platforms.

**Output:** 52+ shorts produced across 2 languages
**Platforms:** YouTube Shorts, Instagram Reels
**Languages:** Korean, English

## Pipeline Stages

### Stage 1 — Content Generation (Claude)
- Viral-style topic selection from 70+ subtopic pool
- Hook-first script structure optimized for <60s format
- Platform-native formatting (vertical 9:16)

### Stage 2 — Translation (Claude Sonnet)
- Culturally adapted translations (not literal)
- Localized examples and references per market
- Tone adjustment for target audience

### Stage 3 — Text-to-Speech
- Edge TTS (free tier) for cost efficiency
- Language-specific voice selection
- Speed and tone optimization per language

### Stage 4 — Video Composition (FFmpeg)
- Pexels stock footage auto-sourced by topic
- ASS subtitle overlay (bold, centered)
- Background music at 10% volume
- Vertical format (1080x1920)

### Stage 5 — Multi-Platform Upload
- YouTube Shorts via Data API v3
- Instagram Reels via automated uploader
- Upload tracking in PostgreSQL
- Rate limiting to respect platform limits

## Architecture

```
Content Generator (Claude)
      │
      ├──▶ Korean Pipeline ──▶ Edge TTS (ko) ──▶ FFmpeg ──▶ YouTube/IG
      │
      └──▶ English Pipeline ──▶ Edge TTS (en) ──▶ FFmpeg ──▶ YouTube/IG
```

## Production Schedule

| Time | Action |
|------|--------|
| 07:00 | Generate ko:4 + en:1 shorts |
| 08:00 | Instagram upload batch (3/day) |
| 09:00 | YouTube upload batch #1 |
| 16:00 | YouTube upload batch #2 |

## Cost Efficiency

| Component | Cost |
|-----------|------|
| Claude API (content) | ~$0.02/short |
| Edge TTS | Free |
| Pexels footage | Free |
| FFmpeg | Free |
| **Total per short** | **~$0.02** |

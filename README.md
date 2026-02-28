# AI Automation Portfolio

> Production AI systems generating content across 9 channels — fully autonomous, running 24/7.

## What I Build

I design and operate **end-to-end AI automation pipelines** that handle everything from research to publishing with zero manual intervention.

## Live Production Systems

| System | Output | Status |
|--------|--------|--------|
| [themoneyplaybooks.com](https://themoneyplaybooks.com) | 90+ SEO articles (Finance) | ✅ Live |
| [techstackdaily.com](https://techstackdaily.com) | 56+ SEO articles (Tech/AI) | ✅ Live |
| [@TheMoneyPlaybooks](https://youtube.com/@TheMoneyPlaybooks) | Longform finance/tech videos | ✅ Live |
| YouTube Shorts | 52+ shorts across 2 languages | ✅ Live |
| Instagram Reels | AI-powered content automation | ✅ Live |
| Digital Products | 10 products on Gumroad | ✅ Live |

**Total monthly infrastructure cost: ~$200**

---

## Architecture Overview

### 1. YouTube Longform Pipeline (7 Stages)

Fully automated video production — topic selection to YouTube upload.

```
┌─────────────┐    ┌──────────────┐    ┌─────────────┐
│   Topic      │───▶│   Script     │───▶│   Voice     │
│   Research   │    │   Generation │    │   (TTS)     │
│  (Claude)    │    │  (Claude     │    │  (OpenAI)   │
│              │    │   Opus)      │    │             │
└─────────────┘    └──────────────┘    └──────┬──────┘
                                              │
┌─────────────┐    ┌──────────────┐    ┌──────▼──────┐
│   YouTube   │◀───│  Thumbnail   │◀───│   Video     │
│   Upload    │    │  (DALL-E 3)  │    │  Composer   │
│  (API v3)   │    │              │    │  (FFmpeg)   │
└─────────────┘    └──────────────┘    └─────────────┘
```

**Key specs:**
- ~15 min production time per video
- Fast cuts (3-5s) + zoompan + crossfade transitions + SFX
- Auto-generated DALL-E 3 thumbnails
- Affiliate links auto-inserted in descriptions
- Playlist auto-assignment (Finance / Tech)

### 2. SEO Content Engine

Automated article generation, optimization, and deployment.

```
┌─────────────┐    ┌──────────────┐    ┌─────────────┐
│  Keyword    │───▶│   Article    │───▶│    SEO      │
│  Research   │    │  Generation  │    │ Optimizer   │
│             │    │  (Claude)    │    │ (Claude)    │
└─────────────┘    └──────────────┘    └──────┬──────┘
                                              │
┌─────────────┐    ┌──────────────┐    ┌──────▼──────┐
│  Google     │◀───│   Vercel     │◀───│ Affiliate   │
│  Indexing   │    │   Deploy     │    │  Linker     │
└─────────────┘    └──────────────┘    └─────────────┘
```

**Key specs:**
- 146+ articles generated and deployed
- EEAT-aligned content with semantic SEO
- Auto CTA injection + affiliate link management
- Google/Bing Search Console + IndexNow integration
- Next.js 14 SSG on Vercel

### 3. Multilingual Shorts Factory

Batch production of short-form content across languages.

```
┌─────────────┐    ┌──────────────┐    ┌─────────────┐
│  Content    │───▶│  Translation │───▶│    TTS      │
│  Generator  │    │  (Claude)    │    │ (Edge TTS)  │
│  (Claude)   │    │              │    │             │
└─────────────┘    └──────────────┘    └──────┬──────┘
                                              │
┌─────────────┐    ┌──────────────┐    ┌──────▼──────┐
│  YouTube    │◀───│  Instagram   │◀───│   Video     │
│  Upload     │    │  Upload      │    │  Composer   │
└─────────────┘    └──────────────┘    └─────────────┘
```

**Key specs:**
- 5 shorts/day automated production
- Korean + English channels
- Pexels stock footage auto-sourced
- Cross-posting to Instagram Reels

---

## Claude API Expertise

### Model Routing Strategy

Cost-optimized routing between Claude models based on task complexity:

```python
# Model selection based on task requirements
ROUTING = {
    "script_generation":  "opus",    # Complex creative writing
    "seo_optimization":   "sonnet",  # Analytical tasks
    "content_tagging":    "haiku",   # Simple classification
    "translation":        "sonnet",  # Balanced quality/cost
    "topic_research":     "sonnet",  # Research + analysis
}
```

**Result: 60% API cost reduction** while maintaining output quality.

### Prompt Engineering Patterns

- **Multi-stage chains**: Research → Outline → Draft → Optimize → Format
- **Structured output**: JSON schema enforcement for pipeline integration
- **Context management**: Dynamic context window optimization per task
- **Error recovery**: Automatic retry with prompt adjustment on failure
- **Token optimization**: Prompt compression and caching strategies

---

## Tech Stack

| Category | Technologies |
|----------|-------------|
| **Core** | Python 3.11+, asyncio, PostgreSQL 16 |
| **AI/LLM** | Claude API (Opus/Sonnet/Haiku), OpenAI API (GPT-4, DALL-E 3, TTS) |
| **Video** | FFmpeg, pydub, Pexels API |
| **Web** | Next.js 14, React, Vercel, SSG |
| **Data** | asyncpg, Pydantic, SQLAlchemy |
| **DevOps** | Docker, APScheduler, GitHub Actions |
| **APIs** | YouTube Data API v3, Google Search Console, IndexNow, Telegram Bot |
| **Workflow** | n8n, Make.com |

---

## Production Metrics

| Metric | Value |
|--------|-------|
| Total content pieces | 250+ |
| Automated channels | 9 |
| Pipeline stages (longform) | 7 |
| Avg. video production time | ~15 minutes |
| Monthly infrastructure cost | ~$200 |
| Manual intervention required | Near zero |
| Uptime | 24/7 scheduled |

---

## Contact

- **Upwork**: [JeongHo Han — AI Automation Expert](https://www.upwork.com/freelancers/~01efa015cd580282a1)
- **Email**: jjeongho91@gmail.com
- **YouTube**: [@TheMoneyPlaybooks](https://youtube.com/@TheMoneyPlaybooks)

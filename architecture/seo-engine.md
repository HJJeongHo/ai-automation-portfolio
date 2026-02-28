# SEO Content Engine — Architecture Deep Dive

## Overview

Automated article generation, optimization, and deployment pipeline serving two niche sites with 146+ articles.

**Sites:**
- themoneyplaybooks.com (Finance — 90+ articles)
- techstackdaily.com (Tech/AI — 56+ articles)

## Pipeline Stages

### Stage 1 — Keyword Research
- Trend analysis and keyword clustering
- Competition scoring and search volume estimation
- Topic gap identification against existing content

### Stage 2 — Article Generation (Claude Sonnet)
- EEAT-aligned content generation (Experience, Expertise, Authority, Trust)
- 1,500–3,000 word articles with proper heading structure
- Internal linking to existing articles
- Statistics and data points for credibility

### Stage 3 — SEO Optimization (Claude)
- Meta title and description optimization
- Schema markup generation (Article, FAQ, HowTo)
- Keyword density analysis and adjustment
- Readability scoring and improvement

### Stage 4 — Affiliate Link Injection
- Context-aware CTA placement (inline, box, table, editor's pick)
- Affiliate link auto-insertion based on article topic
- Multiple CTA styles for A/B testing potential

### Stage 5 — Deployment (Vercel)
- Next.js 14 Static Site Generation
- Automatic sitemap generation
- Google/Bing Search Console submission
- IndexNow for instant indexing

## Content Pipeline

```
Keyword Research
      │
      ▼
Article Generation (Claude Sonnet)
      │
      ▼
SEO Optimization (Claude)
      │
      ▼
Affiliate CTA Injection
      │
      ▼
Next.js SSG Build ──▶ Vercel Deploy
      │
      ▼
Google/Bing Indexing (IndexNow)
```

## Infrastructure

| Component | Technology |
|-----------|-----------|
| CMS / Framework | Next.js 14 (SSG) |
| Hosting | Vercel |
| Database | PostgreSQL 16 |
| AI | Claude API (Sonnet) |
| Indexing | Google Search Console, IndexNow |
| Analytics | Google Analytics 4 |
| Monitoring | Telegram Bot alerts |

## Results

| Metric | Value |
|--------|-------|
| Total articles | 146+ |
| Sites | 2 (finance + tech) |
| CTA coverage | 108/112 articles |
| Deployment | Automated (Vercel SSG) |
| Indexing | Automated (IndexNow) |

"""
Multi-Stage Prompt Chain Example
================================
Demonstrates a production pattern for chaining Claude API calls
to produce high-quality content through iterative refinement.

This is a simplified version of the pattern used in production.
Actual implementation includes error handling, retries, and monitoring.
"""

import asyncio
from dataclasses import dataclass


@dataclass
class PipelineConfig:
    """Configuration for the content generation pipeline."""
    research_model: str = "claude-sonnet-4-20250514"
    draft_model: str = "claude-opus-4-20250514"
    optimize_model: str = "claude-sonnet-4-20250514"
    max_retries: int = 3


async def research_stage(client, topic: str) -> dict:
    """
    Stage 1: Research and outline generation.
    Uses Sonnet for cost-efficient analytical work.
    """
    response = await client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=2000,
        messages=[{
            "role": "user",
            "content": f"""Research this topic and produce a structured outline.

Topic: {topic}

Return JSON:
{{
    "title": "...",
    "hook": "Opening hook sentence",
    "sections": [
        {{"heading": "...", "key_points": ["..."], "data_needed": ["..."]}}
    ],
    "target_keywords": ["..."],
    "estimated_word_count": 2000
}}"""
        }]
    )
    return parse_json_response(response)


async def draft_stage(client, outline: dict) -> str:
    """
    Stage 2: Full draft generation.
    Uses Opus for complex creative writing.
    """
    response = await client.messages.create(
        model="claude-opus-4-20250514",
        max_tokens=4000,
        messages=[{
            "role": "user",
            "content": f"""Write a full article based on this outline.

Outline: {outline}

Requirements:
- Hook-driven introduction (first 2 sentences must grab attention)
- Each section flows naturally into the next
- Include specific data points and statistics
- Conversational yet authoritative tone
- 1,500-2,500 words"""
        }]
    )
    return response.content[0].text


async def optimize_stage(client, draft: str, keywords: list) -> dict:
    """
    Stage 3: SEO optimization pass.
    Uses Sonnet for analytical optimization work.
    """
    response = await client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=4000,
        messages=[{
            "role": "user",
            "content": f"""Optimize this article for SEO.

Article:
{draft}

Target keywords: {keywords}

Return JSON:
{{
    "optimized_article": "...",
    "meta_title": "... (under 60 chars)",
    "meta_description": "... (under 160 chars)",
    "suggested_internal_links": ["..."],
    "readability_score": 0-100
}}"""
        }]
    )
    return parse_json_response(response)


async def run_pipeline(topic: str):
    """
    Execute the full content generation pipeline.
    Each stage feeds into the next with structured data passing.
    """
    # Stage 1: Research (Sonnet — cost efficient)
    outline = await research_stage(client, topic)
    print(f"✅ Research complete: {len(outline['sections'])} sections")

    # Stage 2: Draft (Opus — highest quality)
    draft = await draft_stage(client, outline)
    print(f"✅ Draft complete: {len(draft.split())} words")

    # Stage 3: Optimize (Sonnet — analytical)
    result = await optimize_stage(client, draft, outline["target_keywords"])
    print(f"✅ Optimization complete: readability {result['readability_score']}/100")

    return result


def parse_json_response(response) -> dict:
    """Extract and parse JSON from Claude response."""
    import json
    text = response.content[0].text
    # Handle markdown code blocks
    if "```json" in text:
        text = text.split("```json")[1].split("```")[0]
    elif "```" in text:
        text = text.split("```")[1].split("```")[0]
    return json.loads(text.strip())

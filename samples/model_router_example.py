"""
LLM Model Router Example
=========================
Demonstrates cost-optimized routing between Claude models
based on task complexity. This pattern reduced API costs by 60%.

Production pattern — simplified for portfolio demonstration.
"""

from enum import Enum
from dataclasses import dataclass


class TaskComplexity(Enum):
    """Task complexity levels mapped to model tiers."""
    HIGH = "high"       # Creative, nuanced, long-form → Opus
    MEDIUM = "medium"   # Analytical, structured → Sonnet
    LOW = "low"         # Classification, tagging → Haiku


@dataclass
class ModelConfig:
    model_id: str
    cost_per_1m_input: float
    cost_per_1m_output: float
    max_tokens: int


# Model pricing (as of 2025)
MODELS = {
    TaskComplexity.HIGH: ModelConfig(
        model_id="claude-opus-4-20250514",
        cost_per_1m_input=15.0,
        cost_per_1m_output=75.0,
        max_tokens=4096,
    ),
    TaskComplexity.MEDIUM: ModelConfig(
        model_id="claude-sonnet-4-20250514",
        cost_per_1m_input=3.0,
        cost_per_1m_output=15.0,
        max_tokens=4096,
    ),
    TaskComplexity.LOW: ModelConfig(
        model_id="claude-haiku-4-5-20251001",
        cost_per_1m_input=0.80,
        cost_per_1m_output=4.0,
        max_tokens=2048,
    ),
}

# Task-to-complexity mapping
TASK_ROUTING = {
    # HIGH — Requires creativity and nuance
    "script_generation": TaskComplexity.HIGH,
    "article_writing": TaskComplexity.HIGH,
    "case_study": TaskComplexity.HIGH,

    # MEDIUM — Analytical and structured
    "seo_optimization": TaskComplexity.MEDIUM,
    "topic_research": TaskComplexity.MEDIUM,
    "translation": TaskComplexity.MEDIUM,
    "outline_generation": TaskComplexity.MEDIUM,
    "meta_generation": TaskComplexity.MEDIUM,

    # LOW — Simple, fast tasks
    "content_tagging": TaskComplexity.LOW,
    "sentiment_analysis": TaskComplexity.LOW,
    "title_scoring": TaskComplexity.LOW,
    "keyword_extraction": TaskComplexity.LOW,
    "language_detection": TaskComplexity.LOW,
}


class ModelRouter:
    """
    Routes tasks to the optimal Claude model based on complexity.

    Cost savings example:
    - Before (all Opus):     $15/1M input across all tasks
    - After (routed):        ~$5.6/1M input weighted average
    - Savings:               ~60%
    """

    def __init__(self, client):
        self.client = client
        self._usage_log = []

    def get_model(self, task_type: str) -> ModelConfig:
        """Get the optimal model for a given task type."""
        complexity = TASK_ROUTING.get(task_type, TaskComplexity.MEDIUM)
        return MODELS[complexity]

    async def generate(self, task_type: str, prompt: str, **kwargs) -> str:
        """
        Route a generation request to the optimal model.
        Handles model selection, token limits, and usage tracking.
        """
        config = self.get_model(task_type)

        response = await self.client.messages.create(
            model=config.model_id,
            max_tokens=kwargs.get("max_tokens", config.max_tokens),
            messages=[{"role": "user", "content": prompt}],
        )

        # Track usage for cost monitoring
        self._log_usage(task_type, config, response.usage)

        return response.content[0].text

    def _log_usage(self, task_type, config, usage):
        """Log API usage for cost tracking and optimization."""
        cost = (
            (usage.input_tokens / 1_000_000) * config.cost_per_1m_input
            + (usage.output_tokens / 1_000_000) * config.cost_per_1m_output
        )
        self._usage_log.append({
            "task": task_type,
            "model": config.model_id,
            "input_tokens": usage.input_tokens,
            "output_tokens": usage.output_tokens,
            "cost_usd": round(cost, 6),
        })

    def get_cost_summary(self) -> dict:
        """Get aggregated cost summary by model tier."""
        summary = {}
        for entry in self._usage_log:
            model = entry["model"]
            if model not in summary:
                summary[model] = {"calls": 0, "total_cost": 0}
            summary[model]["calls"] += 1
            summary[model]["total_cost"] += entry["cost_usd"]
        return summary


# Usage example:
#
# router = ModelRouter(anthropic_client)
#
# # Automatically routes to Opus (high complexity)
# script = await router.generate("script_generation", "Write a video script about...")
#
# # Automatically routes to Sonnet (medium complexity)
# seo = await router.generate("seo_optimization", "Optimize this article...")
#
# # Automatically routes to Haiku (low complexity)
# tags = await router.generate("content_tagging", "Tag this content...")
#
# print(router.get_cost_summary())

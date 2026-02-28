"""
Async Workflow Orchestrator Example
====================================
Demonstrates production-grade pipeline orchestration with:
- Async stage execution
- Error recovery and retry logic
- Progress tracking via database
- Telegram notifications for monitoring

Simplified from production — actual implementation includes
database persistence, file management, and API integrations.
"""

import asyncio
import time
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Callable


class StageStatus(Enum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    RETRYING = "retrying"


@dataclass
class StageResult:
    stage_name: str
    status: StageStatus
    output: Any = None
    error: str | None = None
    duration_seconds: float = 0
    retries: int = 0


@dataclass
class PipelineConfig:
    max_retries: int = 3
    retry_delay_seconds: float = 2.0
    notify_on_failure: bool = True
    notify_on_completion: bool = True


class PipelineOrchestrator:
    """
    Orchestrates multi-stage content production pipelines.

    Features:
    - Sequential stage execution with data passing
    - Automatic retry with exponential backoff
    - Real-time progress tracking
    - Telegram alerts on failure/completion
    - Database state persistence for recovery
    """

    def __init__(self, name: str, config: PipelineConfig | None = None):
        self.name = name
        self.config = config or PipelineConfig()
        self.stages: list[tuple[str, Callable]] = []
        self.results: list[StageResult] = []

    def add_stage(self, name: str, func: Callable):
        """Register a pipeline stage."""
        self.stages.append((name, func))
        return self

    async def run(self, initial_input: Any = None) -> list[StageResult]:
        """Execute all stages sequentially, passing output forward."""
        current_input = initial_input
        self.results = []

        print(f"🚀 Pipeline '{self.name}' starting ({len(self.stages)} stages)")

        for stage_name, stage_func in self.stages:
            result = await self._run_stage(stage_name, stage_func, current_input)
            self.results.append(result)

            if result.status == StageStatus.FAILED:
                print(f"❌ Pipeline failed at stage: {stage_name}")
                if self.config.notify_on_failure:
                    await self._notify(f"❌ {self.name} failed at {stage_name}: {result.error}")
                break

            current_input = result.output
            print(f"✅ {stage_name} completed ({result.duration_seconds:.1f}s)")

        else:
            # All stages completed successfully
            total_time = sum(r.duration_seconds for r in self.results)
            print(f"🎉 Pipeline '{self.name}' completed in {total_time:.1f}s")
            if self.config.notify_on_completion:
                await self._notify(f"✅ {self.name} completed ({total_time:.0f}s)")

        return self.results

    async def _run_stage(self, name: str, func: Callable, input_data: Any) -> StageResult:
        """Run a single stage with retry logic."""
        retries = 0

        while retries <= self.config.max_retries:
            start = time.monotonic()
            try:
                output = await func(input_data)
                return StageResult(
                    stage_name=name,
                    status=StageStatus.COMPLETED,
                    output=output,
                    duration_seconds=time.monotonic() - start,
                    retries=retries,
                )
            except Exception as e:
                retries += 1
                if retries > self.config.max_retries:
                    return StageResult(
                        stage_name=name,
                        status=StageStatus.FAILED,
                        error=str(e),
                        duration_seconds=time.monotonic() - start,
                        retries=retries - 1,
                    )

                delay = self.config.retry_delay_seconds * (2 ** (retries - 1))
                print(f"⚠️ {name} failed (attempt {retries}), retrying in {delay}s...")
                await asyncio.sleep(delay)

    async def _notify(self, message: str):
        """Send notification via Telegram (placeholder)."""
        # In production: await telegram_notifier.send(message)
        print(f"📤 Notification: {message}")


# ─── Usage Example ───

async def example_pipeline():
    """Example: Video production pipeline."""

    async def research(topic):
        # Claude API call for topic research
        return {"topic": topic, "outline": ["intro", "main", "conclusion"]}

    async def generate_script(research_data):
        # Claude Opus for script writing
        return {"script": "Full video script...", "word_count": 2000}

    async def generate_voice(script_data):
        # TTS API call
        return {"audio_path": "/output/voice.mp3", "duration": 480}

    async def compose_video(voice_data):
        # FFmpeg video composition
        return {"video_path": "/output/final.mp4", "duration": 480}

    async def upload(video_data):
        # YouTube API upload
        return {"video_id": "abc123", "url": "https://youtube.com/watch?v=abc123"}

    # Build and run pipeline
    pipeline = PipelineOrchestrator("longform-video")
    pipeline.add_stage("research", research)
    pipeline.add_stage("script", generate_script)
    pipeline.add_stage("voice", generate_voice)
    pipeline.add_stage("compose", compose_video)
    pipeline.add_stage("upload", upload)

    results = await pipeline.run("AI Investment Strategies 2025")
    return results

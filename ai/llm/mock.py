"""
NEXUS TITAN — Mock LLM Provider
Transparent, labeled mock provider for testing and offline environments.
Adheres strictly to Article II (No Fake AI) of the Engineering Constitution.
"""

import time
from typing import AsyncIterator, List, Optional
from ai.llm.base import LLMProvider
from ai.runtime.schema import AIRequest, AIResponse


class MockLLMProvider(LLMProvider):
    """
    Simulated provider that clearly tags all responses as [MOCK_PROVIDER / DEMO_MODE].
    Provides deterministic completions and synthetic embeddings for testing pipelines.
    """

    def __init__(self, latency_seconds: float = 0.01):
        self._latency = latency_seconds

    @property
    def provider_name(self) -> str:
        return "mock_provider"

    @property
    def is_mock(self) -> bool:
        return True

    async def generate(self, request: AIRequest) -> AIResponse:
        start_time = time.perf_counter()
        
        # Transparent mock notification prefix
        mock_output = (
            f"[MOCK_PROVIDER / DEMO_MODE] Model '{request.model}' processed prompt: "
            f"'{request.prompt[:60]}...' (deterministic test output)"
        )
        
        # Approximate token counts based on whitespace splitting
        input_tokens = len(request.prompt.split()) + (len(request.system_prompt.split()) if request.system_prompt else 0)
        output_tokens = len(mock_output.split())
        
        latency_ms = (time.perf_counter() - start_time + self._latency) * 1000.0

        return AIResponse(
            request_id=request.request_id,
            model=request.model,
            text=mock_output,
            finish_reason="stop",
            latency_ms=round(latency_ms, 2),
            input_tokens=input_tokens,
            output_tokens=output_tokens,
            is_mock=True,
            tools_used=request.tools_requested,
        )

    async def stream(self, request: AIRequest) -> AsyncIterator[str]:
        tokens = [
            "[MOCK_PROVIDER / DEMO_MODE] ",
            "Streaming ",
            "response ",
            "for: ",
            request.prompt[:30],
        ]
        for token in tokens:
            yield token

    async def embed(self, texts: List[str], model: Optional[str] = None) -> List[List[float]]:
        """
        Produces synthetic 128-dimensional deterministic embeddings for pipeline tests.
        """
        embeddings = []
        for text in texts:
            # Deterministic hash-based 128-dim vector
            seed = sum(ord(c) for c in text)
            vec = [float((seed + i) % 100) / 100.0 for i in range(128)]
            # Normalize vector
            norm = sum(x * x for x in vec) ** 0.5
            embeddings.append([x / norm for x in vec] if norm > 0 else vec)
        return embeddings

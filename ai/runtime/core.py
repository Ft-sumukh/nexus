"""
NEXUS TITAN — Central AI Runtime Orchestrator
Coordinates request validation, model routing, telemetry tracking, and tool availability.
"""

import time
import logging
from typing import AsyncIterator, Dict, List, Optional
from ai.runtime.schema import AIRequest, AIResponse, TelemetryTrace
from ai.llm.base import LLMProvider
from ai.tools.registry import ToolRegistry

logger = logging.getLogger("nexus.titan.ai_runtime")


class AIRuntime:
    """
    Central operational boundary for AI applications.
    Coordinates providers, tools, and telemetry.
    """

    def __init__(self, default_provider: LLMProvider, tool_registry: Optional[ToolRegistry] = None):
        self._providers: Dict[str, LLMProvider] = {default_provider.provider_name: default_provider}
        self._default_provider_name = default_provider.provider_name
        self._tool_registry = tool_registry or ToolRegistry()
        self._traces: List[TelemetryTrace] = []

    def register_provider(self, provider: LLMProvider, is_default: bool = False) -> None:
        """Registers a new LLM provider backend."""
        self._providers[provider.provider_name] = provider
        if is_default:
            self._default_provider_name = provider.provider_name

    def get_provider(self, name: Optional[str] = None) -> LLMProvider:
        """Retrieves a provider by name or returns the default provider."""
        provider_name = name or self._default_provider_name
        if provider_name not in self._providers:
            raise KeyError(f"LLM Provider '{provider_name}' is not registered in AI Runtime.")
        return self._providers[provider_name]

    @property
    def tool_registry(self) -> ToolRegistry:
        return self._tool_registry

    @property
    def traces(self) -> List[TelemetryTrace]:
        return list(self._traces)

    async def execute(self, request: AIRequest, provider_name: Optional[str] = None) -> AIResponse:
        """
        Executes an AI request with end-to-end telemetry and validation.
        """
        provider = self.get_provider(provider_name)
        start_time = time.perf_counter()
        error_msg: Optional[str] = None

        try:
            # Verify requested tools exist in registry
            for tool_name in request.tools_requested:
                if not self._tool_registry.get(tool_name):
                    logger.warning(f"Request {request.request_id}: Requested tool '{tool_name}' not found.")

            response = await provider.generate(request)
            return response
        except Exception as e:
            error_msg = str(e)
            logger.error(f"AI Runtime execution error on request {request.request_id}: {e}")
            raise
        finally:
            duration_ms = (time.perf_counter() - start_time) * 1000.0
            trace = TelemetryTrace(
                request_id=request.request_id,
                model=request.model,
                duration_ms=round(duration_ms, 2),
                input_tokens=len(request.prompt.split()),
                output_tokens=0,
                error=error_msg,
                hardware_mode="CPU_ONLY"
            )
            self._traces.append(trace)

    async def stream(self, request: AIRequest, provider_name: Optional[str] = None) -> AsyncIterator[str]:
        """
        Streams responses from the selected provider.
        """
        provider = self.get_provider(provider_name)
        async for chunk in provider.stream(request):
            yield chunk

"""
NEXUS TITAN — Central AI Runtime Orchestrator
Coordinates request validation, model routing, pipeline stages, telemetry, and tool availability.
"""

from typing import AsyncIterator, Dict, List, Optional
from ai.runtime.schema import (
    AIRequest,
    AIResponse,
    ModelMetadata,
    ModelCapability,
    TelemetryTrace,
    RuntimeMetricsSnapshot
)
from ai.runtime.router import ModelRouter
from ai.runtime.prompts import PromptRegistry
from ai.runtime.telemetry import (
    TelemetrySink,
    InMemoryTelemetrySink,
    FileTelemetrySink,
    CompositeTelemetrySink,
    RuntimeMetricsAggregator
)
from ai.runtime.pipeline import (
    PipelineOrchestrator,
    RequestValidationStage,
    ModelRoutingStage,
    ContextPreparationStage,
    ToolAvailabilityStage,
    InferenceStage,
    ResponseValidationStage,
    TelemetryTraceStage
)
from ai.llm.base import LLMProvider
from ai.tools.registry import ToolRegistry


class AIRuntime:
    """
    Central operational boundary for AI applications in NEXUS TITAN.
    Orchestrates the 7-stage request pipeline, model routing, prompt templates,
    and structured telemetry emission.
    """

    def __init__(
        self,
        default_provider: LLMProvider,
        tool_registry: Optional[ToolRegistry] = None,
        telemetry_sink: Optional[TelemetrySink] = None,
        trace_log_path: str = "logs/traces/ai_traces.jsonl"
    ):
        self._providers: Dict[str, LLMProvider] = {default_provider.provider_name: default_provider}
        self._default_provider_name = default_provider.provider_name
        self._tool_registry = tool_registry or ToolRegistry()
        self._router = ModelRouter(default_model_id="mock-model-v1")
        self._prompt_registry = PromptRegistry()

        # Telemetry Sink setup (in-memory buffer + optional file persistence)
        in_memory_sink = InMemoryTelemetrySink(max_capacity=1000)
        file_sink = FileTelemetrySink(filepath=trace_log_path)
        self._telemetry_sink = telemetry_sink or CompositeTelemetrySink([in_memory_sink, file_sink])
        self._metrics_aggregator = RuntimeMetricsAggregator(self._telemetry_sink)

        # Register default mock models in router
        self._router.register_model(
            ModelMetadata(
                model_id="mock-fast-v1",
                provider_name=default_provider.provider_name,
                capabilities=[ModelCapability.FAST],
                context_window=4096,
                is_mock=True,
                description="Fast mock model for latency-sensitive queries"
            ),
            is_default=True
        )
        self._router.register_model(
            ModelMetadata(
                model_id="mock-reasoning-v1",
                provider_name=default_provider.provider_name,
                capabilities=[ModelCapability.COMPLEX_REASONING],
                context_window=16384,
                is_mock=True,
                description="Reasoning-optimized mock model for complex systems analysis"
            ),
            fallback_model_id="mock-fast-v1"
        )

        # Construct 7-stage pipeline
        self._build_pipeline()

    def _build_pipeline(self) -> None:
        stages = [
            RequestValidationStage(),
            ModelRoutingStage(self._router, self._providers),
            ContextPreparationStage(self._prompt_registry),
            ToolAvailabilityStage(self._tool_registry),
            InferenceStage(),
            ResponseValidationStage(),
            TelemetryTraceStage(self._telemetry_sink),
        ]
        self._pipeline = PipelineOrchestrator(stages)

    def register_provider(self, provider: LLMProvider, is_default: bool = False) -> None:
        """Registers a new LLM provider backend."""
        self._providers[provider.provider_name] = provider
        if is_default:
            self._default_provider_name = provider.provider_name
        self._build_pipeline()

    def get_provider(self, name: Optional[str] = None) -> LLMProvider:
        """Retrieves a provider by name or returns default."""
        provider_name = name or self._default_provider_name
        if provider_name not in self._providers:
            raise KeyError(f"LLM Provider '{provider_name}' is not registered.")
        return self._providers[provider_name]

    @property
    def router(self) -> ModelRouter:
        return self._router

    @property
    def prompt_registry(self) -> PromptRegistry:
        return self._prompt_registry

    @property
    def tool_registry(self) -> ToolRegistry:
        return self._tool_registry

    @property
    def telemetry_sink(self) -> TelemetrySink:
        return self._telemetry_sink

    @property
    def metrics(self) -> RuntimeMetricsSnapshot:
        return self._metrics_aggregator.snapshot()

    @property
    def traces(self) -> List[TelemetryTrace]:
        return self._telemetry_sink.get_traces(limit=100)

    async def execute(self, request: AIRequest) -> AIResponse:
        """
        Executes an AI request through the 7-stage pipeline.
        """
        return await self._pipeline.execute(request)

    async def stream(self, request: AIRequest, provider_name: Optional[str] = None) -> AsyncIterator[str]:
        """
        Streams completions directly from the resolved provider.
        """
        decision = self._router.resolve(request)
        provider = self.get_provider(provider_name or decision.provider_name)
        async for chunk in provider.stream(request):
            yield chunk

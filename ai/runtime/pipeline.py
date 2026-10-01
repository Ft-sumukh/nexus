"""
NEXUS TITAN — 7-Stage Request Pipeline Orchestrator
Executes AI requests through sequential, observable stages.
Adheres strictly to Section 10 of the Master Specification.
"""

from abc import ABC, abstractmethod
import time
import logging
from typing import Any, Dict, List, Optional
from ai.runtime.schema import AIRequest, AIResponse, TelemetryTrace
from ai.runtime.router import ModelRouter, RoutingDecision
from ai.runtime.prompts import PromptRegistry
from ai.runtime.telemetry import TelemetrySink
from ai.tools.registry import ToolRegistry
from ai.llm.base import LLMProvider

logger = logging.getLogger("nexus.titan.pipeline")


class PipelineContext:
    """
    Mutable state passed sequentially through pipeline stages.
    """

    def __init__(self, request: AIRequest):
        self.request = request
        self.routing_decision: Optional[RoutingDecision] = None
        self.provider: Optional[LLMProvider] = None
        self.fallback_provider: Optional[LLMProvider] = None
        self.resolved_prompt: str = request.prompt
        self.resolved_system_prompt: Optional[str] = request.system_prompt
        self.tools_verified: List[str] = []
        self.response: Optional[AIResponse] = None
        self.error: Optional[str] = None
        self.fallback_used: bool = False
        self.timings_ms: Dict[str, float] = {}
        self.start_time: float = time.perf_counter()


class PipelineStage(ABC):
    """
    Abstract stage in the sequential request processing pipeline.
    """

    @property
    @abstractmethod
    def name(self) -> str:
        pass

    @abstractmethod
    async def process(self, context: PipelineContext) -> None:
        pass


class RequestValidationStage(PipelineStage):
    """
    Stage 1: Defensive validation of prompt size, constraints, and execution budget.
    """
    @property
    def name(self) -> str:
        return "1_validation"

    async def process(self, context: PipelineContext) -> None:
        req = context.request
        if not req.prompt.strip():
            raise ValueError("Prompt cannot be empty or solely whitespace.")
        if req.max_tokens < 1 or req.max_tokens > 32768:
            raise ValueError(f"Invalid max_tokens constraint: {req.max_tokens}")
        if req.execution_budget_ms and req.execution_budget_ms < 10.0:
            raise ValueError(f"Execution budget too low: {req.execution_budget_ms}ms")


class ModelRoutingStage(PipelineStage):
    """
    Stage 2: Determines optimal model and provider using ModelRouter.
    """
    def __init__(self, router: ModelRouter, providers: Dict[str, LLMProvider]):
        self._router = router
        self._providers = providers

    @property
    def name(self) -> str:
        return "2_routing"

    async def process(self, context: PipelineContext) -> None:
        decision = self._router.resolve(context.request)
        context.routing_decision = decision

        # Resolve primary provider
        prov = self._providers.get(decision.provider_name)
        if not prov and "mock_provider" in self._providers:
            prov = self._providers["mock_provider"]
        if not prov:
            raise KeyError(f"No active provider matching '{decision.provider_name}'")
        context.provider = prov

        # Resolve fallback provider if configured
        if decision.fallback_model_id:
            fallback_meta = self._router.get_model(decision.fallback_model_id)
            if fallback_meta:
                context.fallback_provider = self._providers.get(fallback_meta.provider_name)


class ContextPreparationStage(PipelineStage):
    """
    Stage 3: Applies versioned prompt templates and context variable interpolation.
    """
    def __init__(self, prompt_registry: PromptRegistry):
        self._prompt_registry = prompt_registry

    @property
    def name(self) -> str:
        return "3_context"

    async def process(self, context: PipelineContext) -> None:
        req = context.request
        if req.prompt_version and ":" in req.prompt_version:
            tmpl_name, tmpl_ver = req.prompt_version.split(":", 1)
            tmpl = self._prompt_registry.get(tmpl_name, tmpl_ver)
            if tmpl:
                context.resolved_prompt = tmpl.format(req.context_variables)
                if tmpl.system_prompt and not req.system_prompt:
                    context.resolved_system_prompt = tmpl.system_prompt


class ToolAvailabilityStage(PipelineStage):
    """
    Stage 4: Verifies availability and permissions of requested tools.
    """
    def __init__(self, tool_registry: ToolRegistry):
        self._tool_registry = tool_registry

    @property
    def name(self) -> str:
        return "4_tools"

    async def process(self, context: PipelineContext) -> None:
        for tool_name in context.request.tools_requested:
            tool = self._tool_registry.get(tool_name)
            if tool:
                context.tools_verified.append(tool.name)
            else:
                logger.warning(
                    f"Request {context.request.request_id}: Tool '{tool_name}' not found in registry."
                )


class InferenceStage(PipelineStage):
    """
    Stage 5: Executes inference with automated fallback on provider failure.
    """
    @property
    def name(self) -> str:
        return "5_inference"

    async def process(self, context: PipelineContext) -> None:
        # Create invocation request with resolved prompt
        inv_request = context.request.model_copy(
            update={
                "prompt": context.resolved_prompt,
                "system_prompt": context.resolved_system_prompt,
                "model": context.routing_decision.model_id if context.routing_decision else context.request.model
            }
        )

        try:
            assert context.provider is not None
            response = await context.provider.generate(inv_request)
            context.response = response
        except Exception as primary_err:
            logger.warning(
                f"Primary provider failed for request {context.request.request_id}: {primary_err}. Attempting fallback..."
            )
            if context.fallback_provider and context.routing_decision and context.routing_decision.fallback_model_id:
                fallback_req = inv_request.model_copy(
                    update={"model": context.routing_decision.fallback_model_id}
                )
                response = await context.fallback_provider.generate(fallback_req)
                response.fallback_used = True
                context.fallback_used = True
                context.response = response
            else:
                context.error = str(primary_err)
                raise


class ResponseValidationStage(PipelineStage):
    """
    Stage 6: Validates response integrity and attaches routing metadata.
    """
    @property
    def name(self) -> str:
        return "6_validation"

    async def process(self, context: PipelineContext) -> None:
        if not context.response:
            raise RuntimeError("Inference stage completed without generating a response.")

        resp = context.response
        resp.prompt_version = context.request.prompt_version
        resp.provider_name = context.provider.provider_name if context.provider else "unknown"
        resp.tools_used = context.tools_verified
        resp.fallback_used = context.fallback_used


class TelemetryTraceStage(PipelineStage):
    """
    Stage 7: Collects per-stage metrics and emits structured trace to sink.
    """
    def __init__(self, sink: TelemetrySink):
        self._sink = sink

    @property
    def name(self) -> str:
        return "7_telemetry"

    async def process(self, context: PipelineContext) -> None:
        total_duration_ms = (time.perf_counter() - context.start_time) * 1000.0

        if context.response:
            context.response.pipeline_timings_ms = dict(context.timings_ms)

        trace = TelemetryTrace(
            request_id=context.request.request_id,
            model=context.response.model if context.response else context.request.model,
            provider_name=context.provider.provider_name if context.provider else "unknown",
            prompt_version=context.request.prompt_version,
            duration_ms=round(total_duration_ms, 2),
            input_tokens=context.response.input_tokens if context.response else len(context.request.prompt.split()),
            output_tokens=context.response.output_tokens if context.response else 0,
            cost_usd=context.response.cost_usd if (context.response and context.response.cost_usd) else 0.0,
            fallback_used=context.fallback_used,
            pipeline_timings_ms=dict(context.timings_ms),
            error=context.error,
            hardware_mode="CPU_ONLY"
        )
        self._sink.record(trace)


class PipelineOrchestrator:
    """
    Sequentially runs requests through all 7 pipeline stages with per-stage latency tracking.
    """

    def __init__(self, stages: List[PipelineStage]):
        self._stages = stages

    async def execute(self, request: AIRequest) -> AIResponse:
        context = PipelineContext(request)

        for stage in self._stages:
            stage_start = time.perf_counter()
            try:
                await stage.process(context)
            except Exception as e:
                context.error = str(e)
                context.timings_ms[stage.name] = round((time.perf_counter() - stage_start) * 1000.0, 2)
                # Ensure telemetry stage runs even on failure
                for final_stage in self._stages:
                    if isinstance(final_stage, TelemetryTraceStage):
                        await final_stage.process(context)
                raise
            finally:
                context.timings_ms[stage.name] = round((time.perf_counter() - stage_start) * 1000.0, 2)

        assert context.response is not None
        return context.response

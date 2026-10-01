import pytest
from typing import AsyncIterator, List, Optional
from ai.runtime.schema import (
    AIRequest,
    ModelCapability,
    ModelMetadata,
    RoutingPreference
)
from ai.runtime.router import ModelRouter
from ai.runtime.prompts import PromptTemplate, PromptRegistry
from ai.runtime.telemetry import InMemoryTelemetrySink
from ai.tools.base import Tool
from ai.tools.registry import ToolRegistry
from ai.llm.base import LLMProvider
from ai.llm.mock import MockLLMProvider
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
from pydantic import BaseModel


class FailingProvider(LLMProvider):
    """Provider designed to raise an error to test fallback behavior."""
    @property
    def provider_name(self) -> str:
        return "failing_provider"

    @property
    def is_mock(self) -> bool:
        return True

    async def generate(self, request: AIRequest):
        raise ConnectionError("Primary provider backend connection dropped.")

    async def stream(self, request: AIRequest) -> AsyncIterator[str]:
        yield "error"

    async def embed(self, texts: List[str], model: Optional[str] = None):
        return [[0.0]]


class DummyInput(BaseModel):
    query: str


class DummyTool(Tool):
    @property
    def name(self) -> str:
        return "dummy_search"

    @property
    def description(self) -> str:
        return "Search tool"

    @property
    def input_model(self):
        return DummyInput

    async def execute(self, params: DummyInput):
        return {"status": "ok"}


@pytest.fixture
def pipeline_setup():
    mock_prov = MockLLMProvider()
    failing_prov = FailingProvider()
    providers = {
        mock_prov.provider_name: mock_prov,
        failing_prov.provider_name: failing_prov
    }

    router = ModelRouter(default_model_id="fast-v1")
    router.register_model(
        ModelMetadata(
            model_id="fast-v1",
            provider_name=mock_prov.provider_name,
            capabilities=[ModelCapability.FAST],
            is_mock=True
        ),
        is_default=True
    )
    router.register_model(
        ModelMetadata(
            model_id="fragile-v1",
            provider_name=failing_prov.provider_name,
            capabilities=[ModelCapability.COMPLEX_REASONING],
            is_mock=True
        ),
        fallback_model_id="fast-v1"
    )

    prompt_reg = PromptRegistry()
    prompt_reg.register(
        PromptTemplate(
            name="sys_check",
            version="1.0.0",
            template_str="Check node {node_id} status for user {user}.",
            system_prompt="Monitor systems status."
        )
    )

    tool_reg = ToolRegistry()
    tool_reg.register(DummyTool())

    sink = InMemoryTelemetrySink()

    stages = [
        RequestValidationStage(),
        ModelRoutingStage(router, providers),
        ContextPreparationStage(prompt_reg),
        ToolAvailabilityStage(tool_reg),
        InferenceStage(),
        ResponseValidationStage(),
        TelemetryTraceStage(sink),
    ]
    orchestrator = PipelineOrchestrator(stages)

    return orchestrator, sink


@pytest.mark.asyncio
async def test_full_7_stage_pipeline_success(pipeline_setup):
    orchestrator, sink = pipeline_setup

    req = AIRequest(
        prompt="Execute systems check",
        prompt_version="sys_check:1.0.0",
        context_variables={"node_id": "titan-01", "user": "admin"},
        tools_requested=["dummy_search"]
    )

    response = await orchestrator.execute(req)

    # 1. Verification of output
    assert response.request_id == req.request_id
    assert response.prompt_version == "sys_check:1.0.0"
    assert "titan-01" in response.text
    assert "dummy_search" in response.tools_used
    assert response.fallback_used is False

    # 2. Verification of stage timing breakdown
    timings = response.pipeline_timings_ms
    assert "1_validation" in timings
    assert "2_routing" in timings
    assert "3_context" in timings
    assert "4_tools" in timings
    assert "5_inference" in timings
    assert "6_validation" in timings

    # 3. Verification of trace emission
    traces = sink.get_traces()
    assert len(traces) == 1
    assert traces[0].request_id == req.request_id
    assert traces[0].error is None


@pytest.mark.asyncio
async def test_pipeline_fallback_on_primary_failure(pipeline_setup):
    orchestrator, sink = pipeline_setup

    # Explicitly request fragile model which fails on primary inference
    req = AIRequest(
        prompt="Analyze complex race condition",
        model="fragile-v1"
    )

    response = await orchestrator.execute(req)

    # Fallback to fast-v1 should have occurred seamlessly
    assert response.fallback_used is True
    assert response.model == "fast-v1"
    assert "[MOCK_PROVIDER / DEMO_MODE]" in response.text

    traces = sink.get_traces()
    assert len(traces) == 1
    assert traces[0].fallback_used is True
    assert traces[0].error is None


@pytest.mark.asyncio
async def test_pipeline_validation_stage_failure(pipeline_setup):
    orchestrator, sink = pipeline_setup

    req = AIRequest(prompt="   ")  # Empty prompt

    with pytest.raises(ValueError, match="Prompt cannot be empty"):
        await orchestrator.execute(req)

    # Telemetry should capture the error trace
    traces = sink.get_traces()
    assert len(traces) == 1
    assert "Prompt cannot be empty" in str(traces[0].error)

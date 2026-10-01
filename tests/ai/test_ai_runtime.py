import pytest
from ai.runtime.schema import AIRequest, RoutingPreference
from ai.runtime.core import AIRuntime
from ai.runtime.prompts import PromptTemplate
from ai.llm.mock import MockLLMProvider


@pytest.mark.asyncio
async def test_ai_runtime_execution_with_mock_provider():
    mock_provider = MockLLMProvider(latency_seconds=0.005)
    runtime = AIRuntime(default_provider=mock_provider)

    request = AIRequest(
        prompt="Analyze memory access patterns in matrix multiplication.",
        model="titan-mock-v1"
    )

    response = await runtime.execute(request)

    # Verification of response attributes
    assert response.request_id == request.request_id
    assert response.is_mock is True
    assert "[MOCK_PROVIDER / DEMO_MODE]" in response.text
    assert response.latency_ms >= 5.0
    assert response.input_tokens > 0
    assert response.output_tokens > 0
    assert "5_inference" in response.pipeline_timings_ms

    # Verification of recorded telemetry trace
    assert len(runtime.traces) == 1
    trace = runtime.traces[0]
    assert trace.request_id == request.request_id
    assert trace.hardware_mode == "CPU_ONLY"
    assert trace.error is None


@pytest.mark.asyncio
async def test_ai_runtime_streaming():
    mock_provider = MockLLMProvider()
    runtime = AIRuntime(default_provider=mock_provider)

    request = AIRequest(prompt="Stream test prompt", model="titan-mock-v1")
    chunks = []
    async for chunk in runtime.stream(request):
        chunks.append(chunk)

    assert len(chunks) > 0
    combined = "".join(chunks)
    assert "[MOCK_PROVIDER / DEMO_MODE]" in combined


@pytest.mark.asyncio
async def test_mock_embeddings():
    mock_provider = MockLLMProvider()
    texts = ["matrix multiplication", "cache coherence"]
    vectors = await mock_provider.embed(texts)

    assert len(vectors) == 2
    assert len(vectors[0]) == 128
    assert len(vectors[1]) == 128
    assert sum(abs(x) for x in vectors[0]) > 0


@pytest.mark.asyncio
async def test_ai_runtime_with_prompt_templates_and_metrics():
    mock_provider = MockLLMProvider(latency_seconds=0.002)
    runtime = AIRuntime(default_provider=mock_provider)

    # Register template
    runtime.prompt_registry.register(
        PromptTemplate(
            name="cache_analysis",
            version="1.0.0",
            template_str="Analyze L1 cache hit rate on processor {cpu_model} under workload {workload}."
        )
    )

    request = AIRequest(
        prompt="Placeholder",
        prompt_version="cache_analysis:1.0.0",
        context_variables={"cpu_model": "AMD Ryzen 9", "workload": "GEMM tiled"},
        routing_preference=RoutingPreference.FAST
    )

    response = await runtime.execute(request)
    assert "AMD Ryzen 9" in response.text
    assert "GEMM tiled" in response.text

    # Verify metrics snapshot
    metrics = runtime.metrics
    assert metrics.total_requests >= 1
    assert metrics.successful_requests >= 1
    assert metrics.failed_requests == 0
    assert metrics.avg_latency_ms > 0

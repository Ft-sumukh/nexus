import pytest
from ai.runtime.schema import AIRequest
from ai.runtime.core import AIRuntime
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
    assert response.model == "titan-mock-v1"
    assert response.is_mock is True
    assert "[MOCK_PROVIDER / DEMO_MODE]" in response.text
    assert response.latency_ms >= 5.0
    assert response.input_tokens > 0
    assert response.output_tokens > 0

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
    # Vectors should be non-zero
    assert sum(abs(x) for x in vectors[0]) > 0

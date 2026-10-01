import pytest
from ai.runtime.router import ModelRouter
from ai.runtime.schema import AIRequest, ModelCapability, ModelMetadata, RoutingPreference


@pytest.fixture
def configured_router():
    router = ModelRouter(default_model_id="fast-model")
    router.register_model(
        ModelMetadata(
            model_id="fast-model",
            provider_name="mock_provider",
            capabilities=[ModelCapability.FAST],
            is_mock=True
        ),
        is_default=True
    )
    router.register_model(
        ModelMetadata(
            model_id="reasoning-model",
            provider_name="mock_provider",
            capabilities=[ModelCapability.COMPLEX_REASONING],
            is_mock=True
        ),
        fallback_model_id="fast-model"
    )
    router.register_model(
        ModelMetadata(
            model_id="local-model",
            provider_name="mock_provider",
            capabilities=[ModelCapability.LOCAL_PRIVATE],
            is_local=True,
            is_mock=True
        )
    )
    return router


def test_explicit_model_routing(configured_router):
    req = AIRequest(prompt="Hello world", model="reasoning-model")
    decision = configured_router.resolve(req)

    assert decision.model_id == "reasoning-model"
    assert decision.fallback_model_id == "fast-model"
    assert "Explicit" in decision.reason


def test_preference_fast_routing(configured_router):
    req = AIRequest(
        prompt="Tell me a joke",
        routing_preference=RoutingPreference.FAST
    )
    decision = configured_router.resolve(req)

    assert decision.model_id == "fast-model"
    assert "FAST" in decision.reason


def test_preference_complex_routing(configured_router):
    req = AIRequest(
        prompt="Explain quantum entanglement",
        routing_preference=RoutingPreference.COMPLEX
    )
    decision = configured_router.resolve(req)

    assert decision.model_id == "reasoning-model"
    assert "COMPLEX" in decision.reason


def test_auto_heuristic_complex_keyword_routing(configured_router):
    req = AIRequest(
        prompt="Benchmark matrix multiplication and measure cache coherence",
        routing_preference=RoutingPreference.AUTO
    )
    decision = configured_router.resolve(req)

    assert decision.model_id == "reasoning-model"
    assert "AUTO heuristic" in decision.reason


def test_auto_heuristic_simple_prompt_routing(configured_router):
    req = AIRequest(
        prompt="What is the capital of France?",
        routing_preference=RoutingPreference.AUTO
    )
    decision = configured_router.resolve(req)

    assert decision.model_id == "fast-model"

"""
NEXUS TITAN — Configurable Model Router
Implements capability-based, rule-based, and fallback routing policies.
Adheres to Section 12 of the Master Specification.
"""

from typing import Dict, List, Optional
from pydantic import BaseModel
from ai.runtime.schema import AIRequest, ModelCapability, ModelMetadata, RoutingPreference


class RoutingDecision(BaseModel):
    """
    Result of a model routing determination.
    """
    model_id: str
    provider_name: str
    reason: str
    fallback_model_id: Optional[str] = None


class ModelRouter:
    """
    Routes AI requests to the optimal model based on prompt characteristics,
    declared capabilities, explicit user hints, and fallback policies.
    """

    # Keywords triggering complex reasoning route under AUTO mode
    COMPLEX_KEYWORDS = {
        "benchmark", "research", "analyze", "architecture", "optimization",
        "mathematics", "theorem", "concurrency", "deadlock", "algorithm",
        "numerical", "profiling", "coalescing", "cache coherence"
    }

    def __init__(self, default_model_id: str = "mock-model-v1"):
        self._models: Dict[str, ModelMetadata] = {}
        self._default_model_id = default_model_id
        self._fallbacks: Dict[str, str] = {}

    def register_model(
        self,
        metadata: ModelMetadata,
        fallback_model_id: Optional[str] = None,
        is_default: bool = False
    ) -> None:
        """Registers a model metadata entry and optional fallback."""
        self._models[metadata.model_id] = metadata
        if fallback_model_id:
            self._fallbacks[metadata.model_id] = fallback_model_id
        if is_default:
            self._default_model_id = metadata.model_id

    def get_model(self, model_id: str) -> Optional[ModelMetadata]:
        return self._models.get(model_id)

    def list_models(self) -> List[ModelMetadata]:
        return list(self._models.values())

    def get_fallback(self, model_id: str) -> Optional[ModelMetadata]:
        fallback_id = self._fallbacks.get(model_id)
        if fallback_id and fallback_id in self._models:
            return self._models[fallback_id]
        if self._default_model_id in self._models and self._default_model_id != model_id:
            return self._models[self._default_model_id]
        return None

    def resolve(self, request: AIRequest) -> RoutingDecision:
        """
        Resolves the appropriate model for an incoming request.
        """
        # 1. Exact model requested and present
        if request.model in self._models:
            meta = self._models[request.model]
            return RoutingDecision(
                model_id=meta.model_id,
                provider_name=meta.provider_name,
                reason="Explicit model ID requested by client",
                fallback_model_id=self._fallbacks.get(meta.model_id)
            )

        # 2. Preference: FAST
        if request.routing_preference == RoutingPreference.FAST:
            for meta in self._models.values():
                if ModelCapability.FAST in meta.capabilities:
                    return RoutingDecision(
                        model_id=meta.model_id,
                        provider_name=meta.provider_name,
                        reason="Routing preference: FAST",
                        fallback_model_id=self._fallbacks.get(meta.model_id)
                    )

        # 3. Preference: COMPLEX
        if request.routing_preference == RoutingPreference.COMPLEX:
            for meta in self._models.values():
                if ModelCapability.COMPLEX_REASONING in meta.capabilities:
                    return RoutingDecision(
                        model_id=meta.model_id,
                        provider_name=meta.provider_name,
                        reason="Routing preference: COMPLEX_REASONING",
                        fallback_model_id=self._fallbacks.get(meta.model_id)
                    )

        # 4. Preference: LOCAL
        if request.routing_preference == RoutingPreference.LOCAL:
            for meta in self._models.values():
                if meta.is_local or ModelCapability.LOCAL_PRIVATE in meta.capabilities:
                    return RoutingDecision(
                        model_id=meta.model_id,
                        provider_name=meta.provider_name,
                        reason="Routing preference: LOCAL_PRIVATE",
                        fallback_model_id=self._fallbacks.get(meta.model_id)
                    )

        # 5. AUTO heuristic routing
        prompt_lower = request.prompt.lower()
        word_count = len(request.prompt.split())

        is_complex = (
            word_count > 150 or
            any(kw in prompt_lower for kw in self.COMPLEX_KEYWORDS)
        )

        if is_complex:
            for meta in self._models.values():
                if ModelCapability.COMPLEX_REASONING in meta.capabilities:
                    return RoutingDecision(
                        model_id=meta.model_id,
                        provider_name=meta.provider_name,
                        reason=f"AUTO heuristic: complex workload detected (words={word_count})",
                        fallback_model_id=self._fallbacks.get(meta.model_id)
                    )

        # Fallback to default registered model
        if self._default_model_id in self._models:
            meta = self._models[self._default_model_id]
            return RoutingDecision(
                model_id=meta.model_id,
                provider_name=meta.provider_name,
                reason="Default model fallback",
                fallback_model_id=self._fallbacks.get(meta.model_id)
            )

        # Safe fallback if registry is minimal
        return RoutingDecision(
            model_id=request.model,
            provider_name="default",
            reason="Unregistered model passthrough"
        )

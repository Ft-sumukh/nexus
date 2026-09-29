"""
NEXUS TITAN — LLM Provider Abstraction
Base interface for remote, local, and mock LLM backends.
"""

from abc import ABC, abstractmethod
from typing import AsyncIterator, List, Optional
from ai.runtime.schema import AIRequest, AIResponse


class LLMProvider(ABC):
    """
    Abstract base class for all LLM providers.
    Prevents coupling core business and agent logic to any vendor-specific SDK.
    """

    @property
    @abstractmethod
    def provider_name(self) -> str:
        """Machine-readable name of the provider."""
        pass

    @property
    @abstractmethod
    def is_mock(self) -> bool:
        """True if the provider produces simulated or mock responses."""
        pass

    @abstractmethod
    async def generate(self, request: AIRequest) -> AIResponse:
        """
        Executes a single synchronous/turn completion.
        """
        pass

    @abstractmethod
    async def stream(self, request: AIRequest) -> AsyncIterator[str]:
        """
        Streams completion tokens asynchronously.
        """
        pass

    @abstractmethod
    async def embed(self, texts: List[str], model: Optional[str] = None) -> List[List[float]]:
        """
        Generates dense vector embeddings for input strings.
        """
        pass

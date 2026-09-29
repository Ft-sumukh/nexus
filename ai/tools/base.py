"""
NEXUS TITAN — Controlled Tool Abstraction
Enforces strict schemas, timeouts, and human-in-the-loop safety boundaries.
Adheres strictly to Article III (No Unsafe System Access) of the Engineering Constitution.
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, Type
from pydantic import BaseModel


class Tool(ABC):
    """
    Abstract base class for all tools accessible to AI agents.
    Every tool must define input schemas, mutation status, and timeout limits.
    """

    @property
    @abstractmethod
    def name(self) -> str:
        """Unique machine-readable tool identifier."""
        pass

    @property
    @abstractmethod
    def description(self) -> str:
        """Clear explanation of tool function for agent planning."""
        pass

    @property
    @abstractmethod
    def input_model(self) -> Type[BaseModel]:
        """Pydantic model validating input parameters."""
        pass

    @property
    def is_mutating(self) -> bool:
        """
        True if the tool alters state (filesystem, database, external API, processes).
        Mutating tools trigger approval gates.
        """
        return False

    @property
    def requires_approval(self) -> bool:
        """True if execution requires explicit human approval."""
        return self.is_mutating

    @property
    def timeout_seconds(self) -> float:
        """Maximum execution duration before forced cancellation."""
        return 30.0

    @abstractmethod
    async def execute(self, params: BaseModel) -> Dict[str, Any]:
        """
        Executes the tool with validated parameters.
        """
        pass

"""
NEXUS TITAN — Agent Finite State Machine
Explicit state representation and transition guards.
Prevents unbounded loops and enforces transparent state tracking.
"""

from enum import Enum
import time
from typing import Dict, List, Set


class AgentState(str, Enum):
    """
    Explicit, auditable states for AI agents in NEXUS TITAN.
    States are never hidden implicitly within LLM prompt text.
    """
    CREATED = "CREATED"
    PLANNING = "PLANNING"
    WAITING_FOR_TOOL = "WAITING_FOR_TOOL"
    EXECUTING = "EXECUTING"
    OBSERVING = "OBSERVING"
    WAITING_FOR_APPROVAL = "WAITING_FOR_APPROVAL"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"
    CANCELLED = "CANCELLED"


# Allowed state transitions matrix
VALID_TRANSITIONS: Dict[AgentState, Set[AgentState]] = {
    AgentState.CREATED: {AgentState.PLANNING, AgentState.CANCELLED, AgentState.FAILED},
    AgentState.PLANNING: {
        AgentState.WAITING_FOR_TOOL,
        AgentState.EXECUTING,
        AgentState.COMPLETED,
        AgentState.FAILED,
        AgentState.CANCELLED,
    },
    AgentState.WAITING_FOR_TOOL: {
        AgentState.WAITING_FOR_APPROVAL,
        AgentState.EXECUTING,
        AgentState.FAILED,
        AgentState.CANCELLED,
    },
    AgentState.WAITING_FOR_APPROVAL: {
        AgentState.EXECUTING,
        AgentState.CANCELLED,
        AgentState.FAILED,
    },
    AgentState.EXECUTING: {
        AgentState.OBSERVING,
        AgentState.FAILED,
        AgentState.CANCELLED,
    },
    AgentState.OBSERVING: {
        AgentState.PLANNING,
        AgentState.COMPLETED,
        AgentState.FAILED,
        AgentState.CANCELLED,
    },
    AgentState.COMPLETED: set(),  # Terminal state
    AgentState.FAILED: set(),     # Terminal state
    AgentState.CANCELLED: set(),  # Terminal state
}


class InvalidStateTransitionError(Exception):
    pass


class AgentStateMachine:
    """
    Guards and records agent lifecycle transitions.
    """

    def __init__(self, agent_id: str):
        self.agent_id = agent_id
        self._current_state = AgentState.CREATED
        self._history: List[Dict[str, any]] = [
            {"state": self._current_state, "timestamp": time.time(), "reason": "Initial creation"}
        ]

    @property
    def current_state(self) -> AgentState:
        return self._current_state

    @property
    def is_terminal(self) -> bool:
        return self._current_state in {AgentState.COMPLETED, AgentState.FAILED, AgentState.CANCELLED}

    @property
    def history(self) -> List[Dict[str, any]]:
        return list(self._history)

    def transition_to(self, new_state: AgentState, reason: str = "") -> None:
        """
        Transitions the agent to a new state if permitted by the transition matrix.
        """
        allowed = VALID_TRANSITIONS.get(self._current_state, set())
        if new_state not in allowed:
            raise InvalidStateTransitionError(
                f"Agent '{self.agent_id}': Cannot transition from {self._current_state.value} to {new_state.value}."
            )

        self._current_state = new_state
        self._history.append({
            "state": new_state,
            "timestamp": time.time(),
            "reason": reason
        })

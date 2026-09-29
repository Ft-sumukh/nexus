import pytest
from ai.agents.state import AgentState, AgentStateMachine, InvalidStateTransitionError


def test_agent_state_machine_valid_progression():
    machine = AgentStateMachine(agent_id="agt_001")
    assert machine.current_state == AgentState.CREATED
    assert machine.is_terminal is False

    # CREATED -> PLANNING
    machine.transition_to(AgentState.PLANNING, reason="Decomposing user goal")
    assert machine.current_state == AgentState.PLANNING

    # PLANNING -> WAITING_FOR_TOOL
    machine.transition_to(AgentState.WAITING_FOR_TOOL, reason="Selecting search tool")
    assert machine.current_state == AgentState.WAITING_FOR_TOOL

    # WAITING_FOR_TOOL -> EXECUTING
    machine.transition_to(AgentState.EXECUTING, reason="Executing query")
    assert machine.current_state == AgentState.EXECUTING

    # EXECUTING -> OBSERVING
    machine.transition_to(AgentState.OBSERVING, reason="Parsing output results")
    assert machine.current_state == AgentState.OBSERVING

    # OBSERVING -> COMPLETED
    machine.transition_to(AgentState.COMPLETED, reason="Goal satisfied")
    assert machine.current_state == AgentState.COMPLETED
    assert machine.is_terminal is True

    # History audit trail verification
    history = machine.history
    assert len(history) == 6  # Initial creation + 5 transitions
    assert history[-1]["state"] == AgentState.COMPLETED


def test_agent_state_machine_invalid_transition_rejected():
    machine = AgentStateMachine(agent_id="agt_002")

    # CREATED directly to COMPLETED is not allowed
    with pytest.raises(InvalidStateTransitionError):
        machine.transition_to(AgentState.COMPLETED)

    # Transition to PLANNING
    machine.transition_to(AgentState.PLANNING)

    # PLANNING directly to OBSERVING without EXECUTING is not allowed
    with pytest.raises(InvalidStateTransitionError):
        machine.transition_to(AgentState.OBSERVING)


def test_terminal_states_prevent_further_transitions():
    machine = AgentStateMachine(agent_id="agt_003")
    machine.transition_to(AgentState.CANCELLED, reason="Cancelled by user")

    assert machine.is_terminal is True
    with pytest.raises(InvalidStateTransitionError):
        machine.transition_to(AgentState.PLANNING)

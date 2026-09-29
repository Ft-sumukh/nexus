"""
NEXUS TITAN — Tool Registry
Centralized repository for discovering and securely executing tools.
"""

from typing import Any, Dict, List, Optional
from pydantic import ValidationError
from ai.tools.base import Tool


class ToolExecutionError(Exception):
    pass


class ApprovalRequiredError(ToolExecutionError):
    pass


class ToolRegistry:
    """
    Manages tool registration, input validation, permission checking, and dispatch.
    """

    def __init__(self):
        self._tools: Dict[str, Tool] = {}

    def register(self, tool: Tool) -> None:
        """Registers a tool in the registry."""
        if tool.name in self._tools:
            raise ValueError(f"Tool with name '{tool.name}' is already registered.")
        self._tools[tool.name] = tool

    def get(self, name: str) -> Optional[Tool]:
        """Retrieves a registered tool by name."""
        return self._tools.get(name)

    def list_tools(self) -> List[Dict[str, Any]]:
        """Returns metadata descriptors for all registered tools."""
        descriptors = []
        for tool in self._tools.values():
            descriptors.append({
                "name": tool.name,
                "description": tool.description,
                "input_schema": tool.input_model.model_json_schema(),
                "is_mutating": tool.is_mutating,
                "requires_approval": tool.requires_approval,
                "timeout_seconds": tool.timeout_seconds,
            })
        return descriptors

    async def execute(
        self,
        name: str,
        raw_params: Dict[str, Any],
        approved: bool = False
    ) -> Dict[str, Any]:
        """
        Validates parameters and executes the tool under permission checks.
        """
        tool = self.get(name)
        if not tool:
            raise ToolExecutionError(f"Tool '{name}' not found in registry.")

        if tool.requires_approval and not approved:
            raise ApprovalRequiredError(
                f"Tool '{name}' is a privileged or mutating operation requiring human approval."
            )

        # Validate input against tool's Pydantic model
        try:
            validated_params = tool.input_model.model_validate(raw_params)
        except ValidationError as e:
            raise ToolExecutionError(f"Parameter validation failed for tool '{name}': {e}") from e

        return await tool.execute(validated_params)

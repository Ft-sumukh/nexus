import pytest
from typing import Any, Dict, Type
from pydantic import BaseModel, Field
from ai.tools.base import Tool
from ai.tools.registry import ToolRegistry, ToolExecutionError, ApprovalRequiredError


class CalculatorInput(BaseModel):
    a: float = Field(..., description="First operand")
    b: float = Field(..., description="Second operand")
    operation: str = Field(..., description="add, sub, mul, div")


class CalculatorTool(Tool):
    @property
    def name(self) -> str:
        return "calculator"

    @property
    def description(self) -> str:
        return "Executes basic arithmetic operations"

    @property
    def input_model(self) -> Type[BaseModel]:
        return CalculatorInput

    async def execute(self, params: CalculatorInput) -> Dict[str, Any]:
        if params.operation == "add":
            res = params.a + params.b
        elif params.operation == "sub":
            res = params.a - params.b
        elif params.operation == "mul":
            res = params.a * params.b
        elif params.operation == "div":
            if params.b == 0:
                raise ValueError("Division by zero")
            res = params.a / params.b
        else:
            raise ValueError(f"Unknown operation: {params.operation}")
        return {"result": res}


class DeleteFileInput(BaseModel):
    filepath: str


class MutatingDeleteTool(Tool):
    @property
    def name(self) -> str:
        return "file_delete"

    @property
    def description(self) -> str:
        return "Deletes a file (mutating, privileged)"

    @property
    def input_model(self) -> Type[BaseModel]:
        return DeleteFileInput

    @property
    def is_mutating(self) -> bool:
        return True

    async def execute(self, params: DeleteFileInput) -> Dict[str, Any]:
        return {"deleted": params.filepath}


@pytest.mark.asyncio
async def test_tool_registry_and_execution():
    registry = ToolRegistry()
    calc = CalculatorTool()
    registry.register(calc)

    # Listed tools descriptor check
    tools = registry.list_tools()
    assert len(tools) == 1
    assert tools[0]["name"] == "calculator"
    assert tools[0]["is_mutating"] is False

    # Successful execution
    out = await registry.execute("calculator", {"a": 15, "b": 27, "operation": "add"})
    assert out["result"] == 42


@pytest.mark.asyncio
async def test_mutating_tool_approval_gate():
    registry = ToolRegistry()
    del_tool = MutatingDeleteTool()
    registry.register(del_tool)

    # Attempt execution without approval -> MUST raise ApprovalRequiredError
    with pytest.raises(ApprovalRequiredError):
        await registry.execute("file_delete", {"filepath": "/tmp/test.txt"}, approved=False)

    # Approved execution -> succeeds
    out = await registry.execute("file_delete", {"filepath": "/tmp/test.txt"}, approved=True)
    assert out["deleted"] == "/tmp/test.txt"


@pytest.mark.asyncio
async def test_invalid_parameters_fail_validation():
    registry = ToolRegistry()
    calc = CalculatorTool()
    registry.register(calc)

    with pytest.raises(ToolExecutionError):
        # Missing 'b' and 'operation'
        await registry.execute("calculator", {"a": 10})

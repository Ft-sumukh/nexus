"""
NEXUS TITAN — High-Level API Server
FastAPI entry point bridging user interfaces, AI runtime, and systems telemetry.
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import time
import os
import subprocess
import json

from ai.runtime.schema import AIRequest, AIResponse
from ai.runtime.core import AIRuntime
from ai.llm.mock import MockLLMProvider
from ai.tools.registry import ToolRegistry

app = FastAPI(
    title="NEXUS TITAN API",
    description="AI Systems, Runtime & High-Performance Computing Laboratory API",
    version="0.1.0"
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global foundational runtime instance with transparent mock provider for testing
_mock_provider = MockLLMProvider()
_tool_registry = ToolRegistry()
ai_runtime = AIRuntime(default_provider=_mock_provider, tool_registry=_tool_registry)


@app.get("/health")
async def health_check():
    """
    Standard health check endpoint.
    """
    return {
        "status": "healthy",
        "service": "nexus-titan-api",
        "version": "0.1.0",
        "hardware_mode": "CPU_ONLY",
        "timestamp": time.time(),
    }


@app.get("/telemetry/hardware")
async def get_hardware_telemetry():
    """
    Returns verified host hardware diagnostics.
    Attempts to read from the compiled C++ titan::HardwareProbe executable or falls back to OS probing.
    """
    exe_path = os.path.join(os.path.dirname(__file__), "..", "..", "build", "systems", "test_hardware_probe.exe")
    exe_path = os.path.abspath(exe_path)

    if os.path.exists(exe_path):
        try:
            res = subprocess.run([exe_path], capture_output=True, text=True, timeout=5)
            return {
                "source": "titan_hardware_probe_cpp",
                "output": res.stdout,
                "exit_code": res.returncode,
                "cuda_available": False,
                "mode": "CPU_ONLY"
            }
        except Exception as e:
            return {"error": f"Failed executing hardware probe executable: {e}"}

    # Fallback Python OS inspect
    import multiprocessing
    return {
        "source": "python_os_probe_fallback",
        "logical_cores": multiprocessing.cpu_count(),
        "cuda_available": False,
        "mode": "CPU_ONLY"
    }


@app.get("/ai/v1/tools")
async def list_available_tools():
    """
    Lists all registered AI tools with schemas and permissions.
    """
    return {
        "tools": ai_runtime.tool_registry.list_tools()
    }


@app.post("/ai/v1/runtime/execute", response_model=AIResponse)
async def execute_ai_request(request: AIRequest):
    """
    Executes an AI request through the central AI runtime.
    """
    try:
        response = await ai_runtime.execute(request)
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

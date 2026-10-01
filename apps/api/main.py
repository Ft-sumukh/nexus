"""
NEXUS TITAN — High-Level API Server
FastAPI entry point bridging user interfaces, AI runtime, model routing, and systems telemetry.
"""

from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
import time
import os
import subprocess
from typing import List, Optional

from ai.runtime.schema import (
    AIRequest,
    AIResponse,
    ModelMetadata,
    TelemetryTrace,
    RuntimeMetricsSnapshot
)
from ai.runtime.core import AIRuntime
from ai.llm.mock import MockLLMProvider
from ai.tools.registry import ToolRegistry
from ai.runtime.prompts import PromptTemplate

app = FastAPI(
    title="NEXUS TITAN API",
    description="AI Systems, Runtime & High-Performance Computing Laboratory API",
    version="0.2.0"
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

# Register foundational prompt templates
ai_runtime.prompt_registry.register(
    PromptTemplate(
        name="system_diagnosis",
        version="1.0.0",
        template_str="Analyze the following system anomaly on host '{hostname}':\nError Log: {log_excerpt}\nSuggest potential root causes.",
        system_prompt="You are an expert systems performance engineer analyzing telemetry.",
        description="Diagnoses operating-system and hardware anomalies from log excerpts."
    )
)
ai_runtime.prompt_registry.register(
    PromptTemplate(
        name="benchmark_analysis",
        version="1.0.0",
        template_str="Algorithm '{algorithm_name}' executed on input size {input_size}.\nSingle-thread runtime: {cpu_ms} ms, Multi-thread: {parallel_ms} ms, GPU: {gpu_ms} ms.\nExplain where time was spent.",
        system_prompt="You are an expert high-performance computing performance analyst.",
        description="Analyzes computational benchmark speedup and memory bottlenecks."
    )
)


@app.get("/health")
async def health_check():
    """
    Standard health check endpoint.
    """
    return {
        "status": "healthy",
        "service": "nexus-titan-api",
        "version": "0.2.0",
        "hardware_mode": "CPU_ONLY",
        "timestamp": time.time(),
    }


@app.get("/telemetry/hardware")
async def get_hardware_telemetry():
    """
    Returns verified host hardware diagnostics.
    Invokes the compiled C++ titan::HardwareProbe executable or falls back to Python OS inspect.
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

    import multiprocessing
    return {
        "source": "python_os_probe_fallback",
        "logical_cores": multiprocessing.cpu_count(),
        "cuda_available": False,
        "mode": "CPU_ONLY"
    }


@app.get("/ai/v1/models", response_model=List[ModelMetadata])
async def list_available_models():
    """
    Lists all models registered in the model router along with capabilities.
    """
    return ai_runtime.router.list_models()


@app.get("/ai/v1/tools")
async def list_available_tools():
    """
    Lists all registered AI tools with schemas and permissions.
    """
    return {
        "tools": ai_runtime.tool_registry.list_tools()
    }


@app.get("/ai/v1/prompts")
async def list_prompt_templates():
    """
    Lists all registered versioned prompt templates.
    """
    return {
        "templates": [t.model_dump() for t in ai_runtime.prompt_registry.list_templates()]
    }


@app.post("/ai/v1/runtime/execute", response_model=AIResponse)
async def execute_ai_request(request: AIRequest):
    """
    Executes an AI request through the 7-stage pipeline.
    """
    try:
        response = await ai_runtime.execute(request)
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/ai/v1/runtime/traces", response_model=List[TelemetryTrace])
async def get_runtime_traces(
    limit: int = Query(default=50, ge=1, le=500),
    model: Optional[str] = Query(default=None)
):
    """
    Queries recent telemetry traces emitted by the AI runtime pipeline.
    """
    return ai_runtime.telemetry_sink.get_traces(limit=limit, model=model)


@app.get("/ai/v1/runtime/metrics", response_model=RuntimeMetricsSnapshot)
async def get_runtime_metrics():
    """
    Returns real-time aggregated operational metrics (latency, tokens, error rates).
    """
    return ai_runtime.metrics

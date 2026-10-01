"""
NEXUS TITAN — AI Runtime Schemas
Defines structured request, response, telemetry, model metadata, and metrics contracts.
"""

from enum import Enum
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field
import uuid
import time


class ModelCapability(str, Enum):
    """
    Classifies model capabilities for dynamic routing.
    """
    FAST = "FAST"
    COMPLEX_REASONING = "COMPLEX_REASONING"
    EMBEDDING = "EMBEDDING"
    LOCAL_PRIVATE = "LOCAL_PRIVATE"


class RoutingPreference(str, Enum):
    """
    User or system preference for model routing.
    """
    AUTO = "AUTO"
    FAST = "FAST"
    COMPLEX = "COMPLEX"
    LOCAL = "LOCAL"


class ModelMetadata(BaseModel):
    """
    Metadata describing an available model backend.
    """
    model_id: str
    provider_name: str
    capabilities: List[ModelCapability] = Field(default_factory=list)
    context_window: int = 8192
    cost_per_1k_input_usd: float = 0.0
    cost_per_1k_output_usd: float = 0.0
    is_local: bool = False
    is_mock: bool = True
    description: str = ""


class AIRequest(BaseModel):
    """
    Standardized AI request received by the orchestrator.
    """
    request_id: str = Field(default_factory=lambda: f"req_{uuid.uuid4().hex[:12]}")
    prompt: str = Field(..., min_length=1, description="Primary user or task prompt")
    system_prompt: Optional[str] = Field(default=None, description="System instruction prompt")
    model: str = Field(default="mock-model-v1", description="Requested model identifier or routing alias")
    prompt_version: Optional[str] = Field(default=None, description="Version tag of the prompt template used")
    routing_preference: RoutingPreference = Field(
        default=RoutingPreference.AUTO,
        description="Routing policy hint"
    )
    temperature: float = Field(default=0.7, ge=0.0, le=2.0)
    max_tokens: int = Field(default=1024, ge=1, le=32768)
    execution_budget_ms: Optional[float] = Field(default=30000.0, ge=100.0, description="Max execution budget")
    tools_requested: List[str] = Field(default_factory=list, description="List of tools requested for the turn")
    context_variables: Dict[str, Any] = Field(default_factory=dict, description="Variables for template interpolation")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Contextual tracing metadata")
    created_at: float = Field(default_factory=time.time)


class AIResponse(BaseModel):
    """
    Standardized AI response emitted by the orchestrator with full telemetry and stage diagnostics.
    """
    request_id: str
    model: str
    provider_name: str = "unknown"
    prompt_version: Optional[str] = None
    text: str
    finish_reason: str = "stop"
    latency_ms: float
    input_tokens: int
    output_tokens: int
    tools_used: List[str] = Field(default_factory=list)
    citations: List[Dict[str, Any]] = Field(default_factory=list)
    cost_usd: Optional[float] = 0.0
    is_mock: bool = False
    fallback_used: bool = False
    pipeline_timings_ms: Dict[str, float] = Field(
        default_factory=dict,
        description="Detailed latency breakdown across pipeline stages"
    )
    timestamp: float = Field(default_factory=time.time)


class TelemetryTrace(BaseModel):
    """
    Telemetry trace record stored for MLOps observability, audit trails, and evaluation.
    """
    trace_id: str = Field(default_factory=lambda: f"trc_{uuid.uuid4().hex[:12]}")
    request_id: str
    model: str
    provider_name: str = "unknown"
    prompt_version: Optional[str] = None
    duration_ms: float
    input_tokens: int
    output_tokens: int
    cost_usd: float = 0.0
    fallback_used: bool = False
    pipeline_timings_ms: Dict[str, float] = Field(default_factory=dict)
    error: Optional[str] = None
    hardware_mode: str = "CPU_ONLY"
    timestamp: float = Field(default_factory=time.time)


class RuntimeMetricsSnapshot(BaseModel):
    """
    Aggregated operational performance snapshot.
    """
    total_requests: int
    successful_requests: int
    failed_requests: int
    fallback_requests: int
    total_input_tokens: int
    total_output_tokens: int
    avg_latency_ms: float
    p95_latency_ms: float
    total_cost_usd: float
    hardware_mode: str = "CPU_ONLY"
    timestamp: float = Field(default_factory=time.time)

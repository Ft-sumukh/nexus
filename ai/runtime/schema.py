"""
NEXUS TITAN — AI Runtime Schemas
Defines structured request, response, and telemetry contracts.
"""

from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field
import uuid
import time


class AIRequest(BaseModel):
    """
    Standardized AI request received by the orchestrator.
    """
    request_id: str = Field(default_factory=lambda: f"req_{uuid.uuid4().hex[:12]}")
    prompt: str = Field(..., min_length=1, description="Primary user or task prompt")
    system_prompt: Optional[str] = Field(default=None, description="System instruction prompt")
    model: str = Field(default="mock-model-v1", description="Requested model identifier")
    temperature: float = Field(default=0.7, ge=0.0, le=2.0)
    max_tokens: int = Field(default=1024, ge=1, le=32768)
    tools_requested: List[str] = Field(default_factory=list, description="List of tools requested for the turn")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Contextual tracing metadata")
    created_at: float = Field(default_factory=time.time)


class AIResponse(BaseModel):
    """
    Standardized AI response emitted by the orchestrator with full telemetry.
    """
    request_id: str
    model: str
    text: str
    finish_reason: str = "stop"
    latency_ms: float
    input_tokens: int
    output_tokens: int
    tools_used: List[str] = Field(default_factory=list)
    citations: List[Dict[str, Any]] = Field(default_factory=list)
    cost_usd: Optional[float] = None
    is_mock: bool = False
    timestamp: float = Field(default_factory=time.time)


class TelemetryTrace(BaseModel):
    """
    Telemetry trace record stored for MLOps observability and evaluation.
    """
    trace_id: str = Field(default_factory=lambda: f"trc_{uuid.uuid4().hex[:12]}")
    request_id: str
    model: str
    duration_ms: float
    input_tokens: int
    output_tokens: int
    error: Optional[str] = None
    hardware_mode: str = "CPU_ONLY"
    timestamp: float = Field(default_factory=time.time)

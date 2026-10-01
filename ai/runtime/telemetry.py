"""
NEXUS TITAN — Telemetry Sinks & Metrics Aggregator
Captures structured execution traces, persists to JSONL, and calculates runtime metrics.
"""

from abc import ABC, abstractmethod
import json
import os
import threading
from typing import List, Optional
from ai.runtime.schema import TelemetryTrace, RuntimeMetricsSnapshot


class TelemetrySink(ABC):
    """
    Abstract sink destination for telemetry trace emission.
    """

    @abstractmethod
    def record(self, trace: TelemetryTrace) -> None:
        """Records a single telemetry trace."""
        pass

    @abstractmethod
    def get_traces(self, limit: int = 100, model: Optional[str] = None) -> List[TelemetryTrace]:
        """Queries recorded traces."""
        pass


class InMemoryTelemetrySink(TelemetrySink):
    """
    Thread-safe in-memory ring buffer for telemetry traces.
    """

    def __init__(self, max_capacity: int = 1000):
        self._max_capacity = max_capacity
        self._traces: List[TelemetryTrace] = []
        self._lock = threading.Lock()

    def record(self, trace: TelemetryTrace) -> None:
        with self._lock:
            if len(self._traces) >= self._max_capacity:
                self._traces.pop(0)
            self._traces.append(trace)

    def get_traces(self, limit: int = 100, model: Optional[str] = None) -> List[TelemetryTrace]:
        with self._lock:
            matching = [
                t for t in self._traces
                if model is None or t.model == model
            ]
            return list(reversed(matching[-limit:]))


class FileTelemetrySink(TelemetrySink):
    """
    Appends traces as JSONL lines for durable audit trails.
    """

    def __init__(self, filepath: str = "logs/traces/ai_traces.jsonl"):
        self._filepath = os.path.abspath(filepath)
        os.makedirs(os.path.dirname(self._filepath), exist_ok=True)
        self._lock = threading.Lock()

    def record(self, trace: TelemetryTrace) -> None:
        line = trace.model_dump_json() + "\n"
        with self._lock:
            with open(self._filepath, "a", encoding="utf-8") as f:
                f.write(line)

    def get_traces(self, limit: int = 100, model: Optional[str] = None) -> List[TelemetryTrace]:
        if not os.path.exists(self._filepath):
            return []
        traces = []
        with self._lock:
            with open(self._filepath, "r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if not line:
                        continue
                    try:
                        t = TelemetryTrace.model_validate_json(line)
                        if model is None or t.model == model:
                            traces.append(t)
                    except Exception:
                        continue
        return list(reversed(traces[-limit:]))


class CompositeTelemetrySink(TelemetrySink):
    """
    Broadcasts telemetry traces to multiple sink destinations.
    """

    def __init__(self, sinks: List[TelemetrySink]):
        self._sinks = sinks

    def record(self, trace: TelemetryTrace) -> None:
        for sink in self._sinks:
            sink.record(trace)

    def get_traces(self, limit: int = 100, model: Optional[str] = None) -> List[TelemetryTrace]:
        if self._sinks:
            return self._sinks[0].get_traces(limit, model)
        return []


class RuntimeMetricsAggregator:
    """
    Calculates operational health and latency metrics across telemetry traces.
    """

    def __init__(self, sink: TelemetrySink):
        self._sink = sink

    def snapshot(self) -> RuntimeMetricsSnapshot:
        traces = self._sink.get_traces(limit=1000)

        total_requests = len(traces)
        if total_requests == 0:
            return RuntimeMetricsSnapshot(
                total_requests=0,
                successful_requests=0,
                failed_requests=0,
                fallback_requests=0,
                total_input_tokens=0,
                total_output_tokens=0,
                avg_latency_ms=0.0,
                p95_latency_ms=0.0,
                total_cost_usd=0.0,
                hardware_mode="CPU_ONLY"
            )

        failed = sum(1 for t in traces if t.error is not None)
        successful = total_requests - failed
        fallbacks = sum(1 for t in traces if t.fallback_used)
        total_in_tok = sum(t.input_tokens for t in traces)
        total_out_tok = sum(t.output_tokens for t in traces)
        total_cost = sum(t.cost_usd for t in traces)

        latencies = sorted([t.duration_ms for t in traces])
        avg_lat = sum(latencies) / len(latencies)

        # Calculate p95 index
        p95_idx = int(len(latencies) * 0.95)
        p95_lat = latencies[min(p95_idx, len(latencies) - 1)]

        return RuntimeMetricsSnapshot(
            total_requests=total_requests,
            successful_requests=successful,
            failed_requests=failed,
            fallback_requests=fallbacks,
            total_input_tokens=total_in_tok,
            total_output_tokens=total_out_tok,
            avg_latency_ms=round(avg_lat, 2),
            p95_latency_ms=round(p95_lat, 2),
            total_cost_usd=round(total_cost, 4),
            hardware_mode=traces[0].hardware_mode if traces else "CPU_ONLY"
        )

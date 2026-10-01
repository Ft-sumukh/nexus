import pytest
import os
import tempfile
from ai.runtime.schema import TelemetryTrace
from ai.runtime.telemetry import (
    InMemoryTelemetrySink,
    FileTelemetrySink,
    RuntimeMetricsAggregator
)


def test_in_memory_telemetry_sink():
    sink = InMemoryTelemetrySink(max_capacity=3)

    for i in range(5):
        sink.record(
            TelemetryTrace(
                request_id=f"req_{i}",
                model="mock-v1",
                duration_ms=10.0 * (i + 1),
                input_tokens=10,
                output_tokens=20
            )
        )

    # Should retain only the latest 3 items due to max_capacity=3
    traces = sink.get_traces()
    assert len(traces) == 3
    assert traces[0].request_id == "req_4"
    assert traces[1].request_id == "req_3"
    assert traces[2].request_id == "req_2"


def test_file_telemetry_sink_roundtrip():
    with tempfile.TemporaryDirectory() as tmpdir:
        filepath = os.path.join(tmpdir, "traces.jsonl")
        sink = FileTelemetrySink(filepath=filepath)

        trace = TelemetryTrace(
            request_id="req_test_01",
            model="mock-fast-v1",
            duration_ms=14.5,
            input_tokens=5,
            output_tokens=15,
            cost_usd=0.0001
        )
        sink.record(trace)

        # Read back
        traces = sink.get_traces()
        assert len(traces) == 1
        assert traces[0].request_id == "req_test_01"
        assert traces[0].duration_ms == 14.5
        assert traces[0].cost_usd == 0.0001


def test_runtime_metrics_aggregator():
    sink = InMemoryTelemetrySink(max_capacity=100)
    aggregator = RuntimeMetricsAggregator(sink)

    # Empty snapshot check
    empty_snap = aggregator.snapshot()
    assert empty_snap.total_requests == 0
    assert empty_snap.avg_latency_ms == 0.0

    # Record 4 traces
    latencies = [10.0, 20.0, 30.0, 100.0]
    for i, lat in enumerate(latencies):
        sink.record(
            TelemetryTrace(
                request_id=f"req_{i}",
                model="mock-v1",
                duration_ms=lat,
                input_tokens=10,
                output_tokens=20,
                error="Sample error" if i == 3 else None,
                fallback_used=True if i == 2 else False
            )
        )

    snap = aggregator.snapshot()
    assert snap.total_requests == 4
    assert snap.successful_requests == 3
    assert snap.failed_requests == 1
    assert snap.fallback_requests == 1
    assert snap.total_input_tokens == 40
    assert snap.total_output_tokens == 80
    assert snap.avg_latency_ms == 40.0
    assert snap.p95_latency_ms >= 100.0

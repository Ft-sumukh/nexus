import pytest
import httpx
from apps.api.main import app


@pytest.mark.asyncio
async def test_fastapi_health():
    transport = httpx.ASGITransport(app=app)
    async with httpx.AsyncClient(transport=transport, base_url="http://test") as client:
        resp = await client.get("/health")
        assert resp.status_code == 200
        data = resp.json()
        assert data["status"] == "healthy"
        assert data["service"] == "nexus-titan-api"
        assert data["hardware_mode"] == "CPU_ONLY"


@pytest.mark.asyncio
async def test_fastapi_models_and_prompts():
    transport = httpx.ASGITransport(app=app)
    async with httpx.AsyncClient(transport=transport, base_url="http://test") as client:
        # Check models
        models_resp = await client.get("/ai/v1/models")
        assert models_resp.status_code == 200
        models = models_resp.json()
        assert len(models) >= 2
        model_ids = [m["model_id"] for m in models]
        assert "mock-fast-v1" in model_ids
        assert "mock-reasoning-v1" in model_ids

        # Check prompt templates
        prompts_resp = await client.get("/ai/v1/prompts")
        assert prompts_resp.status_code == 200
        data = prompts_resp.json()
        assert "templates" in data
        names = [t["name"] for t in data["templates"]]
        assert "system_diagnosis" in names


@pytest.mark.asyncio
async def test_fastapi_execute_and_telemetry_flow():
    transport = httpx.ASGITransport(app=app)
    async with httpx.AsyncClient(transport=transport, base_url="http://test") as client:
        # Execute an AI request
        payload = {
            "prompt": "Benchmark algorithm throughput on input size 1000",
            "routing_preference": "FAST"
        }
        exec_resp = await client.post("/ai/v1/runtime/execute", json=payload)
        assert exec_resp.status_code == 200
        exec_data = exec_resp.json()
        assert exec_data["model"] == "mock-fast-v1"
        assert "5_inference" in exec_data["pipeline_timings_ms"]

        # Fetch traces
        traces_resp = await client.get("/ai/v1/runtime/traces")
        assert traces_resp.status_code == 200
        traces = traces_resp.json()
        assert len(traces) >= 1
        assert traces[0]["request_id"] == exec_data["request_id"]

        # Fetch metrics
        metrics_resp = await client.get("/ai/v1/runtime/metrics")
        assert metrics_resp.status_code == 200
        metrics = metrics_resp.json()
        assert metrics["total_requests"] >= 1
        assert metrics["successful_requests"] >= 1

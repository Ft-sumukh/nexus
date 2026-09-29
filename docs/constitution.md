# NEXUS TITAN — Engineering Constitution

**Document Version:** 1.0.0  
**Status:** Inviolable Project Law  
**Project:** NEXUS TITAN — AI Systems, Runtime & High-Performance Computing Laboratory  

---

## Preamble

NEXUS TITAN is an integrated engineering and research platform connecting high-level artificial intelligence applications to the underlying computing systems that execute them.

To maintain absolute technical integrity, scientific rigor, and production reliability, all contributors, AI agents, and systems engineers must abide by this Constitution.

---

## Article I: No Fake Performance

1. **Empirical Measurement Mandatory**: No performance metric (e.g. throughput, latency, memory footprint, cache misses, GPU speedup) may be reported unless it was measured directly on the host system executing actual benchmark code.
2. **Prohibited Claims**: The project strictly prohibits hardcoding unsubstantiated marketing claims (e.g., "10x faster", "50,000 req/sec", "99.9% accuracy", "zero latency") in source code, documentation, or user interfaces.
3. **Reproducibility Metadata**: Every benchmark result recorded by the platform must capture:
   - Unique Benchmark ID
   - Algorithm & Implementation variant (naive, optimized CPU, multithreaded CPU, GPU)
   - Input size and data characteristics
   - Host hardware specs (CPU model, physical/logical cores, RAM, GPU model, driver/compute capability)
   - Concurrency parameters (thread count, block/grid dimensions)
   - Wall-clock runtime, memory high-water mark, and speedup ratio
   - Git commit hash and timestamp

---

## Article II: No Fake AI

1. **Genuine Inference or Explicit Labeling**: When calling language models or embedding models, requests must pass to an actual inference runtime (remote API, local engine via llama.cpp/Ollama/PyTorch, or Hugging Face).
2. **Transparent Mock / Demo Mode**: In unit tests, offline environments, or when credentials are absent, the system may utilize mock providers. However, mock outputs must be explicitly tagged:
   ```text
   [MOCK_PROVIDER / DEMO_MODE]
   ```
   The user interface and API telemetry must explicitly notify the user that mock mode is active. Hardcoded responses pretending to be live generative reasoning are strictly forbidden.
3. **Citations & Evidence**: The RAG subsystem must never hallucinate or invent citations. If retrieved context is insufficient to answer a user prompt, the system must explicitly state that the available evidence is insufficient.

---

## Article III: No Unsafe System Access

1. **Controlled Tool Interfaces**: The AI agent runtime and LLM orchestrator must NEVER be granted direct, unconstrained access to host shells, operating-system processes, filesystem roots, network sockets, or raw database connections.
2. **Permission Boundaries & Sandboxing**: All tool invocations must adhere to a strict permission schema:
   - Tool name, description, input schema (Pydantic / Zod), and output schema
   - Mandatory execution timeout
   - Read-only vs. mutating classification
3. **Human-in-the-Loop for Privileged Actions**: Operations involving database mutations, file deletion, arbitrary shell/code execution, or network exfiltration must require explicit human approval before execution.
4. **Code Execution Sandboxing**: If code execution tools are provided, code must run in an isolated environment (container or sandbox) with strict memory, CPU, process count, and execution time limits.

---

## Article IV: Hardware-Aware Execution & CPU-Only Mode

1. **Universal CPU Fallback**: NEXUS TITAN must remain 100% buildable, testable, and runnable on systems lacking a dedicated GPU or CUDA toolchain.
2. **Explicit Capability Telemetry**: The platform must dynamically probe the host hardware at runtime. If CUDA is not detected:
   - CUDA features must be reported as `unavailable`.
   - CPU reference implementations must execute as fallback.
   - The user interface and telemetry must explicitly display `cuda_available: false`.
3. **CPU vs. GPU Equivalence Testing**: For every CUDA kernel, a mathematically identical CPU reference implementation must exist. Correctness must be numerically verified before comparing performance.

---

## Article V: Layer Isolation & Architecture Boundaries

1. **Three-Layer Separation**:
   - **Layer A (NEXUS — Intelligent Application Layer)**: Python & TypeScript. Orchestrates agents, RAG, tool calling, NLP, evaluation, and AI security.
   - **Layer B (TITAN — Systems Layer)**: Modern C++ (C++20). Implements process management, thread pools, memory allocators, CPU scheduling, synchronization, networking, and storage.
   - **Layer C (QUANTUM COMPUTE — High-Performance Computing)**: C++20 & CUDA. Implements algorithms, numerical computing, parallelism, and GPU acceleration.
2. **No Shortcut Implementations**: Low-level systems primitives (thread pools, memory allocators, bounded queues) must be implemented in C/C++, not simulated with Python standard library wrappers. Python acts as the high-level experiment coordinator.

---

## Article VI: Definition of Done & Incremental Progression

1. **Sequential Progression**: Development proceeds strictly phase-by-phase. No phase may be marked complete until all exit criteria are satisfied.
2. **Mandatory Exit Criteria for Every Phase**:
   - [ ] Working implementation committed to the repository
   - [ ] Automated tests added and passing (100% pass rate)
   - [ ] No compiler warnings under strict warning flags (`/W4` or `-Wall -Wextra`)
   - [ ] Architecture documentation updated
   - [ ] Real benchmark measurements recorded (where applicable)
   - [ ] Known limitations documented honestly
3. **Preservation of Working Code**: Never break, overwrite, or delete working components from prior phases without technical justification.

---

*Adopted by NEXUS TITAN Systems Architecture Team.*

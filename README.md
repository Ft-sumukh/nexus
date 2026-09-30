# NEXUS TITAN

### AI Systems, Runtime & High-Performance Computing Laboratory

> **NEXUS TITAN** is an integrated engineering and research platform exploring the complete journey from intelligent AI applications through AI runtime infrastructure, operating-system concepts, networking, storage, CPU execution, parallel computing, GPU acceleration, CUDA, and measurable system performance.

```text
AI Application ➔ AI Runtime ➔ Backend ➔ Operating System ➔ Networking ➔ Storage ➔ CPU ➔ Parallel Computing ➔ GPU / CUDA ➔ Measured Performance
```

[![C++20](https://img.shields.io/badge/C%2B%2B-20-00599C?logo=c%2B%2B&logoColor=white)](https://isocpp.org/)
[![CMake](https://img.shields.io/badge/CMake-3.25%2B-064F8C?logo=cmake&logoColor=white)](https://cmake.org/)
[![Python](https://img.shields.io/badge/Python-3.12%2B-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115%2B-009688?logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![Node.js](https://img.shields.io/badge/Node.js-%3E%3D20.0.0-339933?logo=node.js&logoColor=white)](https://nodejs.org/)
[![TypeScript](https://img.shields.io/badge/TypeScript-5.x-3178C6?logo=typescript&logoColor=white)](https://www.typescriptlang.org/)
[![Fastify](https://img.shields.io/badge/Fastify-5.x-000000?logo=fastify&logoColor=white)](https://www.fastify.io/)
[![Docker](https://img.shields.io/badge/Docker-Compose-2496ED?logo=docker&logoColor=white)](https://www.docker.com/)
[![License](https://img.shields.io/badge/License-Proprietary-red.svg)](#license)

---

## Table of Contents

1. [Project Overview](#project-overview)
2. [Project Philosophy & Constitution](#project-philosophy--constitution)
3. [System Architecture](#system-architecture)
4. [The Three Core Layers](#the-three-core-layers)
   * [Layer A — NEXUS (Intelligent Applications)](#layer-a--nexus-intelligent-applications)
   * [Layer B — TITAN (Systems Infrastructure)](#layer-b--titan-systems-infrastructure)
   * [Layer C — QUANTUM COMPUTE (High-Performance Computing)](#layer-c--quantum-compute-high-performance-computing)
5. [The Central Integration Story](#the-central-integration-story)
6. [Comprehensive Feature Matrix](#comprehensive-feature-matrix)
7. [AI Architecture & Runtime](#ai-architecture--runtime)
8. [Systems Architecture (TITAN)](#systems-architecture-titan)
9. [High-Performance Compute & Algorithms (QUANTUM)](#high-performance-compute--algorithms-quantum)
10. [Hardware-Aware Execution & CPU-Only Mode](#hardware-aware-execution--cpu-only-mode)
11. [Performance Engineering & Benchmark Methodology](#performance-engineering--benchmark-methodology)
12. [Profiling & Sanitizers](#profiling--sanitizers)
13. [Research Framework & Experimental Methodology](#research-framework--experimental-methodology)
14. [Technology Stack](#technology-stack)
15. [Repository Structure](#repository-structure)
16. [Installation & Prerequisites](#installation--prerequisites)
17. [Quick Start](#quick-start)
18. [Environment Configuration](#environment-configuration)
19. [Running the Application](#running-the-application)
20. [Docker Container Architecture](#docker-container-architecture)
21. [Automated Verification & Test Suites](#automated-verification--test-suites)
22. [CI/CD Pipeline](#cicd-pipeline)
23. [Security Architecture & Safe Tool Execution](#security-architecture--safe-tool-execution)
24. [Observability & Telemetry](#observability--telemetry)
25. [20-Phase Master Roadmap](#20-phase-master-roadmap)
26. [Current Project Status Dashboard](#current-project-status-dashboard)
27. [Known Limitations](#known-limitations)
28. [Troubleshooting Guide](#troubleshooting-guide)
29. [Documentation Map](#documentation-map)
30. [Code Quality & Contribution Guide](#code-quality--contribution-guide)
31. [License](#license)
32. [Author & Acknowledgements](#author--acknowledgements)

---

## Project Overview

### What is NEXUS TITAN?
**NEXUS TITAN** is an integrated software platform, systems laboratory, and empirical research environment designed to bridge the chasm between modern high-level artificial intelligence workflows and the low-level operating-system and hardware primitives that execute them.

Traditional AI curricula and frameworks treat computing systems as a black box: Python scripts invoke opaque remote APIs or heavily wrapped tensor libraries, obscuring process lifecycles, memory allocation strategies, thread scheduling, network framing, and hardware memory transfers. Conversely, traditional systems programming laboratories examine operating-system concepts (concurrency, paging, virtual memory, non-blocking I/O) in isolation, detached from modern data-intensive and agentic AI workloads.

NEXUS TITAN unifies these domains into a single, cohesive codebase. It allows an engineer or researcher to trace an operation end-to-end:
$$\text{User Request} \longrightarrow \text{Agent Decision} \longrightarrow \text{Controlled Tool Gate} \longrightarrow \text{C++ Runtime} \longrightarrow \text{CPU / CUDA Kernel} \longrightarrow \text{Empirical Telemetry} \longrightarrow \text{AI Synthesis}$$

### Why Does It Exist?
The project answers foundational, measurable engineering questions:
* **Knowledge Retrieval:** How does document chunking geometry and hybrid retrieval (dense semantic vectors + sparse BM25) impact retrieval recall, ranking latency, and context precision?
* **Tool Invocation:** How can LLM agent architectures safely call external tools without exposing host processes, filesystems, and network stacks to uncontrolled arbitrary execution?
* **Agent State Representation:** How can stateful agentic workflows be modeled as auditable finite state machines rather than opaque prompt loops?
* **Systems Execution:** How do process supervisors, worker thread pools, and bounded queues handle bursty, concurrent inference requests?
* **Memory & Hardware:** At what tensor dimensions does GPU acceleration overcome host-to-device PCIe transfer overhead? Where is the crossover between memory-bandwidth saturation and compute-bound throughput?
* **Measurement vs. Speculation:** How do we measure system performance with statistical rigor instead of relying on unverified claims?

### What NEXUS TITAN Is Not
* **NOT** a generic chatbot wrapper around third-party APIs.
* **NOT** a trivial Retrieval-Augmented Generation (RAG) toy demo.
* **NOT** a disconnected collection of academic C assignments or isolated CUDA samples.
* **NOT** a benchmark harness filled with hardcoded or simulated performance numbers.
* **NOT** an unconstrained autonomous agent granted raw shell access.

---

## Project Philosophy & Constitution

NEXUS TITAN operates under the inviolable rules defined in the [Engineering Constitution](docs/constitution.md):

```text
CORRECTNESS ➔ MEASUREMENT ➔ REPRODUCIBILITY ➔ SECURITY ➔ PERFORMANCE ➔ EXPLAINABILITY
```

### The Six Constitutional Laws

1. **Article I: No Fake Performance:** No performance claim (throughput, latency, memory footprint, cache misses, GPU speedup) may be reported unless it was measured directly on the host system executing actual benchmark code. Hardcoded marketing numbers (e.g. "10x faster", "99.9% accuracy", "50,000 req/sec") are strictly prohibited.
2. **Article II: No Fake AI:** When inference is requested, the system must invoke an actual model engine (remote API or local runtime). When running offline or in unit tests, mock providers must explicitly tag outputs with:
   ```text
   [MOCK_PROVIDER / DEMO_MODE]
   ```
   Simulating AI reasoning with hidden hardcoded strings is forbidden.
3. **Article III: No Unsafe System Access:** AI agents never receive raw, unconstrained access to host shells, operating-system processes, filesystem roots, or network sockets. Privileged actions require strict Pydantic schemas, permission categorization, and human-in-the-loop approval.
4. **Article IV: Hardware-Aware Execution & CPU-Only Mode:** The platform must build, test, and run reliably on CPU-only machines. When CUDA is absent, the system degrades gracefully to CPU reference implementations and honestly reports `cuda_available: false`.
5. **Article V: Layer Isolation & Architecture Boundaries:** Low-level systems primitives (thread pools, memory allocators, bounded queues) must be implemented in C/C++, not simulated with Python standard library wrappers. Python acts as the high-level orchestrator.
6. **Article VI: Incremental Verification:** Development proceeds phase-by-phase. No phase is complete without passing tests, honest documentation, and verifiable builds.

---

## System Architecture

The following diagram illustrates the complete conceptual architecture and dataflow across all three layers:

```mermaid
flowchart TD
    subgraph UI ["Presentation Layer"]
        User(["User / Engineer"]) --> WebApp["Web Application (React / Next.js)"]
        WebApp --> APIServer["API Server (FastAPI / Fastify Bridge)"]
    end

    subgraph LayerA ["Layer A — NEXUS (AI Application Infrastructure)"]
        APIServer --> AIOrch["AI Runtime Orchestrator"]
        AIOrch --> RAG["RAG Engine (Hybrid Search & Citations)"]
        AIOrch --> Tools["Controlled Tool Registry & Approval Gate"]
        AIOrch --> Agents["Agent Runtime (Finite State Machine)"]
        RAG --> LLMGateway["LLM Gateway (Provider Abstraction)"]
        Tools --> LLMGateway
        Agents --> LLMGateway
        LLMGateway --> RemoteProv["Remote Model Provider"]
        LLMGateway --> LocalProv["Local Inference Runtime"]
        LLMGateway --> MockProv["Transparent Mock Provider"]
    end

    subgraph LayerB ["Layer B — TITAN (Systems Infrastructure - C++20)"]
        Tools --> SysRuntime["Systems Runtime Interface"]
        SysRuntime --> ProcMgr["Process Supervisor (fork / exec / wait)"]
        SysRuntime --> ThreadPool["Thread Pool & Bounded Queue"]
        SysRuntime --> SchedSim["CPU Scheduler Simulator"]
        SysRuntime --> MemAlloc["Custom Memory Allocator"]
        SysRuntime --> NetEngine["Non-blocking Networking & Event Loop"]
        SysRuntime --> StorageEngine["Storage Engine (MemTable + WAL)"]
        SysRuntime --> HwProbe["Hardware Probe (CPUs / RAM / GPU)"]
    end

    subgraph LayerC ["Layer C — QUANTUM COMPUTE (High-Performance Computing)"]
        SysRuntime --> AlgoLab["Algorithm Laboratory (Graph, DP, Numerical)"]
        SysRuntime --> Benchmarks["Unified Benchmark Framework"]
        Benchmarks --> CPURef["CPU Reference & Parallel Kernels"]
        Benchmarks --> CUDAKernels["CUDA Acceleration Engine"]
    end

    subgraph TelemetryPipeline ["Observability & Feedback Loop"]
        HwProbe --> Telemetry["Structured Telemetry Collector"]
        Benchmarks --> Telemetry
        AIOrch --> Telemetry
        Telemetry --> Dashboard["Performance Dashboard & AI Explanation"]
        Dashboard --> User
    end

    classDef implemented fill:#2e7d32,stroke:#1b5e20,color:#ffffff;
    classDef partial fill:#f57f17,stroke:#e65100,color:#ffffff;
    classDef planned fill:#455a64,stroke:#263238,color:#ffffff;

    class HwProbe,MockProv,Tools,Agents,AIOrch,APIServer implemented;
    class SysRuntime,Benchmarks,CPURef,Telemetry partial;
    class RAG,RemoteProv,LocalProv,ProcMgr,ThreadPool,SchedSim,MemAlloc,NetEngine,StorageEngine,AlgoLab,CUDAKernels,Dashboard planned;
```

---

## The Three Core Layers

NEXUS TITAN is structurally divided into three interconnected layers:

### Layer A — NEXUS (Intelligent Applications)
* **Primary Languages:** Python 3.12+ & TypeScript 5.x
* **Core Components:**
  * **Central AI Runtime (`ai/runtime/`):** Manages request schemas ([`AIRequest`](file:///d:/week/nexus/ai/runtime/schema.py#L11-L22), [`AIResponse`](file:///d:/week/nexus/ai/runtime/schema.py#L25-L39)), model routing, token accounting, and latency telemetry.
  * **LLM Provider Abstraction (`ai/llm/`):** Clean [`LLMProvider`](file:///d:/week/nexus/ai/llm/base.py#L10-L40) abstract base class separating business logic from vendor SDKs; includes verified [`MockLLMProvider`](file:///d:/week/nexus/ai/llm/mock.py#L11-L68) for deterministic offline testing.
  * **Controlled Tool Registry (`ai/tools/`):** Tool base class enforcing Pydantic validation schemas, execution timeouts, and human approval gates on mutating operations.
  * **Agent State Machine (`ai/agents/`):** Finite state machine enforcing 9 explicit lifecycle states with transition validation and history audit logging.
  * **Future Modules (Planned):** RAG ingestion pipeline (Phase 4), automated retrieval evaluation (Phase 6), adversarial security test suite (Phase 7), and MLOps experiment tracking (Phase 8).

### Layer B — TITAN (Systems Infrastructure)
* **Primary Language:** Modern C++ (C++20) compiled via CMake & Ninja
* **Core Components:**
  * **Hardware Probe (`systems/runtime/`):** Dynamic host interrogation library ([`titan::HardwareProbe`](file:///d:/week/nexus/systems/runtime/include/titan/hardware_probe.hpp#L25-L38)) querying Windows Win32 APIs and POSIX sysconf to inspect physical cores, logical threads, RAM, and accelerator presence.
  * **Future Modules (Planned):** Process manager & supervisor with signal handling (Phase 9), production thread pool with condition variables and bounded work queue (Phase 9), CPU scheduling simulator (Phase 10), custom free-list memory allocator (Phase 11), virtual memory paging simulator (Phase 11), non-blocking network event loop (Phase 12), and key-value store with Write-Ahead Logging (Phase 13).

### Layer C — QUANTUM COMPUTE (High-Performance Computing)
* **Primary Languages:** C++20 (Multithreading / SIMD) and CUDA C++
* **Core Components:**
  * **Build System:** Root [`CMakeLists.txt`](file:///d:/week/nexus/CMakeLists.txt) probing for CUDA compiler via `check_language(CUDA)` and automatically compiling in CPU-Only Mode (`-DTITAN_CPU_ONLY=1`) when absent.
  * **Future Modules (Planned):** Graph and dynamic programming benchmark suite (Phase 14), parallel CPU algorithms validating Amdahl's Law (Phase 15), GPU kernels for GEMM, reductions, and prefix scans with mandatory CPU reference implementations (Phase 16), and unified benchmark framework (Phase 17).

---

## The Central Integration Story

The defining capability of NEXUS TITAN is connecting high-level AI reasoning with low-level systems execution:

```text
User: "Benchmark matrix multiplication for dimension N=2048."
   │
   ▼
1. AI Agent receives task and transitions state: CREATED ➔ PLANNING ➔ WAITING_FOR_TOOL
   │
   ▼
2. Tool Gate checks permissions: `benchmark_gemm` is non-mutating ➔ Approved
   │
   ▼
3. C++ Systems Runtime invokes compiled benchmark engine
   │
   ▼
4. Execution Engine runs:
   a. CPU Single-Threaded Reference Kernel
   b. CPU Multi-Threaded Parallel Kernel (OpenMP / std::thread)
   c. CUDA Kernel (if GPU present; otherwise flagged as UNAVAILABLE)
   │
   ▼
5. Systems Telemetry measures:
   - Host-to-Device transfer duration (ms)
   - Kernel computation duration (ms)
   - Device-to-Host transfer duration (ms)
   - Total wall-clock time and calculated GFLOPS
   - Speedup ratio over single-threaded baseline
   │
   ▼
6. AI Agent synthesizes results, identifies hardware bottleneck (e.g. transfer overhead vs compute), and formats analysis
   │
   ▼
7. Web Dashboard renders comparative performance scaling curve
```

*Implementation Status:* The architectural interfaces, tool registry, approval gates, and C++ hardware telemetry are **Implemented**. The end-to-end multi-kernel benchmark orchestration will be finalized in **Phase 18**.

---

## Comprehensive Feature Matrix

The following table provides an honest accounting of every major subsystem in the repository:

| Subsystem | Component | Description | Status | Reference Code / Docs |
|---|---|---|---|---|
| **Constitution** | Engineering Rules | Inviolable laws on performance, AI transparency, and security | ✅ Implemented | [`docs/constitution.md`](file:///d:/week/nexus/docs/constitution.md) |
| **Architecture** | Master Specification | 3-layer architecture, 20-phase roadmap, and computing stack | ✅ Implemented | [`docs/architecture.md`](file:///d:/week/nexus/docs/architecture.md), [`docs/roadmap.md`](file:///d:/week/nexus/docs/roadmap.md) |
| **Decisions** | ADR Records | Architecture Decision Records for Monolith, Stack, Tenancy, Errors | ✅ Implemented | [`docs/decisions/`](file:///d:/week/nexus/docs/decisions) (ADR-001–004) |
| **AI Runtime** | Request / Response | Pydantic contracts with token accounting and wall-clock latency | ✅ Implemented | [`ai/runtime/schema.py`](file:///d:/week/nexus/ai/runtime/schema.py) |
| **AI Runtime** | Central Orchestrator | `AIRuntime` managing routing, tool verification, and traces | ✅ Implemented | [`ai/runtime/core.py`](file:///d:/week/nexus/ai/runtime/core.py) |
| **LLM Gateway** | Provider Interface | Abstract `LLMProvider` decoupling business logic from vendors | ✅ Implemented | [`ai/llm/base.py`](file:///d:/week/nexus/ai/llm/base.py) |
| **LLM Gateway** | Transparent Mock | `MockLLMProvider` strictly tagging `[MOCK_PROVIDER / DEMO_MODE]` | ✅ Implemented | [`ai/llm/mock.py`](file:///d:/week/nexus/ai/llm/mock.py) |
| **LLM Gateway** | Remote Providers | OpenAI, Anthropic, Google Gemini API adapters | 📋 Planned | Deferred to Phase 3 |
| **Tool System** | Controlled Tools | Abstract `Tool` with Pydantic validation & execution timeouts | ✅ Implemented | [`ai/tools/base.py`](file:///d:/week/nexus/ai/tools/base.py) |
| **Tool System** | Permission Registry | `ToolRegistry` enforcing human approval for mutating actions | ✅ Implemented | [`ai/tools/registry.py`](file:///d:/week/nexus/ai/tools/registry.py) |
| **Agent Runtime**| State Machine | Explicit 9-state finite state machine with transition guards | ✅ Implemented | [`ai/agents/state.py`](file:///d:/week/nexus/ai/agents/state.py) |
| **Agent Runtime**| Autonomous Loop | Multi-step agent planning loops and memory management | 📋 Planned | Deferred to Phase 5 |
| **RAG Engine** | Ingestion & Search | Chunking, embeddings, hybrid retrieval, and citation engine | 📋 Planned | Deferred to Phase 4 |
| **AI Security** | Threat Defenses | Adversarial test suite for prompt injection and data leakage | 📋 Planned | Deferred to Phase 7 |
| **MLOps** | Tracking & Registry | Dataset versioning, model registry, and experiment logs | 📋 Planned | Deferred to Phase 8 |
| **Systems** | Hardware Probe | C++20 OS interrogation for cores, RAM, and GPU detection | ✅ Implemented | [`systems/runtime/src/hardware_probe.cpp`](file:///d:/week/nexus/systems/runtime/src/hardware_probe.cpp) |
| **Systems** | Build System | Root CMakeLists.txt with Ninja, MSVC /W4, and CPU fallback | ✅ Implemented | [`CMakeLists.txt`](file:///d:/week/nexus/CMakeLists.txt) |
| **Systems** | Process Manager | C++ process supervisor with fork, exec, wait, and signals | 📋 Planned | Deferred to Phase 9 |
| **Systems** | Thread Pool | Bounded queue, condition variables, and throughput metrics | 📋 Planned | Deferred to Phase 9 |
| **Systems** | CPU Scheduler | FCFS, SJF, SRTF, Round Robin, and MLFQ simulation | 📋 Planned | Deferred to Phase 10 |
| **Systems** | Memory Allocator | Custom free-list allocator with fragmentation measurements | 📋 Planned | Deferred to Phase 11 |
| **Systems** | Virtual Memory | Page table simulator with FIFO, LRU, and Optimal replacement | 📋 Planned | Deferred to Phase 11 |
| **Systems** | Networking | Non-blocking event loop (select/poll/epoll) and HTTP server | 📋 Planned | Deferred to Phase 12 |
| **Systems** | Storage Engine | Educational KV store with MemTable, WAL, and crash recovery | 📋 Planned | Deferred to Phase 13 |
| **Algorithms** | Algorithm Lab | Graph, Dynamic Programming, String, and Numerical algorithms | 📋 Planned | Deferred to Phase 14 |
| **Parallelism** | CPU Parallelism | Multithreaded algorithms measuring Amdahl's Law speedup | 📋 Planned | Deferred to Phase 15 |
| **CUDA Engine** | GPU Kernels | Matrix mult, reductions, scan with mandatory CPU references | 📋 Planned | Deferred to Phase 16 |
| **Benchmark** | Unified Framework | Structured benchmark runner capturing hardware and commits | 📋 Planned | Deferred to Phase 17 |
| **Backend API** | FastAPI Service | Python API exposing `/health`, `/telemetry`, `/ai/v1/runtime` | ✅ Implemented | [`apps/api/main.py`](file:///d:/week/nexus/apps/api/main.py) |
| **Web Bridge** | Fastify Service | TypeScript server with RFC 7807 errors and health probes | ✅ Implemented | [`src/presentation/http/app.ts`](file:///d:/week/nexus/src/presentation/http/app.ts) |
| **Containers** | Docker Compose | Multi-container definitions for Postgres, Redis, API, Web | ✅ Implemented | [`docker-compose.yml`](file:///d:/week/nexus/docker-compose.yml) |
| **CI / CD** | GitHub Actions | Automated workflow for Python, C++20, and TypeScript | ✅ Implemented | [`.github/workflows/ci.yml`](file:///d:/week/nexus/.github/workflows/ci.yml) |

---

## AI Architecture & Runtime

### Request Lifecycle
Every AI invocation flows through an explicit validation and tracing lifecycle:

```text
Incoming Request
       │
       ▼
1. Validation (Pydantic AIRequest: prompt, model, max_tokens)
       │
       ▼
2. Model Selection (Configurable routing to remote, local, or mock)
       │
       ▼
3. Tool Discovery (Verify requested tools exist in ToolRegistry)
       │
       ▼
4. Context & Retrieval (Assemble context; RAG integration in Phase 4)
       │
       ▼
5. Inference Execution (Provider generate() or stream())
       │
       ▼
6. Response Sanitization (Format output, calculate duration, estimate tokens)
       │
       ▼
7. Telemetry Trace (Record request_id, model, latency_ms, hardware_mode)
```

### LLM Provider Abstraction
The [`LLMProvider`](file:///d:/week/nexus/ai/llm/base.py#L10-L40) interface isolates application code from LLM vendors:
```python
class LLMProvider(ABC):
    @property
    @abstractmethod
    def provider_name(self) -> str: pass

    @property
    @abstractmethod
    def is_mock(self) -> bool: pass

    @abstractmethod
    async def generate(self, request: AIRequest) -> AIResponse: pass

    @abstractmethod
    async def stream(self, request: AIRequest) -> AsyncIterator[str]: pass

    @abstractmethod
    async def embed(self, texts: List[str], model: Optional[str] = None) -> List[List[float]]: pass
```

The verified [`MockLLMProvider`](file:///d:/week/nexus/ai/llm/mock.py#L11-L68) guarantees offline testability and constitutional compliance by prefixing all outputs with `[MOCK_PROVIDER / DEMO_MODE]`.

### Agent State Machine
To eliminate implicit, uncontrolled agent reasoning loops, NEXUS TITAN enforces an explicit finite state machine ([`AgentStateMachine`](file:///d:/week/nexus/ai/agents/state.py#L65-L105)):

```mermaid
stateDiagram-v2
    [*] --> CREATED
    CREATED --> PLANNING
    CREATED --> CANCELLED
    PLANNING --> WAITING_FOR_TOOL
    PLANNING --> EXECUTING
    PLANNING --> COMPLETED
    PLANNING --> FAILED
    WAITING_FOR_TOOL --> WAITING_FOR_APPROVAL: Mutating Tool
    WAITING_FOR_TOOL --> EXECUTING: Read-Only Tool
    WAITING_FOR_APPROVAL --> EXECUTING: Approved
    WAITING_FOR_APPROVAL --> CANCELLED: Rejected
    EXECUTING --> OBSERVING
    OBSERVING --> PLANNING: Next Iteration
    OBSERVING --> COMPLETED: Goal Satisfied
    COMPLETED --> [*]
    FAILED --> [*]
    CANCELLED --> [*]
```

---

## Systems Architecture (TITAN)

The TITAN layer exposes operating-system primitives and hardware interactions using standard C++20.

### Dynamic Hardware Interrogation
The [`titan::HardwareProbe`](file:///d:/week/nexus/systems/runtime/include/titan/hardware_probe.hpp#L25-L38) queries the operating system directly at startup:
* **Architecture:** Identifies `x86_64 (AMD64)`, `ARM64`, or `x86` via Windows `GetNativeSystemInfo` or POSIX `sysconf`.
* **Cores:** Queries logical processor relationship structures (`GetLogicalProcessorInformation`) to separate physical cores from hyperthreaded logical cores.
* **Memory:** Interrogates `GlobalMemoryStatusEx` to obtain exact total physical bytes and available memory.
* **Accelerator:** Probes for CUDA compute devices via `cudaGetDeviceCount`. If absent, gracefully sets `build_mode = "CPU_ONLY"`.

### Planned Systems Subsystems (Phases 9–13)
* **Process Supervisor:** Interfacing with OS process management (`fork`, `exec`, `wait`, signals on POSIX; `CreateProcess`, `TerminateProcess` on Windows) with output pipe capture.
* **Thread Pool:** Producer-consumer model with bounded thread-safe work queue (`std::mutex`, `std::condition_variable`), worker threads, and queue wait latency telemetry.
* **CPU Scheduler Simulator:** Configurable simulator evaluating FCFS, SJF, SRTF, Priority, Round Robin, and MLFQ with metrics for turnaround time, wait time, and throughput.
* **Memory Allocator:** Custom free-list allocator demonstrating first-fit/best-fit allocation, coalescing, memory alignment, and external fragmentation tracking.
* **Key-Value Storage Engine:** Append-only Write-Ahead Log (WAL), in-memory MemTable, SSTables, and crash recovery verification.

---

## High-Performance Compute & Algorithms (QUANTUM)

The QUANTUM COMPUTE layer explores algorithmic efficiency, multithreading, and GPU acceleration.

### Algorithmic Scope (Phases 14–17)
* **Graph Algorithms:** Dijkstra, Bellman-Ford, Floyd-Warshall, BFS, DFS, Minimum Spanning Tree (Kruskal/Prim), Topological Sort, A*, and Max-Flow.
* **Dynamic Programming:** 0/1 Knapsack, Longest Common Subsequence (LCS), Levenshtein Edit Distance, Matrix Chain Multiplication, and Bitmask DP.
* **Numerical Methods:** Root finding, Gaussian elimination, matrix inversion, numerical integration (Simpson's rule), and Monte Carlo simulation.
* **Parallel Computing:** Parallel reductions, thread-level data parallelism, OpenMP/SIMD vectorization, and empirical validation of Amdahl's Law.

---

## Hardware-Aware Execution & CPU-Only Mode

NEXUS TITAN is designed to run anywhere—from high-end multi-GPU server clusters to CPU-only developer laptops.

### Dynamic Compilation & Execution Logic

```text
CMake Build Configuration
          │
          ▼
check_language(CUDA)
          │
    ┌─────┴─────────────────────────┐
    │                               │
    ▼                               ▼
[CUDA Compiler Found]       [No CUDA Compiler]
    │                               │
Enable CUDA Language        Set -DTITAN_CPU_ONLY=1
Compile titan_cuda          Compile CPU Fallbacks
Telemetry: GPU Active       Telemetry: CPU-Only Active
```

### Actual Measured Hardware Output
The native C++ hardware probe was compiled with MSVC 19.44 and Ninja on the host machine. The actual verified output:

```text
========================================================
  NEXUS TITAN — Host Hardware Diagnostics
========================================================
  CPU Architecture:  x86_64 (AMD64)
  Physical Cores:    10
  Logical Threads:   12
  Total Memory:      15.72 GB
  Available Memory:  5.24 GB
  Build Mode:        CPU_ONLY
  CUDA Available:    NO (CPU Fallback Active)
  GPU Device:        None (Compiled in CPU-Only Mode)
========================================================
```

---

## Performance Engineering & Benchmark Methodology

In strict compliance with Constitution Article I, NEXUS TITAN rejects fabricated or unsubstantiated performance claims.

### Benchmark Execution Standards
When the Unified Benchmark Framework is executed (Phase 17+):
1. **Warm-up Iterations:** Mandatory untimed warm-up cycles to eliminate JIT, disk cache, or CPU governor warm-up variance.
2. **Repeated Runs:** Benchmarks run across multiple iterations ($N \ge 10$) to capture mean, median, standard deviation, and 99th percentile tail latency.
3. **Hardware Context:** Every benchmark entry records the exact CPU model, available memory, thread count, and git commit.
4. **Speedup Formula:**
   $$\text{Speedup} = \frac{T_{\text{CPU Single-Thread Baseline}}}{T_{\text{Accelerated / Multi-Thread}}}$$
   Speedup claims are only valid when measured on identical input data and hardware.

---

## Profiling & Sanitizers

The C++ systems layer is engineered for practical debugging and memory safety:
* **AddressSanitizer (ASan):** Detects out-of-bounds memory accesses, use-after-free, and double-free errors.
* **UndefinedBehaviorSanitizer (UBSan):** Catches integer overflow, misaligned pointers, and undefined behavior.
* **ThreadSanitizer (TSan):** Validates thread safety, detecting data races in synchronization primitives and thread pools.
* **Compiler Warning Policy:** Compiles cleanly with zero warnings under `/W4` on MSVC and `-Wall -Wextra -Wpedantic` on GCC/Clang.

---

## Research Framework & Experimental Methodology

Every research study conducted in NEXUS TITAN must follow the structured research schema:

```text
├── Experiment ID:        EXP-001 (Unique identifier)
├── Research Question:    e.g., At what matrix dimension does GPU acceleration overcome PCIe transfer overhead?
├── Hypothesis:           e.g., For N < 512, CPU single-threaded execution will be faster due to PCIe transfer latency.
├── Hardware & OS:        Host specifications and driver versions
├── Dataset / Input:      Deterministic input generator
├── Independent Vars:     Input dimension N, thread count, block size
├── Dependent Vars:       Wall-clock time (ms), transfer time (ms), kernel time (ms), GFLOPS
├── Raw Measurements:     Recorded CSV / JSON telemetry logs
├── Limitations:          Hardware thermal throttling, memory bandwidth constraints
└── Conclusion:           Empirically supported findings
```

---

## Technology Stack

The following technologies are actively integrated into the repository:

| Domain | Technology | Version | Purpose | Status |
|---|---|---|---|---|
| **Systems Runtime** | **C++20** | ISO C++20 | Low-level systems, hardware probing, and compute engines | ✅ Implemented |
| **Build System** | **CMake** | $\ge$ 3.25 | Cross-platform C++ build generation | ✅ Implemented |
| **Build Generator**| **Ninja** | $\ge$ 1.11 | High-speed C++ compilation backend | ✅ Implemented |
| **C++ Compiler** | **MSVC / Clang** | MSVC 19.44 | Native machine code compilation | ✅ Implemented |
| **AI Runtime** | **Python** | 3.12 / 3.14 | AI orchestration, schemas, and API server | ✅ Implemented |
| **API Framework** | **FastAPI** | $\ge$ 0.115 | Asynchronous REST API server | ✅ Implemented |
| **Validation** | **Pydantic** | $\ge$ 2.10 | Type enforcement for AI schemas and tool inputs | ✅ Implemented |
| **Web Server** | **Node.js** | $\ge$ 20 (LTS 22)| JavaScript/TypeScript application runtime | ✅ Implemented |
| **Web Language** | **TypeScript** | $\ge$ 5.8 | End-to-end type safety for presentation services | ✅ Implemented |
| **Web Framework** | **Fastify** | $\ge$ 5.2 | High-throughput presentation bridge with RFC 7807 | ✅ Implemented |
| **Schema Parser** | **Zod** | $\ge$ 3.24 | Runtime environment validation for Node services | ✅ Implemented |
| **Test Runner (Py)**| **pytest** | $\ge$ 8.3 | Automated testing for AI runtime and tools | ✅ Implemented |
| **Test Runner (TS)**| **Vitest** | $\ge$ 3.0 | Automated testing for TypeScript presentation layer | ✅ Implemented |
| **Test Runner (C++)**| **CTest** | $\ge$ 3.25 | Automated testing for native C++ binaries | ✅ Implemented |
| **Containers** | **Docker** | Compose v2 | Multi-container definitions (PostgreSQL 16, Redis 7) | ✅ Implemented |
| **CI / CD** | **GitHub Actions**| v4 / v5 | Multi-OS continuous integration pipeline | ✅ Implemented |

---

## Repository Structure

The actual file tree of the NEXUS TITAN repository:

```text
nexus/
├── .env.example                               # Documented environment variable template
├── .gitignore                                 # Git ignore rules for node, dist, build, and caches
├── .github/
│   └── workflows/
│       └── ci.yml                             # Multi-OS GitHub Actions CI pipeline
├── CMakeLists.txt                             # Root C++20 CMake build configuration
├── docker-compose.yml                         # Multi-container stack (Postgres, Redis, API, Web)
├── package.json                               # TypeScript dependencies & scripts
├── package-lock.json                          # NPM deterministic dependency tree
├── pyproject.toml                             # Python packaging (PEP 621) & pytest config
├── README.md                                  # Master project manual & presentation document
├── tsconfig.json                              # Strict TypeScript configuration (NodeNext ESM)
├── vitest.config.ts                           # Vitest configuration for TypeScript tests
│
├── apps/                                      # Application services
│   └── api/
│       └── main.py                            # FastAPI entry point & systems telemetry bridge
│
├── ai/                                        # Layer A: AI Application Infrastructure
│   ├── agents/
│   │   ├── __init__.py
│   │   └── state.py                           # AgentState enum & finite state machine
│   ├── evaluation/
│   │   └── __init__.py                        # Evaluation foundation stub
│   ├── llm/
│   │   ├── __init__.py
│   │   ├── base.py                            # Abstract LLMProvider interface
│   │   └── mock.py                            # Constitutionally tagged MockLLMProvider
│   ├── mlops/
│   │   └── __init__.py                        # MLOps foundation stub
│   ├── rag/
│   │   └── __init__.py                        # RAG foundation stub
│   ├── runtime/
│   │   ├── __init__.py
│   │   ├── core.py                            # Central AIRuntime orchestrator
│   │   └── schema.py                          # AIRequest, AIResponse, TelemetryTrace schemas
│   ├── security/
│   │   └── __init__.py                        # AI Security foundation stub
│   └── tools/
│       ├── __init__.py
│       ├── base.py                            # Controlled Tool base class
│       └── registry.py                        # ToolRegistry with approval gates
│
├── systems/                                   # Layer B: TITAN Systems Infrastructure
│   ├── CMakeLists.txt                         # Systems CMake build configuration
│   └── runtime/
│       ├── include/
│       │   └── titan/
│       │       └── hardware_probe.hpp         # C++ Hardware probe interface
│       ├── src/
│       │   └── hardware_probe.cpp             # Win32 / POSIX hardware probe implementation
│       └── tests/
│           └── test_hardware_probe.cpp        # CTest hardware probe unit test
│
├── src/                                       # TypeScript Presentation & Bridge Layer
│   ├── index.ts                               # Fastify server bootstrap & graceful shutdown
│   ├── config/
│   │   └── index.ts                           # Zod environment variable parsing
│   ├── domain/
│   │   └── errors/
│   │       └── index.ts                       # RFC 7807 Problem Details error hierarchy
│   ├── infrastructure/
│   │   └── logging/
│   │       └── logger.ts                      # Pino structured logging
│   └── presentation/
│       └── http/
│           ├── app.ts                         # Fastify application factory
│           └── routes/
│               ├── api.ts                     # API metadata endpoint (/api/v1)
│               └── health.ts                  # Health endpoints (/health, /live, /ready)
│
├── tests/                                     # Automated test suites
│   ├── ai/
│   │   ├── test_agent_state.py                # Agent state machine transitions test
│   │   ├── test_ai_runtime.py                 # AI runtime telemetry & mock tests
│   │   └── test_tools.py                      # Tool registration & approval gate tests
│   ├── integration/
│   │   └── health.test.ts                     # HTTP integration & RFC 7807 tests
│   └── unit/
│       ├── config.test.ts                     # Zod config validation tests
│       └── errors.test.ts                     # Domain error hierarchy tests
│
├── docs/                                      # Project specifications & records
│   ├── architecture.md                        # Master system architecture document
│   ├── constitution.md                        # Inviolable Engineering Constitution
│   ├── roadmap.md                             # 20-phase master development roadmap
│   ├── architecture/
│   │   └── system-architecture.md             # Detailed layered architecture specification
│   ├── decisions/                             # Architecture Decision Records
│   │   ├── ADR-001-modular-monolith-architecture.md
│   │   ├── ADR-002-technology-stack-selection.md
│   │   ├── ADR-003-data-isolation-strategy.md
│   │   └── ADR-004-standardized-error-handling.md
│   └── product/
│       └── specification.md                   # Product requirements & assumptions
│
├── infrastructure/                            # Container & orchestration assets
│   └── docker/
│       ├── Dockerfile.api                     # Python API multi-stage container build
│       └── Dockerfile.web                     # TypeScript Web multi-stage container build
│
└── scripts/                                   # Development & verification automation
    ├── build_systems.bat                      # Native MSVC/Ninja C++ builder
    ├── build_systems.ps1                      # PowerShell wrapper for C++ builder
    └── run_checks.ps1                         # Unified test runner across all 3 stacks
```

---

## Installation & Prerequisites

### Prerequisites

| Tool | Minimum Version | Verified Host Version | Download / Installation |
|---|---|---|---|
| **Git** | 2.30+ | 2.52.0 (Windows) | [git-scm.com](https://git-scm.com/) |
| **Python** | 3.11+ | 3.14.4 (Windows AMD64) | [python.org](https://www.python.org/) |
| **Node.js** | 20.0+ | 22.19.0 (LTS) | [nodejs.org](https://nodejs.org/) |
| **C++ Compiler** | C++20 compliant | MSVC 19.44 (Visual Studio 2022) / GCC 12+ / Clang 15+ | [visualstudio.microsoft.com](https://visualstudio.microsoft.com/) |
| **CMake** | 3.25+ | 3.31.6 | [cmake.org](https://cmake.org/) |
| **Ninja** | 1.10+ | 1.12.0 | Included with Visual Studio / [ninja-build.org](https://ninja-build.org/) |

> [!NOTE]
> NVIDIA GPU hardware and the CUDA Toolkit are **optional**. If CUDA is not detected, the build system automatically configures the project in CPU-Only Mode.

---

## Quick Start

Execute these commands to clone the repository, install dependencies, and run all verification suites:

### 1. Clone the Repository
```bash
git clone https://github.com/Ft-sumukh/nexus.git
cd nexus
```

### 2. Configure Environment
```bash
# On Linux / macOS:
cp .env.example .env

# On Windows (PowerShell):
Copy-Item .env.example .env
```

### 3. Install Dependencies
```bash
# Install Node.js / TypeScript dependencies
npm install

# Install Python dependencies
pip install -e .[dev]
```

### 4. Run Unified Verification Across All Three Stacks
On Windows (PowerShell):
```powershell
.\scripts\run_checks.ps1
```
This single script configures and compiles the C++20 systems layer, runs CTest, executes all Python AI pytest suites, and runs TypeScript type checking and Vitest tests.

---

## Environment Configuration

Configuration is managed strictly through environment variables and validated at startup using Zod in Node.js and Pydantic in Python.

| Variable | Type | Default | Description | Example |
|---|---|---|---|---|
| `NODE_ENV` | String | `development` | Runtime environment (`development`, `test`, `production`) | `production` |
| `PORT` | Integer | `3000` | HTTP port for the Fastify presentation server | `3000` |
| `HOST` | String | `0.0.0.0` | Network binding interface | `127.0.0.1` |
| `LOG_LEVEL` | String | `info` | Structured logging verbosity (`debug`, `info`, `warn`, `error`) | `info` |
| `CORS_ORIGIN` | String | `*` | Allowed cross-origin domain | `http://localhost:5173` |
| `SESSION_SECRET` | String | *(dev-fallback)* | Cryptographic key for session cookies (min 16 chars) | `openssl rand -base64 32` |
| `JWT_SECRET` | String | *(dev-fallback)* | Cryptographic key for token signing (min 16 chars) | `openssl rand -base64 32` |
| `DATABASE_URL` | String | *(optional)* | PostgreSQL target connection string (Phase 4+) | `postgresql://postgres:postgres@localhost:5432/nexus_titan` |
| `TENANCY_MODE` | String | `shared-table` | Data isolation mode (`shared-table` vs `schema-per-tenant`) | `shared-table` |

---

## Running the Application

### Running the Python AI API Service (Port 8000)
```bash
uvicorn apps.api.main:app --host 0.0.0.0 --port 8000 --reload
```
Available endpoints:
* `GET http://localhost:8000/health` — Service health status
* `GET http://localhost:8000/telemetry/hardware` — Invokes C++ hardware probe and returns host metrics
* `GET http://localhost:8000/ai/v1/tools` — Lists registered tools, schemas, and approval requirements
* `POST http://localhost:8000/ai/v1/runtime/execute` — Submits a prompt to the central AI runtime

### Running the TypeScript Presentation Service (Port 3000)
```bash
# Development mode with live watch/reload:
npm run dev

# Production build and execution:
npm run build
npm start
```
Available endpoints:
* `GET http://localhost:3000/health` — Full process telemetry (uptime, memory usage RSS/heap)
* `GET http://localhost:3000/health/live` — Liveness probe (Kubernetes / container orchestrators)
* `GET http://localhost:3000/health/ready` — Readiness probe
* `GET http://localhost:3000/api/v1` — Root API descriptor

---

## Docker Container Architecture

A multi-container setup is defined in [`docker-compose.yml`](file:///d:/week/nexus/docker-compose.yml):

```yaml
services:
  postgres:  # PostgreSQL 16 Alpine with volume persistence and healthcheck
  redis:     # Redis 7 Alpine in-memory broker with healthcheck
  api:       # Python FastAPI service with C++ hardware probe runtime
  web:       # Node 22 / Fastify presentation web shell
```

### Launching Local Database & Cache
```bash
docker compose up -d postgres redis
```

### Stopping Services
```bash
docker compose down
```

---

## Automated Verification & Test Suites

NEXUS TITAN maintains automated test suites across all three language ecosystems. Currently, **24 automated tests are implemented and passing with a 100% pass rate**:

```text
=============================================================================
                          TEST EXECUTION SUMMARY
=============================================================================
  Language / Framework       Suite                   Tests Passed    Duration
-----------------------------------------------------------------------------
  C++20 (MSVC / CTest)       test_hardware_probe     1 / 1 (100%)    0.03s
  Python 3 (pytest)          tests/ai/               9 / 9 (100%)    0.10s
  TypeScript (Vitest / tsc)  tests/unit/ & integr/   14 / 14 (100%)  1.69s
-----------------------------------------------------------------------------
  TOTAL VERIFIED TESTS                               24 / 24 (100%)  < 2.0s
=============================================================================
```

### 1. Running C++ Systems Tests
```powershell
.\scripts\build_systems.ps1
```
Output:
```text
Test project D:/week/nexus/build
    Start 1: TestHardwareProbe
1/1 Test #1: TestHardwareProbe ................   Passed    0.03 sec

100% tests passed, 0 tests failed out of 1
```

### 2. Running Python AI Tests
```bash
python -m pytest tests/ai -v
```
Output:
```text
tests/ai/test_agent_state.py::test_agent_state_machine_valid_progression PASSED
tests/ai/test_agent_state.py::test_agent_state_machine_invalid_transition_rejected PASSED
tests/ai/test_agent_state.py::test_terminal_states_prevent_further_transitions PASSED
tests/ai/test_ai_runtime.py::test_ai_runtime_execution_with_mock_provider PASSED
tests/ai/test_ai_runtime.py::test_ai_runtime_streaming PASSED
tests/ai/test_ai_runtime.py::test_mock_embeddings PASSED
tests/ai/test_tools.py::test_tool_registry_and_execution PASSED
tests/ai/test_tools.py::test_mutating_tool_approval_gate PASSED
tests/ai/test_tools.py::test_invalid_parameters_fail_validation PASSED

============================== 9 passed in 0.10s ==============================
```

### 3. Running TypeScript Tests
```bash
npm test
```
Output:
```text
 ✓ tests/unit/errors.test.ts (5 tests) 19ms
 ✓ tests/unit/config.test.ts (4 tests) 23ms
 ✓ tests/integration/health.test.ts (5 tests) 188ms

 Test Files  3 passed (3)
      Tests  14 passed (14)
   Duration  1.69s
```

---

## CI/CD Pipeline

Continuous integration is managed via GitHub Actions in [`.github/workflows/ci.yml`](file:///d:/week/nexus/.github/workflows/ci.yml):

* **Job 1: `python-ai-tests` (Ubuntu)**
  * Sets up Python 3.12, installs dependencies, and runs `pytest tests/ai -v`.
* **Job 2: `cpp-systems-build` (Matrix: Ubuntu & Windows)**
  * Installs Ninja on Linux, configures CMake in CPU-Only mode, compiles C++ targets, and executes CTest.
* **Job 3: `typescript-presentation-tests` (Ubuntu)**
  * Sets up Node.js 22, installs npm packages, runs `tsc --noEmit` static typechecking, executes Vitest suite, and validates `npm run build`.

---

## Security Architecture & Safe Tool Execution

In adherence to Constitution Article III, NEXUS TITAN enforces defensive security at every boundary:

### 1. Controlled Tool Interface
Every tool accessible to an AI agent inherits from the abstract [`Tool`](file:///d:/week/nexus/ai/tools/base.py#L10-L50) class:
* Input arguments must validate against a strict Pydantic model.
* Mutating operations (filesystem writes, file deletion, database modification, network requests) are flagged `is_mutating = True`.
* Mutating tools trigger a mandatory approval gate:
  ```python
  if tool.requires_approval and not approved:
      raise ApprovalRequiredError(f"Tool '{name}' requires explicit human approval.")
  ```

### 2. Standardized RFC 7807 Problem Details
All API error responses follow the **RFC 7807 Problem Details** standard, sanitizing stack traces and internal database schemas from production responses:
```json
{
  "type": "https://nexus.platform/errors/resource-not-found",
  "title": "NotFound",
  "status": 404,
  "detail": "Endpoint with identifier '/unregistered' was not found.",
  "code": "RESOURCE_NOT_FOUND",
  "instance": "/unregistered",
  "timestamp": "2026-09-30T17:09:54.811Z"
}
```

---

## Observability & Telemetry

NEXUS TITAN records structured telemetry at both the AI and Systems layers:

### AI Request Telemetry
Every call through [`AIRuntime.execute()`](file:///d:/week/nexus/ai/runtime/core.py#L42-L73) emits a [`TelemetryTrace`](file:///d:/week/nexus/ai/runtime/schema.py#L42-L53):
* `request_id`: Unique tracing UUID.
* `model`: Model identifier invoked.
* `duration_ms`: High-resolution wall-clock duration (`time.perf_counter()`).
* `input_tokens` / `output_tokens`: Calculated token usage.
* `hardware_mode`: `"CPU_ONLY"` or `"CUDA_ENABLED"`.
* `error`: Exception message if failed, `None` if successful.

### Systems Telemetry
The Fastify HTTP layer injects or propagates correlation IDs (`x-request-id`) on every incoming request, logged via structured Pino JSON. Process health endpoints expose live RSS, heap usage, and uptime metrics.

---

## 20-Phase Master Roadmap

NEXUS TITAN progresses systematically through 20 phases. Current verified status:

* [x] **Phase 00 — Engineering Constitution:** Codified the 6 inviolable laws in [`docs/constitution.md`](file:///d:/week/nexus/docs/constitution.md).
* [x] **Phase 01 — Repository & Development Foundation:** Multi-language repository (C++20, Python, TypeScript), CMake build system, C++ Hardware Probe, Python AI Runtime & Mock Provider, Tool Registry with approval gates, Agent State Machine, Docker Compose, CI workflow, and passing tests.
* [ ] **Phase 02 — AI Runtime Foundation:** Advanced request context pipelines, streaming backpressure, model routing policies, and persistent trace logging.
* [ ] **Phase 03 — LLM Gateway:** Remote provider adapters (OpenAI, Anthropic, Gemini) and local llama.cpp / Ollama integration.
* [ ] **Phase 04 — RAG Engine:** Document ingestion, chunking strategies, pgvector storage, hybrid retrieval (BM25 + vector), reranker, and citation engine.
* [ ] **Phase 05 — Tool Calling & Agent Runtime:** Multi-step autonomous planning loops, budget limits, execution timeouts, and memory state.
* [ ] **Phase 06 — AI Evaluation:** Retrieval benchmarks (Recall@K, MRR, nDCG), context relevance, and hallucination scoring.
* [ ] **Phase 07 — AI Security:** Adversarial test suite for prompt injection, indirect document injection, and secret exfiltration.
* [ ] **Phase 08 — MLOps Infrastructure:** Experiment tracking, model registry, dataset versioning, and deployment metadata.
* [ ] **Phase 09 — Process & Thread Runtime:** C++ process supervisor (`fork`, `exec`, signals) and production-grade thread pool with bounded work queue.
* [ ] **Phase 10 — CPU Scheduling & Synchronization:** FCFS, SJF, SRTF, Round Robin, and MLFQ simulation + Mutex, Semaphore, and Peterson's demonstrations.
* [ ] **Phase 11 — Memory & Virtual Memory:** Custom free-list memory allocator (fragmentation metrics) + Paging simulator (FIFO, LRU, Optimal).
* [ ] **Phase 12 — IPC & Networking:** Pipes, shared memory, domain sockets, TCP/UDP sockets, non-blocking event loop (`select`, `poll`, `epoll`).
* [ ] **Phase 13 — Storage Engine:** Key-value store with MemTable, Write-Ahead Log (WAL), append-only log, and crash recovery.
* [ ] **Phase 14 — Algorithm Laboratory:** Graph algorithms, Dynamic Programming, String algorithms, and Numerical computing benchmarks.
* [ ] **Phase 15 — Parallel Computing:** CPU multithreading, data parallelism, reductions, and empirical Amdahl's Law validation.
* [ ] **Phase 16 — CUDA / GPU Engine:** CUDA kernels for GEMM, reductions, and prefix scans with mandatory CPU reference implementations.
* [ ] **Phase 17 — Performance Engineering:** Unified benchmark framework, memory throughput profiling, and speedup analysis.
* [ ] **Phase 18 — Unified Runtime Integration:** End-to-end user journey: User $\to$ Agent $\to$ Benchmark Tool $\to$ Hardware $\to$ AI Explanation $\to$ Dashboard.
* [ ] **Phase 19 — Security & Reliability:** Sandboxing, fault injection, failover drills, and AddressSanitizer/ThreadSanitizer audits.
* [ ] **Phase 20 — Research Experiments & Publication:** Empirical research papers and reproducible research experiment artifacts.

---

## Current Project Status Dashboard

| Layer / Area | Implementation Status | Verified Evidence |
|---|---|---|
| **Phase 0 Constitution** | ✅ Complete | [`docs/constitution.md`](file:///d:/week/nexus/docs/constitution.md) approved |
| **Phase 1 Repository** | ✅ Complete | Multi-language tree, CMake, Python packaging, Docker, CI |
| **Systems Runtime (C++)** | 🟡 Active Foundation | C++20 Hardware Probe tested & passing in CTest (0.03s) |
| **AI Runtime (Python)** | 🟡 Active Foundation | Schemas, AIRuntime, MockLLMProvider, Tools, Agent State tested in pytest (0.10s) |
| **Presentation (TS)** | 🟡 Active Foundation | Fastify, RFC 7807 errors, Zod config tested in Vitest (1.69s) |
| **LLM Gateway** | 🟡 Mock Implemented | Mock provider working; live remote providers in Phase 3 |
| **RAG Subsystem** | 📋 Planned | Architecture designed; implementation in Phase 4 |
| **Autonomous Agents** | 🟡 State Machine Ready | FSM & transitions verified; multi-step loop in Phase 5 |
| **OS Components (C++)** | 📋 Planned | Architecture designed; thread pool & supervisor in Phase 9 |
| **Compute & CUDA** | 🟡 CPU Fallback Ready | CMake CUDA probe with CPU fallback verified; kernels in Phase 16 |
| **Benchmarking** | 📋 Planned | Methodology documented; framework implementation in Phase 17 |

---

## Known Limitations

In compliance with our engineering standards, we explicitly document all current project constraints:
1. **CPU-Only Operation on Current Host:** The host development machine lacks an NVIDIA GPU / CUDA compiler. The system compiles cleanly in CPU-Only Mode with software fallbacks. GPU acceleration will remain unverified until executed on a CUDA-capable host.
2. **Mock AI Inference Only:** Current unit tests and runtime endpoints use `MockLLMProvider`. No live API keys (OpenAI, Anthropic, Gemini) are wired into the baseline, preventing accidental cloud costs during development.
3. **No Distributed Storage Cluster:** The key-value store and relational database are designed as single-node local instances (PostgreSQL via Docker); distributed databases and sharding are out of scope.
4. **Tool Sandboxing is Logical:** Tool execution checks are enforced through Python permission checks and approval gates; process-level OS sandboxing (e.g. Docker-in-Docker or seccomp) will be introduced in Phase 19.

---

## Troubleshooting Guide

### 1. C++ Build: `vcvars64.bat not found`
* **Cause:** Visual Studio 2022 Community is not installed in the standard path.
* **Fix:** Update `$VsCMake` and `$VCVARS` in [`scripts/build_systems.bat`](file:///d:/week/nexus/scripts/build_systems.bat) to point to your Visual Studio `vcvars64.bat` path.

### 2. PowerShell Execution Policy Restriction
* **Cause:** Windows restricts running unsigned PowerShell scripts by default.
* **Fix:** Run the script with bypass mode:
  ```powershell
  powershell -ExecutionPolicy Bypass -File .\scripts\run_checks.ps1
  ```

### 3. Port Conflicts (Port 3000 or 8000 in use)
* **Fix:** Change the port in `.env` (`PORT=3001` or `PORT=8001`) or kill the conflicting process:
  ```powershell
  Get-Process -Id (Get-NetTCPConnection -LocalPort 3000).OwningProcess | Stop-Process
  ```

---

## Documentation Map

All specifications, architectural designs, and decision records are maintained in the repository:

* [**docs/constitution.md**](docs/constitution.md) — The Inviolable Engineering Constitution (6 core laws).
* [**docs/architecture.md**](docs/architecture.md) — Master System Architecture & Computing Stack.
* [**docs/roadmap.md**](docs/roadmap.md) — The 20-Phase Master Development Roadmap.
* [**docs/product/specification.md**](docs/product/specification.md) — Product requirements, assumptions, and open questions.
* [**docs/architecture/system-architecture.md**](docs/architecture/system-architecture.md) — Detailed layered modular monolith specification.
* [**docs/decisions/ADR-001-modular-monolith-architecture.md**](docs/decisions/ADR-001-modular-monolith-architecture.md) — ADR 001: Modular Monolith Architecture.
* [**docs/decisions/ADR-002-technology-stack-selection.md**](docs/decisions/ADR-002-technology-stack-selection.md) — ADR 002: Technology Stack & Language Selection.
* [**docs/decisions/ADR-003-data-isolation-strategy.md**](docs/decisions/ADR-003-data-isolation-strategy.md) — ADR 003: Multi-Tenancy & Data Isolation Strategy.
* [**docs/decisions/ADR-004-standardized-error-handling.md**](docs/decisions/ADR-004-standardized-error-handling.md) — ADR 004: RFC 7807 Problem Details Error Handling.

---

## Code Quality & Contribution Guide

### Branching & Commit Conventions
* All development branches fork from `main`.
* Commits must follow Conventional Commits format:
  * `feat:` New features or capabilities
  * `fix:` Bug fixes or corrections
  * `test:` New or updated automated tests
  * `docs:` Documentation and specification updates
  * `refactor:` Code refactoring without behavioral changes

### Testing & Verification Requirements
* Pull requests must pass the unified verification runner (`.\scripts\run_checks.ps1`) with 100% pass rate.
* New performance claims must include verifiable benchmark logs detailing hardware specs, input sizes, and run counts.
* Code must compile with zero warnings under `/W4` on MSVC and `-Wall -Wextra` on GCC/Clang.

---

## License

This project is proprietary and confidential. License information will be added separately.

---

## Author & Acknowledgements

* **Author:** Ft.sumukh ([GitHub Profile](https://github.com/Ft-sumukh))
* **Repository:** [`https://github.com/Ft-sumukh/nexus.git`](https://github.com/Ft-sumukh/nexus.git)
* **Acknowledgements:** Built with modern open-source foundations including ISO C++20, Kitware CMake, FastAPI, Pydantic, Node.js, TypeScript, Fastify, and Vitest.

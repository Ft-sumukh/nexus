# NEXUS TITAN — System Architecture & Computing Stack

**Document Version:** 1.0.0  
**Status:** Approved Master Architecture  
**Scope:** AI Systems, Runtime & High-Performance Computing Laboratory  

---

## 1. High-Level Vision & Computing Stack

NEXUS TITAN demonstrates the complete computational journey of modern intelligent applications:

```text
                    USER
                      │
                      ▼
              WEB APPLICATION (React / Next.js / TypeScript)
                      │
                      ▼
                 API SERVER (FastAPI / Fastify Bridge)
                      │
                      ▼
              AI ORCHESTRATOR
                      │
          ┌───────────┼───────────┐
          ▼           ▼           ▼
      RAG Engine   Tool System  Agent Runtime
          │           │           │
          └───────────┼───────────┘
                      ▼
                 LLM GATEWAY (Provider Abstraction)
                      │
             ┌────────┴────────┐
             ▼                 ▼
      Remote Provider     Local Model Engine
                               │
                               ▼
                       INFERENCE RUNTIME
                               │
                       ┌───────┴───────┐
                       ▼               ▼
                      CPU             GPU
                       │               │
                       ▼               ▼
                SYSTEM RUNTIME    CUDA ENGINE
                   (C++20)       (Kernels / Fallback)
                       │
          ┌────────────┼────────────┐
          ▼            ▼            ▼
      Processes      Memory      Networking
          │            │            │
          └────────────┼────────────┘
                       ▼
                    STORAGE (Key-Value / WAL)
```

---

## 2. The Three Layer Architecture

### Layer A — NEXUS (Intelligent Application Infrastructure)
* **Runtime Language:** Python 3.12+ / 3.14 + TypeScript
* **Core Responsibilities:**
  * **AI Runtime:** Request validation, model routing, context assembly, telemetry tracking (`request_id`, tokens, latency).
  * **LLM Gateway:** Provider abstraction supporting remote APIs (OpenAI, Anthropic, Gemini), local engines (Ollama, llama.cpp, PyTorch), and transparent mock providers for offline testing.
  * **RAG Engine:** Ingestion (PDF, HTML, Markdown, TXT, JSON), chunking strategies, embeddings, hybrid retrieval (BM25 + vector similarity), reranking, and citation provenance.
  * **Agent Runtime:** Explicit finite state machine (`CREATED`, `PLANNING`, `WAITING_FOR_TOOL`, `EXECUTING`, `OBSERVING`, `WAITING_FOR_APPROVAL`, `COMPLETED`, `FAILED`, `CANCELLED`).
  * **Tool System:** Controlled tool interfaces with strict Pydantic schemas, permission classification, and human-in-the-loop approval.
  * **AI Security:** Defenses against direct/indirect prompt injection, secret extraction, and tool abuse.
  * **MLOps & Evaluation:** Retrieval metrics (Recall@K, MRR, nDCG), grounding validation, experiment tracking, and model registry.

### Layer B — TITAN (Systems Infrastructure)
* **Runtime Language:** Modern C++ (C++20) with CMake
* **Core Responsibilities:**
  * **Process Manager:** Process supervisor demonstrating `fork`, `exec`, `wait`, signals, lifecycle control, and output capture.
  * **Thread Pool:** Production-grade thread pool with bounded work queue, condition variables, backpressure, and throughput telemetry.
  * **CPU Scheduling:** Simulators and comparative visualizations for FCFS, SJF, SRTF, Priority, Round Robin, and Multilevel Feedback Queue (MLFQ).
  * **Synchronization:** Demonstrations of mutexes, semaphores, condition variables, spinlocks, and Peterson's algorithm.
  * **Deadlock Laboratory:** Demonstration and detection of Coffman conditions (mutual exclusion, hold & wait, no preemption, circular wait).
  * **Memory Allocator:** Custom free-list allocator demonstrating allocation, deallocation, coalescing, alignment, and fragmentation analysis.
  * **Virtual Memory Simulator:** Paging simulator tracking page faults, frames, hit rates, and replacement policies (FIFO, LRU, Optimal).
  * **IPC & Networking:** Educational implementations of pipes, shared memory, Unix domain sockets, TCP/UDP servers, and non-blocking event loops (`select`, `poll`, `epoll`).
  * **Storage Engine:** Educational key-value store with MemTable, Write-Ahead Log (WAL), append-only logs, and crash recovery.

### Layer C — QUANTUM COMPUTE (High-Performance Computing Layer)
* **Runtime Language:** C++20, SIMD/Multithreading, and CUDA (with CPU-Only Fallbacks)
* **Core Responsibilities:**
  * **Algorithm Laboratory:** Graph algorithms (Dijkstra, Bellman-Ford, A*, Max Flow), Dynamic Programming, String algorithms (KMP, Z-Algorithm, Trie), and Numerical Computing (matrix operations, numerical integration, Monte Carlo).
  * **Parallel Computing:** Thread-level parallelism, data parallelism, reductions, and empirical verification of Amdahl's Law.
  * **CUDA Engine:** High-performance kernels for vector addition, matrix multiplication, tiled GEMM, reductions, histograms, and prefix scans.
  * **CPU-Only Graceful Fallback:** Every GPU kernel has an exact CPU reference implementation. Host capability detection routes workloads to CPU when CUDA is absent.
  * **Unified Benchmark Framework:** Objective measurement recording runtime, memory high-water mark, throughput, speedup, and hardware specs across implementations.

---

## 3. Data & Telemetry Flow

The platform bridges high-level AI queries to systems measurements:

```text
User asks: "Benchmark matrix multiplication."
   │
   ▼
AI Agent identifies required tool: `benchmark_runner`
   │
   ▼
Permission check: Tool is executable without mutation -> Approved
   │
   ▼
Systems Runtime invokes C++ / CUDA benchmark executable
   │
   ▼
Execution Engine runs:
   1. CPU Single-Threaded Reference
   2. CPU Multi-Threaded Parallel Version
   3. CUDA Kernel (if GPU present; otherwise flagged as unavailable)
   │
   ▼
Benchmark Collector records:
   - input_size (N x N)
   - threads used
   - wall_clock_runtime_ms
   - memory_bytes
   - calculated GFLOPS
   - speedup ratio
   │
   ▼
AI Agent synthesizes results, identifies bottlenecks (e.g. memory bandwidth vs compute bound), and outputs explanation
   │
   ▼
Web Dashboard visualizes comparative performance curves
```

---

## 4. Hardware Detection & Execution Strategy

1. **At Application Startup**:
   - The systems runtime executes `titan::HardwareProbe` to inspect physical/logical cores, CPU architecture, total RAM, and GPU capability via CUDA runtime query (`cudaGetDeviceCount`).
2. **If CUDA Hardware & Toolchain are Present**:
   - Compiles CUDA engine (`titan_cuda`).
   - Enables GPU benchmarking and profiling.
3. **If CUDA is Absent (Current Host)**:
   - CMake sets `-DTITAN_CPU_ONLY=1`.
   - `titan::HardwareProbe` reports `cuda_available: false`.
   - All benchmarks execute CPU single-threaded and CPU multi-threaded variants.
   - UI explicitly displays `Hardware: CPU-Only Mode (No GPU Detected)`.
   - No GPU speedup is faked or hardcoded.

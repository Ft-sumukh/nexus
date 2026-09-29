# NEXUS TITAN

### AI Systems, Runtime & High-Performance Computing Laboratory

> **NEXUS TITAN** is an integrated engineering and research platform demonstrating how intelligent AI applications connect to the underlying computing systems that execute them.

```text
AI Application ➔ AI Runtime ➔ Backend ➔ Operating System ➔ Networking ➔ CPU ➔ Memory ➔ GPU / CUDA
```

[![C++20](https://img.shields.io/badge/C%2B%2B-20-blue.svg)](https://isocpp.org/)
[![CMake](https://img.shields.io/badge/CMake-3.25%2B-red.svg)](https://cmake.org/)
[![Python](https://img.shields.io/badge/Python-3.12%2B-brightgreen.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115%2B-teal.svg)](https://fastapi.tiangolo.com/)
[![Node Version](https://img.shields.io/badge/Node-%3E%3D20.0.0-green.svg)](https://nodejs.org/)
[![TypeScript](https://img.shields.io/badge/TypeScript-5.x-blue.svg)](https://www.typescriptlang.org/)
[![License](https://img.shields.io/badge/License-Proprietary-red.svg)](#)

---

## Table of Contents
1. [Core Purpose & Philosophy](#core-purpose--philosophy)
2. [The Three-Layer Architecture](#the-three-layer-architecture)
3. [The End-to-End Computing Journey](#the-end-to-end-computing-journey)
4. [Engineering Constitution](#engineering-constitution)
5. [Hardware-Aware Execution & CPU-Only Mode](#hardware-aware-execution--cpu-only-mode)
6. [Repository Structure](#repository-structure)
7. [Getting Started & Local Setup](#getting-started--local-setup)
8. [Unified Verification & Testing](#unified-verification--testing)
9. [20-Phase Master Roadmap](#20-phase-master-roadmap)
10. [Current Status & Next Steps](#current-status--next-steps)

---

## Core Purpose & Philosophy

NEXUS TITAN answers the foundational questions bridging AI and Systems:
* How do modern AI applications retrieve knowledge?
* How do LLM applications securely call tools?
* How do agents maintain explicit state?
* How are concurrent AI workloads scheduled across CPUs and threads?
* How do processes, memory allocators, and event loops interact with inference pipelines?
* At what matrix dimension does GPU acceleration overcome host-to-device memory transfer overhead?
* What is the real system bottleneck under memory-bandwidth-bound vs compute-bound workloads?

### Foundational Principles
```text
CORRECTNESS ➔ MEASUREMENT ➔ REPRODUCIBILITY ➔ SECURITY ➔ PERFORMANCE ➔ EXPLAINABILITY
```

---

## The Three-Layer Architecture

NEXUS TITAN is structured into three connected domains:

### 1. Layer A — NEXUS (Intelligent Application Layer)
* **Stack:** Python (FastAPI, Pydantic) & TypeScript (React / Next.js)
* **Capabilities:** Central AI Runtime, LLM Provider Abstraction (Remote, Local, and Transparent Mock), RAG Pipeline, Controlled Tool Registry with approval gates, Finite State Machine Agents, AI Security, and MLOps tracking.

### 2. Layer B — TITAN (Systems Infrastructure Layer)
* **Stack:** Modern C++ (C++20), CMake, Ninja, MSVC / Clang / GCC
* **Capabilities:** Process manager & supervisor (`fork`, `exec`, signals), production thread pool with bounded queue, CPU scheduling simulator (FCFS, SJF, RR, MLFQ), custom memory allocator (fragmentation metrics), virtual memory simulator, non-blocking networking, and key-value storage engine with Write-Ahead Logging (WAL).

### 3. Layer C — QUANTUM COMPUTE (High-Performance Computing Layer)
* **Stack:** C++20 Multithreading / SIMD & CUDA (with CPU reference fallbacks)
* **Capabilities:** Algorithm laboratory (Graph, Dynamic Programming, Numerical computing), parallel computing benchmarks (Amdahl's law validation), CUDA kernels (GEMM, reductions, prefix scan), and unified benchmark framework.

---

## The End-to-End Computing Journey

```text
                         USER
                           │
                           ▼
                    WEB APPLICATION
                           │
                           ▼
                      API SERVER
                           │
                  AI ORCHESTRATOR
                           │
          ┌────────────────┼────────────────┐
          ▼                ▼                ▼
       RAG Engine     Tool System     Agent Runtime
          │                │                │
          └────────────────┼────────────────┘
                           ▼
                      LLM GATEWAY
                           │
                ┌──────────┴──────────┐
                ▼                     ▼
           Model Provider        Local Model
                                      │
                                      ▼
                               Inference Runtime
                                      │
                         ┌────────────┴────────────┐
                         ▼                         ▼
                       CPU                       GPU
                         │                         │
                         ▼                         ▼
                   SYSTEM RUNTIME             CUDA ENGINE
                         │
              ┌──────────┼──────────┐
              ▼          ▼          ▼
          Processes    Memory    Network
              │          │          │
              └──────────┼──────────┘
                         ▼
                     STORAGE
```

---

## Engineering Constitution

NEXUS TITAN strictly adheres to the [Engineering Constitution](docs/constitution.md):
1. **No Fake Performance:** Every metric must be measured directly on host hardware executing real code. No unsubstantiated claims (e.g. "10x faster") are permitted.
2. **No Fake AI:** Models must execute real inference; offline/test environments utilize transparent mock providers explicitly tagged `[MOCK_PROVIDER / DEMO_MODE]`.
3. **No Unsafe System Access:** Agents never receive unrestricted host shell, filesystem, or network access. Mutating tools enforce permission checks and human approval gates.
4. **Hardware-Aware Execution:** Systems compile and run with 100% functionality on CPU-only machines. GPU features degrade gracefully with explicit `cuda_available: false` telemetry.
5. **Reproducibility:** Benchmarks log input size, hardware specs, thread counts, speedups, and git commit hashes.

---

## Hardware-Aware Execution & CPU-Only Mode

The platform dynamically interrogates host hardware at startup using the native C++ `titan::HardwareProbe`.

* When CUDA hardware and `nvcc` are present: The CUDA engine compiles and GPU benchmarks run with CPU equivalence verification.
* When CUDA is absent (such as CPU-only development environments): CMake automatically configures `-DTITAN_CPU_ONLY=1`. The system executes CPU reference implementations, and telemetry honestly reports:
  ```text
  Hardware: CPU-Only Mode (No GPU Detected)
  CUDA Available: NO (CPU Fallback Active)
  ```

---

## Repository Structure

```text
nexus/
├── CMakeLists.txt              # Root C++20 CMake configuration
├── docker-compose.yml          # Container stack (Postgres, Redis, API, Web)
├── pyproject.toml              # Python package & pytest configuration
├── package.json                # TypeScript & web dependencies
├── tsconfig.json               # TypeScript configuration
├── vitest.config.ts            # Vitest unit & integration test runner
├── .env.example                # Unified environment variables
├── README.md                   # This project manual
│
├── apps/                       # Application entry points
│   ├── api/                    # FastAPI backend service (main.py)
│   └── web/                    # Presentation shell
│
├── ai/                         # Layer A: AI Application Infrastructure
│   ├── runtime/                # Central AI Runtime (core.py, schema.py)
│   ├── llm/                    # Provider abstraction (base.py, mock.py)
│   ├── tools/                  # Controlled tools & registry (base.py, registry.py)
│   ├── agents/                 # State machine & lifecycle (state.py)
│   ├── rag/                    # RAG engine foundation
│   ├── evaluation/             # Retrieval & grounding metrics
│   ├── security/               # Prompt injection defense
│   └── mlops/                  # Experiment tracking
│
├── systems/                    # Layer B: TITAN Systems Infrastructure (C++20)
│   ├── CMakeLists.txt          # Systems layer CMake build target
│   └── runtime/                # Hardware probe & telemetry
│       ├── include/titan/      # C++ headers (hardware_probe.hpp)
│       ├── src/                # C++ source (hardware_probe.cpp)
│       └── tests/              # CTest test suite (test_hardware_probe.cpp)
│
├── algorithms/                 # Layer C: Algorithm Laboratory
├── cuda/                       # Layer C: CUDA & CPU Fallback Kernels
├── benchmarks/                 # Unified Benchmark Framework
├── experiments/                # Research Experiment Framework
├── datasets/                   # Test datasets and evaluation benchmarks
├── docs/                       # Specifications & records
│   ├── constitution.md         # Inviolable Engineering Constitution
│   ├── architecture.md         # Master System Architecture
│   └── roadmap.md              # 20-Phase Master Roadmap
├── infrastructure/             # Dockerfiles & deployment
│   └── docker/
│       ├── Dockerfile.api
│       └── Dockerfile.web
├── scripts/                    # Build & verification automation
│   ├── build_systems.ps1       # CMake build & CTest runner
│   ├── build_systems.bat       # Native MSVC / Ninja batch builder
│   └── run_checks.ps1          # Unified quality runner across all 3 stacks
└── tests/                      # Automated test suite
    ├── ai/                     # Python AI tests (pytest)
    ├── systems/                # Systems tests
    └── integration/            # HTTP integration tests (vitest)
```

---

## Getting Started & Local Setup

### Prerequisites
* **C++ Compiler:** Visual Studio 2022 Community (MSVC `cl.exe`) or GCC 12+ / Clang 15+
* **Build System:** CMake 3.25+ and Ninja
* **Python:** Python 3.12+ (tested on Python 3.14)
* **Node.js:** Node.js 20+ (tested on Node.js 22 LTS)

### Quickstart

1. **Clone and Setup:**
   ```bash
   git clone https://github.com/Ft-sumukh/nexus.git
   cd nexus
   ```

2. **Run Unified Verification:**
   On Windows (PowerShell):
   ```powershell
   .\scripts\run_checks.ps1
   ```

3. **Build C++ Systems Layer Independently:**
   ```powershell
   .\scripts\build_systems.ps1
   ```

4. **Run Python AI Runtime Tests:**
   ```bash
   python -m pytest tests/ai -v
   ```

5. **Run TypeScript Tests:**
   ```bash
   npm test
   ```

6. **Start Local Docker Services (PostgreSQL + Redis):**
   ```bash
   docker compose up -d postgres redis
   ```

---

## 20-Phase Master Roadmap

* [x] **Phase 00:** Engineering Constitution (`docs/constitution.md`)
* [x] **Phase 01:** Repository & Development Foundation (C++20, Python, TS, CMake, CI)
* [ ] **Phase 02:** AI Runtime Foundation
* [ ] **Phase 03:** LLM Gateway
* [ ] **Phase 04:** RAG Engine
* [ ] **Phase 05:** Tool Calling & Agent Runtime
* [ ] **Phase 06:** AI Evaluation
* [ ] **Phase 07:** AI Security
* [ ] **Phase 08:** MLOps Infrastructure
* [ ] **Phase 09:** Process & Thread Runtime
* [ ] **Phase 10:** CPU Scheduling & Synchronization
* [ ] **Phase 11:** Memory & Virtual Memory
* [ ] **Phase 12:** IPC & Networking
* [ ] **Phase 13:** Storage Engine
* [ ] **Phase 14:** Algorithm Laboratory
* [ ] **Phase 15:** Parallel Computing
* [ ] **Phase 16:** CUDA / GPU Engine
* [ ] **Phase 17:** Performance Engineering
* [ ] **Phase 18:** Unified Runtime Integration
* [ ] **Phase 19:** Security & Reliability
* [ ] **Phase 20:** Research Experiments & Publication

See [docs/roadmap.md](docs/roadmap.md) for detailed deliverables and exit criteria.

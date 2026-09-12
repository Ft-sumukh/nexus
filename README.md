# NEXUS — Connected Operational Platform

> **NEXUS** connects: **Users + Data + Systems + Intelligence + Automation + Workflows**

[![Node Version](https://img.shields.io/badge/node-%3E%3D20.0.0-brightgreen.svg)](https://nodejs.org/)
[![TypeScript](https://img.shields.io/badge/TypeScript-5.x-blue.svg)](https://www.typescriptlang.org/)
[![Fastify](https://img.shields.io/badge/Fastify-5.x-black.svg)](https://www.fastify.io/)
[![Architecture](https://img.shields.io/badge/Architecture-Modular%20Monolith-orange.svg)](#high-level-architecture)
[![License](https://img.shields.io/badge/License-Proprietary-red.svg)](#)

---

## Table of Contents
1. [Overview & Vision](#overview--vision)
2. [Current Status](#current-status)
3. [High-Level Architecture](#high-level-architecture)
4. [Technology Stack](#technology-stack)
5. [Repository Structure](#repository-structure)
6. [Local Setup & Getting Started](#local-setup--getting-started)
7. [Environment Configuration](#environment-configuration)
8. [Development Commands](#development-commands)
9. [Testing Strategy](#testing-strategy)
10. [Master Roadmap](#master-roadmap)
11. [Engineering Principles](#engineering-principles)

---

## Overview & Vision

**NEXUS** is an enterprise-grade operational software platform designed to integrate structured enterprise data, user-driven workflows, external software systems, and intelligent automation into a unified, extensible environment.

Rather than fragmenting into distributed microservices prematurely or descending into an unmanageable monolithic codebase, NEXUS follows the **Modular Monolith** pattern with strict Clean Architecture boundaries (Presentation $\to$ Application $\to$ Domain $\to$ Infrastructure).

---

## Current Status

- **Active Phase:** **Phase 1 — Project Foundation & Master Specification** (Completed)
- **Next Phase:** **Phase 2 — Repository & Development Environment**
- **System State:** Clean, verified runnable baseline with strict TypeScript, Zod environment validation, structured Pino logging, Fastify application factory with RFC 7807 problem details, health endpoints, and automated unit/integration tests.

---

## High-Level Architecture

NEXUS enforces clean inward-pointing dependencies:

```
+-------------------------------------------------------------+
|                     Presentation Layer                      |
|       Fastify HTTP Routes, Controllers, RFC 7807 Errors     |
+------------------------------+------------------------------+
                               |
                               v
+------------------------------+------------------------------+
|                     Application Layer                       |
|           Use Cases, DTOs, Port Interfaces                  |
+------------------------------+------------------------------+
                               |
                               v
+------------------------------+------------------------------+
|                        Domain Layer                         |
|        Entities, Aggregates, Domain Rules & Errors          |
+------------------------------+------------------------------+
                               ^
                               | implements ports
+------------------------------+------------------------------+
|                    Infrastructure Layer                     |
|    PostgreSQL (Drizzle), Pino Logger, AI Adapters           |
+-------------------------------------------------------------+
```

Key architectural standards:
- **API-First Design**: Uniform RESTful JSON interfaces with standardized RFC 7807 Problem Details for all errors.
- **Port-and-Adapter Isolation**: Database adapters, external service integrations, and future AI providers sit strictly behind application port interfaces.
- **Multi-Tenancy Readiness**: Baseline shared-database isolation using `tenant_id` scoping and PostgreSQL Row-Level Security, with a decoupled repository pattern allowing schema-per-tenant upgrades.

See the complete architectural design in [docs/architecture/system-architecture.md](docs/architecture/system-architecture.md).

---

## Technology Stack

| Layer / Concern | Technology | Selection Justification |
|---|---|---|
| **Runtime** | **Node.js 22 LTS** | Industry-standard async runtime with native ESM and top performance. |
| **Language** | **TypeScript 5.x** | End-to-end static typing, compile-time safety, zero-cost abstractions. |
| **HTTP Framework** | **Fastify 5.x** | High throughput, native JSON schema validation, encapsulated plugin design. |
| **Logging** | **Pino 9.x** | Blazingly fast, structured JSON logging with correlation ID tracing. |
| **Validation** | **Zod 3.x** | Defensive schema validation for config, incoming requests, and boundaries. |
| **Testing** | **Vitest 3.x** | Fast, zero-config ESM and TypeScript test runner with built-in mocking. |
| **Database Target** | **PostgreSQL + Drizzle ORM** | Type-safe SQL queries, explicit migrations, zero runtime overhead (Phase 4+). |

See Architecture Decision Records for details:
- [ADR-001: Modular Monolith Architecture](docs/decisions/ADR-001-modular-monolith-architecture.md)
- [ADR-002: Technology Stack Selection](docs/decisions/ADR-002-technology-stack-selection.md)
- [ADR-003: Multi-Tenancy Strategy](docs/decisions/ADR-003-data-isolation-strategy.md)
- [ADR-004: Standardized Error Handling](docs/decisions/ADR-004-standardized-error-handling.md)

---

## Repository Structure

```
nexus/
├── .env.example                # Documented environment variable template
├── .gitignore                  # Git ignore rules for node, dist, and secrets
├── package.json                # Project dependencies and script runner
├── tsconfig.json               # Strict TypeScript configuration (NodeNext)
├── vitest.config.ts            # Vitest unit & integration test runner config
├── README.md                   # This project manual
├── docs/                       # Project documentation
│   ├── architecture/           # System architecture specifications
│   │   └── system-architecture.md
│   ├── decisions/              # Architecture Decision Records (ADRs)
│   │   ├── ADR-001-modular-monolith-architecture.md
│   │   ├── ADR-002-technology-stack-selection.md
│   │   ├── ADR-003-data-isolation-strategy.md
│   │   └── ADR-004-standardized-error-handling.md
│   ├── product/                # Product discovery & specifications
│   │   └── specification.md
│   └── roadmap.md              # 19-phase master implementation roadmap
├── src/                        # Application source code
│   ├── config/                 # Environment validation via Zod
│   │   └── index.ts
│   ├── domain/                 # Domain models, errors, and pure business rules
│   │   └── errors/
│   │       └── index.ts
│   ├── application/            # Application use cases, ports, and DTOs (Phase 3+)
│   ├── infrastructure/         # Logger, database adapters, external clients
│   │   └── logging/
│   │       └── logger.ts
│   ├── presentation/           # HTTP controllers, Fastify app factory, routes
│   │   └── http/
│   │       ├── app.ts
│   │       └── routes/
│   │           ├── health.ts
│   │           └── api.ts
│   └── index.ts                # Application bootstrap and graceful shutdown
└── tests/                      # Automated test suite
    ├── unit/                   # Isolated unit tests
    │   ├── config.test.ts
    │   └── errors.test.ts
    └── integration/            # HTTP and component integration tests
        └── health.test.ts
```

---

## Local Setup & Getting Started

### Prerequisites
- **Node.js**: `v20.0.0` or later (tested on `v22.19.0`)
- **npm**: `v10.0.0` or later

### Installation

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd nexus
   ```

2. **Install dependencies:**
   ```bash
   npm install
   ```

3. **Configure the environment:**
   ```bash
   cp .env.example .env
   ```

4. **Verify installation by running tests:**
   ```bash
   npm test
   ```

5. **Start the development server:**
   ```bash
   npm run dev
   ```

The server will be reachable at `http://localhost:3000`.

---

## Environment Configuration

All runtime configuration is managed through environment variables and validated at startup using Zod. See `.env.example` for full options:

| Variable | Default | Description |
|---|---|---|
| `NODE_ENV` | `development` | Runtime environment (`development`, `test`, `production`, `staging`). |
| `PORT` | `3000` | HTTP port the server listens on. |
| `HOST` | `0.0.0.0` | Network binding interface. |
| `LOG_LEVEL` | `info` | Pino logging level (`debug`, `info`, `warn`, `error`). |
| `CORS_ORIGIN` | `*` | Allowed CORS origin. |
| `SESSION_SECRET` | *(dev fallback)* | Secret used for cookie sessions (min 16 chars). |
| `JWT_SECRET` | *(dev fallback)* | Secret used for token verification (min 16 chars). |

---

## Development Commands

| Command | Action |
|---|---|
| `npm run dev` | Starts server in development mode with live watch/reload via `tsx`. |
| `npm run build` | Compiles TypeScript source files into `dist/`. |
| `npm start` | Runs the compiled production build from `dist/index.js`. |
| `npm test` | Runs all unit and integration tests with Vitest. |
| `npm run test:watch` | Runs Vitest in interactive watch mode. |
| `npm run test:coverage`| Executes the test suite and generates code coverage report. |
| `npm run typecheck` | Validates TypeScript types across the project without emitting files. |

---

## Testing Strategy

NEXUS enforces automated testing at every phase:
- **Unit Tests (`tests/unit/`)**: Validates domain logic, error schemas, and config parsing in complete isolation.
- **Integration Tests (`tests/integration/`)**: Validates HTTP routes, request injection, headers, status codes, and database interaction.
- **Run Tests**:
  ```bash
  npm test
  ```

---

## Master Roadmap

Development proceeds sequentially through 19 phases. Key milestones:
- **Phase 01:** Foundation & Master Specification *(Completed)*
- **Phase 02:** Repository & Development Environment *(Next)*
- **Phase 04:** Database & Data Model Foundation
- **Phase 06:** Authentication & Authorization
- **Phase 07:** Core Business Modules
- **Phase 08:** Frontend & Application Shell
- **Phase 10:** AI & Automation Capabilities

Review the full roadmap in [docs/roadmap.md](docs/roadmap.md).

---

## Engineering Principles

1. **Correctness $\to$ Security $\to$ Maintainability $\to$ Simplicity $\to$ Performance $\to$ Scale**
2. **Never skip foundational work.**
3. **No premature abstractions or speculative features.**
4. **Always verify:** Code is not complete until compiled, executed, and tested.

# NEXUS — System Architecture Specification

**Architecture Pattern:** Modular Monolith with Clean Architecture Layers  
**Current Phase:** Phase 1 — Project Foundation & Master Specification  
**Status:** Approved Baseline  

---

## 1. Architectural Philosophy

NEXUS is engineered as a **Modular Monolith**. This pattern delivers the highest developer velocity, simplest deployment topology, and easiest transactional consistency during initial phases, while strictly enforcing bounded context boundaries to allow individual domain modules to be extracted into independent microservices if and when operational scale demands it.

### Core Principles
1. **Simplicity Before Distribution**: No microservices, Kubernetes clusters, or distributed event buses until concrete operational requirements demand them.
2. **Strict Layer Decoupling**: Inward-pointing dependencies. The Domain layer is pure and has zero dependencies on frameworks, databases, or transport mechanisms.
3. **Ports and Adapters (Hexagonal)**: External systems (databases, HTTP clients, AI models, message brokers) are accessed exclusively via domain/application port interfaces implemented in the Infrastructure layer.
4. **Defense in Depth**: Every layer validates its inputs. Never rely on the presentation layer alone for data integrity or security guarantees.

---

## 2. High-Level Layer Architecture

```
+-------------------------------------------------------------------------+
|                          Presentation Layer                             |
|    - HTTP Fastify Routes & Controllers   - Middleware / Hooks          |
|    - Request / Response Serialization     - Swagger / OpenAPI Docs      |
+------------------------------------+------------------------------------+
                                     |
                                     v
+------------------------------------+------------------------------------+
|                          Application Layer                              |
|    - Use Cases & Orchestrators          - Application DTOs              |
|    - Port Interfaces (In / Out)         - Workflow Coordinators         |
+------------------------------------+------------------------------------+
                                     |
                                     v
+------------------------------------+------------------------------------+
|                            Domain Layer                                 |
|    - Domain Entities & Aggregates       - Value Objects                 |
|    - Domain Business Rules              - Domain Events & Errors        |
+------------------------------------+------------------------------------+
                                     ^
                                     | implements ports
+------------------------------------+------------------------------------+
|                       Infrastructure Layer                              |
|    - Persistence (Drizzle ORM)         - External Service Clients       |
|    - Logger (Pino)                     - AI Provider Adapters           |
|    - Environment Config (Zod)          - Message Queue Adapters         |
+-------------------------------------------------------------------------+
```

### Layer Responsibilities

| Layer | Path | Responsibility | Permitted Dependencies |
|---|---|---|---|
| **Presentation** | `src/presentation` | Handles HTTP requests, parses schemas, invokes application use cases, maps errors to RFC 7807 responses. | Application, Domain, Config |
| **Application** | `src/application` | Orchestrates business workflows, defines port interfaces (repositories, external services), transforms DTOs. | Domain |
| **Domain** | `src/domain` | Pure business entities, domain validation rules, domain error hierarchy, domain events. | None (zero external framework dependencies) |
| **Infrastructure** | `src/infrastructure`| Implements application ports (database persistence, caching, logging, external APIs, AI adapters). | Domain, Application, Third-party libs |
| **Config** | `src/config` | Loads, parses, and validates environment configuration at startup using Zod. | Zod, dotenv |

---

## 3. Cross-Cutting Concerns

Cross-cutting concerns are organized into dedicated modules rather than scattered through business logic:

### 3.1 Error Handling & Problem Details
- All application and domain errors inherit from `AppError` (`src/domain/errors/index.ts`).
- Errors are mapped uniformly in the presentation error handler to **RFC 7807 Problem Details**:
```json
{
  "type": "https://nexus.platform/errors/resource-not-found",
  "title": "NotFound",
  "status": 404,
  "detail": "User with identifier 'usr_123' was not found.",
  "code": "RESOURCE_NOT_FOUND",
  "instance": "/api/v1/users/usr_123",
  "timestamp": "2026-09-12T15:40:00.000Z"
}
```
- In production, unhandled exceptions return a generic message to prevent leaking internal stack traces or database schema details.

### 3.2 Observability & Structured Logging
- Logging uses **Pino** for extreme speed and standard JSON structure.
- Every incoming HTTP request is assigned a unique correlation ID (`x-request-id`), either forwarded from upstream reverse proxies or generated as a UUID v4.
- Standard health probes:
  - `GET /health/live`: Liveness probe for process uptime.
  - `GET /health/ready`: Readiness probe checking critical dependencies (e.g. database connectivity).
  - `GET /health`: Comprehensive metrics (uptime, memory usage, environment).

### 3.3 Security Baseline
- **Strict Input Validation**: Every endpoint defines explicit input schemas.
- **Header Hardening**: Fastify security headers (HSTS, Content Security Policy, X-Frame-Options, X-Content-Type-Options).
- **Graceful Lifecycle**: Process intercepts `SIGTERM` and `SIGINT` to safely drain traffic before exiting.

---

## 4. Multi-Tenancy Strategy (Phase 4+)

NEXUS is designed to support multi-tenant operational data. The evaluated models are:

1. **Shared Database / Shared Table with Tenant ID (Selected Baseline)**:
   - Every tenant-owned database record includes a `tenant_id` foreign key.
   - Tenancy is enforced at the data-access repository layer through scoped queries and PostgreSQL Row-Level Security (RLS).
   - **Trade-offs**: Optimal cost, simplified migrations, excellent resource utilization; requires strict enforcement in query abstractions.
2. **Shared Database / Separate Schema (Enterprise Upgrade Path)**:
   - One PostgreSQL schema per tenant (`tenant_acme`, `tenant_beta`).
   - Stronger logical isolation; migration orchestration is more complex.
3. **Database-per-tenant (High-Compliance Dedicated Tier)**:
   - Dedicated database instance for demanding enterprise tenants.

The system will start with Model 1 (Shared Database / Shared Table with `tenant_id`), with the repository abstraction designed to easily swap in Model 2 or 3 for enterprise customers without rewriting domain business logic.

---

## 5. AI & Extensibility Architecture (Phase 10+)

To prevent vendor lock-in and preserve code cleanliness, AI features will interact with an abstract port:

```typescript
export interface AiGatewayPort {
  generateText(prompt: string, context: Record<string, unknown>): Promise<string>;
  generateStructuredOutput<T>(prompt: string, schema: z.ZodSchema<T>): Promise<T>;
  createEmbeddings(text: string): Promise<number[]>;
}
```

Adapters will be implemented in `src/infrastructure/ai/` for providers such as Google Gemini, OpenAI, or local Ollama instances. Business use cases will depend solely on `AiGatewayPort`.

---

## 6. Testing Strategy

The system enforces a balanced testing pyramid:

```
        /   E2E Tests   \        Critical end-to-end user workflows
       /  Integration   \       Fastify HTTP injection, DB queries, migrations
      /   Unit Tests     \      Domain business logic, validators, DTO mappers
```

- **Unit Tests**: Test pure domain logic, error formatting, and configuration parsing in isolation (sub-second execution via Vitest).
- **Integration Tests**: Test Fastify route handlers, database queries, and repository implementations against realistic environments.
- **E2E Tests**: Test high-level API workflows and eventual frontend user journeys.

# ADR-002: Core Technology Stack & Framework Selection

## Status
Accepted

## Context
NEXUS requires a robust, scalable, secure, and maintainable technology foundation that supports rapid development without sacrificing type safety or long-term production quality. The chosen stack must provide strong typing, high asynchronous throughput, an active open-source ecosystem, and compatibility with modern containerized environments.

## Decision
We select the following core technology stack:

1. **Runtime & Language**: **TypeScript 5.x on Node.js 22 LTS (ESM)**
   - *Why*: End-to-end type safety across application boundaries, shared validation models (Zod), massive talent pool, superior asynchronous I/O capabilities, and native modern ECMAScript module support in Node 22.
   - *Alternatives Considered*:
     - *Go*: High performance and simple concurrency, but slower velocity for dynamic business domains and lacking unified schema/type sharing with TypeScript frontends.
     - *Python (FastAPI)*: Excellent for AI scripting, but weaker concurrency under CPU/IO mixed workloads, dynamic typing issues at scale, and fragmented ORM typing.
     - *Java / Kotlin (Spring Boot)*: Highly enterprise-capable, but heavy memory footprint, slower startup times, and higher development ceremony.
   - *Replaceability*: Baseline platform choice.

2. **Backend Web Framework**: **Fastify**
   - *Why*: Exceptional performance (up to 2x faster than Express), native JSON schema validation, encapsulated plugin architecture (ideal for modular monoliths), first-class Pino logger integration, and native async/await lifecycle hooks.
   - *Alternatives Considered*:
     - *Express*: Widespread familiarity, but unmaintained for long stretches, callback-oriented legacy architecture, slower performance, and lacks built-in schema validation.
     - *NestJS*: Highly structured, but introduces heavy abstraction overhead (decorators, reflection metadata, DI ceremony) that adds unnecessary complexity at this stage.
   - *Replaceability*: Replaceable at the Presentation layer; domain and application layers remain framework-agnostic.

3. **Validation & Configuration**: **Zod**
   - *Why*: Declarative, developer-friendly schema definition with zero compilation step, automatic TypeScript type inference, and defensive parsing at system boundaries.
   - *Alternatives Considered*: Joi, Yup, TypeBox.
   - *Replaceability*: Replaceable via validation adapters.

4. **Testing Framework**: **Vitest**
   - *Why*: Native TypeScript and ESM support out of the box, zero-configuration transpilation, compatibility with Jest APIs, and blazingly fast execution.
   - *Alternatives Considered*: Jest (slower, requires complex Babel/ts-jest configurations for ESM), Mocha.
   - *Replaceability*: Replaceable.

5. **Data Persistence Target (Phase 4+)**: **PostgreSQL with Drizzle ORM**
   - *Why*: PostgreSQL is the premier open-source relational database with robust JSON support, row-level security (RLS), and full-text search. Drizzle ORM provides lightweight, type-safe SQL queries with zero runtime overhead and explicit migration management.
   - *Alternatives Considered*: Prisma (heavy binary engine, schema lock-in, connection pooling friction), TypeORM (legacy active record patterns, loose typing).
   - *Replaceability*: Replaceable at the Infrastructure layer.

## Consequences
### Positive
- Unified language (TypeScript) simplifies developer workflows and enables seamless type sharing.
- Fastify's encapsulated plugin model natively mirrors our modular monolith boundaries.
- Zod prevents invalid state and configuration from poisoning application layers.
- Fast test feedback cycle with Vitest.

### Negative
- Asynchronous Node.js requires careful CPU-bound task offloading (e.g. heavy crypto or image processing should use worker threads or background workers).

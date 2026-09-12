# ADR-003: Multi-Tenancy and Data Isolation Strategy

## Status
Accepted

## Context
NEXUS will support multi-tenant operations where multiple organizations or customer accounts store data within the platform. Ensuring strict tenant data isolation is a critical security and privacy requirement. Cross-tenant data leakage is unacceptable.

Three tenancy models were evaluated:
1. **Shared Database / Shared Table (Row-Level Isolation)**: All tenants share the same database and tables. Every table includes a `tenant_id` column.
2. **Shared Database / Separate Schemas**: Each tenant has an isolated PostgreSQL schema within a shared database instance.
3. **Database-per-Tenant**: Each tenant has a dedicated PostgreSQL database instance.

## Decision
We adopt a **Shared Database / Shared Table model with explicit tenant scoping and PostgreSQL Row-Level Security (RLS)** as the primary baseline, while architecting the data-access layer to support **Separate Schemas** for enterprise tenants requiring dedicated compliance.

### Implementation Rules:
1. Every tenant-scoped entity in the domain must include a `tenantId` property.
2. All repository queries must automatically inject the authenticated `tenantId` as a query filter.
3. Background jobs, analytics, and AI workflows must run in an explicit tenant context.
4. Database connections will utilize PostgreSQL Row-Level Security (RLS) policies as a secondary defense layer in Phase 4.

## Consequences
### Positive
- Cost-effective and highly scalable for hundreds to thousands of organizations.
- Uniform schema migration across all tenants with a single migration command.
- Efficient connection pooling and resource utilization.

### Negative
- Developers must exercise discipline never to execute un-scoped queries; requires automated test assertions and RLS policies to prevent human error.

## Replaceability
Replaceable. By isolating data access behind repository interfaces in the Infrastructure layer, tenant routing can be updated to point to separate schemas or separate databases without modifying application or domain logic.

# ADR-004: Standardized Error Handling and RFC 7807 Problem Details

## Status
Accepted

## Context
APIs that lack a standardized error schema create friction for frontend consumers, third-party developers, and automated integrations. Typical anti-patterns include returning generic `500 Internal Server Error` strings, inconsistent JSON error shapes (`{ "err": "..." }` vs `{ "message": "..." }`), or inadvertently leaking internal database error messages, SQL queries, and stack traces to clients.

## Decision
NEXUS adopts the **RFC 7807 (Problem Details for HTTP APIs)** standard for all API error responses.

### Error Envelope Schema
```json
{
  "type": "https://nexus.platform/errors/<error-code-kebab>",
  "title": "<Short Human-Readable Summary>",
  "status": <HTTP Status Code>,
  "detail": "<Specific occurrence explanation>",
  "code": "<MACHINE_READABLE_CODE>",
  "instance": "<Request Path or Resource URI>",
  "errors": [
    {
      "field": "<Optional field name for validation errors>",
      "message": "<Field-specific error message>",
      "code": "<Optional sub-code>"
    }
  ],
  "timestamp": "<ISO-8601 Timestamp>"
}
```

### Domain Error Mapping
- Domain and application errors inherit from an abstract `AppError` base class (`src/domain/errors/index.ts`).
- Concrete subclasses (`NotFoundError`, `ValidationError`, `UnauthorizedError`, `ForbiddenError`, `ConflictError`, `RateLimitError`, `InternalError`) define their respective HTTP status codes and machine-readable error codes.
- The Fastify presentation layer intercepts these errors and transforms them via `toProblemDetails()`.
- Unhandled internal exceptions are logged with full stack traces at `logger.error()`, while returning sanitized generic 500 problem details in production.

## Consequences
### Positive
- Predictable, machine-readable contract for all API consumers and client SDKs.
- Clear separation between operational client errors (4xx) and unexpected server defects (500).
- Protection against information leakage in production environments.

### Negative
- All endpoints must route exceptions through the centralized error hierarchy rather than emitting raw responses.

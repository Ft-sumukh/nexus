import { describe, it, expect } from 'vitest';
import {
  AppError,
  NotFoundError,
  ValidationError,
  UnauthorizedError,
  ForbiddenError,
  ConflictError,
  RateLimitError,
  InternalError,
} from '../../src/domain/errors/index.js';

describe('Domain Errors & Problem Details', () => {
  it('NotFoundError should produce 404 problem details', () => {
    const error = new NotFoundError('User', 'usr_123');
    expect(error.statusCode).toBe(404);
    expect(error.errorCode).toBe('RESOURCE_NOT_FOUND');
    expect(error.message).toBe("User with identifier 'usr_123' was not found.");

    const details = error.toProblemDetails('/api/v1/users/usr_123');
    expect(details.status).toBe(404);
    expect(details.title).toBe('NotFound');
    expect(details.type).toContain('resource-not-found');
    expect(details.instance).toBe('/api/v1/users/usr_123');
    expect(details.timestamp).toBeDefined();
  });

  it('ValidationError should include field details when provided', () => {
    const error = new ValidationError('Invalid input data', [
      { field: 'email', message: 'Must be a valid email address', code: 'INVALID_EMAIL' },
    ]);
    expect(error.statusCode).toBe(400);
    expect(error.errorCode).toBe('VALIDATION_FAILED');
    expect(error.errors).toHaveLength(1);

    const details = error.toProblemDetails();
    expect(details.status).toBe(400);
    expect(details.errors?.[0]?.field).toBe('email');
  });

  it('UnauthorizedError and ForbiddenError should have 401 and 403 status codes', () => {
    const unauth = new UnauthorizedError();
    expect(unauth.statusCode).toBe(401);
    expect(unauth.errorCode).toBe('UNAUTHORIZED');

    const forbidden = new ForbiddenError();
    expect(forbidden.statusCode).toBe(403);
    expect(forbidden.errorCode).toBe('FORBIDDEN');
  });

  it('ConflictError and RateLimitError should have 409 and 429 status codes', () => {
    const conflict = new ConflictError('User email already exists');
    expect(conflict.statusCode).toBe(409);

    const rateLimit = new RateLimitError();
    expect(rateLimit.statusCode).toBe(429);
  });

  it('InternalError should encapsulate root cause', () => {
    const rootCause = new Error('Database connection timeout');
    const internal = new InternalError('Failed to query records', rootCause);
    expect(internal.statusCode).toBe(500);
    expect(internal.cause).toBe(rootCause);
  });
});

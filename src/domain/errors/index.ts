/**
 * RFC 7807 Problem Details representation.
 */
export interface ProblemDetails {
  type: string;
  title: string;
  status: number;
  detail: string;
  instance?: string;
  code?: string;
  errors?: Array<{
    field?: string;
    message: string;
    code?: string;
  }>;
  timestamp: string;
}

/**
 * Base Application Error class.
 * All domain and application errors inherit from this class.
 */
export abstract class AppError extends Error {
  public abstract readonly statusCode: number;
  public abstract readonly errorCode: string;
  public readonly isOperational: boolean = true;
  public readonly errors?: Array<{ field?: string; message: string; code?: string }>;

  constructor(
    message: string,
    options?: {
      cause?: unknown;
      errors?: Array<{ field?: string; message: string; code?: string }>;
    }
  ) {
    super(message);
    this.name = this.constructor.name;
    if (options?.cause) {
      this.cause = options.cause;
    }
    if (options?.errors) {
      this.errors = options.errors;
    }
    Error.captureStackTrace(this, this.constructor);
  }

  public toProblemDetails(instance?: string): ProblemDetails {
    return {
      type: `https://nexus.platform/errors/${this.errorCode.toLowerCase().replace(/_/g, '-')}`,
      title: this.name.replace(/Error$/, ''),
      status: this.statusCode,
      detail: this.message,
      code: this.errorCode,
      ...(this.errors && { errors: this.errors }),
      ...(instance && { instance }),
      timestamp: new Date().toISOString(),
    };
  }
}

export class NotFoundError extends AppError {
  public readonly statusCode = 404;
  public readonly errorCode = 'RESOURCE_NOT_FOUND';

  constructor(resource: string, identifier?: string | number) {
    const detail = identifier
      ? `${resource} with identifier '${identifier}' was not found.`
      : `${resource} was not found.`;
    super(detail);
  }
}

export class ValidationError extends AppError {
  public readonly statusCode = 400;
  public readonly errorCode = 'VALIDATION_FAILED';

  constructor(
    message: string = 'Validation failed',
    errors?: Array<{ field?: string; message: string; code?: string }>
  ) {
    super(message, { errors });
  }
}

export class UnauthorizedError extends AppError {
  public readonly statusCode = 401;
  public readonly errorCode = 'UNAUTHORIZED';

  constructor(message: string = 'Authentication is required to access this resource') {
    super(message);
  }
}

export class ForbiddenError extends AppError {
  public readonly statusCode = 403;
  public readonly errorCode = 'FORBIDDEN';

  constructor(message: string = 'You do not have permission to access this resource') {
    super(message);
  }
}

export class ConflictError extends AppError {
  public readonly statusCode = 409;
  public readonly errorCode = 'CONFLICT';

  constructor(message: string) {
    super(message);
  }
}

export class RateLimitError extends AppError {
  public readonly statusCode = 429;
  public readonly errorCode = 'RATE_LIMIT_EXCEEDED';

  constructor(message: string = 'Too many requests. Please try again later.') {
    super(message);
  }
}

export class InternalError extends AppError {
  public readonly statusCode = 500;
  public readonly errorCode = 'INTERNAL_ERROR';

  constructor(message: string = 'An unexpected internal error occurred', cause?: unknown) {
    super(message, { cause });
  }
}

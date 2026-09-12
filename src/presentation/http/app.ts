import fastify from 'fastify';
import { randomUUID } from 'node:crypto';
import { config } from '../../config/index.js';
import { logger } from '../../infrastructure/logging/logger.js';
import { AppError, NotFoundError } from '../../domain/errors/index.js';
import { healthRoutes } from './routes/health.js';
import { apiRoutes } from './routes/api.js';

export interface BuildAppOptions {
  disableLogging?: boolean;
}

/**
 * Builds and configures the Fastify application instance.
 */
export function buildApp(options: BuildAppOptions = {}) {
  const app = fastify({
    loggerInstance: options.disableLogging ? undefined : logger,
    genReqId: (req) => {
      const headerId = req.headers['x-request-id'];
      if (typeof headerId === 'string' && headerId.length > 0) {
        return headerId;
      }
      return randomUUID();
    },
  });

  // Global Not Found Handler (RFC 7807)
  app.setNotFoundHandler(async (request, reply) => {
    const error = new NotFoundError('Endpoint', request.url);
    return reply.status(404).send(error.toProblemDetails(request.url));
  });

  // Global Error Handler (RFC 7807 Problem Details)
  app.setErrorHandler(async (error: unknown, request, reply) => {
    if (error instanceof AppError) {
      if (error.statusCode >= 500) {
        request.log.error({ err: error }, `Application error: ${error.message}`);
      } else {
        request.log.warn({ err: error }, `Client operational error: ${error.message}`);
      }
      return reply.status(error.statusCode).send(error.toProblemDetails(request.url));
    }

    // Fastify schema validation error
    if (
      typeof error === 'object' &&
      error !== null &&
      'validation' in error &&
      Array.isArray((error as { validation?: unknown[] }).validation)
    ) {
      const fastifyError = error as { message: string; validation: Array<{ instancePath?: string; message?: string; params?: { missingProperty?: string } }> };
      const validationDetails = {
        type: 'https://nexus.platform/errors/validation-failed',
        title: 'Validation Failed',
        status: 400,
        detail: fastifyError.message,
        code: 'VALIDATION_FAILED',
        errors: fastifyError.validation.map((v) => ({
          field: v.instancePath || v.params?.missingProperty,
          message: v.message || 'Invalid value',
        })),
        instance: request.url,
        timestamp: new Date().toISOString(),
      };
      return reply.status(400).send(validationDetails);
    }

    // Unhandled exception
    const errorMessage = error instanceof Error ? error.message : 'Unknown error occurred';
    request.log.error({ err: error }, `Unhandled server exception: ${errorMessage}`);

    const isDev = config.NODE_ENV === 'development' || config.NODE_ENV === 'test';
    const problemDetails = {
      type: 'https://nexus.platform/errors/internal-error',
      title: 'Internal Server Error',
      status: 500,
      detail: isDev ? errorMessage : 'An unexpected error occurred processing your request.',
      code: 'INTERNAL_ERROR',
      instance: request.url,
      timestamp: new Date().toISOString(),
    };

    return reply.status(500).send(problemDetails);
  });

  // Register foundational route plugins
  app.register(healthRoutes);
  app.register(apiRoutes, { prefix: '/api' });

  return app;
}

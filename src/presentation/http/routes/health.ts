import type { FastifyPluginAsync } from 'fastify';
import { config } from '../../../config/index.js';

export const healthRoutes: FastifyPluginAsync = async (fastify) => {
  // Liveness probe: returns 200 if the process is up and listening
  fastify.get('/health/live', async (_request, reply) => {
    return reply.status(200).send({
      status: 'ok',
      probe: 'liveness',
      timestamp: new Date().toISOString(),
    });
  });

  // Readiness probe: returns 200 if the process is ready to handle traffic
  fastify.get('/health/ready', async (_request, reply) => {
    // In Phase 4+, this probe can check database connectivity
    return reply.status(200).send({
      status: 'ok',
      probe: 'readiness',
      timestamp: new Date().toISOString(),
      dependencies: {
        database: 'not_configured_for_phase_1',
      },
    });
  });

  // Comprehensive health status
  fastify.get('/health', async (_request, reply) => {
    const memory = process.memoryUsage();
    return reply.status(200).send({
      status: 'healthy',
      service: config.APP_NAME,
      version: config.APP_VERSION,
      environment: config.NODE_ENV,
      uptime: Math.floor(process.uptime()),
      timestamp: new Date().toISOString(),
      metrics: {
        rssBytes: memory.rss,
        heapUsedBytes: memory.heapUsed,
        heapTotalBytes: memory.heapTotal,
      },
    });
  });
};

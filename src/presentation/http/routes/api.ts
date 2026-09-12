import type { FastifyPluginAsync } from 'fastify';
import { config } from '../../../config/index.js';

export const apiRoutes: FastifyPluginAsync = async (fastify) => {
  fastify.get('/v1', async (_request, reply) => {
    return reply.status(200).send({
      name: 'NEXUS API',
      version: 'v1',
      environment: config.NODE_ENV,
      status: 'operational',
      docsUrl: '/docs',
      modules: {
        foundation: 'active',
        authentication: 'planned_phase_6',
        tenancy: 'planned_phase_4',
        intelligence: 'planned_phase_10',
      },
    });
  });
};

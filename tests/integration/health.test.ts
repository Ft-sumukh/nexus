import { describe, it, expect, beforeAll, afterAll } from 'vitest';
import type { FastifyInstance } from 'fastify';
import { buildApp } from '../../src/presentation/http/app.js';

describe('HTTP Endpoints Integration', () => {
  let app: ReturnType<typeof buildApp>;

  beforeAll(async () => {
    app = buildApp({ disableLogging: true });
    await app.ready();
  });

  afterAll(async () => {
    await app.close();
  });

  it('GET /health returns 200 with service metadata', async () => {
    const response = await app.inject({
      method: 'GET',
      url: '/health',
    });

    expect(response.statusCode).toBe(200);
    const body = JSON.parse(response.body);
    expect(body.status).toBe('healthy');
    expect(body.service).toBe('nexus');
    expect(body.version).toBeDefined();
    expect(body.uptime).toBeGreaterThanOrEqual(0);
    expect(body.metrics).toHaveProperty('heapUsedBytes');
  });

  it('GET /health/live returns 200 for liveness probe', async () => {
    const response = await app.inject({
      method: 'GET',
      url: '/health/live',
    });

    expect(response.statusCode).toBe(200);
    const body = JSON.parse(response.body);
    expect(body.status).toBe('ok');
    expect(body.probe).toBe('liveness');
  });

  it('GET /health/ready returns 200 for readiness probe', async () => {
    const response = await app.inject({
      method: 'GET',
      url: '/health/ready',
    });

    expect(response.statusCode).toBe(200);
    const body = JSON.parse(response.body);
    expect(body.status).toBe('ok');
    expect(body.probe).toBe('readiness');
  });

  it('GET /api/v1 returns 200 with API status descriptor', async () => {
    const response = await app.inject({
      method: 'GET',
      url: '/api/v1',
    });

    expect(response.statusCode).toBe(200);
    const body = JSON.parse(response.body);
    expect(body.name).toBe('NEXUS API');
    expect(body.version).toBe('v1');
    expect(body.status).toBe('operational');
    expect(body.modules).toHaveProperty('foundation');
  });

  it('GET non-existent route returns 404 RFC 7807 Problem Details', async () => {
    const response = await app.inject({
      method: 'GET',
      url: '/unregistered-path',
    });

    expect(response.statusCode).toBe(404);
    const body = JSON.parse(response.body);
    expect(body.status).toBe(404);
    expect(body.title).toBe('NotFound');
    expect(body.code).toBe('RESOURCE_NOT_FOUND');
    expect(body.instance).toBe('/unregistered-path');
  });
});

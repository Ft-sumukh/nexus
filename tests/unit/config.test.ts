import { describe, it, expect } from 'vitest';
import { loadConfig } from '../../src/config/index.js';

describe('Configuration Module', () => {
  it('should load default configuration when minimal environment is provided', () => {
    const config = loadConfig({});
    expect(config.NODE_ENV).toBe('development');
    expect(config.PORT).toBe(3000);
    expect(config.HOST).toBe('0.0.0.0');
    expect(config.LOG_LEVEL).toBe('info');
    expect(config.APP_NAME).toBe('nexus');
    expect(config.TENANCY_MODE).toBe('shared-table');
  });

  it('should override defaults with valid environment variables', () => {
    const config = loadConfig({
      NODE_ENV: 'production',
      PORT: '8080',
      HOST: '127.0.0.1',
      LOG_LEVEL: 'warn',
      APP_NAME: 'nexus-prod',
      TENANCY_MODE: 'schema-per-tenant',
      SESSION_SECRET: 'production-session-secret-min16chars',
      JWT_SECRET: 'production-jwt-secret-min16chars',
    });

    expect(config.NODE_ENV).toBe('production');
    expect(config.PORT).toBe(8080);
    expect(config.HOST).toBe('127.0.0.1');
    expect(config.LOG_LEVEL).toBe('warn');
    expect(config.APP_NAME).toBe('nexus-prod');
    expect(config.TENANCY_MODE).toBe('schema-per-tenant');
  });

  it('should throw an error on invalid port number', () => {
    expect(() => {
      loadConfig({ PORT: 'not-a-number' });
    }).toThrow(/Configuration validation failed/);
  });

  it('should throw an error on invalid environment value', () => {
    expect(() => {
      loadConfig({ NODE_ENV: 'invalid-env' });
    }).toThrow(/Configuration validation failed/);
  });
});

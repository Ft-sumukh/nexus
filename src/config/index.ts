import { z } from 'zod';
import dotenv from 'dotenv';

// Load .env if present
dotenv.config();

/**
 * Environment configuration schema.
 * Validates all required environment variables at process bootstrap.
 */
const environmentSchema = z.object({
  NODE_ENV: z
    .enum(['development', 'test', 'production', 'staging'])
    .default('development'),
  PORT: z
    .string()
    .transform((val) => parseInt(val, 10))
    .pipe(z.number().positive().max(65535))
    .default('3000'),
  HOST: z.string().default('0.0.0.0'),
  LOG_LEVEL: z
    .enum(['fatal', 'error', 'warn', 'info', 'debug', 'trace'])
    .default('info'),
  APP_NAME: z.string().default('nexus'),
  APP_VERSION: z.string().default('0.1.0'),

  // Security
  CORS_ORIGIN: z.string().default('*'),
  SESSION_SECRET: z.string().min(16).default('development-fallback-session-secret-min16'),
  JWT_SECRET: z.string().min(16).default('development-fallback-jwt-secret-min16'),
  JWT_EXPIRES_IN: z.string().default('1h'),

  // Tenancy (Phase 4+)
  TENANCY_MODE: z.enum(['shared-table', 'schema-per-tenant']).default('shared-table'),

  // Database (Phase 4+)
  DATABASE_URL: z.string().optional(),
});

export type Config = z.infer<typeof environmentSchema>;

/**
 * Parses and validates environment variables.
 * Throws a detailed error at startup if the configuration is invalid.
 */
export function loadConfig(env: Record<string, string | undefined> = process.env): Config {
  const result = environmentSchema.safeParse(env);

  if (!result.success) {
    const errorDetails = result.error.issues
      .map((issue) => ` - [${issue.path.join('.')}]: ${issue.message}`)
      .join('\n');
    throw new Error(`Configuration validation failed:\n${errorDetails}`);
  }

  return result.data;
}

export const config = loadConfig();

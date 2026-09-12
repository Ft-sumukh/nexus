import pino from 'pino';
import { config } from '../../config/index.js';

/**
 * Configure Pino structured logger based on environment.
 */
export const logger = pino({
  level: config.LOG_LEVEL,
  transport:
    config.NODE_ENV === 'development'
      ? {
          target: 'pino-pretty',
          options: {
            colorize: true,
            translateTime: 'SYS:yyyy-mm-dd HH:MM:ss.l',
            ignore: 'pid,hostname',
          },
        }
      : undefined,
  base: {
    service: config.APP_NAME,
    version: config.APP_VERSION,
    env: config.NODE_ENV,
  },
  timestamp: pino.stdTimeFunctions.isoTime,
});

/**
 * Creates a child logger with contextual metadata.
 */
export function createChildLogger(module: string, context: Record<string, unknown> = {}) {
  return logger.child({ module, ...context });
}

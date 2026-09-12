import { config } from './config/index.js';
import { logger } from './infrastructure/logging/logger.js';
import { buildApp } from './presentation/http/app.js';

async function main(): Promise<void> {
  logger.info(
    {
      env: config.NODE_ENV,
      version: config.APP_VERSION,
    },
    `Starting ${config.APP_NAME} server...`
  );

  const app = buildApp();

  try {
    const address = await app.listen({
      port: config.PORT,
      host: config.HOST,
    });
    logger.info(`NEXUS server listening at ${address}`);
  } catch (err) {
    logger.fatal({ err }, 'Failed to start NEXUS server');
    process.exit(1);
  }

  // Graceful shutdown handler
  const shutdown = async (signal: string) => {
    logger.info(`Received ${signal}, initiating graceful shutdown...`);
    try {
      await app.close();
      logger.info('NEXUS HTTP server closed gracefully');
      process.exit(0);
    } catch (err) {
      logger.error({ err }, 'Error during graceful shutdown');
      process.exit(1);
    }
  };

  process.on('SIGTERM', () => void shutdown('SIGTERM'));
  process.on('SIGINT', () => void shutdown('SIGINT'));

  process.on('unhandledRejection', (reason) => {
    logger.fatal({ reason }, 'Unhandled promise rejection');
    process.exit(1);
  });

  process.on('uncaughtException', (err) => {
    logger.fatal({ err }, 'Uncaught exception');
    process.exit(1);
  });
}

void main();

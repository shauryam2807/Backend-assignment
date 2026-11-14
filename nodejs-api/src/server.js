/**
 * Server Entrypoint
 * Starts the Express HTTP server with graceful shutdown support.
 */
require('dotenv').config();
const app = require('./app');
const pool = require('./config/database');

const PORT = parseInt(process.env.PORT, 10) || 3000;

const server = app.listen(PORT, () => {
  console.log(`🚀 MFAPIs Node.js API server running on port ${PORT}`);
  console.log(`   Health check: http://localhost:${PORT}/health`);
  console.log(`   Twelve Data Price: http://localhost:${PORT}/price?symbol=BTC/USD`);
});

// ---------------------------------------------------------------------------
// Graceful Shutdown (handles Render, Docker, Kubernetes, and Ctrl+C)
// ---------------------------------------------------------------------------
function gracefulShutdown(signal) {
  console.log(`\n${signal} received — shutting down gracefully...`);
  server.close(async () => {
    console.log('HTTP server closed');
    try {
      await pool.end();
      console.log('PostgreSQL pool closed');
    } catch (err) {
      console.error('Error closing database pool:', err.message);
    }
    process.exit(0);
  });

  // Force exit after 10 seconds if connections don't close
  setTimeout(() => {
    console.error('Forced shutdown after 10s timeout');
    process.exit(1);
  }, 10000);
}

process.on('SIGTERM', () => gracefulShutdown('SIGTERM'));
process.on('SIGINT', () => gracefulShutdown('SIGINT'));

module.exports = server;

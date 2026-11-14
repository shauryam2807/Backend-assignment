/**
 * In-Memory TTL Cache Service
 * 30-second TTL prevents upstream rate limits while ensuring fresh data.
 */
const NodeCache = require('node-cache');

// Standard TTL: 30 seconds, periodic cleanup: every 60 seconds
const cache = new NodeCache({
  stdTTL: 30,
  checkperiod: 60,
  useClones: false,
});

module.exports = cache;


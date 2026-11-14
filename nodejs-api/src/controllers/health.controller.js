/**
 * Health Check Controller
 * Includes database connectivity probe for production monitoring.
 */
const pool = require('../config/database');

exports.getHealth = async (req, res) => {
  let dbStatus = 'unknown';
  let dbLatencyMs = null;

  try {
    const start = Date.now();
    await pool.query('SELECT 1');
    dbLatencyMs = Date.now() - start;
    dbStatus = 'connected';
  } catch (err) {
    dbStatus = 'disconnected';
    console.error('[Health] Database ping failed:', err.message);
  }

  const status = dbStatus === 'connected' ? 'healthy' : 'degraded';

  res.json({
    status,
    service: 'MFAPIs Financial Data Platform (Node.js)',
    version: '2.0.0',
    twelvedata_compatible: true,
    runtime: `Node.js ${process.version}`,
    uptime_seconds: Math.floor(process.uptime()),
    database: {
      status: dbStatus,
      latency_ms: dbLatencyMs,
    },
    data_sources: {
      crypto_ohlcv: 'Binance Public API',
      forex_ohlcv: 'Yahoo Finance (Interbank)',
      forex_rates: 'ECB via Frankfurter',
      crypto_market: 'CoinGecko',
      economic: 'FRED (St. Louis Fed)',
    },
    endpoints: {
      health: '/health',
      twelve_data_time_series: '/time_series?symbol=BTC/USD&interval=1day',
      twelve_data_quote: '/quote?symbol=BTC/USD',
      twelve_data_price: '/price?symbol=BTC/USD',
      twelve_data_exchange_rate: '/exchange_rate?symbol=EUR/USD',
      twelve_data_eod: '/eod?symbol=BTC/USD',
      twelve_data_cryptos: '/cryptocurrencies',
      twelve_data_forex_pairs: '/forex_pairs',
      forex_sample: '/v1/forex/sample',
      crypto_sample: '/v1/crypto/sample',
      economic_sample: '/v1/economic/sample',
    },
  });
};

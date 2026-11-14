/**
 * Controller for Twelve Data compatible /exchange_rate endpoint
 * Response format: {"symbol": "EUR/USD", "rate": 1.0852, "timestamp": 1731514789}
 */
const liveFetcher = require('../services/liveFetcher');
const ForexOhlcv = require('../models/forexOhlcv.model');
const ForexRate = require('../models/forexRate.model');

exports.getExchangeRate = async (req, res, next) => {
  try {
    const symbol = req.symbol;

    // 1. Live Forex Attempt (Yahoo Finance)
    const liveRate = await liveFetcher.fetchLiveForexRate(symbol);
    if (liveRate !== null) {
      return res.json({
        symbol,
        rate: liveRate,
        timestamp: Math.floor(Date.now() / 1000),
      });
    }

    // 2. Fallback: Forex OHLCV table
    const latestOhlcv = await ForexOhlcv.getLatest(symbol);
    if (latestOhlcv) {
      return res.json({
        symbol,
        rate: parseFloat(latestOhlcv.close_price),
        timestamp: Math.floor(Date.now() / 1000),
      });
    }

    // 3. Fallback: Forex Daily Rates table
    if (symbol.includes('/')) {
      const [base, target] = symbol.split('/');
      let rate = await ForexRate.getLatestRate(base, target);
      if (rate) {
        return res.json({
          symbol,
          rate: parseFloat(rate.exchange_rate),
          timestamp: Math.floor(Date.now() / 1000),
        });
      }

      // Check inverted rate (e.g., target -> base)
      const invRate = await ForexRate.getLatestRate(target, base);
      if (invRate && parseFloat(invRate.exchange_rate) > 0) {
        return res.json({
          symbol,
          rate: parseFloat((1 / parseFloat(invRate.exchange_rate)).toFixed(5)),
          timestamp: Math.floor(Date.now() / 1000),
        });
      }
    }

    return res.status(404).json({
      status: 'error',
      message: `Symbol not found: ${symbol}`,
    });
  } catch (err) {
    next(err);
  }
};


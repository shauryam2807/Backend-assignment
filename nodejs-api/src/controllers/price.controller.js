/**
 * Controller for Twelve Data compatible /price endpoint
 * Response format: {"price": "123.45"}
 */
const liveFetcher = require('../services/liveFetcher');
const CryptoOhlcv = require('../models/cryptoOhlcv.model');
const ForexOhlcv = require('../models/forexOhlcv.model');
const ForexRate = require('../models/forexRate.model');

exports.getPrice = async (req, res, next) => {
  try {
    const symbol = req.symbol; // injected by validateSymbol middleware

    // 1. Live Crypto Attempt (Binance)
    const liveCrypto = await liveFetcher.fetchLiveCryptoPrice(symbol);
    if (liveCrypto !== null) {
      return res.json({ price: liveCrypto.toFixed(2) });
    }

    // 2. Live Forex Attempt (Yahoo Finance)
    const liveForex = await liveFetcher.fetchLiveForexRate(symbol);
    if (liveForex !== null) {
      return res.json({ price: liveForex.toFixed(5) });
    }

    // 3. Fallback: Stored Crypto OHLCV in DB
    if (symbol.includes('/') && ['BTC', 'ETH', 'SOL', 'BNB', 'XRP'].some((c) => symbol.includes(c))) {
      const latestCrypto = await CryptoOhlcv.getLatest(symbol);
      if (latestCrypto) {
        return res.json({ price: parseFloat(latestCrypto.close_price).toFixed(2) });
      }
    }

    // 4. Fallback: Stored Forex OHLCV in DB
    const latestForexOhlcv = await ForexOhlcv.getLatest(symbol);
    if (latestForexOhlcv) {
      return res.json({ price: parseFloat(latestForexOhlcv.close_price).toFixed(5) });
    }

    // 5. Fallback: Stored Forex Daily Rates in DB
    if (symbol.includes('/')) {
      const [base, target] = symbol.split('/');
      const rate = await ForexRate.getLatestRate(base, target);
      if (rate) {
        return res.json({ price: parseFloat(rate.exchange_rate).toFixed(5) });
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


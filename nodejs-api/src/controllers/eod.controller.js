/**
 * Controller for Twelve Data compatible /eod endpoint
 * Returns latest End-of-Day price and candle details
 */
const liveFetcher = require('../services/liveFetcher');
const CryptoOhlcv = require('../models/cryptoOhlcv.model');
const ForexOhlcv = require('../models/forexOhlcv.model');

exports.getEod = async (req, res, next) => {
  try {
    const symbol = req.symbol;
    const isCrypto = ['BTC', 'ETH', 'SOL', 'BNB', 'XRP'].some((c) => symbol.includes(c));

    if (isCrypto) {
      // 1. Live candle
      const liveCandle = await liveFetcher.fetchLiveCryptoKline(symbol);
      if (liveCandle) {
        return res.json({
          symbol,
          exchange: 'Binance',
          currency: symbol.split('/')[1] || 'USD',
          datetime: liveCandle.datetime,
          close: liveCandle.close,
          open: liveCandle.open,
          high: liveCandle.high,
          low: liveCandle.low,
          volume: liveCandle.volume,
        });
      }

      // 2. DB fallback
      const latest = await CryptoOhlcv.getLatest(symbol);
      if (latest) {
        const cDate = typeof latest.candle_date === 'string' ? latest.candle_date : new Date(latest.candle_date).toISOString().split('T')[0];
        return res.json({
          symbol,
          exchange: 'Binance',
          currency: symbol.split('/')[1] || 'USD',
          datetime: cDate,
          close: parseFloat(latest.close_price).toFixed(2),
          open: parseFloat(latest.open_price).toFixed(2),
          high: parseFloat(latest.high_price).toFixed(2),
          low: parseFloat(latest.low_price).toFixed(2),
          volume: String(Math.floor(parseFloat(latest.volume || 0))),
        });
      }
    }

    // Forex EOD
    const liveFxCandle = await liveFetcher.fetchLiveForexCandle(symbol);
    if (liveFxCandle) {
      return res.json({
        symbol,
        exchange: 'FOREX',
        currency: symbol.split('/')[1] || 'USD',
        datetime: liveFxCandle.datetime,
        close: liveFxCandle.close,
        open: liveFxCandle.open,
        high: liveFxCandle.high,
        low: liveFxCandle.low,
        volume: liveFxCandle.volume,
      });
    }

    const latestFx = await ForexOhlcv.getLatest(symbol);
    if (latestFx) {
      const cDate = typeof latestFx.candle_date === 'string' ? latestFx.candle_date : new Date(latestFx.candle_date).toISOString().split('T')[0];
      return res.json({
        symbol,
        exchange: 'FOREX',
        currency: symbol.split('/')[1] || 'USD',
        datetime: cDate,
        close: parseFloat(latestFx.close_price).toFixed(5),
        open: parseFloat(latestFx.open_price).toFixed(5),
        high: parseFloat(latestFx.high_price).toFixed(5),
        low: parseFloat(latestFx.low_price).toFixed(5),
        volume: '0',
      });
    }

    return res.status(404).json({
      status: 'error',
      message: `Symbol not found: ${symbol}`,
    });
  } catch (err) {
    next(err);
  }
};


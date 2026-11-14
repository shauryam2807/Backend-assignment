/**
 * Controller for Twelve Data compatible /time_series endpoint
 * Response format: { meta: {...}, values: [...], status: "ok" }
 */
const liveFetcher = require('../services/liveFetcher');
const CryptoOhlcv = require('../models/cryptoOhlcv.model');
const ForexOhlcv = require('../models/forexOhlcv.model');

exports.getTimeSeries = async (req, res, next) => {
  try {
    const symbol = req.symbol;
    const interval = req.query.interval || '1day';
    let outputsize = parseInt(req.query.outputsize, 10);
    if (isNaN(outputsize) || outputsize <= 0) outputsize = 30;
    outputsize = Math.min(outputsize, 5000);

    const isCrypto = ['BTC', 'ETH', 'SOL', 'BNB', 'XRP'].some((c) => symbol.includes(c));

    if (isCrypto) {
      // 1. Fetch historical from DB
      const historical = await CryptoOhlcv.getCandles(symbol, outputsize);
      const values = [];

      // 2. Fetch live active candle from Binance
      const liveCandle = await liveFetcher.fetchLiveCryptoKline(symbol, interval);
      if (liveCandle) {
        values.push(liveCandle);
      }

      for (const row of historical) {
        const cDate = typeof row.candle_date === 'string' ? row.candle_date : new Date(row.candle_date).toISOString().split('T')[0];
        if (liveCandle && liveCandle.datetime === cDate) continue;

        values.push({
          datetime: cDate,
          open: parseFloat(row.open_price).toFixed(2),
          high: parseFloat(row.high_price).toFixed(2),
          low: parseFloat(row.low_price).toFixed(2),
          close: parseFloat(row.close_price).toFixed(2),
          volume: String(Math.floor(parseFloat(row.volume || 0))),
        });

        if (values.length >= outputsize) break;
      }

      if (values.length > 0) {
        const parts = symbol.split('/');
        return res.json({
          meta: {
            symbol,
            interval,
            currency_base: parts[0],
            currency_quote: parts[1] || 'USD',
            exchange: 'Binance',
            type: 'Digital Currency',
          },
          values: values.slice(0, outputsize),
          status: 'ok',
        });
      }
    }

    // Forex OHLC (Yahoo Finance Live + Historical DB)
    const historicalFx = await ForexOhlcv.getCandles(symbol, outputsize);
    const valuesFx = [];

    const liveFxCandle = await liveFetcher.fetchLiveForexCandle(symbol);
    if (liveFxCandle) {
      valuesFx.push(liveFxCandle);
    }

    for (const row of historicalFx) {
      const cDate = typeof row.candle_date === 'string' ? row.candle_date : new Date(row.candle_date).toISOString().split('T')[0];
      if (liveFxCandle && liveFxCandle.datetime === cDate) continue;

      valuesFx.push({
        datetime: cDate,
        open: parseFloat(row.open_price).toFixed(5),
        high: parseFloat(row.high_price).toFixed(5),
        low: parseFloat(row.low_price).toFixed(5),
        close: parseFloat(row.close_price).toFixed(5),
        volume: String(Math.floor(parseFloat(row.volume || 0))),
      });

      if (valuesFx.length >= outputsize) break;
    }

    if (valuesFx.length > 0) {
      const parts = symbol.split('/');
      return res.json({
        meta: {
          symbol,
          interval,
          currency_base: parts[0],
          currency_quote: parts[1] || 'USD',
          type: 'Physical Currency',
        },
        values: valuesFx.slice(0, outputsize),
        status: 'ok',
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


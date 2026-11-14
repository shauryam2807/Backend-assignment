/**
 * Controller for Twelve Data compatible /quote endpoint
 * Returns snapshot quote with 52-week range and change metrics
 */
const liveFetcher = require('../services/liveFetcher');
const CryptoOhlcv = require('../models/cryptoOhlcv.model');
const ForexOhlcv = require('../models/forexOhlcv.model');

exports.getQuote = async (req, res, next) => {
  try {
    const symbol = req.symbol;
    const isCrypto = ['BTC', 'ETH', 'SOL', 'BNB', 'XRP'].some((c) => symbol.includes(c));

    if (isCrypto) {
      const historical = await CryptoOhlcv.getCandles(symbol, 365);
      const liveCandle = await liveFetcher.fetchLiveCryptoKline(symbol);

      if (historical.length > 0 || liveCandle) {
        let closePrice, openPrice, highPrice, lowPrice, volume, candleDate, prevClose;

        if (liveCandle) {
          closePrice = parseFloat(liveCandle.close);
          openPrice = parseFloat(liveCandle.open);
          highPrice = parseFloat(liveCandle.high);
          lowPrice = parseFloat(liveCandle.low);
          volume = liveCandle.volume;
          candleDate = liveCandle.datetime;
          prevClose = historical.length > 0 ? parseFloat(historical[0].close_price) : closePrice;
        } else {
          const latest = historical[0];
          const prev = historical[1] || latest;
          closePrice = parseFloat(latest.close_price);
          openPrice = parseFloat(latest.open_price);
          highPrice = parseFloat(latest.high_price);
          lowPrice = parseFloat(latest.low_price);
          volume = String(Math.floor(parseFloat(latest.volume || 0)));
          candleDate = typeof latest.candle_date === 'string' ? latest.candle_date : new Date(latest.candle_date).toISOString().split('T')[0];
          prevClose = parseFloat(prev.close_price);
        }

        const change = closePrice - prevClose;
        const percentChange = prevClose !== 0 ? (change / prevClose) * 100 : 0;

        const allCloses = historical.map((r) => parseFloat(r.close_price)).concat([closePrice]);
        const w52Low = Math.min(...allCloses);
        const w52High = Math.max(...allCloses);

        const parts = symbol.split('/');
        return res.json({
          symbol,
          name: `${parts[0]} / ${parts[1] || 'USD'}`,
          exchange: 'Binance',
          currency: parts[1] || 'USD',
          datetime: candleDate,
          timestamp: Math.floor(Date.now() / 1000),
          open: openPrice.toFixed(2),
          high: highPrice.toFixed(2),
          low: lowPrice.toFixed(2),
          close: closePrice.toFixed(2),
          volume,
          previous_close: prevClose.toFixed(2),
          change: (change >= 0 ? '+' : '') + change.toFixed(2),
          percent_change: (percentChange >= 0 ? '+' : '') + percentChange.toFixed(4),
          is_market_open: true,
          fifty_two_week: {
            low: w52Low.toFixed(2),
            high: w52High.toFixed(2),
            range: `${w52Low.toFixed(2)} - ${w52High.toFixed(2)}`,
          },
        });
      }
    }

    // Forex OHLC Quote
    const historicalFx = await ForexOhlcv.getCandles(symbol, 365);
    const liveFxCandle = await liveFetcher.fetchLiveForexCandle(symbol);

    if (historicalFx.length > 0 || liveFxCandle) {
      let closePrice, openPrice, highPrice, lowPrice, candleDate, prevClose;

      if (liveFxCandle) {
        closePrice = parseFloat(liveFxCandle.close);
        openPrice = parseFloat(liveFxCandle.open);
        highPrice = parseFloat(liveFxCandle.high);
        lowPrice = parseFloat(liveFxCandle.low);
        candleDate = liveFxCandle.datetime;
        prevClose = historicalFx.length > 0 ? parseFloat(historicalFx[0].close_price) : closePrice;
      } else {
        const latest = historicalFx[0];
        const prev = historicalFx[1] || latest;
        closePrice = parseFloat(latest.close_price);
        openPrice = parseFloat(latest.open_price);
        highPrice = parseFloat(latest.high_price);
        lowPrice = parseFloat(latest.low_price);
        candleDate = typeof latest.candle_date === 'string' ? latest.candle_date : new Date(latest.candle_date).toISOString().split('T')[0];
        prevClose = parseFloat(prev.close_price);
      }

      const change = closePrice - prevClose;
      const percentChange = prevClose !== 0 ? (change / prevClose) * 100 : 0;

      const allCloses = historicalFx.map((r) => parseFloat(r.close_price)).concat([closePrice]);
      const w52Low = Math.min(...allCloses);
      const w52High = Math.max(...allCloses);

      const parts = symbol.split('/');
      return res.json({
        symbol,
        name: `${parts[0]} / ${parts[1] || 'USD'}`,
        exchange: 'FOREX',
        currency: parts[1] || 'USD',
        datetime: candleDate,
        timestamp: Math.floor(Date.now() / 1000),
        open: openPrice.toFixed(5),
        high: highPrice.toFixed(5),
        low: lowPrice.toFixed(5),
        close: closePrice.toFixed(5),
        volume: '0',
        previous_close: prevClose.toFixed(5),
        change: (change >= 0 ? '+' : '') + change.toFixed(5),
        percent_change: (percentChange >= 0 ? '+' : '') + percentChange.toFixed(4),
        is_market_open: true,
        fifty_two_week: {
          low: w52Low.toFixed(5),
          high: w52High.toFixed(5),
          range: `${w52Low.toFixed(5)} - ${w52High.toFixed(5)}`,
        },
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


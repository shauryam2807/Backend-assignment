/**
 * Live Financial Data Fetcher
 * Directly queries institutional feeds:
 * - Binance Public API for Crypto
 * - Yahoo Finance for Forex
 */
const axios = require('axios');
const cache = require('./cache');

const CRYPTO_MAP = {
  'BTC/USD': 'BTCUSDT',
  'ETH/USD': 'ETHUSDT',
  'SOL/USD': 'SOLUSDT',
  'BNB/USD': 'BNBUSDT',
  'XRP/USD': 'XRPUSDT',
  'BTC': 'BTCUSDT',
  'ETH': 'ETHUSDT',
  'SOL': 'SOLUSDT',
  'BNB': 'BNBUSDT',
  'XRP': 'XRPUSDT',
};

const FOREX_MAP = {
  'EUR/USD': 'EURUSD=X',
  'GBP/USD': 'GBPUSD=X',
  'USD/JPY': 'USDJPY=X',
  'USD/INR': 'USDINR=X',
  'USD/CAD': 'USDCAD=X',
  'AUD/USD': 'AUDUSD=X',
  'USD/CHF': 'USDCHF=X',
};

const USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36';

function getBinanceTicker(symbol) {
  if (!symbol) return null;
  const clean = symbol.toUpperCase().trim();

  // Guard: Reject forex symbols so they never hit Binance
  if (FOREX_MAP[clean]) return null;
  if (CRYPTO_MAP[clean]) return CRYPTO_MAP[clean];

  if (clean.includes('/')) {
    const [base, quote] = clean.split('/');
    const fiatCurrencies = ['EUR', 'GBP', 'JPY', 'INR', 'CAD', 'AUD', 'CHF', 'NZD', 'SGD', 'HKD'];
    if (fiatCurrencies.includes(base)) return null;
    if (quote === 'USD' || quote === 'USDT') return `${base}USDT`;
  }
  return null;
}

function getForexTicker(pair) {
  if (!pair) return null;
  const clean = pair.toUpperCase().trim();
  if (FOREX_MAP[clean]) return FOREX_MAP[clean];
  if (clean.includes('/')) {
    const [base, target] = clean.split('/');
    return `${base}${target}=X`;
  }
  return null;
}

/**
 * Fetch current real-time price from Binance
 */
async function fetchLiveCryptoPrice(symbol) {
  const ticker = getBinanceTicker(symbol);
  if (!ticker) return null;

  const cacheKey = `crypto_price:${ticker}`;
  const cached = cache.get(cacheKey);
  if (cached !== undefined) return cached;

  try {
    const url = `https://api.binance.com/api/v3/ticker/price?symbol=${ticker}`;
    const resp = await axios.get(url, { timeout: 5000 });
    if (resp.status === 200 && resp.data?.price) {
      const price = parseFloat(resp.data.price);
      if (price > 0) {
        cache.set(cacheKey, price, 30);
        return price;
      }
    }
  } catch (err) {
    console.warn(`[liveFetcher] Binance price error for ${ticker}:`, err.message);
  }
  return null;
}

/**
 * Fetch latest daily kline/candle from Binance
 */
async function fetchLiveCryptoKline(symbol, interval = '1d') {
  const ticker = getBinanceTicker(symbol);
  if (!ticker) return null;

  let bInterval = '1d';
  if (['1min', '1m'].includes(interval)) bInterval = '1m';
  else if (['5min', '5m'].includes(interval)) bInterval = '5m';
  else if (['15min', '15m'].includes(interval)) bInterval = '15m';
  else if (['1h', '1hour'].includes(interval)) bInterval = '1h';
  else if (['1week', '1w'].includes(interval)) bInterval = '1w';

  const cacheKey = `crypto_kline:${ticker}:${bInterval}`;
  const cached = cache.get(cacheKey);
  if (cached !== undefined) return cached;

  try {
    const url = `https://api.binance.com/api/v3/klines?symbol=${ticker}&interval=${bInterval}&limit=1`;
    const resp = await axios.get(url, { timeout: 5000 });
    if (resp.status === 200 && Array.isArray(resp.data) && resp.data.length > 0) {
      const c = resp.data[0];
      const candleDate = new Date(c[0]).toISOString().split('T')[0];
      const candle = {
        datetime: candleDate,
        open: parseFloat(c[1]).toFixed(2),
        high: parseFloat(c[2]).toFixed(2),
        low: parseFloat(c[3]).toFixed(2),
        close: parseFloat(c[4]).toFixed(2),
        volume: String(Math.floor(parseFloat(c[5]))),
      };
      cache.set(cacheKey, candle, 30);
      return candle;
    }
  } catch (err) {
    console.warn(`[liveFetcher] Binance kline error for ${ticker}:`, err.message);
  }
  return null;
}

/**
 * Fetch current real-time forex rate from Yahoo Finance
 */
async function fetchLiveForexRate(pair) {
  const ticker = getForexTicker(pair);
  if (!ticker) return null;

  const cacheKey = `forex_rate:${ticker}`;
  const cached = cache.get(cacheKey);
  if (cached !== undefined) return cached;

  try {
    const url = `https://query1.finance.yahoo.com/v8/finance/chart/${ticker}?range=1d&interval=1m`;
    const resp = await axios.get(url, {
      headers: { 'User-Agent': USER_AGENT },
      timeout: 5000,
    });
    if (resp.status === 200) {
      const result = resp.data?.chart?.result;
      if (Array.isArray(result) && result.length > 0) {
        const price = result[0]?.meta?.regularMarketPrice;
        if (price && parseFloat(price) > 0) {
          const rate = parseFloat(parseFloat(price).toFixed(5));
          cache.set(cacheKey, rate, 30);
          return rate;
        }
      }
    }
  } catch (err) {
    console.warn(`[liveFetcher] Yahoo forex rate error for ${ticker}:`, err.message);
  }
  return null;
}

/**
 * Fetch latest daily candle for forex from Yahoo Finance
 */
async function fetchLiveForexCandle(pair) {
  const ticker = getForexTicker(pair);
  if (!ticker) return null;

  const cacheKey = `forex_candle:${ticker}`;
  const cached = cache.get(cacheKey);
  if (cached !== undefined) return cached;

  try {
    const url = `https://query1.finance.yahoo.com/v8/finance/chart/${ticker}?range=5d&interval=1d`;
    const resp = await axios.get(url, {
      headers: { 'User-Agent': USER_AGENT },
      timeout: 5000,
    });
    if (resp.status === 200) {
      const result = resp.data?.chart?.result;
      if (Array.isArray(result) && result.length > 0) {
        const res = result[0];
        const timestamps = res.timestamp || [];
        const quotes = res.indicators?.quote?.[0] || {};
        const opens = quotes.open || [];
        const highs = quotes.high || [];
        const lows = quotes.low || [];
        const closes = quotes.close || [];
        const volumes = quotes.volume || [];

        for (let i = timestamps.length - 1; i >= 0; i--) {
          const o = opens[i];
          const h = highs[i];
          const l = lows[i];
          const c = closes[i];
          if (o !== null && h !== null && l !== null && c !== null && o !== undefined) {
            const candleDate = new Date(timestamps[i] * 1000).toISOString().split('T')[0];
            const candle = {
              datetime: candleDate,
              open: parseFloat(o).toFixed(5),
              high: parseFloat(h).toFixed(5),
              low: parseFloat(l).toFixed(5),
              close: parseFloat(c).toFixed(5),
              volume: String(Math.floor(parseFloat(volumes[i] || 0))),
            };
            cache.set(cacheKey, candle, 30);
            return candle;
          }
        }
      }
    }
  } catch (err) {
    console.warn(`[liveFetcher] Yahoo forex candle error for ${ticker}:`, err.message);
  }
  return null;
}

module.exports = {
  CRYPTO_MAP,
  FOREX_MAP,
  getBinanceTicker,
  getForexTicker,
  fetchLiveCryptoPrice,
  fetchLiveCryptoKline,
  fetchLiveForexRate,
  fetchLiveForexCandle,
};


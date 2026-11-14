const {
  getBinanceTicker,
  getForexTicker,
  CRYPTO_MAP,
  FOREX_MAP,
} = require('../src/services/liveFetcher');
const cache = require('../src/services/cache');

describe('Live Fetcher & Symbol Resolution', () => {
  test('Crypto symbols resolve to Binance tickers', () => {
    expect(getBinanceTicker('BTC/USD')).toBe('BTCUSDT');
    expect(getBinanceTicker('ETH/USD')).toBe('ETHUSDT');
    expect(getBinanceTicker('SOL')).toBe('SOLUSDT');
  });

  test('Forex symbols MUST NEVER resolve to Binance tickers (Forex Guard)', () => {
    expect(getBinanceTicker('EUR/USD')).toBeNull();
    expect(getBinanceTicker('GBP/USD')).toBeNull();
    expect(getBinanceTicker('USD/JPY')).toBeNull();
    expect(getBinanceTicker('USD/INR')).toBeNull();
  });

  test('Forex symbols resolve to Yahoo Finance tickers', () => {
    expect(getForexTicker('EUR/USD')).toBe('EURUSD=X');
    expect(getForexTicker('GBP/USD')).toBe('GBPUSD=X');
    expect(getForexTicker('USD/JPY')).toBe('USDJPY=X');
  });

  test('Cache set and get works with TTL', () => {
    cache.set('test_key', 12345, 10);
    expect(cache.get('test_key')).toBe(12345);
    cache.del('test_key');
    expect(cache.get('test_key')).toBeUndefined();
  });
});


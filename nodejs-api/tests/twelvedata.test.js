const request = require('supertest');
const app = require('../src/app');
const pool = require('../src/config/database');

describe('Twelve Data Compatible API Endpoints', () => {
  afterAll(async () => {
    await pool.end();
  });
  // Validation tests
  test('GET /price without symbol should return 400', async () => {
    const res = await request(app).get('/price');
    expect(res.statusCode).toBe(400);
    expect(res.body.status).toBe('error');
    expect(res.body.message).toContain('Missing required parameter');
  });

  test('GET /time_series without symbol should return 400', async () => {
    const res = await request(app).get('/time_series');
    expect(res.statusCode).toBe(400);
  });

  // Reference Endpoints
  test('GET /cryptocurrencies returns valid symbol list', async () => {
    const res = await request(app).get('/cryptocurrencies');
    expect(res.statusCode).toBe(200);
    expect(res.body.status).toBe('ok');
    expect(Array.isArray(res.body.data)).toBe(true);
    expect(res.body.data.some((c) => c.symbol === 'BTC/USD')).toBe(true);
  });

  test('GET /forex_pairs returns valid forex pair list', async () => {
    const res = await request(app).get('/forex_pairs');
    expect(res.statusCode).toBe(200);
    expect(res.body.status).toBe('ok');
    expect(Array.isArray(res.body.data)).toBe(true);
    expect(res.body.data.some((p) => p.symbol === 'EUR/USD')).toBe(true);
  });

  // Live / Contract Endpoints
  test('GET /price?symbol=BTC/USD returns price string matching Twelve Data contract', async () => {
    const res = await request(app).get('/price?symbol=BTC/USD');
    expect(res.statusCode).toBe(200);
    expect(res.body.price).toBeDefined();
    expect(typeof res.body.price).toBe('string');
    expect(parseFloat(res.body.price)).toBeGreaterThan(0);
  }, 20000);

  test('GET /price?symbol=EUR/USD returns forex price string', async () => {
    const res = await request(app).get('/price?symbol=EUR/USD');
    expect(res.statusCode).toBe(200);
    expect(res.body.price).toBeDefined();
    expect(parseFloat(res.body.price)).toBeGreaterThan(0);
  }, 20000);

  test('GET /exchange_rate?symbol=EUR/USD returns rate and timestamp', async () => {
    const res = await request(app).get('/exchange_rate?symbol=EUR/USD');
    expect(res.statusCode).toBe(200);
    expect(res.body.symbol).toBe('EUR/USD');
    expect(typeof res.body.rate).toBe('number');
    expect(res.body.timestamp).toBeDefined();
  }, 20000);

  test('GET /time_series?symbol=BTC/USD returns meta and values array', async () => {
    const res = await request(app).get('/time_series?symbol=BTC/USD&interval=1day&outputsize=5');
    expect(res.statusCode).toBe(200);
    expect(res.body.meta).toBeDefined();
    expect(res.body.meta.symbol).toBe('BTC/USD');
    expect(res.body.meta.exchange).toBe('Binance');
    expect(Array.isArray(res.body.values)).toBe(true);
    if (res.body.values.length > 0) {
      const v = res.body.values[0];
      expect(v.datetime).toBeDefined();
      expect(v.open).toBeDefined();
      expect(v.high).toBeDefined();
      expect(v.low).toBeDefined();
      expect(v.close).toBeDefined();
    }
  }, 20000);

  test('GET /quote?symbol=BTC/USD returns complete quote snapshot', async () => {
    const res = await request(app).get('/quote?symbol=BTC/USD');
    expect(res.statusCode).toBe(200);
    expect(res.body.symbol).toBe('BTC/USD');
    expect(res.body.exchange).toBe('Binance');
    expect(res.body.open).toBeDefined();
    expect(res.body.high).toBeDefined();
    expect(res.body.low).toBeDefined();
    expect(res.body.close).toBeDefined();
    expect(res.body.fifty_two_week).toBeDefined();
  }, 20000);

  test('GET /eod?symbol=BTC/USD returns end of day candle', async () => {
    const res = await request(app).get('/eod?symbol=BTC/USD');
    expect(res.statusCode).toBe(200);
    expect(res.body.symbol).toBe('BTC/USD');
    expect(res.body.close).toBeDefined();
  }, 20000);
});

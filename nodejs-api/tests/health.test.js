const request = require('supertest');
const app = require('../src/app');
const pool = require('../src/config/database');

describe('Health and Root Endpoints', () => {
  afterAll(async () => {
    await pool.end();
  });

  test('GET / should return platform metadata', async () => {
    const res = await request(app).get('/');
    expect(res.statusCode).toBe(200);
    expect(res.body.name).toContain('MFAPIs');
    expect(res.body.version).toBe('2.0.0');
    expect(res.body.github).toBeDefined();
  });

  test('GET /health should report system status with DB check', async () => {
    const res = await request(app).get('/health');
    expect(res.statusCode).toBe(200);
    expect(['healthy', 'degraded']).toContain(res.body.status);
    expect(res.body.twelvedata_compatible).toBe(true);
    expect(res.body.data_sources).toBeDefined();
    expect(res.body.database).toBeDefined();
    expect(res.body.database.status).toBeDefined();
    expect(res.body.uptime_seconds).toBeGreaterThanOrEqual(0);
  });

  test('GET /unknown-route should return 404', async () => {
    const res = await request(app).get('/unknown-endpoint-xyz');
    expect(res.statusCode).toBe(404);
    expect(res.body.status).toBe('error');
  });
});

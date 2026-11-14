/**
 * Model for `crypto_ohlcv_daily` table
 */
const pool = require('../config/database');

exports.getCandles = async (symbol, limit = 30) => {
  try {
    const query = `
      SELECT symbol, candle_date, open_price, high_price, low_price, close_price, volume
      FROM crypto_ohlcv_daily
      WHERE symbol = $1
      ORDER BY candle_date DESC
      LIMIT $2
    `;
    const { rows } = await pool.query(query, [symbol, limit]);
    return rows;
  } catch (err) {
    console.error(`[CryptoOhlcv] Query error for ${symbol}:`, err.message);
    return [];
  }
};

exports.getLatest = async (symbol) => {
  const rows = await exports.getCandles(symbol, 1);
  return rows.length > 0 ? rows[0] : null;
};


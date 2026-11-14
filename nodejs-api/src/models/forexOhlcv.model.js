/**
 * Model for `forex_ohlcv_daily` table
 */
const pool = require('../config/database');

exports.getCandles = async (pairName, limit = 30) => {
  try {
    const query = `
      SELECT pair_name, candle_date, open_price, high_price, low_price, close_price, volume
      FROM forex_ohlcv_daily
      WHERE pair_name = $1
      ORDER BY candle_date DESC
      LIMIT $2
    `;
    const { rows } = await pool.query(query, [pairName, limit]);
    return rows;
  } catch (err) {
    console.error(`[ForexOhlcv] Query error for ${pairName}:`, err.message);
    return [];
  }
};

exports.getLatest = async (pairName) => {
  const rows = await exports.getCandles(pairName, 1);
  return rows.length > 0 ? rows[0] : null;
};


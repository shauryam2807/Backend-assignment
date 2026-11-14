/**
 * Model for `crypto_daily_prices` and `cryptocurrencies` tables
 */
const pool = require('../config/database');

exports.getSamplePrices = async (limit = 25) => {
  try {
    const query = `
      SELECT coin_id, price_date, price_usd, market_cap_usd, total_volume_usd, source, raw_response_id
      FROM crypto_daily_prices
      ORDER BY price_date DESC
      LIMIT $1
    `;
    const { rows } = await pool.query(query, [limit]);
    return rows;
  } catch (err) {
    console.error('[CryptoPrice] Query error for sample prices:', err.message);
    return [];
  }
};


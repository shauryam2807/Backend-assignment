/**
 * Model for `forex_daily_rates` and `forex_pairs` tables
 */
const pool = require('../config/database');

exports.getLatestRate = async (baseCurrency, targetCurrency) => {
  try {
    const query = `
      SELECT base_currency, target_currency, rate_date, exchange_rate, source
      FROM forex_daily_rates
      WHERE base_currency = $1 AND target_currency = $2
      ORDER BY rate_date DESC
      LIMIT 1
    `;
    const { rows } = await pool.query(query, [baseCurrency, targetCurrency]);
    return rows.length > 0 ? rows[0] : null;
  } catch (err) {
    console.error(`[ForexRate] Query error for ${baseCurrency}/${targetCurrency}:`, err.message);
    return null;
  }
};

exports.getSampleRates = async (limit = 25) => {
  try {
    const query = `
      SELECT base_currency, target_currency, rate_date, exchange_rate, source, raw_response_id
      FROM forex_daily_rates
      ORDER BY rate_date DESC
      LIMIT $1
    `;
    const { rows } = await pool.query(query, [limit]);
    return rows;
  } catch (err) {
    console.error('[ForexRate] Query error for sample rates:', err.message);
    return [];
  }
};


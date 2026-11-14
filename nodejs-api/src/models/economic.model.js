/**
 * Model for `economic_indicators` and `economic_indicator_values` tables
 */
const pool = require('../config/database');

exports.getSampleValues = async (limit = 25) => {
  try {
    const query = `
      SELECT indicator_id, observation_date, value, source, raw_response_id
      FROM economic_indicator_values
      ORDER BY observation_date DESC
      LIMIT $1
    `;
    const { rows } = await pool.query(query, [limit]);
    return rows;
  } catch (err) {
    console.error('[Economic] Query error for sample values:', err.message);
    return [];
  }
};


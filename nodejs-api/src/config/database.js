/**
 * Database Configuration & Connection Pool
 * Uses PostgreSQL connection pool via `pg` library.
 */
const { Pool } = require('pg');
require('dotenv').config();

let connectionString = process.env.DATABASE_URL || 'postgresql://postgres:postgres@localhost:5432/mfapis_db';

// Clean SQLAlchemy psycopg2 prefix if present
if (connectionString.includes('+psycopg2')) {
  connectionString = connectionString.replace('+psycopg2', '');
}

const pool = new Pool({
  connectionString,
  max: 20,
  idleTimeoutMillis: 30000,
  connectionTimeoutMillis: 5000,
});

pool.on('error', (err) => {
  console.error('Unexpected error on idle PostgreSQL client:', err);
});

module.exports = pool;


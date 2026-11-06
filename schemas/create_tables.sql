CREATE TABLE IF NOT EXISTS forex_pairs (
    id              SERIAL PRIMARY KEY,
    base_currency   VARCHAR(3) NOT NULL,
    target_currency VARCHAR(3) NOT NULL,
    pair_name       VARCHAR(10) NOT NULL,
    source          VARCHAR(50) DEFAULT 'frankfurter',
    is_active       BOOLEAN DEFAULT TRUE,
    created_at      TIMESTAMP DEFAULT NOW(),
    updated_at      TIMESTAMP DEFAULT NOW(),
    UNIQUE(base_currency, target_currency)
);

CREATE TABLE IF NOT EXISTS forex_daily_rates (
    id              SERIAL PRIMARY KEY,
    base_currency   VARCHAR(3) NOT NULL,
    target_currency VARCHAR(3) NOT NULL,
    rate_date       DATE NOT NULL,
    exchange_rate   DECIMAL(18, 8) NOT NULL,
    source          VARCHAR(50) DEFAULT 'frankfurter',
    raw_response_id VARCHAR(100),
    created_at      TIMESTAMP DEFAULT NOW(),
    updated_at      TIMESTAMP DEFAULT NOW(),
    UNIQUE(base_currency, target_currency, rate_date)
);

CREATE INDEX IF NOT EXISTS idx_forex_rates_date ON forex_daily_rates(rate_date);
CREATE INDEX IF NOT EXISTS idx_forex_rates_pair ON forex_daily_rates(base_currency, target_currency);

CREATE TABLE IF NOT EXISTS cryptocurrencies (
    id              SERIAL PRIMARY KEY,
    coin_id         VARCHAR(100) NOT NULL UNIQUE,
    symbol          VARCHAR(20) NOT NULL,
    name            VARCHAR(200) NOT NULL,
    market_cap_rank INTEGER,
    category        VARCHAR(100),
    description     TEXT,
    homepage_url    VARCHAR(500),
    image_url       VARCHAR(500),
    source          VARCHAR(50) DEFAULT 'coingecko',
    is_active       BOOLEAN DEFAULT TRUE,
    created_at      TIMESTAMP DEFAULT NOW(),
    updated_at      TIMESTAMP DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS crypto_daily_prices (
    id              SERIAL PRIMARY KEY,
    coin_id         VARCHAR(100) NOT NULL,
    price_date      DATE NOT NULL,
    price_usd       DECIMAL(24, 8),
    market_cap_usd  DECIMAL(24, 2),
    total_volume_usd DECIMAL(24, 2),
    price_change_24h DECIMAL(12, 4),
    high_24h        DECIMAL(24, 8),
    low_24h         DECIMAL(24, 8),
    circulating_supply DECIMAL(24, 2),
    source          VARCHAR(50) DEFAULT 'coingecko',
    raw_response_id VARCHAR(100),
    created_at      TIMESTAMP DEFAULT NOW(),
    updated_at      TIMESTAMP DEFAULT NOW(),
    UNIQUE(coin_id, price_date)
);

CREATE INDEX IF NOT EXISTS idx_crypto_prices_date ON crypto_daily_prices(price_date);
CREATE INDEX IF NOT EXISTS idx_crypto_prices_coin ON crypto_daily_prices(coin_id);

CREATE TABLE IF NOT EXISTS economic_indicators (
    id              SERIAL PRIMARY KEY,
    indicator_id    VARCHAR(50) NOT NULL UNIQUE,
    name            VARCHAR(300) NOT NULL,
    description     TEXT,
    frequency       VARCHAR(20),
    units           VARCHAR(100),
    seasonal_adjustment VARCHAR(50),
    country         VARCHAR(50) DEFAULT 'US',
    category        VARCHAR(100),
    source_agency   VARCHAR(200),
    source          VARCHAR(50) DEFAULT 'fred',
    is_active       BOOLEAN DEFAULT TRUE,
    created_at      TIMESTAMP DEFAULT NOW(),
    updated_at      TIMESTAMP DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS economic_indicator_values (
    id              SERIAL PRIMARY KEY,
    indicator_id    VARCHAR(50) NOT NULL,
    observation_date DATE NOT NULL,
    value           DECIMAL(20, 4),
    country         VARCHAR(50) DEFAULT 'US',
    source          VARCHAR(50) DEFAULT 'fred',
    raw_response_id VARCHAR(100),
    created_at      TIMESTAMP DEFAULT NOW(),
    updated_at      TIMESTAMP DEFAULT NOW(),
    UNIQUE(indicator_id, observation_date)
);

CREATE INDEX IF NOT EXISTS idx_econ_values_date ON economic_indicator_values(observation_date);
CREATE INDEX IF NOT EXISTS idx_econ_values_indicator ON economic_indicator_values(indicator_id);

CREATE TABLE IF NOT EXISTS pipeline_runs (
    id              SERIAL PRIMARY KEY,
    pipeline_name   VARCHAR(100) NOT NULL,
    run_status      VARCHAR(20) NOT NULL,
    records_extracted INTEGER DEFAULT 0,
    records_transformed INTEGER DEFAULT 0,
    records_loaded  INTEGER DEFAULT 0,
    error_message   TEXT,
    started_at      TIMESTAMP NOT NULL DEFAULT NOW(),
    completed_at    TIMESTAMP,
    duration_seconds DECIMAL(10, 2)
);

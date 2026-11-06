# Data Quality Framework

## Validation Pipeline Architecture

Data quality validation is applied at every stage of the ETL pipeline:

```
RAW API DATA → [Extract Validation] → [Transform Validation] → [Load Validation] → DATABASE
     ↓                  ↓                      ↓                     ↓
  Schema check    Type coercion         Constraint check       Upsert conflict
  HTTP status     Null handling         Dedup by key           resolution
  Rate limit      Range checks          Foreign key            updated_at
  retry           Date parsing          integrity              timestamp
```

## Validation Rules by Category

### Forex Data
| Rule | Implementation | Action on Failure |
|------|---------------|-------------------|
| Exchange rate must be positive | `rate > 0` check in transformer | Row dropped with warning log |
| Currency code must be 3 chars | `len(code) == 3` validation | Row dropped |
| Rate date must be valid date | `pd.to_datetime()` with error handling | Row dropped |
| No duplicate (base, target, date) | `drop_duplicates(subset=[...], keep='last')` | Keeps latest |
| Rate within reasonable range | Compared against historical averages | Flagged in logs |
| Base ≠ Target currency | Filtered in transformer | Row excluded |

### Cryptocurrency Data
| Rule | Implementation | Action on Failure |
|------|---------------|-------------------|
| Price must be non-negative | `price >= 0` (stablecoins can be near 0) | Row dropped |
| Coin ID must be non-empty | `coin_id != ""` check | Row dropped |
| Market cap must be non-negative | `_safe_float()` returns None for invalid | Stored as NULL |
| Symbol must be uppercase | `.upper()` applied in transformer | Auto-corrected |
| Historical timestamps valid | `datetime.fromtimestamp()` with UTC | Invalid dates dropped |
| Volume must be non-negative | `_safe_float()` with range check | Stored as NULL if invalid |

### Economic Data
| Rule | Implementation | Action on Failure |
|------|---------------|-------------------|
| FRED missing value marker "." | Detected and converted to NULL | Stored as NULL |
| Observation date must be valid | `_safe_date()` parsing | Row dropped |
| Indicator ID must match config | Validated against `ECONOMIC_INDICATORS` | Row dropped |
| Numeric values must be parseable | `_safe_float()` with fallback | Stored as NULL |
| No future-dated observations | `date <= today` check | Row dropped |

## Data Quality Metrics

After each pipeline run, the following metrics are tracked in `pipeline_runs` table:

| Metric | Column | Description |
|--------|--------|-------------|
| Records Extracted | `records_extracted` | Total raw records from API |
| Records Transformed | `records_transformed` | Records after cleaning/validation |
| Records Loaded | `records_loaded` | Records successfully written to DB |
| Drop Rate | Computed | `(extracted - loaded) / extracted * 100%` |
| Duration | `duration_seconds` | Pipeline execution time |
| Status | `run_status` | `success` or `failed` |
| Error Detail | `error_message` | Stack trace on failure |

### Expected Quality Thresholds
| Category | Expected Drop Rate | Acceptable Range |
|----------|--------------------|------------------|
| Forex | < 1% | 0-2% (weekends/holidays excluded) |
| Crypto | < 5% | 0-10% (rate limiting may skip coins) |
| Economic | < 3% | 0-5% (FRED "." values converted to NULL) |

## Missing Data Handling Strategy

| Source | Missing Data Pattern | Handling |
|--------|---------------------|----------|
| Frankfurter | No data on weekends/holidays | Expected gaps, not filled |
| CoinGecko | 429 rate limit skips | Coins without history have current-day only |
| CoinGecko | Null market_cap for small coins | Stored as NULL, not zero |
| FRED | "." string for unavailable | Converted to NULL via `_safe_float()` |
| FRED | Revised data points | Latest value kept via UPSERT |

## Data Freshness Requirements

| Category | Update Frequency | Maximum Acceptable Staleness |
|----------|-----------------|------------------------------|
| Forex Rates | Daily (business days) | 3 days (covers weekends) |
| Crypto Prices | Daily | 1 day |
| Economic Indicators | Varies (daily to quarterly) | Depends on indicator frequency |

## Duplicate Prevention

All tables use PostgreSQL UPSERT (INSERT ... ON CONFLICT DO UPDATE) with unique constraints:

| Table | Unique Constraint | Conflict Resolution |
|-------|-------------------|---------------------|
| `forex_pairs` | `(base_currency, target_currency)` | Update pair_name, is_active |
| `forex_daily_rates` | `(base_currency, target_currency, rate_date)` | Update exchange_rate |
| `cryptocurrencies` | `(coin_id)` | Update name, rank, image |
| `crypto_daily_prices` | `(coin_id, price_date)` | Update price, market_cap, volume |
| `economic_indicators` | `(indicator_id)` | Update name, description |
| `economic_indicator_values` | `(indicator_id, observation_date)` | Update value |

## Monitoring and Alerting

Pipeline runs are logged to `pipeline_runs` table. Query for monitoring:

```sql
SELECT pipeline_name, run_status, records_loaded, duration_seconds,
       started_at, error_message
FROM pipeline_runs
ORDER BY started_at DESC
LIMIT 10;
```

Alert conditions:
- `run_status = 'failed'` → Investigate error_message
- `records_loaded = 0` for a successful run → API may be down
- `duration_seconds > 300` → Performance degradation
- Drop rate > threshold → Data quality issue at source

## Reconciliation Approach

To verify data integrity between source and database:

```sql
-- Compare loaded record count with expected
SELECT 'forex_daily_rates' AS table_name, COUNT(*) AS db_count FROM forex_daily_rates
UNION ALL
SELECT 'crypto_daily_prices', COUNT(*) FROM crypto_daily_prices
UNION ALL
SELECT 'economic_indicator_values', COUNT(*) FROM economic_indicator_values;
```

Cross-reference with `raw_responses/` JSON files to verify extraction completeness.

# Data Source Licensing & Legal Compliance

## Disclaimer

This document provides a summary of data source licensing for reference purposes only.
It does not constitute legal advice. Always consult the original Terms of Service before
commercial use. License terms may change — verify current terms at the linked URLs.

## Source License Summary

| Source | License Type | Free Tier | Commercial Redistribution | Attribution Required | Link |
|--------|-------------|-----------|--------------------------|---------------------|------|
| Frankfurter | Open Source (MIT) | ✅ Unlimited | ✅ Allowed | No | [Terms](https://www.frankfurter.dev) |
| European Central Bank | Public Data | ✅ Unlimited | ✅ Allowed with attribution | Yes — cite ECB | [Policy](https://www.ecb.europa.eu/home/disclaimer/html/index.en.html) |
| CoinGecko | Freemium API | ✅ 10-30 req/min | ⚠️ Free tier: personal only | Yes — "Powered by CoinGecko" | [Terms](https://www.coingecko.com/en/terms) |
| CoinGecko Pro | Paid API | 500 req/min | ✅ Allowed with paid plan | Yes | [Pricing](https://www.coingecko.com/en/api/pricing) |
| FRED (St. Louis Fed) | Public Domain | ✅ 120 req/min | ✅ Allowed with attribution | Yes — cite source agency | [Terms](https://fred.stlouisfed.org/docs/api/terms_of_use.html) |
| Yahoo Finance | Unofficial/Scraping | ✅ No official API | ❌ TOS prohibits scraping | N/A | [TOS](https://legal.yahoo.com/us/en/yahoo/terms/otos/index.html) |
| Alpha Vantage | Freemium API | ✅ 25 req/day | ⚠️ Free: personal only | Check license | [Terms](https://www.alphavantage.co/terms_of_service/) |
| World Bank | CC BY-4.0 | ✅ Unlimited | ✅ Allowed with attribution | Yes — "World Bank Open Data" | [Terms](https://www.worldbank.org/en/about/legal/terms-of-use-for-datasets) |
| Twelve Data | Freemium API | ✅ 8 req/min | ⚠️ Free: personal only | Check license | [Terms](https://twelvedata.com/terms) |

## Implemented Sources — Detailed Analysis

### 1. Frankfurter API (Forex)
- **License:** MIT open source, wraps ECB data
- **Rate Limits:** No enforced limit (be respectful)
- **Commercial Use:** ✅ Fully allowed — MIT license permits commercial redistribution
- **Attribution:** Not required but recommended
- **Data Origin:** European Central Bank reference rates
- **Risk Level:** 🟢 LOW

### 2. CoinGecko API (Crypto)
- **License:** Proprietary freemium
- **Rate Limits:** Free tier — 10-30 requests/minute, Demo API key available
- **Commercial Use:** ⚠️ Free tier restricted to personal/non-commercial use
- **Attribution:** Required — must display "Powered by CoinGecko"
- **For Commercial Launch:** Paid plan required (~\$129/month for Analyst plan)
- **Risk Level:** 🟡 MEDIUM — requires paid upgrade for production

### 3. FRED API (Economic Data)
- **License:** Public domain (US Government data)
- **Rate Limits:** 120 requests/minute per API key
- **Commercial Use:** ✅ Allowed — US Government data is public domain
- **Attribution:** Required — must cite the original source agency (e.g., "Source: U.S. Bureau of Labor Statistics")
- **Data Coverage:** 800,000+ time series
- **Risk Level:** 🟢 LOW

## Attribution Requirements

When using data from these sources, include the following attributions:

| Source | Required Attribution Text |
|--------|--------------------------|
| ECB/Frankfurter | "Exchange rates provided by the European Central Bank" |
| CoinGecko | "Cryptocurrency data powered by CoinGecko" |
| FRED | "Source: Federal Reserve Bank of St. Louis" + original agency |
| World Bank | "Source: World Bank Open Data, licensed under CC BY-4.0" |

## Commercial Launch Recommendations

### Phase 1 — MVP (Low Risk)
Use only Frankfurter (MIT) and FRED (Public Domain) — both fully free for commercial use.

### Phase 2 — Growth
Add CoinGecko with paid Analyst plan (~\$129/month) for commercial crypto data rights.

### Phase 3 — Scale
Evaluate Alpha Vantage paid plans or Polygon.io for equity data with commercial licenses.

### Sources to Avoid
- **Yahoo Finance** — No official API; scraping violates TOS. High legal risk.
- **Any unofficial API wrappers** — Verify the underlying data source license independently.

## Data Retention Policies

| Source | Retention Requirement | Our Policy |
|--------|----------------------|------------|
| CoinGecko (Free) | Do not cache > 10 minutes (per TOS) | Store historical only; refresh current daily |
| FRED | No restriction | Full historical retention |
| Frankfurter | No restriction | Full historical retention |

## Compliance Checklist

- [ ] Verify current TOS before any commercial deployment
- [ ] Implement required attribution in all user-facing outputs
- [ ] Upgrade CoinGecko to paid plan before commercial launch
- [ ] Register separate FRED API keys for production vs development
- [ ] Set up monitoring for API rate limit compliance
- [ ] Document data lineage for audit purposes

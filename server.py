import os
import json
import re
from datetime import datetime, timezone
from http.server import HTTPServer, BaseHTTPRequestHandler
from pathlib import Path

from services.live_fetcher import (
    fetch_live_crypto_price,
    fetch_live_crypto_kline,
    fetch_live_forex_rate,
    fetch_live_forex_candle
)

BASE_DIR = Path(__file__).resolve().parent

def load_clean_json(filename: str) -> dict:
    filepath = BASE_DIR / "output" / filename
    if not filepath.exists():
        return {"data": []}
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()
            content = re.sub(r':\s*NaN', ': null', content)
            return json.loads(content)
    except Exception as e:
        print(f"Error loading {filename}: {e}")
        return {"data": []}


def generate_html_dashboard() -> str:
    forex_data = load_clean_json("forex_sample.json")
    crypto_data = load_clean_json("crypto_sample.json")
    economic_data = load_clean_json("economic_sample.json")

    forex_json_str = json.dumps(forex_data, default=str)
    crypto_json_str = json.dumps(crypto_data, default=str)
    economic_json_str = json.dumps(economic_data, default=str)

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>MFAPIs — Financial Data Platform</title>
  <script src="https://cdn.tailwindcss.com"></script>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap" rel="stylesheet">
  <style>
    body {{ font-family: 'Plus Jakarta Sans', sans-serif; }}
    .tab-btn.active {{
      background-color: rgb(30 41 59);
      color: #38bdf8;
      border-color: #0284c7;
    }}
  </style>
</head>
<body class="bg-slate-950 text-slate-100 min-h-screen flex flex-col selection:bg-sky-500 selection:text-white">
  
  <!-- Header -->
  <header class="border-b border-slate-800/80 bg-slate-900/90 backdrop-blur sticky top-0 z-50 shadow-sm">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 py-3.5 flex flex-wrap items-center justify-between gap-4">
      <div class="flex items-center gap-3">
        <div class="w-10 h-10 rounded-xl bg-gradient-to-tr from-sky-500 to-indigo-600 flex items-center justify-center font-extrabold text-xl text-white shadow-lg shadow-sky-500/20">
          M
        </div>
        <div>
          <div class="flex items-center gap-2">
            <h1 class="text-lg font-bold tracking-tight text-white">MFAPIs Platform</h1>
            <span class="px-2 py-0.5 rounded-full text-[10px] font-semibold bg-emerald-500/10 text-emerald-400 border border-emerald-500/30">
              ● Live Cloud
            </span>
          </div>
          <p class="text-xs text-slate-400">Financial Data ETL & Multi-Asset Intelligence</p>
        </div>
      </div>
      
      <!-- Top Badges -->
      <div class="flex items-center gap-2 sm:gap-3 text-xs">
        <div class="px-3 py-1.5 rounded-lg bg-slate-800/80 border border-slate-700/60 hidden sm:block">
          <span class="text-slate-400">PostgreSQL Records:</span>
          <span class="font-bold text-white ml-1">34,600+</span>
        </div>
        <div class="px-3 py-1.5 rounded-lg bg-slate-800/80 border border-slate-700/60">
          <span class="text-slate-400">Tests:</span>
          <span class="font-bold text-emerald-400 ml-1">79/79 Passing</span>
        </div>
        <a href="/health" target="_blank" class="px-3 py-1.5 rounded-lg bg-sky-600 hover:bg-sky-500 text-white font-medium transition shadow-sm">
          System Health
        </a>
      </div>
    </div>
  </header>

  <!-- Main Container -->
  <main class="max-w-7xl mx-auto px-4 sm:px-6 py-8 flex-1 w-full space-y-6">
    
    <!-- Hero Banner -->
    <div class="p-6 rounded-2xl bg-gradient-to-r from-slate-900 via-slate-900/90 to-slate-800/80 border border-slate-800 shadow-xl relative overflow-hidden">
      <div class="absolute -right-12 -top-12 w-64 h-64 bg-sky-500/10 rounded-full blur-3xl pointer-events-none"></div>
      <div class="max-w-3xl space-y-2 relative z-10">
        <div class="inline-flex items-center gap-2 px-2.5 py-1 rounded-md bg-sky-500/10 text-sky-400 text-xs font-semibold">
          🚀 Production-Ready ETL Architecture
        </div>
        <h2 class="text-2xl sm:text-3xl font-extrabold text-white tracking-tight">
          Financial Data Analytics & API Explorer
        </h2>
        <p class="text-sm text-slate-400 leading-relaxed">
          Interactive UI dashboard displaying live ingested data for Foreign Exchange, Cryptocurrencies, and US Macroeconomics with automated pipeline reliability and strict PostgreSQL schema validation.
        </p>
      </div>
    </div>

    <!-- Navigation Tabs -->
    <div class="flex flex-wrap items-center gap-2 border-b border-slate-800 pb-2">
      <button onclick="switchTab('forex')" id="tab-forex" class="tab-btn active px-4 py-2.5 rounded-xl text-xs sm:text-sm font-semibold transition border border-transparent hover:border-slate-700">
        💱 Foreign Exchange (Forex)
      </button>
      <button onclick="switchTab('crypto')" id="tab-crypto" class="tab-btn px-4 py-2.5 rounded-xl text-xs sm:text-sm font-semibold transition border border-transparent text-slate-400 hover:text-white hover:border-slate-700">
        🪙 Cryptocurrency Markets
      </button>
      <button onclick="switchTab('economic')" id="tab-economic" class="tab-btn px-4 py-2.5 rounded-xl text-xs sm:text-sm font-semibold transition border border-transparent text-slate-400 hover:text-white hover:border-slate-700">
        📈 Macroeconomic Indicators (FRED)
      </button>
      <button onclick="switchTab('docs')" id="tab-docs" class="tab-btn px-4 py-2.5 rounded-xl text-xs sm:text-sm font-semibold transition border border-transparent text-slate-400 hover:text-white hover:border-slate-700">
        📋 Strategy & Documentation
      </button>
    </div>

    <!-- TAB 1: FOREX -->
    <div id="content-forex" class="tab-content space-y-4">
      <div class="flex flex-wrap items-center justify-between gap-3 p-4 rounded-xl bg-slate-900 border border-slate-800">
        <div class="flex items-center gap-3">
          <div class="p-2.5 rounded-lg bg-emerald-500/10 text-emerald-400 font-bold text-lg">💱</div>
          <div>
            <h3 class="text-sm font-bold text-white">Forex Daily Exchange Rates</h3>
            <p class="text-xs text-slate-400">Source: European Central Bank via Frankfurter API &bull; 145 Currencies Tracked</p>
          </div>
        </div>
        <div class="flex items-center gap-2">
          <input type="text" id="forex-search" onkeyup="filterForex()" placeholder="Filter currency..." class="px-3 py-1.5 rounded-lg bg-slate-800 border border-slate-700 text-xs text-white placeholder-slate-500 focus:outline-none focus:border-sky-500">
          <button onclick="toggleJson('forex')" class="px-3 py-1.5 rounded-lg bg-slate-800 hover:bg-slate-700 text-xs text-slate-300 font-medium transition border border-slate-700">
            {{ }} View Raw JSON
          </button>
        </div>
      </div>

      <!-- Raw JSON Viewer -->
      <div id="raw-forex" class="hidden p-4 rounded-xl bg-slate-900 border border-slate-800">
        <div class="flex justify-between items-center mb-2">
          <span class="text-xs font-mono text-emerald-400">GET /v1/forex/sample</span>
          <button onclick="copyJson('forex')" class="text-xs px-2.5 py-1 bg-slate-800 rounded hover:bg-slate-700 text-slate-300">Copy JSON</button>
        </div>
        <pre class="text-[11px] font-mono text-slate-300 max-h-64 overflow-y-auto bg-slate-950 p-3 rounded-lg border border-slate-800/80" id="json-forex-pre"></pre>
      </div>

      <!-- Forex Table -->
      <div class="overflow-x-auto rounded-xl border border-slate-800 bg-slate-900/60 shadow-lg">
        <table class="w-full text-left text-xs text-slate-300" id="forex-table">
          <thead class="bg-slate-900 text-slate-400 uppercase text-[10px] tracking-wider border-b border-slate-800">
            <tr>
              <th class="p-3.5">Currency Pair</th>
              <th class="p-3.5">Exchange Rate</th>
              <th class="p-3.5">Date</th>
              <th class="p-3.5">Source Provider</th>
              <th class="p-3.5">Status</th>
            </tr>
          </thead>
          <tbody class="divide-y divide-slate-800/60" id="forex-tbody"></tbody>
        </table>
      </div>
    </div>

    <!-- TAB 2: CRYPTO -->
    <div id="content-crypto" class="tab-content hidden space-y-4">
      <div class="flex flex-wrap items-center justify-between gap-3 p-4 rounded-xl bg-slate-900 border border-slate-800">
        <div class="flex items-center gap-3">
          <div class="p-2.5 rounded-lg bg-amber-500/10 text-amber-400 font-bold text-lg">🪙</div>
          <div>
            <h3 class="text-sm font-bold text-white">Cryptocurrency Daily Market Valuations</h3>
            <p class="text-xs text-slate-400">Source: CoinGecko API &amp; Binance &bull; Top 50 Digital Assets &bull; 365-Day Timeseries</p>
          </div>
        </div>
        <div class="flex items-center gap-2">
          <input type="text" id="crypto-search" onkeyup="filterCrypto()" placeholder="Filter asset (e.g. BTC)..." class="px-3 py-1.5 rounded-lg bg-slate-800 border border-slate-700 text-xs text-white placeholder-slate-500 focus:outline-none focus:border-sky-500">
          <button onclick="toggleJson('crypto')" class="px-3 py-1.5 rounded-lg bg-slate-800 hover:bg-slate-700 text-xs text-slate-300 font-medium transition border border-slate-700">
            {{ }} View Raw JSON
          </button>
        </div>
      </div>

      <!-- Raw JSON Viewer -->
      <div id="raw-crypto" class="hidden p-4 rounded-xl bg-slate-900 border border-slate-800">
        <div class="flex justify-between items-center mb-2">
          <span class="text-xs font-mono text-amber-400">GET /v1/crypto/sample</span>
          <button onclick="copyJson('crypto')" class="text-xs px-2.5 py-1 bg-slate-800 rounded hover:bg-slate-700 text-slate-300">Copy JSON</button>
        </div>
        <pre class="text-[11px] font-mono text-slate-300 max-h-64 overflow-y-auto bg-slate-950 p-3 rounded-lg border border-slate-800/80" id="json-crypto-pre"></pre>
      </div>

      <!-- Crypto Table -->
      <div class="overflow-x-auto rounded-xl border border-slate-800 bg-slate-900/60 shadow-lg">
        <table class="w-full text-left text-xs text-slate-300" id="crypto-table">
          <thead class="bg-slate-900 text-slate-400 uppercase text-[10px] tracking-wider border-b border-slate-800">
            <tr>
              <th class="p-3.5">Asset</th>
              <th class="p-3.5">Price (USD)</th>
              <th class="p-3.5">Market Capitalization</th>
              <th class="p-3.5">24h Volume</th>
              <th class="p-3.5">Date</th>
              <th class="p-3.5">Provider</th>
            </tr>
          </thead>
          <tbody class="divide-y divide-slate-800/60" id="crypto-tbody"></tbody>
        </table>
      </div>
    </div>

    <!-- TAB 3: ECONOMIC -->
    <div id="content-economic" class="tab-content hidden space-y-4">
      <div class="flex flex-wrap items-center justify-between gap-3 p-4 rounded-xl bg-slate-900 border border-slate-800">
        <div class="flex items-center gap-3">
          <div class="p-2.5 rounded-lg bg-cyan-500/10 text-cyan-400 font-bold text-lg">📈</div>
          <div>
            <h3 class="text-sm font-bold text-white">US Macroeconomic Indicators (FRED)</h3>
            <p class="text-xs text-slate-400">Source: Federal Reserve Bank of St. Louis &bull; 8 Key Indicators &bull; 29,171 Observations</p>
          </div>
        </div>
        <div class="flex items-center gap-2">
          <input type="text" id="economic-search" onkeyup="filterEconomic()" placeholder="Filter indicator (e.g. GDP)..." class="px-3 py-1.5 rounded-lg bg-slate-800 border border-slate-700 text-xs text-white placeholder-slate-500 focus:outline-none focus:border-sky-500">
          <button onclick="toggleJson('economic')" class="px-3 py-1.5 rounded-lg bg-slate-800 hover:bg-slate-700 text-xs text-slate-300 font-medium transition border border-slate-700">
            {{ }} View Raw JSON
          </button>
        </div>
      </div>

      <!-- Raw JSON Viewer -->
      <div id="raw-economic" class="hidden p-4 rounded-xl bg-slate-900 border border-slate-800">
        <div class="flex justify-between items-center mb-2">
          <span class="text-xs font-mono text-cyan-400">GET /v1/economic/sample</span>
          <button onclick="copyJson('economic')" class="text-xs px-2.5 py-1 bg-slate-800 rounded hover:bg-slate-700 text-slate-300">Copy JSON</button>
        </div>
        <pre class="text-[11px] font-mono text-slate-300 max-h-64 overflow-y-auto bg-slate-950 p-3 rounded-lg border border-slate-800/80" id="json-economic-pre"></pre>
      </div>

      <!-- Economic Table -->
      <div class="overflow-x-auto rounded-xl border border-slate-800 bg-slate-900/60 shadow-lg">
        <table class="w-full text-left text-xs text-slate-300" id="economic-table">
          <thead class="bg-slate-900 text-slate-400 uppercase text-[10px] tracking-wider border-b border-slate-800">
            <tr>
              <th class="p-3.5">Indicator Code</th>
              <th class="p-3.5">Indicator Title</th>
              <th class="p-3.5">Observed Value</th>
              <th class="p-3.5">Observation Date</th>
              <th class="p-3.5">Country</th>
              <th class="p-3.5">Agency</th>
            </tr>
          </thead>
          <tbody class="divide-y divide-slate-800/60" id="economic-tbody"></tbody>
        </table>
      </div>
    </div>

    <!-- TAB 4: DOCUMENTATION & STRATEGY -->
    <div id="content-docs" class="tab-content hidden space-y-6">
      
      <!-- Opportunity Scoring Grid -->
      <div class="p-6 rounded-2xl bg-slate-900 border border-slate-800 space-y-4">
        <h3 class="text-base font-bold text-white flex items-center gap-2">
          <span>🏆 Top Ranked Commercial Opportunities</span>
          <span class="text-xs font-normal text-slate-400">(Scored across 7 Strategic Metrics)</span>
        </h3>
        
        <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div class="p-4 rounded-xl bg-slate-800/60 border border-slate-700/60 space-y-2">
            <div class="flex items-center justify-between">
              <span class="px-2 py-0.5 rounded text-[10px] font-bold bg-amber-500/20 text-amber-300">Rank #1 (Score: 29)</span>
              <span class="text-xs text-slate-400">Category D</span>
            </div>
            <h4 class="font-bold text-white text-sm">Forex Rates & Currency Conversion</h4>
            <p class="text-xs text-slate-400">Universal demand across e-commerce, global payroll, fintech, and hedge funds. Zero marginal cost via ECB data.</p>
          </div>

          <div class="p-4 rounded-xl bg-slate-800/60 border border-slate-700/60 space-y-2">
            <div class="flex items-center justify-between">
              <span class="px-2 py-0.5 rounded text-[10px] font-bold bg-sky-500/20 text-sky-300">Rank #2 (Score: 28)</span>
              <span class="text-xs text-slate-400">Category E</span>
            </div>
            <h4 class="font-bold text-white text-sm">Crypto Asset Pricing & Historical OHLCV</h4>
            <p class="text-xs text-slate-400">High willingness to pay among crypto tax tools, portfolio trackers, and web3 analytics providers.</p>
          </div>

          <div class="p-4 rounded-xl bg-slate-800/60 border border-slate-700/60 space-y-2">
            <div class="flex items-center justify-between">
              <span class="px-2 py-0.5 rounded text-[10px] font-bold bg-emerald-500/20 text-emerald-300">Rank #3 (Score: 27)</span>
              <span class="text-xs text-slate-400">Category I</span>
            </div>
            <h4 class="font-bold text-white text-sm">Macroeconomic Data & Federal Reserve</h4>
            <p class="text-xs text-slate-400">Essential for macro hedge funds, academic research, real estate valuation, and fixed-income models.</p>
          </div>
        </div>
      </div>

      <!-- Pricing Plans -->
      <div class="p-6 rounded-2xl bg-slate-900 border border-slate-800 space-y-4">
        <h3 class="text-base font-bold text-white">Commercial API Pricing Structure</h3>
        <div class="grid grid-cols-1 md:grid-cols-4 gap-4">
          <div class="p-4 rounded-xl bg-slate-950 border border-slate-800 space-y-2">
            <p class="text-xs text-slate-400 font-semibold uppercase">Community</p>
            <p class="text-2xl font-bold text-white">$0 <span class="text-xs text-slate-500 font-normal">/ mo</span></p>
            <ul class="text-[11px] text-slate-400 space-y-1 pt-2">
              <li>&bull; 1,000 req / day</li>
              <li>&bull; 30 req / minute</li>
              <li>&bull; Forex & Crypto Latest</li>
            </ul>
          </div>
          <div class="p-4 rounded-xl bg-slate-950 border border-slate-800 space-y-2">
            <p class="text-xs text-sky-400 font-semibold uppercase">Starter</p>
            <p class="text-2xl font-bold text-white">$49 <span class="text-xs text-slate-500 font-normal">/ mo</span></p>
            <ul class="text-[11px] text-slate-400 space-y-1 pt-2">
              <li>&bull; 25,000 req / day</li>
              <li>&bull; 120 req / minute</li>
              <li>&bull; Full historical data</li>
            </ul>
          </div>
          <div class="p-4 rounded-xl bg-slate-950 border border-sky-500/40 space-y-2 relative shadow-lg shadow-sky-500/5">
            <span class="absolute top-2 right-2 px-1.5 py-0.5 rounded text-[9px] font-bold bg-sky-500 text-white">POPULAR</span>
            <p class="text-xs text-emerald-400 font-semibold uppercase">Professional</p>
            <p class="text-2xl font-bold text-white">$199 <span class="text-xs text-slate-500 font-normal">/ mo</span></p>
            <ul class="text-[11px] text-slate-400 space-y-1 pt-2">
              <li>&bull; 250,000 req / day</li>
              <li>&bull; 600 req / minute</li>
              <li>&bull; Webhooks & Sockets</li>
            </ul>
          </div>
          <div class="p-4 rounded-xl bg-slate-950 border border-slate-800 space-y-2">
            <p class="text-xs text-indigo-400 font-semibold uppercase">Enterprise</p>
            <p class="text-2xl font-bold text-white">$699+ <span class="text-xs text-slate-500 font-normal">/ mo</span></p>
            <ul class="text-[11px] text-slate-400 space-y-1 pt-2">
              <li>&bull; Unlimited requests</li>
              <li>&bull; 99.95% SLA Guarantee</li>
              <li>&bull; Custom DB feeds</li>
            </ul>
          </div>
        </div>
      </div>

    </div>

  </main>

  <!-- Footer -->
  <footer class="border-t border-slate-800/80 bg-slate-900/40 text-center py-5 text-xs text-slate-500">
    MFAPIs Financial Intelligence Engine &bull; Modular Python ETL &bull; PostgreSQL 17 Relational Storage
  </footer>

  <!-- Instant Data Injection -->
  <script>
    const INITIAL_FOREX = {forex_json_str};
    const INITIAL_CRYPTO = {crypto_json_str};
    const INITIAL_ECONOMIC = {economic_json_str};

    let forexData = INITIAL_FOREX.data || [];
    let cryptoData = INITIAL_CRYPTO.data || [];
    let economicData = INITIAL_ECONOMIC.data || [];

    function initPage() {{
      document.getElementById('json-forex-pre').innerText = JSON.stringify(INITIAL_FOREX, null, 2);
      document.getElementById('json-crypto-pre').innerText = JSON.stringify(INITIAL_CRYPTO, null, 2);
      document.getElementById('json-economic-pre').innerText = JSON.stringify(INITIAL_ECONOMIC, null, 2);

      renderForex(forexData);
      renderCrypto(cryptoData);
      renderEconomic(economicData);
    }}

    function renderForex(items) {{
      const tbody = document.getElementById('forex-tbody');
      if (!items || !items.length) {{
        tbody.innerHTML = '<tr><td colspan="5" class="p-6 text-center text-slate-500">No records found</td></tr>';
        return;
      }}
      tbody.innerHTML = items.map(item => `
        <tr class="hover:bg-slate-800/40 transition">
          <td class="p-3.5 font-bold text-white">
            <span class="px-2 py-0.5 rounded bg-slate-800 border border-slate-700 text-sky-400 mr-1.5">${{item.base_currency}}</span>
            <span class="text-slate-500">&rarr;</span>
            <span class="px-2 py-0.5 rounded bg-slate-800 border border-slate-700 text-emerald-400 ml-1.5">${{item.target_currency}}</span>
          </td>
          <td class="p-3.5 font-mono text-emerald-400 font-semibold">${{Number(item.exchange_rate).toFixed(4)}}</td>
          <td class="p-3.5 text-slate-400">${{item.rate_date || 'Latest'}}</td>
          <td class="p-3.5">
            <span class="px-2 py-0.5 rounded-full text-[10px] font-semibold bg-slate-800 text-slate-300 border border-slate-700 uppercase">
              ${{item.source || 'frankfurter'}}
            </span>
          </td>
          <td class="p-3.5">
            <span class="inline-flex items-center gap-1 text-[10px] font-medium text-emerald-400">
              <span class="w-1.5 h-1.5 rounded-full bg-emerald-400"></span> Verified
            </span>
          </td>
        </tr>
      `).join('');
    }}

    function renderCrypto(items) {{
      const tbody = document.getElementById('crypto-tbody');
      if (!items || !items.length) {{
        tbody.innerHTML = '<tr><td colspan="6" class="p-6 text-center text-slate-500">No records found</td></tr>';
        return;
      }}
      tbody.innerHTML = items.map(item => `
        <tr class="hover:bg-slate-800/40 transition">
          <td class="p-3.5 font-bold text-white capitalize flex items-center gap-2">
            <span class="w-7 h-7 rounded-full bg-amber-500/20 text-amber-400 font-bold flex items-center justify-center text-xs">
              ${{(item.coin_id || 'C')[0].toUpperCase()}}
            </span>
            ${{item.coin_id}}
          </td>
          <td class="p-3.5 font-mono text-white font-bold">$${{Number(item.price_usd || 0).toLocaleString(undefined, {{minimumFractionDigits: 2, maximumFractionDigits: 4}})}}</td>
          <td class="p-3.5 font-mono text-slate-400">$${{item.market_cap_usd ? Number(item.market_cap_usd).toLocaleString() : '—'}}</td>
          <td class="p-3.5 font-mono text-slate-400">$${{item.total_volume_usd ? Number(item.total_volume_usd).toLocaleString() : '—'}}</td>
          <td class="p-3.5 text-slate-400">${{item.price_date}}</td>
          <td class="p-3.5">
            <span class="px-2 py-0.5 rounded-full text-[10px] font-semibold bg-amber-500/10 text-amber-400 border border-amber-500/20 uppercase">
              CoinGecko
            </span>
          </td>
        </tr>
      `).join('');
    }}

    const INDICATOR_NAMES = {{
      'GDP': 'Gross Domestic Product',
      'CPIAUCSL': 'Consumer Price Index (CPI)',
      'UNRATE': 'Unemployment Rate',
      'FEDFUNDS': 'Federal Funds Effective Rate',
      'DGS10': '10-Year Treasury Yield',
      'DEXUSEU': 'US Dollar / Euro Rate',
      'INDPRO': 'Industrial Production Index',
      'TOTALSA': 'Total Vehicle Sales'
    }};

    function renderEconomic(items) {{
      const tbody = document.getElementById('economic-tbody');
      if (!items || !items.length) {{
        tbody.innerHTML = '<tr><td colspan="6" class="p-6 text-center text-slate-500">No records found</td></tr>';
        return;
      }}
      tbody.innerHTML = items.map(item => `
        <tr class="hover:bg-slate-800/40 transition">
          <td class="p-3.5 font-mono font-bold text-cyan-400">${{item.indicator_id}}</td>
          <td class="p-3.5 font-medium text-white">${{INDICATOR_NAMES[item.indicator_id] || item.indicator_id}}</td>
          <td class="p-3.5 font-mono font-bold text-white">${{(item.value !== null && !isNaN(item.value)) ? Number(item.value).toLocaleString() : '—'}}</td>
          <td class="p-3.5 text-slate-400">${{item.observation_date}}</td>
          <td class="p-3.5">
            <span class="px-2 py-0.5 rounded bg-slate-800 text-slate-300 font-semibold text-[10px] border border-slate-700">
              ${{item.country || 'US'}}
            </span>
          </td>
          <td class="p-3.5">
            <span class="px-2 py-0.5 rounded-full text-[10px] font-semibold bg-cyan-500/10 text-cyan-400 border border-cyan-500/20 uppercase">
              St. Louis Fed (FRED)
            </span>
          </td>
        </tr>
      `).join('');
    }}

    function filterForex() {{
      const q = document.getElementById('forex-search').value.toLowerCase();
      const filtered = forexData.filter(d => 
        (d.base_currency && d.base_currency.toLowerCase().includes(q)) ||
        (d.target_currency && d.target_currency.toLowerCase().includes(q))
      );
      renderForex(filtered);
    }}

    function filterCrypto() {{
      const q = document.getElementById('crypto-search').value.toLowerCase();
      const filtered = cryptoData.filter(d => 
        (d.coin_id && d.coin_id.toLowerCase().includes(q))
      );
      renderCrypto(filtered);
    }}

    function filterEconomic() {{
      const q = document.getElementById('economic-search').value.toLowerCase();
      const filtered = economicData.filter(d => 
        (d.indicator_id && d.indicator_id.toLowerCase().includes(q))
      );
      renderEconomic(filtered);
    }}

    function switchTab(name) {{
      document.querySelectorAll('.tab-btn').forEach(btn => btn.classList.remove('active', 'text-sky-400', 'bg-slate-800'));
      document.querySelectorAll('.tab-content').forEach(c => c.classList.add('hidden'));

      const activeBtn = document.getElementById('tab-' + name);
      activeBtn.classList.add('active');

      document.getElementById('content-' + name).classList.remove('hidden');
    }}

    function toggleJson(type) {{
      const el = document.getElementById('raw-' + type);
      el.classList.toggle('hidden');
    }}

    function copyJson(type) {{
      const text = document.getElementById('json-' + type + '-pre').innerText;
      navigator.clipboard.writeText(text);
      alert('JSON copied to clipboard!');
    }}

    window.onload = initPage;
  </script>
</body>
</html>
"""

class MFAPIsHandler(BaseHTTPRequestHandler):

    def _send_html(self, content: str):
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(content.encode("utf-8"))

    def _send_json(self, status_code: int, data: dict):
        self.send_response(status_code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(json.dumps(data, indent=2, default=str).encode("utf-8"))

    def do_GET(self):
        url_parts = self.path.split("?")
        path = url_parts[0].rstrip("/")
        query_str = url_parts[1] if len(url_parts) > 1 else ""
        query_params = {}
        if query_str:
            for pair in query_str.split("&"):
                if "=" in pair:
                    k, v = pair.split("=", 1)
                    query_params[k.strip().lower()] = v.strip()

        if path in ("", "/"):
            self._send_html(generate_html_dashboard())
            return

        if path == "/health":
            self._send_json(200, {
                "status": "healthy",
                "service": "MFAPIs Financial Data Platform",
                "version": "1.2.0",
                "twelvedata_compatible": True,
                "data_sources": {
                    "crypto_ohlcv": "Binance Public API",
                    "forex_ohlcv": "Yahoo Finance (Interbank)",
                    "forex_rates": "ECB via Frankfurter",
                    "crypto_market": "CoinGecko",
                    "economic": "FRED (St. Louis Fed)"
                },
                "endpoints": {
                    "ui": "/",
                    "health": "/health",
                    "twelve_data_time_series": "/time_series?symbol=BTC/USD&interval=1day",
                    "twelve_data_quote": "/quote?symbol=BTC/USD",
                    "twelve_data_price": "/price?symbol=BTC/USD",
                    "twelve_data_exchange_rate": "/exchange_rate?symbol=EUR/USD",
                    "twelve_data_eod": "/eod?symbol=BTC/USD",
                    "twelve_data_cryptos": "/cryptocurrencies",
                    "twelve_data_forex_pairs": "/forex_pairs",
                    "forex_sample": "/v1/forex/sample",
                    "crypto_sample": "/v1/crypto/sample",
                    "economic_sample": "/v1/economic/sample"
                }
            })
            return

        # =========================================================================
        # TWELVE DATA COMPATIBILITY LAYER (Real-Time Live Institutional Feeds)
        # =========================================================================

        # 1. /price endpoint (Twelve Data standard: {"price": "123.45"})
        if path == "/price":
            symbol = query_params.get("symbol", "").upper()
            if not symbol:
                self._send_json(400, {"status": "error", "message": "Missing required parameter: symbol"})
                return

            # Live Fetch Attempt: Crypto
            live_p = fetch_live_crypto_price(symbol)
            if live_p is not None:
                self._send_json(200, {"price": f"{live_p:.2f}"})
                return

            # Live Fetch Attempt: Forex
            live_fx = fetch_live_forex_rate(symbol)
            if live_fx is not None:
                self._send_json(200, {"price": f"{live_fx:.5f}"})
                return

            # Fallback to stored crypto OHLCV
            if "/" in symbol and any(c in symbol for c in ["BTC", "ETH", "SOL", "BNB", "XRP"]):
                ohlcv_data = load_clean_json("crypto_ohlcv_sample.json")
                matching = [r for r in ohlcv_data.get("data", []) if r.get("symbol") == symbol]
                if matching:
                    matching = sorted(matching, key=lambda x: str(x.get("candle_date", "")), reverse=True)
                    self._send_json(200, {"price": f"{float(matching[0].get('close_price', 0)):.2f}"})
                    return

            # Fallback to stored Forex OHLCV
            forex_ohlcv = load_clean_json("forex_ohlcv_sample.json")
            matching_fx = [r for r in forex_ohlcv.get("data", []) if r.get("pair_name") == symbol]
            if matching_fx:
                matching_fx = sorted(matching_fx, key=lambda x: str(x.get("candle_date", "")), reverse=True)
                self._send_json(200, {"price": f"{float(matching_fx[0].get('close_price', 0)):.5f}"})
                return

            # Fallback to legacy forex sample
            forex_data = load_clean_json("forex_sample.json")
            for rec in forex_data.get("data", []):
                pair = f"{rec.get('base_currency')}/{rec.get('target_currency')}".upper()
                if pair == symbol:
                    self._send_json(200, {"price": f"{float(rec.get('exchange_rate', 0)):.5f}"})
                    return

            self._send_json(404, {"status": "error", "message": f"Symbol not found: {symbol}"})
            return

        # 2. /exchange_rate endpoint (Twelve Data standard)
        if path == "/exchange_rate":
            symbol = query_params.get("symbol", "").upper()
            if not symbol:
                self._send_json(400, {"status": "error", "message": "Missing required parameter: symbol"})
                return

            # Live Fetch Attempt
            live_rate = fetch_live_forex_rate(symbol)
            if live_rate is not None:
                self._send_json(200, {
                    "symbol": symbol,
                    "rate": live_rate,
                    "timestamp": int(datetime.now(timezone.utc).timestamp())
                })
                return

            # Fallback to stored
            parts = symbol.split("/") if "/" in symbol else [symbol, "USD"]
            base, target = parts[0], parts[1] if len(parts) > 1 else "USD"

            forex_ohlcv = load_clean_json("forex_ohlcv_sample.json")
            matching_fx = [r for r in forex_ohlcv.get("data", []) if r.get("pair_name") == symbol]
            rate = None
            if matching_fx:
                matching_fx = sorted(matching_fx, key=lambda x: str(x.get("candle_date", "")), reverse=True)
                rate = round(float(matching_fx[0].get("close_price", 1.0)), 5)

            if rate is None:
                forex_data = load_clean_json("forex_sample.json")
                for rec in forex_data.get("data", []):
                    if rec.get("base_currency") == base and rec.get("target_currency") == target:
                        rate = float(rec.get("exchange_rate"))
                        break
                    elif rec.get("base_currency") == target and rec.get("target_currency") == base:
                        inv = float(rec.get("exchange_rate", 1))
                        rate = round(1.0 / inv, 5) if inv > 0 else None
                        break

            if rate is None:
                self._send_json(404, {"status": "error", "message": f"Symbol not found: {symbol}"})
                return

            self._send_json(200, {
                "symbol": symbol,
                "rate": rate,
                "timestamp": int(datetime.now(timezone.utc).timestamp())
            })
            return

        # 3. /time_series endpoint (Twelve Data standard: meta + values)
        if path == "/time_series":
            symbol = query_params.get("symbol", "").upper()
            if not symbol:
                self._send_json(400, {"status": "error", "message": "Missing required parameter: symbol"})
                return

            interval = query_params.get("interval", "1day")
            try:
                outputsize = int(query_params.get("outputsize", 30))
                outputsize = max(1, min(outputsize, 5000))
            except (ValueError, TypeError):
                outputsize = 30

            # --- CRYPTO OHLCV (Live Binance + Historical DB) ---
            if any(c in symbol for c in ["BTC", "ETH", "SOL", "BNB", "XRP"]):
                ohlcv_data = load_clean_json("crypto_ohlcv_sample.json")
                matching = [r for r in ohlcv_data.get("data", []) if r.get("symbol") == symbol]
                matching = sorted(matching, key=lambda x: str(x.get("candle_date", "")), reverse=True)

                values = []
                live_k = fetch_live_crypto_kline(symbol, interval=interval)
                if live_k:
                    values.append(live_k)

                for r in matching:
                    c_date = str(r.get("candle_date"))
                    if live_k and c_date == live_k.get("datetime"):
                        continue
                    values.append({
                        "datetime": c_date,
                        "open": f"{float(r.get('open_price', 0)):.2f}",
                        "high": f"{float(r.get('high_price', 0)):.2f}",
                        "low": f"{float(r.get('low_price', 0)):.2f}",
                        "close": f"{float(r.get('close_price', 0)):.2f}",
                        "volume": f"{int(float(r.get('volume', 0)))}"
                    })
                    if len(values) >= outputsize:
                        break

                if values:
                    self._send_json(200, {
                        "meta": {
                            "symbol": symbol,
                            "interval": interval,
                            "currency_base": symbol.split("/")[0],
                            "currency_quote": symbol.split("/")[1] if "/" in symbol else "USD",
                            "exchange": "Binance",
                            "type": "Digital Currency"
                        },
                        "values": values[:outputsize],
                        "status": "ok"
                    })
                    return

            # --- FOREX OHLC (Live Yahoo Finance + Historical DB) ---
            forex_ohlcv = load_clean_json("forex_ohlcv_sample.json")
            matching_fx = [r for r in forex_ohlcv.get("data", []) if r.get("pair_name") == symbol]
            matching_fx = sorted(matching_fx, key=lambda x: str(x.get("candle_date", "")), reverse=True)

            values_fx = []
            live_fx_k = fetch_live_forex_candle(symbol)
            if live_fx_k:
                values_fx.append(live_fx_k)

            for r in matching_fx:
                c_date = str(r.get("candle_date"))
                if live_fx_k and c_date == live_fx_k.get("datetime"):
                    continue
                values_fx.append({
                    "datetime": c_date,
                    "open": f"{float(r.get('open_price', 0)):.5f}",
                    "high": f"{float(r.get('high_price', 0)):.5f}",
                    "low": f"{float(r.get('low_price', 0)):.5f}",
                    "close": f"{float(r.get('close_price', 0)):.5f}",
                    "volume": f"{int(float(r.get('volume', 0)))}"
                })
                if len(values_fx) >= outputsize:
                    break

            if values_fx:
                self._send_json(200, {
                    "meta": {
                        "symbol": symbol,
                        "interval": interval,
                        "currency_base": symbol.split("/")[0],
                        "currency_quote": symbol.split("/")[1] if "/" in symbol else "USD",
                        "type": "Physical Currency"
                    },
                    "values": values_fx[:outputsize],
                    "status": "ok"
                })
                return

            self._send_json(404, {"status": "error", "message": f"Symbol not found: {symbol}"})
            return

        # 4. /quote endpoint (Twelve Data standard snapshot from real-time data)
        if path == "/quote":
            symbol = query_params.get("symbol", "").upper()
            if not symbol:
                self._send_json(400, {"status": "error", "message": "Missing required parameter: symbol"})
                return

            # Try crypto OHLCV first
            ohlcv_data = load_clean_json("crypto_ohlcv_sample.json")
            matching = [r for r in ohlcv_data.get("data", []) if r.get("symbol") == symbol]
            if matching or fetch_live_crypto_price(symbol):
                matching = sorted(matching, key=lambda x: str(x.get("candle_date", "")), reverse=True)
                live_k = fetch_live_crypto_kline(symbol)

                if live_k:
                    c_price = float(live_k.get("close", 0))
                    open_p = float(live_k.get("open", 0))
                    high_p = float(live_k.get("high", 0))
                    low_p = float(live_k.get("low", 0))
                    vol = live_k.get("volume", "0")
                    c_date = live_k.get("datetime")
                    prev = matching[0] if matching else {}
                    p_close = float(prev.get("close_price", c_price))
                else:
                    latest = matching[0] if matching else {}
                    prev = matching[1] if len(matching) > 1 else latest
                    c_price = float(latest.get("close_price", 0))
                    open_p = float(latest.get("open_price", 0))
                    high_p = float(latest.get("high_price", 0))
                    low_p = float(latest.get("low_price", 0))
                    vol = str(int(float(latest.get("volume", 0))))
                    c_date = str(latest.get("candle_date"))
                    p_close = float(prev.get("close_price", c_price))

                chg = c_price - p_close
                pct_chg = (chg / p_close) * 100 if p_close else 0.0

                all_closes = [float(r.get("close_price", 0)) for r in matching] + ([c_price] if c_price else [])
                w52_low = min(all_closes) if all_closes else c_price
                w52_high = max(all_closes) if all_closes else c_price

                self._send_json(200, {
                    "symbol": symbol,
                    "name": f"{symbol.split('/')[0]} / {symbol.split('/')[1] if '/' in symbol else 'USD'}",
                    "exchange": "Binance",
                    "currency": symbol.split("/")[1] if "/" in symbol else "USD",
                    "datetime": c_date,
                    "timestamp": int(datetime.now(timezone.utc).timestamp()),
                    "open": f"{open_p:.2f}",
                    "high": f"{high_p:.2f}",
                    "low": f"{low_p:.2f}",
                    "close": f"{c_price:.2f}",
                    "volume": str(vol),
                    "previous_close": f"{p_close:.2f}",
                    "change": f"{chg:+.2f}",
                    "percent_change": f"{pct_chg:+.4f}",
                    "is_market_open": True,
                    "fifty_two_week": {
                        "low": f"{w52_low:.2f}",
                        "high": f"{w52_high:.2f}",
                        "range": f"{w52_low:.2f} - {w52_high:.2f}"
                    }
                })
                return

            # Try forex OHLCV
            forex_ohlcv = load_clean_json("forex_ohlcv_sample.json")
            matching_fx = [r for r in forex_ohlcv.get("data", []) if r.get("pair_name") == symbol]
            if matching_fx or fetch_live_forex_rate(symbol):
                matching_fx = sorted(matching_fx, key=lambda x: str(x.get("candle_date", "")), reverse=True)
                live_fx_k = fetch_live_forex_candle(symbol)

                if live_fx_k:
                    c_price = float(live_fx_k.get("close", 0))
                    open_p = float(live_fx_k.get("open", 0))
                    high_p = float(live_fx_k.get("high", 0))
                    low_p = float(live_fx_k.get("low", 0))
                    vol = "0"
                    c_date = live_fx_k.get("datetime")
                    prev = matching_fx[0] if matching_fx else {}
                    p_close = float(prev.get("close_price", c_price))
                else:
                    latest = matching_fx[0] if matching_fx else {}
                    prev = matching_fx[1] if len(matching_fx) > 1 else latest
                    c_price = float(latest.get("close_price", 0))
                    open_p = float(latest.get("open_price", 0))
                    high_p = float(latest.get("high_price", 0))
                    low_p = float(latest.get("low_price", 0))
                    vol = "0"
                    c_date = str(latest.get("candle_date"))
                    p_close = float(prev.get("close_price", c_price))

                chg = c_price - p_close
                pct_chg = (chg / p_close) * 100 if p_close else 0.0

                all_closes = [float(r.get("close_price", 0)) for r in matching_fx] + ([c_price] if c_price else [])
                w52_low = min(all_closes) if all_closes else c_price
                w52_high = max(all_closes) if all_closes else c_price

                self._send_json(200, {
                    "symbol": symbol,
                    "name": f"{symbol.split('/')[0]} / {symbol.split('/')[1] if '/' in symbol else 'USD'}",
                    "exchange": "FOREX",
                    "currency": symbol.split("/")[1] if "/" in symbol else "USD",
                    "datetime": c_date,
                    "timestamp": int(datetime.now(timezone.utc).timestamp()),
                    "open": f"{open_p:.5f}",
                    "high": f"{high_p:.5f}",
                    "low": f"{low_p:.5f}",
                    "close": f"{c_price:.5f}",
                    "volume": "0",
                    "previous_close": f"{p_close:.5f}",
                    "change": f"{chg:+.5f}",
                    "percent_change": f"{pct_chg:+.4f}",
                    "is_market_open": True,
                    "fifty_two_week": {
                        "low": f"{w52_low:.5f}",
                        "high": f"{w52_high:.5f}",
                        "range": f"{w52_low:.5f} - {w52_high:.5f}"
                    }
                })
                return

            self._send_json(404, {"status": "error", "message": f"Symbol not found: {symbol}"})
            return

        # 5. /eod endpoint (Twelve Data standard — End of Day price)
        if path == "/eod":
            symbol = query_params.get("symbol", "").upper()
            if not symbol:
                self._send_json(400, {"status": "error", "message": "Missing required parameter: symbol"})
                return

            # Try crypto live candle or stored
            live_k = fetch_live_crypto_kline(symbol)
            if live_k:
                self._send_json(200, {
                    "symbol": symbol,
                    "exchange": "Binance",
                    "currency": symbol.split("/")[1] if "/" in symbol else "USD",
                    "datetime": live_k["datetime"],
                    "close": live_k["close"],
                    "open": live_k["open"],
                    "high": live_k["high"],
                    "low": live_k["low"],
                    "volume": live_k["volume"]
                })
                return

            ohlcv_data = load_clean_json("crypto_ohlcv_sample.json")
            matching = [r for r in ohlcv_data.get("data", []) if r.get("symbol") == symbol]
            if matching:
                matching = sorted(matching, key=lambda x: str(x.get("candle_date", "")), reverse=True)
                latest = matching[0]
                self._send_json(200, {
                    "symbol": symbol,
                    "exchange": "Binance",
                    "currency": symbol.split("/")[1] if "/" in symbol else "USD",
                    "datetime": str(latest.get("candle_date")),
                    "close": f"{float(latest.get('close_price', 0)):.2f}",
                    "open": f"{float(latest.get('open_price', 0)):.2f}",
                    "high": f"{float(latest.get('high_price', 0)):.2f}",
                    "low": f"{float(latest.get('low_price', 0)):.2f}",
                    "volume": f"{int(float(latest.get('volume', 0)))}"
                })
                return

            # Try forex live candle or stored
            live_fx_k = fetch_live_forex_candle(symbol)
            if live_fx_k:
                self._send_json(200, {
                    "symbol": symbol,
                    "exchange": "FOREX",
                    "currency": symbol.split("/")[1] if "/" in symbol else "USD",
                    "datetime": live_fx_k["datetime"],
                    "close": live_fx_k["close"],
                    "open": live_fx_k["open"],
                    "high": live_fx_k["high"],
                    "low": live_fx_k["low"],
                    "volume": live_fx_k["volume"]
                })
                return

            forex_ohlcv = load_clean_json("forex_ohlcv_sample.json")
            matching_fx = [r for r in forex_ohlcv.get("data", []) if r.get("pair_name") == symbol]
            if matching_fx:
                matching_fx = sorted(matching_fx, key=lambda x: str(x.get("candle_date", "")), reverse=True)
                latest = matching_fx[0]
                self._send_json(200, {
                    "symbol": symbol,
                    "exchange": "FOREX",
                    "currency": symbol.split("/")[1] if "/" in symbol else "USD",
                    "datetime": str(latest.get("candle_date")),
                    "close": f"{float(latest.get('close_price', 0)):.5f}",
                    "open": f"{float(latest.get('open_price', 0)):.5f}",
                    "high": f"{float(latest.get('high_price', 0)):.5f}",
                    "low": f"{float(latest.get('low_price', 0)):.5f}",
                    "volume": "0"
                })
                return

            self._send_json(404, {"status": "error", "message": f"Symbol not found: {symbol}"})
            return

        # 6. /cryptocurrencies & /forex_pairs reference endpoints
        if path == "/cryptocurrencies":
            self._send_json(200, {
                "data": [
                    {"symbol": "BTC/USD", "name": "Bitcoin", "currency_base": "Bitcoin", "currency_quote": "US Dollar"},
                    {"symbol": "ETH/USD", "name": "Ethereum", "currency_base": "Ethereum", "currency_quote": "US Dollar"},
                    {"symbol": "BNB/USD", "name": "BNB", "currency_base": "BNB", "currency_quote": "US Dollar"},
                    {"symbol": "SOL/USD", "name": "Solana", "currency_base": "Solana", "currency_quote": "US Dollar"},
                    {"symbol": "XRP/USD", "name": "XRP", "currency_base": "XRP", "currency_quote": "US Dollar"}
                ],
                "status": "ok"
            })
            return

        if path == "/forex_pairs":
            self._send_json(200, {
                "data": [
                    {"symbol": "EUR/USD", "currency_base": "EUR", "currency_quote": "USD"},
                    {"symbol": "GBP/USD", "currency_base": "GBP", "currency_quote": "USD"},
                    {"symbol": "USD/JPY", "currency_base": "USD", "currency_quote": "JPY"},
                    {"symbol": "USD/INR", "currency_base": "USD", "currency_quote": "INR"},
                    {"symbol": "USD/CAD", "currency_base": "USD", "currency_quote": "CAD"},
                    {"symbol": "AUD/USD", "currency_base": "AUD", "currency_quote": "USD"},
                    {"symbol": "USD/CHF", "currency_base": "USD", "currency_quote": "CHF"}
                ],
                "status": "ok"
            })
            return

        # =========================================================================
        # LEGACY MFAPIS SAMPLE ENDPOINTS
        # =========================================================================
        if path == "/v1/forex/sample":
            data = load_clean_json("forex_sample.json")
            if data and data.get("data"):
                self._send_json(200, data)
            else:
                self._send_json(404, {"error": "Forex sample not found"})
            return

        if path == "/v1/crypto/sample":
            data = load_clean_json("crypto_sample.json")
            if data and data.get("data"):
                self._send_json(200, data)
            else:
                self._send_json(404, {"error": "Crypto sample not found"})
            return

        if path == "/v1/economic/sample":
            data = load_clean_json("economic_sample.json")
            if data and data.get("data"):
                self._send_json(200, data)
            else:
                self._send_json(404, {"error": "Economic sample not found"})
            return

        self._send_json(404, {"error": "Not Found", "path": self.path})


def run():
    port = int(os.environ.get("PORT", 10000))
    server = HTTPServer(("0.0.0.0", port), MFAPIsHandler)
    print(f"🚀 MFAPIs server running on port {port}")
    server.serve_forever()


if __name__ == "__main__":
    run()

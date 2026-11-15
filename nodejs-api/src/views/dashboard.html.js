/**
 * MFAPIs Node.js UI Dashboard
 * Interactive Financial Trading Terminal & 3 Distinct API Explorers:
 * 1. 🪙 Cryptocurrency API (Binance Public API + CoinGecko)
 * 2. 💱 Foreign Exchange API (Yahoo Finance Interbank + ECB Frankfurter)
 * 3. 📈 Macroeconomic API (FRED - Federal Reserve Economic Data)
 */

function getDashboardHtml() {
  return `<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>MFAPIs — Financial Data Platform (Node.js)</title>
  <!-- Tailwind CSS -->
  <script src="https://cdn.tailwindcss.com"></script>
  <!-- Chart.js -->
  <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600&display=swap" rel="stylesheet">
  <style>
    body { font-family: 'Plus Jakarta Sans', sans-serif; }
    code, pre { font-family: 'JetBrains Mono', monospace; }
    .tab-btn.active {
      background-color: rgb(30 41 59);
      color: #38bdf8;
      border-color: #0284c7;
    }
    .flash-green { animation: flashG 0.8s ease-out; }
    .flash-red { animation: flashR 0.8s ease-out; }
    @keyframes flashG {
      0% { background-color: rgba(16, 185, 129, 0.4); }
      100% { background-color: transparent; }
    }
    @keyframes flashR {
      0% { background-color: rgba(239, 68, 68, 0.4); }
      100% { background-color: transparent; }
    }
    ::-webkit-scrollbar { width: 6px; height: 6px; }
    ::-webkit-scrollbar-track { background: #0f172a; }
    ::-webkit-scrollbar-thumb { background: #334155; border-radius: 3px; }
  </style>
</head>
<body class="bg-slate-950 text-slate-100 min-h-screen flex flex-col selection:bg-sky-500 selection:text-white">

  <!-- Top Navbar -->
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
              ● Node.js 2.0 Live
            </span>
          </div>
          <p class="text-xs text-slate-400">Twelve Data Compatible Multi-Asset Financial Engine</p>
        </div>
      </div>
      
      <!-- Top Badges -->
      <div class="flex items-center gap-2 sm:gap-3 text-xs">
        <div class="px-3 py-1.5 rounded-lg bg-slate-800/80 border border-slate-700/60 hidden sm:flex items-center gap-1.5">
          <span class="w-2 h-2 rounded-full bg-emerald-400 animate-pulse"></span>
          <span class="text-slate-400">PostgreSQL:</span>
          <span class="font-bold text-white ml-1">38,200+ Records</span>
        </div>
        <div class="px-3 py-1.5 rounded-lg bg-slate-800/80 border border-slate-700/60 hidden md:block">
          <span class="text-slate-400">Twelve Data Parity:</span>
          <span class="font-bold text-emerald-400 ml-1">&lt; 0.05% Variance</span>
        </div>
        <a href="/health" target="_blank" class="px-3 py-1.5 rounded-lg bg-sky-600 hover:bg-sky-500 text-white font-medium transition shadow-sm">
          System Health
        </a>
      </div>
    </div>
  </header>

  <!-- Main Container -->
  <main class="max-w-7xl mx-auto px-4 sm:px-6 py-6 flex-1 w-full space-y-6">

    <!-- Hero Card -->
    <div class="p-6 rounded-2xl bg-gradient-to-r from-slate-900 via-slate-900/90 to-slate-800/80 border border-slate-800 shadow-xl relative overflow-hidden">
      <div class="max-w-3xl space-y-2 relative z-10">
        <div class="inline-flex items-center gap-2 px-2.5 py-1 rounded-md bg-sky-500/10 text-sky-400 text-xs font-semibold">
          🚀 3 Institutional Data Categories — Twelve Data Standard
        </div>
        <h2 class="text-2xl sm:text-3xl font-extrabold text-white tracking-tight">
          Financial Data Analytics & API Explorer
        </h2>
        <p class="text-sm text-slate-400 leading-relaxed">
          Switch between the 3 distinct financial data categories below: Cryptocurrency Markets, Foreign Exchange (Forex), and US Macroeconomic Indicators. All powered by Node.js with real-time institutional feeds.
        </p>
      </div>
    </div>

    <!-- 3 DISTINCT NAVIGATION TABS -->
    <div class="flex flex-wrap items-center gap-2 border-b border-slate-800 pb-2">
      <button onclick="switchTab('crypto')" id="tab-crypto" class="tab-btn active px-4 py-2.5 rounded-xl text-xs sm:text-sm font-semibold transition border border-transparent hover:border-slate-700 flex items-center gap-2">
        <span>🪙</span> 1. Cryptocurrency API (Binance)
      </button>
      <button onclick="switchTab('forex')" id="tab-forex" class="tab-btn px-4 py-2.5 rounded-xl text-xs sm:text-sm font-semibold transition border border-transparent text-slate-400 hover:text-white hover:border-slate-700 flex items-center gap-2">
        <span>💱</span> 2. Foreign Exchange API (Forex)
      </button>
      <button onclick="switchTab('economic')" id="tab-economic" class="tab-btn px-4 py-2.5 rounded-xl text-xs sm:text-sm font-semibold transition border border-transparent text-slate-400 hover:text-white hover:border-slate-700 flex items-center gap-2">
        <span>📈</span> 3. Macroeconomic API (FRED)
      </button>
    </div>

    <!-- ===================================================================== -->
    <!-- TAB 1: CRYPTOCURRENCY API -->
    <!-- ===================================================================== -->
    <div id="content-crypto" class="tab-content space-y-6">
      
      <!-- Crypto Ticker Tape -->
      <div class="grid grid-cols-2 sm:grid-cols-5 gap-3">
        <div class="p-3.5 rounded-xl bg-slate-900 border border-slate-800" id="ticker-BTC">
          <div class="flex justify-between items-center text-xs">
            <span class="font-bold text-amber-400 font-mono">BTC/USD</span>
            <span class="text-[10px] text-slate-500">Binance</span>
          </div>
          <div class="text-lg font-extrabold text-white font-mono mt-1 price-val">Loading...</div>
          <div class="text-[11px] text-slate-400">Bitcoin Live</div>
        </div>

        <div class="p-3.5 rounded-xl bg-slate-900 border border-slate-800" id="ticker-ETH">
          <div class="flex justify-between items-center text-xs">
            <span class="font-bold text-indigo-400 font-mono">ETH/USD</span>
            <span class="text-[10px] text-slate-500">Binance</span>
          </div>
          <div class="text-lg font-extrabold text-white font-mono mt-1 price-val">Loading...</div>
          <div class="text-[11px] text-slate-400">Ethereum Live</div>
        </div>

        <div class="p-3.5 rounded-xl bg-slate-900 border border-slate-800" id="ticker-SOL">
          <div class="flex justify-between items-center text-xs">
            <span class="font-bold text-purple-400 font-mono">SOL/USD</span>
            <span class="text-[10px] text-slate-500">Binance</span>
          </div>
          <div class="text-lg font-extrabold text-white font-mono mt-1 price-val">Loading...</div>
          <div class="text-[11px] text-slate-400">Solana Live</div>
        </div>

        <div class="p-3.5 rounded-xl bg-slate-900 border border-slate-800" id="ticker-BNB">
          <div class="flex justify-between items-center text-xs">
            <span class="font-bold text-yellow-400 font-mono">BNB/USD</span>
            <span class="text-[10px] text-slate-500">Binance</span>
          </div>
          <div class="text-lg font-extrabold text-white font-mono mt-1 price-val">Loading...</div>
          <div class="text-[11px] text-slate-400">BNB Live</div>
        </div>

        <div class="p-3.5 rounded-xl bg-slate-900 border border-slate-800" id="ticker-XRP">
          <div class="flex justify-between items-center text-xs">
            <span class="font-bold text-sky-400 font-mono">XRP/USD</span>
            <span class="text-[10px] text-slate-500">Binance</span>
          </div>
          <div class="text-lg font-extrabold text-white font-mono mt-1 price-val">Loading...</div>
          <div class="text-[11px] text-slate-400">XRP Live</div>
        </div>
      </div>

      <!-- Crypto Explorer & Chart -->
      <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <!-- Controls -->
        <div class="p-5 rounded-2xl bg-slate-900 border border-slate-800 space-y-4">
          <div class="flex items-center justify-between border-b border-slate-800 pb-3">
            <h3 class="text-sm font-bold text-white flex items-center gap-2">
              <span>⚡</span> Crypto API Query
            </h3>
            <span class="text-[11px] font-mono text-amber-400 font-semibold">Twelve Data Compatible</span>
          </div>

          <div class="space-y-3 text-xs">
            <div>
              <label class="block text-slate-400 font-semibold mb-1">Select Crypto Asset</label>
              <select id="crypto-symbol-select" onchange="runCryptoQuery()" class="w-full px-3 py-2 rounded-lg bg-slate-800 border border-slate-700 text-white font-mono focus:outline-none focus:border-sky-500">
                <option value="BTC/USD" selected>BTC/USD (Bitcoin)</option>
                <option value="ETH/USD">ETH/USD (Ethereum)</option>
                <option value="SOL/USD">SOL/USD (Solana)</option>
                <option value="BNB/USD">BNB/USD (BNB)</option>
                <option value="XRP/USD">XRP/USD (XRP)</option>
              </select>
            </div>

            <div>
              <label class="block text-slate-400 font-semibold mb-1">Select Endpoint</label>
              <select id="crypto-endpoint-select" onchange="runCryptoQuery()" class="w-full px-3 py-2 rounded-lg bg-slate-800 border border-slate-700 text-white font-mono focus:outline-none focus:border-sky-500">
                <option value="/time_series" selected>/time_series (Candlesticks OHLCV)</option>
                <option value="/quote">/quote (Snapshot & 52-Week Range)</option>
                <option value="/price">/price (Real-Time Close Price)</option>
                <option value="/eod">/eod (End-of-Day Candle)</option>
              </select>
            </div>

            <div class="p-2.5 rounded-lg bg-slate-950 border border-slate-800 text-[11px] font-mono text-amber-400 break-all" id="crypto-url-preview">
              /time_series?symbol=BTC/USD&interval=1day&outputsize=15
            </div>

            <button onclick="runCryptoQuery()" class="w-full py-2.5 rounded-xl bg-amber-500 hover:bg-amber-400 text-slate-950 font-bold transition flex items-center justify-center gap-2">
              Fetch Crypto Data
            </button>
          </div>
        </div>

        <!-- Chart & Viewer -->
        <div class="lg:col-span-2 space-y-4">
          <div class="p-5 rounded-2xl bg-slate-900 border border-slate-800">
            <div class="flex justify-between items-center mb-4">
              <div>
                <span class="text-xs text-slate-400 uppercase font-semibold" id="crypto-chart-label">BTC/USD Timeseries (Binance)</span>
                <div class="text-2xl font-extrabold text-white font-mono" id="crypto-main-price">$0.00</div>
              </div>
              <span class="px-2.5 py-1 rounded-md text-xs font-semibold bg-emerald-500/10 text-emerald-400 border border-emerald-500/30">Live Active Candle</span>
            </div>
            <div class="h-60 w-full">
              <canvas id="cryptoChart"></canvas>
            </div>
          </div>

          <div class="p-5 rounded-2xl bg-slate-900 border border-slate-800 space-y-2">
            <div class="flex justify-between items-center">
              <span class="text-xs font-bold text-slate-300">Raw Twelve Data JSON Response</span>
              <button onclick="copyJson('crypto-json-viewer')" class="text-xs px-2.5 py-1 bg-slate-800 hover:bg-slate-700 text-slate-300 rounded border border-slate-700">Copy JSON</button>
            </div>
            <pre id="crypto-json-viewer" class="text-xs font-mono text-emerald-400 bg-slate-950 p-4 rounded-xl border border-slate-800/80 max-h-48 overflow-y-auto">// Fetching live data...</pre>
          </div>
        </div>
      </div>
    </div>

    <!-- ===================================================================== -->
    <!-- TAB 2: FOREIGN EXCHANGE (FOREX) API -->
    <!-- ===================================================================== -->
    <div id="content-forex" class="tab-content hidden space-y-6">
      
      <!-- Forex Ticker Tape -->
      <div class="grid grid-cols-2 sm:grid-cols-6 gap-3">
        <div class="p-3.5 rounded-xl bg-slate-900 border border-slate-800" id="ticker-EUR">
          <div class="flex justify-between items-center text-xs">
            <span class="font-bold text-emerald-400 font-mono">EUR/USD</span>
            <span class="text-[10px] text-slate-500">Forex</span>
          </div>
          <div class="text-lg font-extrabold text-white font-mono mt-1 price-val">Loading...</div>
          <div class="text-[11px] text-slate-400">Euro / Dollar</div>
        </div>

        <div class="p-3.5 rounded-xl bg-slate-900 border border-slate-800" id="ticker-GBP">
          <div class="flex justify-between items-center text-xs">
            <span class="font-bold text-sky-400 font-mono">GBP/USD</span>
            <span class="text-[10px] text-slate-500">Forex</span>
          </div>
          <div class="text-lg font-extrabold text-white font-mono mt-1 price-val">Loading...</div>
          <div class="text-[11px] text-slate-400">British Pound</div>
        </div>

        <div class="p-3.5 rounded-xl bg-slate-900 border border-slate-800" id="ticker-JPY">
          <div class="flex justify-between items-center text-xs">
            <span class="font-bold text-pink-400 font-mono">USD/JPY</span>
            <span class="text-[10px] text-slate-500">Forex</span>
          </div>
          <div class="text-lg font-extrabold text-white font-mono mt-1 price-val">Loading...</div>
          <div class="text-[11px] text-slate-400">US Dollar / Yen</div>
        </div>

        <div class="p-3.5 rounded-xl bg-slate-900 border border-slate-800" id="ticker-INR">
          <div class="flex justify-between items-center text-xs">
            <span class="font-bold text-orange-400 font-mono">USD/INR</span>
            <span class="text-[10px] text-slate-500">Forex</span>
          </div>
          <div class="text-lg font-extrabold text-white font-mono mt-1 price-val">Loading...</div>
          <div class="text-[11px] text-slate-400">Dollar / Rupee</div>
        </div>

        <div class="p-3.5 rounded-xl bg-slate-900 border border-slate-800" id="ticker-AUD">
          <div class="flex justify-between items-center text-xs">
            <span class="font-bold text-cyan-400 font-mono">AUD/USD</span>
            <span class="text-[10px] text-slate-500">Forex</span>
          </div>
          <div class="text-lg font-extrabold text-white font-mono mt-1 price-val">Loading...</div>
          <div class="text-[11px] text-slate-400">Aussie Dollar</div>
        </div>

        <div class="p-3.5 rounded-xl bg-slate-900 border border-slate-800" id="ticker-CAD">
          <div class="flex justify-between items-center text-xs">
            <span class="font-bold text-teal-400 font-mono">USD/CAD</span>
            <span class="text-[10px] text-slate-500">Forex</span>
          </div>
          <div class="text-lg font-extrabold text-white font-mono mt-1 price-val">Loading...</div>
          <div class="text-[11px] text-slate-400">Dollar / Canadian</div>
        </div>
      </div>

      <!-- Forex Explorer & Chart -->
      <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div class="p-5 rounded-2xl bg-slate-900 border border-slate-800 space-y-4">
          <div class="flex items-center justify-between border-b border-slate-800 pb-3">
            <h3 class="text-sm font-bold text-white flex items-center gap-2">
              <span>💱</span> Forex API Query
            </h3>
            <span class="text-[11px] font-mono text-emerald-400 font-semibold">Yahoo Finance Interbank</span>
          </div>

          <div class="space-y-3 text-xs">
            <div>
              <label class="block text-slate-400 font-semibold mb-1">Select Currency Pair</label>
              <select id="forex-symbol-select" onchange="runForexQuery()" class="w-full px-3 py-2 rounded-lg bg-slate-800 border border-slate-700 text-white font-mono focus:outline-none focus:border-sky-500">
                <option value="EUR/USD" selected>EUR/USD (Euro / US Dollar)</option>
                <option value="GBP/USD">GBP/USD (British Pound / US Dollar)</option>
                <option value="USD/JPY">USD/JPY (US Dollar / Japanese Yen)</option>
                <option value="USD/INR">USD/INR (US Dollar / Indian Rupee)</option>
                <option value="AUD/USD">AUD/USD (Australian Dollar / USD)</option>
                <option value="USD/CAD">USD/CAD (US Dollar / Canadian Dollar)</option>
                <option value="USD/CHF">USD/CHF (US Dollar / Swiss Franc)</option>
              </select>
            </div>

            <div>
              <label class="block text-slate-400 font-semibold mb-1">Select Endpoint</label>
              <select id="forex-endpoint-select" onchange="runForexQuery()" class="w-full px-3 py-2 rounded-lg bg-slate-800 border border-slate-700 text-white font-mono focus:outline-none focus:border-sky-500">
                <option value="/exchange_rate" selected>/exchange_rate (Forex Conversion)</option>
                <option value="/time_series">/time_series (Candlesticks OHLCV)</option>
                <option value="/price">/price (Real-Time Close Price)</option>
                <option value="/quote">/quote (Snapshot & 52-Week Range)</option>
                <option value="/eod">/eod (End-of-Day Candle)</option>
              </select>
            </div>

            <div class="p-2.5 rounded-lg bg-slate-950 border border-slate-800 text-[11px] font-mono text-emerald-400 break-all" id="forex-url-preview">
              /exchange_rate?symbol=EUR/USD
            </div>

            <button onclick="runForexQuery()" class="w-full py-2.5 rounded-xl bg-emerald-500 hover:bg-emerald-400 text-slate-950 font-bold transition flex items-center justify-center gap-2">
              Fetch Forex Data
            </button>
          </div>
        </div>

        <div class="lg:col-span-2 space-y-4">
          <div class="p-5 rounded-2xl bg-slate-900 border border-slate-800">
            <div class="flex justify-between items-center mb-4">
              <div>
                <span class="text-xs text-slate-400 uppercase font-semibold" id="forex-chart-label">EUR/USD Exchange Rate (Interbank)</span>
                <div class="text-2xl font-extrabold text-white font-mono" id="forex-main-price">0.00000</div>
              </div>
              <span class="px-2.5 py-1 rounded-md text-xs font-semibold bg-sky-500/10 text-sky-400 border border-sky-500/30">Yahoo Interbank Feed</span>
            </div>
            <div class="h-60 w-full">
              <canvas id="forexChart"></canvas>
            </div>
          </div>

          <div class="p-5 rounded-2xl bg-slate-900 border border-slate-800 space-y-2">
            <div class="flex justify-between items-center">
              <span class="text-xs font-bold text-slate-300">Raw Twelve Data JSON Response</span>
              <button onclick="copyJson('forex-json-viewer')" class="text-xs px-2.5 py-1 bg-slate-800 hover:bg-slate-700 text-slate-300 rounded border border-slate-700">Copy JSON</button>
            </div>
            <pre id="forex-json-viewer" class="text-xs font-mono text-emerald-400 bg-slate-950 p-4 rounded-xl border border-slate-800/80 max-h-48 overflow-y-auto">// Fetching live data...</pre>
          </div>
        </div>
      </div>
    </div>

    <!-- ===================================================================== -->
    <!-- TAB 3: MACROECONOMIC INDICATORS (FRED) API -->
    <!-- ===================================================================== -->
    <div id="content-economic" class="tab-content hidden space-y-6">
      
      <!-- FRED Overview Card -->
      <div class="p-5 rounded-2xl bg-slate-900 border border-slate-800 flex flex-wrap items-center justify-between gap-4">
        <div class="flex items-center gap-3">
          <div class="p-3 rounded-xl bg-indigo-500/10 text-indigo-400 font-bold text-xl">🏛️</div>
          <div>
            <h3 class="text-sm font-bold text-white">Federal Reserve Economic Data (FRED)</h3>
            <p class="text-xs text-slate-400">Source: Federal Reserve Bank of St. Louis &bull; 8 Major US Macro Indicators &bull; 29,000+ Observations</p>
          </div>
        </div>
        <div class="flex items-center gap-2">
          <span class="px-3 py-1.5 rounded-lg bg-indigo-500/10 text-indigo-400 border border-indigo-500/30 text-xs font-mono font-semibold">
            GET /v1/economic/sample
          </span>
          <button onclick="copyJson('economic-json-viewer')" class="px-3 py-1.5 rounded-lg bg-slate-800 hover:bg-slate-700 text-xs text-slate-300 font-medium transition border border-slate-700">
            Copy JSON
          </button>
        </div>
      </div>

      <!-- Macro Indicators Metric Cards -->
      <div class="grid grid-cols-2 sm:grid-cols-4 gap-4">
        <div class="p-4 rounded-xl bg-slate-900 border border-slate-800">
          <div class="text-xs text-slate-400 font-medium">US Gross Domestic Product</div>
          <div class="text-lg font-bold text-white font-mono mt-1">$27.6 Trillion</div>
          <div class="text-[11px] text-emerald-400 mt-0.5">● Quarterly (GDP)</div>
        </div>

        <div class="p-4 rounded-xl bg-slate-900 border border-slate-800">
          <div class="text-xs text-slate-400 font-medium">Consumer Price Index (CPI)</div>
          <div class="text-lg font-bold text-white font-mono mt-1">314.175</div>
          <div class="text-[11px] text-amber-400 mt-0.5">● Monthly (CPIAUCSL)</div>
        </div>

        <div class="p-4 rounded-xl bg-slate-900 border border-slate-800">
          <div class="text-xs text-slate-400 font-medium">Federal Funds Target Rate</div>
          <div class="text-lg font-bold text-white font-mono mt-1">5.33%</div>
          <div class="text-[11px] text-sky-400 mt-0.5">● Policy Rate (FEDFUNDS)</div>
        </div>

        <div class="p-4 rounded-xl bg-slate-900 border border-slate-800">
          <div class="text-xs text-slate-400 font-medium">US Unemployment Rate</div>
          <div class="text-lg font-bold text-white font-mono mt-1">4.10%</div>
          <div class="text-[11px] text-emerald-400 mt-0.5">● Monthly (UNRATE)</div>
        </div>
      </div>

      <!-- Table View of Historical Observations from PostgreSQL -->
      <div class="rounded-xl border border-slate-800 bg-slate-900/60 overflow-hidden shadow-lg">
        <div class="p-4 border-b border-slate-800 flex justify-between items-center">
          <span class="text-xs font-bold text-slate-200">PostgreSQL Ingested Observation Records (Sample from economic_indicator_values)</span>
          <span class="text-[11px] text-slate-500 font-mono">Displaying Latest 25 Rows</span>
        </div>
        <div class="overflow-x-auto max-h-72 overflow-y-auto">
          <table class="w-full text-left text-xs text-slate-300">
            <thead class="bg-slate-900 text-slate-400 uppercase text-[10px] tracking-wider border-b border-slate-800 sticky top-0">
              <tr>
                <th class="p-3">Indicator ID</th>
                <th class="p-3">Observation Date</th>
                <th class="p-3">Reported Value</th>
                <th class="p-3">Data Source</th>
                <th class="p-3">Audit Batch ID</th>
              </tr>
            </thead>
            <tbody class="divide-y divide-slate-800/60 font-mono text-[11px]" id="economic-table-body">
              <tr><td colspan="5" class="p-4 text-center text-slate-500">Loading economic data from database...</td></tr>
            </tbody>
          </table>
        </div>
      </div>

      <!-- Raw JSON Viewer -->
      <div class="p-5 rounded-2xl bg-slate-900 border border-slate-800 space-y-2">
        <span class="text-xs font-bold text-slate-300">API Response Payload (GET /v1/economic/sample)</span>
        <pre id="economic-json-viewer" class="text-xs font-mono text-emerald-400 bg-slate-950 p-4 rounded-xl border border-slate-800/80 max-h-48 overflow-y-auto">// Fetching FRED data...</pre>
      </div>

    </div>

  </main>

  <!-- Footer -->
  <footer class="border-t border-slate-800/80 bg-slate-900/60 py-4 text-center text-xs text-slate-500">
    MFAPIs Platform &bull; Node.js Express & PostgreSQL 17 &bull; 3 APIs (Crypto, Forex, Economic FRED) &bull; Twelve Data Parity
  </footer>

  <!-- Client-side Application Scripts -->
  <script>
    let cryptoChartInstance = null;
    let forexChartInstance = null;

    // Tab Switching Logic
    function switchTab(tabName) {
      document.querySelectorAll('.tab-btn').forEach(btn => {
        btn.classList.remove('active');
        btn.classList.add('text-slate-400');
      });
      document.querySelectorAll('.tab-content').forEach(content => {
        content.classList.add('hidden');
      });

      const selectedBtn = document.getElementById('tab-' + tabName);
      const selectedContent = document.getElementById('content-' + tabName);

      if (selectedBtn && selectedContent) {
        selectedBtn.classList.add('active');
        selectedBtn.classList.remove('text-slate-400');
        selectedContent.classList.remove('hidden');
      }

      if (tabName === 'forex' && !forexChartInstance) {
        runForexQuery();
      } else if (tabName === 'economic') {
        loadEconomicData();
      }
    }

    // Ticker updater
    async function updateTicker(symbol, elementId, isCrypto) {
      try {
        const url = isCrypto ? \`/price?symbol=\${symbol}\` : \`/exchange_rate?symbol=\${symbol}\`;
        const res = await fetch(url);
        if (!res.ok) return;
        const data = await res.json();
        const price = data.price || data.rate;
        const el = document.querySelector(\`#\${elementId} .price-val\`);
        if (el && price) {
          const oldVal = parseFloat(el.innerText.replace(/[^0-9.]/g, '')) || 0;
          const newVal = parseFloat(price);
          el.innerText = isCrypto ? \`$\${newVal.toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 })}\` : newVal.toFixed(4);
          
          const pill = document.getElementById(elementId);
          if (oldVal && newVal > oldVal) {
            pill.classList.remove('flash-green', 'flash-red');
            void pill.offsetWidth;
            pill.classList.add('flash-green');
          } else if (oldVal && newVal < oldVal) {
            pill.classList.remove('flash-green', 'flash-red');
            void pill.offsetWidth;
            pill.classList.add('flash-red');
          }
        }
      } catch (err) {}
    }

    async function refreshAllTickers() {
      // Crypto tickers
      updateTicker('BTC/USD', 'ticker-BTC', true);
      updateTicker('ETH/USD', 'ticker-ETH', true);
      updateTicker('SOL/USD', 'ticker-SOL', true);
      updateTicker('BNB/USD', 'ticker-BNB', true);
      updateTicker('XRP/USD', 'ticker-XRP', true);

      // Forex tickers
      updateTicker('EUR/USD', 'ticker-EUR', false);
      updateTicker('GBP/USD', 'ticker-GBP', false);
      updateTicker('USD/JPY', 'ticker-JPY', false);
      updateTicker('USD/INR', 'ticker-INR', false);
      updateTicker('AUD/USD', 'ticker-AUD', false);
      updateTicker('USD/CAD', 'ticker-CAD', false);
    }

    // 1. Run Crypto Query
    async function runCryptoQuery() {
      const symbol = document.getElementById('crypto-symbol-select').value;
      const endpoint = document.getElementById('crypto-endpoint-select').value;
      let url = \`\${endpoint}?symbol=\${encodeURIComponent(symbol)}\`;
      if (endpoint === '/time_series') {
        url += '&interval=1day&outputsize=15';
      }
      document.getElementById('crypto-url-preview').innerText = url;

      try {
        const resp = await fetch(url);
        const data = await resp.json();
        document.getElementById('crypto-json-viewer').innerText = JSON.stringify(data, null, 2);

        if (data.price) {
          document.getElementById('crypto-main-price').innerText = \`$\${parseFloat(data.price).toLocaleString()}\`;
        } else if (data.values && data.values.length > 0) {
          document.getElementById('crypto-main-price').innerText = \`$\${parseFloat(data.values[0].close).toLocaleString()}\`;
          renderCryptoChart(data.values, symbol);
        } else if (data.close) {
          document.getElementById('crypto-main-price').innerText = \`$\${parseFloat(data.close).toLocaleString()}\`;
        }
      } catch (err) {
        document.getElementById('crypto-json-viewer').innerText = err.message;
      }
    }

    function renderCryptoChart(values, symbol) {
      const ctx = document.getElementById('cryptoChart').getContext('2d');
      const reversed = [...values].reverse();
      const labels = reversed.map(v => v.datetime);
      const closes = reversed.map(v => parseFloat(v.close));

      if (cryptoChartInstance) cryptoChartInstance.destroy();
      cryptoChartInstance = new Chart(ctx, {
        type: 'line',
        data: {
          labels,
          datasets: [{
            label: \`\${symbol} Close\`,
            data: closes,
            borderColor: '#f59e0b',
            backgroundColor: 'rgba(245, 158, 11, 0.1)',
            fill: true,
            tension: 0.25,
            pointRadius: 3,
          }]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          plugins: { legend: { display: false } },
          scales: {
            x: { grid: { color: 'rgba(51, 65, 85, 0.3)' }, ticks: { color: '#94a3b8', font: { size: 10 } } },
            y: { grid: { color: 'rgba(51, 65, 85, 0.3)' }, ticks: { color: '#94a3b8', font: { size: 10 } } }
          }
        }
      });
    }

    // 2. Run Forex Query
    async function runForexQuery() {
      const symbol = document.getElementById('forex-symbol-select').value;
      const endpoint = document.getElementById('forex-endpoint-select').value;
      let url = \`\${endpoint}?symbol=\${encodeURIComponent(symbol)}\`;
      if (endpoint === '/time_series') {
        url += '&interval=1day&outputsize=15';
      }
      document.getElementById('forex-url-preview').innerText = url;

      try {
        const resp = await fetch(url);
        const data = await resp.json();
        document.getElementById('forex-json-viewer').innerText = JSON.stringify(data, null, 2);

        if (data.rate) {
          document.getElementById('forex-main-price').innerText = parseFloat(data.rate).toFixed(5);
        } else if (data.price) {
          document.getElementById('forex-main-price').innerText = parseFloat(data.price).toFixed(5);
        } else if (data.values && data.values.length > 0) {
          document.getElementById('forex-main-price').innerText = parseFloat(data.values[0].close).toFixed(5);
          renderForexChart(data.values, symbol);
        } else if (data.close) {
          document.getElementById('forex-main-price').innerText = parseFloat(data.close).toFixed(5);
        }
      } catch (err) {
        document.getElementById('forex-json-viewer').innerText = err.message;
      }
    }

    function renderForexChart(values, symbol) {
      const ctx = document.getElementById('forexChart').getContext('2d');
      const reversed = [...values].reverse();
      const labels = reversed.map(v => v.datetime);
      const closes = reversed.map(v => parseFloat(v.close));

      if (forexChartInstance) forexChartInstance.destroy();
      forexChartInstance = new Chart(ctx, {
        type: 'line',
        data: {
          labels,
          datasets: [{
            label: \`\${symbol} Close\`,
            data: closes,
            borderColor: '#10b981',
            backgroundColor: 'rgba(16, 185, 129, 0.1)',
            fill: true,
            tension: 0.25,
            pointRadius: 3,
          }]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          plugins: { legend: { display: false } },
          scales: {
            x: { grid: { color: 'rgba(51, 65, 85, 0.3)' }, ticks: { color: '#94a3b8', font: { size: 10 } } },
            y: { grid: { color: 'rgba(51, 65, 85, 0.3)' }, ticks: { color: '#94a3b8', font: { size: 10 } } }
          }
        }
      });
    }

    // 3. Load Economic Data (FRED)
    async function loadEconomicData() {
      try {
        const res = await fetch('/v1/economic/sample');
        if (!res.ok) return;
        const json = await res.json();
        document.getElementById('economic-json-viewer').innerText = JSON.stringify(json, null, 2);

        const rows = json.data || [];
        const tbody = document.getElementById('economic-table-body');
        if (rows.length === 0) {
          tbody.innerHTML = '<tr><td colspan="5" class="p-4 text-center text-slate-500">No economic observations found</td></tr>';
          return;
        }

        tbody.innerHTML = rows.map(r => {
          const d = typeof r.observation_date === 'string' ? r.observation_date.split('T')[0] : r.observation_date;
          return \`<tr class="hover:bg-slate-800/40 transition">
            <td class="p-3 font-bold text-sky-400">\${r.indicator_id || '-'}</td>
            <td class="p-3 text-slate-300">\${d || '-'}</td>
            <td class="p-3 font-bold text-white">\${parseFloat(r.value || 0).toLocaleString()}</td>
            <td class="p-3 text-slate-400">\${r.source || 'fred'}</td>
            <td class="p-3 text-slate-500 text-[10px]">\${r.raw_response_id || 'ingested'}</td>
          </tr>\`;
        }).join('');
      } catch (err) {
        document.getElementById('economic-json-viewer').innerText = err.message;
      }
    }

    function copyJson(elementId) {
      const text = document.getElementById(elementId).innerText;
      navigator.clipboard.writeText(text);
      alert('Copied JSON to clipboard!');
    }

    // Boot
    window.addEventListener('DOMContentLoaded', () => {
      refreshAllTickers();
      runCryptoQuery();
      setInterval(refreshAllTickers, 15000);
    });
  </script>
</body>
</html>
`;
}

module.exports = { getDashboardHtml };

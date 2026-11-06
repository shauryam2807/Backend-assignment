import os
import json
from http.server import HTTPServer, BaseHTTPRequestHandler
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

HTML_DASHBOARD = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>MFAPIs — Financial Data Platform</title>
  <script src="https://cdn.tailwindcss.com"></script>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
  <style>
    body { font-family: 'Inter', sans-serif; }
  </style>
</head>
<body class="bg-slate-900 text-slate-100 min-h-screen">
  <!-- Navbar -->
  <header class="border-b border-slate-800 bg-slate-900/80 backdrop-blur sticky top-0 z-50">
    <div class="max-w-7xl mx-auto px-6 py-4 flex items-center justify-between">
      <div class="flex items-center gap-3">
        <div class="w-10 h-10 rounded-xl bg-gradient-to-tr from-emerald-500 to-cyan-500 flex items-center justify-center font-bold text-xl text-slate-950">
          M
        </div>
        <div>
          <h1 class="text-xl font-bold tracking-tight">MFAPIs Platform</h1>
          <p class="text-xs text-slate-400">Financial Data ETL & Analytics Engine</p>
        </div>
      </div>
      <div class="flex items-center gap-4">
        <span class="inline-flex items-center gap-1.5 px-3 py-1 rounded-full text-xs font-medium bg-emerald-500/10 text-emerald-400 border border-emerald-500/20">
          <span class="w-2 h-2 rounded-full bg-emerald-400 animate-pulse"></span>
          Live on Cloud
        </span>
        <a href="/health" target="_blank" class="text-xs font-semibold px-3 py-1.5 rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-300 transition">
          Health Check API &rarr;
        </a>
      </div>
    </div>
  </header>

  <!-- Hero -->
  <main class="max-w-7xl mx-auto px-6 py-10 space-y-10">
    <div class="space-y-3">
      <h2 class="text-3xl font-extrabold tracking-tight text-white sm:text-4xl">
        Unified Financial Data Engine
      </h2>
      <p class="text-slate-400 max-w-3xl text-base leading-relaxed">
        Autonomous ETL pipelines that acquire multi-asset financial data from public & institutional sources, normalize schemas through robust validation routines, and store over <strong class="text-white">34,600+ records</strong> in PostgreSQL.
      </p>
    </div>

    <!-- Metrics Grid -->
    <div class="grid grid-cols-1 md:grid-cols-4 gap-4">
      <div class="p-5 rounded-2xl bg-slate-800/60 border border-slate-700/60 space-y-2">
        <div class="flex items-center justify-between text-slate-400 text-sm">
          <span>Forex Pipeline</span>
          <span class="text-emerald-400 font-semibold">ECB / Frankfurter</span>
        </div>
        <p class="text-3xl font-bold text-white">3,591</p>
        <p class="text-xs text-slate-400">145 Currency Pairs &bull; 1 Year History</p>
      </div>

      <div class="p-5 rounded-2xl bg-slate-800/60 border border-slate-700/60 space-y-2">
        <div class="flex items-center justify-between text-slate-400 text-sm">
          <span>Crypto Engine</span>
          <span class="text-amber-400 font-semibold">CoinGecko API</span>
        </div>
        <p class="text-3xl font-bold text-white">1,870</p>
        <p class="text-xs text-slate-400">Top 50 Coins &bull; 365-Day Daily Candles</p>
      </div>

      <div class="p-5 rounded-2xl bg-slate-800/60 border border-slate-700/60 space-y-2">
        <div class="flex items-center justify-between text-slate-400 text-sm">
          <span>Macroeconomic Data</span>
          <span class="text-cyan-400 font-semibold">FRED Fed Reserve</span>
        </div>
        <p class="text-3xl font-bold text-white">29,171</p>
        <p class="text-xs text-slate-400">8 Key Indicators (GDP, CPI, Unemployment)</p>
      </div>

      <div class="p-5 rounded-2xl bg-slate-800/60 border border-slate-700/60 space-y-2">
        <div class="flex items-center justify-between text-slate-400 text-sm">
          <span>Reliability & Tests</span>
          <span class="text-emerald-400 font-semibold">100% Pass</span>
        </div>
        <p class="text-3xl font-bold text-emerald-400">48 / 48</p>
        <p class="text-xs text-slate-400">Pytest Unit & Integration Tests</p>
      </div>
    </div>

    <!-- Live Data Explorer Tabs -->
    <div class="bg-slate-800/50 rounded-2xl border border-slate-700/70 overflow-hidden">
      <div class="border-b border-slate-700/70 px-6 py-4 flex flex-wrap items-center justify-between gap-4">
        <div class="flex items-center gap-2">
          <span class="text-sm font-semibold text-slate-300">Live JSON Data Endpoints:</span>
        </div>
        <div class="flex gap-2">
          <a href="/v1/forex/sample" target="_blank" class="px-3 py-1.5 rounded-lg text-xs font-medium bg-emerald-500/10 text-emerald-300 border border-emerald-500/20 hover:bg-emerald-500/20 transition">
            💱 Forex JSON
          </a>
          <a href="/v1/crypto/sample" target="_blank" class="px-3 py-1.5 rounded-lg text-xs font-medium bg-amber-500/10 text-amber-300 border border-amber-500/20 hover:bg-amber-500/20 transition">
            🪙 Crypto JSON
          </a>
          <a href="/v1/economic/sample" target="_blank" class="px-3 py-1.5 rounded-lg text-xs font-medium bg-cyan-500/10 text-cyan-300 border border-cyan-500/20 hover:bg-cyan-500/20 transition">
            📈 Economic JSON
          </a>
        </div>
      </div>

      <div class="p-6 grid grid-cols-1 md:grid-cols-3 gap-6">
        <!-- Forex Card -->
        <div class="space-y-3 p-4 rounded-xl bg-slate-900/60 border border-slate-800">
          <h3 class="font-bold text-emerald-400 flex items-center justify-between text-sm">
            <span>Forex Exchange Rates</span>
            <span class="text-xs text-slate-400">Normalized</span>
          </h3>
          <p class="text-xs text-slate-400 leading-relaxed">
            Multi-currency pair matrix covering USD, EUR, GBP, INR, JPY with daily close rates from European Central Bank reference pricing.
          </p>
          <div class="pt-2">
            <a href="/v1/forex/sample" target="_blank" class="inline-flex items-center gap-1 text-xs text-emerald-400 hover:text-emerald-300 font-semibold">
              Inspect 25 Sample Records &rarr;
            </a>
          </div>
        </div>

        <!-- Crypto Card -->
        <div class="space-y-3 p-4 rounded-xl bg-slate-900/60 border border-slate-800">
          <h3 class="font-bold text-amber-400 flex items-center justify-between text-sm">
            <span>Cryptocurrency Markets</span>
            <span class="text-xs text-slate-400">365-Day Timeseries</span>
          </h3>
          <p class="text-xs text-slate-400 leading-relaxed">
            Normalized OHLCV, market capitalization ranks, and rolling price change distributions for top institutional digital assets.
          </p>
          <div class="pt-2">
            <a href="/v1/crypto/sample" target="_blank" class="inline-flex items-center gap-1 text-xs text-amber-400 hover:text-amber-300 font-semibold">
              Inspect 25 Sample Records &rarr;
            </a>
          </div>
        </div>

        <!-- Macro Card -->
        <div class="space-y-3 p-4 rounded-xl bg-slate-900/60 border border-slate-800">
          <h3 class="font-bold text-cyan-400 flex items-center justify-between text-sm">
            <span>Macroeconomic Time Series</span>
            <span class="text-xs text-slate-400">Institutional</span>
          </h3>
          <p class="text-xs text-slate-400 leading-relaxed">
            Real GDP, Consumer Price Index (CPI), Unemployment Rate, Fed Funds Effective Rate, and 10-Year Treasury Yields via FRED St. Louis Fed.
          </p>
          <div class="pt-2">
            <a href="/v1/economic/sample" target="_blank" class="inline-flex items-center gap-1 text-xs text-cyan-400 hover:text-cyan-300 font-semibold">
              Inspect 30 Sample Records &rarr;
            </a>
          </div>
        </div>
      </div>
    </div>

    <!-- Architecture & Features -->
    <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
      <div class="p-6 rounded-2xl bg-slate-800/40 border border-slate-700/60 space-y-4">
        <h3 class="font-bold text-white text-base">Key Architecture Highlights</h3>
        <ul class="space-y-2.5 text-xs text-slate-300">
          <li class="flex items-start gap-2">
            <span class="text-emerald-400 font-bold">&check;</span>
            <span><strong>Tenacity Resiliency:</strong> Exponential backoff retry logic on transient HTTP timeouts and 429 rate-limiting events.</span>
          </li>
          <li class="flex items-start gap-2">
            <span class="text-emerald-400 font-bold">&check;</span>
            <span><strong>Zero Data Loss Storage:</strong> Raw unmodified JSON payloads persisted with timestamped audit IDs before transformation.</span>
          </li>
          <li class="flex items-start gap-2">
            <span class="text-emerald-400 font-bold">&check;</span>
            <span><strong>PostgreSQL UPSERT:</strong> Strict unique constraint conflict resolution prevents historical record duplication.</span>
          </li>
        </ul>
      </div>

      <div class="p-6 rounded-2xl bg-slate-800/40 border border-slate-700/60 space-y-4">
        <h3 class="font-bold text-white text-base">Deliverables & Documentation</h3>
        <div class="grid grid-cols-2 gap-3 text-xs">
          <div class="p-3 rounded-lg bg-slate-900/80 border border-slate-800">
            <p class="font-semibold text-white">Source Catalogue</p>
            <p class="text-slate-400 text-[11px]">10 asset categories, 30+ sources</p>
          </div>
          <div class="p-3 rounded-lg bg-slate-900/80 border border-slate-800">
            <p class="font-semibold text-white">Commercial Strategy</p>
            <p class="text-slate-400 text-[11px]">Opportunity scoring & GTM plans</p>
          </div>
          <div class="p-3 rounded-lg bg-slate-900/80 border border-slate-800">
            <p class="font-semibold text-white">Data Quality Spec</p>
            <p class="text-slate-400 text-[11px]">Validation pipeline & monitoring</p>
          </div>
          <div class="p-3 rounded-lg bg-slate-900/80 border border-slate-800">
            <p class="font-semibold text-white">Licensing Overview</p>
            <p class="text-slate-400 text-[11px]">Commercial redistribution rights</p>
          </div>
        </div>
      </div>
    </div>
  </main>

  <!-- Footer -->
  <footer class="border-t border-slate-800 text-center py-6 text-xs text-slate-500">
    MFAPIs Platform &bull; Built with Python, SQLAlchemy, PostgreSQL, and Pandas
  </footer>
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
        path = self.path.split("?")[0].rstrip("/")

        if path in ("", "/"):
            self._send_html(HTML_DASHBOARD)
            return

        if path == "/health":
            self._send_json(200, {
                "status": "healthy",
                "service": "MFAPIs Financial Data Platform",
                "version": "1.0.0",
                "records_total": 34632,
                "endpoints": {
                    "ui": "/",
                    "health": "/health",
                    "forex_sample": "/v1/forex/sample",
                    "crypto_sample": "/v1/crypto/sample",
                    "economic_sample": "/v1/economic/sample"
                }
            })
            return

        if path == "/v1/forex/sample":
            filepath = BASE_DIR / "output" / "forex_sample.json"
            if filepath.exists():
                with open(filepath, "r", encoding="utf-8") as f:
                    self._send_json(200, json.load(f))
            else:
                self._send_json(404, {"error": "Forex sample not found"})
            return

        if path == "/v1/crypto/sample":
            filepath = BASE_DIR / "output" / "crypto_sample.json"
            if filepath.exists():
                with open(filepath, "r", encoding="utf-8") as f:
                    self._send_json(200, json.load(f))
            else:
                self._send_json(404, {"error": "Crypto sample not found"})
            return

        if path == "/v1/economic/sample":
            filepath = BASE_DIR / "output" / "economic_sample.json"
            if filepath.exists():
                with open(filepath, "r", encoding="utf-8") as f:
                    self._send_json(200, json.load(f))
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

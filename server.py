import os
import json
from http.server import HTTPServer, BaseHTTPRequestHandler
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

class MFAPIsHandler(BaseHTTPRequestHandler):

    def _send_json(self, status_code: int, data: dict):
        self.send_response(status_code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(json.dumps(data, indent=2, default=str).encode("utf-8"))

    def do_GET(self):
        path = self.path.split("?")[0].rstrip("/")

        if path in ("", "/", "/health"):
            self._send_json(200, {
                "status": "healthy",
                "service": "MFAPIs Financial Data Platform",
                "version": "1.0.0",
                "endpoints": {
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


"""Local dev server for the frontend: `python serve.py` -> http://localhost:3000

Plain `python -m http.server 3000` also works; this one forces the right MIME types
for JavaScript modules on Windows and serves 404.html for unknown pages.
"""
import functools
import http.server
from pathlib import Path

ROOT = Path(__file__).parent
PORT = 3000


class Handler(http.server.SimpleHTTPRequestHandler):
    extensions_map = {**http.server.SimpleHTTPRequestHandler.extensions_map,
                      ".js": "text/javascript", ".css": "text/css", ".html": "text/html", ".svg": "image/svg+xml"}

    def send_error(self, code, message=None, explain=None):
        page = ROOT / "404.html"
        if code == 404 and page.exists():
            body = page.read_bytes()
            self.send_response(404)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)
        else:
            super().send_error(code, message, explain)


if __name__ == "__main__":
    server = http.server.ThreadingHTTPServer(("", PORT), functools.partial(Handler, directory=str(ROOT)))
    print(f"Frontend running at http://localhost:{PORT}  (API expected at http://localhost:8000/api)")
    server.serve_forever()

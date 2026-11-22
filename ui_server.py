"""Small standard-library web interface for the phishing detector.

The server binds to localhost, serves only bundled static files, and exposes three
JSON analysis endpoints. Submitted URLs are passed to the existing static parser;
they are never fetched, resolved, or executed.
"""

from __future__ import annotations

import argparse
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import json
from pathlib import Path
from typing import Any

from phishing_detector import MAX_EMAIL_BYTES, analyze_email_content, analyze_email_file, analyze_url


HOST = "127.0.0.1"
PORT = 8765
MAX_URL_CHARS = 4_096
MAX_JSON_OVERHEAD = 8_192
STATIC_ROOT = Path(__file__).with_name("web")
STATIC_FILES = {
    "/": ("index.html", "text/html; charset=utf-8"),
    "/index.html": ("index.html", "text/html; charset=utf-8"),
    "/styles.css": ("styles.css", "text/css; charset=utf-8"),
    "/app.js": ("app.js", "text/javascript; charset=utf-8"),
}


class ClientInputError(ValueError):
    """A validation problem that is safe to report to the browser."""


class RequestTooLarge(ClientInputError):
    """The request exceeded a documented prototype limit."""


class PhishingUIHandler(BaseHTTPRequestHandler):
    server_version = "PhishingDetectorUI/1.0"

    def _is_local_browser_request(self, *, require_origin: bool = False) -> bool:
        """Reject foreign Host/Origin headers on this localhost-only demo.

        Besides loopback binding, Host validation reduces DNS-rebinding risk.
        The browser interface is served from this same origin only.
        """
        port = self.server.server_port
        allowed_hosts = {f"127.0.0.1:{port}", f"localhost:{port}"}
        host = self.headers.get("Host", "").strip().lower()
        if host not in allowed_hosts:
            return False
        if require_origin:
            origin = self.headers.get("Origin")
            if origin and origin.lower() not in {f"http://{h}" for h in allowed_hosts}:
                return False
        return True

    def do_GET(self) -> None:
        if not self._is_local_browser_request():
            self._send_json(HTTPStatus.FORBIDDEN, {"error": "Local browser access only"})
            return
        asset = STATIC_FILES.get(self.path.split("?", 1)[0])
        if asset is None:
            self._send_json(HTTPStatus.NOT_FOUND, {"error": "Not found"})
            return
        filename, content_type = asset
        try:
            body = (STATIC_ROOT / filename).read_bytes()
        except OSError:
            self._send_json(HTTPStatus.INTERNAL_SERVER_ERROR, {"error": "UI asset unavailable"})
            return
        self.send_response(HTTPStatus.OK)
        self._security_headers()
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(body)

    def do_POST(self) -> None:
        if not self._is_local_browser_request(require_origin=True):
            self._send_json(HTTPStatus.FORBIDDEN, {"error": "Local browser access only"})
            return
        try:
            if self.path == "/api/analyze-url":
                result = self._analyze_url_request()
            elif self.path == "/api/analyze-email":
                result = self._analyze_email_request()
            elif self.path == "/api/analyze-email-file":
                result = self._analyze_email_file_request()
            else:
                self._send_json(HTTPStatus.NOT_FOUND, {"error": "Not found"})
                return
        except RequestTooLarge as exc:
            self._send_json(HTTPStatus.REQUEST_ENTITY_TOO_LARGE, {"error": str(exc)})
            return
        except (ClientInputError, ValueError) as exc:
            self._send_json(HTTPStatus.BAD_REQUEST, {"error": str(exc)})
            return
        self._send_json(HTTPStatus.OK, {"result": result})

    def _analyze_url_request(self) -> dict[str, Any]:
        payload = self._read_json(MAX_URL_CHARS + MAX_JSON_OVERHEAD)
        value = payload.get("url")
        if not isinstance(value, str):
            raise ClientInputError("URL must be text")
        if len(value) > MAX_URL_CHARS:
            raise RequestTooLarge(f"URL exceeds the {MAX_URL_CHARS:,}-character interface limit")
        return analyze_url(value)

    def _analyze_email_request(self) -> dict[str, Any]:
        payload = self._read_json(MAX_EMAIL_BYTES + MAX_JSON_OVERHEAD)
        value = payload.get("text")
        if not isinstance(value, str):
            raise ClientInputError("Email message must be text")
        if not value.strip():
            raise ClientInputError("Paste an email message or choose an .eml file")
        if len(value.encode("utf-8")) > MAX_EMAIL_BYTES:
            raise RequestTooLarge("Email exceeds the 2 MB prototype limit")
        return analyze_email_content(plain_text=value)

    def _analyze_email_file_request(self) -> dict[str, Any]:
        body = self._read_body(MAX_EMAIL_BYTES)
        if not body:
            raise ClientInputError("Choose a non-empty .eml file")
        return analyze_email_file(body)

    def _read_json(self, limit: int) -> dict[str, Any]:
        content_type = self.headers.get("Content-Type", "").split(";", 1)[0].strip().lower()
        if content_type != "application/json":
            raise ClientInputError("Content-Type must be application/json")
        raw = self._read_body(limit)
        try:
            payload = json.loads(raw.decode("utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError) as exc:
            raise ClientInputError("Request body must contain valid UTF-8 JSON") from exc
        if not isinstance(payload, dict):
            raise ClientInputError("JSON body must be an object")
        return payload

    def _read_body(self, limit: int) -> bytes:
        raw_length = self.headers.get("Content-Length")
        if raw_length is None:
            raise ClientInputError("Content-Length is required")
        try:
            length = int(raw_length)
        except ValueError as exc:
            raise ClientInputError("Invalid Content-Length") from exc
        if length < 0:
            raise ClientInputError("Invalid Content-Length")
        if length > limit:
            raise RequestTooLarge("Request exceeds the permitted input size")
        return self.rfile.read(length)

    def _send_json(self, status: HTTPStatus, payload: dict[str, Any]) -> None:
        body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self._security_headers()
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(body)

    def _security_headers(self) -> None:
        self.send_header("Content-Security-Policy", "default-src 'self'; script-src 'self'; style-src 'self'; img-src 'none'; connect-src 'self'; base-uri 'none'; form-action 'self'; frame-ancestors 'none'")
        self.send_header("X-Content-Type-Options", "nosniff")
        self.send_header("Referrer-Policy", "no-referrer")

    def log_message(self, format: str, *args: object) -> None:
        # Keep the demo quiet while still showing method, path, and status.
        print(f"{self.address_string()} - {format % args}")


def create_server(host: str = HOST, port: int = PORT) -> ThreadingHTTPServer:
    return ThreadingHTTPServer((host, port), PhishingUIHandler)


def main() -> None:
    parser = argparse.ArgumentParser(description="Run the local phishing detector web interface")
    parser.add_argument("--host", default=HOST, choices=[HOST], help="Local bind address (localhost only)")
    parser.add_argument("--port", type=int, default=PORT, help="Local TCP port")
    args = parser.parse_args()
    server = create_server(args.host, args.port)
    print(f"Phishing Detector UI: http://{args.host}:{server.server_port}")
    print("Press Ctrl+C to stop. Submitted links are analyzed as text and are never visited.")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nStopping server.")
    finally:
        server.server_close()


if __name__ == "__main__":
    main()

import json
from pathlib import Path
import threading
import unittest
from urllib.error import HTTPError
from urllib.request import Request, urlopen

from ui_server import create_server


PROJECT_ROOT = Path(__file__).parent


class UIServerIntegrationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.server = create_server(port=0)
        cls.thread = threading.Thread(target=cls.server.serve_forever, daemon=True)
        cls.thread.start()
        cls.base_url = f"http://127.0.0.1:{cls.server.server_port}"

    @classmethod
    def tearDownClass(cls):
        cls.server.shutdown()
        cls.server.server_close()
        cls.thread.join(timeout=2)

    def request(self, path, *, data=None, content_type=None, extra_headers=None):
        headers = dict(extra_headers or {})
        if content_type:
            headers["Content-Type"] = content_type
        request = Request(self.base_url + path, data=data, headers=headers)
        try:
            response = urlopen(request, timeout=2)
        except HTTPError as exc:
            with exc:
                return exc.code, json.loads(exc.read())
        with response:
            body = response.read()
            if response.headers.get_content_type() == "application/json":
                return response.status, json.loads(body)
            return response.status, body.decode("utf-8")

    def post_json(self, path, payload):
        return self.request(
            path,
            data=json.dumps(payload).encode("utf-8"),
            content_type="application/json",
        )

    def test_index_serves_single_page_interface(self):
        status, body = self.request("/")
        self.assertEqual(status, 200)
        self.assertIn("URL Scanner", body)
        self.assertIn("Email Scanner", body)

    def test_url_api_connects_to_detector(self):
        status, body = self.post_json("/api/analyze-url", {"url": "http://192.0.2.10/login"})
        self.assertEqual(status, 200)
        self.assertEqual(body["result"]["classification"], "HIGH RISK")
        self.assertEqual(body["result"]["score"], 4)

    def test_invalid_url_keeps_detector_classification(self):
        status, body = self.post_json("/api/analyze-url", {"url": "javascript:alert(1)"})
        self.assertEqual(status, 200)
        self.assertEqual(body["result"]["classification"], "INVALID INPUT")

    def test_pasted_email_api_returns_embedded_urls(self):
        text = "Urgent: enter your password at http://192.0.2.10/login"
        status, body = self.post_json("/api/analyze-email", {"text": text})
        self.assertEqual(status, 200)
        self.assertEqual(body["result"]["classification"], "HIGH RISK")
        self.assertEqual(body["result"]["urls_total"], 1)

    def test_eml_upload_api_uses_existing_file_parser(self):
        raw = (PROJECT_ROOT / "samples" / "suspicious_email.eml").read_bytes()
        status, body = self.request(
            "/api/analyze-email-file", data=raw, content_type="application/octet-stream"
        )
        self.assertEqual(status, 200)
        self.assertEqual(body["result"]["classification"], "HIGH RISK")
        self.assertEqual(body["result"]["subject"], "Urgent account verification required")

    def test_empty_email_returns_clear_validation_error(self):
        status, body = self.post_json("/api/analyze-email", {"text": "   "})
        self.assertEqual(status, 400)
        self.assertIn("Paste an email message", body["error"])

    def test_unknown_path_is_not_served(self):
        status, body = self.request("/../phishing_detector.py")
        self.assertEqual(status, 404)
        self.assertEqual(body["error"], "Not found")

    def test_rejects_nonlocal_host_header(self):
        status, body = self.request("/", extra_headers={"Host": "attacker.example"})
        self.assertEqual(status, 403)
        self.assertIn("Local browser access", body["error"])

    def test_rejects_foreign_origin_header(self):
        status, body = self.request(
            "/api/analyze-url",
            data=json.dumps({"url": "https://example.org"}).encode("utf-8"),
            content_type="application/json",
            extra_headers={"Origin": "http://attacker.example"},
        )
        self.assertEqual(status, 403)
        self.assertIn("Local browser access", body["error"])

    def test_frontend_uses_text_nodes_for_untrusted_results(self):
        script = (PROJECT_ROOT / "web" / "app.js").read_text(encoding="utf-8")
        self.assertIn("textContent", script)
        self.assertNotIn("innerHTML", script)


if __name__ == "__main__":
    unittest.main()

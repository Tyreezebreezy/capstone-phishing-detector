import unittest
from phishing_detector import analyze_url, analyze_email_content, analyze_email_file, classify


class PhishingDetectorTests(unittest.TestCase):
    def test_classification_boundaries(self):
        self.assertEqual([classify(x) for x in (0, 1, 2, 3, 4)],
                         ["NO INDICATORS FOUND", "REVIEW RECOMMENDED", "REVIEW RECOMMENDED", "HIGH RISK", "HIGH RISK"])

    def test_normal_https_url(self):
        self.assertEqual(analyze_url("https://example.org")["score"], 0)

    def test_http_weak_risk(self):
        self.assertEqual(analyze_url("http://example.org")["score"], 1)

    def test_ip_address_and_login(self):
        self.assertEqual(analyze_url("http://192.0.2.10/login")["classification"], "HIGH RISK")

    def test_user_info_obfuscation(self):
        self.assertEqual(analyze_url("https://trusted.example@other.example/")["score"], 2)

    def test_punycode(self):
        self.assertEqual(analyze_url("https://xn--e1afmkfd.example/")["score"], 1)

    def test_login_word_weak_indicator(self):
        self.assertEqual(analyze_url("https://example.org/login")["classification"], "REVIEW RECOMMENDED")

    def test_unsupported_scheme(self):
        self.assertEqual(analyze_url("javascript:alert(1)")["classification"], "INVALID INPUT")

    def test_whitespace_is_invalid(self):
        self.assertEqual(analyze_url("https://exa mple.org/")["classification"], "INVALID INPUT")

    def test_malformed_port(self):
        self.assertEqual(analyze_url("https://example.org:abc/")["classification"], "INVALID INPUT")

    def test_benign_pasted_email(self):
        self.assertEqual(analyze_email_content("The meeting is tomorrow at noon.")["score"], 0)

    def test_urgent_only(self):
        self.assertEqual(analyze_email_content("Urgent: meeting moved.")["score"], 1)

    def test_credential_request(self):
        self.assertEqual(analyze_email_content("Enter your password to proceed.")["score"], 2)

    def test_phishing_pasted_email(self):
        result = analyze_email_content("Urgent: verify your password immediately at http://192.0.2.10/login")
        self.assertEqual(result["classification"], "HIGH RISK")
        self.assertEqual(len(result["urls"]), 1)

    def test_misleading_html_link(self):
        result = analyze_email_content(html_text='<a href="https://actual.example/">https://trusted.example/</a>')
        self.assertEqual(result["score"], 3)

    def test_html_link_same_host(self):
        result = analyze_email_content(html_text='<a href="https://example.org/">https://example.org/</a>')
        self.assertEqual(result["score"], 0)
        self.assertEqual(result["urls_total"], 1)

    def test_eml_parses_subject_and_sender(self):
        raw = (b"From: Faculty <faculty@example.edu>\nSubject: Project update\n"
               b"MIME-Version: 1.0\nContent-Type: text/plain; charset=UTF-8\n\nSee you soon.")
        result = analyze_email_file(raw)
        self.assertEqual(result["subject"], "Project update")
        self.assertEqual(result["score"], 0)

    def test_eml_parses_html(self):
        raw = (b"From: Team <team@example.org>\nSubject: Link\nMIME-Version: 1.0\n"
               b"Content-Type: text/html\n\n"
               b'<a href="http://192.0.2.10/login">https://portal.example.org</a>')
        self.assertEqual(analyze_email_file(raw)["classification"], "HIGH RISK")

    def test_eml_size_limit(self):
        with self.assertRaises(ValueError):
            analyze_email_file(b"A" * 2_000_001)

    def test_email_url_dedup(self):
        result = analyze_email_content("https://example.org https://example.org")
        self.assertEqual(result["urls_total"], 1)


if __name__ == "__main__":
    unittest.main()

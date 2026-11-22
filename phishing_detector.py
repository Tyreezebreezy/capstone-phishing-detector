"""Capstone 1 minimum working phishing screener.

Static offline heuristics, not a security verdict. Never visits links or runs attachments.
Python 3.10+; standard library only.
"""

import argparse
from email import policy
from email.parser import BytesParser
from html.parser import HTMLParser
import ipaddress
from pathlib import Path
import re
from urllib.parse import urlsplit

URL_RE = re.compile(r"https?://[^\s<>\"'()]+", flags=re.IGNORECASE)
URGENT_PHRASES = (
    "act now", "immediately", "urgent", "account suspended", "within 24 hours",
    "final warning", "account will be locked", "limited time to respond",
)
SENSITIVE_PHRASES = (
    "verify your password", "enter your password", "confirm your password",
    "provide your password", "provide your ssn", "provide your credit card",
    "enter your one-time code", "send your password",
)
MAX_URLS = 20
MAX_EMAIL_BYTES = 2_000_000


def classify(score):
    if score >= 3:
        return "HIGH RISK"
    if score >= 1:
        return "REVIEW RECOMMENDED"
    return "NO INDICATORS FOUND"


def defang(value):
    """Keep printed URLs non-clickable in reports/terminal output."""
    return value.replace("https://", "hxxps[:]//").replace("http://", "hxxp[:]//")


def analyze_url(url):
    """Parse and assess a URL locally; never fetch, resolve, or browse it."""
    raw = url.strip()
    invalid = {"input": raw, "score": 0, "classification": "INVALID INPUT", "findings": []}
    if not raw or any(ch.isspace() or ord(ch) < 32 for ch in raw):
        return {**invalid, "findings": ["Empty URL or whitespace/control characters"]}
    candidate = raw if "://" in raw or ":" in raw.split("/", 1)[0] else "https://" + raw
    try:
        parsed = urlsplit(candidate)
        host = parsed.hostname
        _ = parsed.port  # Validate port syntax.
        if parsed.scheme.lower() not in {"http", "https"} or not host:
            raise ValueError("Only http(s) URLs with hostnames are accepted")
        hostname = host.rstrip(".").encode("idna").decode("ascii").lower()
        if not hostname or len(hostname) > 253:
            raise ValueError("Invalid hostname")
        try:
            ip = ipaddress.ip_address(hostname)
        except ValueError:
            ip = None
            labels = hostname.split(".")
            if len(labels) < 2 or any(
                not 1 <= len(part) <= 63
                or re.fullmatch(r"[a-z0-9](?:[a-z0-9-]*[a-z0-9])?", part) is None
                for part in labels
            ):
                raise ValueError("Invalid hostname")
    except (ValueError, UnicodeError) as exc:
        return {**invalid, "findings": [f"Cannot parse URL: {exc}"]}

    score, findings = 0, []
    if parsed.scheme.lower() == "http":
        score += 1
        findings.append("HTTP used instead of HTTPS (weak indicator on its own)")
    if parsed.username is not None or parsed.password is not None:
        score += 2
        findings.append("URL contains user information before @, which can disguise the destination")
    if ip is not None:
        score += 2
        findings.append("Destination uses a numeric IP address rather than a domain")
    if "xn--" in hostname:
        score += 1
        findings.append("Hostname contains punycode/IDN encoding (not automatically malicious)")
    if re.search(r"(?:^|[/_.=-])(verify|reset-password|password|login)(?:$|[/_.?=&-])", parsed.path.lower()):
        score += 1
        findings.append("URL path contains login or verification terms (weak indicator)")
    return {"input": raw, "score": score, "classification": classify(score), "findings": findings}


class HTMLLinkParser(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.links = []
        self.visible_text = []
        self.link_mismatches = []
        self._href = None
        self._anchor_text = []

    def handle_starttag(self, tag, attrs):
        if tag.lower() != "a":
            return
        self._href = dict(attrs).get("href") or ""
        self._anchor_text = []
        if self._href.lower().startswith(("http://", "https://")):
            self.links.append(self._href)

    def handle_data(self, data):
        self.visible_text.append(data)
        if self._href is not None:
            self._anchor_text.append(data)

    def handle_endtag(self, tag):
        if tag.lower() != "a" or self._href is None:
            return
        displayed = "".join(self._anchor_text).strip()
        if displayed.lower().startswith(("http://", "https://")):
            try:
                expected_host = urlsplit(displayed).hostname
                actual_host = urlsplit(self._href).hostname
                if expected_host and actual_host and expected_host.lower() != actual_host.lower():
                    self.link_mismatches.append((displayed, self._href))
            except ValueError:
                pass
        self._href = None
        self._anchor_text = []


def analyze_email_content(plain_text="", html_text="", subject="", sender=""):
    """A shared engine for pasted text and parsed .eml messages."""
    collector = HTMLLinkParser()
    if html_text:
        collector.feed(html_text)
    combined = " ".join([subject, plain_text, " ".join(collector.visible_text)]).lower()
    urls = [match.rstrip(".,;!])") for match in URL_RE.findall(plain_text)]
    urls.extend(collector.links)
    unique_urls = list(dict.fromkeys(urls))
    inspected = [analyze_url(u) for u in unique_urls[:MAX_URLS]]

    score, findings = 0, []
    if any(term in combined for term in URGENT_PHRASES):
        score += 1
        findings.append("Urgency or account-threat wording was detected")
    if any(term in combined for term in SENSITIVE_PHRASES):
        score += 2
        findings.append("Message explicitly asks for sensitive credentials or information")
    if collector.link_mismatches:
        score += 3
        findings.append("Displayed website hostname differs from an HTML link's actual destination")
    if inspected:
        max_url_risk = max(item["score"] for item in inspected)
        if max_url_risk:
            score += max_url_risk
            findings.append("An embedded URL triggered one or more structural warnings")
    if len(unique_urls) > MAX_URLS:
        findings.append(f"Only the first {MAX_URLS} of {len(unique_urls)} unique URLs were checked")

    return {
        "type": "email", "subject": subject or "(not provided)",
        "sender": sender or "(not provided)", "score": score,
        "classification": classify(score), "findings": findings,
        "urls": inspected, "urls_total": len(unique_urls),
    }


def analyze_email_file(raw_bytes):
    if len(raw_bytes) > MAX_EMAIL_BYTES:
        raise ValueError("Email exceeds the 2 MB prototype limit")
    message = BytesParser(policy=policy.default).parsebytes(raw_bytes)
    plain_parts, html_parts = [], []
    for part in message.walk():
        if part.get_content_disposition() == "attachment":
            continue
        kind = part.get_content_type()
        if kind not in {"text/plain", "text/html"}:
            continue
        try:
            value = part.get_content()
        except (LookupError, UnicodeError, ValueError):
            continue
        if isinstance(value, str):
            (plain_parts if kind == "text/plain" else html_parts).append(value)
    return analyze_email_content(
        plain_text="\n".join(plain_parts), html_text="\n".join(html_parts),
        subject=str(message.get("Subject", "")), sender=str(message.get("From", "")),
    )


def display(result):
    print(f"\nRESULT: {result['classification']} | heuristic score: {result['score']}")
    if result.get("type") == "email":
        print(f"Subject: {result['subject']} | Sender: {result['sender']}")
    for finding in result["findings"]:
        print(f" - {finding}")
    if "urls" in result:
        print(f"Embedded URLs inspected: {len(result['urls'])}/{result['urls_total']}")
        for url_result in result["urls"]:
            print(f" * {defang(url_result['input'])} [{url_result['classification']}]")
            for finding in url_result["findings"]:
                print(f"    - {finding}")
    print("WARNING: Risk is not a probability. No indicators does not mean safe.")


def run_menu():
    while True:
        print("\nPHISHING DETECTOR MWM | 1: URL | 2: Paste email | 3: .eml file | q: Quit")
        choice = input("Choose: ").strip().lower()
        if choice == "q":
            return
        if choice == "1":
            display(analyze_url(input("Enter URL: ")))
        elif choice == "2":
            print("Paste email text. Type END on a separate line when finished:")
            lines = []
            while True:
                line = input()
                if line == "END":
                    break
                lines.append(line)
            display(analyze_email_content(plain_text="\n".join(lines)))
        elif choice == "3":
            path = Path(input("Path to .eml file: ").strip().strip('"'))
            try:
                display(analyze_email_file(path.read_bytes()))
            except (OSError, ValueError) as exc:
                print(f"Could not analyze file: {exc}")
        else:
            print("Choose 1, 2, 3, or q.")


def main():
    parser = argparse.ArgumentParser(description="Offline rule-based email and URL phishing demo")
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--url", help="Analyze one URL")
    mode.add_argument("--text", help="Analyze pasted email text")
    mode.add_argument("--email", type=Path, help="Analyze a .eml email file")
    args = parser.parse_args()
    try:
        if args.url is not None:
            display(analyze_url(args.url))
        elif args.text is not None:
            display(analyze_email_content(plain_text=args.text))
        elif args.email is not None:
            display(analyze_email_file(args.email.read_bytes()))
        else:
            run_menu()
    except (OSError, ValueError) as exc:
        parser.exit(2, f"Error: {exc}\n")


if __name__ == "__main__":
    main()

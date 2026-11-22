# How the Phishing Detector Works

## Simple explanation

The detector accepts one URL, pasted email text, or a raw `.eml` file and examines the input locally for a small set of explainable warning signs. Each triggered rule contributes a fixed number of points, and the total maps to a risk label. Email analysis also extracts HTTP(S) links, runs the same URL analyzer on the first 20 unique links, and reports every individual URL finding. The program never visits a submitted link, resolves a hostname, opens an attachment, contacts a reputation service, or treats the score as a probability.

## Technical explanation

The core implementation is `phishing_detector.py`.

1. `analyze_url()` strips outer whitespace, validates URL syntax, normalizes the hostname through IDNA, applies URL rules, sums their weights, and returns a dictionary containing the original input, score, classification, and findings.
2. `analyze_email_content()` combines the subject, plain text, and visible text extracted from HTML. It applies message-wording rules, checks HTML anchors for host mismatches, extracts unique HTTP(S) links, and invokes `analyze_url()` for up to 20 links.
3. Email scoring adds the fixed email-rule weights and the score of the most suspicious inspected URL. It does not add every URL score together.
4. `analyze_email_file()` enforces the 2 MB limit, parses bytes with `BytesParser(policy=policy.default)`, and collects supported text parts. Parts whose content disposition is `attachment` are skipped.
5. `classify()` maps score 0 to `NO INDICATORS FOUND`, scores 1–2 to `REVIEW RECOMMENDED`, and scores 3 or higher to `HIGH RISK`.

`ui_server.py` exposes the engine to a local web page through three endpoints:

- `POST /api/analyze-url` with a JSON URL;
- `POST /api/analyze-email` with JSON pasted text; and
- `POST /api/analyze-email-file` with raw `.eml` bytes.

The server allowlists static assets, applies a restrictive Content Security Policy, rejects oversized requests, and binds only to `127.0.0.1`. The browser code constructs result elements with `textContent`; it does not interpolate submitted values as HTML.

## Email analysis

### Pasted text

Pasted text is passed as the plain-text body. No sender or subject is inferred, so the result reports `(not provided)` for those fields. HTTP(S) strings matching the project's URL pattern are extracted, deduplicated while preserving order, and inspected.

### `.eml` files

The email parser reads the `Subject` and `From` headers for display. It walks MIME parts and accepts only `text/plain` and `text/html` parts that are not marked as attachments. Unsupported, malformed, or undecodable parts may be skipped. The program does not save or execute attachments.

### HTML links

The `HTMLLinkParser` collects HTTP(S) `href` values and visible text. When visible anchor text itself looks like an HTTP(S) URL, the parser compares its hostname with the `href` hostname. Different hostnames trigger a +3 finding. It does not follow redirects or determine whether either host is trustworthy.

### Email rules

| Rule | Weight | Implementation detail |
|---|---:|---|
| Urgency or account-threat wording | +1 | Case-insensitive substring match against the fixed `URGENT_PHRASES` tuple. |
| Explicit sensitive-information request | +2 | Case-insensitive substring match against `SENSITIVE_PHRASES`. |
| Visible-link hostname mismatch | +3 | Compares displayed HTTP(S) hostname with the HTML anchor destination hostname. |
| Embedded URL risk | + highest URL score | Adds only the maximum score among inspected embedded URLs. |

The subject participates in the wording scan. The sender is displayed but is not authenticated or scored.

## URL analysis

The detector accepts HTTP and HTTPS URLs. If the input does not contain a scheme-like prefix, it prepends `https://` for parsing. It rejects empty input, whitespace or control characters inside the value, unsupported schemes, missing or malformed hosts, invalid IDNA conversion, overlong hostnames, invalid domain labels, and malformed ports.

| Rule | Weight | Meaning and limitation |
|---|---:|---|
| HTTP instead of HTTPS | +1 | A weak transport indicator. Legitimate HTTP sites exist, and HTTPS alone does not prove safety. |
| User information before `@` | +2 | A username/password component can visually disguise the real destination host. |
| Numeric IP address host | +2 | Direct IP destinations are less recognizable to users but are not automatically malicious. |
| Punycode/IDN encoding | +1 | Flags `xn--` in the normalized hostname. Internationalized domains can be legitimate. |
| Login or verification path term | +1 | Matches `verify`, `reset-password`, `password`, or `login` at path-token boundaries. This is a weak indicator. |

The analyzer does not check the query string for those path terms, expand shortened links, inspect certificates, resolve DNS, retrieve content, compare brand names, or query reputation data.

## Classification logic

| Condition | Result |
|---|---|
| URL cannot be parsed or validated | `INVALID INPUT`, score 0, parse finding |
| Valid analysis score = 0 | `NO INDICATORS FOUND` |
| Valid analysis score = 1–2 | `REVIEW RECOMMENDED` |
| Valid analysis score ≥ 3 | `HIGH RISK` |

These labels describe the output of the implemented rules. They are not calibrated probabilities, and a zero score does not mean an input is safe.

## Limits

- False positives are possible because legitimate messages can use urgency, login terminology, IP addresses, HTTP, or punycode.
- False negatives are possible because phishing can avoid every implemented phrase and structural rule.
- No labeled real-world dataset has been evaluated, so the project has no established accuracy, precision, recall, or false-positive rate.
- No SPF, DKIM, DMARC, sender reputation, or mailbox authentication is performed.
- No live reputation, DNS, redirect, certificate, webpage, image, QR-code, or attachment analysis is performed.
- The phrase lists are English-language and use straightforward substring matching.
- MIME and URL parsing coverage is intentionally limited for a small academic prototype.

See [`LIMITATIONS.md`](LIMITATIONS.md) for presentation guidance about these boundaries.

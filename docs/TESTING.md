# Testing and Validation

## Automated suite

Run from the repository root:

```bash
python -m unittest -v
```

The current suite contains 30 tests:

- 20 detector tests in `test_detector.py`;
- 10 local UI/backend integration tests in `test_ui_server.py`.

The integration suite starts a temporary server on `127.0.0.1` with an operating-system-assigned port and makes loopback HTTP requests. A restricted execution environment may need to permit loopback sockets.

## Coverage by behavior

| Area | Verified examples |
|---|---|
| URL validation | Unsupported schemes, embedded whitespace, malformed ports |
| URL rules | HTTP, numeric IP, user-info obfuscation, punycode, login path term |
| Classification | Exact score boundaries 0, 1–2, and 3+ |
| Email wording | Benign text, urgency, credential request |
| Email URLs | Extraction, deduplication, per-URL analysis |
| HTML links | Matching and misleading displayed destinations |
| `.eml` | Header/body parsing, HTML parsing, 2 MB limit |
| Web integration | Static UI, URL/email/file endpoints, validation, allowlisted routes |
| Safe rendering | Frontend uses text nodes and does not use `innerHTML` for results |
| Local web access | Rejects unexpected Host and cross-origin Origin headers |

## Verified baseline

The detector's original 20 tests passed before the graphical interface was added. After the interface and integration tests were added, all 28 tests passed in an environment where loopback HTTP was allowed. The documentation audit reruns the same suite; record the most recent command output in the final handoff rather than treating this file as a live test dashboard.

## Manual UI checklist

1. Start `python ui_server.py` and open <http://127.0.0.1:8765>.
2. Scan `https://example.org` and confirm score 0 with `NO INDICATORS FOUND`.
3. Scan `http://192.0.2.10/login` and confirm score 4 with three URL findings.
4. Paste a suspicious message containing urgency, a credential request, and the synthetic IP URL; inspect the email and embedded-URL findings.
5. Upload `samples/suspicious_email.eml`; verify subject, sender, link mismatch, and URL details.
6. Submit an unsupported scheme such as `javascript:alert(1)`; confirm `INVALID INPUT`.
7. Submit an empty form; confirm a clear validation error.
8. Reset the form; confirm inputs, file selection, error, and results are cleared.
9. Paste literal HTML such as `<script>alert('demo')</script>`; confirm it remains text and no dialog executes.
10. Check desktop and mobile widths for clipping or horizontal overflow.

The most recent UI verification screenshots are stored in `screenshots/`.

## Continuous integration

`.github/workflows/tests.yml` runs `python -m unittest -v` on Python 3.10, 3.11, 3.12, and 3.13 for pushes and pull requests. The workflow uses no package-install step because runtime and tests use the standard library.

## What tests do not prove

Unit and integration tests establish that the implementation behaves as specified for selected synthetic cases. They do not establish:

- real-world phishing-detection accuracy;
- acceptable false-positive or false-negative rates;
- resistance to adversarial evasion;
- performance at production scale; or
- fitness for deployment as a security control.

Those claims would require a labeled dataset, an evaluation protocol, representative sampling, and independent review.

## PC transfer follow-up (2026-11-22)

The recovered ZIP was audited in a separate environment. The 20 detector tests remained unchanged. Two additional integration tests were added for Host and Origin request validation, bringing the suite to 30. GitHub Actions has **not** been observed running on the user's GitHub account; run and confirm the workflow after private publication. Browser-based validation on the transferred Windows PC is still required.

## Windows verification (2026-11-22)

The recovered source passed all 30 tests on Windows with Python 3.11.9 (`python -m unittest discover -v`) and Python 3.14.2 (`py -3 -m unittest discover -v`). `TEST_WINDOWS.cmd` also passed all 30 tests. The integration helper now closes success and error responses explicitly, eliminating the Python 3.14 resource-cleanup warnings. The detection engine and classification rules are unchanged.

A real Chromium browser exercised normal/suspicious URLs, review/invalid labels, normal/suspicious pasted email, both sample `.eml` files, blank inputs, reset, literal script text, wrong file extensions, and oversized files. Desktop and 390px layouts were checked. The browser console had no errors or warnings, and application requests stayed on localhost. macOS and teammate hardware have not been tested directly.

The initial private publication at commit `d0b0d3527983c6488bbcfadde3692c53cbcdafce` passed [all four GitHub Actions jobs](https://github.com/Tyreezebreezy/capstone-phishing-detector/actions/runs/44992669336) on Ubuntu with Python 3.10, 3.11, 3.12, and 3.13. A fresh GitHub clone matched all 64 tracked files and passed all 30 Windows tests. It also launched from outside its repository with site packages disabled (`python -S launch.py --no-browser --port 0`), served the interface, and returned the expected URL result.

`RUN_UI_WINDOWS.cmd` also served HTTP 200 on loopback. Both Unix scripts passed `sh -n`; an attempted `TEST_MAC_LINUX.sh` run under Git for Windows encountered this PC's Microsoft Store `python3` alias. Native macOS/Linux launcher behavior is not established by that Windows shell attempt or the Linux unit-test matrix.

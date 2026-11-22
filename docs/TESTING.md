# Testing and Validation

## Run the complete suite

From the repository root on Windows:

```powershell
py -3 -m unittest discover -v
```

On macOS/Linux:

```bash
python3 -m unittest discover -v
```

`python -m unittest discover -v` also works when `python` selects Python 3.10+. The `TEST_WINDOWS.cmd` and `TEST_MAC_LINUX.sh` wrappers run the same test modules.

The suite contains **30 tests**: 20 in `test_detector.py` and 10 in `test_ui_server.py`. The engine tests construct their fixtures in memory. The integration tests start a temporary server on `127.0.0.1` with an operating-system-assigned port, make real loopback requests, and load `samples/suspicious_email.eml` for the upload case. Restricted environments must permit loopback sockets. No external analysis service or installed Python package is required.

## Existing automated coverage

| Area | Cases exercised |
|---|---|
| URL validation | Unsupported scheme, embedded whitespace, malformed port |
| URL rules | HTTP, numeric IP, user information, punycode, login path term |
| Classification | Score boundaries 0, 1–2, and 3+ |
| Email wording | Benign text, urgency, credential request, combined suspicious text |
| Email links | Extraction, deduplication, matching and misleading HTML anchor hosts |
| `.eml` parsing | Subject/sender, HTML body, 2 MB parser limit |
| HTTP integration | Interface route, URL/text/file analysis, invalid URL, empty email, unknown path |
| Local access checks | Rejection of foreign Host and supplied Origin headers |
| Frontend source guard | Presence of `textContent` and absence of `innerHTML` |

The frontend source guard is not a browser execution test. Automated coverage is selective: it does not exhaust every MIME structure, request-size boundary, UI interaction, or malformed input.

## Manual UI checklist

Start the platform launcher described in [teammate setup](../TEAMMATE_SETUP.md). Use synthetic inputs only.

1. Scan `https://example.org`: score 0, `NO INDICATORS FOUND`.
2. Scan `http://example.org`: score 1, `REVIEW RECOMMENDED`.
3. Scan `http://192.0.2.10/login`: score 4, `HIGH RISK`, three URL findings.
4. Paste `The meeting is tomorrow at noon.`: score 0.
5. Paste `Urgent: enter your password at http://192.0.2.10/login`: score 7 with one inspected URL.
6. Upload each fixture: `normal_email.eml` scores 0; `suspicious_email.eml` scores 10 and reports the HTML-link hostname mismatch. Check subject, sender, and URL details.
7. Scan `javascript:alert(1)`: `INVALID INPUT`. Submit blank forms and check validation messages.
8. Select a file and enter pasted text: confirm the file takes precedence. Reset and confirm both inputs, file selection, errors, and results clear.
9. Paste literal `<script>alert('demo')</script>` text and use it in a synthetic `.eml` subject: confirm no script executes and displayed metadata remains text.
10. Check wrong file extensions, files over 2,000,000 bytes, and desktop/narrow layouts for errors or overflow.

Record the browser, platform, cases run, and outcome in the pull request. The images in [`screenshots/`](../screenshots/) illustrate the interface; they are not a live test dashboard.

## Continuous integration and platform scope

The [workflow](../.github/workflows/tests.yml) runs `python -m unittest -v` on Ubuntu with Python 3.10, 3.11, 3.12, and 3.13 for pushes and pull requests. This discovers the same 30 tests. It uses read-only repository contents permission and no dependency-install step.

Check the [Actions results](https://github.com/Tyreezebreezy/capstone-phishing-detector/actions/workflows/tests.yml) for the exact commit under review. A green Linux test matrix does not verify the graphical launchers on macOS or every teammate's computer. Native macOS launcher behavior remains unverified; Windows verification and current CI results belong in the relevant pull request.

## What tests do not prove

Unit and integration tests check selected expected behavior. They do not establish real-world phishing accuracy, precision, recall, false-positive or false-negative rates, adversarial robustness, production-scale performance, or fitness as a security control. Such claims require a labeled dataset and a separate evaluation protocol.

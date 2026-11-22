# Limitations and Responsible Interpretation

## What the result means

A result is a deterministic summary of the rules in `phishing_detector.py`. The heuristic score is not a probability, confidence level, or measured likelihood of phishing. The labels are convenient demonstration categories:

- score 0: `NO INDICATORS FOUND`;
- score 1–2: `REVIEW RECOMMENDED`; and
- score 3 or more: `HIGH RISK`.

`NO INDICATORS FOUND` means only that none of the implemented rules fired.

## False positives

Legitimate messages may use urgency, ask a user to log in, include a direct IP address, use HTTP for a test environment, or use an internationalized domain. The detector may therefore recommend review or mark a legitimate message high risk.

## False negatives

Attackers can avoid the fixed English phrases, use images or QR codes, hide content in unsupported MIME structures, use a normal-looking HTTPS domain, compromise a legitimate site, or rely on social context. The prototype may return no indicators for a harmful message.

## Features not implemented

- Real-world accuracy evaluation or a labeled dataset.
- Mailbox access or automatic message quarantine.
- SPF, DKIM, DMARC, sender/domain reputation, or identity verification.
- DNS, WHOIS, certificate, redirect, webpage, or URL-shortener expansion.
- Machine learning, large language models, or external APIs.
- Attachment, image, QR-code, macro, or malware analysis.
- Comprehensive MIME, encoding, obfuscation, or non-English-language analysis.
- A database, accounts, authentication, audit storage, or commercial deployment.

## Parsing and input boundaries

- Only the first 20 unique extracted HTTP(S) URLs are analyzed. The result reports the total extracted count and whether inspection was truncated.
- HTML text collection does not evaluate browser visibility. Script/style text can influence wording checks; the program does not execute it.
- MIME traversal skips individual parts marked as attachments, but is not a comprehensive attachment-container filter. Nested text parts can still be encountered. No attachment content is executed or scanned for malware.
- The web interface limits URLs to 4,096 characters, pasted email text to 2,000,000 UTF-8 bytes, and `.eml` uploads to 2,000,000 bytes. JSON endpoints also cap the complete encoded request body, so heavily escaped text can reach that cap before the text limit.
- The `.eml` parser enforces the same byte limit. CLI text and URL inputs do not use the web interface's separate size limits.

## Privacy and retention

The application is designed for local processing. The provided launchers and server CLI bind to `127.0.0.1`; browser requests remain on the same computer. Analysis data exists in process memory while a request is handled and is returned to the local interface. The application code does not persist submissions to a database or file and does not transmit them to an external service. Standard request logging prints method, path, status, and client address but not submitted content.

Users should still avoid pasting unnecessary confidential information during demonstrations. Local processing reduces exposure; it does not remove the responsibility to use authorized, minimal, synthetic data.

## Safe demonstration guidance

- Use `example.org`, `example.edu`, and documentation addresses such as `192.0.2.10`.
- Do not use live phishing links.
- Do not click or copy a submitted link into a browser.
- Do not open attachments from suspicious messages.
- Present test results as software verification, not detection-accuracy evidence.

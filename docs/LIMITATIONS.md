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

## Privacy and retention

The application is designed for local processing. The web server binds to `127.0.0.1`; browser requests remain on the same computer. Analysis data exists in process memory while a request is handled and is returned to the local interface. The application code does not persist submissions to a database or file and does not transmit them to an external service. Standard request logging prints method, path, status, and client address but not submitted content.

Users should still avoid pasting unnecessary confidential information during demonstrations. Local processing reduces exposure; it does not remove the responsibility to use authorized, minimal, synthetic data.

## Safe demonstration guidance

- Use `example.org`, `example.edu`, and documentation addresses such as `192.0.2.10`.
- Do not use live phishing links.
- Do not click or copy a submitted link into a browser.
- Do not open attachments from suspicious messages.
- Present test results as software verification, not detection-accuracy evidence.

# Phishing Detector: Standards, Frameworks, and Methodology

**Project:** Capstone 1 Phishing Detector (offline minimum working model)

**Status:** This is a *rule-based educational demonstration*, not a certified or standards-compliant email security gateway. These references explain the threat and inform secure handling. The team's heuristic rule weights and the 0 / 1-2 / 3+ classification thresholds are custom choices. They are **not** prescribed by NIST, MITRE, OWASP, the IETF, or an RFC.

## References connected to current implementation

| Reference | Type | Relationship to actual code | Status and limits |
| --- | --- | --- | --- |
| [NIST: Phishing guidance](https://www.nist.gov/itl/smallbusinesscyber/guidance-topic/phishing) | Government guidance, not a scoring standard | Context for social engineering, suspicious messages and credentials. The code uses English urgency and credential-request phrase checks. | **Conceptual reference.** The code does not implement a NIST-designated phishing scoring algorithm. |
| [MITRE ATT&CK T1566: Phishing](https://attack.mitre.org/techniques/T1566/) and [T1566.002: Spearphishing Link](https://attack.mitre.org/techniques/T1566/002/) | Adversary behavior taxonomy, not a compliance standard | Explains why email-borne links are a relevant threat category. | **Threat mapping only.** An ATT&CK label does not mean the system detects all examples of that technique. |
| [RFC 5322: Internet Message Format](https://www.rfc-editor.org/info/rfc5322/) | IETF Internet Message Format specification | Raw `.eml` content is parsed using Python `email.parser.BytesParser`, and Subject, From, text/plain and text/html fields are processed. | **Implementation-related reference.** No independent standards conformance testing has been performed. |
| [RFC 3986: URI Generic Syntax](https://www.rfc-editor.org/info/rfc3986/) | IETF URI syntax standard | URLs are decomposed using Python's `urllib.parse.urlsplit`, then scheme, host, port and structural features are checked. | **Implementation-related reference.** The parser is not a comprehensive RFC 3986 or browser-equivalence validator. |
| [OWASP Input Validation Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Input_Validation_Cheat_Sheet.html) | Application security guidance | The web server limits input sizes and rejects invalid requests; URL analysis checks syntactic features. | **Defensive design alignment**, not a full OWASP assessment. |
| [OWASP Cross Site Scripting Prevention Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Cross_Site_Scripting_Prevention_Cheat_Sheet.html) | Application security guidance | The frontend builds results using DOM nodes and `textContent` to display untrusted email and URL text instead of executing HTML. | **Defensive design alignment**, not a security certification. |

## Future-relevant email authentication standards (NOT implemented)

| Reference | What it covers | Current status |
| --- | --- | --- |
| [RFC 7208: SPF](https://www.rfc-editor.org/info/rfc7208/) | Sender Policy Framework authorizing the use of domains by mail systems. | **Not implemented.** No SPF verification or DNS checks. |
| [RFC 6376: DKIM](https://www.rfc-editor.org/info/rfc6376/) | DomainKeys Identified Mail signatures. | **Not implemented.** No DKIM signature verification. |
| [RFC 9989: DMARC](https://www.rfc-editor.org/info/rfc9989/) | Domain-based Message Authentication, Reporting, and Conformance; **obsoletes RFC 7489 and RFC 9091**. | **Not implemented.** No authenticated-domain alignment or DMARC policy enforcement. |
| [NIST SP 800-177 Rev. 1: Trustworthy Email](https://csrc.nist.gov/pubs/sp/800/177/r1/final) | Guidance on email security protocols and trust technologies. | **Future design reference**, not proof of compliance. |

Note: Many older tutorials cite RFC 7489 as the DMARC specification. RFC 9989 is the current successor (published 2026). The project does not perform DMARC checks under either RFC.

## Implemented checks and custom weights (from `phishing_detector.py`)

| Input | Detection feature | Weight |
| --- | --- | ---: |
| URL | HTTP rather than HTTPS | +1 |
| URL | Username/password userinfo within URL authority (`@` obfuscation) | +2 |
| URL | Numeric IP address as host | +2 |
| URL | Punycode or `xn--` hostname | +1 |
| URL | `verify`, `reset-password`, `password`, or `login` path terms | +1 |
| Email | Urgency/account-threat phrase | +1 |
| Email | Explicit sensitive-information request | +2 |
| Email | Visible URL host differs from the actual HTML anchor host | +3 |
| Email | Strongest of the inspected embedded URL scores | +maximum URL score |

**Thresholds:** Score 0 = `NO INDICATORS FOUND`; 1–2 = `REVIEW RECOMMENDED`; 3+ = `HIGH RISK`. Invalid URLs return `INVALID INPUT` and are not assigned a valid risk level. Email scoring uses *only the highest-scoring inspected embedded URL*, not a sum over all URLs. The program inspects a maximum of 20 unique extracted URLs.

## Exactly what the system does not claim

- The heuristic score is not a calibrated probability, NIST risk score, MITRE ATT&CK detection coverage metric, or certification result.
- A score of zero does not establish safety. HTTPS does not establish legitimacy.
- The `From` header is displayed but is **not authenticated or scored**.
- The system cannot confirm whether a site is live, compromised, blacklisted, or malicious because it does not access it.
- There is no measured precision, recall, false-positive rate, or false-negative rate on an independently labeled dataset.
- No live email-security gateway, attachment scanning, or machine-learning classifier is implemented.

## Describing the methodology

The design can be described as **“an offline, explainable, rule-based phishing screening prototype informed by NIST phishing guidance, mapped to MITRE ATT&CK T1566, using standard-library email and URL parsing and OWASP-inspired untrusted-input handling.”**

Do **not** describe it as “NIST-certified,” “MITRE-certified,” “RFC-compliant,” or as a tool that “uses NIST scoring.” All mappings and claims should be reviewed by the team before publication or presentation.

> Historical pre-publication archive audit. Its unverified PC/GitHub statements describe that earlier environment; see [docs/TESTING.md](docs/TESTING.md) for the Windows follow-up.

# Capstone 1 sanity audit — 2026-11-22

## Source of truth
Recovered `Capstone1_Phishing_Detector_Private_GitHub_Handoff_2026-11-22.zip` and compared its contents with `Capstone1_Phishing_Detector_Complete_2026-11-21.zip`. Both archives passed ZIP integrity checks. The newer archive adds the standards document and GitHub handoff to the same MWM.

## Verified in the current environment
- 20 existing detection-engine tests pass.
- 10 UI/server integration tests pass, **30 tests total**, including the 2 added in this recovery audit.
- Python files compile successfully. JavaScript `node --check` passes.
- HTTP loopback API tests verify URL, pasted email, `.eml` upload, malformed inputs, and allowlisted routes.
- Frontend source displays untrusted result text through `textContent` and DOM nodes, not `innerHTML`.
- The rule weights and thresholds in `docs/PHISHING_STANDARDS_AND_METHODS.md` match `phishing_detector.py`.
- Editable Mermaid diagrams and rendered SVG/PNG, sample `.eml` files, README, GitHub Actions configuration, and UI screenshots are present.
- The rule engine `phishing_detector.py` matches the earlier archive byte-for-byte (SHA256: `cbca1acd1fb32b219106954694373e72f3c5d17b6f49e5ce5d2c43524ee17b74`).
- No project `.git` history or authenticated GitHub publishing state is bundled; **GitHub publication cannot be inferred**.

## Targeted recovery fix
The loopback web server previously trusted any incoming Host/Origin. It now checks requests for local Host and POST Origin, reducing inadvertent cross-site access/DNS-rebinding exposure. Added 2 corresponding integration tests. The detection/scoring engine and browser interface were not modified.

## Not verified here
- Whether the old laptop's latest unarchived code transferred to the new Windows PC.
- Whether the app is currently installed or running on the new PC.
- Windows-specific launch paths, browser UI behavior and firewall controls on the new PC.
- GitHub repo ownership, private visibility, collaborators or live CI (requires authenticated GitHub access).
- Real-world detection performance or security certification.

## Browser test limitation
The current execution environment rejected direct Chromium navigation to local addresses with `ERR_BLOCKED_BY_ADMINISTRATOR`; automated Python HTTP integration tests succeeded. Therefore fresh browser viewport/screenshot QA was **not** independently completed here. Existing screenshots from the 2026-11-21 package were visually inspected. Run the manual Windows browser checklist before group presentation.

## Documentation/status
- Official RFC Editor lists RFC 9989 as the 2026 successor to RFCs 7489 and 9091 (DMARC), **not implemented** by the project.
- Official GitHub Actions READMEs document `actions/checkout@v7` and `actions/setup-python@v7`. Their presence in the workflow does not verify a live GitHub Actions run.
- NIST phishing guidance and MITRE ATT&CK are conceptual references only. Rule weights are original project heuristics, not a certified standard.
- Project `LICENSE` file is still absent; the group must choose one deliberately if desired.

## Next gate
Verify on the Windows PC, publish to PRIVATE GitHub after confirming the authenticated owner and no existing repo, invite classmates, verify CI, then work on FIU Week 13 together.

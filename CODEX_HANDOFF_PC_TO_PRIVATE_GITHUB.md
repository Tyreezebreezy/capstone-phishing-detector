# CODEX HANDOFF | Capstone 1 Phishing Detector | PC recovery, QA, private GitHub

**Date:** November 22, 2026  
**Project:** `capstone-phishing-detector`  
**Target:** A private GitHub repository owned by the student's authenticated GitHub account, accessible to invited classmates  
**Scope:** Recover, validate, publish, and verify the **existing** minimum working model. Do **not** rebuild or add features unless a concrete defect requires it.

## 1. What the project IS

A small, local-first phishing *screening prototype*, written in Python 3.10+ standard library plus bundled HTML/CSS/JavaScript. A Python server on `127.0.0.1` serves the interface to a web browser running on the **same machine**. Each teammate can clone the private repo and run their own local copy, anywhere, after installing Python. This is not a hosted site, a standalone `file://` page, or an executable that works without Python.

Already implemented:
- URL analysis; pasted email analysis; `.eml` file analysis.
- Email link extraction and URL analysis; transparent rule-based scoring and explanations.
- `web/` UI, `ui_server.py`, `launch.py` and cross-platform launch/test scripts.
- Automated tests, two synthetic `.eml` samples, screenshots, technical documentation, 10 Mermaid diagrams and PNG/SVG exports, GitHub Actions configuration.

Current known heuristic labels: `NO INDICATORS FOUND` (0), `REVIEW RECOMMENDED` (1–2), `HIGH RISK` (3+), `INVALID INPUT` for bad URLs. Scores are **not probabilities or validated threat verdicts**. Do not promise phishing detection accuracy.

## 2. Source of truth: recover without losing PC changes

The supplied archive is **`Capstone1_Phishing_Detector_Codex_Ready_2026-11-22.zip`**, containing the `capstone-phishing-detector/` project folder. It is derived from the latest team-portable archive and has the current handoff added. Avoid the older, similarly named `capstone_phishing_mwm_v02.zip` unless a comparison proves it has newer valid edits.

1. Record `whoami`, current directory, `python --version` / `py -3 --version`, `git --version`, `gh --version` (if installed). Identify which Windows desktop/PC is being used.
2. Search likely local paths first: Downloads, Documents, Desktop, OneDrive Documents if applicable, the earlier `<user-documents>/Codex/<earlier-session>/outputs/`, and any known `Development` folder. Do **not** indiscriminately crawl unrelated folders or delete anything.
3. Find Git repos named `capstone-phishing-detector`, `capstone_phishing_mwm_v02`, or similar; record `git status`, `git remote -v`, recent commits and any uncommitted work. Determine whether the project's actual canonical repository is already on this PC or on GitHub.
4. Compare the source archive with any existing project copy. Preserve newer, unique, or uncommitted work. Back it up before changes. Don't overwrite, reset, clean, force-push or delete someone else's modifications.
5. If no newer copy exists, extract the supplied archive to a stable local workspace such as `Documents\Development\capstone-phishing-detector`. Avoid nested duplicate `capstone-phishing-detector\capstone-phishing-detector` roots.
6. Work from the folder containing `phishing_detector.py`, `ui_server.py`, `web/`, `test_detector.py`, `test_ui_server.py`, `README.md`, `docs/`, and `.github/`.

## 3. Mandatory local sanity check on THIS PC

From the project root:

```powershell
py -3 --version
py -3 -m unittest discover -v
py -3 launch.py
```

If `py` is absent use `python`; install Python 3.10+ if neither works. `START_WINDOWS.cmd` and `TEST_WINDOWS.cmd` should work as simple launchers. Open `http://127.0.0.1:8765` in the PC's browser after starting the server.

Perform actual checks, not just a screenshot review:
- `https://example.org` -> `NO INDICATORS FOUND`, score 0.
- `http://192.0.2.10/login` -> `HIGH RISK`, score 4.
- Paste a benign message and an example suspicious message (synthetic only).
- Upload `samples/suspicious_email.eml` -> check result and URL findings; test `samples/normal_email.eml`.
- Confirm invalid/blank input, reset, and the handling of malicious text without executing injected HTML/JS.
- Check that UI, styles and script load in browser with no missing files; no browser console errors; sensible narrow-screen layout.
- Verify the server binds **only** to loopback, does not resolve/visit submitted URLs or send email to services, and does not retain input in a database.
- Confirm local Host and Origin checks and input-size limits. Use reserved documentation domains and IPs in tests.
- Check for stray credentials, personal email contents, API keys, private screenshots, or large build artifacts before Git upload.

**Known baseline from an independent Linux runtime check (Nov 22):** archive integrity PASS; `python -m unittest discover -v` **30/30 passed** (20 detector + 10 UI/server tests); Python syntax PASS; `node --check web/app.js` PASS; `launch.py --no-browser --port 18766` served the UI (`HTTP 200`) and analyzed a URL (`HIGH RISK`, score 4). The engine source checksum is `cbca1acd1fb32b219106954694373e72f3c5d17b6f49e5ce5d2c43524ee17b74`. **Windows, macOS, GitHub Actions, and teammate machines are NOT confirmed by those Linux checks.** Codex must record results of its own Windows execution and report failures instead of restating the baseline as new testing.

If a test fails, diagnose and apply the smallest necessary patch, then rerun the full suite. Do not rewrite the detector, scoring rules, or UI without an actual defect. If Python port 8765 is occupied, close the old instance or use `py -3 launch.py --port 8766` and visit that address.

## 4. Private GitHub publication: required outcome

**Do not assume this archive is already on GitHub.** The supplied ZIP contains no `.git` history or configured remote. GitHub account authentication is not included in the ZIP.

1. Check `gh auth status`. If needed, prompt the student to authenticate via interactive `gh auth login` on the PC. Never request or print access tokens or save credentials to the repository. Confirm the correct personal account.
2. Check whether `capstone-phishing-detector` already exists under that account with `gh repo view OWNER/capstone-phishing-detector --json url,isPrivate,nameWithOwner`. Also examine `git remote -v` on any existing clone. If an authoritative class group repo already exists, **reconcile with it** rather than creating a second repo.
3. If the repo exists, verify it is PRIVATE. Clone/fetch safely; compare commits and files; work on a new branch and submit a pull request if other work or conflicts exist. Never force-push or replace teammates' changes. If currently public, do not push class materials until privacy is addressed and owner approves.
4. If no target repo exists, and the correct owner and source folder are confirmed, initialize `main` and publish the cleaned working project as **PRIVATE**. Example only for a genuinely new repo:

```powershell
git init -b main
git add .
git commit -m "Initial Capstone 1 phishing detector MWM"
gh repo create capstone-phishing-detector --private --source=. --remote=origin --push
```

5. Verify actual remote location, visibility and commit SHA. Inspect GitHub README rendering, Mermaid diagrams, screenshots, provenance/standards documentation, and file tree.
6. Trigger/inspect GitHub Actions and verify it really runs successfully (not merely that `.github/workflows/tests.yml` exists). Current workflow targets Python 3.10–3.13; preserve the matrix unless failures justify a change. Do not claim the workflow passed until GitHub confirms it.
7. Update README's pre-publication note if it says the repository has not been published. Commit/push this correction safely.
8. Invite classmates to the private repo only with **verified GitHub usernames provided/approved by the student**. Provide instructions for **Settings > Collaborators** if invitations require the account owner. Invitations are not access until accepted.
9. For a fresh teammate checkout, follow `TEAMMATE_SETUP.md`: authenticate, `git clone` the private URL, `cd capstone-phishing-detector`, run `python -m unittest -v`, then `python launch.py` (or appropriate OS launcher), and open localhost. No Python installer needs to be bundled and no cloud server should be set up.

## 5. Documentation, ethics and standards checks (do not start Week 13 answers)

Verify—not merely assume—the following files match source code:
- `README.md`, `TEAMMATE_SETUP.md`, `CONTRIBUTING.md`.
- `docs/HOW_IT_WORKS.md`, `docs/SYSTEM_ARCHITECTURE.md`, `docs/TESTING.md`, `docs/LIMITATIONS.md`.
- `docs/PHISHING_STANDARDS_AND_METHODS.md`, `docs/PROVENANCE_AND_ETHICS.md`.
- 10 `.mmd` diagrams and their SVG/PNG exports.

Standards references are **context/mappings**, not certifications or implemented email-authentication engines: NIST phishing guidance; MITRE ATT&CK T1566; RFC 5322; RFC 3986; OWASP input handling; SPF/DKIM/DMARC are **not implemented**. The scoring weights are project-created heuristics. No independently measured accuracy, false-positive rate or recall exists. Preserve accurate AI/Codex disclosure. There is no team-approved project `LICENSE` on record: do not invent one; note license decision is pending.

Only after the repository is verified will we complete the FIU Week 13 Provenance and Ethics assignment **together**. Do not draft/substitute classmates' experiences as facts, do not submit the class assignment, and do not imply teammates reviewed material unless they did.

## 6. Final acceptance checklist

- [ ] Canonical version identified on PC; no local work overwritten.
- [ ] Python 3.10+ confirmed; tests passed on this PC (actual count/results documented).
- [ ] URL, email and `.eml` workflows demonstrated in the PC browser.
- [ ] Windows startup scripts work; teammates can run separate localhost copies.
- [ ] No unexpected third-party runtime dependencies, credentials, or private data in repo.
- [ ] Documentation/diagrams reflect code and correctly state limitations.
- [ ] Repo actually exists in correct GitHub account and is **PRIVATE**.
- [ ] Commit SHA and GitHub URL reported; GitHub Actions actually pass (or failure described).
- [ ] Teammate invitation status recorded, pending usernames if not yet provided.
- [ ] Week 13 not started until owner returns.

## 7. Required Codex report

Return a concise audit with: discovered PC paths and which source was chosen; differences reconciled; **exact** test commands and results; local browser scenarios; changes made; private repository URL, owner and commit SHA; Actions run link/status; teammate invitation state; outstanding issues and owner actions. If any step is blocked by missing authentication, permissions, or a team decision, state precisely what remains, **without claiming it was completed**.

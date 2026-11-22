> **Historical report (2026-11-21):** This describes the earlier 28-test build. For the 2026-11-22 restored and hardened 30-test build, see [`SANITY_AUDIT_2026-11-22.md`](SANITY_AUDIT_2026-11-22.md).

# Capstone 1 Phishing Detector — Final Handoff Report

## Completed work

The repository was audited against the implementation rather than prior descriptions. The detector engine, 20 original tests, 8 UI integration tests, two synthetic `.eml` samples, local web server, HTML/CSS/JavaScript interface, screenshots, and README were reviewed.

Created or substantially updated:

- `README.md` — concise project overview, verified commands, architecture, rules, limitations, collaboration, AI disclosure, and references.
- `CONTRIBUTING.md` — student workflow, safety rules, validation, pull-request checklist, and publication guidance.
- `.gitignore` — Python, editor, operating-system, and temporary artifacts.
- `.github/workflows/tests.yml` — Python 3.10–3.13 unittest matrix using `actions/checkout@v7` and `actions/setup-python@v7`.
- `docs/HOW_IT_WORKS.md` — simple and technical explanations of URL, email, `.eml`, scoring, and boundaries.
- `docs/SYSTEM_ARCHITECTURE.md` — complete embedded diagram package and presentation order.
- `docs/TESTING.md` — automated/manual validation and accuracy caveat.
- `docs/PROVENANCE_AND_ETHICS.md` — components, licenses, AI assistance, privacy, ethics, and team-confirmation items.
- `docs/LIMITATIONS.md` — responsible interpretation, false positives/negatives, exclusions, and demo safety.
- `docs/diagrams/` — ten editable Mermaid sources.
- `docs/diagrams/rendered/` — ten SVG and ten PNG presentation exports.

No detection rule, threshold, phrase list, parser behavior, or input limit was changed during the documentation handoff.

## Diagram package

Completed and rendered:

1. Simplified professor-facing overview.
2. High-level system architecture.
3. URL detection flowchart with invalid-input path.
4. Email detection flowchart.
5. Level 0 data-flow context diagram.
6. Level 1 data-flow diagram.
7. Sequence diagram.
8. Scoring/classification decision flow.
9. Repository component diagram.
10. Testing and validation workflow.

All Mermaid sources rendered successfully with Mermaid CLI 11.12.0. PNG exports were visually inspected. System architecture, Level 1 data flow, and testing workflow were revised and re-rendered to improve slide legibility.

## Verified capabilities

- URL input validation and five URL structural rules.
- Pasted-text email analysis and three email-level rules.
- `.eml` parsing of headers and text parts, with attachment parts skipped.
- Unique HTTP(S) URL extraction and analysis of the first 20 URLs.
- Email scoring using the most suspicious embedded URL score.
- Exact labels and thresholds documented from source.
- CLI and local single-page web UI.
- 2 MB email limit and 4,096-character web URL limit.
- Escaped/defanged frontend result display.
- Local-only server binding with no external analysis calls or storage layer.

## Validation results

- Python syntax compilation: passed.
- JavaScript syntax check: passed.
- Final automated test suite: **28/28 passed**.
  - Detector tests: 20/20.
  - UI/backend integration tests: 8/8.
- Mermaid rendering: 10/10 sources produced SVG and PNG exports.
- Visual diagram inspection: completed for all 10 PNGs.
- Earlier UI/browser verification: desktop and mobile layouts, URL flow, pasted email, sample `.eml`, validation, reset, and literal malicious-text rendering passed with no relevant console errors.

A restricted sandbox initially denied loopback sockets with `WinError 10013`; this is an environment constraint. The complete suite passed when loopback-only access was permitted.

## Documentation discrepancies corrected

- The project now documents the existing web interface instead of describing the system as CLI-only.
- Sender information is correctly described as displayed but not authenticated or scored.
- Email URL scoring is documented as adding the maximum inspected URL score, not the sum of all URL scores.
- HTML host mismatch applies only when visible anchor text itself begins with HTTP(S).
- Attachment parts are skipped; the project does not perform attachment analysis.
- Passing tests are clearly separated from any claim of real-world detection accuracy.
- Local request logging is distinguished from persistent input storage.

## GitHub status

The delivered folder is **not currently a Git repository** and has no configured remote. No commit, push, pull request, or live GitHub Actions run was performed. The workflow and collaboration files are ready for team review.

After confirming the correct repository URL, a team member can:

```bash
git init
git add .
git commit -m "Document architecture and capstone handoff"
git branch -M main
git remote add origin <confirmed-repository-url>
git push -u origin main
```

If a shared repository already exists, clone or pull that repository first and copy/review these changes on a branch instead of initializing over classmates' work.

## Group confirmation still needed

- Final GitHub repository URL, visibility, and collaborators.
- Project license for original team code and documentation.
- Student names/roles and any course-required acknowledgements.
- Instructor-required format and placement of AI disclosure.
- Whether the team will use any real or labeled email dataset later and what approval applies.
- Whether screenshots contain only content approved for presentation.

## Remaining limitations

The detector has no measured real-world accuracy, sender authentication, live reputation checks, redirect/DNS/certificate inspection, machine learning, attachment analysis, multilingual rule set, database, or production deployment controls. Fixed rules may produce false positives and false negatives.

## Three-diagram presentation walkthrough

1. Start with `simplified-overview`: explain input → warning-sign checks → score → understandable reasons, while emphasizing local processing.
2. Show `system-architecture`: explain how direct URLs and email-extracted URLs share one analyzer and how email rules join the same scoring path.
3. Show `scoring`: explain `0`, `1–2`, and `3+`, then state clearly that the score is not a phishing probability.

Use `url-analysis` or `email-analysis` for implementation questions and `testing-workflow` when distinguishing software tests from detection-accuracy evaluation.

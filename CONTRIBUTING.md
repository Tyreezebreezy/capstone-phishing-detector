# Contributing

This repository is an academic proof of concept. Keep changes small, explainable, and easy for classmates to review.

## Before starting

1. Confirm the intended GitHub repository and issue/task with the group.
2. Pull the latest changes and create a short-lived branch such as `docs/email-flow` or `fix/url-validation`.
3. Do not commit real suspicious URLs, private emails, credentials, student records, or other personal information.

## Development rules

- Preserve the offline safety boundary: never visit, resolve, or execute submitted links.
- Do not open or execute attachments.
- Do not add cloud services, accounts, databases, paid APIs, or machine-learning dependencies without explicit group approval and a revised scope.
- Keep detection rules and weights in `phishing_detector.py` synchronized with tests and documentation.
- Use reserved example domains and documentation IP ranges in fixtures.
- Render untrusted content as text, not executable HTML.

## Validate a change

Run from the repository root:

```bash
python -m unittest -v
```

For UI changes, also run `python ui_server.py`, open <http://127.0.0.1:8765>, and manually exercise the affected flow. Record what you tested in the pull request.

For Mermaid changes, verify the source renders in GitHub or with Mermaid CLI. Keep the editable `.mmd` file and update the matching export in `docs/diagrams/rendered/` when rendering is available.

## Pull-request checklist

- [ ] Tests pass locally.
- [ ] New behavior has a regression test.
- [ ] README and technical documentation match the implementation.
- [ ] No secrets, personal data, or live malicious samples were added.
- [ ] No detection-accuracy claim is based only on unit tests.
- [ ] Diagram source and rendered export agree.
- [ ] AI-assisted material was reviewed and disclosed when relevant.

## Publishing

Do not force-push shared branches or overwrite another student's changes. Use a pull request and wait for classmate review. The private repository is [Tyreezebreezy/capstone-phishing-detector](https://github.com/Tyreezebreezy/capstone-phishing-detector). Clone it after accepting the owner's invitation; confirm `git remote -v` before pushing.

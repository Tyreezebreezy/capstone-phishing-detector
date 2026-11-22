# Development Provenance and Acknowledgments

This record distinguishes verified assistance, third-party tools, and decisions still requiring student-team review.

## AI assistance

Recorded ChatGPT/Codex assistance includes reviewing the supplied Python detector, tests, samples, README, and local UI; generating the standard-library web-server layer and browser interface; generating integration tests; refining technical documentation and Mermaid diagrams; and running automated and browser-based verification. Later repository work included Windows recovery, private GitHub publication, explicit HTTP-response cleanup in the test helper, and a documentation quality-control pass.

This record does not establish the authorship of the original detection logic. It does not imply that the team has approved every generated decision or completed an independent dataset evaluation.

The student team remains responsible for understanding and reviewing the work, confirming author names and roles, and meeting FIU course and instructor requirements for AI acknowledgment. Any required course-specific disclosure must be retained in the appropriate submission; its final wording and placement have not yet been confirmed.

## Third-party components

The runtime application has no installed third-party Python or JavaScript dependencies.

| Component | Official source | License | Project use |
|---|---|---|---|
| Python and Python standard library | [Python Software Foundation](https://www.python.org/) | [PSF License and historical license stack](https://docs.python.org/3/license.html) | Runs the detector, email parser, URL parser, HTTP server, tests, and command-line interface. |
| Mermaid / Mermaid CLI 11.12.0 | [mermaid-js/mermaid](https://github.com/mermaid-js/mermaid) and [mermaid-js/mermaid-cli](https://github.com/mermaid-js/mermaid-cli) | MIT | Editable documentation diagrams and generated SVG/PNG exports; used as a temporary documentation tool and not loaded by the detector at runtime. |
| `actions/checkout` | [GitHub action repository](https://github.com/actions/checkout) | [MIT License](https://github.com/actions/checkout/blob/main/LICENSE) | Checks out repository content in the included GitHub Actions workflow. |
| `actions/setup-python` | [GitHub action repository](https://github.com/actions/setup-python) | [MIT License](https://github.com/actions/setup-python/blob/main/LICENSE) | Selects tested Python versions in GitHub Actions. |

## Data and services

- The repository has no research dataset. Its two synthetic `.eml` fixtures use example domains and a documentation IP address.
- The detector uses no external analysis API, telemetry, reputation service, or externally hosted UI asset.
- GitHub hosts the private repository and runs CI; it is not part of the local detection process.

## Privacy and ethics

Use authorized, minimal, preferably synthetic inputs. Local processing does not eliminate exposure through terminal history, browser state, screenshots, or the computer itself. False positives and false negatives require human interpretation; the English substring rules are not evidence of broad language coverage or fairness. See [limitations and responsible use](LIMITATIONS.md).

The [ACM Code of Ethics](https://www.acm.org/code-of-ethics), especially privacy (1.6) and confidentiality (1.7), provides context for these practices. This is a design interpretation, not a claim of institutional approval or formal compliance. Preserve third-party notices and do not introduce proprietary datasets, private emails, or copied code without appropriate permission.

## Pending team decisions

- **Project license:** no `LICENSE` has been selected. The component licenses above do not license the team's own work. Decide before public redistribution.
- **Academic acknowledgment:** confirm author roles and the instructor's required AI disclosure.
- **Future evaluation:** agree on data authorization and retention before using non-synthetic messages.

Earlier recovery reports and detailed verification history remain available in Git history. They are not current setup instructions.

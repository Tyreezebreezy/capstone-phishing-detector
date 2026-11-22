# Provenance, AI Assistance, and Ethics

This document records components and assistance verified during the repository audit. It should be reviewed by the project team before academic submission.

## Third-party components

The runtime application has no installed third-party Python or JavaScript dependencies.

| Component | Official source | License | Project use |
|---|---|---|---|
| Python and Python standard library | [Python Software Foundation](https://www.python.org/) | [PSF License and historical license stack](https://docs.python.org/3/license.html) | Runs the detector, email parser, URL parser, HTTP server, tests, and command-line interface. |
| Mermaid / Mermaid CLI 11.12.0 | [mermaid-js/mermaid](https://github.com/mermaid-js/mermaid) and [mermaid-js/mermaid-cli](https://github.com/mermaid-js/mermaid-cli) | MIT | Editable documentation diagrams and generated SVG/PNG exports; used as a temporary documentation tool and not loaded by the detector at runtime. |
| `actions/checkout` | [GitHub action repository](https://github.com/actions/checkout) | [MIT License](https://github.com/actions/checkout/blob/main/LICENSE) | Checks out repository content in the included GitHub Actions workflow. |
| `actions/setup-python` | [GitHub action repository](https://github.com/actions/setup-python) | [MIT License](https://github.com/actions/setup-python/blob/main/LICENSE) | Selects tested Python versions in GitHub Actions. |

### Data, services, and samples

- The repository contains no research dataset.
- The two `.eml` samples are synthetic project fixtures using reserved example domains and a documentation IP address.
- The application does not call cloud services, reputation providers, analytics, advertising, or external APIs.
- The UI bundles its own HTML, CSS, and JavaScript and loads no external assets.
- GitHub Actions is relevant only when the repository is published and the workflow runs on GitHub.

### Project license status

No `LICENSE` file was present, and no project license was selected during this handoff. The licenses above cover their respective third-party components; they do not automatically license the team's original code or documentation. The group should choose a project license with instructor/team approval before public redistribution.

## AI assistance disclosure

Verified ChatGPT/Codex contributions include:

- reviewing the supplied Python detector, tests, samples, README, and local UI;
- designing and generating the standard-library web-server layer and plain web interface;
- generating UI/backend integration tests;
- generating and refining Markdown technical documentation;
- generating Mermaid diagram source and rendering/visual-validation support;
- running syntax checks, automated tests, and browser-based interface checks; and
- identifying documentation boundaries, repository-readiness gaps, and limitations.

AI assistance does not replace authorship review. The student team should:

1. read every source and documentation change;
2. confirm that the diagrams match the code;
3. rerun the tests in the team's environment;
4. correct any course-specific wording or attribution requirement; and
5. disclose AI use according to FIU course and instructor policy.

This handoff does not claim that the team approved every AI-generated decision, prompt, or sentence. It records work performed in the Codex sessions represented by the deliverables. Team review and any future dataset evaluation remain unverified until the team completes them. The owner authorized publication to the private Tyreezebreezy/capstone-phishing-detector repository.

## Ethical issues

### Privacy and confidentiality

Email messages can contain names, addresses, authentication codes, account information, health information, school records, or business communications. Even a demonstration should use only authorized and necessary content. Synthetic messages are preferable.

The local-only design reduces disclosure risk:

- the server binds to `127.0.0.1`;
- inputs are processed in memory;
- the application has no database or telemetry;
- message bodies and submitted URLs are not written to the server request log; and
- the application makes no external analysis request.

Local processing does not eliminate every risk. The computer, terminal history, browser state, screenshots, copied text, or future modifications could still expose data. Users remain responsible for authorization, access controls, and deletion of demonstration artifacts.

### False positives and false negatives

A false positive can cause unnecessary concern or unfairly characterize a legitimate sender. A false negative can create false reassurance and contribute to unsafe action. The UI therefore presents findings and a heuristic label, not a definitive verdict. Results should support human review, not replace it.

### Safe handling of suspicious material

The program parses links as strings and does not visit or resolve them. It skips attachment parts rather than opening them. Demonstrations should use reserved synthetic domains and addresses; live phishing samples add risk without being necessary for the capstone proof of concept.

### Fairness and language coverage

The message rules are fixed English-language substring lists. They may behave differently across languages, dialects, writing styles, cultural contexts, and accessibility tools. Presenting this detector as broadly fair or language-neutral would be unsupported.

### Attribution and licensing

Team members must preserve third-party notices, distinguish external licenses from the project's license, and avoid copying proprietary datasets, emails, or source code without permission. AI-generated material also requires human provenance and citation review.

## Professional ethics

The [ACM Code of Ethics and Professional Conduct](https://www.acm.org/code-of-ethics) includes Principle 1.6, “Respect privacy.” The official commentary emphasizes legitimate purpose, minimal collection, transparency, appropriate retention, and protection against unauthorized access or disclosure.

Applied to this project, that principle supports local processing, no database, no telemetry, synthetic demonstrations, a 2 MB input limit, and explicit documentation of what is and is not retained. This is the handoff author's interpretation of how the ACM principle informs the design; it is not evidence of a formal team decision or institutional compliance determination.

Principle 1.7, confidentiality, is also relevant when a user has authorized access to an email but should not disclose it to classmates, external services, or a public repository.

## Items requiring team confirmation

- The final project license.
- The exact names/roles to include in academic attribution.
- The instructor's required wording and placement for AI disclosure.
- Verified classmate GitHub usernames for invitations; the owner has required private visibility.
- Retention/deletion expectations for demonstration inputs and screenshots.
- Whether any non-synthetic data will be used in future evaluation and what approval is required.

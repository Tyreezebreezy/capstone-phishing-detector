# System Architecture and Diagram Package

All diagrams describe the audited implementation. Editable sources are in [`diagrams/`](diagrams/); rendered SVG and PNG exports are in [`diagrams/rendered/`](diagrams/rendered/).

The shared visual language uses teal for application processes, navy text, neutral data movement, and amber notes. No diagram introduces a database, cloud service, reputation API, mailbox connection, attachment engine, or machine-learning component.

## Presentation overview

This simplified view is intended for an audience unfamiliar with the code.

```mermaid
flowchart TD
    Input["1. Student enters a URL<br/>or email"] --> Inspect["2. Program checks<br/>explainable warning signs"]
    Inspect --> Score["3. Rule weights create<br/>a heuristic score"]
    Score --> Explain["4. Program shows<br/>risk label + reasons"]
    Safety["Everything stays local.<br/>Links and attachments are not opened."]
    Safety -. safety boundary .-> Inspect
```

Source: [`simplified-overview.mmd`](diagrams/simplified-overview.mmd)

## A. High-level system architecture

The direct URL path and email path converge at the URL analyzer and scoring/classification logic. Results return to the same local interface.

```mermaid
flowchart LR
    User([User]) --> UI["Local interface<br/>Web UI or CLI"]
    UI -->|One URL| URLInput[URL input]
    UI -->|Pasted text or .eml bytes| EmailInput[Email input]
    URLInput --> URLAnalyzer[URL analyzer]
    EmailInput --> EmailParser[Email parser]
    EmailParser --> TextRules[Email text rules]
    EmailParser --> URLExtract[URL extraction]
    URLExtract --> URLAnalyzer
    URLAnalyzer --> URLRules[URL structural rules]
    URLRules --> Score[Heuristic scoring]
    TextRules --> Score
    Score --> Classify[Risk classification]
    Classify --> Results["Results<br/>label, score, findings, extracted URLs"]
    Results --> User
    note["Local processing only<br/>No link visits, DNS, APIs, database,<br/>or attachment execution"]
    note -. constraint .-> URLAnalyzer
    note -. constraint .-> EmailParser
```

Source: [`system-architecture.mmd`](diagrams/system-architecture.mmd)

## B. URL detection flowchart

Invalid URL input is handled before rule scoring. Valid URLs pass through the five implemented structural rules.

```mermaid
flowchart TD
    A([Receive URL text]) --> B[Trim surrounding whitespace]
    B --> C{"Empty, whitespace inside,<br/>or control characters?"}
    C -->|Yes| Invalid["INVALID INPUT<br/>score 0 + parse finding"]
    C -->|No| D[Add https scheme if omitted]
    D --> E[Parse scheme, hostname, port, path, user info]
    E --> F{"HTTP or HTTPS,<br/>valid hostname and port?"}
    F -->|No| Invalid
    F -->|Yes| G[Normalize hostname with IDNA]
    G --> H["Run URL rules<br/>HTTP +1<br/>user info before @ +2<br/>numeric IP host +2<br/>punycode +1<br/>login/verification path term +1"]
    H --> I[Collect every triggered finding]
    I --> J[Sum heuristic score]
    J --> K{"Score"}
    K -->|0| Safe[NO INDICATORS FOUND]
    K -->|1 to 2| Review[REVIEW RECOMMENDED]
    K -->|3 or more| High[HIGH RISK]
    Safe --> Result[Return input, score, label, findings]
    Review --> Result
    High --> Result
    Invalid --> Result
```

Source: [`url-analysis.mmd`](diagrams/url-analysis.mmd)

## C. Email detection flowchart

The sender header is displayed but not authenticated or scored. The parser skips MIME parts marked as attachments and analyzes only supported text parts.

```mermaid
flowchart TD
    A([Receive email input]) --> B{"Input mode"}
    B -->|Pasted text| C[Use text as plain body]
    B -->|.eml bytes| D{"Larger than 2 MB?"}
    D -->|Yes| E[Reject with validation error]
    D -->|No| F[Parse message with Python email parser]
    F --> G[Read Subject and From for display]
    F --> H[Collect text/plain and text/html parts]
    H --> I[Skip parts marked as attachments]
    C --> J[Build analysis text]
    G --> J
    I --> J
    J --> K["Run email rules<br/>urgency/account threat +1<br/>sensitive-information request +2<br/>visible-link host mismatch +3"]
    J --> L["Extract unique HTTP(S) URLs"]
    L --> M[Analyze first 20 URLs with URL analyzer]
    M --> N[Add highest embedded URL score]
    K --> O[Combine score and findings]
    N --> O
    O --> P{"Combined score"}
    P -->|0| Q[NO INDICATORS FOUND]
    P -->|1 to 2| R[REVIEW RECOMMENDED]
    P -->|3 or more| S[HIGH RISK]
    Q --> T["Return label, score, findings,<br/>subject, sender, URL results and total"]
    R --> T
    S --> T
```

Source: [`email-analysis.mmd`](diagrams/email-analysis.mmd)

## D1. Data flow — Level 0 context

```mermaid
flowchart LR
    User([User]) -->|URL, pasted message, or .eml file| System[Local phishing detector]
    System -->|Classification, heuristic score, findings, extracted URL results| User
    LocalNote["Processing boundary: the user's computer<br/>Input is not sent to an external service or retained in a database"]
    LocalNote -. describes .-> System
```

Source: [`data-flow-level-0.mmd`](diagrams/data-flow-level-0.mmd)

## D2. Data flow — Level 1

Input is held only as needed in process memory. The project has no persistence layer. The server's request log contains method, path, status, and client address—not submitted message bodies.

```mermaid
flowchart TD
    UserIn([User input]) -->|URL text| P1[1. Validate and parse URL]
    UserIn -->|Pasted email text| P2[2. Prepare email content]
    UserIn -->|.eml bytes| P3[3. Parse .eml message]
    P3 -->|Subject, From, plain text, HTML text| P2
    P2 -->|Visible text| P4[4. Apply email wording rules]
    P2 -->|"Unique HTTP(S) URLs"| P5[5. Analyze embedded URLs]
    P1 --> P6[6. Score and classify URL]
    P5 --> P6
    P4 --> P7[7. Combine email score and findings]
    P6 -->|Individual URL results; highest URL score| P7
    P6 -->|Direct URL result| Output[8. Format result]
    P7 -->|Email result| Output
    Output -->|Label, score, findings, URL details| UserOut([User result])
    Memory["Ephemeral process memory only<br/>No database or external transmission"]
    Memory -. boundary .-> P1
    Memory -. boundary .-> P2
```

Source: [`data-flow-level-1.mmd`](diagrams/data-flow-level-1.mmd)

## E. Sequence diagram

The “local interface” participant represents either the web UI/server pair or the CLI. Both call the same detection engine.

```mermaid
sequenceDiagram
    autonumber
    actor User
    participant UI as Local interface
    participant Parser as Email parser
    participant URL as URL analyzer
    participant Rules as Detection rules
    participant Score as Scoring/classification
    alt Direct URL scan
        User->>UI: Submit one URL
        UI->>URL: analyze_url(text)
        URL->>Rules: Evaluate URL structure
        Rules->>Score: URL findings and weights
        Score-->>UI: Label, score, findings
    else Pasted email scan
        User->>UI: Submit message text
        UI->>Parser: analyze_email_content(text)
        Parser->>Rules: Evaluate wording and HTML links
        Parser->>URL: Analyze extracted URLs (max 20)
        URL->>Rules: Evaluate each URL
        Rules->>Score: Email findings + highest URL score
        Score-->>UI: Email result and URL details
    else .eml scan
        User->>UI: Submit .eml bytes
        UI->>Parser: analyze_email_file(bytes)
        Parser->>Parser: Parse headers and body, skip attachments
        Parser->>Rules: Evaluate wording and HTML links
        Parser->>URL: Analyze extracted URLs (max 20)
        Rules->>Score: Findings and weights
        Score-->>UI: Email result and URL details
    end
    UI-->>User: Render escaped, non-clickable explanations
```

Source: [`sequence.mmd`](diagrams/sequence.mmd)

## F. Scoring and classification logic

```mermaid
flowchart TD
    A([Analysis request]) --> B{"Valid URL input<br/>or valid email request?"}
    B -->|No| Invalid["INVALID INPUT or validation error<br/>URL invalid result uses score 0"]
    B -->|Yes| C[Sum implemented rule weights]
    C --> D{"Heuristic score"}
    D -->|0| Safe[NO INDICATORS FOUND]
    D -->|1 or 2| Review[REVIEW RECOMMENDED]
    D -->|3 or more| High[HIGH RISK]
    Safe --> Warning["Score is not a probability.<br/>No indicators does not mean safe."]
    Review --> Warning
    High --> Warning
    Invalid --> Warning
```

Source: [`scoring.mmd`](diagrams/scoring.mmd)

## G. Repository component diagram

```mermaid
flowchart TD
    Repo[capstone-phishing-detector]
    Repo --> Engine["phishing_detector.py<br/>rules, parsing, scoring, CLI"]
    Repo --> Server["ui_server.py<br/>localhost static/API server"]
    Server --> Web["web/<br/>HTML, CSS, JavaScript UI"]
    Server --> Engine
    Repo --> Unit["test_detector.py<br/>20 engine tests"]
    Unit --> Engine
    Repo --> Integration["test_ui_server.py<br/>10 integration tests"]
    Integration --> Server
    Repo --> Samples["samples/<br/>synthetic .eml fixtures"]
    Unit --> Samples
    Integration --> Samples
    Repo --> Docs["README.md, CONTRIBUTING.md, docs/"]
    Docs --> Diagrams["docs/diagrams/<br/>Mermaid sources + rendered exports"]
    Repo --> CI[".github/workflows/tests.yml<br/>automated unittest run"]
    CI --> Unit
    CI --> Integration
    Repo --> Screens["screenshots/<br/>verified UI views"]
```

Source: [`components.mmd`](diagrams/components.mmd)

## H. Testing and validation workflow

Passing tests demonstrate agreement with selected expected cases. They are not an independent measurement of phishing-detection quality.

```mermaid
flowchart TD
    Source[Source or documentation change] --> Local[Run local unit and integration tests]
    Local --> Decision{All tests pass?}
    Decision -->|No| Review[Review failure and implementation]
    Review --> Fix[Targeted correction + regression test]
    Fix --> Local
    Decision -->|Yes| Human[Human review of behavior, docs, and diagrams]
    Human --> Commit[Git commit / pull request]
    Commit --> CI[GitHub Actions runs test suite]
    CI --> CIDecision{CI passes?}
    CIDecision -->|No| Review
    CIDecision -->|Yes| Ready[Ready for team review or merge]
    Accuracy["Important: passing tests demonstrates expected coded behavior,<br/>not real-world phishing-detection accuracy"]
    Ready -. does not establish .-> Accuracy
```

Source: [`testing-workflow.mmd`](diagrams/testing-workflow.mmd)

## Export and verification

Mermaid sources are intentionally kept separate so they remain editable and can be reviewed in pull requests. All ten sources were rendered with Mermaid CLI 11.12.0 to SVG and PNG in `docs/diagrams/rendered/`. The rendered PNGs were visually inspected for clipped text, overlapping labels, incorrect arrows, and inconsistent source/export pairs; three layouts were revised and re-rendered to improve presentation legibility.

During Windows recovery on 2026-11-22, the component diagram was corrected to show 10 integration tests in the embedded diagram, `.mmd`, and SVG. Its PNG was regenerated from the corrected SVG in Chromium; the other nine exports were preserved. All ten embedded diagrams also loaded in the private GitHub preview.

Suggested rendering commands:

```bash
npx -y @mermaid-js/mermaid-cli -i docs/diagrams/system-architecture.mmd -o docs/diagrams/rendered/system-architecture.svg -b transparent
npx -y @mermaid-js/mermaid-cli -i docs/diagrams/system-architecture.mmd -o docs/diagrams/rendered/system-architecture.png -b white -w 1800
```

Repeat for each `.mmd` source. Mermaid is a documentation/build tool here; the phishing detector does not require it at runtime.

## Suggested capstone presentation order

1. **Simplified overview** — establish the four-step story and local safety boundary.
2. **High-level system architecture** — show how URL and email paths share the URL analyzer and scoring logic.
3. **Scoring and classification** — explain the labels, exact thresholds, and why the score is not a probability.

Use the URL or email flowchart only if the professor asks for implementation detail. Use the testing workflow to answer questions about validation versus real-world accuracy.

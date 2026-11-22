# Running the Capstone 1 phishing detector on your own computer

## What is portable?
This repository contains everything needed to run the **same local phishing detector** on Windows, macOS, or Linux. It uses only Python's standard library and the bundled HTML/CSS/JavaScript interface, so you do **not** need `pip install`, an API key, a database, or an internet connection after you have downloaded the repository and installed Python.

**Prerequisite on each computer: Python 3.10 or newer.** Python may not already be installed. Different operating systems need their own Python installation. A web browser is also required.

The interface is **not** a standalone `index.html` file you open with `file://`. It talks to a Python backend. `launch.py` runs that backend on `127.0.0.1` on **your own machine**, and opens your browser automatically at `http://127.0.0.1:8765`. This does **not** require teammates to be on the same network, share a server, or be together in person. Each teammate runs their own local copy.

## Windows
1. Download the ZIP from the private GitHub repository (**Code > Download ZIP**) or clone the repository.
2. Extract the ZIP (if downloaded).
3. Install Python 3.10+ if necessary. Verify with `py -3 --version` or `python --version` in PowerShell.
4. Double-click `START_WINDOWS.cmd` in the extracted project folder. A terminal window stays open while the app is running.
5. If your browser does not open automatically, visit `http://127.0.0.1:8765` manually.
6. Stop the server by pressing `Ctrl+C` in the terminal window.

Run tests by double-clicking `TEST_WINDOWS.cmd` or entering `python -m unittest -v`.

## macOS or Linux
1. Download or clone the repository.
2. Install Python 3.10+ if necessary. Verify using `python3 --version`.
3. In a terminal opened in the project folder, run `sh START_MAC_LINUX.sh` (or `python3 launch.py`).
4. If needed, visit `http://127.0.0.1:8765` manually.
5. Stop with `Ctrl+C`.

Run tests with `sh TEST_MAC_LINUX.sh` or `python3 -m unittest -v`.

## Git clone (any platform with Git)
```bash
git clone https://github.com/Tyreezebreezy/capstone-phishing-detector.git
cd capstone-phishing-detector
```
Group members must accept the invitation to the **private** repository and authenticate to GitHub. With GitHub CLI installed, run `gh auth login` and `gh auth setup-git` before cloning. Alternatively use Git Credential Manager or your configured SSH credentials. Never put tokens in clone URLs or project files.

After cloning, run `python -m unittest discover -v`, then use your OS launcher above. To contribute, create a branch, make a small change, rerun tests, push the branch, and open a pull request; see [CONTRIBUTING.md](CONTRIBUTING.md).

## Offline use and privacy
- After cloning/downloading and installing Python, the tool runs without internet.
- Submitted emails and URLs are analyzed locally; the tool does not fetch sites or email services.
- A browser is used only as the interface; it communicates with the Python server on the same computer.
- Do not scan real private messages without permission; the capstone demo should use synthetic examples.

## Troubleshooting
- `Python not found`: install Python 3.10+ and reopen your terminal.
- `Address already in use`: close an earlier app/server instance or use `python launch.py --port 8766` and open the printed address.
- Browser does not open: copy the printed local address into any modern browser.
- `file://` or double-clicking `web/index.html` does not work as a complete app: launch the backend with the scripts above.
- Running the application directly from inside a ZIP may fail: **extract it first**.

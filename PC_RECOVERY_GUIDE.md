> Historical recovery procedure. The working repository is now [Tyreezebreezy/capstone-phishing-detector](https://github.com/Tyreezebreezy/capstone-phishing-detector) (private). New teammates should follow [TEAMMATE_SETUP.md](TEAMMATE_SETUP.md); do not create another repository.

# PC Recovery Guide — Capstone 1 Phishing Detector

**Status:** This package was reconstructed from the complete project archives supplied in ChatGPT and tested in a separate environment on 2026-11-22. This is not a scan of the user's new Windows PC. The previous local Python detection engine is preserved byte-for-byte.

## A. Recover onto your Windows PC

1. Download `Capstone1_Phishing_Detector_Codex_Ready_2026-11-22.zip`.
2. In Windows File Explorer, right-click the ZIP and choose **Extract All**. Put it somewhere easy to find, such as `Documents\Projects`.
3. Open the extracted `capstone-phishing-detector` folder. You should see `phishing_detector.py`, `ui_server.py`, `web`, `docs`, `samples`, `TEST_WINDOWS.cmd`, and `RUN_UI_WINDOWS.cmd`.
4. Double-click `TEST_WINDOWS.cmd`. The expected result is **30 passing tests**. If it fails, preserve the error output rather than replacing source files indiscriminately.
5. Double-click `RUN_UI_WINDOWS.cmd`. Open **http://127.0.0.1:8765** in the browser. Keep the terminal window open while using the app.
6. In **URL Scanner**, enter `http://192.0.2.10/login` and expect **HIGH RISK, score 4**. Enter `https://example.org` and expect **NO INDICATORS FOUND, score 0**.
7. In **Email Scanner**, paste `Urgent: enter your password at http://192.0.2.10/login` and expect a **HIGH RISK** result containing an extracted URL. Use `samples/suspicious_email.eml` to test upload.
8. Verify that **Reset** clears input and results. Do not paste actual private messages into demonstration screenshots.

> This software does not visit a submitted website; it checks URL text only. There are no external runtime dependencies, APIs, passwords, or services to restore. It is a demonstration, not a verified security product.

## B. Check whether an earlier copy or GitHub repository exists

On Windows, check your usual project directories (your Desktop, Documents, Downloads, and Codex output folders). Look for `ui_server.py`, `phishing_detector.py`, or `capstone_phishing_mwm_v02`. Avoid deleting a different version until its changes have been compared.

If Git and GitHub CLI are installed, open PowerShell in the recovered project folder:

```powershell
git --version
gh --version
gh auth status
gh api user --jq .login
```

After you confirm the account name, check for a private repository:

```powershell
gh repo view YOUR_GITHUB_USERNAME/capstone-phishing-detector --json nameWithOwner,isPrivate,url
```

If it already exists, **clone it into a separate directory**, inspect its contents, and merge the recovered version on a branch; **never force-push or overwrite classmates' work**.

## C. Publish only when it does not already exist

With the authenticated **correct personal GitHub account**, and only after tests pass, open PowerShell inside the extracted `capstone-phishing-detector` folder:

```powershell
git init -b main
git add .
git commit -m "Restore tested Capstone 1 phishing detector"
gh auth setup-git
gh repo create capstone-phishing-detector --private --source=. --remote=origin --push
```

**Do not run `git init` or `gh repo create` if this project folder already has a `.git` directory or the target repository exists.** Use the repository's actual clone and a review branch instead.

Then verify (replace `YOUR_GITHUB_USERNAME` with the username returned by `gh api user --jq .login`):

```powershell
gh repo view YOUR_GITHUB_USERNAME/capstone-phishing-detector --json nameWithOwner,isPrivate,url
gh run list -R YOUR_GITHUB_USERNAME/capstone-phishing-detector --limit 5
```

Only claim publication succeeded when the repository is visible **to the signed-in account**, shows `isPrivate: true`, and the code is present. Only claim GitHub Actions passed after a green workflow run is visible. Invite teammates from GitHub **Settings → Collaborators → Add people**, using their GitHub usernames.

## D. Troubleshooting

- **`python` or `py` not recognized:** Install Python 3.10+ for Windows; reopen the terminal.
- **`git` or `gh` not recognized:** Install Git for Windows and/or GitHub CLI, then reopen the terminal.
- **Test fails with a loopback/network permission error:** Confirm localhost traffic is allowed by local security controls. Do not disable firewall settings globally.
- **Browser says connection refused:** Keep the `RUN_UI_WINDOWS.cmd` terminal running; look for an error about port 8765. Stop a stale instance or use `python ui_server.py --port 8766` and open port 8766.
- **ZIP downloaded but looks empty:** Use Windows **Extract All**. The source lives inside one `capstone-phishing-detector` folder.
- **GitHub repository appears missing:** Check that `gh auth status` reports the intended account. Private repositories are visible only to the owner and explicitly invited collaborators.
- **Old laptop has extra work:** Compare by Git commit or source files before replacing anything; this recovered package contains only the attached archive history, not the unseen laptop drive.

## E. What is deliberately not rebuilt

No database, paid API, accounts, ML model, attachment scanner, or third-party service is needed for the minimum working model. The project is not yet hosted as a public website: group members clone the private repo and run it locally.

## F. After the recovery

Once the private repository, collaborator access, and tests are verified, the next assignment is FIU Capstone 1 Week 13 Provenance and Ethics. Verify actual group-used libraries, code/data provenance, AI-assisted work, and ethics decisions with the group before submitting.

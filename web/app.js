"use strict";

const MAX_EMAIL_BYTES = 2_000_000;
const tabs = {
  url: document.querySelector("#url-tab"),
  email: document.querySelector("#email-tab"),
};
const panels = {
  url: document.querySelector("#url-panel"),
  email: document.querySelector("#email-panel"),
};
const results = document.querySelector("#results");
const workingStatus = document.querySelector("#working-status");
const urlForm = document.querySelector("#url-form");
const emailForm = document.querySelector("#email-form");
const urlInput = document.querySelector("#url-input");
const emailInput = document.querySelector("#email-input");
const emailFile = document.querySelector("#email-file");
const fileStatus = document.querySelector("#file-status");
const urlError = document.querySelector("#url-error");
const emailError = document.querySelector("#email-error");

function setMode(mode) {
  for (const name of Object.keys(tabs)) {
    const active = name === mode;
    tabs[name].classList.toggle("is-active", active);
    tabs[name].setAttribute("aria-selected", String(active));
    panels[name].hidden = !active;
  }
  clearMessages();
  results.hidden = true;
  (mode === "url" ? urlInput : emailInput).focus();
}

function clearMessages() {
  urlError.textContent = "";
  emailError.textContent = "";
  workingStatus.textContent = "";
}

function resetAll() {
  urlForm.reset();
  emailForm.reset();
  fileStatus.textContent = "No file selected";
  clearMessages();
  results.replaceChildren();
  results.hidden = true;
  const activeMode = tabs.url.classList.contains("is-active") ? "url" : "email";
  (activeMode === "url" ? urlInput : emailInput).focus();
}

function setBusy(form, busy, message) {
  for (const control of form.querySelectorAll("button, input, textarea")) {
    control.disabled = busy;
  }
  workingStatus.textContent = busy ? message : "";
}

async function requestAnalysis(url, options) {
  const response = await fetch(url, options);
  let payload;
  try {
    payload = await response.json();
  } catch {
    throw new Error("The local server returned an unreadable response");
  }
  if (!response.ok) {
    throw new Error(payload.error || "The request could not be analyzed");
  }
  return payload.result;
}

function riskClass(classification) {
  if (classification === "HIGH RISK" || classification === "INVALID INPUT") return "risk-high";
  if (classification === "REVIEW RECOMMENDED") return "risk-review";
  return "risk-safe";
}

function element(tag, className, text) {
  const node = document.createElement(tag);
  if (className) node.className = className;
  if (text !== undefined) node.textContent = text;
  return node;
}

function defang(value) {
  return value.replace(/^https:\/\//i, "hxxps[:]//").replace(/^http:\/\//i, "hxxp[:]//");
}

function findingsBlock(items) {
  const section = element("section", "result-section");
  section.append(element("h3", "", "Triggered findings"));
  if (!items.length) {
    section.append(element("p", "empty-findings", "No heuristic findings were triggered."));
    return section;
  }
  const list = element("ul", "finding-list");
  for (const finding of items) list.append(element("li", "", finding));
  section.append(list);
  return section;
}

function urlResultsBlock(items, total) {
  const section = element("section", "result-section");
  section.append(element("h3", "", `Extracted URLs (${items.length} of ${total} inspected)`));
  if (!items.length) {
    section.append(element("p", "empty-findings", "No URLs were extracted from this message."));
    return section;
  }
  const list = element("div", "url-list");
  for (const item of items) {
    const row = element("article", "url-row");
    const header = element("div", "url-row-header");
    header.append(element("span", "url-value", defang(item.input)));
    header.append(element("span", "url-classification", item.classification));
    row.append(header);
    if (item.findings.length) {
      const findings = element("ul", "");
      for (const finding of item.findings) findings.append(element("li", "", finding));
      row.append(findings);
    } else {
      row.append(element("p", "", "No structural URL findings."));
    }
    list.append(row);
  }
  section.append(list);
  return section;
}

function renderResult(result) {
  results.replaceChildren();
  results.className = `results ${riskClass(result.classification)}`;

  const heading = element("div", "result-heading");
  const titleWrap = element("div", "");
  const title = element("h2", "classification", result.classification);
  title.id = "results-title";
  titleWrap.append(title);
  const score = element("div", "score-block");
  score.append(element("span", "", "Heuristic score"));
  score.append(element("strong", "", String(result.score)));
  heading.append(titleWrap, score);
  results.append(heading);

  if (result.type === "email") {
    const meta = element("div", "result-meta");
    const subject = element("div", "");
    subject.append(element("strong", "", "Subject"), element("span", "", result.subject));
    const sender = element("div", "");
    sender.append(element("strong", "", "Sender"), element("span", "", result.sender));
    meta.append(subject, sender);
    results.append(meta);
  }

  results.append(findingsBlock(result.findings));
  if (result.urls) results.append(urlResultsBlock(result.urls, result.urls_total));
  results.hidden = false;
  results.scrollIntoView({ behavior: "smooth", block: "start" });
}

tabs.url.addEventListener("click", () => setMode("url"));
tabs.email.addEventListener("click", () => setMode("email"));
for (const button of document.querySelectorAll(".reset")) button.addEventListener("click", resetAll);

emailFile.addEventListener("change", () => {
  const file = emailFile.files[0];
  fileStatus.textContent = file ? `${file.name} — ${(file.size / 1024).toFixed(1)} KB selected` : "No file selected";
  emailError.textContent = "";
});

urlForm.addEventListener("submit", async (event) => {
  event.preventDefault();
  clearMessages();
  const value = urlInput.value;
  if (!value.trim()) {
    urlError.textContent = "Enter a URL to analyze.";
    urlInput.focus();
    return;
  }
  setBusy(urlForm, true, "Analyzing URL locally…");
  try {
    const result = await requestAnalysis("/api/analyze-url", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ url: value }),
    });
    renderResult(result);
  } catch (error) {
    urlError.textContent = error.message;
  } finally {
    setBusy(urlForm, false, "");
  }
});

emailForm.addEventListener("submit", async (event) => {
  event.preventDefault();
  clearMessages();
  const file = emailFile.files[0];
  const text = emailInput.value;
  if (!file && !text.trim()) {
    emailError.textContent = "Paste an email message or choose an .eml file.";
    emailInput.focus();
    return;
  }
  if (file && !file.name.toLowerCase().endsWith(".eml")) {
    emailError.textContent = "Choose a file with the .eml extension.";
    emailFile.focus();
    return;
  }
  if (file && file.size > MAX_EMAIL_BYTES) {
    emailError.textContent = "Email exceeds the 2 MB prototype limit.";
    emailFile.focus();
    return;
  }

  setBusy(emailForm, true, "Analyzing email locally…");
  try {
    const result = file
      ? await requestAnalysis("/api/analyze-email-file", {
          method: "POST",
          headers: { "Content-Type": "application/octet-stream" },
          body: await file.arrayBuffer(),
        })
      : await requestAnalysis("/api/analyze-email", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ text }),
        });
    renderResult(result);
  } catch (error) {
    emailError.textContent = error.message;
  } finally {
    setBusy(emailForm, false, "");
  }
});

---
name: gas-medical-webapp-generator
description: Use when building a Google Apps Script (GAS) doctor interactive web application connected to Google Sheets (for master log & transaction audit trail) and Google Docs/Word/PDF (for medical document generation). Covers deployment, access levels, passcode gating, schema evolution, and the UI patterns that make structured clinical forms fast enough that physicians actually use them.
---

# GAS Medical WebApp Generator

## Overview

Build interactive clinical web applications for physicians on Google Apps Script. Three tiers:

1. **Interactive Web App** — HTML/JS frontend with structured option matrices, numeric blanks, and real-time text synthesis.
2. **Google Sheets Master Log** — transactional audit trail (operator, timestamp, patient code, findings, document links).
3. **Google Docs / Word / PDF** — formal documents generated on save, with direct export URLs.

## When to Use

- Clinical examination reporting tools (echocardiography, sonography, endoscopy, radiology, EKG).
- Admission notes / H&P and other structured clinical documentation.
- Any tool needing an audit log in Sheets plus downloadable formal reports.
- Zero-cost cloud deployment for a small medical team via `clasp`.

---

## Architecture

```
[ Frontend: index.html ] --google.script.run--> [ Backend: Code.gs ]
                                                       |
                     +---------------------------------+---------------------------------+
                     |                                                                   |
       [ Google Sheets: Master_* tabs ]                          [ Drive folder: generated Docs ]
                                                                              |
                                                        +---------------------+---------------------+
                                                        |                                           |
                                              /export?format=pdf                        /export?format=docx
```

---

## Non-negotiables

These come from real failures. Violating any of them costs a redeploy or a data migration.

### 1. Pick the right access level — `ANYONE` does NOT mean anyone

| manifest value | who can actually open the link |
| :--- | :--- |
| `MYSELF` | only the deploying account |
| `ANYONE` | anyone **with a Google account**, after signing in to Google |
| `ANYONE_ANONYMOUS` | truly public — link only, no account needed |

If the requirement is "send the doctors a link and it just works", it is `ANYONE_ANONYMOUS`.
`ANYONE` returns a **302 to `accounts.google.com/ServiceLogin`**, which you will not notice from your own browser because you are already signed in. Verify with an unauthenticated fetch and check for a 302.

```json
{
  "timeZone": "Asia/Taipei",
  "dependencies": {},
  "exceptionLogging": "STACKDRIVER",
  "runtimeVersion": "V8",
  "webapp": {
    "executeAs": "USER_DEPLOYING",
    "access": "ANYONE_ANONYMOUS"
  },
  "oauthScopes": [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/documents",
    "https://www.googleapis.com/auth/drive",
    "https://www.googleapis.com/auth/script.external_request"
  ]
}
```

`executeAs: USER_DEPLOYING` means all Sheets/Docs writes run as the deployer, so anonymous users need no permissions of their own. Combine it with an in-app passcode (below) rather than leaving it open.

### 2. Always redeploy with `-i <deploymentId>`

`create-deployment` **creates** a deployment. Without `-i` every run mints a brand-new `/exec` URL and the link your users already have stays frozen on an old version. A project left like this accumulates dozens of dead deployments.

```bash
npx -y @google/clasp@latest push --force

# ⚠️ update the EXISTING url — never omit -i
npx -y @google/clasp@latest create-deployment \
  -i <existing-deployment-id> \
  -d "v6.1 description"

npx -y @google/clasp@latest list-deployments
```

Record the production deployment ID in the project's `CLAUDE.md` on day one.

### 3. Sheet schema is append-only

The `getOrCreateSheet()` pattern only writes headers when the tab is empty. Once a tab holds real rows, header order is frozen and `appendRow()` writes **by position**. Inserting a column in the middle silently shifts every historical row.

Add new columns at the **end** of the headers array, and update the read-side index map in the same commit.

### 4. Adding an OAuth scope breaks the live app until re-authorization

After introducing a service that needs a new scope, `/exec` stops serving the page and redirects to `script.google.com/home` until the project owner opens the editor, runs any function, and completes "Review permissions → Advanced → Allow".

`PropertiesService`, `CacheService`, `Utilities`, `Session`, `HtmlService` need **no** extra scope — build auth and session logic on those and the manifest never changes.

### 5. The first render must not depend on a server round-trip

If the UI waits for `google.script.run` before it will display anything, every backend failure becomes a white screen with an unreadable error. Render first, then ask the server what to do.

Also guard for the case where the page is not being served by Apps Script at all — a very common user error is double-clicking `index.html` inside the synced Drive folder, which opens the source file locally and leaves `google` undefined.

```javascript
function hasBackend() {
  return typeof google !== 'undefined' && google && google.script && google.script.run;
}

function server(fnName) {
  var args = Array.prototype.slice.call(arguments, 1);
  if (!hasBackend()) return Promise.reject(new Error(NOT_HOSTED_MSG));
  return new Promise(function (resolve, reject) {
    google.script.run.withSuccessHandler(resolve).withFailureHandler(reject)
      [fnName].apply(null, [session.token].concat(args));
  });
}
```

On boot: `bootApp()` unconditionally, then `getAuthConfig()` decides whether to raise a lock screen. If `hasBackend()` is false, render a banner naming the problem and linking the correct `/exec` URL.

---

## Backend patterns

### Spreadsheet handle with fallback

`SpreadsheetApp.getActiveSpreadsheet()` returns `null` in a standalone script. Never call it directly.

```javascript
function getSpreadsheet() {
  try {
    var ss = SpreadsheetApp.getActiveSpreadsheet();
    if (ss) return ss;
  } catch (e) {}
  return SpreadsheetApp.openById(SPREADSHEET_ID);
}
```

### Document creation and export URLs

```javascript
function getReportsFolder_(folderName) {
  var ssFile = DriveApp.getFileById(getSpreadsheet().getId());
  var parent = ssFile.getParents().hasNext() ? ssFile.getParents().next() : DriveApp.getRootFolder();
  var it = parent.getFoldersByName(folderName);
  return it.hasNext() ? it.next() : parent.createFolder(folderName);
}

function docLinks_(docId) {
  return {
    docId:   docId,
    docUrl:  'https://docs.google.com/document/d/' + docId + '/edit',
    pdfUrl:  'https://docs.google.com/document/d/' + docId + '/export?format=pdf',
    docxUrl: 'https://docs.google.com/document/d/' + docId + '/export?format=docx'
  };
}

function createReport(record, id, timestamp) {
  var folder = getReportsFolder_('臨床檢查報告_GoogleDocs');
  var doc = DocumentApp.create('報告_' + record.patientId + '_' +
    Utilities.formatDate(timestamp, 'Asia/Taipei', 'yyyyMMdd_HHmm'));
  var body = doc.getBody();
  body.setMarginTop(40).setMarginBottom(40).setMarginLeft(48).setMarginRight(48);

  // ... appendParagraph / appendTable sections ...

  doc.saveAndClose();
  DriveApp.getFileById(doc.getId()).moveTo(folder);   // modern API; not addFile + removeFile
  return docLinks_(doc.getId());
}
```

Generating export URLs by string is far faster and simpler than converting blobs through the Drive service.

### Text styling: `setForegroundColor`, never `setFontColor`

`setFontColor` is a **SpreadsheetApp `Range`** method. A DocumentApp `Paragraph` colours text with **`setForegroundColor`**. The names are close enough that the wrong one reads as correct, and the failure is invisible until someone presses Save:

```
TypeError: body.appendParagraph(...).setFontSize(...).setFontColor is not a function
```

Because report generation usually runs *before* the Sheets append, the whole save aborts — in the reference implementation this went undetected across two releases, so nothing had ever been saved successfully.

Do not blanket find-and-replace: the same file legitimately calls `Range.setFontColor` when styling sheet headers. Fix only the DocumentApp call sites.

Paragraph-level styling that does exist: `setFontSize`, `setBold`, `setItalic`, `setUnderline`, `setFontFamily`, `setForegroundColor`, `setBackgroundColor`, `setAlignment`, `setSpacingBefore/After`, `setIndentStart/End/FirstLine`, `setHeading`, `setLinkUrl`.

### Repeating page headers

For a letterhead that appears on every printed page, use a real header section rather than body paragraphs:

```javascript
var header = doc.getHeader() || doc.addHeader();   // addHeader() throws if one exists
header.clear();
var table = header.appendTable([['', '', '']]);
table.setBorderColor('#000000').setBorderWidth(1);
table.setColumnWidth(0, 215).setColumnWidth(1, 190).setColumnWidth(2, 105);
```

A fresh table cell already contains one empty paragraph — reuse it for the first line, or every cell starts with a blank row:

```javascript
var first = cell.getChild(0).asParagraph();
first.setText(lines[0]);
for (var i = 1; i < lines.length; i++) cell.appendParagraph(lines[i]);
```

DocumentApp cannot insert an auto-updating page-number field; a footer page number has to be static or omitted.

### Sheet tab bootstrap

```javascript
function getOrCreateSheet(ss, sheetName, headers) {
  var sheet = ss.getSheetByName(sheetName) || ss.insertSheet(sheetName);
  if (sheet.getLastRow() === 0) {
    sheet.appendRow(headers);
    sheet.getRange(1, 1, 1, headers.length)
      .setFontWeight('bold').setBackground('#1e293b').setFontColor('#f8fafc');
    sheet.setFrozenRows(1);
  }
  return sheet;
}
```

---

## Passcode gate (for `ANYONE_ANONYMOUS` deployments)

A public link needs a gate. This pattern needs no extra OAuth scope and no server-side session storage.

**Stateless signed token.** `CacheService` maxes out at 6 hours and can evict early, so storing sessions there logs people out at random. Sign the token instead and store nothing:

```javascript
var AUTH_ENABLED = false;   // master switch — see below

function sha256Hex_(str) {
  var bytes = Utilities.computeDigest(Utilities.DigestAlgorithm.SHA_256, str, Utilities.Charset.UTF_8);
  var hex = '';
  for (var i = 0; i < bytes.length; i++) hex += ('0' + (bytes[i] & 0xFF).toString(16)).slice(-2);
  return hex;
}

function issueToken_() {
  var exp = new Date().getTime() + SESSION_HOURS * 3600 * 1000;
  return exp + '.' + sha256Hex_(getSalt_() + '|' + exp + '|' + getPasscodeHash_());
}

function isValidToken_(token) {
  var parts = String(token || '').split('.');
  if (parts.length !== 2) return false;
  var exp = parseInt(parts[0], 10);
  if (!exp || exp < new Date().getTime()) return false;
  return sha256Hex_(getSalt_() + '|' + exp + '|' + getPasscodeHash_()) === parts[1];
}
```

Because the passcode hash is part of the signature, **changing the passcode invalidates every outstanding token automatically** — no session table to purge.

**Store the passcode as a salted hash in Script Properties**, never in source. Provide a `setAppPasscode()` function the owner runs once from the editor.

**Token-first convention.** Every client-callable function takes the token as its first argument and starts with the guard. The client wrapper injects it, so call sites stay clean.

```javascript
function authFail_(token) {
  if (!AUTH_ENABLED) return null;
  if (isValidToken_(token)) return null;
  return { status: 'auth_required', message: '登入已逾期，請重新輸入密碼。' };
}

function saveExamRecord(token, record) {
  var gate = authFail_(token);
  if (gate) return gate;
  ...
}
```

**Ship a master switch, not hardcoded auth.** Requirements like "turn the password off for now, we'll set it up later" are routine. With `AUTH_ENABLED` plus a `getAuthConfig()` endpoint the client reads on boot, that request is a one-line change instead of a refactor — and the whole implementation stays in place for when it comes back.

Add brute-force resistance with a `CacheService` failure counter (lock after N attempts per 15 min) and `Utilities.sleep(700)` on each failure. Cache eviction only resets the counter, which is harmless.

---

## Frontend patterns

### Generate repetitive UI from config objects

A clinical form has enormous repetition — 10 review-of-systems groups, 10 physical-exam systems, dozens of quick-fill chips. Hand-writing that HTML produces a file nobody can maintain. Drive it from arrays:

```javascript
var ROS_SYSTEMS = [
  ['resp', '呼吸 Respiratory', ['Cough', 'Sputum', 'Dyspnea', 'Hemoptysis', 'Wheezing']],
  ['cv',   '心血管 Cardiovascular', ['Chest pain', 'Palpitation', 'Orthopnea', 'Leg edema']]
  // ...
];
```

Adding a symptom becomes a one-line array edit.

### Protect hand-edited fields with a dirty flag

Auto-synthesised text must never overwrite what the physician typed. Track which outputs have been touched and skip them, with an explicit "regenerate" button to opt back in.

```javascript
var manualEdits = {};
function setIfAuto(id, value) {
  if (manualEdits[id]) return;
  var el = document.getElementById(id);
  if (el && value) el.value = value;
}
// input listener on each generated field: manualEdits[id] = true
```

Show the state in the UI ("3 fields locked from overwrite") so the behaviour is visible rather than mysterious.

### Pair every completeness section with a one-click escape

This is the difference between a thorough form and an abandoned one. Adding review-of-systems, family history, social history and a 10-system physical exam triples the typing unless each section ships with a bulk default:

- ROS → **"all negative"**, then click the positives (tri-state chips: 1st click `+`, 2nd `−`, 3rd clears)
- Physical exam → **"fill all normal"**, then edit the abnormal systems
- Past history → **"non-contributory"**
- Social history → **"denies smoking / alcohol / betel nut"**
- Labs → **"mark pending"**

Standard templates exist to provide breadth; `non-contributory` is what stops note bloat. Build both sides.

### Draft autosave

Clinical work gets interrupted constantly. Debounce-save the whole form to `localStorage` and restore on load. Wrap every `localStorage` call — some sandboxes block it.

```javascript
function lsGet(k) { try { return window.localStorage.getItem(k); } catch (e) { return null; } }
function lsSet(k, v) { try { window.localStorage.setItem(k, v); } catch (e) {} }
```

### Copy-to-clipboard beats every visual feature

Most physicians still have to paste into a hospital HIS. A one-click "copy full text" on the live preview is worth more than any amount of styling.

---

## Clinical content

Anchor structure and thresholds to published standards, and **write down the source and the year** — guidelines move.

| Domain | Anchor |
| :--- | :--- |
| Admission note / H&P | demographics → CC → HPI → PMH/PSH/meds/allergies → family & social → ROS → vitals & PE → labs → problem-based A&P |
| Imaging & exam reports | RSNA structured reporting: indication → technique → comparison → findings → impression |
| Echocardiography | ASE reporting standardization: indication, vitals, chambers, valves, pericardium, contrast/maneuvers, hemodynamics, comparison, summary |
| Colonoscopy | ASGE/ACG quality indicators — cecal intubation with photo documentation, bowel prep score, **withdrawal time ≥ 8 min (2024 update, was 6)**, resected lesions documented by size/shape/location/method |

Assessment and plan should be **problem-based**: each active problem carries its own plan, not one free-text box for diagnoses and another for orders.

Localise the social history. In Taiwan, betel nut is a required field alongside smoking and alcohol.

---

## Verification

GAS web apps resist automated checking: static fetches of `/exec` only return the outer shell because user content lives in a sandboxed `googleusercontent.com` iframe. Browser automation may also be unavailable. Do what can be done, then be explicit about what was not verified.

```bash
# per-<script>-block syntax check
node -e "const fs=require('fs');const s=fs.readFileSync('index.html','utf8');
[...s.matchAll(/<script>([\s\S]*?)<\/script>/g)].forEach((m,i)=>{
  try{new Function(m[1]);console.log('block',i+1,'OK')}catch(e){console.log('block',i+1,'ERR',e.message)}});"

# inline handlers resolve to defined functions; getElementById targets exist
node -e "const fs=require('fs');const s=fs.readFileSync('index.html','utf8');
const c=new Set([...s.matchAll(/on(?:click|change|input|keyup)=\"([\w\$]+)\(/g)].map(m=>m[1]));
const d=new Set([...s.matchAll(/function\s+([\w\$]+)\s*\(/g)].map(m=>m[1]));
console.log('missing handlers:',[...c].filter(f=>!d.has(f)));"
```

`node --check` fails on `.gs` files (`MODULE_NOT_FOUND`) — use `new Function(fs.readFileSync('Code.gs','utf8'))` instead.

Then check the HTTP layer (200, not a 302 to the Google sign-in page) and hand the remaining click-through to the user as a short numbered checklist.

For a large single-file frontend, write it in sections to a scratch directory and concatenate, then syntax-check immediately. Producing 3000+ lines in one shot makes structural errors hard to localise.

---

## Common Pitfalls & Solutions

| Issue / Pitfall | Cause | Solution |
| :--- | :--- | :--- |
| `/exec` redirects to `accounts.google.com` | `access: "ANYONE"` means "any signed-in Google account", not public | Use `ANYONE_ANONYMOUS`; gate with an in-app passcode |
| Users still see an old version after a push | `create-deployment` without `-i` minted a new URL | Always redeploy with `-i <existing-deployment-id>` |
| `google is not defined` | `index.html` opened as a local file instead of the `/exec` URL | Guard with `hasBackend()` and show a banner linking the real URL |
| Blank page whenever the backend hiccups | UI render gated behind a `google.script.run` round-trip | Render first, query auth/config after |
| Historical Sheet rows shift columns | A header was inserted mid-array | Schema is append-only; update read-side indices together |
| `/exec` redirects to `script.google.com/home` | A new OAuth scope was added and not yet authorized | Owner runs any function in the editor and approves; prefer scope-free services |
| Users randomly logged out | Sessions stored in `CacheService` (6 h max, evictable) | Use stateless signed tokens |
| Physician's manual edits get wiped | Generator writes outputs unconditionally on every change | `manualEdits` dirty flag + explicit regenerate button |
| Form is "complete" but nobody uses it | Every added section increased typing | Pair each section with a bulk normal/denied/non-contributory button |
| `Cannot read property 'appendRow' of null` | Tab missing, or `getActiveSpreadsheet()` returned null in a standalone script | `getOrCreateSheet()` + `getSpreadsheet()` with `openById` fallback |
| `User has not enabled the Google Apps Script API` | API off in the Google account | Turn it on at `https://script.google.com/home/usersettings` |
| `clasp: command not found` but credentials exist | Not installed globally; `~/.clasprc.json` still valid | `npx -y @google/clasp@latest <cmd>` (match the `.clasp.json` format version) |
| Docs left in Drive root | Created by `DocumentApp.create()` before being filed | `DriveApp.getFileById(id).moveTo(folder)` after `saveAndClose()` |
| `...setFontSize(...).setFontColor is not a function` | `setFontColor` is a Sheets `Range` method, not a Docs `Paragraph` one | Use `setForegroundColor`; leave genuine `Range.setFontColor` calls alone |
| Every cell in a generated table starts with a blank line | A new `TableCell` already holds one empty paragraph | Reuse `cell.getChild(0).asParagraph()` for the first line |
| A Docs API error only surfaces when a user clicks Save | Static checks cannot tell whether a Google API method exists | Ship a `runSelfTest()` that generates and then trashes a real document |

## Related

- **`admission-note-clinical-exam-system`** — the clinical domain layer: which sections a note needs, hospital form layout, ROS/PE interaction patterns, exam-modality guideline anchors, PHI handling.

# CLAUDE.md

Guidance for Claude Code working in this directory.

## What this project is

Modify and redeploy **陽明醫院 臨床醫療紀錄與報告系統** (Clinical Documentation System) — a
Google Apps Script web app that generates inpatient admission notes (H&P) and structured
exam reports (echo / abdominal US / UGI endoscopy / colonoscopy) for hospital staff.

**Production URL (v6.0, live):**
`https://script.google.com/macros/s/AKfycbyucGUOYz9eS9IrLWohMtYJ8Hm-oZmhgyhmKXZJjE1gf8DZj_Ra9r9_lzuUHgVVf2zL5g/exec`

The objective is to bring the note output in line with 陽明醫院's **real pre-printed
ADMISSION NOTE form**, then redeploy to the same URL so existing users keep their link.

## ⚠️ Read this before planning any work

**The real GAS project lives at the root of `github.com/ckt520728/2026-Antigravity`** —
`.clasp.json`, `appsscript.json`, `Code.gs` (971 lines) and `index.html` (v6.0). That is
the source of truth for both tiers. Script ID:
`1vmdg7x6X6kHzRnh1gA7u2GlRk_lnDW6Mvaava0SD-qdsdoowh4AhzyTL`.

**The only remaining blocker is `clasp login`** — an interactive browser sign-in as the
owning Google account, which Claude cannot perform. The deployment ID for
`create-deployment -i` also still needs `clasp list-deployments` after that login.

⚠️ **`src/index.html` here is NOT the canonical source.** It descends from a recovery of
the deployed `/exec` page, so it lost every original comment and had some HTML entities
decoded. Before anything is deployed, the changes in it must be **re-applied onto the
repo's `index.html`** — see `handoff.md` §2b. Do not overwrite the repo copy with it.

## Layout

```
CLAUDE.md                              this file
handoff.md                             current state, findings, blockers, next steps
STATE/option-ledger.md                 Oak-loop ledger — the workflow's durable state
baseline/index.v6.0.recovered.html     recovered live frontend (3,469 lines) — read-only reference
baseline/recover_from_exec.py          re-recovers the frontend from the /exec URL
```

`Admission-note-clinical-exam-system` (0 bytes, no extension) was already in this folder
and is not used by anything. Left in place — ask before deleting.

## Governing skills

Three skills define how this work is done. Read them before making changes.

| Skill | Role | Location |
|---|---|---|
| `oak-loop-engineering` | **workflow logic** — how work is proposed, gated, promoted | `~/.claude/skills/oak-loop-engineering` |
| `admission-note-clinical-exam-system` | **clinical domain** — what the note must contain, hospital form layout | `github.com/ckt520728/2026-Antigravity` → `.agents/skills/` |
| `gas-medical-webapp-generator` | **platform** — GAS deployment, auth, Sheets schema, Docs export | same repo, same path |

The two GitHub skills are a matched pair: domain layer and platform layer. The
`references/form-layout.md` beside the domain skill holds the **field-level inventory of
the real paper form** — that document is the specification for the work in this project.

### Working under the Oak loop

`STATE/option-ledger.md` is the loop's durable state; update it **every cycle**, not at
the end. The rules that bite here:

- Everything starts at **L1 (report-only)**. Nothing self-promotes.
- **Deploying is an absolute human gate** — it is publish/production and irreversible for
  users holding the link. Never redeploy without a recorded approval from Dr Chu.
- Maker and checker must not be the same actor; the checker defaults to REJECT.
- Attempt cap is **3** same-target corrections, then `ESCALATE_HUMAN`.
- Predict cost/side-effects/failure modes *before* acting, then record the surprise.

## Status

Work happens in **`src/index.html`**; `baseline/index.v6.0.recovered.html` is the untouched
v6.0 source and the rollback point. Run `node tests/check_note_output.js` after any change
to the note generators.

**Items 1 and 2 below are done**, as is the Personal History move (now under 過去病史 with
the new `admWaterExposure` field) — verified by **24** assertions. 檢查報告 is kept by
Dr Chu's decision even though the paper form omits it. Items 3–5 remain, plus one
**declared incompleteness**: the generated Doc still places Personal History under 家族史,
because placement lives in `Code.gs` (`handoff.md` §1c has the 3-line patch).
The authority for the format is
**`115-1-10 病歷書寫格式.DOC`** in the Drive root — the hospital's own template — *not*
the skill's `form-layout.md`, which differs from it in three places (see `handoff.md` §5).
⚠️ That .DOC is a *filled* form containing a real patient's identifiers: take layout only,
never copy identifiers, and don't leave extracted text lying around.

## The actual delta to build

v6.0 already implements the *headings* of the real form (主訴 / 現在病歷 / 過去病史 with its
four subheadings / 藥物過敏 / 家族史 / 系統回顧 / 理學檢查 / 檢驗報告 / 檢查報告 / 初步診斷 /
治療及計劃 / 主治醫師), the ROC-date letterhead, tri-state ROS chips, the `manualEdits`
dirty flag, localStorage autosave, the passcode gate, and colonoscopy withdrawal time at
the correct **≥ 8 min (ASGE/ACG 2024)**.

What it does **not** yet match is the form's *content model* — it still uses the generic
templates from the skill rather than 陽明醫院's own. That gap is the work:

1. **ROS** — app has a generic **10**-system list (incl. `endo`); the form has **9**
   (systemic, skin, HEENT, CV, respiratory, GI, urogenital, musculoskeletal,
   neurological) with its own symptom lists.
2. **Physical exam** — app emits prose normal sentences; the form uses **numbered items
   with `(+)`/`(-)` flags** per system (`HEENT: 1.Conjunctivae pale(-) .icteric
   sclerae(-) …`) and a `Conscious: E_V_M_` line.
3. **Medications** — app has one free-text box; the form groups by **date + issuing
   hospital**, then numbers each drug with strength/qty/frequency/route/days.
4. **Labs** — app uses prose placeholders; the form writes
   `CBC  2/18  WBC:__  Hgb:__  PLT:__  MCV:__` (panel + date + space-separated values).
5. **Disclaimer** — the domain skill requires it *in the product*; v6.0 has none.

Full evidence and per-item detail: `handoff.md`.

## Conventions and hazards

- **Redeploy with `-i <deploymentId>` or users keep the old version.** Record the real
  deployment id in this file the moment it is known.
- **Access level must stay `ANYONE_ANONYMOUS`.** Verified: the live URL returns **200**
  to an unauthenticated request. `ANYONE` would 302 to the Google sign-in page — and you
  would not notice from your own signed-in browser.
- **Sheet schema is append-only.** New columns go at the *end*; update the read-side index
  map in the same change.
- **Adding an OAuth scope breaks the live app** until the owner re-authorizes in the
  editor. Prefer `PropertiesService` / `CacheService` / `Utilities`, which need no scope.
- **`setForegroundColor`, never `setFontColor`, on a Docs `Paragraph`** — `setFontColor`
  is a Sheets `Range` method and the failure only appears when a user presses Save.
  Genuine `Range.setFontColor` calls on sheet headers are correct; leave them alone.
- **Syntax-check every frontend edit** — the web layer cannot be exercised from a
  terminal:
  ```bash
  node -e "const fs=require('fs');const s=fs.readFileSync('index.html','utf8');
  [...s.matchAll(/<script>([\s\S]*?)<\/script>/g)].forEach((m,i)=>{
    try{new Function(m[1]);console.log('block',i+1,'OK')}catch(e){console.log('block',i+1,'ERR',e.message)}});"
  ```
  All 3 blocks of the recovered baseline pass — keep it that way.
- **`node --check` fails on `.gs`** — use `new Function(fs.readFileSync('Code.gs','utf8'))`.

## PHI — non-negotiable

This app collects **姓名, 病歷號, 身分證號碼, 生日, 床號**. Accordingly:

- **Never commit a scan or photo of a real chart or a filled form.** Layout is what's
  needed; ask for de-identified samples.
- **Never paste real patient data into a test, fixture, prompt, or commit message.**
- The passcode gate ships **on** — the form asks for national IDs, so an open endpoint is
  not acceptable.
- This folder is inside **Google Drive**, which syncs. Treat anything written here as
  leaving the machine.

## Console encoding

The Windows console is **cp950** — printing CJK from Python mangles or crashes. Files are
written as valid UTF-8 regardless; verify by reading the file back, not by echoing it.
Also: the Bash tool collapses backslashes in heredocs — write Python to a file and run it
rather than piping a heredoc.

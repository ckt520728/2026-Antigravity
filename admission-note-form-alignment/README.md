# Admission note — 陽明醫院 form alignment (work in progress)

Work-in-progress folder for bringing the admission note in this repo's Apps Script project
(`../Code.gs`, `../index.html`, v6.0) into line with 陽明醫院's **real pre-printed
ADMISSION NOTE form**, run under the `oak-loop-engineering` workflow.

**Status: L1 (report-only). Nothing here has been deployed.** The live `/exec` app is
untouched.

## Read these first

| File | What it is |
|---|---|
| `handoff.md` | current state, what changed, what is blocked, open questions |
| `CLAUDE.md` | project guidance for Claude Code sessions |
| `STATE/option-ledger.md` | the Oak loop's durable state — Features, Options, predictions vs outcomes |

## What changed

`src/index.html` replaces the generic clinical templates with the hospital's own:

- **ROS** — the form's 9 systems and symptom lists, serialised as
  `5.Respiratory：dyspnea(+)；cough(-)…`
- **Physical exam** — the form's numbered `(+)`/`(-)` item grid (per-item toggle chips)
  plus `Conscious: E4V5M6` and the `Wound` line, replacing prose normal sentences
- **Personal History** — moved under 過去病史 per the form, with a new
  contaminated-water field
- **Labs** — the form's `CBC  2/18   WBC:12.3  Hgb:10.2` convention, plus the missing
  SMA and KUB panels and per-panel dates
- **Disclaimer** — persistent in-product bar (the tool records and formats; it does not
  diagnose)

`node tests/check_note_output.js` runs 31 assertions over the note generators against a
stubbed DOM. All pass.

## Deploying

`src/index.html` **is** `../index.html` with these changes applied on top — re-based onto
the real source on 2026-08-12, comments and HTML entities intact. Diff against
`../index.html` is 13 hunks, all intended. It can be copied over `../index.html` directly.

One backend change is still outstanding: print `record.personalHistory` under 過去病史 and
drop the `Personal and social history :` line at `../Code.gs:629`. See `handoff.md` §1c.

## 🔴 The passcode gate is currently off

`../Code.gs:49` has `AUTH_ENABLED = false`, and the live `/exec` answers **200 to an
unauthenticated request** — so anyone with the link can open an app that collects
**身分證號碼**. Turning it on: set `AUTH_ENABLED = true`, run `setAppPasscode()` once from
the editor, redeploy with `-i <deploymentId>`.

## Provenance and PHI

The format authority is 陽明醫院's own template, `115-1-10 病歷書寫格式.DOC`, held on
Dr Chu's Drive. **That file is a filled form containing a real patient's identifiers.**
Only its layout was used; **no identifier appears anywhere in this folder**, and the
extracted text was deleted after reading. Do not add it, or any filled chart, to this repo.

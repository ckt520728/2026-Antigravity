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

## ⚠️ Before anyone deploys this

`src/index.html` was reconstructed from the **deployed page**, before the real source in
this repo was found. It is faithful in logic but **lost the original source comments**.

**Do not copy it over `../index.html`.** Re-apply the changes onto the repo's own
`index.html` — they are well isolated (`ROS_SYSTEMS`, `PE_FORM` and its render/build
functions, `buildPersonalHistoryLines`, `LAB_PANELS`/`labLine_`, the draft v7 migration,
the disclaimer bar) — then re-run the test suite. See `handoff.md` §2b.

One backend change is also outstanding: print `record.personalHistory` under 過去病史 and
drop the `Personal and social history :` line at `../Code.gs:629`. See `handoff.md` §1c.

## Provenance and PHI

The format authority is 陽明醫院's own template, `115-1-10 病歷書寫格式.DOC`, held on
Dr Chu's Drive. **That file is a filled form containing a real patient's identifiers.**
Only its layout was used; **no identifier appears anywhere in this folder**, and the
extracted text was deleted after reading. Do not add it, or any filled chart, to this repo.

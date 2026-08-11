# Oak Option Ledger — Admission Note & Clinical Exam System

Durable evidence for the loop's Features, SubTasks, Options, Models, and planning
decisions. Update at the end of **every** interaction, not in a later batch.

`loop-pause-all: false`

**Opened:** 2026-08-11 · **Current level: L1 (report-only)** · **Owner: Dr Chu**

> Per `oak-loop-engineering`: nothing here self-promotes. Status changes only on a
> recorded human decision in § Gate decisions.

---

## Parent objective and reward

- **Parent objective:** the deployed 陽明醫院 clinical documentation web app produces an
  admission note matching the hospital's real pre-printed ADMISSION NOTE form, and
  remains reachable by ward staff at its existing `/exec` URL.
- **Trusted closed-world reward:**
  - all `<script>` blocks parse (`new Function()` per block) — currently **3/3 green**;
  - every inline handler resolves to a defined function; every `getElementById` target exists;
  - `/exec` returns **HTTP 200 to an unauthenticated request** (not a 302 to
    `accounts.google.com`) — currently **green**;
  - backend `runSelfTest()` generates and trashes a real Doc without error *(not yet
    available — see Feature `F3`)*.
- **Human-only judgment:** whether the generated note is clinically correct and
  acceptable to 陽明醫院; whether the form reproduction is faithful; all wording of
  clinical text; the replace-vs-both decision on ROS/PE templates.
- **Terminal-Feature bonus:** bounded +1 per gap in `handoff.md` §4 closed with its
  regression test green. May not override the parent reward or any gate below.
- **Risk/cost penalties:** each redeploy (user-visible, irreversible for anyone holding
  the link); each added OAuth scope (breaks the live app until re-authorised); any
  frontend diff > ~400 lines in one gate.
- **Absolute path/action gates — `ESCALATE_HUMAN`, no exceptions:**
  - **any deploy / push / publish**, including `clasp push` and `create-deployment`;
  - `appsscript.json` `oauthScopes` or `webapp.access`;
  - the passcode / token / auth code path;
  - Sheets **header order** (schema is append-only; a mid-array insert silently shifts
    every historical row);
  - anything touching real patient data — 姓名, 病歷號, **身分證號碼**, 生日, 床號.
- **Attempt cap:** 3 same-target corrections → `ESCALATE_HUMAN` with the full trail.
- **Daily budget:** ≤ 1 redeploy per day; frontend edit cycles otherwise unbounded but
  logged.
- **Kill switch:** `loop-pause-all` above. Setting it `true` halts every level.
- **Evidence policy:** raw traces kept in this folder. **No patient data, no passcode, no
  token, no credential may be written to this ledger** — reference by description only.
  Retention: life of the project; access: Dr Chu.
- **Durable state authority:** this file, append-only in spirit (supersede rows, don't
  erase). Authorised by Dr Chu's instruction to run under `oak-loop-engineering`.
- **Read-only attestation (this session):** `curl` GET of the `/exec` URL and `gh api`
  reads only; all parsing local and bounded; **zero writes to the Apps Script project,
  zero writes to any Google Sheet or Doc**; the only mutations were new files created
  inside this folder.

---

## Baseline

- **Current primitive procedure:** edit the Apps Script project by hand in the web
  editor, then redeploy from the editor UI.
- **Reward/result:** v6.0 live and serving 200. Headings already match the real form;
  content model does not (see Features `F1`, `F2`).
- **Planning decisions/tool calls:** this session — ~20 tool calls to establish state
  from a standing start with no source checkout.
- **Tokens/time/cost:** one session; no external spend.
- **Side effects/risk:** none this session (read-only against Google; writes confined to
  this folder).

---

## Maintenance

- **Prune/reset every:** end of each working session.
- **Last pass:** 2026-08-11.
- **Confidence floor/reset rule:** any Feature whose detector has not been re-run in 3
  sessions drops to `proposed` and must be re-probed before it can justify an Option.

---

## Feature registry

### Feature: F1 — ROS list diverges from the hospital form

- **version:** v1
- **detector/probe:** extract `ROS_SYSTEMS` from the frontend; compare its key set with
  the 9 systems in `form-layout.md`. Fires when the sets differ.
- **positive evidence:** v6.0 `ROS_SYSTEMS` = `general, heent, resp, cv, gi, gu, msk,
  neuro, skin, endo` — **10** keys including `endo`, which the form has no equivalent for;
  symptom lists also differ (form's GI carries 11 items incl. melena and small caliber
  stool). Observed 2026-08-11 in `baseline/index.v6.0.recovered.html`.
- **counterexamples:** none yet.
- **predictive use:** predicts that a physician comparing generated output against the
  paper form will find missing and extra ROS lines.
- **novelty vs existing Features:** distinct from `F2` — same form, different section and
  different failure (list membership vs interaction model).
- **confidence/update-rate:** HIGH on the detector (mechanical set comparison, no
  judgement). Contingent on `Q1` — *unconfirmed* that 陽明醫院's form is the one in
  `form-layout.md`.
- **status:** verified *(detector)* / **blocked on `Q1`** *(clinical premise)*

### Feature: F2 — PE uses prose sentences, not the form's item grid

- **version:** v1
- **detector/probe:** read `PE_SYSTEMS`; fire if a system's normal value is a prose
  sentence rather than numbered `(+)`/`(-)` items.
- **positive evidence:** `peAbdomen` normal = `'Soft and flat, normoactive bowel sounds,
  no tenderness, no rebound tenderness, liver and spleen impalpable.'` The form instead
  specifies `Abdomen: 1.soft(+) 2.Bowel sound:__ … 11.Scar(-)`. Observed 2026-08-11.
- **counterexamples:** none yet.
- **predictive use:** predicts that matching the form requires a **new interaction
  model** (per-item toggles), not a string swap — i.e. a materially larger change than
  `F1`.
- **novelty vs existing Features:** `F1` is data; `F2` is data **and** UI behaviour.
- **confidence/update-rate:** HIGH on the detector; same `Q1` contingency as `F1`.
- **status:** verified *(detector)* / **blocked on `Q1`**

### Feature: F3 — backend is unreadable, so document-layout gaps cannot be closed

- **version:** v1
- **detector/probe:** look for `.clasp.json` / `~/.clasprc.json` / a known script ID.
  Fires when the backend cannot be read.
- **positive evidence:** none present on this machine (checked 2026-08-11). Only five
  server function *names* are visible from the frontend.
- **counterexamples:** none.
- **predictive use:** predicts that gaps **G3** (medication grouping), **G4** (lab
  format) and **G6** (self-test) cannot be attempted, and that **no deploy is possible**,
  until access is granted.
- **novelty vs existing Features:** environmental, not clinical.
- **confidence/update-rate:** HIGH — mechanically checkable, no judgement.
- **status:** ❌ **FALSIFIED 2026-08-12 (cycle 4).** The detector was sound but its search
  scope was wrong: it looked only at the local filesystem. `Code.gs`, `appsscript.json` and
  `.clasp.json` were in `github.com/ckt520728/2026-Antigravity` — a repo this loop had
  already read *twice* for the two skills, without ever listing its root.
- **corrected detector (v2):** before declaring a source unavailable, list the root of
  every repo already known to the project, not just the paths being fetched from it.
- **cost of the error:** three cycles of work were scoped around a blocker that was not
  real. G6 was reported as "blocked" when `runSelfTest()` already existed; the §1c Doc
  patch was written as a guess when the exact code was readable; and `src/index.html` was
  built from a lossy `/exec` recovery instead of the real source, and now needs re-basing.
  Nothing shipped on the false premise — the L1 gate held — but the planning was wrong.

### Feature: F4 — an authoritative copy of the real form exists on the Drive

- **version:** v1
- **detector/probe:** search the Drive root for a 病歷書寫格式 / admission-note template
  document; extract with `antiword -m UTF-8.txt`.
- **positive evidence:** `115-1-10 病歷書寫格式.DOC` (Drive root, dated 2026-01-10) is
  陽明醫院's own filled ADMISSION NOTE template. Confirms `Q1` and supplies the exact ROS
  symptom lists and PE item numbering.
- **counterexamples:** none.
- **predictive use:** replaces `form-layout.md` as the authority; predicted (correctly)
  that the reference skill would be *close but incomplete*.
- **⚠️ PHI:** the file **contains a real patient's 姓名 / 病歷號 / 身分證號碼 / 生日 /
  床號**. Only the *layout* was taken; **no identifier was copied into any project file**,
  and the extracted text was deleted immediately after reading. Do not re-extract it into
  a durable location.
- **novelty vs existing Features:** supersedes the assumption behind `F1`/`F2`.
- **confidence/update-rate:** HIGH — primary source, read directly.
- **status:** verified

### Feature: F5 — the frontend composes the note text, not the backend

- **version:** v1
- **detector/probe:** read the payload passed to `saveAdmissionNoteRecord`; check whether
  section bodies are composed client-side.
- **positive evidence:** the record object sends **already-composed strings** —
  `reviewOfSystems: buildROSText()`, `physicalExam: buildPEText()`, `vitalSigns`,
  `labsReport`, `studiesReport`. `Code.gs` places these under fixed headings.
- **counterexamples:** none found; heading text and document layout still live server-side.
- **predictive use:** predicts that any change to *section content* is achievable without
  backend access, and that only heading/layout changes and deployment need `Code.gs`.
- **novelty vs existing Features:** materially narrows `F3`.
- **confidence/update-rate:** HIGH for content; **UNVERIFIED end-to-end** — the generated
  Doc has not been seen, because that requires a deploy.
- **status:** verified *(client side)* / unconfirmed *(rendered document)*

---

## SubTasks

### SubTask: ST1 — obtain backend access *(precondition for everything downstream)*

- **parent Feature:** F3
- **initiation evidence:** F3 fires.
- **terminal test:** `clasp clone-script <SCRIPT_ID>` yields `Code.gs` + `appsscript.json`
  locally, **and** `clasp list-deployments` prints the deployment id backing the live URL.
- **reward:** parent reward + terminal bonus; unblocks G3/G4/G6 and all deployment.
- **attempt/escalation:** not machine-solvable — `clasp login` is an interactive browser
  sign-in. **Escalated to Dr Chu on 2026-08-11** (`handoff.md` §2).
- **allowed actions:** none autonomous. Ask only.
- **status:** active — **awaiting Dr Chu**

### SubTask: ST2 — align ROS and PE with the real form

- **parent Feature:** F1, F2
- **initiation evidence:** F1/F2 fire **and** `Q1` (is this 陽明醫院's form?) and `Q2`
  (replace, or offer both?) are answered.
- **terminal test:** generated ROS covers exactly the form's 9 systems and their symptom
  lists; PE renders the form's numbered `(+)`/`(-)` items plus `Conscious: E_V_M_`; all 3
  script blocks still parse; every handler still resolves; a side-by-side against the
  paper form is approved by Dr Chu.
- **reward:** parent reward + bounded bonus per gap closed. **Clinical faithfulness is
  human-judged and cannot be auto-scored.**
- **attempt/escalation:** cap 3, then hand back with the trail.
- **allowed actions:** edit the frontend copy in this folder only. **No deploy.**
- **status:** **solved in `src/` (2026-08-11, cycle 2) — awaiting independent check and
  Dr Chu's review.** `Q1` confirmed by `F4`; `Q2` answered by Dr Chu: *replace*.
  Terminal test: **18/18 automated checks pass** (`tests/check_note_output.js`), 3/3
  script blocks parse, 0 unresolved handlers. The remaining clause of the terminal test —
  side-by-side approval against the paper form — is **human judgement and still open**.

---

### SubTask: ST3 — place Personal History per the hospital form

- **parent Feature:** F4
- **initiation evidence:** `F4` shows `Personal History :` under 過去病史 with four fixed
  items; Dr Chu instructed the move and instructed that 檢查報告 be kept.
- **terminal test:** the composed note emits Personal History after
  `4. Home medication reviews`, omits it from 家族史, still emits 檢查報告, and preserves
  every social-history value already captured.
- **reward:** parent reward + bounded terminal bonus.
- **attempt/escalation:** cap 3. The Doc-side placement is **out of reach** and was
  escalated rather than worked around (see the Option's declared incompleteness).
- **allowed actions:** frontend only. **No deploy.**
- **status:** **solved for the frontend (2026-08-12)** — 24/24 checks pass.
  **Doc-side placement remains open, blocked on `Code.gs`.**

## Options

`status`: `proposed` (L1) → `gated` (L2) → `allowlisted` (L3). Only a recorded human
decision in § Gate decisions changes status.

### Option: recover_frontend_from_exec

- **version:** v1
- **status:** **proposed (L1)** — read-only, and it has now run once successfully
- **order:** 1
- **solves SubTask:** partially mitigates ST1 (recovers the frontend; not the backend)
- **initiation contract:** the `/exec` URL returns 200 and the response embeds a
  `userHtml` JSON field.
- **policy/steps:** GET `/exec` → locate `\x22userHtml\x22:\x22` → unescape the JS string
  layer (`\xNN`, `\\`, `\/`) → `json.loads` → write `baseline/index.<ver>.recovered.html`.
  Implemented as `baseline/recover_from_exec.py`.
- **termination condition:** output is well-formed HTML **and** every `<script>` block
  parses under `new Function()`.
- **rollback/cleanup:** writes one file into `baseline/`; delete to undo. Touches nothing
  on Google.
- **regression test:** the 3-block parse check in `CLAUDE.md` § Conventions.
- **worktree:** not required (no mutation outside this folder).
- **signal:** trials=1, successes=1, same-target-attempts=0
- **checker/gate evidence:** *not yet independently checked.* Self-reported result:
  3,469 lines, 3/3 blocks parse. **Needs an independent checker before L2.**

---

### Option: replace_ros_pe_with_hospital_form

- **version:** v1
- **status:** **proposed (L1)** — written to `src/`, **not deployed**
- **order:** 2
- **solves SubTask:** ST2
- **initiation contract:** `F1`/`F2` fire, `F4` supplies the authoritative layout, and
  Dr Chu has chosen *replace* over *offer both*.
- **policy/steps:** replace `ROS_SYSTEMS` with the form's 9 systems; replace `PE_SYSTEMS`
  (prose) with `PE_FORM` (numbered `(+)`/`(-)` items + free-text lines); rewrite
  `buildROSText` to `N.system：symptom(-)；…`; add `peState`/`peActive` with
  `composePE`/`peRefreshChips`/`peSyncField`; re-point `renderPE`/`peAllNormal`/`peClear`/
  `buildPEText`; extend the draft to v7 while still restoring v6 text.
- **termination condition:** all script blocks parse, no unresolved handlers, no stale
  `PE_SYSTEMS` reference, and `tests/check_note_output.js` exits 0.
- **rollback/cleanup:** `baseline/index.v6.0.recovered.html` is the untouched v6.0 source;
  restoring it reverts everything. **Nothing on Google was touched, so there is nothing to
  roll back server-side.**
- **regression test:** `node tests/check_note_output.js` (18 assertions) + the 3-block
  parse check.
- **worktree:** not used — mutation is confined to this project folder and the pre-change
  source is preserved verbatim in `baseline/`.
- **signal:** trials=1, successes=1, same-target-attempts=0
- **checker/gate evidence:** ⛔ **none — maker has not been checked.** The author of the
  change also wrote its tests, so per the maker/checker split this **cannot** advance to
  L2 on this evidence. Needs an independent checker plus Dr Chu's clinical review.

### Option: move_personal_history_to_past_history

- **version:** v1
- **status:** **proposed (L1)** — written to `src/`, **not deployed**
- **order:** 3
- **solves SubTask:** ST3 (below)
- **initiation contract:** `F4` shows Personal History under 過去病史 and Dr Chu has
  instructed the move; 檢查報告 to be preserved.
- **policy/steps:** add the `admWaterExposure` field (the form's 4th item, absent from the
  app); add `buildPersonalHistoryLines()`; emit the block after `4. Home medication
  reviews` in the note composer; remove the `Personal and social history :` line from
  家族史; add a `personalHistory` field to the record for the future backend edit; extend
  `markSocialDenied()` to reset the new field.
- **termination condition:** section order matches the form; `Personal and social history`
  no longer appears under 家族史; 檢查報告 still emitted; all static checks green;
  `tests/check_note_output.js` exits 0.
- **rollback/cleanup:** `baseline/index.v6.0.recovered.html` remains the untouched v6.0
  source. Nothing on Google was touched.
- **regression test:** `node tests/check_note_output.js` — now **24** assertions, 6 of
  them covering this change.
- **worktree:** not used; mutation confined to this folder with the pre-change source
  preserved.
- **signal:** trials=1, successes=1, same-target-attempts=0
- **checker/gate evidence:** ⛔ **none — maker wrote its own tests again.** Cannot advance
  past L1 on this evidence.
- **⚠️ known incompleteness (declared, not discovered later):** the generated **Doc** still
  places Personal History under 家族史, because that is decided in `Code.gs`. A workaround
  existed (fold the block into the `medications` field) and was **rejected** — it would
  have corrupted the Sheets `medications` column, violating the parent objective's
  append-only/audit constraint to fix a layout issue. Escalated rather than guessed at.

## Option Models

### Model: recover_frontend_from_exec@v1

- **predicted terminal state:** full frontend HTML recovered, syntactically valid.
- **predicted cumulative reward:** unblocks all frontend gap analysis without backend access.
- **predicted time/tokens/cost:** ~1 fetch + local parsing; no external spend.
- **predicted touched paths/external effects:** writes `baseline/` only; **read-only**
  against Google.
- **predicted failure modes:** (a) content served only inside a sandboxed
  `googleusercontent.com` iframe, so `/exec` yields a shell; (b) escaping deeper than one
  JS layer; (c) charset corruption of CJK.
- **success probability (declared before the trial):** 0.5 — the platform skill warns that
  static fetches "only return the outer shell".
- **ground-truth source/timing:** immediate (per-block `new Function()` parse).
- **confidence/update-rate:** raise on success; a single success is **not** promotion
  evidence.
- **surprise/promotion thresholds (declared before trial 1):** any block failing to parse
  = HIGH surprise, abandon the approach.
- **human calibration approval:** ⛔ **not yet given — promotion is blocked, correctly.**
- **calibration history:**
  - *trial 1, 2026-08-11* — predicted 0.5, **outcome success** (Brier `(0.5−1)² = 0.25`).
    Component surprise: failure mode (a) **did not occur** — the app HTML was inline in
    the `/exec` response, contrary to the platform skill's warning. Failure mode (b)
    **partially occurred**: escaping was two layers (JS literal wrapping JSON), one more
    than assumed. Failure mode (c) was a *false alarm from the cp950 console*, not real
    corruption — bytes were valid UTF-8 throughout.
  - **Model update:** for this app, `/exec` serves the frontend inline. Treat the
    platform skill's "outer shell only" note as *not* applying here — but n=1, so this is
    a prior, not a fact.

---

### Model: replace_ros_pe_with_hospital_form@v1

- **predicted terminal state:** ROS/PE emit the hospital form's notation; all static
  checks stay green.
- **predicted cumulative reward:** closes G1 + G2 — the substance of the user's request.
- **predicted time/tokens/cost:** one session; no external spend.
- **predicted touched paths/external effects:** `src/index.html`, plus a new test file.
  **No writes to Google, no deploy.**
- **predicted failure modes:** (a) `renderPE` rebuilding `innerHTML` wipes restored draft
  text; (b) changed ROS keys silently half-restore old drafts; (c) unreviewed items get
  auto-asserted as negative — a *clinical safety* failure, not a cosmetic one;
  (d) removed PE ids (`peBack`/`peNeuro`/`peSkin`) leave dangling references.
- **success probability (declared before the trial):** 0.7
- **ground-truth source/timing:** immediate for structure/format (automated); **delayed
  and human** for clinical faithfulness and for how the generated Doc actually renders.
- **confidence/update-rate:** raise only after an independent checker reproduces the test
  result; a self-written test passing is weak evidence.
- **surprise/promotion thresholds (declared before trial 1):** any parse failure or any
  auto-asserted unreviewed finding = HIGH surprise, revert.
- **human calibration approval:** ⛔ **not given — promotion blocked.**
- **calibration history:**
  - *trial 1, 2026-08-11* — predicted 0.7, **outcome success** on the automated clause
    (Brier `(0.7−1)² = 0.09`). Failure mode (a) **did occur** and was caught before the
    run: `restoreDraft` now re-applies PE text after `renderPE()`. (b) **occurred** and was
    handled by accepting v6 drafts for text while discarding stale chip state. (c) was
    **designed out** — `buildROSText` prints only explicitly-clicked items and `composePE`
    prints nothing for an untouched block; both are asserted by the test suite.
    (d) **did not occur** — 0 stale `PE_SYSTEMS` references.
  - **Model update:** the risky part of this change was **draft-state migration**, not the
    template data. Predicted-vs-actual on the *rendered Google Doc* is still **unknown** —
    the automated evidence covers the client-composed string only.

## Planning decisions

| cycle | state/Feature | candidates | chosen | predicted utility/risk | baseline | actual utility/risk | decision error |
|------:|---------------|------------|--------|------------------------|----------|---------------------|----------------|
| 1 | F3 fires: no source, no credentials | (a) ask Dr Chu and stop; (b) recover frontend from `/exec` first, then ask | **(b)** | moderate utility, ~zero risk (read-only); worst case wasted parsing | ask-and-stop → zero information while waiting | **higher than predicted** — full frontend recovered, so the entire gap analysis (§4 of handoff) was possible *while* blocked; the ask still went out | none — but success probability was underestimated (0.5 → observed success) |
| 2 | Dr Chu answers "replace"; F1/F2 actionable | (a) build ROS/PE from `form-layout.md`; (b) look for a hospital-authored copy of the form first, then build | **(b)** | one extra probe (~1 tool call) against the risk of building the wrong template | (a) would have shipped `form-layout.md`'s structure directly | **(b) paid off** — `F4` found 陽明醫院's own template, which differs from the reference in 3 ways (Personal History under 過去病史, a `Wound` PE line, no 檢查報告). (a) would have produced a form that was subtly wrong and looked authoritative | none — the cheap probe was correctly ordered before the expensive build |
| 3 | Dr Chu decides: move Personal History, keep 檢查報告 | (a) frontend-only move, accept Doc divergence; (b) fold the block into the `medications` field so the Doc moves too | **(a)** | (b) would move the Doc text now, but writes social history into the Sheets `medications` column — an audit-trail corruption, and unverifiable without `Code.gs` | leaving it under 家族史 → contradicts the instruction and the paper form | **(a) taken.** Preview + clipboard (the primary physician route) now correct; Doc placement escalated with an exact 3-line patch | none — but this is a *declared* incompleteness, not a solved item; it must not be reported as "done" |

---

## Interaction log

| cycle | Option | prediction | evidence | component surprise | Model/update-rate change | next action |
|------:|--------|------------|----------|--------------------|--------------------------|-------------|
| 1 | recover_frontend_from_exec@v1 | 0.5 success; expected an iframe shell | 3,469 lines recovered; 3/3 script blocks parse | **MEDIUM** — inline not iframed; escaping one layer deeper; CJK "corruption" was a console artefact | confidence ↑ but held at `proposed`; n=1 | escalate ST1 to Dr Chu; hold all mutation at L1 |
| 2 | replace_ros_pe_with_hospital_form@v1 | 0.7 success; 4 named failure modes | 18/18 assertions pass; 3/3 blocks parse; 0 stale refs; 0 unresolved handlers | **MEDIUM** — two predicted failure modes (draft wipe, stale draft keys) were real and needed handling; the *rendered Doc* remains unobserved | risk model updated: draft-state migration is the hazard, not the template data | hold at L1; request independent check + Dr Chu's side-by-side review; escalate the 3 form discrepancies in `F4` |
| 3 | move_personal_history_to_past_history@v1 | 0.8 success on the frontend; predicted the Doc side would be unreachable | 24/24 assertions; section order matches the form; `Personal and social history` gone from 家族史; 檢查報告 retained | **LOW** — the frontend move went as predicted. The genuine finding was a *choice*, not a surprise: a field-stuffing workaround could have moved it in the Doc at the cost of the Sheets audit column | no Model change; confirms `F5` (frontend composes text) has a hard edge — **placement** is backend, **content** is frontend | hold at L1; hand the 3-line `Code.gs` patch to Dr Chu with the source request |
| 4 | add_disclaimer_and_lab_panel_format@v1 | 0.85 success; risk was UI churn in the lab grid | 31/31 assertions; 0 bad blocks; 0 unresolved handlers; all new ids resolve | **HIGH — but from an unrelated direction:** the end-of-day push revealed `Code.gs` in `2026-Antigravity`, falsifying `F3` | `F3` marked FALSIFIED; new meta-Feature `F6` recorded; `src/index.html` demoted from "the source" to "a copy needing re-base" | re-base onto the repo's `index.html`; apply the §1c patch against real code |

---

### Feature: F6 — "not found locally" was mistaken for "not available"

- **version:** v1
- **detector/probe:** when any Option is blocked on a missing artefact, enumerate every
  source already known to the project (repos, Drive folders, deployed endpoints) and
  confirm each has actually been *listed*, not merely *fetched from*.
- **positive evidence:** `F3` declared the backend unrecoverable on 2026-08-11 after
  checking only the local filesystem. On 2026-08-12 a `git clone` of `2026-Antigravity`
  — already used twice for the skills — showed `Code.gs` at its root. Similarly `F4`
  found the authoritative form only because cycle 2 happened to probe the Drive root.
- **counterexamples:** none yet.
- **predictive use:** predicts that "blocked" claims in this project are unreliable until
  known sources have been enumerated; a cheap listing beats an expensive workaround.
- **novelty vs existing Features:** meta-level — about the loop's own search behaviour,
  not the product.
- **confidence/update-rate:** HIGH — two independent instances in four cycles.
- **status:** verified

## Gate decisions

| date | artifact | transition | checker evidence | planning utility | approved by |
|------|----------|------------|------------------|------------------|-------------|
| — | *(none yet — nothing has been promoted, and nothing has been deployed)* | | | | |

---

## Archive

*(empty)*

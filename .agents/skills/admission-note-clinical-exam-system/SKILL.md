---
name: admission-note-clinical-exam-system
description: Use when designing or extending a clinical documentation product — inpatient admission notes (H&P) and structured examination reports (echocardiography, abdominal ultrasound, upper/lower GI endoscopy). Covers which sections a defensible note needs, how to lay a generated document out like a hospital's own paper form, the interaction patterns that keep a complete form fast enough that physicians actually use it, the guideline anchors for each exam modality, and the PHI handling the domain requires. Triggers on 住院病歷, admission note, H&P, ROS, 系統回顧, physical examination template, 檢查報告, echo/sono/UGI/LGI report, problem-based assessment and plan.
---

# Admission Note & Clinical Exam Reporting System

## Overview

How to build the *clinical product*: what belongs in an admission note, how the generated document should look, and which interaction patterns decide whether a physician keeps using it.

This is the domain layer. The platform layer — Google Apps Script, `clasp`, deployment, access levels, passcode gating, Sheets schema — lives in the sibling skill **`gas-medical-webapp-generator`**. Read that one for plumbing; read this one for what to build.

## The governing constraint

> **Completeness that costs typing gets abandoned.**

Every section you add makes the note more defensible and the tool slower. A form that grows from 6 sections to 9, with a 10-system review of systems and a 10-system physical exam, is strictly worse than the short version *unless* each addition ships with a bulk escape.

This single trade-off drives most of the design decisions below. Standard templates exist to provide breadth; `non-contributory` is what stops note bloat. Build both sides or don't add the section.

---

## Part 1 — Admission note sections

A defensible teaching-hospital H&P needs all of these. The middle column is what most home-grown tools omit.

| # | Section | Commonly missing | Bulk escape to ship with it |
|---|---|---|---|
| 1 | Demographics + **informant & reliability** | informant | — |
| 2 | Chief complaint | | quick-fill chips |
| 3 | History of present illness (+ ED course) | ED course | LQQOPERA chips |
| 4 | Past medical history | | condition checkboxes |
| 5 | **Past surgical history** | ✅ | "denied" |
| 6 | **Current medications** (reconciliation) | ✅ | "none on admission" |
| 7 | Allergies | | NKDA default |
| 8 | **Family history** | ✅ | "non-contributory" |
| 9 | **Social history** | ✅ | "denies all" |
| 10 | **Review of systems** | ✅ | **"all negative"** |
| 11 | Vital signs + **physical exam by system** | per-system split | **"all normal"** |
| 12 | **Admission labs & imaging** | ✅ | "pending" |
| 13 | **Problem-based** assessment **and** plan | problem pairing | scenario templates |

Two structural rules that matter more than the section list:

- **Physical exam is per-system, not one textarea.** Ten systems (General/Consciousness, HEENT, Neck, Chest, Heart, Abdomen, Back/Flank, Extremities, Neurological, Skin), each with a standard normal sentence and chips for common abnormals.
- **Assessment and plan are paired.** One problem carries its own plan. Two independent free-text boxes — one for diagnoses, one for orders — is the single most common design error, and it makes the note unusable for handover.

Regulatory framing worth surfacing in the UI: an H&P is generally required within 24 hours of admission (US CMS 42 CFR 482.24). A countdown against the admission timestamp is cheap and welcome.

---

## Part 2 — Interaction patterns

These are what make a complete form fast. Each has been used in production.

### Tri-state ROS chips

A review of systems is ~55 symptoms across ~10 systems. Checkboxes can't express the three states a note needs.

```
click 1 → positive (+)     click 2 → negative (−)     click 3 → clear
```

Plus one **"all negative"** button that stamps every system, after which the physician clicks only the positives. Render from config, never hand-written HTML:

```js
var ROS_SYSTEMS = [
  ['resp', '呼吸 Respiratory', ['Cough', 'Sputum', 'Dyspnea', 'Hemoptysis', 'Wheezing']],
  ['cv',   '心血管 Cardiovascular', ['Chest pain', 'Palpitation', 'Orthopnea', 'Leg edema']]
  // ...
];
```

Serialise in the notation clinicians already write: `Respiratory：dyspnea(-)；cough(-)；chest pain(-)`.

### Per-system physical exam with normal defaults

```js
var PE_SYSTEMS = [
  ['peAbdomen', 'Abdomen (腹部)',
    'Soft and flat, normoactive bowel sounds, no tenderness, no rebound tenderness, liver and spleen impalpable.',
    [['右下腹壓痛 (McBurney)', 'Tenderness over the right lower quadrant with positive McBurney point and rebound tenderness.']]]
];
```

One "fill all normal" button, then edit the abnormal systems. This is the highest-leverage button in the whole product.

### Problem-based A&P with scenario templates

Rows of `{problem, plan}`, add/remove freely, plus one-click admission scenarios that populate a full problem list (appendicitis, community-acquired pneumonia, AKI on CKD, decompensated heart failure, pyelonephritis, upper GI bleeding). Renumber plan lines continuously across problems when rendering.

### Dirty-flag protection on generated text

Any field the generator writes must stop being overwritten the moment a physician edits it, with an explicit "regenerate" action to opt back in.

```js
var manualEdits = {};
function setIfAuto(id, value) {
  if (manualEdits[id]) return;
  var el = document.getElementById(id);
  if (el && value) el.value = value;
}
```

Show the state ("3 fields locked from overwrite"). Without this, changing any dropdown silently destroys typed text — a defect that survived two releases in the reference implementation because nobody clicked *after* typing.

### Draft autosave and copy-to-clipboard

Clinical work is interrupted constantly: debounce-save the whole form to `localStorage`, restore on load, tell the user you did. And most physicians still paste into a hospital HIS — a one-click "copy full text" on the live preview is worth more than any styling.

---

## Part 3 — Matching a hospital's own paper form

Departments compare your output against the pre-printed form they already use. Matching it is what makes the tool feel official.

**Letterhead belongs in a repeating page header**, not the body — the paper form's header is on every page:

```
┌──────────────────────┬─────────────────────────┬───────────────┐
│      <醫院名稱>       │ 病歷號：                 │ 床號：         │
│   ADMISSION  NOTE    │ 姓　　名：               │ 生日：         │
│                      │ 身分證號碼：             │ 性別：         │
│                      │ 住院日期：115 年 02 月 18 日 │            │
└──────────────────────┴─────────────────────────┴───────────────┘
```

Keep the hospital name in **one constant** so re-branding is a single edit.

**Adopt the form's own heading style and order.** A Taiwanese form uses `中文(English)：`:

```
主訴(Chief Complaints)：      現在病歷(Present Illness)：
過去病史(Past History)：      藥物過敏(Drug Allergy)：
家族史(Family History)：      系統回顧(Review of Systems)：
理學檢查(Physical Examination)：
檢驗報告：                    檢查報告：
初步診斷(Impression)：        治療及計劃(Management and Plan)：
                                              主治醫師：
```

Note `檢驗報告` (lab values) and `檢查報告` (imaging/studies) are **separate sections** — don't merge them into one "labs & imaging" block. And `過去病史` carries four fixed subheadings: Disease / trauma or surgery / hospitalization / home medication reviews.

**Mirror the layout in the live preview** so the form is WYSIWYG. A preview that differs from the output is worse than no preview.

See `references/form-layout.md` for the full field inventory and the ROC-date helper.

---

## Part 4 — Exam report modules

Structure every modality the same way, per RSNA structured reporting:

> **indication → technique → comparison → findings → impression → recommendation**

Auto-populate technique per modality; let it be edited. Clinicians prefer reports organised into consistent sections and subsections.

| Modality | Anchor | Must capture |
|---|---|---|
| Echocardiography | ASE reporting standardization | LVEF, chamber dimensions, wall motion, diastolic function, **RV/TAPSE**, **IVC**, valves, pericardium, **BP at study**, **contrast/bubble study**, comparison |
| Abdominal ultrasound | — | liver echogenicity & focal lesions, biliary, CBD, pancreas/spleen, **both kidneys with size**, ascites |
| Upper GI endoscopy | LA classification | esophagus (LA grade A–D), **Z-line distance**, GEJ, stomach by region, ulcer stage (A1/A2, H1/H2, S1/S2), duodenum, **CLO test** |
| Colonoscopy | **ASGE/ACG 2024** | extent, **BBPS**, **withdrawal time ≥ 8 min** (raised from 6), **cecal landmark photo documentation**, polyps as **location × size × morphology × resection method** |

Two rules learned the hard way:

- **Stamp thresholds with their guideline and year.** The reference implementation shipped `Normal >= 6 min` for withdrawal time long after the 2024 update moved it to 8. A number with no provenance never gets revisited.
- **Derive the impression from the numbers.** LVEF < 40 / 40–49 / ≥ 50 should produce different diagnoses, impressions *and* follow-up recommendations. A positive CLO test should append eradication therapy to the plan automatically.

---

## Part 5 — Localisation (Taiwan)

- **ROC calendar** on the letterhead: `year − 1911`, rendered `115 年 02 月 18 日`.
- **Betel nut is a required social-history field**, beside smoking (pack-year) and alcohol. Combined smoking + alcohol + betel nut use carries a far higher oral-cancer risk than any one alone, and hospital intake forms ask for it.
- **TOCC** (travel / occupation / contact / cluster) is expected in the social history.
- **身分證號碼 is separate from 病歷號.** The national ID is a stronger identifier than the chart number — see Part 6.
- UI labels bilingual (`主訴 (Chief Complaint, CC)`); generated note body in English.
- Machine translation of dictated Chinese is **general-purpose, not medical**. Always label the output as requiring review.

---

## Part 6 — PHI and safety

Non-negotiable in this domain:

- **Never commit reference scans of real charts.** A hospital form sample carries chart number, name, **national ID**, birth date and bed number. Take the layout, add the folder to `.gitignore`, and say so — git history is effectively permanent, and these repos get pushed to GitHub.
- **Gate the app before collecting national IDs.** A publicly reachable, unauthenticated endpoint that writes to the author's Drive is tolerable for a demo with fake data; it is not once the form asks for 身分證號碼. Ship the passcode switched on, or don't ship the field.
- **De-identify anything you ask a user to upload.** Request redacted samples up front; layout is what you need, not content.
- **Keep the disclaimer in the product**, not just the docs: the tool records and formats, it does not diagnose.

---

## Part 7 — Verification

The web layer of these systems cannot be exercised from a terminal, so add a **self-test function that drives the real document generator with dummy data and deletes what it creates**. Run it after every change to the report layout.

This exists because a static audit — syntax, call resolution, DOM wiring — is structurally blind to whether a document API method exists. In the reference implementation `setFontColor` (a Sheets method) was chained onto a Docs paragraph, so *every save had failed since the first release* while all static checks passed. The self-test catches that class in one editor run.

Cover both branches of anything conditional (populated problem list *and* the empty fallback), plus the export-URL shape.

---

## Common Pitfalls & Solutions

| Pitfall | Why it happens | Fix |
| :--- | :--- | :--- |
| Physicians stop using the "complete" form | Each new section added typing | Every section ships a bulk normal/denied/pending button |
| Typed findings vanish | Generator rewrites outputs on every change | `manualEdits` dirty flag + explicit regenerate |
| Assessment can't be handed over | Diagnoses and orders in two unpaired boxes | Problem-based rows: one problem, one plan |
| Output "doesn't look like our form" | Custom letterhead and heading style | Copy the department's heading text, order and letterhead; repeat it in a page header |
| Preview disagrees with the document | Two independent renderers | Build both from the same field set; mirror the layout |
| Stale clinical thresholds | Numbers with no provenance | Record guideline + year beside every threshold |
| Real patient data in git | Reference scans dropped into the repo | `.gitignore` the folder; request de-identified samples |
| Save silently broken for months | No end-to-end path exercised | Self-test that generates and deletes a real document |
| ROS unusable | Checkboxes can't express positive/negative/unset | Tri-state chips + "all negative" |

## Related

- **`gas-medical-webapp-generator`** — the Google Apps Script platform layer: deployment, access levels, passcode gating, Sheets schema evolution, Docs/PDF/Word export.
- `references/form-layout.md` — full hospital-form field inventory, ROC date helper, section-to-field mapping.

# AGENTS.md — 2026 Consciousness and binocular rivalry

Instructions for OpenCode / Kimi K3 agents and swarm workers. `CLAUDE.md` is the master rule set. This file must not contradict it; if a conflict appears, follow `CLAUDE.md` and report the conflict to the orchestrator.

## 1. Project goal

Explain the key findings, methods, and implications of Doris Tsao's lab preprint from October 2026 (bioRxiv, Hesse et al. 2026) on consciousness and binocular flash suppression (雙眼閃光抑制, a variant of binocular rivalry 雙眼競爭). The audience is the general public. Four deliverables:

- Motion-explainer video (zh-TW)
- HTML deck (zh-TW)
- PowerPoint deck (English)
- Personal homepage blog post (zh-TW)

## 2. Folder map

- `research/raw/`, `research/01`–`08`: Phase 1 outputs. **Read-only for Phase 2.**
- `research/05_glossary.csv`: zh-TW terminology source.
- `research/06_fact_sheet.json`: fact source. Each fact has an `id` (e.g., F39) and a `status`.
- `research/08_qa_report.md`: independent QA findings from Phase 1.
- `research/09_fix_log.md`: fixes applied after QA (incl. F40 restored). `research/06_fact_sheet_README.md`: fact-sheet fields and status legend.
- `phase2/00_brief/`: brief and `style_refs/` (reference files for style).
- `phase2/video/`, `phase2/html_deck/`, `phase2/pptx/`, `phase2/blog/`, `phase2/qa/`: Phase 2 outputs.
- `.claude/skills/<name>/SKILL.md`: skills (see section 6).
- `handoffs.md` and `task_manifest.json`: Phase 2 handoff and task list (to be created by the orchestrator).

## 3. Workflow

Jev-engineering two-phase process. Phase 1 is complete in Claude Code. Phase 2 runs here in OpenCode with a Kimi K3 swarm.

1. Brief stress-test: `grill-with-docs` with the human, covering the brief (P2-00) and the plan.
2. Canary gate: **P2-00 brief is a canary. A human must review and approve it before any fan-out.** No worker starts before approval.
3. Parallel generation by the swarm roles in section 4.
4. Each deliverable passes `verify-with-rubric` in an isolated sub-agent before it counts as done.
5. Publishing, deploying, and pushing are performed only by a human.

## 4. Swarm roles and output ownership

Each worker writes **only** to its own folder. Each deliverable folder also contains its own `sources.md`.

| Task ID | Role | Writes only to | Notes |
|---|---|---|---|
| P2-00 | Brief (canary) | `phase2/00_brief/` | Human review required before fan-out |
| P2-V1 | Video script and storyboard | `phase2/video/storyboard/` | Includes `sources.md` for the video |
| P2-V2 | Video render (Remotion) | `phase2/video/render/` | Renders from P2-V1 storyboard only |
| P2-H1 | HTML deck (zh-TW) | `phase2/html_deck/` | Includes `sources.md` |
| P2-P1 | English PPTX | `phase2/pptx/` | Includes `sources.md` |
| P2-B1 | zh-TW blog post | `phase2/blog/` | Includes `sources.md` |
| P2-Q1 | QA and rubric verification | `phase2/qa/` | Reads all of `phase2/` for grading; writes only to `phase2/qa/`; must not grade its own output |

Workers may read `research/` and `phase2/00_brief/` as inputs. Workers must not read or write another task's output folder, except that P2-Q1 may read all `phase2/` folders for grading.

## 5. Content rules (hard; same as CLAUDE.md)

1. **Facts**: use only facts with `status: "verified"` from `research/06_fact_sheet.json`. Cite each fact id in `sources.md`.
2. **secondary_only**: may be used only if labeled "初步" or "待證實" (English deliverables: "preliminary" or "pending confirmation").
3. **unverified and contradicted**: never use, including as a counterpoint. Example: F57 "consciousness has a frame rate" (contradicted) must not appear. F40 (`p = 3×10^-40`) was corrected to verified (see `research/09_fix_log.md`); cite it only together with its comparison context (conscious vs suppressed gain), never as an effect size (the effect size is the 1.21 ratio, F39).
4. **Preprint disclaimer**: every deliverable must state "bioRxiv 預印本、尚未經同儕審查". The English PPTX must state "bioRxiv preprint, not yet peer reviewed".
5. **Paradigm**: describe as binocular flash suppression (雙眼閃光抑制), a variant of binocular rivalry (雙眼競爭).
6. **Forbidden phrasing**: never say "意識有影格率" or "意識的幀率" (Tsao rejected this). No overclaims such as "solves consciousness".
7. **2020 numbers**: the 2020 eLife figures (e.g., 93 / 57 / 73) must be labeled as 2020 and must not be attributed to the 2026 Hesse et al. study.
8. **GNWT / IIT**: these are our interpretation. Do not attribute them to Tsao or Hesse et al.
9. **Terminology**: zh-TW terms follow `research/05_glossary.csv`. Use Taiwan usage (資訊, 演算法, 皮質, 顳葉). No Simplified Chinese or PRC usage.
10. **Units**: frequency in Hz, time in ms (e.g., 15 Hz, about 60 ms).
11. **sources.md**: required for every deliverable. List every fact id used, its status, and where it appears.
12. **No invented facts**: if information is missing, mark it "待證實" or remove it. Never fill gaps from memory.

## 6. Skills (path: `.claude/skills/<name>/SKILL.md`)

Pre-work:
- `grill-with-docs`: stress-test the brief and plan with the human before fan-out; produces ADR and GLOSSARY. Human-invoked only (`disable-model-invocation: true`). Depends on `grilling` and `domain-modeling`.
- `grilling`: the interview flow used by `grill-with-docs`.
- `domain-modeling`: write or edit GLOSSARY and ADR files.
- `map-vs-territory`: diagnose brief gaps when a task is vague or a previous output looked right but was wrong.
- `blindspot-pass`: before starting, list the unstated assumptions and undefined edges in the brief. Output a list only, no content.
- `reference-anchor`: anchor style to concrete files in `phase2/00_brief/style_refs/` rather than prose descriptions.
- `decision-first-plan`: order the plan by how likely the human is to change each decision; decisions first.

During execution:
- `deviation-log`: record every non-obvious assumption and deviation during swarm runs. Choose the conservative option and log it; do not stall waiting for answers.

Before acceptance:
- `comprehension-quiz`: the human must understand the key judgment calls in each deliverable before accepting it.
- `verify-with-rubric`: **mandatory gate for subjective outputs (video, deck, blog).** A separate, context-isolated sub-agent grades against the rubric. The producer never self-grades.

Style references (`phase2/00_brief/style_refs/`): `soil-html-deck_SKILL.md`, `soil-deck-pipeline_SKILL.md`, `publish-lab-blog_SKILL.md`, `publish-lab-blog_PITFALLS.md`, `personal-blog-post-writing_SKILL.md`, `Thariq_finding_unknown_README.md`. Use these via `reference-anchor`. Do not run any publish step from these references.

## 7. Forbidden actions (all agents)

- Publishing, deploying, or pushing anything (including `publish-lab-blog` steps). Human only.
- Spending money, subscribing to paid services, or calling paid APIs without human approval.
- Editing any file under `research/`.
- Inventing facts or filling gaps from memory.
- Sending messages or external notifications.
- Installing packages or changing permissions automatically. This machine has no Python; use node for scripts. NotebookLM CLI auth is currently broken (`research/raw/nlm_status.md`); report auth errors, do not work around them or store tokens.
- Editing `CLAUDE.md` or `AGENTS.md`.
- Fanning out before human approval of P2-00.

## 8. Acceptance (per deliverable)

A deliverable is done only when all of the following hold:
(a) it passes `verify-with-rubric`;
(b) it contains the preprint disclaimer;
(c) it cites only verified facts, with secondary_only facts labeled;
(d) it ships `sources.md`;
(e) zh-TW terminology checks pass (not applicable to the English PPTX).

If any check fails, return the item to its owner. Do not mark it complete on your own.

## 9. Reporting

Report the task ID, the files written, and the checks performed. Report errors briefly. Do not retry silently. If a dependency or input is missing, stop and report it.

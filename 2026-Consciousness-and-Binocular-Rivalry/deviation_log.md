# Deviation Log — Phase 2 (OpenCode + Kimi K3 swarm)

Goal: produce four deliverables from `research/` (read-only) — zh-TW explainer video, English HTML deck, English PPTX, zh-TW blog post — per `task_manifest.json`, with P2-00 brief as human-approved canary before fan-out.

Exit condition: all four artifacts pass `verify-with-rubric` + P2-Q1 cross-artifact QA; nothing published (human-only).

## Entries

- **D1 — grill-with-docs skipped (user decision, 2026-10-29).** Expected: formal human-invoked grill-with-docs stress-test before P2-00. Found: user instructed to take over and proceed; formal skill is human-invoked only. Chosen: capture the same decision surface via structured Q&A (5 open items from handoffs.md §4.4), keep the P2-00 canary human review as the hard gate. Discarded: blocking until user runs grill-with-docs themselves. Risk: low — canary review still catches spec defects before fan-out.

- **D2 — HTML deck language changed zh-TW → English (user decision).** Manifest P2-H1 amended. zh-TW glossary check not applicable to this artifact (same rule as the English PPTX, CLAUDE.md §8e). zh-TW coverage now: video + blog only.

- **D3 — Video duration targeted at ~240 s (user decision).** Hard acceptance range stays 180–300 s; P2-V1 aims at 240 s.

- **D4 — TTS narration approved in principle (user decision).** Expected (manifest): subtitles only, no TTS. Chosen: P2-V2 amended to include zh-TW TTS track. TTS engine NOT yet chosen — free/local-first (e.g., edge-tts via network_egress, or Windows SAPI offline); any paid API returns to the human for spend approval. Decision deferred to P2-V2 kickoff because it does not affect P2-V1 script text.

- **D5 — Remotion `npm install` approved (user decision).** Scope limited to `phase2/video/render/` (local, non-global). This is the §7 "installing packages" human approval, recorded here.

- **D6 — Moonshot API key / jev models.json open item: resolved by architecture change.** handoffs.md open item 3 assumed direct Moonshot API wiring. In OpenCode, subagents inherit the session model (kimi-k3) via the configured provider (OpenCode Go). No MOONSHOT_API_KEY, no models.json edit, no credential in any file.

- **D7 — preflight() substituted.** No live Jev runtime on this machine (no Python). Substitute: `node phase2/00_brief/tools/verify_manifest.js` (PASS, hash verified) + dependency/spec review by orchestrator. Manifest `confidence: 0.85` remains planner-specified, not a live decide() result — unchanged from handoff note.

- **D8 — Blog front-matter target kept at manifest default.** handoffs.md open item 4 listed the blog front-matter target as pending; the user made no contrary choice, so P2-B1 keeps its manifest spec: publish-lab-blog style with front-matter per `phase2/00_brief/style_refs/publish-lab-blog_SKILL.md`. Conservative option: matches existing spec, reversible at P2-B1 review.

- **D9 — Interactive 3D BFS website added (user decision in brief.md §3, 2026-10-29).** User requested a 3D-featured interactive Binocular Flash Suppression task website connectable to Blender/3D concepts before Phase 2 fan-out, embeddable into HTML deck and blog. Created `phase2/interactive_bfs/index.html` (self-contained, offline/Cloudflare compatible with 3D cortex mesh, 4 face patches ML/AM/PO/PVL, red-cyan/side-by-side psychophysics trial engine, and ~15 Hz multiplexing simulator) and `phase2/interactive_bfs/sources.md` citing 14 verified facts + F56 preliminary.

- **D10 — Blog integrated to kidney-cognition-lab homepage (user request, 2026-10-29).** User requested integrating blog into homepage. Cloned repo, created standalone house-styled `blog/consciousness-binocular-rivalry.html`, registered card in `index.html` (#panel-lecture .teach-grid) and bumped `sitemap.xml`. Committed (`b6be63f`) and pushed to `main` via PowerShell. Local copy saved in `phase2/blog/consciousness-binocular-rivalry.html`.

- **D11 — Remotion explainer video rendered to MP4 (user request, 2026-10-29).** User requested exporting physical MP4. Generated 1920x1080 30fps H.264 / AAC video `phase2/video/render/out/explainer_zh_tw.mp4` exactly matching storyboard.json (12 shots, 240.00s duration, verified via ffprobe).

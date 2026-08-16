# Hospital Staff Attendance System — Handoff

## Status

Discovery is **partially resumed**. Architecture, stack, biometric delivery, and doc language are now confirmed (see "Decisions confirmed on 2026-07-29"). Seven decision areas remain open. Do not initialize Git or write application code until those are confirmed and the user agrees that shared understanding has been reached.

Target workspace: `D:\2026 Hospital management system`

Current workspace state:

- `handoff.md`, `CLAUDE.md`, `.gitignore` present.
- `backend/` scaffolded at the user's explicit instruction (2026-07-29), overriding the earlier "no application code" hold. Built only against confirmed decisions; the seven open items are marked in-code as `TODO(open-decision)` rather than guessed.
  - 7 modules, 15 tables, 29 API endpoints, 19 tests passing.
  - Verified on CPython 3.11.15 (no 3.12 present on this machine); full `requirements.txt` installs cleanly.
  - Implemented: event pairing, work-hour/overtime-candidate calculation, correction state machine, feature flags, audit writes, Excel/Word/plot generation.
  - Not implemented: kiosk offline queue, schedule Excel import, full role/permission matrix.
- `frontend/` not started.
- Not a Git repository.

## Project objective

Build a web-based, cross-platform staff attendance, scheduling, work-hour, and overtime system for a 128-bed regional hospital with about 110 staff in Taoyuan City, Taiwan.

The system is independent from the hospital's existing HIS during Phase 1. The original [`Ebo1996/PHP-Hospital-HMS`](https://github.com/Ebo1996/PHP-Hospital-HMS) is a read-only functional reference, not the production codebase.

The methodology in [`Thariq_finding_unknown`](https://github.com/ckt520728/claude-skills/tree/master/Thariq_finding_unknown) must be incorporated as a governance and delivery workflow.

## Confirmed decisions

1. The project is a sandbox/pilot and must not directly replace the formal HIS or EMR.
2. Preserve the original PHP HMS as a read-only reference under a future `reference/` area; build the pilot independently.
3. `thinking_unknown` is a governance and continuous-improvement layer:
   - map knowns and unknowns;
   - run blindspot and reference-anchor passes;
   - review decision-first plans;
   - record deviations;
   - verify against a predefined rubric;
   - require comprehension before acceptance.
4. `thinking_unknown` must not produce diagnoses, prescriptions, orders, triage decisions, or raw clinical notes.
5. Phase 1 scope was superseded and is now a workforce attendance system, not an ADT/bed-management pilot.
6. Required functional areas, each independently configurable:
   - staff presence/absence;
   - check-in/check-out and work hours;
   - physician OPD schedule control;
   - inpatient ward-level visiting-doctor round sign-in;
   - OPD nurse attendance;
   - ER and inpatient nurse attendance;
   - non-medical staff attendance;
   - nighttime on-duty physician or nursing-specialist attendance;
   - holiday physician or nursing-specialist attendance;
   - total work-hour and overtime calculation.
7. Required outputs: Excel, Word, and statistical plots.
8. Browser-based use on desktop and laptop computers is required.
9. Biometric verification:
   - use hospital-controlled kiosks/terminals and qualified biometric or platform authentication;
   - do not build custom fingerprint/face recognition;
   - never store raw fingerprint images, face images, or recoverable biometric templates;
   - store only necessary signed verification-event metadata;
   - provide a governed non-biometric exception path.
10. Phase 1 attendance remains in shadow mode:
    - run in parallel with existing HR/paper records;
    - overtime is a candidate until approved;
    - corrections require employee request, supervisor approval, HR confirmation, and audit history;
    - do not feed payroll automatically.
11. Inpatient visiting-doctor recording is ward-level `Clinical Round Sign-in` only:
    - no patient name, chart number, diagnosis, or patient-level visit data;
    - presence does not prove completion of clinical assessment or documentation.
12. Scheduling:
    - standard Excel template import;
    - authorized web editing;
    - supervisor-approved schedule versions;
    - every swap/edit retains previous value, actor, timestamp, and reason;
    - `Planned Shift` and `Attendance Event` are separate records and cannot overwrite one another.
13. Phase 1 identity:
    - do not collect or reuse HIS passwords;
    - provision separate pilot accounts from an HR-approved roster;
    - use MFA/passkey;
    - retain an OIDC/LDAP integration boundary;
    - integration cannot be claimed until hospital IT and the HIS vendor confirm an authorized interface.
14. Deployment and data handling:
    - Taiwan is the governing jurisdiction;
    - production-sensitive data is hospital/on-premises first;
    - development and test environments use synthetic or irreversibly de-identified data;
    - external AI services receive no identifiable staff/biometric/clinical data;
    - require encryption, least privilege, audit trail, backup, and an offline/degraded-mode plan.
15. Phase 1 is staff-only and not a public patient portal.
16. Phase 1 remains isolated from the existing HIS.

## Terminology already distinguished

- **Attendance Check-in/Check-out**: staff start/end attendance event.
- **On-duty Sign-in**: nighttime, holiday, or on-call arrival evidence.
- **Clinical Round Sign-in**: ward-level physician presence; not a patient-level record and not proof of completed care.
- **Planned Shift**: approved expected schedule.
- **Attendance Event**: observed check-in/check-out evidence.
- **Overtime Candidate**: calculated time that has not yet completed approval.

## Decisions confirmed on 2026-07-29

17. Architecture: **modular monolith** (the previously pending question — answered yes). Internal modules: Attendance, Scheduling, Overtime, Reporting, Identity, Audit, Unknown Governance.
18. Stack: **Python 3.12 / FastAPI / SQLAlchemy / Alembic** backend, **React 18 + TypeScript + Vite** frontend, **PostgreSQL 16** database. Chosen for the strongest native support of the three required outputs (`openpyxl`, `python-docx`, `matplotlib`).
19. Biometric delivery: **WebAuthn platform authenticator on hospital-controlled kiosks** (Windows Hello fingerprint/face). Server stores only `credential_id`, public key, signature counter, verification time, station ID.
20. Documentation language: **Traditional Chinese**, with English technical terms retained.
21. Feature flags are named per requirement a–j and are runtime-toggleable; disabling a flag hides the UI and returns 404, and never deletes existing data.

Additional reference recorded: [`yash-rana0101/Employer-checkIn-CheckOut-System`](https://github.com/yash-rana0101/Employer-checkIn-CheckOut-System) is a **pure SQL script**, not an architecture. Its value is the four aggregation metrics only — first check-in, last check-out, total out count, total work hours. Place read-only under `reference/employer-checkin/`.

## Resume point

`CLAUDE.md` now exists and is the binding operating-rules document. It supersedes the `AGENTS.md` artifact named below.

Ask one question at a time, with a recommended answer, as required by `grilling`.

Still open, in recommended order:

- kiosk/terminal integration contract and **offline queue behavior** (highest risk — a ward kiosk losing network must not lose attendance evidence);
- authoritative work-hour/overtime policy owners and Taiwan labor-rule review (labor-standards parameters are currently policy defaults marked "not legally reviewed");
- role/permission matrix and segregation of duties;
- exception and correction state machine (draft state machine already recorded in `CLAUDE.md` §10 — needs user confirmation);
- report templates, filters, retention, and access;
- backup, recovery objectives, monitoring, and incident response;
- pilot cohort, duration, success rubric, and go/no-go gates.

Run a blindspot pass before finalizing the design. Close discovery with a decision-first plan. Do not implement until the user explicitly confirms shared understanding.

## Expected initialization artifacts after discovery closes

- ~~`AGENTS.md`~~ — superseded by `CLAUDE.md` (created 2026-07-29, Traditional Chinese).
- `CONTEXT.md` — domain glossary only.
- `docs/adr/` — only for qualifying hard-to-reverse decisions.
- `handoff.md` — updated continuation summary without duplicating the above.
- Git repository baseline in the exact target workspace.
- Read-only reference placement strategy for the upstream PHP HMS.

## Suggested skills

- `grill-with-docs`
- `grilling`
- `domain-modeling`
- `handoff`
- `codebase-design`
- `security` or an equivalent healthcare-security review skill if available
- `github:github`


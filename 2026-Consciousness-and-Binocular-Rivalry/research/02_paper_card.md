# Paper Card: Hesse et al. 2026 (論文卡)

Source tags: [H] = raw/web_biorxiv_hesse2026_fulltext.md; [T] = raw/web_tsao_x_and_press.md; [R] = raw/web_related_papers.md. Section names follow the raw files.

## Status warnings (狀態警示)
- PREPRINT, NOT PEER REVIEWED. [H, header: "NOT peer reviewed"]
- The raw text [H] is a small-model summary of the page, NOT verbatim (stated in [H] line 2). Every number below must be checked against the PDF before publication.
- Tsao X posts were obtained only via search snippets and secondary articles (X returned HTTP 402); treat as SECONDARY. [T, header]

## 1. Bibliography (書目資訊)
- Title: "Rapid alternation of conscious and suppressed stimulus representations in the primate brain" [H, header]
- Authors: Janis K. Hesse (UC Berkeley); Frank F. Lanfranchi (UC Berkeley; Caltech BBE); Conor McGrory (Princeton Neuroscience Institute); Yuelin Shi (UC Berkeley; Caltech BBE); Tatiana A. Engel (Princeton); Doris Y. Tsao (UC Berkeley; HHMI) [H, header]
- DOI: 10.64898/2026.10.15.759299; bioRxiv v1, posted 2026-10-16 [H, header]
- URL: https://www.biorxiv.org/content/10.64898/2026.10.15.759299v1 [H, header]
- Abstract text is a paraphrase; verbatim not captured [H, Abstract].

## 2. Design (實驗設計)
- Paradigm: binocular FLASH SUPPRESSION (a rivalry variant), not classic free rivalry. A priming image goes to one eye for 1 or 2 s, then a second image is flashed to the other eye; the flashed image usually dominates. [H, Paradigm]
- Monkeys made NO report. The percept was validated in 14 human participants by button press. Monkey states were inferred from neural activity (LLR + HMM), not from monkey report. [H, Paradigm]
- Human validation: flashed percept reported on 82% of trials; flashed vs primed t(13)=9.4, p=4e-7; window 300-1000 ms after flash; report latency 0.86 +/- 0.05 s. [H, Paradigm]
- Experiment 1: priming 2 s, test 4 s, blank 500 ms; 10 faces forming 25 pairs; 7 sessions (monkey A) + 3 (monkey M). [H, Paradigm]
- Experiment 2: priming 1 s, test 1 s, blank 250 ms; 1500 faces forming 750 pairs; subset of 60 faces with about 20 trials per condition; 5 sessions (A) + 4 (M). [H, Paradigm]
- Display: red/cyan anaglyph goggles; stimuli 7 deg; 60 x 44 deg LCD. [H, Paradigm]
- Note: the 2020 eLife paper inferred percept from eye movements; the visible 2026 text does not describe eye-movement inference. [H, Paradigm NOTE]

## 3. Methods (方法)
- Subjects: two male rhesus macaques (A, M). [H, Subjects and recording]
- Neuropixels 1.0 NHP probes; Kilosort3; single and multi-units. [H, Subjects and recording]
- Areas: IT face patches ML and AM (fMRI-localized, faces > objects); PFC patches PO (orbitofrontal) and PVL (ventrolateral). [H, Subjects and recording]
- Sample: 3501 visually responsive neurons across sessions; PFC analysis 661 neurons (300 PCA components; IT 500); example raster 429 simultaneous cells; gain analysis 543 cells. [H, Subjects and recording]
- Sessions: 9 (main state analyses); 19 (two-state vs one-state); 10 (single-trial decoding); 7 of 9 (cross-region). [H, Subjects and recording]
- Analysis: Poisson LLR in 10 ms bins; two-state Poisson HMM (hmmlearn, Baum-Welch, Viterbi); sign-flip permutation tests, 1e5 permutations. [H, Discussion, Methods/stats]

## 4. Main results (主要結果)
IT:
- Alternation about 15 times per second [H, Results (IT) / Abstract]; Tsao: "~15 times every second" [T, Tsao on X].
- Dwell time: likelihood autocorrelation time constant 67 ms (mean dwell D=67 ms, median about 46 ms); HMM (5 ms bins) median dwell 64 ms (state 1) and 59 ms (state 2), plateau near 60 ms across bin sizes. [H, Results (IT)] Report as "roughly 60 ms (tens of ms)" [T, Discrepancy flags].
- More than an order of magnitude faster than rivalry switches (~0.5 Hz). [H, Results (IT)]
- Average binocular modulation weak: slope 0.23 vs unambiguous (5550 cell-stimulus pairs, p=8e-133). [H, Results (IT)]
- Reconstruction: in state 1 conscious-face explained variance >80% for SOME features (priming ceiling >90%); suppressed face near chance; reversed in state 2. [H, Results (IT)]
- Single-trial 10-class decoding (chance 10%): full window 40% conscious / 34% suppressed; state 1 >61% conscious vs 4% suppressed (t(9)=11.0, p=2e-6); state 2 reversed (t(9)=-13.7, p=3e-7). [H, Results (IT)]
- Held-out neurons: EV t(29)=17.5, p=6e-17; state 1 t(9)=7.6, p=3e-5; state 2 t(9)=-6.5, p=1e-4. [H, Results (IT)]
- Two-state beats one-state model in all 19 sessions (t(18)=4.84, p=1e-4). [H, Results (IT)]
- Single-cell gain: ratio 1.21 (conscious-in-state-1 vs suppressed-in-state-2), r=0.90; mean firing slightly higher in state 2; linear decoder separates states at 66%. [H, Results (IT)]
- Same neurons switch content (no separate populations). After gain equalization the residual binocular-unambiguous correlation vanishes (r=-0.02, p=0.31): averaging explains weak modulation. [H, Results (IT)]
- Weak ML-AM coordination; authors say results "do not provide strong evidence" for it. [H, Results (IT)]

PFC:
- Reconstruction lower: priming EV <80%, <30% for shape features. [H, Results (PFC)]
- State 1 tracks conscious, state 2 suppressed: EV t(29)=14.2, p=1e-14; decoding p=1e-5 (n=30 pairs). Held-out halves: EV p=3e-4; decoding p=0.03. Modulation slopes 0.91 (state 1), -0.52 (state 2). [H, Results (PFC)]
- Authors: "may therefore be a broad cortical phenomenon". [H, Results (PFC)]

## 5. Controls (對照)
Within-trial subsampling; shuffled templates (EV < 0); On/Off gain fluctuations do not explain states (kappa about 0); averaging, conscious-only and uncoordinated models each fail at least 3 of 4 tests; real data beat averaging model by delta EV 8.2% (p=0.007); initial circular analysis addressed with held-out neurons. [H, Results (IT) Controls; Results (IT) Reconstruction]

## 6. Authors' limitations and open questions (限制與開放問題)
- Open question: "why do representations in some micro-epochs reach awareness, whereas others do not?" [H, Discussion]
- Speculation: suppressed epochs explore alternative interpretations; conscious epochs carry the working hypothesis routed to report/action. [H, Discussion]
- Stated limitations: routing mechanism speculative; switching mechanism unknown; only two monkeys; initial circularity (addressed); weak cross-patch coordination; lower PFC quality. [H, Discussion Limitations]
- Suppressed stimulus is not a weak residue; occupies the same face space in its own epochs. [H, Discussion]
- Discussion links timing to attentional sampling, theta-phase working-memory access, orbitofrontal alternation, hippocampal theta flickering. It does NOT explicitly cite GNWT/IIT or discuss alpha. [H, Discussion]
- Interpretive caveat (not from authors' text): 2 monkeys, face stimuli only, no monkey report; generalization beyond faces UNVERIFIED.

## 7. Authors' public clarifications (作者公開澄清) [SECONDARY]
- Tsao clarification thread: "We have not shown that 'consciousness has a frame rate.' ... we report that inferotemporal and prefrontal cortex alternate between conscious and s[uppressed]..." (truncated snippet) [T, Tsao on X, Clarification thread]. Full four points UNVERIFIED (only point 1 seen).
- Per search summary: consciousness depends on many areas; paper covers only a few nodes. [T, Tsao on X]
- Launch thread claims ("overturns decades of thinking", "pure correlate of conscious awareness") are promotional framing. [T, Tsao on X, Thread 1]
- Authors per Glitchwire: findings "expose a limitation of searching for NCC within the average activity of specific brain regions". [T, Glitchwire]
- Press "consciousness is a 15-times-a-second flicker" is journalistic overstatement contradicted by the clarification. [T, Other secondary coverage]
- Glitchwire caveat: "timing, not area" framing goes beyond what the preprint shows. [T, Glitchwire]

## 8. Lineage: predecessor papers (前作脈絡)
- Hesse JK, Tsao DY (2020), eLife 9:e58360, "A new no-report paradigm reveals that face cells encode both consciously perceived and suppressed stimuli." Macaque IT face patches; percept inferred from eye movements, no active report; many IT neurons tracked the percept; both perceived and suppressed stimuli decodable on single trials. [R, item 1]. Link to 2026: same group and paradigm family; 2026 adds the sub-100 ms alternation (inference by the card author, not stated in [R]).
- Shi Y, Bi D, Hesse JK, Lanfranchi FF, Chen S, Tsao DY (2026), Nature, "Rapid concerted switching of the neural code in the inferotemporal cortex," DOI 10.1038/s41586-026-10267-3. Face cells switch from general face-detection code to face-specific code after a concerted population event lasting <20 ms; faces only, not objects. Publication date discrepant: Mar 25 2026 (Caltech news) vs May 7 2026 (Caltech repository). Preprint bioRxiv 2023-12-06. [R, item 2]. Shared authors (Hesse, Lanfranchi, Shi, Tsao) [H, header; R, item 2].
- Peer-review status of these two: Nature paper published per [R]; eLife published per [R]. Details beyond abstracts UNVERIFIED.

## 9. Discrepancy flags (差異標記)
- Neuron counts: "thousands" (press) vs 3501 total / 543 / 429; consistent if total. [T, Discrepancy flags]
- Dwell: ~60 ms (press) vs 67 ms mean / 46 ms median / 64 & 59 ms HMM. [T; H]
- Abstract says about 15/s; 1/0.067 s is about 15 Hz, a rough consistency check by the card author, not from sources.
- Older notes calling this "binocular rivalry" should read "binocular flash suppression". [T, Discrepancy flags]

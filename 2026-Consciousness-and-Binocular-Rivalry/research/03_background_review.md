# Background Literature Review: Positioning Hesse et al. 2026

Task P1-03. Audience: general-audience content project. Sources: raw files in research/raw (web_related_papers.md, web_biorxiv_hesse2026_fulltext.md) plus textbook knowledge. Tags: [RAW] = taken from the project raw files; [KNOWLEDGE] = well-established classic, from memory, not re-fetched; UNVERIFIED = year/venue/detail not certain. Hesse et al. 2026 is a bioRxiv preprint, NOT peer reviewed, and the raw file is a small-model summary, so numbers must be checked against the PDF.

---

## 1. Binocular rivalry and flash suppression basics (雙眼競爭、閃光抑制)

When the two eyes see different images, we do not see a blend. Perception alternates between the two images, each dominating for a few seconds. This is **binocular rivalry** (雙眼競爭). The effect is that the stimulus stays constant while the percept changes, which makes it a classic tool for separating "what hits the retina" from "what is consciously seen".

- Wheatstone (1838), "Contributions to the physiology of vision. Part the first", *Philosophical Transactions of the Royal Society of London*. He built the stereoscope and described rivalry between dissimilar images. [KNOWLEDGE]
- Levelt (1965), *On Binocular Rivalry*, Institute for Perception RVO-TNO, Soesterberg (monograph). Levelt's propositions describe how stimulus strength affects dominance and suppression durations. [KNOWLEDGE]
- Wolfe (1984), "Reversing ocular dominance and suppression in a single flash", *Vision Research*. Introduced **flash suppression** (閃光抑制): an image shown to one eye is followed by a new image flashed to the other eye, which reliably takes over. [KNOWLEDGE; exact volume UNVERIFIED]
- Logothetis & Schall (1989), "Neuronal correlates of subjective visual perception", *Science*. Monkeys reported motion direction during rivalry. Some cells in area MT/MST followed the percept. [KNOWLEDGE]
- Leopold & Logothetis (1996), "Activity changes in early visual cortex reflect monkeys' percepts during binocular rivalry", *Nature*. Modulation was present in V1/V2/V4 but a minority of cells, and more common in later areas. [KNOWLEDGE]
- Sheinberg & Logothetis (1997), "The role of temporal cortical areas in perceptual organization", *PNAS*. A large fraction of inferotemporal (IT, 下顳葉皮質) cells followed the percept, although the average modulation amplitude was not a pure seen/not-seen signal (see the takeaway below). [KNOWLEDGE; the exact fraction is from memory, UNVERIFIED]
- Blake & Logothetis (2002), "Visual competition", *Nature Reviews Neuroscience*. Standard review. [KNOWLEDGE]

The takeaway for the project is that the 1990s monkey work found the percept reflected weakly in early cortex and increasingly strongly in IT. Even in IT, the average modulation was far from a pure "seen/not seen" signal. The Hesse et al. 2026 preprint says exactly this: earlier studies found only weak modulation in high-level visual cortex [RAW]. Note that the 2026 preprint uses **flash suppression**, not free rivalry. A priming image goes to one eye for 1 or 2 s, and a second image is flashed to the other eye and usually dominates [RAW].

## 2. The neural correlates of consciousness (意識的神經相關物, NCC)

- Crick & Koch (1990), "Towards a neurobiological theory of consciousness", *Seminars in the Neurosciences* 2:263-275. Proposed that consciousness can be studied empirically by searching for neural activity that corresponds to conscious experience. [KNOWLEDGE]
- Koch, Massimini, Boly & Tononi (2016), "Neural correlates of consciousness: progress and problems", *Nature Reviews Neuroscience*. The NCC is defined as the minimal neural mechanisms jointly sufficient for a specific conscious experience. [KNOWLEDGE]

Rivalry and flash suppression are the main workhorse paradigms for NCC work, because the physical input is held constant while the experience varies. The conceptual problem is that "neural activity that tracks the percept" might reflect the consequences of consciousness (reporting, attention, decision) rather than consciousness itself. That is the report confound, covered next.

## 3. No-report paradigms and the report confound (無報告範式)

- Tsuchiya, Wilke, Frässle & Lamme (2015), "No-report paradigms: extracting the true neural correlates of consciousness", *Trends in Cognitive Sciences* 19(12):757-770. Argues that asking subjects to report contaminates NCC measurements with report-related activity (decision, motor, and attention processes), so the true NCC should be inferred in conditions where report is not required. [KNOWLEDGE; page numbers UNVERIFIED]
- Hesse & Tsao (2020), "A new no-report paradigm reveals that face cells encode both consciously perceived and suppressed stimuli", *eLife* 9:e58360. https://elifesciences.org/articles/58360 (PMC7676863) [RAW]. In macaque IT face patches the percept was inferred from eye movements without any active report. Many IT neurons tracked the conscious percept, and both the perceived and the suppressed stimulus could be decoded on single trials. Reviewers noted that single cells may multiplex the illusory percept and the physical stimulus. [RAW]
- Kingir, Segawa, Hesse, Kagan & Wilke (2025, bioRxiv), "Fixation shifts in a novel 'no-report' binocular rivalry paradigm induce saccade-related perceptual switches". https://www.biorxiv.org/content/10.1101/2025.02.09.637085v1 [RAW]. A caution that eye-movement-based inference can itself interact with perceptual switching.

The 2020 paper already contained a hint that the suppressed stimulus is still represented. The 2026 preprint pushes this further (Section 6). One difference to flag for scripts: in 2026 the monkeys made no report, and monkey states were inferred from neural activity (likelihood ratio and a hidden Markov model). The percept was validated by button press in 14 human participants (flashed percept on 82% of trials). The visible 2026 text does not describe eye-movement inference for the monkeys [RAW].

## 4. IT face patches (下顳葉臉部斑塊, ML/AM)

Macaque fMRI finds a handful of cortical regions that respond more to faces than objects. Recordings inside them show nearly all cells are face-selective.

- Tsao, Freiwald, Tootell & Livingstone (2006), "A cortical region consisting entirely of face-selective cells", *Science* 311:670-674. Middle face patch (ML). [KNOWLEDGE]
- Moeller, Freiwald & Tsao (2008), "Patches with links: a unified system for processing faces in the macaque temporal lobe", *Science* 320:1355-1359. Face patches are interconnected. [KNOWLEDGE]
- Freiwald & Tsao (2010), "Functional compartmentalization and viewpoint generalization within the macaque face-processing system", *Science* 330:845-851. Identity coding becomes viewpoint-invariant from ML (middle lateral) to AM (anterior medial). [KNOWLEDGE]
- Chang & Tsao (2017), "The code for facial identity in the primate brain", *Cell* 169:1013-1028. Face cells perform linear projections onto axes of a "face space" (臉空間). [KNOWLEDGE]
- Shi, Bi, Hesse, Lanfranchi, Chen & Tsao (2026), "Rapid concerted switching of the neural code in the inferotemporal cortex", *Nature*, DOI 10.1038/s41586-026-10267-3. Face cells switch from a general detection code to a face-specific code via a concerted population event lasting under 20 ms, for faces only, not objects. [RAW; publication date discrepancy: Mar 25 2026 per Caltech news vs May 7 2026 per Caltech repository]

Why this matters here: "face space" provides a way to read out which face a population is representing at any moment. This is what lets Hesse et al. 2026 decode the conscious face and the suppressed face, from the same neurons, in short time windows. The 2026 study recorded Neuropixels in ML and AM, plus two prefrontal face-related patches (PO and PVL), from two macaques [RAW].

## 5. Theories: GNWT vs IIT and the Cogitate 2025 collaboration (全域神經工作空間 vs 整合資訊理論)

- **Global neuronal workspace theory (GNWT, 全域神經工作空間理論).** Baars (1988), *A Cognitive Theory of Consciousness*, Cambridge UP [KNOWLEDGE]; Dehaene & Changeux (2011), "Experimental and theoretical approaches to conscious processing", *Neuron* 70:200-227 [KNOWLEDGE]. Consciousness is the "ignition" and broadcast of information across a fronto-parietal network, making it available for report and flexible use.
- **Integrated information theory (IIT, 整合資訊理論).** Tononi (2004), "An information integration theory of consciousness", *BMC Neuroscience* 5:42 [KNOWLEDGE]; Tononi, Boly, Massimini & Koch (2016), *Nature Reviews Neuroscience* [KNOWLEDGE; exact title UNVERIFIED]. Consciousness corresponds to the intrinsic cause-effect structure of a physical system, with a posterior cortical "hot zone" emphasized.
- **Cogitate Consortium (2025)**, "Adversarial testing of global neuronal workspace and integrated information theories of consciousness", *Nature*, 30 Apr 2025. Source: https://idw-online.de/en/news851431 (press report) [RAW]. 256 human participants; fMRI, MEG, iEEG; preregistered. No sustained posterior synchronization, which challenges IIT. A general lack of ignition at stimulus offset and limited prefrontal representation of some conscious dimensions challenges GNWT. Neither theory was decisively confirmed or refuted. [RAW]

**Important for positioning:** Hesse et al. 2026 does NOT explicitly cite GNWT or IIT [RAW]. Any script that frames the preprint as "a verdict on GNWT vs IIT" would be our own interpretation and must be labeled as such. A defensible, careful bridge is that both theories were tested largely with non-invasive human measures at coarse timescales, whereas the preprint is single-neuron/population level in monkeys on a ~60 ms timescale. The preprint's phrase "temporal selection beyond localization" and its speculation that conscious epochs carry content "routed to report and action circuits" [RAW] resemble workspace-style language but are not framed as a test of it. Also note the finding of PFC involvement: PFC face patches showed qualitatively similar alternation, with lower reconstruction quality [RAW]. This is of interest given the GNWT/IIT front-versus-back dispute, but the authors do not draw that link.

## 6. Rhythmic and temporal sampling of perception and attention (知覺與注意力的節律取樣)

A separate literature argues that perception and attention are not continuous but sample the world in discrete, rhythmic cycles.

- Busch, Dubois & VanRullen (2009), "The phase of ongoing EEG oscillations predicts visual perception", *Journal of Neuroscience* 29:7869-7876. [KNOWLEDGE]
- Landau & Fries (2012), "Attention samples stimuli rhythmically", *Current Biology* 22:1000-1004. Two competing locations are sampled alternately at about 4 Hz each (about 8 Hz in total). [KNOWLEDGE]
- VanRullen (2016), "Perceptual cycles", *Trends in Cognitive Sciences* 20:723-735. Reviews evidence that perception is rhythmic at roughly theta and alpha frequencies. [KNOWLEDGE]
- Fiebelkorn, Pinsk & Kastner (2018), "A dynamic interplay within the frontoparietal network underlies rhythmic spatial attention", *Neuron* 99:842-853; and Fiebelkorn & Kastner (2019), "A rhythmic theory of attention", *Trends in Cognitive Sciences* 23:87-101. Attention alternates at theta (about 4-8 Hz) between "sampling" and "shifting" states, associated with frontoparietal dynamics. [KNOWLEDGE; page numbers UNVERIFIED]

**How the 15 Hz micro-epoch finding relates.** According to the raw summary, the Hesse et al. population alternates between a conscious-content state and a suppressed-content state about 15 times per second, with median dwell of roughly 60 ms (mean 67 ms) [RAW]. This is more than an order of magnitude faster than perceptual switches in rivalry (about 0.5 Hz) [RAW]. The authors link their timing to rhythmic attentional sampling, theta-phase working-memory access, orbitofrontal alternation during decisions, and theta-paced hippocampal flickering, and suggest temporal structure may be a general organizing principle [RAW]. They do not discuss alpha rhythms [RAW].

Care points for content writers:
- 15 Hz is NOT a theta rhythm (theta is about 4-8 Hz), and it is above the usual alpha band (about 8-12 Hz) and in the beta range by conventional definitions. The preprint's link to theta/attention sampling is thematic ("temporal structure"), not a claim that the micro-epochs are the same oscillation. One possible reading, which is ours and not the authors', is that the state alternation is a faster process nested within slower cycles. Do not state this as a finding.
- Attention-sampling studies measure behavioral or LFP rhythms across spatial locations. The Hesse et al. alternation is in the content represented by a face-cell population for one location. These are different measurements.
- Per the preprint, the switching mechanism is unknown and the routing mechanism is speculative [RAW].

---

## Where Hesse et al. 2026 fits

Hesse JK, Lanfranchi FF, McGrory C, Shi Y, Engel TA, Tsao DY (2026), "Rapid alternation of conscious and suppressed stimulus representations in the primate brain", bioRxiv, DOI 10.64898/2026.10.15.759299, v1 posted 2026-10-16. NOT peer reviewed. [RAW]

1. **Within the rivalry tradition (Section 1).** It offers a candidate explanation, in this dataset only, for why the average percept-related modulation in high-level visual cortex is weak (preprint, not peer reviewed; two monkeys). Their account is that the average mixes two fast-alternating states. After equalizing gain, the residual binocular-versus-unambiguous correlation disappears (r = -0.02), so, according to the authors, averaging explains the weak modulation in this dataset [RAW].
2. **Within no-report work (Section 3).** It extends Hesse & Tsao 2020 from "both stimuli are decodable" to "both stimuli are decodable, but in alternating micro-epochs". Monkeys gave no report; the percept was validated in humans [RAW].
3. **Within face-patch work (Section 4).** It uses the face-space read-out from the Tsao lab system (ML/AM, plus PFC patches) to track which face is represented. Together with Shi et al. 2026 (sub-20 ms code switching), it depicts IT as a system with fast internal state changes [RAW].
4. **Relative to GNWT/IIT (Section 5).** It is orthogonal in framing. The preprint does not cite either theory. Whether the "conscious" epochs are those that get routed onward is an explicit open question and speculation in the paper [RAW].
5. **Relative to rhythmic sampling (Section 6).** It supplies a possible neuronal-population example of discrete temporal selection in perception, but at 15 Hz and in content rather than space. Treat connections to theta literature as the authors' suggestive discussion, not as established.

Limitations to mention (all from the preprint [RAW]): two monkeys; initial circular analysis (addressed with held-out neurons); weak ML-AM coordination; lower PFC reconstruction quality; mechanism unknown; state labels in monkeys are inferred from neural data, which makes the "conscious" label an inference from human validation.

Not independently checked: all numbers above come from the raw summary of the preprint. All items tagged [KNOWLEDGE] were not re-fetched. NotebookLM-exported root notes were not used as citations.

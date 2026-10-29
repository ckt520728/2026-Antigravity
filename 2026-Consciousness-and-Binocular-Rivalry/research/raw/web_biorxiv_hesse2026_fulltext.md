# RAW: bioRxiv full-text extraction — Hesse et al. 2026
Fetched 2026-10-29 by orchestrator via WebFetch. This is a small-model summary of the page text, NOT verbatim. Verify numbers against the PDF before final publication.

URL: https://www.biorxiv.org/content/10.64898/2026.10.15.759299v1 (full text: .../v1.full)
Title: "Rapid alternation of conscious and suppressed stimulus representations in the primate brain"
Authors: Janis K. Hesse (UC Berkeley Neuroscience); Frank F. Lanfranchi (UC Berkeley; Caltech BBE); Conor McGrory (Princeton Neuroscience Institute); Yuelin Shi (UC Berkeley; Caltech BBE); Tatiana A. Engel (Princeton Neuroscience Institute); Doris Y. Tsao (UC Berkeley; HHMI)
DOI: 10.64898/2026.10.15.759299. bioRxiv v1, posted 2026-10-16. NOT peer reviewed.

## Abstract (paraphrase; verbatim text not captured)
- Neuropixels recordings across multiple face patches in inferotemporal (IT) and prefrontal cortex (PFC) during binocular flash suppression: one image is seen while the other is present but suppressed.
- The population alternates between conscious and suppressed micro-epochs about 15 times per second, while the stimulus and the percept stay constant.
- Conscious epochs track the seen image; suppressed epochs track the hidden image. Single neurons follow the same pattern.
- The two epoch types can be told apart, and feature tuning is stronger in conscious epochs. PFC results are qualitatively similar.
- Framing: a pure signal of conscious perception had not been found before, and earlier studies found only weak modulation of high-level visual cortex.
- Conclusion: conscious access requires "temporal selection beyond localization".
- Quote (via secondary source): both IT and PFC "rapidly interleave conscious with suppressed content".

## Subjects and recording
- Two male rhesus macaques (monkey A, monkey M).
- Neuropixels 1.0 NHP probes; Kilosort3 spike sorting; single units and multi-units.
- IT face patches ML and AM, localized by fMRI (faces > objects). PFC patches PO (orbitofrontal) and PVL (ventrolateral); the Fig. 1 legend calls them "lateral orbitofrontal sulcus and infraprincipal dimple".
- Neurons: 3501 visually responsive neurons across sessions. PFC analysis used 661 neurons (300 PCA components; IT used 500). Example raster: 429 simultaneously recorded cells. Tuning-gain analysis: 543 cells.
- Sessions: 9 for the main state analyses; 19 for the two-state vs one-state test; 10 for single-trial decoding; 7 of 9 for the cross-region analysis.

## Paradigm
- Binocular FLASH SUPPRESSION, not classic free rivalry. A priming image goes to one eye for 1 or 2 s, then a second image is flashed to the other eye. The flashed image usually dominates.
- Dichoptic presentation via red/cyan anaglyph goggles; stimuli 7°; 60°×44° LCD screen.
- Experiment 1: priming 2 s, test 4 s, blank 500 ms. 10 faces form 25 pairs. 7 sessions (monkey A) + 3 (monkey M).
- Experiment 2: priming 1 s, test 1 s, blank 250 ms. 1500 faces form 750 pairs; a subset of 60 faces had about 20 trials per condition. 5 sessions (A) + 4 (M).
- The monkeys made NO report. The percept was validated in 14 human participants by button press:
  - flashed percept reported on 82% of trials
  - flashed vs primed: t(13)=9.4, p=4e-7
  - analysis window 300–1000 ms after the flash
  - report latency 0.86±0.05 s
- Monkey states were inferred from neural activity (LLR + HMM), not from a monkey report.
- NOTE: the 2020 eLife paper inferred the percept from eye movements. The visible 2026 text does not describe eye-movement inference for the monkeys.

## Results (IT)
- Average binocular modulation is weak: slope 0.23 vs unambiguous (5550 cell-stimulus pairs, p=8e-133).
- Alternation about 15 times per second (abstract).
- Likelihood autocorrelation time constant 67 ms (Methods: mean dwell D=67 ms, median ≈46 ms).
- HMM (5 ms bins): median dwell 64 ms (state 1) and 59 ms (state 2); plateaus near 60 ms across bin sizes.
- More than an order of magnitude faster than perceptual switches in rivalry (~0.5 Hz).
- Reconstruction:
  - In state 1, conscious-face explained variance was >80% for SOME features (ceiling from priming >90%).
  - The suppressed face was near chance in state 1; the pattern reversed in state 2.
  - The initial analysis was circular; the authors addressed this with held-out neurons.
- Single-trial 10-class decoding (chance 10%):
  - full window: 40% conscious, 34% suppressed
  - state 1: >61% conscious vs 4% suppressed (t(9)=11.0, p=2e-6)
  - state 2: reversed (t(9)=-13.7, p=3e-7)
- Held-out neurons: EV t(29)=17.5, p=6e-17; state 1 t(9)=7.6, p=3e-5; state 2 t(9)=-6.5, p=1e-4.
- The two-state model beats the one-state model in all 19 sessions (t(18)=4.84, p=1e-4).
- Single-cell gain:
  - state 1: gain for conscious face > suppressed face (p = 8 × 10⁻⁹⁵); state 2: reverse (p = 6 × 10⁻⁶⁰)
  - conscious gain in state 1 vs suppressed gain in state 2: p = 3 × 10⁻⁴⁰, mean ratio 1.21, Pearson r = 0.90
  - [orchestrator note 2026-10-29: these three p-values were in the original WebFetch extraction but were omitted when this file was first written; restored here]
  - mean firing slightly higher in state 2
  - a linear decoder separates the two states with 66% accuracy
- The same neurons switch content; there are not separate conscious and suppressed populations.
- After gain equalization, the residual binocular–unambiguous correlation disappears (r=-0.02, p=0.31), so averaging explains the weak modulation.
- Coordination between the ML and AM patches is weak; the authors say the results "do not provide strong evidence" for it.
- Controls:
  - within-trial subsampling
  - shuffled templates (EV < 0)
  - On/Off gain fluctuations do not explain the states (κ≈0)
  - averaging, conscious-only and uncoordinated models each fail at least 3 of 4 tests
  - real data beat the averaging model by ΔEV 8.2% (p=0.007)

## Results (PFC)
- Reconstruction quality is lower: priming EV <80%, and <30% for shape features.
- State 1 tracks the conscious face and state 2 the suppressed face: EV t(29)=14.2, p=1e-14; decoding p=1e-5 (n=30 pairs).
- Held-out halves: EV p=3e-4; decoding p=0.03.
- Modulation slopes: state 1 0.91 (conscious), state 2 -0.52.
- Authors: "may therefore be a broad cortical phenomenon".

## Discussion
- The suppressed stimulus is NOT a weak residue. In its own epochs it occupies the same face space as the conscious face. This may explain unconscious influences on behaviour, attention and affect.
- The authors link the timing to:
  - rhythmic attentional sampling
  - theta-phase working-memory access
  - orbitofrontal alternation during decisions
  - theta-paced hippocampal flickering
- They suggest temporal structure may be a general organizing principle.
- Open question: "why do representations in some micro-epochs reach awareness, whereas others do not?"
- Speculation: suppressed epochs explore alternative interpretations; conscious epochs carry the working hypothesis routed to report and action circuits.
- The Discussion does NOT explicitly cite GNWT or IIT and does not discuss alpha rhythms.
- Limitations:
  - the routing mechanism is speculative
  - the switching mechanism is unknown
  - only two monkeys
  - circularity in the initial analysis (addressed)
  - weak cross-patch coordination
  - lower PFC reconstruction quality
- Methods/stats: Poisson LLR in 10 ms bins; two-state Poisson HMM (hmmlearn, Baum-Welch, Viterbi); sign-flip permutation tests (1e5 permutations).

# 09 Fix log (P1-09)

Applies research/08_qa_report.md issues #1-#17 plus the orchestrator corrections (F40 restored in raw; terminology unification; status legend in README). Edits were minimal string replacements. 02_paper_card.md and raw files were not touched. Checks: 06 parses (77 items, unique ids); 05 has 42 rows (header + 41), every row 5 columns; grep for the old terms in 03-07 returns no hits.

Terminology decisions (applied in 03-07): priming = 前導刺激; reconstruction = 重建; no-report = 無報告 (範式); ignition = 點燃; frame rate = 影格率; spike raster = 放電點陣圖; bin = 時間窗（bin）; 眼眶額葉 = 眶額葉; GNWT = 全域神經工作空間理論; NCC = 意識的神經相關物.

## QA issues

| # | Result | File: change |
|---|---|---|
| 1 | Fixed | 03: "It resolves a long-standing puzzle: why..." -> "It offers a candidate explanation, in this dataset only, for why ... (preprint, not peer reviewed; two monkeys)"; also "so averaging explains the weak modulation" -> "so, according to the authors, averaging explains the weak modulation in this dataset". |
| 2 | Fixed | 03 §1 Sheinberg line: "...cells followed the percept. [KNOWLEDGE]" -> "...followed the percept, although the average modulation amplitude was not a pure seen/not-seen signal (see the takeaway below). [KNOWLEDGE; the exact fraction is from memory, UNVERIFIED]". |
| 3 | Fixed | 04 §8.1: "它在極短時間內輪流『看見』與『被抑制』。" -> "群體神經活動在極短時間內輪流表徵『被看見的臉』與『被抑制的臉』；受試者的知覺本身沒有隨之改變。" |
| 4 | Fixed | 04 §3: "同時記錄數百個神經元，" -> "同時記錄數百個神經元（例：範例中 429 個），". |
| 5 | Fixed | 07 V2 purpose: "為何三十年來平均活動看起來很弱" -> "為何過去研究中平均活動看起來調變很弱（限於這份資料集的作者解釋，預印本）". |
| 6 | Fixed | Unified to glossary terms. 04: 啟動圖 -> 前導刺激, 啟動 2 s/1 s -> 前導刺激 2 s/1 s, 重構 -> 重建. 06: 啟動圖像 -> 前導刺激圖像 (F11), 啟動 -> 前導刺激 (F12, F13, F26, F33, F50), 重構 -> 重建 (F34, F46, F50, F67), 免報告 -> 無報告 (F68, F71, F75), 點火 -> 點燃 (F73). 07: 免報告 -> 無報告 (V8), 啟動 -> 前導刺激 (V9). 03: 免報告範式 -> 無報告範式; NCC 標題 意識神經相關 -> 意識的神經相關物 (also in 04). 05: 啟動影像 -> 前導刺激 (flash suppression), PFC啟動條件 -> PFC前導刺激條件. |
| 7 | Fixed | Decided 影格率. 04 (3 places): 幀率 -> 影格率; 07 A6 heading "影片幀" -> "影格／動畫翻頁書"; 06 F56 already 影格率. 05: new entry "frame rate / 影格率". |
| 8 | Fixed | Decided 放電點陣圖. 04: "範例光柵 429 個同步細胞" -> "範例放電點陣圖（spike raster）中 429 個同時記錄的細胞"; 06 F20: 範例光柵圖 -> 範例放電點陣圖; 07 V2: 光柵圖 -> 放電點陣圖（spike raster）; 05: new entry "spike raster". |
| 9 | Fixed | 06 F68: status verified -> secondary_only; notes now cite "Abstracts and press only" and same tier as F69. |
| 10 | Fixed | 06 F64: contradicted -> unverified; notes rewritten (numbers not in inputs; guardrail "never attribute to 2026" kept). 07 do-not-say row and V8 note updated to "F64 unverified". |
| 11 | Fixed | 06 F24: status kept contradicted; notes + " Per raw summary (visible text does not describe it); check PDF before publish." |
| 12 | Fixed | 06 F44: unverified -> contradicted (consistent with F10/F24 standard); notes explain. 07 A4 note and do-not-say row updated to "F44 contradicted". |
| 13 | Fixed | New research/06_fact_sheet_README.md with status legend (verified = consistent with raw model-summary, not verbatim, PDF check required). JSON kept as a bare array. Also appended "Check PDF before publish." to notes of F42, F46, F52, F53, F54, F55. 07 header points to the README. |
| 14 | Fixed | 分箱 -> 時間窗（bin）: 06 F29 and HMM bin phrase in F31 ("跨分箱大小" -> "跨時間窗大小"), 07 A4 and do-not-say row, 04 ("10 ms bin" -> "10 ms 時間窗（bin）"), 05 LLR entry. 眼眶額葉 -> 眶額葉: 06 F17, F55; 07 V5. |
| 15 | Fixed | 05: added "binocular flash suppression (BFS) / 雙眼閃光抑制（BFS）" entry; GNWT zh changed 全域工作空間理論 -> 全域神經工作空間理論 (matches 03); NCC unified to 意識的神經相關物 (03/04 changed to match glossary). |
| 16 | Fixed | 07 §4: "不要說清單：17 列" -> "18 列" (verified 18 data rows). A7 heading "秒針與心跳" -> "分針與秒針". The "快 30 倍" wording left as is (already self-labelled as derived). |
| 17 | Not changed (by design) | 05_glossary.csv keeps its UTF-8 BOM because the file is meant to be opened in Excel (QA allows this). Strip the BOM (first 3 bytes EF BB BF) only if a program will parse it. |

Counts: 16 fixed, 1 not changed (by design, #17). Severity: all 7 med and 9 of 10 low fixed.

## Orchestrator corrections

- F40 (p = 3x10^-40): status unverified -> verified. claim now states the comparison (conscious gain in state 1 vs suppressed gain in state 2, mean ratio 1.21, r = 0.90); source_ref -> raw web_biorxiv_hesse2026_fulltext.md Results (IT) "Single-cell gain" (restored line; same section also gives p = 8x10^-95 and p = 6x10^-60); notes: "Verified = consistent with the raw model-summary, not verbatim. Check PDF before publish." F39 notes cross-reference F40.
- 04 §7 (lineage): "其餘僅見影片筆記的數字（如 p=3×10^-40、700 ms）不採用" -> "僅見影片筆記的數字（如 700 ms）不採用。p=3×10^-40 已在 raw 全文摘要中找到（F40...），可引用，但公開前須對照 PDF，並須註明比較對象".
- 07 do-not-say row "「p = 3×10^-40」| 原文無此值 | ... | F40 unverified" -> row kept (now 18 rows total) but reworded: do not cite it in isolation as an effect size; F40 verified (pending PDF). F40 removed from the "unverified id" list in 07 §4.
- Not changed: F34, F49, F62, F63, F65, F66, F70, F74, F75, F77 remain unverified; 08 QA report was not edited (its F40 conclusion is now superseded by the restored raw line).

## Resulting status counts in 06
verified 48, secondary_only 13, unverified 11, contradicted 5 (total 77).

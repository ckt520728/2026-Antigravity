# 06_fact_sheet.json README (status legend)

06_fact_sheet.json is a plain JSON array of fact objects (id, claim_en, claim_zh_tw, value, unit, source_ref, status, notes). The legend is kept here so the file stays a bare array.

## status values

| status | meaning |
|---|---|
| verified | Consistent with the raw model-summary of the bioRxiv page (research/raw/web_biorxiv_hesse2026_fulltext.md) or another raw file. NOT verbatim: the raw file is a small-model summary. A PDF check is REQUIRED before publication, for every verified item, whether or not its notes say "Check PDF before publish". |
| secondary_only | Found only in press, social posts, listings or abstracts (e.g. Glitchwire, Tsao on X, Caltech news, idw press report). Must carry the word "preliminary" (初步) in output. |
| unverified | Not found in the raw files (video-note-only claims, or memory-based [KNOWLEDGE] literature). Do not cite as fact. |
| contradicted | Raw files indicate the claim is wrong or over-stated (usually a media or video-note overstatement). The raw files are summaries, so "contradicted" = "not supported by the raw summary"; PDF check still advised. Do not state. |

## Notes
- F40 (p = 3x10^-40) is verified since the orchestrator restored the line in the raw file on 2026-10-29 (the same section also lists p = 8x10^-95 and p = 6x10^-60). PDF check required before publication.
- Terminology fixed across 03-07: priming = 前導刺激, reconstruction = 重建, no-report = 無報告, ignition = 點燃, frame rate = 影格率, spike raster = 放電點陣圖, bin = 時間窗, PO = 眶額葉.

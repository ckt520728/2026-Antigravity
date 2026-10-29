# sources.md — P2-00 Phase 2 共用 Brief

本檔列出 brief.md 引用或授權使用的每個 fact id、其 status,以及在 brief.md 中出現的位置。事實全文以 `research/06_fact_sheet.json` 為準;status 圖例見 `research/06_fact_sheet_README.md`。

## 輸入檔案

| 檔案 | 用途 |
|---|---|
| research/04_dossier.md | 敘事主軸、關鍵訊息(brief 第 1、2、3、9 節) |
| research/05_glossary.csv | zh-TW 術語速查表(brief 第 8 節) |
| research/06_fact_sheet.json | 77 筆事實的 id 與 status(brief 第 4、5 節) |
| research/06_fact_sheet_README.md | status 圖例、F40 特別註記(brief 第 4 節) |
| research/07_analogies_visuals.md | 類比庫與「不要說」清單(brief 第 2、5、7.1 節) |
| CLAUDE.md / AGENTS.md | 硬性內容規則、驗收條件(brief 第 4–7、10 節) |
| phase2/00_brief/style_refs/Thariq_finding_unknown_README.md | 工作流程 skills 脈絡(reference-anchor、deviation-log、verify-with-rubric,brief 第 7 節) |

## brief.md 授權使用的 verified fact id(48 筆)

全部出現於 brief.md「4.1 允許的 verified fact id」;其中部分 id 另在括號註明處重複出現。

| 分組(brief 4.1) | fact id(status 皆為 verified) |
|---|---|
| A. 論文身份 | F01、F02、F03、F05、F06 |
| B. 範式與人類驗證 | F09(另見 3、5)、F11、F12、F13、F14、F23(另見 3)、F25(另見 3、5)、F26 |
| C. 記錄規模 | F15、F16、F17、F18(另見 9)、F19、F20、F21、F22 |
| D. 核心發現:微時段交替 | F27、F28、F29(另見 5)、F30(另見 5)、F31(另見 5)、F32、F67 |
| E. 解碼、重建與對照 | F33、F35、F36(另見 9)、F37、F38、F45、F46 |
| F. 增益與單細胞 | F39(另見 4 規則、9)、F40(另見 4 規則、5)、F41、F42、F43(另見 5) |
| G. PFC 與跨區 | F47(另見 5)、F48(另見 5)、F50、F51、F52 |
| H. 限制與理論脈絡 | F53、F54、F55(另見 5) |

合計:5+8+8+7+7+5+5+3 = **48 筆 verified**。

## brief.md 授權使用的 secondary_only fact id(13 筆,出現處須標「初步」/ "preliminary")

出現於 brief.md「4.2 secondary_only」;F56、F59、F68 另見第 5 節禁用說明中的許可用法。

| fact id | status | brief.md 位置 |
|---|---|---|
| F07、F08、F58、F60、F61、F71、F72、F73、F76 | secondary_only | 4.2 |
| F56(Tsao 澄清語,可引用但標初步) | secondary_only | 4.2、5.1 |
| F59(宣傳語,只可作為作者宣傳措辭引用) | secondary_only | 4.2、5.4 |
| F68(2020 eLife 脈絡,須標 2020) | secondary_only | 4.2、5.11 |
| F69(Shi 2026,只寫年份) | secondary_only | 4.2 |

## brief.md 明令禁用的 fact id(16 筆,永遠不得出現)

列出僅供識別與防堵,不構成授權。出現於 brief.md「4.3 禁用事實 id」與第 5 節對應條目。

| status | fact id |
|---|---|
| contradicted | F04(另見 5.10)、F10、F24(另見 5.11)、F44(另見 5.6)、F57(另見 5.1) |
| unverified | F34(另見 5.8)、F49(另見 5.5)、F62、F63、F64(另見 5.2)、F65(另見 5.8)、F66、F70、F74、F75、F77(另見 5.13) |

## 備註

- F40 已於 2026-10-29 由 orchestrator 恢復為 verified(research/09_fix_log.md);brief 採用其限制:只能連同 F39 的比較脈絡引用,不得當效果量。
- verified 事實在公開發表前仍須逐筆對照 PDF(人類發布階段的工作;見 06_fact_sheet_README.md)。

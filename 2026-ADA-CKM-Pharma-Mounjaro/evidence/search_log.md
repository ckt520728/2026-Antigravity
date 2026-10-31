# 搜尋與查核紀錄

整理日：2026-10-30（Asia/Taipei）。本檔只記錄本輪實際執行的操作與獨立稽查回報，不宣稱系統性回顧或所有來源全文審畢。網路查詢只含公開 URL／PMID／NotebookLM source ID，未上傳本地未公開素材或病人資料。

## 1. NotebookLM 唯讀操作（2026-10-29）

Notebook：`e9c8966b-c3e8-4968-bce1-e6c39aa402b1`

| 實際操作／完整參數 | 結果 | 用途與限制 |
|---|---|---|
| `notebook_get(notebook_id="e9c8966b-c3e8-4968-bce1-e6c39aa402b1")` | 成功；45 sources | 盤點來源清單；未寫入或分享 notebook。 |
| `source_get_content(source_id="15555df5-6709-4702-90f6-b68f67b14a3d")` | 成功；57,186 chars | SURPASS-2 原始全文；Abstract、Methods／Results pp.503–515 支持 C001/C004。 |
| `source_get_content(source_id="22a845a1-e2d0-4934-836a-cec29f701436")` | 成功；44,854 chars | SURMOUNT-5 原始全文；Abstract、Methods、Table 1–3、Fig.1 支持 C001/C005。 |
| `source_get_content(source_id="dc7fd8ad-9fce-4a7d-b8b4-5968fc47277e")` | 成功；47,327 chars | SUMMIT 原始全文；Abstract／Methods pp.427–437 支持 C006。 |
| `source_get_content(source_id="88b5b082-cb5e-428f-a926-154b9ac49d21")` | 成功；61,082 chars | STEP-HFpEF DM 原始全文；Abstract／Methods pp.1394–1407 支持 C007。 |

本輪沒有以 `notebook_query` 的 AI 回答作為證據。NotebookLM 是原始全文存取介面；registry 的 N-entries 標為 `via_notebooklm_primary_text_cross_checked`，對應臨床 claims 仍使用 S01–S04 的 DOI／期刊 locator。詳見 [notebooklm_summary.md](../sources/notebooklm_summary.md)。

## 2. 公開 primary-source 查閱

| 日期 | 實際 URL／query | 對應 | 結果與限制 |
|---|---|---|---|
| 2026-10-29 | `https://pubmed.ncbi.nlm.nih.gov/34170647/` | S01／C004 | 成功；核對 1879、40 週、sema 1 mg、HbA1c 百分點與 T2D 族群；另由 NotebookLM 全文補 1878 至少一劑。 |
| 2026-10-29 | `https://pubmed.ncbi.nlm.nih.gov/38785209/` | S05／C008 | 成功；核對 FLOW 收案 eGFR／UACR、N=3533、sema 1 mg、3.4 年、331 vs 410、HR 0.76。 |
| 2026-10-29 | `https://pubmed.ncbi.nlm.nih.gov/41406444/` | S06／C009 | 成功；核對 mITT 13,165、dulaglutide 1.5 mg、MACE、95.3% CI、NI／superiority P 值。期刊日 2025-12-18，PubMed 收錄 2025-12-17。 |
| 2026-10-29 | `https://pubmed.ncbi.nlm.nih.gov/42114520/` | S12／C010 | 成功；核對 Lancet Diabetes Endocrinol 2026;14(7):544–557、DOI、探索性腎複合與 4.0 年結果；全文／SAP multiplicity 尚未審畢。 |
| 2026-10-29 | `https://www.fda.gov.tw/TC/newsContent.aspx?cid=4&id=t623895` | S09／C003 | 成功；TFDA 2025-11-10 公告第一點；僅支持概括用途，不是完整仿單或給付依據。 |
| 2026-10-30 | `https://pubmed.ncbi.nlm.nih.gov/38078870/` | S13／C019 | 成功；核對 783 lead-in、670 隨機、36–88 週 −5.5% vs +14.0%；abstract level，未完整審 SAP。 |
| 2026-10-30 | `https://www.medicines.org.uk/emc/files/usermanual.15482.pdf` | S11／UK IFU | webfetch 回 `Unsupported fetched file content type: application/pdf`；直接 GET 回 HTTP 403。未取得全文、未建立本地 PDF，S11 降 pending，不作主要依據。 |

S02／S03／S04 另有 Kimi K3 唯讀 clinical auditor 於 2026-10-29 回報以 PubMed `40353578`、`39555826`、`38587233` 抽核主要數字；主控再以 NotebookLM 原始全文獨立核對，不只採信 auditor 自報。

## 3. 本地正式文件與 archive 驗證

| 日期 | 實際操作 | 結果 |
|---|---|---|
| 2026-10-29 | 以 `pypdf.PdfReader` 讀取 `monjaro/sources/mounjaro_us_2026-10-29.pdf` pp.1、3–6、10–11 | 核對 C001/C002/C011–C018：USPI Revised 08/2026；成人劑量、禁忌、GI／AKI、併藥、避孕、麻醉、KwikPen 與 renal monitoring。PDF 直接讀取介面不支援此模型，因此以本地文本抽取核實，未猜讀。 |
| 2026-10-29 | 以 `pypdf.PdfReader` 讀取 `monjaro/sources/zepbound_us_2026-10-29.pdf` p.1 | 核對 C002 的成人體重控制與肥胖伴中重度 OSA；USA only。 |
| 2026-10-29 | SHA-256 對照 `download_manifest.json` | 兩份 USPI hash 均相符。 |
| 2026-10-29 | SHA-256 對照 canonical ZIP 與 `zip_manifest.json` 全部 7 個 extracted entries | 全部相符；archive before／after hash 相同，原始 entry paths 保留。 |
| 2026-10-30 | `python -X utf8 monjaro/evidence/build_registry.py` | 實際產生 27 sources、24 claim rows（21 C＋3 P）；讀回 JSON／CSV。 |

## 4. 未完成與禁止推定

- S10 為 2023 historical-only 文件；不能代替 2026 台灣完整仿單。
- S14 僅候選入口；本次沒有取得可驗證的現行完整仿單附件，維持 pending。
- P001 台灣完整仿單／給付、P002 supplements／SAP／critical correspondence、P003 妊娠與台灣麻醉流程均未完成，不以其他 jurisdiction 文件填空。
- S15／S16 是既有製作／house-style snapshots，不是臨床證據；本輪未重新驗證其 remote 最新狀態。
- 搜尋結果不用於個別病人處方，也不作未核准的 HTML／PPTX／影片／blog 或公開發布。

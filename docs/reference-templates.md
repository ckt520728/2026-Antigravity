# 醫學中心病歷／報告範本研究筆記 (Reference Templates Research)

> 為 v6.0 互動式網頁升級所做的外部範本調研。  
> 調研日期：2026-08-10 ｜ 用途：決定表單要有哪些欄位、順序、以及「什麼算完整的病歷/報告」。

---

## 1. 住院病歷 (Admission Note / H&P) — 標準區段

多家醫學中心與教學醫院範本共同具備的區段（依撰寫順序）：

| # | 區段 | 本系統 v5.0 | v6.0 動作 |
|---|------|-------------|-----------|
| 1 | Patient Demographics（含 informant／可信度） | ✅ 有 | 補 informant / reliability |
| 2 | Chief Complaint (CC) | ✅ 有 | 保留 |
| 3 | History of Present Illness (HPI)（含 ED course） | ✅ 有 | 保留 + LQQOPERA |
| 4 | Past Medical History (PMH) | ✅ 有 | 保留 |
| 5 | **Past Surgical History (PSH)** | ❌ 缺 | **新增** |
| 6 | **Current Medications（用藥整合 reconciliation）** | ❌ 缺 | **新增** |
| 7 | Allergies | ✅ 有 | 保留 |
| 8 | **Family History** | ❌ 缺 | **新增** |
| 9 | **Social History**（菸／酒／檳榔／職業） | ❌ 缺 | **新增（台灣需檳榔欄位）** |
| 10 | **Review of Systems (ROS)** | ❌ 缺（只塞了生命徵象字串） | **新增 10 系統勾選** |
| 11 | Physical Examination（分系統） | ⚠️ 單一 textarea | **改為分系統 + 一鍵全正常** |
| 12 | **Admission Labs & Imaging** | ❌ 缺 | **新增** |
| 13 | Assessment / Impression（**problem list**） | ⚠️ 單一 textarea | **改為 problem-based 條列** |
| 14 | Plan（**每個 problem 各自的 plan**） | ⚠️ 單一 textarea | **改為與 problem 配對** |

### 重點引用

- 核心區段應包含 patient demographics、chief complaint、詳細 HPI、完整 ROS、完整 PE，以及含鑑別診斷與處置方向的 assessment and plan。
- 教學醫院版本另加：ED course、完整內外科病史、**用藥整合 (medications reconciliation)**、家族與社會史含危險因子、入院檢驗與影像判讀、含 ICD-10 的問題清單、以及**每一個 active problem 各自的處置計畫**。
- **避免 note bloat**：範本提供廣度，但內容要依主訴裁剪；與本次入院無關的區段寫 "non-contributory" 即可。→ v6.0 因此為每個新區段都提供「non-contributory / 全部正常」一鍵鍵。
- 法規時限（美國 CMS 42 CFR 482.24）：H&P 須於入院前 30 天內或入院後 24 小時內完成並存入病歷。→ v6.0 在頁首顯示入院時間與距離 24 小時期限的提示。

### 社會史（台灣在地化）

檳榔在台灣社會根深蒂固，已被納入醫院問診表單；同時吸菸、飲酒、嚼檳榔者口腔癌發生率相較全戒者高出約 123 倍。→ v6.0 社會史固定提供 **菸 (pack-year) / 酒 / 檳榔 / 職業 / 旅遊接觸史** 五欄。

---

## 2. 影像／檢查報告 — RSNA 結構化報告

RSNA 委員會制定的報告範本格式包含：科部行政資料、病患基本資料、**臨床病史 (clinical history)**、**檢查技術 (imaging technique)**、**比較影像 (comparison studies)**、觀察與註記 (observations)、**摘要或結論 (summary/impression)**、簽章。

RadReport.org 為免費的最佳實務範本庫，採 RadLex 標準術語；RSNA 與 ESR 共組 Template Library Advisory Panel (TLAP) 維護。文獻顯示轉診醫師偏好**有明確標題與次標題分段**的報告。

**v6.0 動作**：四個檢查模組全部補上 `臨床適應症 (Indication)`、`檢查技術/儀器 (Technique)`、`比較影像 (Comparison)` 三欄，並固定輸出 Technique → Findings → Impression → Recommendation 的段落順序。

---

## 3. 心臟超音波 — ASE 報告標準化建議

ASE《Guidelines for the Standardization of Adult Echocardiography Reporting》(2025) 建議的統一報告要素：
demographic information、essential history、**indication**、**vital signs**、左右心腔評估、瓣膜、動靜脈、心包膜、心外發現、**是否使用顯影劑 (UEA) 或攪拌生理食鹽水**、額外生理學操作、**血流動力學測量 (Doppler、stroke volume、pressure gradient)**、**與過去檢查之比較**、以及 **summary statement**。

**v6.0 動作**：Echo 模組補 `Indication`、`檢查時血壓`、`顯影劑/Bubble study`、`與前次比較`、`RV 功能 (TAPSE)`、`IVC`，並在 findings 輸出中固定「LV → RV → Atria → Valves → Pericardium → Great vessels → Summary」順序。

---

## 4. 大腸鏡 — ASGE/ACG 2024 品質指標

2024 版 ASGE/ACG Quality Task Force 更新重點：

- 優先指標：**ADR**、**SSLDR**、**清腸品質達標率**、**篩檢/追蹤間隔遵從率**。
- **Cecal intubation rate 目標 ≥95%**，需完整進入盲腸並**照相記錄盲腸標誌**。
- **退鏡時間**：45 歲以上正常大腸鏡的建議平均最短退鏡時間已由 6 分鐘**上調為 ≥8 分鐘**。
- 糞便潛血/mt-sDNA 陽性者之 ADR 目標 **≥50%**；**SSLDR ≥6%**。
- 兩項新的切除紀錄指標：(1) 報告需記載病灶的**大小、形狀、部位、切除方式**（目標 ≥98%）；(2) 4–9 mm 病灶以 **cold snare** 切除的比例（目標 ≥90%）。

**v6.0 動作**：
- LGI 模組退鏡時間的提示由 `Normal >= 6 min` 更正為 **`≥8 min (ASGE/ACG 2024)`**，並在低於 8 分鐘時即時警示。
- 新增「**盲腸標誌照相記錄**」勾選（appendiceal orifice / ileocecal valve / TI intubation）。
- 息肉改為可新增多筆的結構化列：**部位 × 大小(mm) × 形態(Paris/Yamada) × 切除方式**，4–9 mm 未選 cold snare 時提示。

---

## 5. 設計結論（給 v6.0 的規格）

1. **完整性優先於美觀**：缺 ROS / 用藥 / 家族社會史 / 分系統 PE 是目前最大的臨床缺口，先補齊。
2. **每個新區段都要有「一鍵正常 / non-contributory」**，否則補完整性等於增加打字負擔，違背「方便、簡易操作」。
3. **問題導向 A&P**：impression 與 plan 必須配對，不能是兩個各自為政的 textarea。
4. **報告文字要能一鍵複製**：多數醫師仍需貼回院內 HIS，複製鍵的價值高於任何視覺效果。
5. **草稿自動保存**：門診/病房隨時被打斷，關掉分頁不能歸零。
6. **入口密碼**：Web App 為 `ANYONE` 存取，必須有密碼閘門。

---

## 參考來源 (Sources)

- [Hospital Admission H&P Template — Orbdoc](https://orbdoc.com/templates/internal-medicine-hospital-admission-hp/)
- [Admission Note Template with Examples — Heidi Health](https://www.heidihealth.com/en-us/blog/admission-note-template)
- [Hospital Admission Note Template — s10.ai](https://s10.ai/blog/hospital-admission-note-template)
- [Inpatient Admission H&P — s10.ai templates](https://s10.ai/templates/inpatient-admission-hp)
- [History and Physical Template 2026 — patientnotes.ai](https://patientnotes.ai/resources/history-physical-template)
- [RadReport reporting templates — RSNA](https://www.rsna.org/practice-tools/data-tools-and-standards/radreport-reporting-templates)
- [RadReport Template Library](https://radreport.org/home/RPT50831)
- [Structured for Success: The RSNA Radiology Reporting Initiative](https://radiologybusiness.com/topics/healthcare-management/healthcare-quality/structured-success-rsna-radiology-reporting)
- [Advancements in Standardizing Radiological Reports: A Comprehensive Review](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC10535385/)
- [Guidelines for the Standardization of Adult Echocardiography Reporting — JASE](https://onlinejase.com/article/S0894-7317(25)00292-5/fulltext)
- [Recommendations for Chamber Quantification — ASE (PDF)](https://www.asecho.org/wp-content/uploads/2013/05/Chamber-Quantification.pdf)
- [ASGE/ACG Quality Task Force Updates Quality Indicators for Colonoscopy](https://info.asge.org/083024-colon-asge/acg-quality-task-force-updates-quality-indicators-for-colonoscopy)
- [ASGE-ACG Quality Indicators for Colonoscopy (2024) FAQ (PDF)](https://www.asge.org/docs/default-source/default-document-library/asge-acg-qi-for-colonoscopy-faq_oct24.pdf)
- [Key quality indicators in colonoscopy — Gastroenterology Report](https://academic.oup.com/gastro/article/doi/10.1093/gastro/goad009/7075782)
- [Review of systems — Wikipedia](https://en.wikipedia.org/wiki/Review_of_systems)
- [Oral cancer in Taiwan — Oral Diseases (Wiley)](https://onlinelibrary.wiley.com/doi/10.1111/odi.15076)

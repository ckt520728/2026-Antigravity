# NCBI 與 AlphaGenome 雙引擎科學知識庫使用手冊 (User Manual)

> **建立日期**：2026-10-12  
> **適用平台**：Google Antigravity / Agentic Coding & Research  
> **核心領域**：臨床醫學、腎臟學、神經認知科學、轉譯醫學、分子遺傳學  

---

## 1. 雙引擎架構概述 (Executive Overview)

在現代生物醫學與轉譯研究中，研究者面對的核心挑戰是「**如何將大量已發表的實證醫學數據，與前瞻的分子遺傳調控機制無縫串接**」：

| 引擎維度 | **NCBI 生物醫學資料庫套件** | **Google DeepMind AlphaGenome** |
| :--- | :--- | :--- |
| **角色定位** | 經典實證醫學與公眾基因體基礎設施 | 次世代 AI 驅動調控基因體學大模型 |
| **核心資料庫** | PubMed, PMC, ClinVar, dbSNP, GenBank | AlphaGenome Atlas, 18-Modality Epigenome, GENCODE v46 |
| **數據特性** | 觀察性、實驗驗證、臨床回報致病性、文獻計量 | 序列到功能 (Sequence-to-Function) 即時預測模型 |
| **主要功能** | 文獻探勘、臨床分類評級、已知多型性頻率查詢 | 非編碼區變異衝擊、組織特異性剪接破壞、染色質可及性預測 |
| **認證變數** | `NCBI_API_KEY`（提升速率至 10 req/s） | `ALPHAGENOME_API_KEY`（必要金鑰，授權雲端推理） |

---

## 2. AlphaGenome 調控基因體學大模型詳解 (AlphaGenome Deep Dive)

### 2.1 核心概念與 18 模態特徵
AlphaGenome 是 Google DeepMind 針對人類基因體開發的統一多模態神經網路模型。它能直接讀取百萬鹼基級別的 DNA 序列，預測單一鹼基置換（SNV）或插入缺失（Indel）對多種分子表型的干擾。

AlphaGenome Variant Impact (AVI) 分數由 18 個生物模態特徵權重組合而成：
1. **Splicing (`fi_MERGED_SPLICING`)**：剪接供體/受體干擾、外顯子跳躍 (Exon Skipping) 與隱蔽剪接。
2. **ATAC-seq (`fi_MAX_ABS_ATAC`)**：轉座酶可及染色質變化。
3. **DNase-seq (`fi_MAX_ABS_DNASE`)**：DNase I 超敏感位點與開放染色質干擾。
4. **ChIP-TF (`fi_MAX_ABS_CHIP_TF`)**：轉錄因子結合親和力變更。
5. **ChIP-Histone (`fi_MAX_ABS_CHIP_HISTONE`)**：組蛋白修飾標記（如 H3K4me3, H3K27ac）。
6. **CAGE (`fi_MAX_ABS_CAGE`)**：帽分析基因表現，標定精確轉錄起始點 (TSS)。
7. **ProCap (`fi_MAX_ABS_PROCAP`)**：新生轉錄起始活化。
8. **RNA-seq (`fi_MAX_ABS_RNA_SEQ`)**：穩態轉錄本豐度與表現量改變。
9. **Polyadenylation (`fi_MAX_ABS_POLYADENYLATION`)**：3' UTR 聚腺苷酸化位點更動。
10. **AlphaMissense (`fi_ALPHAMISSENSE`)**：錯義突變蛋白質結構與演化破壞性分數。
11. **Cactus (`fi_CACTUS_241_WAY`)**：241 種哺乳動物多物種基因體對齊演化保守度。
12. **PhastCons (`fi_PHASTCONS_470_WAY`)**：脊椎動物跨物種序列保守度。
13. **Protein Termination / Start Lost / Stop Lost**：開放閱讀框 (ORF) 破壞。
14. **InDel Flags (`fi_IS_INSERTION`, `fi_IS_DELETION`)**：架構位移特徵。

### 2.2 關鍵指標解讀準則
- **`avi_phred` (Phred-scaled Score)**：
  - 公式：$-10 \times \log_{10}(1 - \text{Quantile})$。
  - **$\ge 10$**：排名前 10% 之功能性變異。
  - **$\ge 20$**：排名前 1% 之高衝擊候選變異。
  - **$\ge 25$**：排名前 0.3% 之極高危分子破壞變異。
- **`top_modality`**：指標驅動源（例如標明是 `Splicing` 還是 `DNASE`，明確指出分子機制）。

### 2.3 座標格式與呼叫規範
- **嚴格規範**：必須使用 1-based GRCh38 座標系統，格式為：
  ```text
  chr<N>:<position>:<ref_allele>><alt_allele>
  範例：chr9:128225994:G>A
  ```
- **區域視窗格式**（飽和突變）：
  ```text
  chr<N>:<start>-<end>
  範例：chr9:128225900-128226050
  ```

---

## 3. NCBI 生物醫學資料庫套件詳解 (NCBI Suite Deep Dive)

### 3.1 PubMed & PMC (`pubmed-database`)
- **應用場景**：醫學文獻檢索、臨床綜述收集、藥物作用機制文獻追溯。
- **核心特色**：
  - 支援布林運算、MeSH 詞彙、臨床研究過濾器。
  - 支援一鍵提取 PMCID 開放獲取全文，提供精確引用書目。

### 3.2 ClinVar (`clinvar-database`)
- **應用場景**：遺傳變異之臨床致病性評估（Clinical Significance）。
- **核心特色**：
  - 提供 ACMG/AMP 評級：Pathogenic（致病）、Likely Pathogenic（可能致病）、VUS（意義未明變異）、Benign（良性）。
  - 顯示臨床審查星級（Review Status）與具體提交機構臨床證據描述。

### 3.3 dbSNP (`dbsnp-database`)
- **應用場景**：已知人類遺傳多型性核對、rsID 與基因組座標轉換。
- **核心特色**：
  - 雙向轉換：輸入 `rs73885319` 即解析出染色體座標、對偶基因型與轉錄本影響。
  - 人群頻率：提供 ALFA、千人基因體、TopMed 等全基因組族群頻率（MAF）。

### 3.4 NCBI Sequence Fetch (`ncbi-sequence-fetch`)
- **應用場景**：精確下載轉錄本 mRNA、CDS 編碼區或前驅蛋白質 FASTA 序列。
- **支援代碼**：RefSeq Accession（如 `NM_001136540.3`、`NP_000305.3`）。

---

## 4. 臨床與研究實戰對話提示詞速查表 (Prompt Cheatsheet)

在 Antigravity 聊天介面中，直接以自然語言提問即可自動觸發相應的技能：

### 臨床遺傳與腎臟疾病範例
1. **腎病相關 APOL1 變異檢索**：
   > 「請查詢 dbSNP 關於 `rs73885319` (APOL1 G1 變異) 的族群頻率，並自 PubMed 搜尋該變異在非裔族群慢性腎臟病進展的關鍵機轉。」
2. **多囊腎 PKHD1 / PKD1 變異臨床評級**：
   > 「請檢索 ClinVar 資料庫中 PKHD1 基因近期回報為 Pathogenic 的變異列表，並總結其臨床審查星等。」

### AlphaGenome 次世代分子衝擊預測範例
3. **非編碼區變異機制分析**：
   > 「請使用 AlphaGenome 分析變異株 `chr9:128225994:G>A`，告訴我它的 AVI Phred 分數以及主要是哪種生物模態（如剪接或開放染色質）驅動了該分數？」
4. **外顯子飽和突變窗口掃描 (In silico Saturation Mutagenesis)**：
   > 「請針對 `chr9:128225900-128226050` 區域進行 AlphaGenome 飽和突變窗口掃描，列出衝擊分數前 5 名的突變熱點。」
5. **產生視覺化互動地圖連結**：
   > 「請為變異 `chr7:140753336:A>T` 生成 AlphaGenome Atlas 的互動網頁檢視連結。」

---

## 5. 合規與研究用途聲明 (Research Use & Compliance)

> [!CAUTION]
> **僅供學術與分子研究使用 (Research Use Only, RUO)**：
> 1. AlphaGenome 模型與 AVI 分數為分子調控機制之理論預測工具，不得直接作為臨床診斷、病患預後評估或用藥處方之唯一依據。
> 2. 請遵守 Google DeepMind 之 [AlphaGenome 服務條款](https://deepmind.google.com/science/alphagenome/)。

# Google Antigravity Science Skills 建置總結與踩坑實錄 (Wrap-up & Pitfalls)

> **建立日期**：2026-10-12  
> **適用平台**：Google Antigravity / Antigravity CLI (`agy`) / Agent Skills  
> **專案倉庫**：`https://github.com/ckt520728/2026-Antigravity`  
> **第二大腦**：`G:\我的雲端硬碟\Second Brain\知識庫\2026-Antigravity\`  

---

## 1. 任務背景與目標 (Executive Background)

本專案旨在將 Google DeepMind 針對 **Google Antigravity** 開發的官方科學技能套件（[Antigravity Science Use Cases](https://antigravity.google/use-cases/science) / `google-deepmind/science-skills`）完整建置至本機開發環境與專案倉庫中。

套件整合了超過 40 個尖端計算生物學、調控基因體學、蛋白質結構生物學、藥物化學與生醫文獻檢索技能，並串接了 **NCBI**（PubMed、ClinVar、dbSNP）與 Google DeepMind 次世代調控基因體學大模型 **AlphaGenome**。

---

## 2. 系統架構與外掛發現機制 (Architecture & Discovery)

Antigravity 具備雙層次外掛與技能加載體系：

```
                    ┌──────────────────────────────────────────────┐
                    │          Google Antigravity Agent            │
                    └──────────────────────┬───────────────────────┘
                                           │
                   ┌───────────────────────┴───────────────────────┐
                   ▼                                               ▼
     【全域外掛層 (Global Plugin)】                 【專案工作區層 (Workspace Project)】
  ~/.gemini/config/plugins/science/               .agents/plugins/science/
  ├── plugin.json (Manifest v1.2.4)               ├── plugin.json
  └── skills/ (40 專屬科學技能庫)                 └── skills/ (40 專屬科學技能庫)
                   │                                               │
                   ▼                                               ▼
  ~/.gemini/config/config.json                    ~/.agents/skills/ (即時對話調用)
  {"plugins": {"science": {"enabled": true}}}
```

### 40 項科學技能清單與分類

1. **基因體學與調控生物學 (Genomics & Regulatory)**：
   - `alphagenome-single-variant-analysis`：組織特異性 RNA 表現、剪接異常、染色質可及性預測。
   - `alphagenome-variant-impact-score`：AlphaGenome Variant Impact (AVI) 分數與 18 模態特徵貢獻度。
   - `alphagenome-atlas-website-links`：AlphaGenome Atlas 網頁互動視圖深層連結生成。
   - `ensembl-database`：轉錄本結構、外顯子與基因座標定位。
   - `clinvar-database`：臨床致病性評級與致病證據解析。
   - `dbsnp-database`：單核苷酸多型性 rsID 雙向解析與頻率查詢。
   - `gnomad-database`：全球人群對偶基因頻率與基因受限指標 (pLI, LOEUF)。
   - `gtex-database`：人體 54 種組織之定量 RNA 表現與 eQTL。
   - `encode-ccres-database`：ENCODE 順式調控元件 (cCREs) 註釋。
   - `ucsc-conservation-and-tfbs`：演化保守度 (phyloP/phastCons) 與轉錄因子結合位。
   - `unibind-database`：實驗驗證之 TF 結合位座標。
   - `jaspar-database`：轉錄因子結合模體矩陣 (PFM/PWM)。

2. **結構生物學與大分子 (Structural Biology & Macromolecules)**：
   - `alphafold-database-fetch-and-analyze`：AlphaFold 結構座標與 pLDDT 信心度分析。
   - `pdb-database`：實驗解析 3D 結構檢索與配體相互作用。
   - `uniprot-database`：蛋白質功能註釋、結構域與分類學。
   - `foldseek-structural-search`：3D 空間結構相似度搜尋。
   - `protein-sequence-similarity-search`：MMseqs2 / BLAST 同源序列搜尋。
   - `protein-sequence-msa`：EBI Clustal Omega 多序列比對。
   - `string-database`：蛋白質交互作用網絡 (PPI) 與富集分析。
   - `pymol`：PyMOL 分子視覺化與結構對齊渲染。
   - `interpro-database`：結構域、超家族與功能預測。

3. **化學資訊學與藥物開發 (Cheminformatics & Therapeutics)**：
   - `pubchem-database`：小分子結構、SMILES 與生物活性數據。
   - `chembl-database`：活性分子、藥物靶點、IC50/Ki 親和力數據。
   - `opentargets-database`：疾病與標靶關聯性、可藥性 (Tractability)。
   - `openfda-database`：FDA 藥物不良反應 (FAERS)、核准與召回通報。
   - `clinical-trials-database`：ClinicalTrials.gov 臨床試驗階段與入選條件。
   - `reactome-database`：生物反應與訊息傳遞路徑富集分析。

4. **科學文獻探勘與本體庫 (Literature Mining & Ontologies)**：
   - `pubmed-database`：PubMed 醫學文獻檢索與關聯挖掘。
   - `literature-search-arxiv`：arXiv 預印本搜尋與全文檢索。
   - `literature-search-biorxiv`：bioRxiv / medRxiv 生物醫學預印本追蹤。
   - `literature-search-europepmc`：Europe PMC 開放獲取全文與引用網絡。
   - `literature-search-openalex`：OpenAlex 全球跨領域學術圖譜。
   - `embl-ebi-ols`：EMBL-EBI 生物本體詞庫查詢 (GO, DOID, HP)。
   - `quickgo-database`：Gene Ontology (GO) 功能與基因產物映射。

5. **古文字學與自定義工作流 (Specialized & Utilities)**：
   - `predictingthepast`：古代拉丁文 (Aeneas) 與古希臘文 (Ithaca) 修復與定年。
   - `workflow-skill-creator`：將多步驟研究流程封裝為標準 Skill。
   - `uv`：高效 Python 套件管理工具鏈。
   - `credentials`：嚴格安全之金鑰驗證與注入協議。

---

## 3. 實戰踩坑紀錄與排錯策略 (Technical Pitfalls & Mitigations)

### 踩坑 1：Windows 下「波浪號路徑」誤解 (`~` vs Desktop)
- **現象**：使用者嘗試建立環境檔時，誤以為 `~` 指的是「桌面」，而在檔案總管中建立了 `C:\Users\YangminRoom1\~.env`，導致所有 SDK 遍尋不著設定檔。
- **原因**：Unix 體系中 `~` 指代使用者家目錄（User Profile），在 Windows 上對應於 `C:\Users\YangminRoom1\`，而非 `Desktop`。此外，Windows 檔案總管會將以點號開頭的檔案（`.env`）視為隱藏檔案或無檔名副檔名。
- **排錯策略**：
  1. 使用 PowerShell 明確指定完整家目錄：`$HOME\.env` 或 `C:\Users\YangminRoom1\.env`。
  2. 若要在檔案總管操作，可在「檢視」中開啟「隱藏的項目」。

---

### 踩坑 2：`.env` 自然語言格式陷阱 (Key-Value Syntax vs Human Label)
- **現象**：使用者在 `.env` 中寫入以下文字：
  ```text
  NCBU API_Key: <36-char-key>
  AlphaGenoe API_Key: <39-char-key>
  ```
- **原因**：
  1. 變數名稱錯字（`NCBU` 應為 `NCBI`，`AlphaGenoe` 應為 `AlphaGenome`）。
  2. 使用冒號與空白（`API_Key:`）而非嚴格等號鍵值對（`KEY=VALUE`）。
  3. `python-dotenv` 與標準環境變數加載器要求嚴格正則表達式 `^[A-Za-z_][A-Za-z0-9_]*=.*$`，任何非標準行會被直接忽略，造成 API 請求時靜默退回未認證模式或拋出 401 Unauthorized。
- **排錯策略**：
  透過 PowerShell 腳本以正則安全解析 Token 長度，自動重建標準 `.env`：
  ```ini
  NCBI_API_KEY=959...a07
  ALPHAGENOME_API_KEY=AIza...
  ```

---

### 踩坑 3：安全憑證協議 (Safe Credentials Protocol)
- **現象**：在排查 API Key 時，若直接執行 `cat .env` 或 `Get-Content .env`，會將敏感金鑰暴露至 LLM 聊天歷程與日誌記錄中。
- **排錯策略**：
  嚴格遵循 `credentials` skill 規範：
  - 僅驗證鍵名是否存在與 Token 長度（如 NCBI 36 字元、AlphaGenome 39 字元）。
  - 對外輸出時一律使用遮罩（如 `[SECRET_OF_LENGTH_39]`），絕不在 stdout 打印明文。

---

### 踩坑 4：Python 依賴隔離與 `uv run --project` 解析路徑
- **現象**：直接執行 `uv run scripts/alphagenome_atlas_avi.py` 遭遇：
  ```text
  ModuleNotFoundError: No module named 'alphagenome'
  ```
- **原因**：
  各 skill 底下擁有獨立的 `pyproject.toml`（指定了 `alphagenome>=0.9.0`、`polars`、`anndata` 等）。若當前工作目錄為使用者家目錄，`uv` 會使用全域預設 Python 環境，而非 skill 的專案虛擬環境。
- **排錯策略**：
  呼叫特定 skill 的腳本時，必須帶上 `--project` 參數指明 skill 根目錄：
  ```powershell
  uv run --project "$SKILL_DIR" "$SKILL_DIR/scripts/alphagenome_atlas_avi.py" [args...]
  ```
  `uv` 會自動建立並快取隔離虛擬環境（安裝 54 個套件耗時不到 1 秒）。

---

### 踩坑 5：Git 備份與大檔排除 (`.venv` 膨脹陷阱)
- **現象**：在準備將科學套件提交至 GitHub 倉庫時，發現插件目錄高達 560MB。
- **原因**：在執行 AlphaGenome 實跑測試時，`uv` 在 `alphagenome_variant_impact_score/.venv` 產生了包含 `scipy`、`polars`、`pyarrow` 的二進制庫，若誤入 git 會導致推送失敗或倉庫嚴重肥大。
- **排錯策略**：
  1. 在 `2026-Antigravity/.gitignore` 中增加 `.env`、`.venv/`、`__pycache__/`。
  2. 使用 `robocopy source dest /E /XD .git .venv __pycache__`，將排除虛擬環境後的 3.54MB 純淨代碼複製進倉庫。

---

## 4. 驗證成果 (Live Verification Benchmarks)

1. **NCBI E-Utilities**：
   - 認證金鑰：`NCBI_API_KEY` 生效。
   - 請求配額：由公用頻寬 3 req/sec 提升至認證頻寬 **10 req/sec**。
2. **Google DeepMind AlphaGenome Atlas**：
   - 認證金鑰：`ALPHAGENOME_API_KEY` 生效。
   - 實跑變異株：`chr9:128225994:G>A`。
   - 輸出指標：
     - **AVI Phred Score**: `24.66`（前 0.34% 高衝擊變異）。
     - **Top Modality**: `Splicing`（剪接破壞特徵貢獻度 `0.77`）。
   - 成功完成雲端即時推理並返回完整 18 模態特徵權重。

# 08 QA 報告 (P1-08, independent QA)

稽核對象：research/02_paper_card.md、03_background_review.md、04_dossier.md、05_glossary.csv、06_fact_sheet.json、07_analogies_visuals.md。
基準：research/raw/*.md（本階段 ground truth）。注意 raw 的 Hesse 2026 全文檔本身是小模型摘要、非逐字（該檔第 2 行），所以本報告的「可追溯」只代表「與 raw 摘要一致」，不代表與 PDF 一致。未使用 verify-with-rubric 技能；檢查依任務所列 (a)–(f) 逐項進行。未修改其他檔案。

## 1. 各檔判定

| 檔案 | 判定 | 摘要 |
|---|---|---|
| 02_paper_card.md | PASS | 數字全部對得上 raw。預印本警示、BFS、2020 與 2026 的區分、無 GNWT/IIT 引用皆正確。 |
| 03_background_review.md | PASS-with-fixes | 有一處過度宣稱（「resolves a long-standing puzzle」），並與 Sheinberg & Logothetis 的敘述略有張力。其餘穩健，[KNOWLEDGE] 標記誠實。 |
| 04_dossier.md | PASS-with-fixes | 數字與警示正確。需修正「看見／被抑制輪流」的措辭可能造成意識本身在切換的誤讀，以及術語不一致。 |
| 05_glossary.csv | PASS-with-fixes | 38 列欄位完整、數字正確。缺 BFS 詞條，部分譯名與他檔不一致。 |
| 06_fact_sheet.json | PASS-with-fixes | 77 筆、id 唯一，inv#1–20 全覆蓋。F40 分類正確（見 §2）。F64、F68 分級有疑義，譯名不一致。 |
| 07_analogies_visuals.md | PASS-with-fixes | 護欄完整。V2 目的句使用已被自己列為禁用的「三十年」，另有計數錯誤與譯名問題。 |

沒有 FAIL。

## 2. 重點查核結果

### (c) 「p = 3×10^-40」（inv#14 / F40）
- 已在 raw/web_biorxiv_hesse2026_fulltext.md 搜尋 `e-40`、`10^-40`、`3×`、`40`，唯一命中是 "full window: 40% conscious"（解碼率）。raw 其他三個檔也沒有。
- 結論是 F40 標為 `unverified` 是正確的，沒有分類錯誤。這個 p 值不在 raw 中，不應標為 verified，也不應引用。
- 全文檔只有可追溯的增益數字：ratio 1.21、r=0.90（F39），這是 inv#14 在 raw 中唯一有根據的部分。「高約 21%」是 1.21 的衍生改寫，F39 的註記已說明。
- 其他 p 值在 raw 中有出處，例如 p=8e-133（斜率 0.23）、p=2e-6、p=0.31。
- 04_dossier §7 與 07 的「不要說」表都已正確把 3×10^-40 列為不採用。
- 只有一個限制：raw 是摘要，所以「摘要中沒有」不等於「PDF 中沒有」。F40 的 notes 用 "No such p-value in raw full text" 是準確的，可以保留。

### 其他分類檢查
- F34、F65（700 ms）、F49（IT–PFC 同步）、F62、F63、F66：raw 中確實找不到，`unverified` 正確。
- F44（30 年）：`unverified` 可接受，但這其實是被 raw 部分反駁的過度宣稱（raw 只說平均「explains」此資料集的弱調變）。見 issue 表 #12。
- F64、F24：標為 `contradicted`，但 raw 只能支持「未見」，不是直接反證。見 issue 表 #10、#11。
- F68 與 F69 來自同一個 raw 檔（web_related_papers.md，標明 "Abstracts and press only"），但分級不同：F68 verified，F69 secondary_only。見 issue 表 #9。
- F72、F73 secondary_only 正確（來源為 idw 新聞稿）。

### (b) 數值一致性
下列數字在 02、04、05、06、07 之間一致，且與 raw 相符：15/s；約 60 ms；HMM 中位 64/59 ms；mean 67 / median 46 ms；0.5 Hz；3501/543/429/661 神經元；2 隻獼猴；14 位人類、82%；61% 對 4%，機率 10%；40%/34%；66%；1.21；EV >80%（僅部分特徵）；PFC 的 EV <80%、形狀 <30%、t(29)=14.2、斜率 0.91/-0.52；19 sessions；r=-0.02。沒有發現數值矛盾。

### (d) 過度宣稱
- 三份文件都沒有把 15 Hz 說成「意識的幀率」，也沒有宣稱「解決意識」。
- GNWT/IIT 全部標為我們的詮釋，未歸給作者（02 §6、03 §5、04 §6、F55）。
- 小問題見 issue 表 #1、#2、#3、#5。

### (f) 其他
- 預印本警示：02、03、04、06（F01）、07（全域硬性提醒 1）皆有。
- 範式為閃光抑制：全部一致。
- 2020 數字（93/57/73）：只出現在 inventory、04 §7、F64、07 的「不要說」表，皆明確標為 2020 且不得歸給 2026。通過。

### (e) zh-TW 用語
- grep 簡體／中國用語（颞、皮层、信息、视、层、频、帧、图、个、实验、数据、算法等）：在 04、05、06、07 中未發現簡體字或 PRC 慣用詞。「顳葉、皮質、資訊、演算法」皆為台灣用法。
- 但有一致性與台灣慣用度問題：見 issue 表 #6、#7、#8、#13、#14。

## 3. Issue 表

嚴重度共 0 high、7 med、10 low（共 17 項）。

| # | 檔案 | 位置／id | 問題 | 建議修正 | 嚴重度 |
|---|---|---|---|---|---|
| 1 | 03_background_review.md | 「Where Hesse et al. 2026 fits」第 1 點（約第 78 行） | 寫成 "It resolves a long-standing puzzle"，這是我們替預印本下的判決，語氣超過 raw。raw 只說作者認為平均「explains」弱調變，且僅限此資料集，也未經同儕審查。 | 改為 "It offers a candidate explanation for…, in this dataset" 並加預印本與兩隻猴子的限定。 | med |
| 2 | 03_background_review.md | §1 第 16 行與第 19 行 | 第 16 行說 Sheinberg & Logothetis 1997 發現「大部分」IT 細胞追隨知覺，第 19 行又說 IT 平均調變「far from pure」且 Hesse 說 earlier studies 只見弱調變。兩者有張力，且 Sheinberg 的細節是 [KNOWLEDGE]（記憶）。 | 補一句說明：追隨知覺的細胞比例高，但平均調變幅度不是純粹的看見／沒看見；或把「large fraction」標 UNVERIFIED。 | low |
| 3 | 04_dossier.md | §8 第 1 點 | 「它在極短時間內輪流『看見』與『被抑制』」暗示大腦在 60 ms 內輪流「看見」。raw 明說 stimulus 與 percept 保持不變，交替的是神經群體表徵的內容。 | 改為「群體神經活動在極短時間內輪流表徵『被看見的臉』與『被抑制的臉』；受試者的知覺本身沒有隨之改變」。 | med |
| 4 | 04_dossier.md | §3「白話」（約第 25 行） | 「同時記錄數百個神經元」。raw 只有範例光柵 429 個同步細胞、總計 3501 個跨 session。「數百」是推論。 | 改為「同時記錄數百個神經元（例：範例中 429 個）」，或僅引用 429。 | low |
| 5 | 07_analogies_visuals.md | V2 purpose（約第 82 行） | 「為何三十年來平均活動看起來很弱」。同檔「不要說」表與 F44 都禁止「過去 30 年完全…」。「30 年」不在 raw，且「三十年來」把一個資料集的解釋推廣成全領域。 | 改為「為何過去研究中平均活動看起來調變很弱（限於這份資料集的作者解釋）」。 | med |
| 6 | 05_glossary.csv、06_fact_sheet.json、04_dossier.md、07 | 術語一致性（priming、reconstruction、no-report、ignition） | 同一概念多種譯名：priming 在 05 為「前導刺激」，04 為「啟動圖」，F11 為「啟動圖像」；reconstruction 在 05/07 為「重建」，F33、F34、F46 為「重構」；no-report 在 05/03 為「無報告範式」，F68/F71/07 V8 為「免報告範式」；ignition 在 05 為「點燃」，F73 為「點火」。 | 統一以 glossary 為準：前導刺激、重建、無報告範式、點燃，並同步修改 04、06、07。 | med |
| 7 | 04_dossier.md、06 F56、07 A6 | 「frame rate」譯名 | 04 用「幀率」，F56 與 07 用「影格率」。同一句 Tsao 引語在不同檔有不同譯法，將造成成品用語不一。 | 擇一並列入 glossary，台灣常見為「幀率」或「畫面更新率」，並標註 F56 的譯法需與 04 一致。 | med |
| 8 | 04_dossier.md、06 F20、07 V2 | 「範例光柵」「光柵圖」 | spike raster 在台灣應譯為「脈衝發放點陣圖」或「放電點陣圖」。「光柵」通常指 grating 或 raster scan，會誤導。 | 改為「點陣圖（raster plot）」。 | med |
| 9 | 06_fact_sheet.json | F68 對 F69/F71/F72 | F68（2020 eLife）標 verified，來源 web_related_papers.md，該檔自述「Abstracts and press only」。同檔的 F69 標 secondary_only。同源不同級。 | F68 改為 secondary_only，或在 notes 說明為何是 verified。 | med |
| 10 | 06_fact_sheet.json | F64 | claim 是「93/57/73% 為 2020 eLife 數字」，但 raw 中沒有這三個數字，也沒有 2020 論文的這些結果。標 `contradicted` 不準，notes 自己也承認數字「not in the inputs」。 | 狀態改為 `unverified`（出處未證實），另用 notes 保留「不可歸給 2026」的護欄。 | low |
| 11 | 06_fact_sheet.json | F24 | 「2026 猴子知覺由眼動推論」標 contradicted。raw 只說 "visible text does not describe"，且明說猴子狀態由神經活動推論。方向正確但 raw 是摘要。 | 可維持，notes 加一句「依 raw 摘要；PDF 待核」。 | low |
| 12 | 06_fact_sheet.json | F44 | 標 unverified，但 raw 有部分反證（只說平均 explains，無「entirely」或「30 年」）。與 F10/F24 的 contradicted 標準不一致。 | 改標 contradicted，或統一各項標準並寫在檔頭的狀態圖例。 | low |
| 13 | 06_fact_sheet.json | 整體 | 沒有狀態圖例。「verified」實為「與 raw 摘要一致」，而 raw 本身非逐字，只有部分筆記提醒 "Check PDF before publish"（如 F42、F46、F52–F55 沒有）。 | 檔頭或 README 加圖例：verified = 與 raw 摘要一致，仍待對 PDF；所有 verified 一律視為待核。 | low |
| 14 | 06_fact_sheet.json、07 | 「分箱」「眼眶額葉」 | 「分箱」（bin）為中國用語色彩，台灣較常見「時間窗」「區間」。「眼眶額葉」在台灣多作「眶額葉」，04 已用「眶額」。 | 改為「時間窗（bin）」「眶額葉」。 | low |
| 15 | 05_glossary.csv | 詞條涵蓋 | 沒有 binocular flash suppression（雙眼閃光抑制，BFS）詞條，而這正是全專案最需要固定的範式用語。另 GNWT 譯名為「全域工作空間理論」，03 為「全域神經工作空間理論」，NCC 在 03 為「意識神經相關」，05 為「意識的神經相關物」。 | 新增 BFS 詞條，統一 GNWT 與 NCC 譯名。 | low |
| 16 | 07_analogies_visuals.md | §4 統計 | 稱「不要說清單：17 列」，實際為 18 列。A7 標題「秒針與心跳」但內文是分針與秒針，且「快 30 倍」是推導（內文已自述）。 | 改為 18 列。A7 標題改為「分針與秒針」。 | low |
| 17 | 05_glossary.csv | 檔案格式 | 檔頭帶 UTF-8 BOM。內容本身 39 行、欄位數一致，Excel 可用，但某些解析器會把第一個欄名讀成含 BOM。 | 若要給程式讀取，去掉 BOM；給 Excel 開則保留。 | low |

# 07 類比與視覺／動畫概念庫 (Analogies and Visual Concepts)

task: P1-07 ｜ 性質：構想／規格素材，非完稿腳本 ｜ 供 Phase 2（影片 zh-TW、HTML deck、英文 PPTX、zh-TW blog）取用
事實來源：research/06_fact_sheet.json（僅引用 status 為 verified 或 secondary_only 的 id；status 圖例見 research/06_fact_sheet_README.md，verified 仍須公開前對照 PDF）。
標記：secondary_only 事實於成品中須加「初步」字樣（F07、F08、F56、F58、F59、F60、F61、F69、F71、F72、F73、F76）。

## 0. 全域硬性提醒 (Global guardrails)

1. 一律註明：Hesse et al. 2026 是 bioRxiv 預印本，尚未同儕審查（F01）。
2. 範式稱「雙眼閃光抑制（binocular flash suppression, BFS），雙眼競爭的變體」（F09）。
3. 「每秒約 15 次」是 IT／PFC 群體表徵內容的交替，不是「意識的影格率」（F28、F48、F56 初步）。
4. 只有 2 隻猴（F15）、僅記錄少數腦區（F58 初步）；猴子沒有報告，狀態由神經活動推論（F23）。

---

## 1. 類比 (Analogies)，共 8 則

### A1 兩個電視頻道快速輪流轉台 (Two TV channels, rapid channel-flipping)
- zh-TW：想像一台電視在兩個頻道之間每秒切換約 15 次，而「只有被切到的那一台」當下才上線；兩個節目其實都在播，大腦只是輪流「點名」其中一個。
- EN：Two channels both keep broadcasting; the brain rapidly takes turns "tuning in" to one.
- 對應 fact：F28、F30、F31、F67、F53
- 類比會誤導之處：電視是兩個不同的接收器輪替；論文指出是「同一批神經元」切換內容，沒有分開的意識族群與被抑制族群（F42）。另外頻道切換易讓人以為「被抑制那台是關掉的」，但被抑制刺激在自己的時段完整佔據同樣的臉空間，並非微弱殘餘（F53）。切換的機制未知（F54）。

### A2 無線電分時共用 (Radio / time-division sharing of one line)
- zh-TW：一條電話線讓兩個人輪流講話，每人每次說約 60 毫秒；如果你只錄下「整條線的平均音量」，就聽不出誰在說什麼。
- EN: One line, two speakers taking ~60 ms turns; the average loudness hides who said what.
- 對應 fact：F30、F31、F42、F27、F43
- 類比會誤導之處：電信分時是工程師設計、固定節拍；此處交替的時長有分布（平均 67 ms、中位數約 46 ms，F30），不是規則節拍器。並且「另一個說話者」是被抑制的圖像，而不是另一個人。

### A3 燈塔光束掃過兩片海面 (Lighthouse beam sweeping two patches of sea)
- zh-TW：光束一次只照亮一片海，另一片仍然存在、只是暫時在暗處；光束掃得很快，所以你拿長曝光相機拍，兩片海都「半亮」。
- EN: The beam lights one patch at a time; a long-exposure photo makes both look dim.
- 對應 fact：F27、F43、F45、F53
- 類比會誤導之處：燈塔光束有單一來源與固定週期；大腦中「誰是光束」未知（F54）。也不可暗示有一個中央「聚光燈」在 PFC 指揮，PFC 本身也在交替（F48），並且 ML 與 AM 的切換協調很弱（F47）。

### A4 長曝光照片 vs 單格快門 (Long-exposure photo vs a single fast shutter)
- zh-TW：傳統分析像把一整晚的星軌拍成一張糊掉的長曝光；這篇研究是改用「單次試驗、10 毫秒時間窗（bin）」的快門，才看清每一瞬間。
- EN: Time-averaging is a long exposure that blurs; single-trial analysis is a fast shutter.
- 對應 fact：F27、F29、F43、F35、F60（初步）
- 類比會誤導之處：長曝光是光學上的真實疊加；神經平均的「抵消」是因為兩個相反的強訊號相加，且需經增益等化才消失（r=-0.02，F43）。不要說「過去 30 年完全是平均造成」（F44 contradicted）；作者用語是平均「可解釋」此資料集中的微弱調變。

### A5 兩位歌手共用一支麥克風 (Two singers sharing one microphone)
- zh-TW：同一支麥克風，A 唱一句、B 唱一句。錄成混音後兩人都很小聲，但你把錄音按 60 毫秒切開，每一小段都很清楚。
- EN: One mic, alternating singers; the mix is faint but each slice is clear.
- 對應 fact：F27、F33、F36、F42
- 類比會誤導之處：歌手是兩個主體有意輪流；此處是同一群神經元的內容切換，無「誰在決定」的主體。意識臉在狀態一中解釋變異量「部分特徵」可超過 80%（F33）；不可說成「完美還原」。

### A6 影格／動畫翻頁書 (Film frames / flip-book) — 僅作「反面教材」
- zh-TW：很容易想到「意識像電影，每秒 15 格」。**不要這樣用。** 曹穎（Tsao）明確表示：「我們並未證明意識有影格率」（F56，初步）。可用的安全版本：「被抑制與被看見的內容在皮質群體中快速輪流出現，這不等於意識本身分成離散影格。」
- EN: The flip-book is the metaphor to avoid; Tsao: "We have not shown that consciousness has a frame rate" (preliminary).
- 對應 fact：F56（初步）、F28、F48、F58（初步）
- 類比會誤導之處：整則都是警示。它把「某腦區群體表徵的內容交替」放大成「意識整體是離散的」。意識依賴多個腦區，論文僅報告少數節點（F58 初步）。

### A7 兩個速度的時鐘：分針與秒針 (Two clocks: slow rivalry vs fast alternation)
- zh-TW：你主觀感覺到的「畫面換邊」像慢慢走的分針（約 0.5 Hz），底下卻有一個快上約 30 倍的秒針在跳（約 15 Hz）。
- EN: The perceived switch is the slow hand (~0.5 Hz); beneath it a much faster hand ticks (~15 Hz).
- 對應 fact：F32、F28、F11、F12
- 類比會誤導之處：「快 30 倍」是 15/0.5 的算術推導，論文原文是「快一個數量級以上」（F32）。0.5 Hz 是自由競爭的切換速率，而本研究是閃光抑制（F09），兩者並非同一個現象；不要說兩者「互相驗證」。

### A8 同一批演員演兩個角色 (One cast playing two roles)
- zh-TW：舞台上永遠是同一批演員，下一幕換戲服換角色；沒有第二批「替補演員」專門演被抑制的角色。
- EN: The same actors, new costume each scene; no separate understudy cast.
- 對應 fact：F42、F39、F41
- 類比會誤導之處：演員換角色是有意識的選擇。實際上狀態一中意識內容的調諧增益比狀態二中被抑制內容高約 1.21 倍（F39），且狀態二平均放電率略高（F41）；意謂兩者不是「完全對稱」的角色互換，只是「不同量測」。

---

## 2. 視覺／動畫概念 (Visual / animation concepts)，共 10 則

欄位：purpose／elements／motion／duration／facts／outputs。

### V1 雙眼閃光抑制示範 (Binocular flash suppression demo, red/cyan anaglyph)
- purpose：讓觀眾親身理解「圖像沒變，但看到的東西變了」。
- elements：紅／青立體眼鏡圖示；左眼（紅濾鏡）見圖 A、右眼（青濾鏡）見圖 B；時間軸條（priming → flash）；一個「你看到的」泡泡框。
- motion：(1) 圖 A 單獨出現 1–2 秒，右側泡泡顯示 A；(2) 圖 B 突然「閃現」到另一眼，泡泡瞬間翻成 B，A 以半透明淡出但仍留在螢幕上標示「仍然存在」；(3) 縮小鏡頭顯示 A、B 都在刺激中。
- duration：20–30 秒（影片）；deck／PPTX 用 3 張連續畫面。
- facts：F09、F11、F14、F25、F26
- outputs：video、deck、pptx、blog（分鏡靜態圖）
- 註：猴子無報告（F23）；人類按鍵驗證 82% 報告看到閃現圖（F25）。旁白用「雙眼閃光抑制，雙眼競爭的變體」。

### V2 平均 vs 微時段訊號圖 (Averaged vs micro-epoch signal: why averaging hides the signal)
- purpose：說明「為何過去研究中平均活動看起來調變很弱」（限於這份資料集的作者解釋，預印本）。
- elements：兩條彩色（暖色=意識、冷色=被抑制）方波／放電率曲線，疊成一條灰色平均線；下方「單次試驗」放電點陣圖（spike raster）。
- motion：先顯示平均線（平緩、微弱，斜率 0.23）；然後「拉開」成兩條時而高時而低、互相反相的曲線；再加回平均，看它如何被抵消成平坦。
- duration：25–40 秒。
- facts：F27、F43、F45、F29、F60（初步）
- outputs：video、deck、pptx、blog
- 註：標「作者詮釋：平均可解釋本資料集的微弱調變」，勿寫「完全」（F44 不可用）。

### V3 HMM 狀態時間軸（約 60 毫秒）(HMM state timeline ~60 ms)
- purpose：呈現兩狀態交替的節律與停留分布。
- elements：水平時間軸 0–500 ms；暖／冷色塊代表狀態一／狀態二；每塊上顯示臉的縮圖；比例尺 60 ms。
- motion：色塊從左向右「掃出」，寬度不一（中位 64／59 ms，F31；平均 67 ms，F30）；一個游標標記每次切換；右側計數器「約 15 次／秒」。
- duration：15–20 秒。
- facts：F29、F30、F31、F28、F67
- outputs：video、deck、pptx、blog
- 註：寬度必須不均勻，避免被誤解為節拍器。

### V4 臉部重建：意識 vs 被抑制 (Face reconstruction, conscious vs suppressed)
- purpose：讓觀眾「看見」群體活動被解碼成臉。
- elements：三欄——真實刺激（兩張臉）、狀態一重建、狀態二重建；EV 計量條。
- motion：狀態一時左欄的「被看見的臉」重建變清晰，被抑制的臉淡到機率水平；切換後交換。EV 數字滑入（意識部分特徵 >80%，F33；單次試驗解碼狀態一 61% 對 4%，F36）。
- duration：25–35 秒。
- facts：F33、F36、F35、F37、F53、F67、F46
- outputs：video、deck、pptx
- 註：需加註「部分特徵」；重建圖為示意（非論文原圖，除非取得授權）；腳註「最初分析具循環性，作者以留出神經元處理」（F46）。

### V5 IT／PFC 腦圖：ML、AM、PO、PVL (IT/PFC brain map)
- purpose：定位記錄的 4 個臉部斑塊。
- elements：獼猴側視腦輪廓；IT 內標 ML、AM（fMRI 定位）；PFC 標 PO（眶額葉）、PVL（腹外側）；Neuropixels 探針圖示。
- motion：探針由上方插入，各斑塊逐一點亮；PFC 以較淡的色調標示「重建品質較低」（F50）。
- duration：12–20 秒。
- facts：F16、F17、F18、F19、F48、F50、F51、F52
- outputs：video、deck、pptx、blog
- 註：標註 3501 個視覺反應神經元（F18）、PFC 分析 661 個（F19）。「廣泛皮質現象」為作者「可能」（F52）。勿畫 IT–PFC 同步箭頭（F49 unverified）。

### V6 15 Hz vs 0.5 Hz 時間尺度對照 (Timescale comparison)
- purpose：突顯內容交替遠快於主觀切換。
- elements：上軌（慢）每 2 秒一次翻轉；下軌（快）同一 2 秒內約 30 次小方塊；對數時間尺。
- motion：兩軌同步跑，下軌方塊快速閃動，上軌偶爾整體翻轉。
- duration：15 秒。
- facts：F28、F32、F30
- outputs：video、deck、pptx
- 註：這是示意，不是實測的同一次試驗；且 0.5 Hz 是自由競爭數字（F32）。

### V7 理論地景：GNWT／IIT／Cogitate (Theory landscape)
- purpose：交代脈絡，同時避免「判決」誤讀。
- elements：左 GNWT（前額—頂葉廣播／點燃）、右 IIT（後部「熱區」）、中間 Cogitate 2025（256 人；fMRI、MEG、iEEG；預先註冊）；Hesse 2026 以小標籤放在畫面邊緣，附「未明確引用 GNWT／IIT」。
- motion：兩個理論的預測箭頭射向中間 Cogitate，各被「挑戰」一部分（無持續後部同步、缺乏點燃），再浮現「兩理論皆未被決定性證實或否證」；最後 Hesse 2026 以虛線連接，標「作者未宣稱判定」。
- duration：30–40 秒。
- facts：F72（初步）、F73（初步）、F55
- outputs：video、deck、pptx、blog
- 註：F72／F73 來自新聞稿（idw），標「初步」。Hesse 與 GNWT／IIT 之連結是我們的詮釋，不是作者的（F55）。

### V8 脈絡時間線 2020→2026 (Lineage timeline)
- purpose：展示這條研究線的演進。
- elements：水平時間軸，節點：2020 Hesse & Tsao eLife（無報告、由眼動推論知覺、IT 臉部細胞追蹤知覺，F68）；2025 Kingir 等（初步，預印本，F71）；2025 Cogitate（Nature，F72 初步）；2026 Shi 等 Nature（臉部細胞經 <20 ms 協同事件切換編碼，僅限臉部，F69 初步）；2026-10-16 Hesse 等 bioRxiv（F01）。
- motion：時間軸由左向右逐點展開，最後一點用「預印本、未同儕審查」徽章閃爍。
- duration：20–30 秒。
- facts：F68、F69、F71、F72、F01
- outputs：video、deck、pptx、blog
- 註：Shi 2026 的月份來源不一致（F70 unverified），只標「2026」。2020 的數字（F64 unverified）一律不放。眼動推論只屬 2020（F24 contradicted 的對應正確說法）。

### V9 實驗兩種設計並排 (Experiment 1 vs 2 design strip)
- purpose：為進階觀眾（deck／blog）說明規模。
- elements：兩條時間條：實驗一（前導刺激 2 s、測試 4 s、空白 500 ms；10 張臉組 25 對）；實驗二（1 s／1 s／250 ms；1500 張臉組 750 對）；2 隻猴、場次計數。
- motion：時間條依序填滿；右側計數器跳動。
- duration：15 秒（影片）；deck 一張圖。
- facts：F12、F13、F15、F22
- outputs：deck、pptx、blog（影片可略）

### V10 作者自述限制清單卡 (Limitations card)
- purpose：結尾的負責任收束，避免過度宣稱。
- elements：5 個圖示卡：預印本（F01）、僅 2 隻猴（F15）、重建最初具循環性（F46）、切換機制未知（F54）、ML–AM 協調弱（F47）；另加一張引述卡：「這可能是廣泛皮質現象」（F52）。
- motion：卡片逐張翻面；最後一張「待回答：為何某些微時段進入意識？」（F54）停留。
- duration：15–20 秒。
- facts：F01、F15、F46、F47、F52、F54、F61（初步）
- outputs：video、deck、pptx、blog

---

## 3. 創作者「不要說」清單 (Do-not-say list)

| 不要說 | 為什麼 | 正確替代 | 依據 |
|---|---|---|---|
| 論文題為 "A temporal multiplexing mechanism for conscious perception" | 非預印本題名 | 題名為 "Rapid alternation of conscious and suppressed stimulus representations in the primate brain"（F02） | F04 contradicted |
| 「2026 實驗就是雙眼競爭」 | 不精確 | 「雙眼閃光抑制，雙眼競爭的變體」（F09） | F10 contradicted |
| 「2026 年猴子的知覺由眼動推論」 | 眼動推論屬 2020 eLife | 2026 猴子不報告，狀態由神經活動（LLR + HMM）推論（F23） | F24 contradicted |
| 「意識有影格率」「意識是每秒 15 次閃爍」 | 曹穎已澄清未證明 | 「IT／PFC 群體表徵內容約每秒 15 次交替」（F28、F48） | F57 contradicted；F56 初步 |
| 93%／57%／73% 當作 2026 結果 | 屬 2020 eLife，且本專案輸入未證實（F64 unverified），不得歸給 2026 | 不引用 | F64 unverified |
| 「感知穩定期 700 毫秒」「700 ms 時間平均是兩張臉的模糊疊加」 | 全文查無 | 不引用 | F65、F34 unverified |
| 「過去 30 年的微弱調變完全是平均抵消所致」 | 過度；作者只說平均可解釋此資料集 | 「平均效應可解釋此資料集的微弱調變」（F43） | F44 contradicted |
| 「IT 與 PFC 以 15 Hz 同步切換」 | 原文無跨區同步結果；ML–AM 協調弱 | 「IT 與 PFC 皆有交替；跨區協調證據不強」（F47、F48） | F49 unverified |
| 孤立引用「p = 3×10^-40」 | raw 摘要有此值（F40 verified，非逐字，公開前須對照 PDF），但它是「意識增益對被抑制增益」的比較 p 值，單獨引用易被誤讀為效果大小 | 「調諧增益比 1.21，r=0.90」（F39）；若引 p 值須註明比較對象並待核 PDF | F40 verified（待核 PDF） |
| 「意識微時段區分度恢復到單獨呈現的水平」 | 原文無此比較 | 「部分特徵 EV 超過 80%」（F33） | F66 unverified |
| 「作者稱這是職涯最重要突破」 | 無來源 | 不引用 | F62 unverified |
| 「證據中等至強」 | 筆記作者主觀評分 | 不引用；改述限制 | F63 unverified |
| 「10 ms 微時段」 | 10 ms 為時間窗（bin）寬度 | 「約 60 ms 的狀態」（F29、F31） | F29 備註 |
| 「這篇是 GNWT 對 IIT 的判決」 | 是我們的詮釋，作者未引用 | 「脈絡：Cogitate 2025 對兩理論皆未決定性證實或否證」（F55、F73 初步） | F55 |
| 「推翻數十年的想法」「純粹的意識相關」 | 屬宣傳措辭 | 若引用，註明為曹穎貼文且屬初步（F59） | F59 secondary_only |
| 把 15 Hz 當成 theta 或 alpha、或引注意力 4 Hz 作為印證 | 15 Hz 不在 theta（4–8 Hz）；相關文獻數字未驗證 | 只說作者推測連結到取樣與 theta 相位存取（F55） | F55；F77 unverified |
| 「Shi 2026 發表於 3 月 25 日／5 月 7 日」 | 日期不一致 | 只寫 2026 | F70 unverified |
| 未標預印本 | 違反全域規則 | 一律加註（F01） | F01 |

---

## 4. 統計 (Counts)
- 類比：8 則（A1–A8；A6 為反面教材，已含「不要這樣用」的警示）
- 視覺／動畫概念：10 則（V1–V10；涵蓋指定的 8 項：V1 閃光抑制、V2 平均 vs 微時段、V3 HMM 時間軸、V4 臉重建、V5 腦圖、V6 15 Hz vs 0.5 Hz、V7 理論地景、V8 時間線）
- 不要說清單：18 列
- 本檔引用 id 檢核：除「不要說」表內刻意列出的 contradicted／unverified id（F04、F10、F24、F57、F64、F34、F44、F49、F62、F63、F65、F66、F70、F77）外，A、V 各節僅使用 verified／secondary_only 的 id。

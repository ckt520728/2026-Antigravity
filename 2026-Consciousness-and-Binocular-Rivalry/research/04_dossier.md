# 研究檔案 Dossier：Hesse et al. 2026（P1-04）

證據標籤：[primary-preprint] = 預印本內容（經 02_paper_card 整理）；[secondary] = 新聞、Tsao 的 X 貼文片段、前作論文摘要；[inference] = 我們的推論。
總警示：本文為 bioRxiv 預印本，**尚未經同儕審查**。02_paper_card 所依的原文為摘要式轉述、非逐字；所有數字在公開前須對照 PDF。Tsao 的 X 貼文僅見搜尋片段，屬 secondary。

## 1. TL;DR

**中文：** 2026 年 10 月 16 日，Hesse、Tsao 等人在 bioRxiv 發表預印本（未經同儕審查）。他們在兩隻獼猴的下顳葉（IT）臉部斑塊與前額葉記錄神經元，發現在「雙眼閃光抑制」情境下，同一群神經元約每秒 15 次（每段約 60 毫秒）在「看見的臉」與「被抑制的臉」之間快速切換。這可能解釋為何過去平均活動顯示的意識調變很弱。但作者並未宣稱「意識有影格率」，結果也僅限於兩隻猴子與臉部刺激。

**English:** In a bioRxiv preprint (16 Oct 2026, not peer reviewed), Hesse, Tsao and colleagues report that in two macaques, face-patch populations in inferotemporal (IT) and prefrontal cortex alternate roughly 15 times per second (about 60 ms per epoch) between representing the perceived face and the suppressed face under binocular flash suppression. Averaging over these fast alternations may explain why earlier studies found only weak percept-related modulation. The authors explicitly do not claim that "consciousness has a frame rate"; the evidence is limited to two monkeys and face stimuli.

## 2. 關鍵發現（Key findings）

1. 範式為雙眼閃光抑制（binocular flash suppression，雙眼競爭的變體）：先對一眼呈現前導刺激 1 或 2 秒，再向另一眼閃現第二張圖，後者通常勝出。猴子不報告，知覺由 14 位人類受試者以按鍵驗證（閃現圖被報告 82% 試次）。[primary-preprint]
2. IT 活動在兩種狀態間交替，約每秒 15 次；平均停留約 67 ms（中位約 46 ms），HMM 估計中位約 59–64 ms，故安全說法為「約 60 毫秒（數十毫秒）」。[primary-preprint]
3. 狀態 1 時，群體表徵「意識到的臉」，狀態 2 時反轉為「被抑制的臉」。單次試驗十選一解碼（機率水準 10%）：狀態 1 意識臉解碼 >61%、被抑制臉僅 4%；整個視窗平均為 40% 對 34%。[primary-preprint]
4. 同一批神經元切換內容，並非兩群不同神經元；雙狀態模型在全部 19 個 session 勝過單狀態模型。[primary-preprint]
5. 傳統「調變微弱」（平均斜率 0.23）可由兩狀態平均解釋：增益校正後殘餘相關消失（r = -0.02）。[primary-preprint]
6. 前額葉（PFC）臉部斑塊（PO、PVL）出現定性相似的交替，但重建品質較低；作者寫「可能是廣泛的皮質現象」。[primary-preprint]
7. 比對照：平均模型、僅意識模型、不協調模型各至少在 4 項檢驗中失敗 3 項；以留出神經元處理初期的循環分析疑慮。[primary-preprint]
8. ML 與 AM 兩斑塊間的協調偏弱，作者稱證據「不強」。[primary-preprint]

## 3. 方法

**白話：** 猴子看著一張臉被送到一隻眼睛，接著另一張臉被「閃」進另一隻眼睛，通常只看到後者。研究者用高密度電極（Neuropixels）同時記錄數百個神經元（例：範例中 429 個），每 10 ms 判斷這群神經元此刻「像是在表徵哪一張臉」，再用統計模型把活動切成兩種狀態，並檢驗哪一種對應看見的臉。猴子沒有回答，因此「看見」是參照人類實驗推論而來。

**技術框 (Technical box)** [primary-preprint]
- 2 隻雄性恆河猴（A、M）；Neuropixels 1.0 NHP；Kilosort3。
- 區域：IT 臉斑塊 ML、AM（fMRI 定位）；PFC 斑塊 PO、PVL。
- 3501 個視覺反應神經元（跨 session）；PFC 分析 661 個；範例放電點陣圖（spike raster）中 429 個同時記錄的細胞。
- 實驗 1：前導刺激 2 s、測試 4 s、10 張臉成 25 對；實驗 2：前導刺激 1 s、測試 1 s、1500 張臉成 750 對（子集 60 張）。
- 分析：10 ms 時間窗（bin）的 Poisson 對數似然比（LLR）+ 雙狀態 Poisson HMM；sign-flip 置換檢定（1e5 次）。
- 紅青 anaglyph 眼鏡，刺激 7°。

## 4. 為何重要與含意

**A. 作者主張（authors' claims）** [primary-preprint；部分為 secondary]
- IT 與 PFC 在意識與被抑制內容之間快速交替；被抑制刺激並非微弱殘影，而在自己的時段占據相同的臉空間。
- 此現象可能是廣泛的皮質現象；以區域平均活動尋找意識的神經相關物（NCC）有其限制（Glitchwire 轉述）[secondary]。
- 推測（作者標為推測）：被抑制時段探索替代解釋，意識時段承載送往報告與行動的「工作假說」。

**B. 我們的詮釋（our interpretation）** [inference]
- 「時間選擇」可能補充「哪個腦區」的問題，但這是我們的框架，並非預印本結論。
- 15 Hz 高於 theta（約 4–8 Hz）與一般 alpha 帶；作者與注意取樣、theta 相位等文獻的連結屬主題性類比，不可說成同一種振盪。
- 猴子的「意識」標籤來自神經狀態加人類驗證的推論。

**C. 需避免的媒體過度解讀（press overstatement to avoid）**
- 「意識有影格率／意識是每秒 15 次的閃爍」：Tsao 公開澄清「We have not shown that 'consciousness has a frame rate'」[secondary，澄清串僅見片段，其餘要點未核實]。
- 「推翻數十年思維」「意識的純粹相關物」：屬發表推文的宣傳語氣，勿當結論 [secondary]。
- 「timing, not area」：超出預印本所示 [secondary]。
- 「已解決意識問題」「適用所有感知」：預印本僅測臉部、兩隻猴。

## 5. 限制與開放問題

作者自述 [primary-preprint]：僅兩隻猴；切換機制未知；路由機制僅為推測；早期有循環分析疑慮（已以留出神經元處理）；跨斑塊協調弱；PFC 品質較低。開放問題：「為何某些微時段的表徵能進入覺察，而另些不能？」
我們補充 [inference]：只用臉；猴子無報告；超出臉部的推廣未經驗證；未經同儕審查；數字尚待對照 PDF。

## 6. 與理論的關係

- **GNWT / IIT：** 預印本**並未引用** GNWT 或 IIT，亦未討論 alpha。任何「對 GNWT 或 IIT 的裁決」都是我們的詮釋 [inference]。唯一可說的橋接：兩理論多以非侵入式人類資料在粗時間尺度檢驗；本研究為猴子群體層級、約 60 ms 尺度。PFC 也有交替現象，與前後腦爭論相關，但作者未建立此連結。
- **Cogitate 2025（Nature，256 位人類，fMRI/MEG/iEEG）：** 對 IIT 與 GNWT 都未給出決定性證實或否證 [secondary]。與本研究尺度與方法完全不同，不宜直接比較。
- **節律取樣（rhythmic sampling）：** Landau & Fries 2012、VanRullen 2016、Fiebelkorn & Kastner 2019 等為知覺／注意的節律文獻 [secondary，部分為記憶中的經典]。預印本討論中提及注意取樣、theta 相位工作記憶存取、眶額交替、海馬 theta 閃動，屬討論性連結 [primary-preprint]。

## 7. 前作脈絡（Lineage）

- **2020 eLife**（Hesse & Tsao）：猴 IT 臉細胞，以眼動推論知覺、無主動報告；知覺與被抑制刺激皆可單次試驗解碼 [secondary]。
- **2026 Nature**（Shi, Bi, Hesse, Lanfranchi, Chen, Tsao）：IT 臉細胞經 <20 ms 的群體協同事件，由一般偵測碼切換為臉特異碼，僅限臉 [secondary]。發表日期有分歧（3 月 25 日對 5 月 7 日），引用時只寫 2026。
- **2026 預印本**（本研究）：同一團隊與範式系列；新增「約 60 ms 的內容交替」[inference：銜接關係為我們所述]。
- **數字防混：** 影片筆記中「人類 93%／ML 57%／AM 73%」屬 **2020 eLife**，**不得**歸給 2026。2026 的人類驗證數字是 82%。
- 筆記中的 "Astera Institute" 與題名 "A temporal multiplexing mechanism…" 與卡片（UC Berkeley/Caltech/Princeton；題名 Rapid alternation…）不一致，**以卡片為準**；僅見影片筆記的數字（如 700 ms）不採用。p=3×10^-40 已在 raw 全文摘要中找到（F40，verified＝與 raw 摘要一致，非逐字），可引用，但公開前須對照 PDF，並須註明比較對象（意識增益對被抑制增益），勿單獨當成效果大小。

## 8. 給一般大眾的關鍵訊息（≤5）

1. 大腦對同一張看不見的圖並非「完全沒反應」：群體神經活動在極短時間內輪流表徵「被看見的臉」與「被抑制的臉」；受試者的知覺本身沒有隨之改變。
2. 這個切換約每秒 15 次，每段只有數十毫秒，比我們察覺到的知覺切換快得多。
3. 這可能解釋為何過去平均起來看不到清楚的意識訊號。
4. 這是預印本，尚未同儕審查，僅兩隻猴子、僅臉部。
5. 不等於「意識有影格率」，作者自己也這麼說。

## 9. 建議的 zh-TW 安全說法

- 頻率：「約每秒 15 次」；時長：「每段約 60 毫秒（數十毫秒）」。避免寫「精確 15 Hz」「剛好 67 毫秒」。
- 範式：「雙眼閃光抑制（雙眼競爭的一種變體）」；勿寫成「經典雙眼競爭」。
- 猴子：「猴子沒有回報看到什麼；知覺由 14 位人類受試者驗證，82% 的試次看到閃現的圖」。
- 規模：「兩隻獼猴、共記錄約三千五百個有視覺反應的神經元」（總計 3501，勿說每次數千）。
- 解碼：「在『意識』時段，十選一的單次辨識率超過 61%（隨機為 10%），被抑制那張臉僅約 4%」。
- 立場：「研究團隊的初步發現，尚待同儕審查與重複驗證」；「作者表示並未證明意識有影格率」。
- 範圍：「在這個臉部實驗中」，勿寫「大腦的意識」「所有感知」。
- 慎用：「證明」「揭開意識之謎」「推翻」。

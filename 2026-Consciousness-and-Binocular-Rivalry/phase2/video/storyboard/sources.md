# sources.md — P2-V1 影片分鏡腳本事實對照表

本文件列出 `phase2/video/storyboard/script_zh_tw.md` 與 `storyboard.json` 引用之事實清單。

## 1. 引用之 Verified 事實清單（共 23 筆）

| Fact ID | Status | 核心陳述與數值 | 出現鏡頭（Shot ID） |
|---|---|---|---|
| **F01** | verified | bioRxiv 預印本，2026-10-16 發表，尚未經同儕審查 | SHOT-12 |
| **F02** | verified | 論文題名：Rapid alternation of conscious and suppressed stimulus representations in the primate brain | SHOT-12 |
| **F03** | verified | 作者群：Hesse, Lanfranchi, McGrory, Shi, Engel, Tsao | SHOT-12 |
| **F05** | verified | DOI：10.64898/2026.10.15.759299 | SHOT-12 |
| **F06** | verified | 機構：UC Berkeley、Caltech BBE、Princeton、HHMI | SHOT-12 |
| **F09** | verified | 範式：雙眼閃光抑制（BFS），雙眼競爭的一種變體 | SHOT-02 |
| **F11** | verified | 前導刺激 1 或 2 秒後閃現新影像，通常占優 | SHOT-02 |
| **F15** | verified | 2 隻雄性恆河猴受試 | SHOT-04 |
| **F16** | verified | Neuropixels 1.0 NHP 探針記錄 | SHOT-04 |
| **F17** | verified | 記錄斑塊：下顳葉 ML、AM 與前額葉 PO、PVL 四個斑塊 | SHOT-04 |
| **F18** | verified | 跨場次共 3501 個視覺反應神經元 | SHOT-04 |
| **F19** | verified | 前額葉皮質分析 661 個神經元 | SHOT-04 |
| **F23** | verified | 猴子無主動按鍵報告，狀態由神經放電推論 | SHOT-05 |
| **F25** | verified | 14 位人類受試者按鍵驗證，82% 試次報告閃現圖 | SHOT-02 |
| **F27** | verified | 時間平均調變微弱，斜率約 0.23 | SHOT-03 |
| **F28** | verified | 神經群體約每秒 15 次（約 15 Hz）交替 | SHOT-07 |
| **F29** | verified | 10 ms 時間窗 Poisson LLR + 雙狀態 HMM 演算法 | SHOT-05 |
| **F30** | verified | 微時段停留時間平均 67 ms、中位約 46 ms，約 60 ms | SHOT-07 |
| **F31** | verified | HMM 中位停留：狀態一 64 ms、狀態二 59 ms | SHOT-07 |
| **F38** | verified | 雙狀態模型於 19/19 場次全面勝過單狀態模型 | SHOT-06 |
| **F39** | verified | 調諧增益比 1.21（意識增益 vs 被抑制增益，效果量） | SHOT-09 |
| **F40** | verified | p = 3×10^-40，連同 F39 之增益比較脈絡引用 | SHOT-09 |
| **F41** | verified | 狀態二平均放電率略高 | SHOT-08 |
| **F42** | verified | 同一批神經元切換內容，並非兩群分開之細胞 | SHOT-07 |
| **F43** | verified | 時間平均消解效應可解釋本資料集微弱調變 | SHOT-09 |
| **F48** | verified | 下顳葉與前額葉皮質皆展現定性相似之高速交替 | SHOT-10 |
| **F52** | verified | 作者討論：這可能是廣泛的大腦皮質現象 | SHOT-10 |
| **F53** | verified | 被抑制刺激並非微弱殘影，在自己的時段占據相同臉空間 | SHOT-08 |
| **F67** | verified | 狀態一表徵看見的臉、狀態二表徵被抑制的臉，約 60 ms | SHOT-07 |

## 2. 引用之 Secondary_Only 事實（已標示初步）

| Fact ID | Status | 核心陳述 | 出現鏡頭（Shot ID） |
|---|---|---|---|
| **F56** | secondary_only | Doris Tsao 澄清：「我們並未證明意識有影格率」（標示初步） | SHOT-11 |

## 3. 防範檢驗與合規紀錄

- **F57（「意識有影格率」，contradicted）**：於 SHOT-11 中作為明確反駁與澄清對象，永久禁止宣稱意識有影格率。
- **預印本聲明**：於 SHOT-12 與腳本開頭明確標註「bioRxiv 預印本、尚未經同儕審查」。
- **用語合規**：全篇使用台灣繁體中文規範（資訊、演算法、皮質、顳葉、影片），口語旁白數字拼讀（如「約每秒十五次」、「三千五百個神經元」）。
- **總時長**：12 個鏡頭時長總和為 240 秒整，符合目標 240 s（範圍 180–300 s）。

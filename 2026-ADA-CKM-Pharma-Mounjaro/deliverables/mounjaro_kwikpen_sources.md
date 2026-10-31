# 來源與製作範圍

查閱日期：2026-10-31。成品為繁體中文衛教示範，非個別處方。作者、機構與COI未經確認，影片不擅自署名。

主要操作及用藥來源為國立陽明交通大學附設醫院網站提供的台灣原廠文件：

| 文件 | 版本與使用範圍 | 網址 |
|---|---|---|
| 台灣仿單 | 內文版本2025-10-03；劑量、適用性、禁忌、安全、避孕 | https://www.hosp.nycu.edu.tw/images/8600/Document/8600-2026/8600_202604_30.pdf |
| 台灣用藥指引 | Literature revised 11 Sep 2025；病人衛教補充 | https://www.hosp.nycu.edu.tw/images/8600/Document/8600-2026/8600_202604_31.pdf |
| 台灣 KwikPen IFU | 末頁 Revised 24 Mar 2026，內碼20260121；操作步驟1–17、保存、排氣失敗重試 | https://www.hosp.nycu.edu.tw/images/8600/Document/8600-2026/8600_202604_32.pdf |
| UK SmPC | 2026-08-29；交叉核對劑量與保存 | https://www.medicines.org.uk/emc/product/15482/smpc |
| UK PIL / manual | 交叉核對病人說明；不同器型仍以隨盒為準 | https://www.medicines.org.uk/emc/product/15482/pil |
| Canada KwikPen IFU | 2026-07-06；親看PDF圖確認全劑1、完成0及長線排氣 | https://pi.lilly.com/ca/mounjaro-ca-ifu-kp.pdf |
| SURMOUNT-1 | DOI 10.1056/NEJMoa2206038；僅提72週試驗與可能幫助減重，無六個月成效保證 | https://www.nejm.org/doi/full/10.1056/NEJMoa2206038 |

院方網址中的2026/04不是仿單版次，未宣稱已確認TFDA最新即時全文。NEJM本輪直連403；相關研究內容亦載於上述台灣仿單臨床試驗章節，影片不使用未讀取全文的數字。

生活調整、每週／每月追蹤、基線／4／12／24–26週評估是教育性管理建議，非仿單規定的固定回診處方。24週約六個月，實際六個曆月約26週，需依起始日期安排。沒有病人資料、模擬療效曲線或減重保證。

## 素材來源

- 所有筆身、部件、皮下組織、注射部位、決策分支、追蹤表均為本次以SVG程式繪製的自訂線稿。不是器材實拍，也不主張比例或顏色等同商品；未使用品牌照片、Logo或付費生成圖。
- 配音：edge-tts，zh-TW-HsiaoChenNeural，逐句合成公開衛教內容；75句實際MP3。無配樂。此動作向TTS服務傳送公開衛教稿，無病人資訊。
- 字型：Noto Sans TC Variable，本機素材複製並以fontTools保留影片所需字形。完整字型與縮減字型均附本機assets。字型屬SIL Open Font License，https://github.com/notofonts/noto-cjk/blob/main/LICENSE 。
- 動畫：本機 GSAP、HyperFrames v0.8.171。一般影片lazy workflow更新回Unknown skill，實作改依已安裝core/CLI/keyframes契約；單檔HTML，未宣稱官方workflow自動化完成。
- FFmpeg／FFprobe：主控下載的npm portable依賴，置於tools/npm-bin，不更改系統全域PATH；僅於渲染process設定PATH。
- 指定GitHub技能以gh api取得base64資料並用Python解碼，讀取motion-explainer-images、motion-design、review-loop及lessons，檔案留在本資料夾作流程依據。未送出feedback，未publish/upload/push。

## 未採用的輸入

References內數格拆劑、抽殘液、合併不同筆、以較高強度筆拆成較小劑量、5直接跳10 mg及固定逐月必升方案均未採用。依官方IFU只示範每支四個完整固定劑量。

# Mounjaro 教材 Production Brief（核准前規劃）

版本：v0.2-review｜整理日：2026-10-30（Asia/Taipei）  
狀態：**規劃 only；outline approval = pending；T4 未派發**。本檔不是任何成品的完成或發布授權。

## 1. 共同輸入與硬 gate

- 主大綱：[slide_outline.md](slide_outline.md)（26 頁，v0.2-review）。
- 證據：[claim ledger](../evidence/claim_ledger.csv)、[source registry](../evidence/source_registry.json)、[evidence summary](../evidence/evidence_summary.md)、[search log](../evidence/search_log.md)。
- 素材：[canonical ZIP manifest](../sources/zip_manifest.json)、[NotebookLM 紀錄](../sources/notebooklm_summary.md)、[house style](../sources/house_style/)。
- 受眾：醫療專業人員。核心原則：先對齊 molecule／brand／formulation／dose／population／comparator／endpoint／jurisdiction，再談選擇。
- 啟動條件：使用者必須對指定 outline **版本與 SHA-256** 明確核准，並記錄日期與範圍；之後才另拆 T4 production Tasks。
- 另需確認：作者／機構／COI、台灣現行完整仿單與給付、各成品工具與費用上限、homepage 整合方式；全部 `[TO CONFIRM]`。
- 發布、上傳、寄送、GitHub push、公開分享與付費生成均需各自明確授權；沉默或舊研究 approval 不可沿用。

## 2. 內容與素材政策

1. 所有臨床數字必須對應 claim ID、source ID 與 locator；新內容若超出 ledger，先回 primary source 查核，不在製作階段補猜。
2. USA／UK／Taiwan 文件分開；P001–P003 未通過前，不產台灣劑量圖、給付表、妊娠停藥間隔或麻醉固定停藥天數。
3. 禁用「萬能鑰匙」、「手術般療效」、直接抗炎／心腎全面受益、GIP 止吐因果及 HF 住院過度陳述。
4. 不呈現拆筆格數、抽殘藥、跳級、同週拼筆、採購省錢方案；archive 僅供稽核。
5. 既有合法素材與純 CSS/SVG／Chart.js 優先。需要新圖時，先另交 `image_briefs.md` 與工具／費用授權；本輪不生圖。
6. 各成品保留 trial funding、open-label、abstract-only、exploratory、US-only 等限制，不因版面相容而刪除關鍵邊界。

## 3. 各成品工作包（核准後才執行）

| 工作包 | 規劃輸入與輸出 | 實際工具／授權前置 | 獨立驗收 |
|---|---|---|---|
| Motion explainer | 由 26 頁大綱另壓縮為旁白節拍、分鏡、字幕與來源卡；輸出格式／長度 `[TO CONFIRM]`。 | 使用實際可用的 HyperFrames／motion workflow；中文旁白、音樂、生圖與渲染工具及費用另批。 | 逐 beat 檢查數字與 claim IDs；字幕無截斷；音訊／影片實際渲染後抽幀 contact sheet 與播放驗收；不得只驗腳本。 |
| Paper document explainer | 以同一證據鏈製作專業人員閱讀版，含摘要、對齊表、安全邊界、參考資料；格式與篇幅 `[TO CONFIRM]`。 | 文件工具與輸出格式另確認；若指定 DOCX/PDF，使用相應實際工具，不假稱生成。 | 全篇 claim/source 對應、表格與分頁 readback；若產 PDF，逐頁渲染檢查；引用與 pending 標記完整。 |
| SOIL HTML deck | 依 26 頁 outline 製作單一 HTML，含 P06／P14 Check-Points 與 RWD。 | 採 `soil-html-deck`；圖片須 base64 內嵌；互動投票或外部連線另授權。 | 瀏覽器逐頁操作、鍵盤導航、RWD、console、連結與圖片離線檢查；所有數字對 ledger。 |
| Editable PowerPoint deck | 與 HTML 同源，但文字／表格可編輯；不是把每頁截圖貼入。 | 採 `soil-teaching-deck` 與實際可用的 PPTX 工具；Windows／PIL／COM 問題依實際環境處理。 | 重新開啟 PPTX，檢查頁數、文字可編輯、字型／溢出／遮擋；實際渲染逐頁 QA。 |
| Homepage blog draft | 將 One Big Idea 改寫為專業人員文章，保留四脈絡與安全邊界；發布位置與 metadata `[TO CONFIRM]`。 | 參考既有 homepage house style；作者／機構／COI 與發布授權另批。 | 草稿事實核對、連結與引用檢查、 homepage 預覽／RWD；公開發布另行核准。 |

## 4. 建議順序與停止點

1. **Outline gate**：取得指定 hash 的明確核准；未核准即停止。
2. **Evidence gate**：完成 P001–P003 中與所欲成品直接相關的項目；若使用者選擇保留 pending，相對內容必須刪除或明顯標記，不得補寫。
3. **Design gate**：確認各成品範圍、時長／篇幅、作者／機構／COI、既有圖片與新圖需求、工具與費用上限。
4. **Asset gate**：先產 image briefs；新圖回來後逐張 QA，未通過不打包。
5. **Build gate**：各工作包獨立產生與驗收，不把一種成品的完成推定為其他成品完成。
6. **Release gate**：另行取得發布授權後才可上傳、push、分享或寄送。

## 5. 本輪明確不做

- 不產最終 HTML、PPTX、影片、公開 blog、新付費圖片或個別病人處方。
- 不把 host subagent 分工寫成 JEV automatic routing ready，不宣稱 300 swarm、token savings 或完整成本。
- 不修改 canonical ZIP、舊研究、`handoff.md` 或沿用舊案 Gate 3／4 approval。

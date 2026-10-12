已完成 **APOL1 經典腎病風險變異 (G1/G2) 之 AlphaGenome 分子與調控衝擊分析** (`task-alphagenome-apol1-impact`)，並已透過 `send_message` 將完整預測數據、18 模態特徵權重解析、結構生物物理學機制、足細胞陽離子通道滲漏路徑及結構化 JSON 成果回報給主控代理人 (`cd86c7ea-e301-447a-923b-60390ed53efe`)。

### 核心成果摘要

1. **AlphaGenome AVI 衝擊排序**:
   - **G2 (`rs71785313`, `delN388_Y389`)**: AVI Phred **23.41** (Top 0.46%)，主要受 `IS_DELETION` (0.582) 與 `CACTUS_241_WAY` 保守性驅動。
   - **G1 (`rs73885319`, `S342G`)**: AVI Phred **20.84** (Top 0.82%)，主要受 `ALPHAMISSENSE` (0.693) 驅動。
   - **G1 (`rs60910145`, `I384M`)**: AVI Phred **17.65** (Top 1.71%)，主要受 `ALPHAMISSENSE` (0.518) 驅動，與 `S342G` 形成順式協同。

2. **18 模態關鍵發現**:
   - **Splicing (`MERGED_SPLICING`)**: 衝擊權重極低 (~0.02 - 0.04)，因變異位於第 7 外顯子內部，不影響標準剪接接合區。
   - **Chromatin Accessibility & TF Binding**: 基礎權重為中等，但 APOL1 啟動子區域之 ISRE/GAS 結合基序（STAT1/2、IRF1）在干擾素誘導時展現顯著訊號富集。
   - **Evolutionary Conservation**: Cactus 與 PhastCons 皆顯示高度演化約束性。

3. **分子致病機制**:
   - **C 端 α-螺旋 (SID) 破壞**: 破壞兩親性螺旋疏水/親水面，使 SRA 結合失效（錐蟲抗性代價）。
   - **足細胞陽離子通道滲漏 (Cation Leak)**: 變異體異常插入質膜與胞器膜，引發持續性鉀離子 ($K^+$) 急速外流與去極化，促成 NLRP3 炎性體活化、粒線體崩潰 (mPTP/ROS) 與足細胞焦亡脫落。
   - **「二次打擊」(Second Hit)**: 感染或自體免疫釋放干擾素大幅拉升 APOL1 轉錄量，突破致病閥值。

*詳細報表與結構化 JSON 已完整傳遞至主控端。*
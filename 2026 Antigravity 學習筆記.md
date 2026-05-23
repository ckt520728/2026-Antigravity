# 🧠 2026 Antigravity 學習筆記：計算神經動力學與循環網路設計艙

本學習筆記詳實記錄了 **2026 Antigravity 神經動力學學習艙** 的核心數學物理描述、Sussillo 學術系列之群體幾何流形架構，以及在 Rigorous Sandboxed Iframe (沙盒環境) 下開發複雜 Web 應用的致命避坑 SOP 與解決方案。

---

## 🔬 第一部分：計算神經動力學 (Computational Neurodynamics) 學術精華

### 1. 單一神經元尺度：LIF 電生理常微分方程 (ODE)
膜電位 $V(t)$ 被視為具有洩漏性的微型電阻-電容 (RC-Leak) 電路。其電量隨時間變化的基本一階常微分方程為：
$$\tau_m \frac{dV}{dt} = -(V - V_{\text{rest}}) + R_m I_{\text{ext}}$$

#### 非線性硬閾值重置機制：
$$\text{If } V(t) \ge V_{\text{th}} \quad \Rightarrow \quad V(t) = V_{\text{spike}} \text{ (放電)} \quad \Rightarrow \quad V(t + \Delta t) = V_{\text{reset}}$$

#### 放電頻率 $f$ 的嚴格非線性數學解析解：
若持續刺激電流 $I_{\text{ext}} > \frac{V_{\text{th}} - V_{\text{rest}}}{R_m}$，則其發放頻率為：
$$f(I_{\text{ext}}) = \left[ t_{\text{ref}} + \tau_m \ln \left( \frac{R_m I_{\text{ext}} + V_{\text{rest}} - V_{\text{reset}}}{R_m I_{\text{ext}} + V_{\text{rest}} - V_{\text{th}}} \right) \right]^{-1}$$

---

### 2. 耦合核團網路尺度：巴金森氏症 STN-GPe 與極限環吸引子 (Limit Cycle)
在多巴胺缺乏狀態下，興奮性 STN 與抑制性 GPe 核團形成強烈的非線性反饋，系統常微分方程組為：
$$\tau_S \frac{dV_S}{dt} = -(V_S - V_{S,\text{rest}}) - W_{GS} f(V_G) + I_{\text{DBS}}(t)$$
$$\tau_G \frac{dV_G}{dt} = -(V_G - V_{G,\text{rest}}) + W_{SG} f(V_S)$$
其中放電率函數為非線性 Sigmoid：$f(v) = [1 + \exp(-k(v - V_{\text{mid}}))]^{-1}$。

#### 💡 吸引子幾何物理意涵：
- **DBS 關閉**：相平面上呈現一個完美的封閉軌道 —— **極限環吸引子 (Limit Cycle Attractor)**。系統最終會收斂到此軌道，產生每秒 4-8 次的病理性靜止震顫。
- **DBS 開啟 (130Hz 高頻強迫電刺激)**：高頻強烈脈衝撕碎相空間流速場，極限環流形瓦解，狀態軌跡脫同步均勻分佈，病理震顫消失。

---

### 3. 群體動力學尺度：David Sussillo 連續時間 RNN 幾何學
大腦皮質運算並非由單一神經元主導，而是投射到低維主成分空間的群體軌跡（Population Trajectory）：
$$\tau \frac{dx_i}{dt} = -x_i + \sum_{j=1}^N W_{ij} \tanh(x_j) + W_{\text{FB}} z(t) + I_i(t)$$
其中輸出為 $z(t) = \mathbf{W}_{\text{out}} \mathbf{r}(t)$，神經元放電率 $r_i = \tanh(x_i)$。

#### RLS (Recursive Least Squares) FORCE 更新機制：
在不更改內部隨機混沌突觸 $W_{ij}$ ($g > 1.5$) 的狀況下，僅藉由線上高頻微調 Readout 突觸 $\mathbf{W}_{\text{out}}$ 穩定混沌：
$$\mathbf{e}(t) = \mathbf{W}_{\text{out}} \mathbf{r}(t) - \mathbf{f}(t)$$
$$\mathbf{P}(t) = \mathbf{P}(t-\Delta t) - \frac{\mathbf{P}(t-\Delta t) \mathbf{r}(t) \mathbf{r}(t)^T \mathbf{P}(t-\Delta t)}{1 + \mathbf{r}(t)^T \mathbf{P}(t-\Delta t) \mathbf{r}(t)}$$
$$\mathbf{W}_{\text{out}}(t) = \mathbf{W}_{\text{out}}(t-\Delta t) - \mathbf{e}(t) \mathbf{P}(t) \mathbf{r}(t)$$

#### 幾何慢速流形與多工計算 (Dynamical Motifs)：
Sussillo & Barak (2013) 指出，RNN 並非靠單一固定點運作，而是利用優化算法 (L-BFGS) 逼近 $\frac{dx}{dt} \approx 0$ 的 **慢速流形 (Slow Manifold)**。藉由將不同的任務動力學放在互為**幾何正交的低維子空間**中：
$$x(t) = \sum_{k} \mathbf{v}_k y_k(t) + x_0$$
切換輸入時系統切換平行相平面，完美實現多工作業且徹底防範災難性遺忘 (Catastrophic Forgetting)。

---

## 🚨 第二部分：Rigorous Sandboxed Iframe (沙盒環境) 致命避坑 SOP

在高級 Web Preview 的沙盒限制下，網頁應用極易因安全權限限制、編碼不一致或瀏覽器非同步加載而徹底空白崩潰或靜音。以下為歷經實踐檢驗的避坑 SOP：

### Bug 1: Lucide 圖標 CDN 加載失敗，導致 ReferenceError 全白崩潰
* **踩坑實錄**：在 TypeScript React 中直接導入 `lucide-react`，若 Preview 環境沒有連接 NPM 依賴或 CDN 加載 ReferenceError，網頁會整頁空白不顯示。
* **SOP 解決方案**：
  在 App 中使用 Try-Catch 彈性降級，或手寫微型手繪 SVG 向量圖。本專案將 Lucide components 包裹在 try-catch 中，一旦加載失敗自動切換為高質感 Emoji 或是 inline SVG，保證 Preview 100% 健全可視。

### Bug 2: 沙盒 Secure Iframe 語音合成 `SecurityError` 崩潰
* **踩坑實錄**：在受限沙盒 Iframe 中，呼叫 `window.speechSynthesis.speak()` 會拋出 `SecurityError: Blocked read/write access to speech API`，導致定時器卡死，網頁直接崩潰。
* **SOP 解決方案**：
  - 用極度嚴謹的 `try-catch` 包裹所有 `speechSynthesis` API 的呼叫。
  - **必須實作 Time-based Fallback 定時器**：一旦語音 API 被沙盒拒絕，立刻自動降級到用前端 JavaScript 的 `setInterval` 與播放速率連動，模擬播客進度條前進、EQ 聲學頻譜起伏與字稿高亮，保證無聲狀態下用戶體驗依舊無縫運作！

### Bug 3: Web Speech API 播客語音微弱 / 靜音 Bug
* **踩坑實錄**：在 Chrome 與 Edge 瀏覽器下，語音列表加載是**非同步**的。若直接呼叫 speak 且未指定 `lang = 'zh-TW'`，瀏覽器會使用預設的英文系統語音去拼讀中文，發出極小像蚊子的雜訊或乾脆完全靜音！
* **SOP 解決方案**：
  1. 呼叫 speak 之前，必須強制指定 `utterance.lang = 'zh-TW'`。
  2. 強制設定音量 `utterance.volume = 1.0` (極大化)。
  3. **必須動態獲取繁體中文語音**：
     ```javascript
     const voices = speechSynthesis.getVoices();
     const zhVoice = voices.find(v => v.lang === 'zh-TW' || v.lang === 'zh_TW') ||
                     voices.find(v => v.lang.toLowerCase().includes('zh')) ||
                     voices.find(v => v.lang.toLowerCase().includes('cmn'));
     if (zhVoice) { utterance.voice = zhVoice; }
     ```
     如此即可確保在 any 本地 Speaker 狀態下，均能發出無比宏亮、標準流暢的台灣繁體中文朗讀聲！

---

## 🛠️ 第三部分：2026 Antigravity 學習艙高級重構與優化

本版本對 App 進行了高維重構，將功能推向極致：

### 1. NotebookLM AI 語音製作艙 (Podcast 面板)
在 Podcast 面板中間新增了高質感的 NotebookLM 合成艙。支持選擇 Neuron 2009 混沌學習、Slow Manifold 2013 慢流形分析、BMI Clinical 解碼器三大學術 Sources，或是讓醫師自定義輸入文本框。點擊合成時：
- **毛玻璃模糊遮罩阻斷**。
- **0~100% 高擬真進度條**。
- **亮綠色 terminal 動態日誌滾動**，展示 NLP 文本解析與 Web Speech 聲院校準。
- 合成結束後，`currentDialogues` 自動被對應主題字稿替換，使用者點擊播放即可立刻進行洪亮清晰的播客朗讀！

### 2. FORCE 混沌學習面板四大場景與 4-Panel 學術圖表
- **引進 `FORCE-RNN-Sim` Skill**：實作 `sinusoid`、`lorenz-output`、`lorenz-internal` (v3)、`fixed-points` 四大模擬場景。
- **參數全面引進滑桿**：
  - 網路規模 $N$ (100 ~ 1500)
  - 增益 $g$ (0.80 ~ 2.00，控制混沌)
  - 正則化 $\alpha$ (1.0 ~ 50.0)
  - 訓練週期 Cycles (5 ~ 100)
  - 主頻率 $f_1$ (0.5Hz ~ 5.0Hz) 與副頻率 $f_2$ (0.5Hz ~ 10.0Hz) 的滑桿與 number input，內部進行週期係數對齊。
  - 「重置與重新訓練」按鈕：一鍵重置 RNN 連接與協方差 $\mathbf{P}$ 矩陣，線上重新即時高頻訓練。
- **4-Panel 學術圖表**：當切換至 `fixed-points` 模式時，Waveform 自動切換為 PC投影、決策分岔分流軌跡、Jacobian  eigenvalues 複數平面分佈、q 直方圖，並滾動輸出 L-BFGS 優化收斂進度。

### 3. 3D Attractor 決策幾何流形面板
- 提供 Point, Line, Limit Cycle, Saddle, Lorenz Chaos 五種 Attraction 相空間繪圖與切換。
- 加入 **「五大吸引子動力學解析艙」**，在切換吸引子時動態展示對應的數學方程、大腦計算角色與臨床實例。
- 3D 空間旋轉速度 `rotSpeed` 與擾動雜訊 `noisePerturb` 滑桿連動，精準呈現大腦決策分岔。

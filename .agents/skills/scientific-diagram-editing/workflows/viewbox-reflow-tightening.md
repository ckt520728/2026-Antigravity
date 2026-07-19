# Workflow: viewBox Tightening & Reflow (畫布收緊與重排佈局)

當科學插圖的子圖排版發生大幅度變更（例如：單列 1x4 橫排重新 reflow 為 2x2 矩陣）時，最常見的美學失敗點是「外層 viewBox 尺寸未更新」，導致圖片周圍產生大片空白帶。請嚴格執行以下重排收緊流程：

## 執行流程

### Step 1 — 計算元素的新坐標與包圍盒 (Bounding Box)
1. 在更新 SVG 的節點坐標時，同步記錄所有子節點（`<rect>`, `<g>`, `<text>`, `<image>` 等）的外邊界值：
   - $X_{min}$, $Y_{min}$ (最左上角)
   - $X_{max}$, $Y_{max}$ (最右下角)
2. 對於包含 `stroke-width` 的路徑或線條，計算邊界時需將筆觸粗細納入 padding 考量（例如在最大/最小值外側增加 $5px - 10px$ 的緩衝）。

### Step 2 — 動態更新外層 viewBox 屬性
1. 定位最外層的 `<svg>` 標籤。
2. 根據計算出的邊界，重寫 `viewBox` 屬性：
   ```xml
   viewBox="[X_min] [Y_min] [Width] [Height]"
   ```
   其中：
   - $\text{Width} = X_{max} - X_{min}$
   - $\text{Height} = Y_{max} - Y_{min}$
3. 若有需要，同步修改 `<svg>` 的 `width` 與 `height` 屬性，使其與新的 `viewBox` 寬高比一致。

### Step 3 — 畫布外邊界裁切檢查 (Clipping Check)
1. 收緊 `viewBox` 後，必須確認沒有任何文字、箭頭或子圖的邊緣被切掉。
2. 如果發現有邊緣裁切現象，微調 `X_min`, `Y_min` 向外擴展 $2\% - 5\%$，並相應增加 `Width` 與 `Height`，為圖表預留安全邊界（Safety Margin）。

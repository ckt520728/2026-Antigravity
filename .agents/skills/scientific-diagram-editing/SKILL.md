---
name: scientific-diagram-editing
description: "編輯與修訂學術插圖與圖表（Scientific Diagram & Figure Editing）。適用於 SVG 向量修改、標籤重命名、佈局重排、上下標數學公式對齊、viewBox 邊界調整、多模態視覺比對審查等圖表編修任務。觸發詞：編修科學圖表、修改論文圖表、edit scientific diagram、edit figure、reflow SVG panels、scientific diagram revision。"
---

# Scientific Diagram Editing Skill

本技能提供學術插圖與圖表（特別是向量 SVG 與嵌入式圖表）的自動化編修與美學品質控制指南。

## 核心操作原則

### 1. 向量語意保留 (Vector Semantics Preservation)
- 圖表編修應在 **向量（SVG）** 層面精確操作其 primitives，切忌直接在柵格（raster）層面進行盲目重繪，確保所有未受影響的區塊（如文字、線條、其他子圖）保持 100% 原始樣式。

### 2. 佈局緊湊與畫布收緊 (viewBox Tightening after Reflow)
- 當進行子圖重新排版（例如從 1x4 橫排改為 2x2 網格）或刪除某些元素時，必須重新計算所有節點的聯集邊界（bounding box），並收緊最外層 SVG 的 `viewBox`，以消除多餘的空白邊帶。
- 詳細工作流請參考：[workflows/viewbox-reflow-tightening.md](file:///C:/Users/User/.gemini/config/skills/scientific-diagram-editing/workflows/viewbox-reflow-tightening.md)。

### 3. 安全文字替換與標籤局部定位 (Anchored String Replace)
- 避免使用盲目的全域 `.replace(A, B)`，這會導致兩項問題：一是雙向交換（A ↔ B）時被複寫；二是對稱面板中同名標籤被錯誤替換。
- **規則**：進行雙向交換時必須先導入預留的雜湊（placeholder）Pass；且每次替換必須錨定其 `x="..."`, `y="..."` 等幾何座標或鄰近脈絡節點，將替換範圍限制在目標面板（panel-scoped）。
- 詳細工作流請參考：[workflows/safe-string-replace.md](file:///C:/Users/User/.gemini/config/skills/scientific-diagram-editing/workflows/safe-string-replace.md)。

### 4. 數學公式與上下標精密排版 (Math-Notation Typesetting)
- 在 SVG 中，直接以 `<tspan>` 排版上下標時容易造成上下標「前後錯開」而非「重疊對齊」。
- **規則**：使用 `<tspan dx="-N em">` 屬性將下標向左回推，使其精確疊在下標下方；且全面禁止使用 Unicode 上下標特殊字元，確保字型渲染統一。
- 詳細工作流請參考：[workflows/math-notation.md](file:///C:/Users/User/.gemini/config/skills/scientific-diagram-editing/workflows/math-notation.md)。

### 5. 雙軌渲染驗證機制 (Layered Verification Loop)
- **第一軌（Holistic Review）**：編輯完成後，切勿僅透過文本判斷，必須渲染成 `output.png`，並藉由視覺評判模型對比原始圖與目標指令，輸出包含 `ship` 或 `revise` 的 JSON 判定。
- **第二軌（Structural Audit）**：若指令中包含 `delete`, `remove`, `swap`, `replace`, `move`, `restructure` 等結構變更，必須額外調用結構審計（[workflows/post-restructure-compactness.md](file:///C:/Users/User/.gemini/config/skills/scientific-diagram-editing/workflows/post-restructure-compactness.md)）檢查四項常見錯誤：
  1. 重複元素（移位時舊元素未被徹底移除）。
  2. 元素移除後的空白洞。
  3. 新置換元素縮水。
  4. 新置換元素顏色/筆觸與周圍不一致。

# Workflow: Math-Notation Typesetting (數學公式與上下標排版)

學術圖表常包含複雜的數學符號（如 $\theta_0$, $y_t^i$ 等）。在 SVG 中直接排版這些符號時，由於缺少像 LaTeX 般完善的排版引擎，容易發生字元重疊或上下標錯位。

## 核心準則

### 1. 禁止使用 Unicode 上下標字元
- **嚴禁** 使用如 `⁰`, `¹`, `₂` 等 Unicode 特殊字型字元來排版。這些字元在不同的作業系統或 PDF 渲染引擎中，經常會因為缺少對應 Font Glyph 而顯示為方塊（Missing Glyphs）或比例失調。
- **解決方案**：一律使用標準文字搭配 `<tspan>` 標籤並調整 `baseline-shift`。

### 2. 解決上下標的左右「前後錯開」問題
在預設情況下，如果在同一個字元後方同時寫入上標與下標的 `tspan`：
```xml
<!-- 錯誤：這會導致下標排在上標的右側，而非重疊排在其正下方 -->
<text>
  y
  <tspan baseline-shift="super" font-size="70%">t</tspan>
  <tspan baseline-shift="sub" font-size="70%">i</tspan>
</text>
```

### 正確做法
- 使用 `dx` 屬性（以 `em` 或 `px` 為單位）對後寫入的 `tspan` 進行負向回推位移，使其橫向座標與前一個標籤重合，實現上下對齊：
```xml
<text>
  y
  <tspan baseline-shift="super" font-size="70%">t</tspan>
  <tspan baseline-shift="sub" font-size="70%" dx="-0.5em">i</tspan>
</text>
```
*註：負向回推值（如 `-0.5em`）應根據上標字元的長度與字型大小動態調整，通常單個字元回推約 `-0.4em` 至 `-0.6em`*。

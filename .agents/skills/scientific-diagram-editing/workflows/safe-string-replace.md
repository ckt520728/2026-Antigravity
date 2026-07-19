# Workflow: Safe String Replace (安全文字替換)

在 SVG 中替換文字或標籤時，隨意的替換極易造成數據損壞或錯誤覆寫。請嚴格執行以下替換模式：

## 模式 A：對稱標籤的局域替換 (Panel-Scoped Replacement)
若圖表中有兩個對稱面板（例如 Panel A 和 Panel B），且兩者都包含同名標籤（如 "Accuracy"），但指令僅要求修改 Panel A 的標籤：

### 錯誤示範
```python
svg_content = svg_content.replace("Accuracy", "Mean Accuracy")
# 錯誤：這會將 Panel A 和 Panel B 的 Accuracy 全部替換
```

### 正確做法
1. 定位該 Text/Tspan 標籤獨有的鄰近屬性（如特定的 `x` 或 `y` 座標，或者 Panel A 特有的父級 `g` 組群 ID）。
2. 在替換時，將包含這些座標與標籤的完整節點字串作為 search target：
```python
target_text = '<text x="120" y="340">Accuracy</text>'
replacement_text = '<text x="120" y="340">Mean Accuracy</text>'
svg_content = svg_content.replace(target_text, replacement_text)
```

---

## 模式 B：雙向標籤交換 (Two-Way Label Swap)
當指令要求將標籤 A 和標籤 B 的位置進行對調（A ↔ B）時：

### 錯誤示範
```python
svg_content = svg_content.replace("Label A", "Label B")
svg_content = svg_content.replace("Label B", "Label A")
# 錯誤：第一步完成後，圖中全部都是 Label B，第二步會把原本 A 的位置也換回 A，導致無任何變化
```

### 正確做法
1. 使用臨時雜湊佔位符（Temporary Hash Placeholders）進行三階段替換：
```python
svg_content = svg_content.replace("Label A", "@@TEMP_B@@")
svg_content = svg_content.replace("Label B", "Label A")
svg_content = svg_content.replace("@@TEMP_B@@", "Label B")
```
2. 替換完成後，必須進行檢索，確認沒有殘留 `@@TEMP_...@@` 字串。

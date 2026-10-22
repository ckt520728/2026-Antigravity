# 健保雲端資料庫雙軌資訊處理架構、自訂技能 (Skill) 封裝暨排坑總結實錄 (Wrap-up & Pitfalls)

> **建立日期**：2026-10-22  
> **研究主持人**：朱國大醫師 (Kwo-Ta Chu, MD, PhD)  
> **院所站點**：陽明醫院 診間工作站 (`YangminRoom1`)  
> **資料來源**：衛生福利部中央健康保險署「健保醫療資訊雲端查詢系統 (NHI MediCloud)」  
> **GitHub 倉庫**：[`https://github.com/ckt520728/2026-Antigravity`](https://github.com/ckt520728/2026-Antigravity)  
> **儲存位置**：`G:\我的雲端硬碟\Second Brain\知識庫\2026-Antigravity\2026-10-22_MediCloud_Records_Dual_Format_Skill_WrapUp_and_Pitfalls.md`  
> **自訂技能**：`medicloud-records-processor` (`.agents/skills/medicloud-records-processor/SKILL.md`)  

---

## 一、 任務緣起與核心痛點 (Executive Summary)

健保醫療資訊雲端查詢系統 (NHI MediCloud) 是台灣臨床醫師獲取跨院病史、檢驗報告與用藥紀錄的最關鍵管道。然而，在日常臨床診療中，醫師從雲端系統所截取或複製之原始資料（Raw Data）往往存在以下顯著痛點：

1. **資訊形態極度異質混雜**：
   - 一類屬於門診**客觀檢驗與診斷報告**（成人預防保健、血液生化、尿液、放射影像 CT/MRI/Sono、內視鏡、病理組織切片）。
   - 另一類則屬於急重症**跨院出院病歷摘要**（加護病房治療經過、重大手術、氣切造口、血液淨化、大面積中風、出院帶藥與跨專科照護計畫）。
2. **格式破碎與版面紊亂**：
   - 原始文字通常為純文字、Tab 分隔或未對齊的純表格文字，缺乏視覺層次；
   - 範本中常殘留「擷取操作提示」與空白預留區，缺乏專業出版水準。
3. **缺乏雙語標準化**：
   - 當需要轉診外院、國際醫療保險申報或學術病歷討論時，亟需將混雜民國年份（如 113年、115年）與在地藥品商名的中文資料，轉換為符合國際醫學中心標準的正式英文出院摘要。

為徹底解決上述問題，本次任務成功確立了**健保雲端「雙軌資訊處理架構（Dual-Track Architecture）」**，研製出 **Format A** 與 **Format B** 兩套高階 Word 範本，完成兩位代表性病患（林淑美、曾詠聖）的中英文正式報告重構，並將全套作業流程封裝為可永久重複調用的系統級技能：`medicloud-records-processor`。

---

## 二、 雙軌資訊處理架構與範本標準 (The Dual-Track Architecture)

```
                            ┌────────────────────────────────────────────────────────┐
                            │     健保醫療資訊雲端查詢系統 (NHI MediCloud Raw Data)  │
                            └───────────────────────────┬────────────────────────────┘
                                                        │
                           ┌────────────────────────────┴────────────────────────────┐
                           ▼                                                         ▼
       【Format A：檢驗檢查與診斷報告類】                        【Format B：跨院出院病歷摘要類】
      (Diagnostic & Laboratory Reports)                         (Hospital Discharge Summaries)
       ├── 成人預防保健 / 健檢數據追蹤                            ├── 醫學中心/區域醫院住院病歷摘要
       ├── 門診血液、生化、尿液檢驗歷程                          ├── 急重症加護病房 (ICU) 重大病程演變
       ├── 放射影像 (X-ray, CT, MRI, 超音波)                     ├── 關鍵介入手術 (PTMC, 支架, 氣切, 透析)
       ├── 內視鏡與組織病理切片報告                              ├── 檢驗與多重微生物培養動態對照
       ├── 門診西藥處方與慢箋領藥紀錄                            ├── 7 欄位結構化出院帶藥專區
       └── 藥物過敏與不良反應紀錄                                └── 出院指示與跨專科追蹤照護計畫
                           │                                                         │
                           ▼                                                         ▼
       專屬範本：MediCloud-檢驗檢查與診斷報告範本.docx          專屬範本：MediCloud-跨院出院病歷摘要範本.docx
       代表案例：林淑美 (高血脂 / CKD 門診追蹤)                 代表案例：曾詠聖 (義大醫院 58 天多器官衰竭出院)
```

### 1. Format A：檢驗檢查與診斷報告類 (Diagnostic & Lab Reports)
* **核心章節**：
  1. 病人基本資訊表 (Header Table)
  2. 一、重點摘要 (Clinical Executive Summary)：以高密度 Callout 框綜整過敏、用藥、檢驗異常、影像結論與臨床建議。
  3. 二、結構化檢驗歷程追蹤比較表：標準 6 欄位（類別、項目、最近值、前次值、參考值、趨勢判讀），異常值標註深紅粗體 (`#B40000`) 與淡紅底色 (`#FFF0F0`)。
  4. 三、西醫用藥紀錄（慢箋與交互作用檢查）
  5. 四、放射影像學報告（Findings & Impression）
  6. 五、病理組織學與內視鏡報告
  7. 六、過敏藥物與住院紀錄宣告

### 2. Format B：跨院出院病歷摘要類 (Hospital Discharge Summaries)
* **核心章節**：
  1. 住院與病人資訊表 (含住出院日期、住院天數、科別、床號、主治醫師)
  2. 一、重大住院核心綱要 (Executive Hospital Summary)：器官衰竭復原、手術介入、出院帶藥方向、照護重點。
  3. 二、臨床診斷與入院病史：完整出院診斷 (ICD-10)、重大傷病發卡狀態、主訴與現病史 (CC & HPI)。
  4. 三、住院治療經過時間軸 (Chronological Timeline)：嚴格按時間與場域重構（如 MICU 階段 1 → MICU 階段 2 → RCC 呼吸照護中心 → MICU 重症救援 → 普通病房復健與出院）。
  5. 四、檢驗數據與微生物培養追蹤：出院前動態檢驗對照表、血液/痰液/尿液培養菌種與抗生素反應。
  6. 五、影像與特殊檢查總結表 (Brain CT/CTA/CTP, TEE, PTMC, CT, Colonoscopy, CXR)。
  7. 六、出院帶藥明細表 (7 欄位：項次、藥品名規格、單次劑量、用法頻率、途徑、總量、適應症與機轉)。
  8. 七、出院指示與跨專科追蹤照護計畫。

---

## 三、 本次代表性案例成果

| 病患姓名 | 檔案類別 | 中文版 Word 檔案 | 英文版 Word 檔案 | 核心臨床特色 |
| :--- | :--- | :--- | :--- | :--- |
| **林淑美**<br>(病歷: 9304799) | **Format A**<br>(檢驗報告) | [`MediCloud_20261022_林淑美.docx`](file:///C:/Users/YangminRoom1/Documents/Dr%20Chu's%20file/Word%20Documents/MediCloud_20261022_林淑美.docx) | [`MediCloud_20261022_林淑美_English.docx`](file:///C:/Users/YangminRoom1/Documents/Dr%20Chu's%20file/Word%20Documents/MediCloud_20261022_林淑美_English.docx) | 成人健檢歷程對照、高膽固醇與高 LDL-C (168 mg/dL) 動脈硬化風險評估、CKD Stage 2 追蹤。 |
| **曾詠聖**<br>(病歷: 1399357) | **Format B**<br>(出院摘要) | [`曾詠聖_義大醫院_20261022.docx`](file:///C:/Users/YangminRoom1/Documents/Dr%20Chu's%20file/Word%20Documents/曾詠聖_義大醫院_20261022.docx) | [`曾詠聖_義大醫院_20261022_English.docx`](file:///C:/Users/YangminRoom1/Documents/Dr%20Chu's%20file/Word%20Documents/曾詠聖_義大醫院_20261022_English.docx) | 義大醫院 58 天住院；橫紋肌溶解無尿 AKI III 經透析後**奇蹟完全恢復停止洗腎** (Cr 0.97)；成功施行 PTMC 解除重度二尖瓣狹窄；氣切成功脫離呼吸器；大面積腦中風二級預防。 |

---

## 四、 開發踩坑實錄與防錯機制 (Pitfalls & Lessons Learned)

在處理 Windows 工作站、Office Word (DOCX) 底層 OpenXML、PowerShell 指令行及多語系轉換過程中，遭遇並克服了以下六大核心坑點：

### 坑點 1：Windows PowerShell 單引號字元跳脫崩潰 (`Dr Chu's file`)
* **現象**：在命令列中執行 `Get-ChildItem -Path 'C:\Users\...\Dr Chu\'s file\...'` 時，PowerShell 將 `Chu's` 的 `'` 誤判為字串結束符號，導致拋出 `ParserError: TerminatorExpectedAtEndOfString` 語法中斷。
* **排坑方案**：
  - 在 PowerShell 中，單引號字串內的撇號必須使用雙單引號（`''`）轉義：`'Dr Chu''s file'`。
  - **最佳解法**：全面透過 Python 腳本或傳遞純雙引號路徑處理，避免讓 Shell 解析複雜檔名中的特殊標點。

### 坑點 2：Windows 終端機預設編碼 (CP950 / Big5) 引發溢位錯誤
* **現象**：在 Windows 繁體中文環境下，終端預設編碼為 `CP950`。當 Python 輸出或處理包含超出 Big5 字元集（如醫學特殊符號、罕見字如 `\u854b`）之路徑或檔案時，直接崩潰報錯：`UnicodeEncodeError: 'cp950' codec can't encode character...`。
* **排坑方案**：
  - 在所有 Python 自動化處理腳本頂部強制宣告標準輸出重新編碼：
    ```python
    import sys
    sys.stdout.reconfigure(encoding='utf-8')
    ```
  - 檔案讀寫均明確指定 `encoding='utf-8', errors='ignore'`。

### 坑點 3：DOCX 底層 OpenXML `<w:sectPr>` 節屬性被誤刪導致排版崩潰
* **現象**：為了清除原始範本中殘留的操作指示與未格式化段落，程式遍歷 `doc._body._body` 並刪除元素。執行後呼叫 `doc.add_table()` 竟拋出致命錯誤：`IndexError: list index out of range`（來自 `self._document_elm.sectPr_lst[key]`）。
* **根因分析**：Word 文件在最後一個段落或 Body 末尾包含 `<w:sectPr>` 標籤，用以定義整篇文件的邊界寬度、直橫向、紙張大小、頁首頁尾。盲目刪除 Body 末端元素導致 `doc.sections` 集合被清空，破壞了文件結構。
* **排坑方案**：
  - 封裝安全清除函式 `clean_body_preserving_sectpr()`，在遍歷刪除時嚴格檢查標籤名稱，絕對保留 `sectPr`：
    ```python
    def clean_body_preserving_sectpr(doc, tbl0):
        body = doc._body._body
        tbl_elem = tbl0._tbl
        found_tbl = False
        elements_to_remove = []
        for elem in list(body):
            if elem == tbl_elem:
                found_tbl = True
                continue
            if found_tbl:
                if elem.tag.endswith('sectPr'):  # 關鍵：保留節屬性
                    continue
                elements_to_remove.append(elem)
        for elem in elements_to_remove:
            body.remove(elem)
    ```

### 坑點 4：資訊顆粒度混淆與臨床重點稀釋
* **現象**：原始抓取檔案中，健保雲端常將零散的門診成人健檢與數十頁的 ICU 出院摘要混在一起。若使用單一範本套用，將導致檢驗數據被文字淹沒，或出院重大處置（如 PTMC、氣切、CVVH）散落在無關段落中。
* **排坑方案**：
  - 確立 **Format A 與 Format B 嚴格分離**原則；
  - 在腳本中加入 `detect_file_category()` 智慧辨識機制：
    * 偵測到「出院病歷摘要、住院日期、出院診斷、Hospital course」關鍵字時自動走 Format B；
    * 偵測到「成人健檢、檢驗項目、總膽固醇、eGFR」時自動走 Format A。

### 坑點 5：醫學名詞與民國紀年之雙語轉譯校準
* **現象**：直接機器翻譯常出現「中華民國113年」被直譯或誤算為「113 AD」，或將重要術語如「經皮穿中隔二尖瓣氣球成型術」翻成不精準的口語英文。
* **排坑方案**：
  - 建立對照表：民國年份自動轉換為西元（ROC Year + 1911）；
  - 醫學術語嚴格對標國際規範（如 `Percutaneous Transvenous Mitral Commissurotomy (PTMC)`、`Continuous Veno-Venous Hemofiltration (CVVH)`、`Catastrophic Illness Certificate`）；
  - 藥品統一採用國際非專利名 (Generic Name) 並保留原廠商品名（如 `Clopidogrel (Plavix)`、`Levothyroxine (Eltroxin)`）。

### 坑點 6：Word 表格單元格內邊距 (Cell Padding) 缺失
* **現象**：Python-docx 原生建立的表格預設沒有內部 Padding，文字會緊貼灰色格線，導致視覺效果擁擠且缺乏醫學中心報告的高級感。
* **排坑方案**：
  - 透過底層 XML 注入 `w:tcMar`，為每個 Cell 設定精確邊界：
    ```python
    def set_cell_margins(cell, top=100, bottom=100, left=140, right=140):
        tcPr = cell._tc.get_or_add_tcPr()
        tcMar = parse_xml(f'''
        <w:tcMar {nsdecls("w")}>
            <w:top w:w="{top}" w:type="dxa"/>
            <w:bottom w:w="{bottom}" w:type="dxa"/>
            <w:left w:w="{left}" w:type="dxa"/>
            <w:right w:w="{right}" w:type="dxa"/>
        </w:tcMar>
        ''')
        tcPr.append(tcMar)
    ```

---

## 五、 自訂技能結構與使用指南 (Skill Integration)

技能已安裝於本機 `.agents/skills/medicloud-records-processor/` 並同步推播至 GitHub 倉庫：

```
.agents/skills/medicloud-records-processor/
├── SKILL.md                               # 技能完整規範與指引
├── scripts/
│   └── process_medicloud.py               # 自動化分類與排版核心腳本
└── templates/
    ├── MediCloud-檢驗檢查與診斷報告範本.docx  # Format A 官方範本
    └── MediCloud-跨院出院病歷摘要範本.docx    # Format B 官方範本
```

### 常用呼叫指令：
```bash
# 1. 自動辨識並產生雙語 Word 文件
python .agents/skills/medicloud-records-processor/scripts/process_medicloud.py -i "<檔案路徑>" -c auto -l both

# 2. 指定以 Format A 產出中文報告
python .agents/skills/medicloud-records-processor/scripts/process_medicloud.py -i "<檔案路徑>" -c lab -l zh

# 3. 指定以 Format B 產出正式英文出院病歷
python .agents/skills/medicloud-records-processor/scripts/process_medicloud.py -i "<檔案路徑>" -c discharge -l en
```

---

## 六、 結論與未來展望

透過本次雙軌化重構與 Skill 封裝，朱院長未來在門診或遠距會診時，僅需將健保雲端抓取之原始文字交由 Agent 處理，系統即可自動識別臨床類型，套用深藍醫療美學範本，精準呈現檢驗歷程趨勢或重症急救時間軸，並一鍵產出中英雙語 Word 報告，大幅提升臨床病歷紀錄之品質、效率與可維護性。

from pathlib import Path
p=Path(__file__).resolve().parents[2]/'deliverables/mounjaro_paper_explainer.md'
s=p.read_text(encoding='utf-8').replace('資料整理：2026-10-31。','證據截止：2026-10-29。資料整理：2026-10-31。')
s=s.replace('下表將四種常被混用的脈絡放回各自研究問題。','下表將四種常被混用的脈絡放回各自研究問題。T2D 指第二型糖尿病（type 2 diabetes），HFpEF 指保留射出分率心衰竭（heart failure with preserved ejection fraction），CKD 指慢性腎臟病（chronic kidney disease）。')
s=s.replace('Kansas City Cardiomyopathy Questionnaire（KCCQ）','堪薩斯市心肌病變問卷（Kansas City Cardiomyopathy Questionnaire, KCCQ）')
s=s.replace('eGFR 50–75 且 UACR >300 至 <5,000，或 eGFR 25 至 <50 且 UACR >100 至 <5,000','eGFR 50–75 mL/min/1.73 m² 且 UACR >300 至 <5,000 mg/g，或 eGFR 25 至 <50 mL/min/1.73 m² 且 UACR >100 至 <5,000 mg/g')
s=s.replace('## 安全溝通 讓證據能轉成正確的下一步','## 維持治療與劑量 先保留當地標示條件\n\nSURMOUNT-4 是 randomized withdrawal 設計：783 人進入 lead-in，之後 670 人隨機分派（335/335）。先使用 tirzepatide 36 週，再隨機維持 52 週；第 36 至 88 週，持續 tirzepatide 組體重變化 −5.5%，改 placebo 組 +14.0%。這是沒有糖尿病、可進入隨機期的選擇人群；不能說所有人停藥都回升 14%。本教材採 abstract 層級核對，完整 SAP 尚未審核；結果支持預先討論維持與追蹤，也不能阻礙遇到急性警訊時的停藥評估。[C019；S13 Abstract/Results]\n\n美國 Mounjaro 成人標示以 2.5 mg 每週一次起始；需要進一步調整時，每次增 2.5 mg，當前劑量至少維持 4 週，成人最大每週 15 mg。這些條件屬美國成人仿單，並非台灣個別處方，也不表示人人都須達到最大劑量。台灣器型與完整仿單尚未核實前，不另製本地病人滴定或操作圖。[C011；S07 §2.1；P001]\n\n## 安全溝通 讓證據能轉成正確的下一步')
s=s.replace('Claim IDs C001–C021','S13 SURMOUNT-4。Abstract/Results；randomized withdrawal、lead-in 選擇人群。https://pmc.ncbi.nlm.nih.gov/articles/PMC10714284/\n\nClaim IDs C001–C021')
p.write_text(s,encoding='utf-8')

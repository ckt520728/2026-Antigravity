"""重建本次來源登錄與 claim ledger；只在 monjaro/evidence 寫入。"""
from pathlib import Path
import csv, json

BASE = Path(__file__).resolve().parent
SOURCES = [
 ('S01','SURPASS-2','2021-06-25','10.1056/NEJMoa2107519','https://pubmed.ncbi.nlm.nih.gov/34170647/','RCT 原始報告','國際試驗','PubMed abstract；NotebookLM 原文 pp.503–515','verified',''),
 ('S02','SURMOUNT-5','2025-05-11','10.1056/NEJMoa2416394','https://pubmed.ncbi.nlm.nih.gov/40353578/','RCT 原始報告','美國及波多黎各試驗','PubMed abstract；NotebookLM 原文 pp.26–36','verified',''),
 ('S03','SUMMIT','2024-11-16','10.1056/NEJMoa2410027','https://pubmed.ncbi.nlm.nih.gov/39555826/','RCT 原始報告','國際試驗','PubMed abstract；NotebookLM 原文 pp.427–437；期刊卷期2025','verified',''),
 ('S04','STEP-HFpEF DM','2024-04-06','10.1056/NEJMoa2313917','https://pubmed.ncbi.nlm.nih.gov/38587233/','RCT 原始報告','國際試驗','PubMed abstract；NotebookLM 原文 pp.1394–1407','verified',''),
 ('S05','FLOW','2024-05-24','10.1056/NEJMoa2403347','https://pubmed.ncbi.nlm.nih.gov/38785209/','RCT 原始報告','國際試驗','PubMed abstract；NEJM 391:109–121；全文更新2025-08-14','verified',''),
 ('S06','SURPASS-CVOT','2025-12-18期刊日（PubMed 收錄2025-12-17）','10.1056/NEJMoa2505928','https://pubmed.ncbi.nlm.nih.gov/41406444/','RCT 原始報告','國際試驗','PubMed abstract；NEJM 393(24):2409–2420','verified',''),
 ('S07','Mounjaro 美國 USPI','2026-08','','https://pi.lilly.com/us/mounjaro-uspi.pdf','原廠正式仿單','USA','§1、2.1、4、5、7.2、8.1、8.3、8.6、12.1、17；PDF頁碼見ledger','verified','monjaro/sources/mounjaro_us_2026-10-29.pdf'),
 ('S08','Zepbound 美國 USPI','2026-08','','https://pi.lilly.com/us/zepbound-uspi.pdf','原廠正式仿單','USA','§1、2.1、2.2、5、7、8','verified','monjaro/sources/zepbound_us_2026-10-29.pdf'),
 ('S09','TFDA：我國減重及降血脂藥品供應穩定','2025-11-10','','https://www.fda.gov.tw/TC/newsContent.aspx?cid=4&id=t623895','主管機關公告','台灣','第一點 Tirzepatide 成分注射筆；非完整仿單','verified',''),
 ('S10','TFDA Mounjaro 初始評估報告','2023-04-20','','https://www.fda.gov.tw/tc/includes/GetFile.ashx?cid=44254&id=f638289376695123554&type=2','主管機關初始審查報告','台灣','p.1 顯示2023核准；0.5mL單劑型，不能代替最新KwikPen仿單','historical_only',''),
 ('S11','Mounjaro KwikPen 使用說明','未取得（2026-10-29嘗試）','','https://www.medicines.org.uk/emc/files/usermanual.15482.pdf','原廠核准使用說明候補','UK','webfetch 不支援 PDF；直接 GET HTTP 403；本次不作主要依據','pending',''),
 ('S12','SURPASS-CVOT 預定探索性腎臟分析','2026-07期刊日（epub 2026-05-11）','10.1016/S2213-8587(26)00032-X','https://pubmed.ncbi.nlm.nih.gov/42114520/','RCT 預定探索性分析','國際試驗','PubMed abstract Methods/Findings；Lancet Diabetes Endocrinol 2026;14(7):544-557；非FLOW相同定義','verified_abstract',''),
 ('S13','SURMOUNT-4','2023-12-11','10.1001/jama.2023.24945','https://pmc.ncbi.nlm.nih.gov/articles/PMC10714284/','隨機停藥試驗','國際試驗','Abstract/Results；週36至88，783進入lead-in、670隨機','verified_abstract',''),
 ('S14','台灣最新完整仿單候選入口','2026-04（醫院網頁標示）','','https://www.hosp.nycu.edu.tw/departments/dep-support/pharmacy/drog-use-search/10388-%E7%8C%9B%E5%81%A5%E6%A8%82%E7%AD%8610%E6%AF%AB%E5%85%8B-0-6%E6%AF%AB%E5%8D%87.html','公立醫院藥品入口','台灣','網頁擷取timeout；未取得附件核准版本，不作完整仿單依據','pending',''),
 ('S15','motion-explainer-images repository','2026-10-29快照','','https://github.com/ckt520728/claude-motion-explainer-images','製作規範','不適用','tree SHA b7c2cd89489d8af3c6f1d3bb891d1e340d435241；README、3個SKILL已讀','verified','monjaro/sources/house_style/claude-motion-explainer-images'),
 ('S16','kidney-cognition-lab house style','2026-10-29快照','','https://github.com/ckt520728/kidney-cognition-lab','網站樣式來源','不適用','tree SHA 0d0f5c5a47d7cf9098e31110611555887ad5bdd0；index及vbm-ei-alzheimers.html已讀','verified','monjaro/sources/house_style/kidney-cognition-lab'),
]
keys=['source_id','title','publication_or_version','doi','url','evidence_type','jurisdiction','locator','status','local_path']
sources=[dict(zip(keys,r),retrieved_at='2026-10-29 Asia/Taipei') for r in SOURCES]
manifest=json.loads((BASE.parent/'sources/zip_manifest.json').read_text('utf8'))
for i,e in enumerate(x for x in manifest['entries'] if x['extracted_sha256']):
 sources.append(dict(zip(keys,[f'Z{i+1:02}',e['name'],'ZIP匯出2026-10-29','','','使用者提供AI研讀素材','未定',e['name'],'read_not_primary','monjaro/sources/studio_zip/'+e['name']]),retrieved_at='2026-10-29 Asia/Taipei',sha256=e['extracted_sha256']))
for sid,title in [('15555df5-6709-4702-90f6-b68f67b14a3d','Frias_2021'),('22a845a1-e2d0-4934-836a-cec29f701436','Aronne_2025'),('dc7fd8ad-9fce-4a7d-b8b4-5968fc47277e','Packer_2025'),('88b5b082-cb5e-428f-a926-154b9ac49d21','Kosiborod_2024')]:
 sources.append(dict(zip(keys,['N-'+sid,title,'NotebookLM live source','','https://notebooklm.google.com/notebook/e9c8966b-c3e8-4968-bce1-e6c39aa402b1','使用者已索引原始論文','國際試驗','source_id='+sid+'；對應 S01–S04 原始全文交叉核實','via_notebooklm_primary_text_cross_checked','monjaro/sources/notebooklm_summary.md']),retrieved_at='2026-10-29 Asia/Taipei'))
(BASE/'source_registry.json').write_text(json.dumps({'scope':'教育規劃；不是系統性回顧；台灣完整仿單尚待核實','as_of':'2026-10-29','sources':sources},ensure_ascii=False,indent=2),'utf8')
with (BASE/'source_registry.csv').open('w',encoding='utf-8-sig',newline='') as f:
 w=csv.DictWriter(f,fieldnames=keys+['retrieved_at','sha256']);w.writeheader();w.writerows(sources)

# claim_id、論點、來源、位置、N、效果/時間、證據、人群、適用性、查核狀態、限制。
ROWS=[
 ('C001','Tirzepatide 是單一分子的 GIP/GLP-1 雙受體促效劑；semaglutide 是 GLP-1 受體促效劑','S07;S02','§12.1；S02 Introduction p.27','不適用','機制；不推導療效為兩倍','藥理/原始報告','藥物機制','機制示意；不能證明所有器官均受益','verified','不採用萬能鑰匙或保證抗炎的比喻'),
 ('C002','美國 Mounjaro 與 Zepbound 品牌適應症須分列','S07;S08','USPI §1；均PDF p.1','不適用','Mounjaro：≥10歲T2D控糖、成人高MACE風險T2D風險降低；Zepbound：成人體重控制及肥胖伴中重度OSA','USA 正式仿單','依各品牌標示人群','僅美國，不能套台灣；08/2026版本','verified_US_only','Mounjaro非僅成人控糖；美國標示亦非台灣HFpEF適應症'),
 ('C003','台灣TFDA已確認猛健樂注射筆有血糖控制及肥胖過重體重控制用途','S09','第一點 Tirzepatide成分注射筆','不適用','公告2025-11-10','TFDA 公告','台灣核准用途概述','可說概括用途；詳細年齡/BMI/OSA須查現行仿單','verified_scope_only','公告不是完整仿單；勿由USA推導台灣MACE/兒科'),
 ('C004','SURPASS-2比較的是semaglutide 1 mg','S01','Methods/Results abstract；正文pp.503–505','1879隨機；1878至少一劑','40週；tirzepatide 5/10/15mg；HbA1c -2.01/-2.24/-2.30百分點，sema1mg -1.86百分點','open-label phase3 RCT','metformin治療仍控制不足T2D成人','控糖比較不能替代sema2.4mg減重比較','verified','HbA1c為百分點，不是相對百分比；不推定所有sema劑量'),
 ('C005','SURMOUNT-5主要結果限無T2D肥胖/過重成人','S02','Abstract；Table2/Fig1 pp.30–31；Methods p.28','751隨機；750用藥分析（374/376）','72週；tirzepatide最大耐受10/15mg：-20.2%（95%CI -21.4至-19.1）；sema1.7/2.4mg：-13.7%（-14.9至-12.6）；P<.001','open-label phase3b RCT','無T2D；BMI≥30或≥27伴相關共病','群體平均，不能保證T2D/HFpEF個案同幅減重','verified','modified treatment-regimen estimand；廠商Lilly資助；非心腎outcome比較'),
 ('C006','SUMMIT降低CV death或HF惡化複合終點，不能說已證實單獨降低CV死亡','S03','Abstract；正文p.427及Table2','731（364/367）','中位104週；36/364(9.9%) vs56/367(15.3%)；HR0.62,95%CI0.41–0.95；CV death8 vs5，HR1.58,CI0.52–4.83','double-blind RCT；tirzepatide≤15mg vs placebo','BMI≥30、HF、LVEF≥50%；包含有/無T2D','肥胖HFpEF；無法與STEP跨試驗排名','verified','不同終點不可當住院率；CV死亡CI寬；52週KCCQ是另一共同主要終點'),
 ('C007','STEP-HFpEF DM證據重點是症狀/功能與體重','S04','Abstract；Methods p.1395；Table2','616隨機','52週；sema2.4mg vs placebo；KCCQ差7.3分(95%CI4.1–10.4)；體重-9.8% vs-3.4%，差-6.4百分點','RCT','T2D、BMI≥30、LVEF≥45%、有症狀HF','不能以此單一試驗宣稱降低CV死亡或與SUMMIT優劣','verified','primary treatment-policy estimand；Novo Nordisk資助'),
 ('C008','FLOW為semaglutide而非tirzepatide的腎臟outcome試驗','S05','Abstract Methods/Results；NEJM pp.109–121','3533（1767/1766）','中位3.4年；sema1mg vs placebo；主要複合331 vs410事件；HR0.76,95%CI0.66–0.88,P=.0003','double-blind RCT；中期分析建議早停','T2D+CKD：eGFR50–75/UACR>300至<5000，或eGFR25至<50/UACR>100至<5000','腎主要複合含CV death；不能轉成tirzepatide class effect','verified','不能稱所有CKD或透析患者的證據；Novo Nordisk資助'),
 ('C009','SURPASS-CVOT已正式發表；MACE非劣性成立，優越性未達顯著','S06','Abstract Methods/Results；NEJM393:2409–2420','13299隨機；排除134；mITT13165（6586/6579）','tirzepatide≤15mg vs dulaglutide1.5mg weekly；MACE801(12.2%) vs862(13.1%)；HR0.92,95.3%CI0.83–1.01；NI P=.003，superiority P=.09','double-blind active-controlled RCT','T2D+已確立ASCVD','不能說勝過dulaglutide或勝過semaglutide；非placebo比較','verified','非劣界值1.05；95.3%不可改95%；Lilly資助'),
 ('C010','2026 SURPASS-CVOT腎臟分析已出刊，但屬探索性','S12','PubMed abstract Methods/Findings','13299隨機、mITT13165；腎指標可用N各有不同','中位4.0年；腎複合396(6.0%) vs498(7.6%)；HR0.77,95%CI0.68–0.88；p=.0002','預定探索性RCT分析','T2D+ASCVD；腎複合含新發持續macroalbuminuria','不能與FLOW的複合終點等同，也不是新獨立RCT','verified_abstract','未完成全文/SAP multiplicity審核；主簡報僅標探索性更新，不升格confirmatory'),
 ('C011','美國成人劑量由2.5mg起、按耐受與目標逐步調整','S07','§2.1 PDF p.3','不適用','2.5mg weekly；需要時每次增2.5mg，當前劑量至少4週；成人最大15mg weekly','USA 仿單','美國成人T2D','台灣完整仿單核實前不作個別處方或臺灣劑量圖','verified_US_only','不採原ZIP 5→10mg跳級或同週拼筆；不是人人需達15mg'),
 ('C012','MTC個人/家族史、MEN2與嚴重過敏是美國標示禁忌','S07','§4/5.1 PDF p.4','不適用','人類MTC風險尚未確立；rodent訊號','USA 仿單','依美國標示','衛教需先核對台灣仿單；勿把rodent致癌寫成人類已證實','verified_US_only','禁忌與不建議使用不能混同'),
 ('C013','嚴重GI反應可致體液流失與AKI','S07','§5.5–5.6 PDF pp.4–5','不適用','持續嘔吐/腹瀉或攝水不足需評估體液與腎功能；嚴重gastroparesis不建議','USA 仿單/上市後警示','尤其已有腎病或易脫水者','一般安全溝通；台灣版本待核','verified_US_only','不能因為renal PK不需調量就聲稱腎臟完全安全'),
 ('C014','合併insulin或sulfonylurea等secretagogue增加低血糖風險','S07','§5.3 PDF p.4','不適用','可能需減少併藥，由醫療團隊調整','USA 仿單','合併治療者','不能說單藥零低血糖；病人勿自行減藥','verified_US_only','不提供通用減量百分比'),
 ('C015','口服荷爾蒙避孕藥可能因胃排空延遲降低效力','S07','§7.2/8.3 PDF pp.10–11','不適用','開始及每次升量後4週：改非口服方法或加屏障法','USA 仿單','使用口服荷爾蒙避孕藥者','USA標示；不得外推全部避孕方式失效','verified_US_only','台灣正式文句及生育計畫停藥期未核完'),
 ('C016','麻醉/深鎮靜有吸入風險，沒有通用仿單停藥天數','S07','§5.9 PDF p.6','不適用','應預先告知手術/麻醉團隊；USPI稱資料不足判定暫停藥能否降低胃殘留風險','USA 仿單','預定麻醉/深鎮靜者','依當地程序與個別症狀風險；非一律停7天','verified_US_only','本輪未審核台灣麻醉指引；不得自行套2023固定停藥規則'),
 ('C017','疑胰臟炎或嚴重過敏應停藥並立即求醫','S07','§5.2/5.4 PDF p.4','不適用','持續嚴重腹痛、呼吸/顏面腫脹等需緊急評估','USA 仿單','用藥者','病人警訊語句需醫師審核；非自我診斷工具','verified_US_only','急性膽囊、視網膜病變亦須說明；不可擅用重啟建議'),
 ('C018','KwikPen為固定劑量；格數算術不等於核准可拆劑方法','S07','USPI §2.2/3 PDF pp.3–4；§5.10 PDF p.6','不適用','每支KwikPen含4個標示劑量；單一病人使用且不得共享','USA 正式仿單','USA對應KwikPen','反駁筆記教學；台灣操作需拿到同器型核准IFU','verified_US_only','不轉載格數換算、抽殘藥、延長一筆8週之教學；UK IFU本次未取得'),
 ('C019','停藥後體重可能回升，應預先規劃追蹤','S13','Abstract/Results，SURMOUNT-4','783進入lead-in；670隨機（335/335）','先用36週，再52週隨機維持；週36至88：持續tirzepatide -5.5%，改placebo +14.0%','randomized withdrawal RCT','無糖尿病肥胖/過重、可進入隨機期者','不等於所有人停藥必回升14%；不可當急性警訊停藥的阻礙','verified_abstract','耐受lead-in的選擇人群；本輪未完整SAP審核'),
 ('C020','原研讀素材的直接抗炎/心腎全面受益語句不可升格為臨床結論','S01;S02;S03;S04;S05','各trial主要終點；ZIP Notes03結論、Report §3','不適用','機制/biomarker/clinical outcome需分層','跨來源方法學判斷','依各藥物/適應人群','不得把不同GLP-1 RA或動物結果當tirzepatide人體證據','verified_boundary','本輪未逐篇核完發炎機制引用；預設不進主要教材'),
 ('C021','原筆記的自訂採購/拆筆與跳級方案不進正式衛教','Z03;Z05;Z06;S07','ZIP Notes02 §2/3；Notes04 Part1；Notes05結論；USPI §2.1/2.2/3','不適用','原筆記5→10mg跳過7.5mg；用半劑與同週拼筆；本次只記錄問題不推薦','AI素材與官方規格核對','未經個案確認的用藥內容','保留來源供稽核，不能把數學量相等當臨床劑量驗證','corrected_excluded','原圖/台灣IFU未齊；不聲稱全部圖片已複核'),
 ('P001','取得台灣目前各強度/器型完整仿單與核准版本','S14;S09','TFDA許可證/仿單附件；尚缺本次驗證','不適用','年齡、BMI、OSA、劑量、禁忌、交互作用、妊娠、麻醉警示、保存/漏打','法規核對待辦','台灣使用者','patient dose/IFU及適應症細節上線前必過gate','pending','不能用2023評估報告或美國2026 label填空'),
 ('P002','正式發布前完成原始補充資料與critical correspondence核讀','S02;S03;S06;S12','supplement/SAP/correspondence','不適用','涉及安全性優劣、心腎作用途徑、探索性multiplicity','文獻深度核對待辦','依trial','已核對abstract主要數字；不是所有clinical查核完成','pending','現規劃不宣稱GIP止吐因果或其他全面優勢'),
 ('P003','妊娠計畫停藥間隔與臺灣現行麻醉流程','S07;S14','§8.1/5.9及台灣指引待補','不適用','不提供統一停藥天數；由處方/麻醉團隊制定','當地臨床流程待核','妊娠或程序規劃者','未通過前只保留諮詢提醒','pending','不從半衰期自行計算臨床停藥方案'),
]
fields=['claim_id','claim','source_ids','locator','participant_N','effect_and_time','evidence_type','population','applicability','verification','limitations','source_urls','verified_at']
lookup={s['source_id']:s for s in sources}
with (BASE/'claim_ledger.csv').open('w',encoding='utf-8-sig',newline='') as f:
 w=csv.DictWriter(f,fieldnames=fields);w.writeheader()
 for row in ROWS:
  d=dict(zip(fields,row));d['source_urls']=' | '.join(lookup[s]['url'] or lookup[s]['local_path'] for s in d['source_ids'].split(';'));d['verified_at']='2026-10-29';w.writerow(d)
print(json.dumps({'sources':len(sources),'claims':len(ROWS)},ensure_ascii=False))

"""建立繁體中文 KwikPen 衛教影片；所有素材僅寫入本資料夾。"""
import asyncio, json, math, re, subprocess, html
from pathlib import Path
import edge_tts
P=Path(__file__).parent
S=[]
def scene(title,lines,voice,art='pen',source='TW IFU'):
    S.append(dict(title=title,lines=lines,voice=voice,art=art,source=source))
scene('先認筆，再開始六個月管理',['Mounjaro KwikPen 多劑量筆','每週一次・個別化調整','先接受醫療人員操作訓練'],'這支影片說明猛健樂多劑量注射筆，以及六個月體重管理。這是衛教示範，不能取代個別處方。請先接受醫療人員的操作訓練。','pen','TW IFU／台灣仿單')
scene('藥物是輔助，結果因人而異',['tirzepatide：GIP／GLP-1 雙受體促效劑','配合飲食與體能活動','72 週試驗 ≠ 六個月保證'],'替爾泊肽作用於兩類腸泌素受體，有助調節食慾與血糖。配合生活調整可以幫助減重，但不能保證個人結果，也不能把七十二週研究當成六個月成效。','mechanism','台灣仿單 §10／SURMOUNT-1')
scene('先由醫師確認適用性',['成人 BMI ≥30；或 ≥27 合併相關共病','禁用：個人／家族 MTC、MEN2','曾對本藥嚴重過敏：禁用'],'用於體重控制，須由醫師依肥胖程度與共病評估。個人或家族有甲狀腺髓質癌，第二型多發性內分泌腫瘤症，或曾對本藥嚴重過敏者禁用。','check','台灣仿單 §2、4')
scene('認識同一支筆的四個部位',['筆蓋與藥匣','標籤：藥名、每劑強度、效期','劑量視窗與旋鈕'],'確認是需要另裝針頭的多劑量筆。從前端的筆蓋、藥匣，到本體標籤、劑量視窗與旋鈕，逐一辨認。不要只靠外觀顏色判斷強度。','parts')
scene('一支筆，四個固定全劑量',['每劑 0.6 mL・每週一劑','5 mg 標示 = 每劑 5 mg','不是每支只有 5 mg，也不是 1.25 mg'],'每支筆提供四個固定劑量，每劑零點六毫升。標示五毫克的筆，每次完整劑量就是五毫克，不能再除以四。不同強度應使用處方指定的筆。','four','台灣仿單 §1／TW IFU p1')
scene('準備用品，先洗手',['肥皂與清水洗手','新針頭、酒精棉、紗布','抗針刺容器先放好'],'先以肥皂與清水洗手，準備正確的注射筆、相容的新針頭、酒精棉和紗布。抗針刺容器應放在伸手可及的位置；針頭通常不含在藥品包裝內。','supplies')
scene('檢查藥名、效期與藥液',['直拔筆蓋・核對處方與 EXP','澄清、無色至淡黃、無顆粒','混濁、變色、損壞或曾冷凍：不用'],'直直拔下筆蓋，核對藥名、劑量與效期。藥液應澄清，無色至淡黃色且沒有顆粒。若混濁、變色、筆身損壞或曾經冷凍，請勿使用。','inspect')
scene('每次注射，都用一支新針頭',['酒精擦拭前端紅色內膜','撕封口・直推針頭後旋緊','取下外罩保留；內罩丟棄'],'用酒精棉擦拭前端紅色內膜。撕開新針頭封口，直推到筆上再旋緊。取下外罩並保留，再拔掉內罩丟棄。每次注射都要換新針頭。','needle')
scene('每次排氣：先對準長線',['慢轉旋鈕，聽到 2 聲喀擦','長線對齊劑量指示器','這是排氣位置，還不是注射劑量'],'每次注射前都要排氣。慢慢旋轉旋鈕，聽到兩聲喀擦，讓視窗中的長線對準指示器。這只是排氣位置，不能把它當成身體注射的劑量。','prime')
scene('朝上輕敲，按住慢數五',['針尖朝上・輕敲藥匣','向空氣排氣，按到底再數 5','視窗回 0，針尖出現藥滴'],'讓針尖朝上，輕敲藥匣使氣泡聚集。向空氣中按下旋鈕到底，持續按住並慢數到五。確認視窗回到零，而且針尖有少量藥液流出。','drop')
scene('沒看到藥滴？有重試上限',['重複完整排氣步驟：最多再 2 次','仍無滴：換新針，最多再 1 次','仍無滴：停止，聯絡醫療人員'],'沒有藥滴時，完整排氣步驟最多再做兩次。仍沒有藥滴，就換新針頭，再排氣最多一次。仍無藥滴請停止，聯絡醫療人員，不要無限重試。','retry')
scene('輪替皮下注射位置',['腹部：距肚臍至少 5 cm','大腿；上臂後側由他人操作','清潔晾乾；輪替位置、避受損皮膚'],'可選腹部或大腿；腹部距離肚臍至少五公分。上臂後側要由他人注射。注射位置用酒精清潔並晾乾。每週輪替位置，避開瘀青、硬塊、疤痕及受損皮膚，也不要緊鄰胰島素注射點。','sites')
scene('旋到「1」：完整劑量',['旋鈕轉到停止，視窗顯示 1','1 = 一個完整的 0.6 mL 劑量','1 不是 1 mg；不數格拆劑'],'排氣完成後，旋轉旋鈕直到停止，視窗顯示一。一代表這支筆的一個完整劑量，並不是一毫克。請勿靠數格拆分劑量，也不要用不同的筆拼湊。','dose')
scene('刺入皮下，按住慢數五',['依訓練將針頭刺入皮膚','按到底並持續按住，慢數 5','確認視窗 0，再拔出針頭'],'依訓練將針頭刺入皮下，按下旋鈕直到停止。持續按住，慢慢數到五，並在拔針前確認視窗顯示零，才算完成這一次注射。','inject')
scene('未見「0」，不要重新轉劑量',['插回皮膚，完成原本注射','不可重轉、不可再打一個全劑量','仍不確定：聯絡醫療人員'],'若拔針後發現視窗沒有回零，請將針頭插回皮膚，完成原本注射，不要重新旋轉劑量。若仍懷疑沒打足，不可再打一劑，應詢問醫療人員。','zero')
scene('卸針、棄針，再蓋筆蓋',['小心套回保留的針頭外罩','旋下針頭，立即入抗針刺容器','不帶針保存；不與他人共用筆'],'若有出血，以紗布輕壓，不搓揉。小心套回外罩，旋下針頭，立即放入抗針刺容器，再蓋筆蓋。不要帶針保存，也不能與他人共用注射筆。','dispose')
scene('四劑或三十天，先到就丟棄',['未使用：2–8°C；不可冷凍','使用後：≤30°C，避熱避光','4 劑／首次使用後 30 天，先到為準'],'未使用的筆冷藏於二到八度，不可冷凍。使用後可放在三十度以下，避熱避光。四劑用完或首次使用後三十天，先到就丟棄；不可抽出殘液當第五劑。','storage','TW IFU p6–7；UK SmPC §6.4')
scene('第 1–4 週：起始適應期',['每週 2.5 mg，持續 4 週','第 5 週起：每週 5 mg','起始劑量不作維持劑量'],'依處方從每週二點五毫克開始，持續四週，再增加至每週五毫克。起始階段讓身體適應；二點五毫克不是建議維持劑量，不能自行延長或變更處方。','start','台灣仿單 §3.1')
scene('要不要升劑？先回答三個問題',['目前劑量是否已至少 4 週？','仍需更多效果，而且能耐受？','由醫師決定，才每次加 2.5 mg'],'後續只有在仍需要更佳效果，而且能耐受時，才由醫師評估升劑。每個目前劑量都至少四週，每次只增加二點五毫克，不能直接從五跳到十毫克。','decision','台灣仿單 §3.1')
scene('六個月不是每月必升',['維持選擇：5／10／15 mg，每週一次','有效可留在較低維持劑量','最大 15 mg／週，不追求一定到頂'],'體重控制建議維持劑量是每週五、十或十五毫克。若五毫克已有效，就可以依醫師評估持續維持。六個月不是每月必須加藥，也不必追求最高劑量。','branch','台灣仿單 §3.1')
scene('24–26 週：持續評估與調整',['基線 → 4 週 → 12 週 → 24–26 週','看體重、腰圍、功能與耐受性','本片回診節點是衛教規劃範例'],'六個月約二十四到二十六週。可和團隊安排基線、第四週、第十二週與六個月評估，檢查效果、安全和生活執行。這些節點是衛教規劃，實際回診依個人需要。','calendar','衛教建議；非仿單強制回診表')
scene('生活調整：可持續，比激進重要',['少量慢吃・均衡營養','依能力增加活動與肌力訓練','CKD：飲水與蛋白質須個別化'],'生活管理可從少量慢吃、均衡飲食與規律活動開始，依能力加入肌力訓練。不要極端節食。若有慢性腎臟病或心衰竭，飲水量與蛋白質攝取須個別評估。','lifestyle','衛教建議；不是個別營養處方')
scene('每週追趨勢，每月看功能',['每週：同條件體重、劑量、腸胃症狀','記錄飲食、活動與血糖（依醫囑）','每月：腰圍、肌力與日常功能'],'每週在相近條件量體重，記錄注射日期、劑量、腸胃症狀、飲食與活動；血糖依醫囑。每月看腰圍、肌力和日常功能，不要用單次體重波動決定加藥。','tracker','衛教追蹤範例；無模擬病人數據')
scene('漏針：記住 96 與 72 小時',['漏打後 ≤96 小時：儘快補','超過 96 小時：跳過，照原排程','兩劑之間至少 72 小時；不加倍'],'漏打後九十六小時內，儘快補打；超過就跳過這一劑，照原定日期打下一劑。兩劑之間至少間隔七十二小時，不能用加倍注射補回。','missed','台灣仿單 §3.1')
scene('腸胃不適，先顧體液與安全',['噁心、嘔吐、腹瀉或便祕','吃喝不足、尿量減少、頭暈：聯絡團隊','胰島素／磺醯脲併用：監測低血糖'],'噁心、腹瀉、嘔吐或便祕都可能發生。若吃喝不足、尿量減少或頭暈，需聯絡團隊評估脫水與腎功能。併用胰島素或磺醯脲時，要注意低血糖，調藥由醫師決定。','safety','台灣仿單 §5.1.3、5.1.5、8')
scene('這些警訊，要立即處理',['持續嚴重腹痛，可能延伸至背部','臉舌喉腫、呼吸或吞嚥困難','停止使用並立即尋求醫療協助'],'若持續劇烈腹痛，尤其延伸至背部，或出現臉、舌、喉嚨腫脹，呼吸或吞嚥困難，請停止使用並立即尋求醫療協助。不要只當作一般腸胃適應。','alert','台灣仿單 §5.1.2、5.1.4')
scene('懷孕、避孕與麻醉，事先告知',['懷孕不使用；備孕、哺乳先問醫師','口服避孕：開始／升劑後 4 週加屏障','或改非口服；麻醉、深鎮靜前先告知'],'懷孕期間不使用，備孕與哺乳先和醫師討論。口服避孕藥使用者，開始治療及每次升劑後四週，應增加屏障避孕或改非口服方式。麻醉或深度鎮靜前，務必告知團隊。','pregnancy','台灣仿單 §5.1.9、6、7')
scene('每一針，都回到三個確認',['確認：正確筆、全劑量、完整注射','追蹤：效果、耐受性、生活功能','隨盒 IFU 優先；帶紀錄與團隊討論'],'最後記住，先確認正確的筆與全劑量，注射時按住數五並確認歸零，再持續追蹤效果與耐受性。器型或說明不同，以隨盒仿單與操作訓練為準，帶著紀錄和醫療團隊討論。','end','台灣仿單 2025-10-03／IFU Revised 2026-03-24')

async def voices():
    # 每個句子獨立合成，時間以實際音檔長度決定。
    (P/'audio').mkdir(exist_ok=True)
    jobs=[]
    for i,s in enumerate(S):
        s['sentences']=[x+'。' for x in s['voice'].split('。') if x]
        for j,t in enumerate(s['sentences']):jobs.append((i,j,t))
    sem=asyncio.Semaphore(3)
    async def one(i,j,t):
        f=P/'audio'/f's{i:02d}-{j:02d}.mp3'
        async with sem:
            if not f.exists():
                for n in range(4):
                    try:
                        await edge_tts.Communicate(t,'zh-TW-HsiaoChenNeural',rate='+3%').save(str(f));break
                    except Exception:
                        if n==3:raise
                        await asyncio.sleep(2)
        return f
    await asyncio.gather(*(one(*j) for j in jobs))

def duration(f):
    probe=P/'ffprobe.exe'
    if probe.exists():return float(subprocess.check_output([str(probe),'-v','error','-show_entries','format=duration','-of','csv=p=0',str(f)]))
    r=subprocess.run([r'C:\Users\User\AppData\Local\CapCut\Apps\8.5.0.3590\ffmpeg.exe','-hide_banner','-i',str(f)],capture_output=True,encoding='utf-8',errors='replace')
    h,m,sec=re.search(r'Duration: (\d+):(\d+):([\d.]+)',r.stderr).groups()
    return int(h)*3600+int(m)*60+float(sec)
def svg(art,i):
    # 自訂線稿：共用同一組筆身幾何，操作以部件位移與狀態切換示意。
    prefix=f'a{i}'
    pen='''<g class="pen-body"><rect x="100" y="210" width="450" height="90" rx="28" fill="#143542" stroke="#f4f7fa" stroke-width="4"/><rect x="125" y="225" width="115" height="60" rx="8" fill="#4dd9cf" fill-opacity=".25" stroke="#4dd9cf" stroke-width="3"/><rect x="270" y="228" width="150" height="54" rx="7" fill="#0b1422"/><rect x="440" y="228" width="65" height="54" rx="6" fill="#0b1422" stroke="#f4f7fa" stroke-width="2"/><g class="knob"><rect x="550" y="215" width="65" height="80" rx="15" fill="#4dd9cf"/><path d="M565 230v50m15-50v50m15-50v50" stroke="#0b1422" stroke-width="3"/></g><path d="M100 255H65" stroke="#f4f7fa" stroke-width="5"/><path d="M65 255H25" stroke="#f4f7fa" stroke-width="2"/></g>'''
    base=f'<svg id="{prefix}" viewBox="0 0 720 560" role="img" aria-label="自訂{art}操作示意圖">'
    text=lambda x,y,t,size=30:f'<text x="{x}" y="{y}" fill="#f4f7fa" font-size="{size}" text-anchor="middle">{html.escape(t)}</text>'
    if art in ['pen','parts','inspect','needle','prime','drop','dose','inject','zero','dispose']:
        out=pen
        value='1' if art in ['dose','inject'] else '0' if art in ['drop','zero'] else '─' if art=='prime' else ''
        label=text(473,268,value,36)+text(345,263,'MOUNJARO',20)
        if art in ['inject','zero']:
            label='<g class="window-one">'+text(473,268,'1',36)+'</g><g class="window-zero" opacity="0">'+text(473,268,'0',36)+'</g>'+text(345,263,'MOUNJARO',20)
        out=out[:-4]+label+'</g>'
        if art=='parts':out+='<rect x="80" y="380" width="140" height="70" rx="20" fill="#143542" stroke="#4dd9cf" stroke-width="3"/>'+text(150,495,'拆下筆蓋')+text(180,160,'藥匣')+text(345,355,'標籤')+text(480,160,'視窗')+text(585,355,'旋鈕')
        if art=='needle':out+='<g class="needle-cover"><rect x="2" y="226" width="65" height="58" rx="9" fill="#143542" stroke="#4dd9cf" stroke-width="3"/></g>'+text(230,400,'外罩保留 → 內罩丟棄')
        if art in ['prime','drop','inject','zero']:out='<g class="orientation" transform="translate(355 255) scale(.7) rotate('+('90' if art in ['prime','drop'] else '-90')+') translate(-355 -255)">'+out+'</g>'
        if art=='drop':out+='<path class="droplet" d="M355 2 C345 14 342 22 355 25 C368 22 365 14 355 2" fill="#4dd9cf"/>'
        if art in ['prime','drop']:out+=text(350,510,'向空氣排氣；不注入身體')
        if art in ['inject','zero']:out='<path d="M15 450H690V550H15Z" fill="#143542" stroke="#4dd9cf" stroke-width="3"/>'+out+text(570,520,'皮下組織示意',25)
        if art=='inject':out+=text(585,130,'按住數 5',38)
        if art=='dose':out+=text(350,420,'1 = 全劑量 ≠ 1 mg',42)
        if art=='dispose':out+='<g class="bin"><rect x="420" y="365" width="150" height="130" rx="12" fill="#143542" stroke="#4dd9cf" stroke-width="4"/><path d="M410 365h170" stroke="#4dd9cf" stroke-width="14"/></g>'+text(245,425,'卸針 → 棄針')
        if art=='inspect':out+=text(350,130,'藥名 ✓  強度 ✓  EXP ✓',34)+text(350,420,'澄清・無顆粒・無冷凍')
    elif art=='sites':
        out='<path d="M280 90h150l55 70 35 175-45 15-30-110v270h-65V365h-30v145h-65V240l-30 110-45-15 35-175Z" fill="#143542" stroke="#f4f7fa" stroke-width="4"/><circle cx="355" cy="255" r="12" fill="#0b1422" stroke="#f4f7fa" stroke-width="3"/><ellipse cx="355" cy="255" rx="70" ry="45" fill="none" stroke="#4dd9cf" stroke-width="16"/><rect x="295" y="365" width="35" height="80" rx="15" fill="#4dd9cf"/><rect x="385" y="365" width="35" height="80" rx="15" fill="#4dd9cf"/>'+text(115,255,'≥5 cm')+text(610,185,'上臂後側')+text(610,235,'由他人注射',26)
    elif art in ['start','decision','branch','calendar','missed']:
        if art=='branch':
            out='<path class="route" d="M70 200H240V140H650M240 200V310H650" fill="none" stroke="#4dd9cf" stroke-width="7"/>'+text(120,150,'5 mg',40)+text(440,100,'有效且耐受 → 維持',30)+text(450,365,'需要且耐受 → 醫師評估升劑',26)+text(370,460,'5／10／15 mg',48)
        else:
            vals=['0','4','12','24–26'] if art=='calendar' else ['2.5','5','7.5','10','12.5','15']
            out='<path class="route" d="M60 270H660" fill="none" stroke="#4dd9cf" stroke-width="6"/>'
            for j,v in enumerate(vals):
                x=70+j*580/(len(vals)-1);out+=f'<circle cx="{x}" cy="270" r="12" fill="#4dd9cf"/>'+text(x,230,v,36)
            out+=text(355,380,'週' if art=='calendar' else '每個目前劑量至少 4 週',32)
            if art=='missed':out=text(350,190,'≤96 h → 補',56)+text(350,290,'>96 h → 跳過',56)+text(350,410,'兩劑至少相隔 72 h',38)
    elif art=='four':
        out=''
        for j in range(4):out+=f'<rect class="dose-block" x="{45+j*165}" y="180" width="140" height="165" rx="18" fill="#143542" stroke="#4dd9cf" stroke-width="4"/>'+text(115+j*165,275,str(j+1),54)
        out+=text(355,420,'4 × 0.6 mL',52)
    elif art=='storage':out=text(350,180,'2–8°C',80)+text(350,290,'使用後 ≤30°C',52)+text(350,410,'4 劑／30 天',54)
    elif art=='retry':out=text(350,180,'無滴 → 再最多 2 次',40)+text(350,285,'換新針 → 再最多 1 次',40)+text(350,400,'仍無滴 → 停止求助',40)
    elif art=='mechanism':out='<circle cx="220" cy="230" r="100" fill="#143542" stroke="#4dd9cf" stroke-width="4"/><circle cx="500" cy="230" r="100" fill="#143542" stroke="#4dd9cf" stroke-width="4"/>'+text(220,245,'GIP',48)+text(500,245,'GLP-1',48)+text(355,430,'食慾與血糖調節',42)
    elif art=='tracker':out=''.join(f'<g class="trackrow-{j}"><rect x="80" y="{110+j*95}" width="560" height="70" rx="10" fill="#143542" stroke="#4dd9cf" stroke-width="2"/>'+text(355,156+j*95,t,30)+'</g>' for j,t in enumerate(['日期：填實際注射日','劑量：抄寫處方 mg','體重：填本週實測 kg','症狀：如實記錄有／無']))
    else:
        words={'check':['適用性','禁忌','用藥清單'],'supplies':['洗手','新針頭','抗針刺容器'],'lifestyle':['均衡飲食','規律活動','保留肌力'],'safety':['腸胃症狀','體液與腎功能','低血糖'],'alert':['嚴重腹痛','呼吸困難','立即就醫'],'pregnancy':['懷孕／哺乳','口服避孕','麻醉／鎮靜'],'end':['認筆','正確注射','持續追蹤']}.get(art,['確認','紀錄','討論'])
        out=''.join(f'<circle class="node" cx="120" cy="{150+j*130}" r="30" fill="#4dd9cf"/>'+text(120,162+j*130,str(j+1),30)+text(410,165+j*130,w,44) for j,w in enumerate(words))
    
    if art in ['drop','inject']:
        out+=''.join(f'<g class="count-{n}" opacity="0">'+text(585,230,str(n),76)+'</g>' for n in range(1,6))
    return base+out+'</svg>'

def build():
    start=0; caps=[];aud=[]
    for i,s in enumerate(S):
        s['start']=round(start,3);t=start+.5;s['audio']=[]
        for j,txt in enumerate(s['sentences']):
            f=P/'audio'/f's{i:02d}-{j:02d}.mp3';d=duration(f)
            a=dict(start=round(t,3),duration=round(d,3),text=txt,file=f'audio/{f.name}');s['audio'].append(a);aud.append(a)
            # 長句依標點分字幕，時間依字數配置，音檔以整句保留。
            chunks=[x for x in re.split(r'(?<=[，；。])',txt) if x]
            total=sum(len(x) for x in chunks)
            for c in chunks:
                cd=d*len(c)/total;caps.append((t,cd,c));t+=cd
            t+=.23
        s['duration']=round(t-start+.5,3);start+=s['duration']
        (P/'assets'/f'{i:02d}-{s["art"]}.svg').write_text(svg(s['art'],i),encoding='utf-8')
    total=round(start,3)
    css='''@font-face{font-family:LocalTC;src:url('assets/LocalTC.ttf')}*{box-sizing:border-box}html,body{margin:0;width:100%;height:100%;background:#0b1422;color:#f4f7fa;font-family:LocalTC,sans-serif}#root{position:relative;width:100%;height:100%;overflow:hidden}.clip{position:absolute;inset:0}.scene{padding:65px 95px}.kicker{font-size:25px;color:#4dd9cf;letter-spacing:3px;margin:0 0 19px}h1{font-size:61px;line-height:1.3;margin:0;max-width:1740px}.content{display:grid;grid-template-columns:820px 1fr;gap:55px;margin-top:36px;align-items:center;height:550px}.art{width:780px;height:550px;display:flex;align-items:center}.art svg{width:100%;height:100%;font-family:LocalTC,sans-serif}.copy{display:flex;flex-direction:column;gap:32px}.item{font-size:37px;line-height:1.5;margin:0;border-left:5px solid #4dd9cf;padding:12px 0 12px 24px}.source{position:absolute;bottom:158px;left:95px;right:95px;font-size:22px;color:#b9c9d8;margin:0}.caption{position:absolute;bottom:45px;left:95px;right:95px;min-height:80px;padding:18px;text-align:center;font-size:34px;line-height:1.45;background:#143542;border-radius:10px}.counter{position:absolute;top:30px;right:95px;color:#b9c9d8;font-size:22px}.rule{position:absolute;left:95px;right:95px;top:195px;height:2px;background:#315361}.progress{position:absolute;bottom:0;left:0;height:7px;width:100%;background:#4dd9cf;transform-origin:left}'''
    scenes=[];tweens=[]
    for i,s in enumerate(S):
        st=s['start'];du=s['duration'];a=svg(s['art'],i)
        scenes.append(f'<section id="scene{i}" class="clip" data-start="{st}" data-duration="{du}" data-track-index="1"><div class="scene"><p class="kicker">MOUNJARO KWIKPEN ・ 衛教示範</p><h1>{s["title"]}</h1><div class="rule"></div><div class="content"><div class="art">{a}</div><div class="copy">'+''.join(f'<p id="item{i}-{j}" class="item">{html.escape(x)}</p>' for j,x in enumerate(s['lines']))+f'</div></div><p class="source">來源：{s["source"]}｜自訂線稿示意・非器材比例圖｜隨盒 IFU 優先</p><span class="counter">{i+1:02d} / {len(S):02d}</span></div></section>')
        for j in range(3):tweens.append(f'tl.fromTo("#item{i}-{j}",{{opacity:0,y:12}},{{opacity:1,y:0,duration:.55,ease:"expo.out"}},{st+.1+j*.25});')
        # 操作部件以同一筆身幾何顯示動作，不以新筆替換。
        if s['art'] in ['drop','inject']:
            for n in range(1,6):
                tweens.append(f'tl.set("#a{i} .count-{n}",{{opacity:1}},{st+3+n-1});')
                tweens.append(f'tl.set("#a{i} .count-{n}",{{opacity:0}},{st+3+n});')
        if s['art']=='tracker':
            for r in range(4):tweens.append(f'tl.fromTo("#a{i} .trackrow-{r}",{{opacity:0}},{{opacity:1,duration:.4}},{st+1+r*2.2});')
        if s['art']=='needle':tweens.append(f'tl.fromTo("#a{i} .needle-cover",{{x:-50}},{{x:0,duration:1,ease:"power2.inOut"}},{st+1});')
        if s['art'] in ['inject','prime','drop']:
            tweens.append(f'tl.fromTo("#a{i} .knob",{{x:28}},{{x:0,duration:1.2,ease:"power2.inOut"}},{st+2});')
        if s['art']=='drop':tweens.append(f'tl.fromTo("#a{i} .droplet",{{opacity:0,y:15}},{{opacity:1,y:0,duration:.7}},{st+4});')
        if s['art'] in ['inject','zero']:
            tweens.append(f'tl.set("#a{i} .window-one",{{opacity:0}},{st+7.8});tl.set("#a{i} .window-zero",{{opacity:1}},{st+7.8});')
        if s['art'] in ['inject','zero']:tweens.append(f'tl.fromTo("#a{i} .pen-body",{{x:80}},{{x:-25,duration:1,ease:"power2.inOut"}},{st+.8});')
    for k,(t,d,c) in enumerate(caps):scenes.append(f'<div class="clip" id="cap{k}" data-start="{t:.3f}" data-duration="{d:.3f}" data-track-index="20"><div class="caption">{html.escape(c)}</div></div>')
    for k,a in enumerate(aud):scenes.append(f'<audio id="voice{k}" class="clip" src="{a["file"]}" data-start="{a["start"]}" data-duration="{a["duration"]}" data-track-index="30"></audio>')
    tweens.append(f'tl.fromTo(".progress",{{scaleX:0}},{{scaleX:1,duration:{total},ease:"none"}},0);')
    out=f'<!doctype html><html lang="zh-Hant"><head><meta charset="UTF-8"><title>Mounjaro KwikPen 與六個月管理</title><script src="assets/gsap.min.js"></script><style>{css}</style></head><body><div id="root" data-composition-id="kwikpen" data-width="1920" data-height="1080" data-fps="24" data-duration="{total}">'+''.join(scenes)+'<div class="progress"></div></div><script>const tl=gsap.timeline({paused:true});'+''.join(tweens)+'window.__timelines["kwikpen"]=tl;</script></body></html>'
    (P/'index.html').write_text(out,encoding='utf-8')
    (P/'scenes.json').write_text(json.dumps(S,ensure_ascii=False,indent=2),encoding='utf-8')
    (P/'audio_meta.json').write_text(json.dumps(dict(voice='zh-TW-HsiaoChenNeural',duration=total,sentences=aud),ensure_ascii=False,indent=2),encoding='utf-8')
    def tc(t):
        ms=round(t*1000);return f'{ms//3600000:02d}:{ms//60000%60:02d}:{ms//1000%60:02d},{ms%1000:03d}'
    (P/'mounjaro-kwikpen.srt').write_text('\n\n'.join(f'{k+1}\n{tc(t)} --> {tc(t+d)}\n{c}' for k,(t,d,c) in enumerate(caps))+'\n',encoding='utf-8')
    (P/'STORYBOARD.md').write_text('# Mounjaro KwikPen 與六個月管理\n\n'+ '\n\n'.join(f'## {i+1:02d} {s["title"]}\n\n{s["start"]:.3f}–{s["start"]+s["duration"]:.3f} 秒｜{s["art"]}｜{s["source"]}\n\n'+s['voice'] for i,s in enumerate(S)),encoding='utf-8')
    print(json.dumps(dict(scenes=len(S),sentences=len(aud),captions=len(caps),duration=total),ensure_ascii=False))

if __name__=='__main__':
    asyncio.run(voices());build()

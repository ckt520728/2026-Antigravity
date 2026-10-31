"""以 UTF-8 檔案執行，避免 PowerShell stdin codepage 損毀中文字。"""
from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[2]
W = ROOT / 'monjaro/workflow'
def load(name):
    return json.loads((W/name).read_text(encoding='utf-8'))
def save(name, value):
    (W/name).write_text(json.dumps(value, ensure_ascii=False, indent=2), encoding='utf-8')

a=load('approval.json')
a['scope']='本機 HTML、可編輯 PowerPoint、paper explainer DOCX、homepage blog 草稿與免費本機 motion 影片製作；不含發布、上傳、付費生成或部署。'
a['approval_evidence']['verified_by']='主控於 2026-10-31 讀回原 session'
a['scope_restatement']='本輪使用者 finish goal 授權由主控重述；不將毀損問號猜回歷史原文'
save('approval.json',a)
q=load('tasks.json');q['outline_approval']=a;q['stage']='T4 本機製作與獨立驗收'
q['tasks'][2]['acceptance'][-1]='歷史 T3 通過；後續使用者 outline 核准由 approval.json 另記'
t=q['tasks'][3];t['objective']='已核准 outline 的本機製作與獨立驗收；細項見 production-tasks.json'
t['acceptance']=['HTML 26 頁與可編輯 PPTX 對齊 outline 與 claim ledger','DOCX 與 blog 自然繁中、四脈絡、安全邊界及來源可回溯','motion 實際渲染、字幕與來源卡驗收','各產物主控獨立讀回；不發布、不花費']
save('tasks.json',q)
p=load('production-tasks.json');p['dispatch_mode']='host 手動明確配置 gpt-6.1-sol medium；非 JEV 自動 routing';p['budget_enforcement']='交接預算；API 硬限制與 usage 未暴露'
specs=[('T4_STATE','同步核准狀態並修復驗證器',['AGENTS.md','handoffs.md','monjaro/workflow/approval.json'],['monjaro/workflow/input-change-20261031.json','monjaro/workflow/validation-results.json'],[],7000),('T4_DOC_BLOG','製作專業閱讀文件與首頁文章草稿',['monjaro/specs/slide_outline.md','monjaro/evidence/claim_ledger.csv'],['monjaro/deliverables/mounjaro_paper_explainer.docx','monjaro/deliverables/mounjaro_paper_explainer.md','monjaro/deliverables/homepage_blog_draft.html'],['T4_STATE'],15000),('T4_DECK','製作 HTML 與可編輯 PowerPoint',['monjaro/specs/slide_outline.md','monjaro/evidence/claim_ledger.csv'],['monjaro/deliverables/mounjaro_evidence_deck.html','monjaro/deliverables/mounjaro_evidence_deck.pptx'],['T4_STATE'],15000),('T4_MOTION','製作免費本機 motion 影片',['monjaro/specs/slide_outline.md','monjaro/evidence/claim_ledger.csv'],['monjaro/deliverables/motion_storyboard.md','monjaro/deliverables/mounjaro_motion_explainer.mp4'],['T4_STATE'],15000),('T4_ACCEPT','主控獨立逐成品驗收',['monjaro/workflow/production-tasks.json'],['monjaro/qa/production_acceptance.md'],['T4_DOC_BLOG','T4_DECK','T4_MOTION'],7000)]
p['tasks']=[dict(task_id=i,objective=o,inputs=ins,outputs=outs,acceptance=['來源與 claim 可回溯','實際渲染或讀回符合工作包規格','無發布與花費'],capabilities=['read','local_write','process_spawn'],depends_on=deps,max_output_tokens=cap,status='待主控驗收' if i=='T4_STATE' else '執行中' if i!='T4_ACCEPT' else '待上游完成') for i,o,ins,outs,deps,cap in specs];save('production-tasks.json',p)
c=load('input-change-20261031.json');c['meaning']='本輪讀取前即與歷史 baseline 不同；不推定變更人與時間、不修改原 baseline；舊成果與 ZIP 另驗 35 檔';save('input-change-20261031.json',c)
notice='> **2026-10-31 現況更新**：使用者已於台北 2026-10-30 核准 v0.2-review outline，SHA-256 `2d499d07f1deb4ac92d48c074618e5152b19c322ee44c5c45158957713953b11`。本輪依 finish goal 授權進行免費本機 HTML／可編輯 PPTX／DOCX／blog 草稿／motion 影片製作與獨立驗收；不含發布、上傳、付費生成或部署。下文 pending／不派發／初始化描述保留為歷史階段。核准見 [approval](monjaro/workflow/approval.json)，production queue 見 [production tasks](monjaro/workflow/production-tasks.json)。自動 JEV routing_ready=false；host 手動 medium 分工另記。原 prompt 與歷史 baseline 不同，差異保留於 input-change-20261031.json；不得宣稱 36 檔全同。\n\n'
for rel in ['AGENTS.md','handoffs.md','monjaro/README.md','monjaro/workflow/WORKFLOW.md','monjaro/workflow/EXECUTION.md']:
    path=ROOT/rel;s=path.read_text(encoding='utf-8');s=s.split('\n\n',1)[1] if s.startswith('> ') else s;n=notice
    if rel.startswith('monjaro/workflow/'):
        n=n.replace('(monjaro/workflow/approval.json)','(approval.json)').replace('(monjaro/workflow/production-tasks.json)','(production-tasks.json)')
    elif rel=='monjaro/README.md':
        n=n.replace('(monjaro/workflow/approval.json)','(workflow/approval.json)').replace('(monjaro/workflow/production-tasks.json)','(workflow/production-tasks.json)')
    path.write_text(n+s,encoding='utf-8')
print('UTF-8 state repaired')

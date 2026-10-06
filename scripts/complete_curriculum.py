"""Generate claim-scoped evidence mapping and source-derived editorial outlines.

Never promotes source-only material to VERIFIED. Evidence must exist and its
runner summary must say PASS before an execution is attached to a claim.
"""
from pathlib import Path
import collections,datetime,hashlib,json,random,re,urllib.parse
ROOT=Path(__file__).resolve().parents[1]
def text(p): return (ROOT/p).read_text(encoding='utf-8-sig')
def write(p,s):
    target=ROOT/p; target.parent.mkdir(parents=True,exist_ok=True); target.write_text(s,encoding='utf-8')
def section(s,n):
    match=re.search(rf'^## {n}\. [^\n]+\n(.*?)(?=^## \d+\. |\Z)',s,re.M|re.S)
    return match[1].strip() if match else ''
def rebase(s,prefix):
    def fix(m):
        dest=m[1]
        if urllib.parse.urlsplit(dest).scheme or dest.startswith('#'): return m[0]
        return ']('+prefix+dest+')'
    return re.sub(r'\]\(([^\s)]+)\)',fix,s)
index=text('00_INDEX.md')
chapters=re.findall(r'\| [A-Z][A-Z0-9]* \| \[[^\]]+\]\(([^)]+\.md)\)',index)
legacy={
 '02_FRONTEND_DEEP_DIVE_AND_BUGS.md':['web/02_JS_RUNTIME.md','web/03_TYPESCRIPT_BOUNDARIES.md','web/04_REACT_MENTAL_MODEL.md','web/05_NEXT_EXECUTION.md'],
 '03_BACKEND_DEEP_DIVE_AND_BUGS.md':['web/06_CSHARP_RUNTIME.md','web/07_ASPNET_LIFECYCLE.md','web/08_API_CONTRACTS.md','web/09_DATABASE_CONCURRENCY.md','web/10_IDENTITY_SECURITY.md','web/15_DATABASE_TRANSACTIONS.md'],
 '04_FE_BE_INTEGRATION_AND_REAL_BUGS.md':['web/11_INTEGRATION_FLOW.md','web/08_API_CONTRACTS.md','debug/02_WEB_OBSERVABILITY.md']}
for p,targets in legacy.items():
    archive='archive/'+p
    if not (ROOT/archive).exists():
        original=text(p)
        write(archive,original.splitlines()[0]+'\n\n> Historical overview, superseded as a teaching source. Original content is retained for traceability; execution claims and snippets are not upgraded by this archive. [Current navigation](../'+p+').\n\n'+rebase('\n'.join(original.splitlines()[1:]),'../'))
    title=text(archive).splitlines()[0]
    write(p,title+'\n\nTrang điều hướng; các bài canonical dưới đây là nguồn giảng dạy chính. Nội dung overview cũ được giữ trong [archive]('+archive+'), không dùng như một nguồn kỹ thuật song song. Snippet lịch sử không được nâng mức kiểm chứng.\n\n'+''.join('- ['+q+']('+q+')\n' for q in targets)+'\n[Theory → lab](BUG_THEORY_MAP.md) · [Index](00_INDEX.md) · [Validation](VALIDATION.md).\n')
write('archive/README.md','# Historical material\n\nCác trang này giữ nội dung cũ để đối chiếu, không phải bài canonical hoặc evidence thực thi hiện tại. Dùng các trang dẫn ở root để tới bài chính.\n\n'+''.join('- ['+p+']('+p+')\n' for p in legacy)+'\n[Index](../00_INDEX.md).\n')

# tuple: log path, matching output marker, command, narrow claim, evidence level.
model={
 'foundations/02_JAVASCRIPT_LANGUAGE.md':('web','snapshot/functional','node examples/web_models.mjs','Snapshot replacement và functional update queue cho kết quả khác trong host model.'),
 'web/02_JS_RUNTIME.md':('web','forced response race','node examples/web_models.mjs','Request completion đảo thứ tự có thể publish stale result; model có ownership guard.'),
 'web/11_INTEGRATION_FLOW.md':('web','rollback ownership','node examples/web_models.mjs','Rollback chỉ thuộc version đang sở hữu optimistic state trong host fixture.'),
 'web/06_CSHARP_RUNTIME.md':('core','checked arithmetic','dotnet run --project examples/CoreModels/CoreModels.csproj -c Release','Checked arithmetic tại int boundary ném exception trong C# fixture, không chứng minh C UB.'),
 'web/14_DOTNET_ASYNC_RUNTIME.md':('core','propagated cancellation','dotnet run --project examples/CoreModels/CoreModels.csproj -c Release','Token cancellation được truyền tới Task.Delay và được quan sát trong fixture.'),
 'embedded_systems/07_DMA_OWNERSHIP.md':('systems','queued buffer','python examples/systems_models.py','Python handoff giữ reference tới buffer mutable, khác immutable snapshot; không mô phỏng cache/DMA hardware.'),
 'embedded_systems/08_CONCURRENCY_BUFFERS.md':('systems','bounded queue','python examples/systems_models.py','Queue bounded chứa hai item và ghi nhận item thứ ba bị drop theo policy trong model.'),
 'embedded_systems/16_REAL_TIME.md':('systems','tick rollover','python examples/systems_models.py','Modulo elapsed model giữ timeout qua rollover với bound không mất nguyên chu kỳ; không phải native C tick.'),
 'os/03_IO_IPC_LIFETIME.md':('systems','file lifecycle','python examples/systems_models.py','Python context manager đóng file trong success/exception path; không đo Linux FD hoặc kernel lifetime.')}
host_pass=(ROOT/'evidence/host-models/summary.json').exists() and json.loads(text('evidence/host-models/summary.json'))['result']=='PASS'
mongo_pass=(ROOT/'evidence/mongo-api/summary.json').exists() and json.loads(text('evidence/mongo-api/summary.json'))['result']=='PASS'
claims=[]
for p in chapters:
    s=text(p); title=s.splitlines()[0].lstrip('# ')
    claim={'chapter':p,'title':title,'level':'UNVERIFIED','claim':section(s,9).split('\n\n')[0],
           'evidence':None,'command':None,'observed':None,
           'limit':'Source/pseudocode review only; no topic-specific executable record. Demo remains BLOCKED.'}
    if host_pass and p in model:
        name,marker,cmd,description=model[p]
        log='evidence/host-models/'+name+'.log'
        lines=[x for x in text(log).splitlines() if marker in x]
        if not lines: raise ValueError('Missing observed output: '+marker)
        claim.update(level='MODEL',claim=description,evidence=log,command=cmd,observed='\n'.join(lines),
                     limit='Chỉ invariant nêu trên trong host fixture; không xác minh toàn bài, MCU/native C/C++, framework hoặc production target.')
    if p=='web/04_REACT_MENTAL_MODEL.md' and json.loads(text('evidence/react-race/summary.json'))['result']=='PASS':
        claim.update(level='VERIFIED',claim='Effect cleanup stale guard giữ B khi phản hồi A tới sau B trong React DOM fixture.',
            evidence='evidence/react-race/fixed.log',command='cd examples/react-race && python verify.py',
            observed=text('evidence/react-race/broken.log')+'\n'+text('evidence/react-race/fixed.log'),
            limit='React DOM/jsdom với hai Promise schedules; không phải HTTP, browser paint, StrictMode hay kiểm chứng toàn bộ React.')
    if mongo_pass and p in {'web/09_DATABASE_CONCURRENCY.md','web/15_DATABASE_TRANSACTIONS.md','web/08_API_CONTRACTS.md'}:
        description=('Conditional single-document update và unique index giữ invariant dưới concurrent HTTP requests.'
                     if p!='web/08_API_CONTRACTS.md' else 'Cùng idempotency key/payload trả một orderId; payload khác bị 409 trong HTTP/MongoDB fixture.')
        claim.update(level='VERIFIED',claim=description,evidence='evidence/mongo-api/verification.log',
            command='python examples/MongoApi/verify.py --mongod <path-to-mongod>',observed=text('evidence/mongo-api/verification.log'),
            limit='Standalone MongoDB, một API instance và 20 rounds; không chứng minh multi-document transaction, replica set, failover hoặc majority write concern. Docker Compose chưa chạy local.')
    claims.append(claim)
    output='content/'+p
    prefix='../../'
    flow=section(s,7)
    failure=section(s,11)
    debug=section(s,12)
    sources=section(s,16).split('[Index]')[0].strip()
    demo=('```text\n'+claim['command']+'\n```\n\nOutput quan sát trích nguyên từ [evidence]('+prefix+claim['evidence']+'):\n\n```text\n'+claim['observed']+'\n```'
          if claim['evidence'] else '**BLOCKED — chưa có demo thực thi riêng cho claim này.** Không có output để trích; không dùng kết quả của bài khác thay thế. Chưa sẵn sàng xuất bản phần demo. Xem [bài nguồn]('+prefix+p+') và [matrix]('+prefix+'THEORY_COVERAGE_MATRIX.md).')
    write(output,'# Outline — '+title+'\n\nMức của claim minh họa: **'+claim['level']+'**. Không phải mức chứng nhận toàn bài.\n\n'+
        '## 1. Hook\n\n'+rebase(failure.split('\n\n')[0],prefix+str(Path(p).parent).replace('\\','/')+'/')+'\n\nĐặt câu hỏi: cơ chế trong ['+title+']('+prefix+p+') giải thích failure này bằng invariant nào?\n\n'+
        '## 2. Mô hình trong 60 giây\n\n```text\nrepresentation -> actor/control flow -> ownership/lifetime -> invariant -> evidence\n```\n\n'+rebase(flow,prefix+str(Path(p).parent).replace('\\','/')+'/')+'\n\n'+
        '## 3. Demo chạy thật\n\nClaim có phạm vi: '+claim['claim']+'\n\n'+demo+'\n\n'+
        '## 4. Cách nó hỏng và cách phát hiện\n\n'+rebase(failure+'\n\n'+debug,prefix+str(Path(p).parent).replace('\\','/')+'/')+'\n\n'+
        '## 5. Giới hạn trung thực\n\n'+claim['limit']+'\n\nOutline này trích nội dung hiện có; không bổ sung bảo đảm về target chưa đo. Chỉ công bố demo khi mức/evidence phù hợp.\n\n'+
        '## 6. Nguồn và câu hỏi tự kiểm tra\n\n'+rebase(sources,prefix+str(Path(p).parent).replace('\\','/')+'/')+'\n\n'+rebase(section(s,15),prefix+str(Path(p).parent).replace('\\','/')+'/')+'\n\n[Index](../../00_INDEX.md) · [Content](../README.md).\n')
write('content/README.md','# Outlines cho kênh\n\nMỗi bài canonical có sáu phần. Chỉ những outline có demo evidence và claim VERIFIED/MODEL được dùng để xuất bản demo; UNVERIFIED có placeholder BLOCKED rõ ràng. Mức áp dụng cho claim được trích, không chứng nhận toàn chương.\n\n'+
      '| Bài | Claim level | Demo |\n|---|---|---|\n'+''.join('| ['+c['title']+']('+c['chapter']+') | '+c['level']+' | '+('Evidence có sẵn' if c['evidence'] else 'BLOCKED')+' |\n' for c in claims)+'\n[Matrix](../THEORY_COVERAGE_MATRIX.md) · [Review](../REVIEW_CHECKLIST.md) · [Index](../00_INDEX.md).\n')
matrix=text('THEORY_COVERAGE_MATRIX.md').split('\n## Claim → evidence → mức độ')[0]
matrix+='\n## Claim → evidence → mức độ\n\nCập nhật '+datetime.date.today().isoformat()+'. Đây là một claim đại diện mỗi bài canonical; không thay độ sâu GOOD/COMPLETE ở bảng lịch sử. VERIFIED chỉ là invariant đã chạy trong fixture; MODEL chỉ là host abstraction; UNVERIFIED là nguồn/pseudocode chưa chạy.\n\n| Bài | Claim đại diện | Evidence | Mức | Giới hạn |\n|---|---|---|---|---|\n'
for c in claims:
    evidence='['+c['evidence']+']('+c['evidence']+')' if c['evidence'] else 'Nguồn ở [bài]('+c['chapter']+'#16-nguồn); chưa có execution log'
    matrix+='| ['+c['title']+']('+c['chapter']+') | '+c['claim'].replace('\n',' ').replace('|','\\|')+' | '+evidence+' | '+c['level']+' | '+c['limit']+' |\n'
write('THEORY_COVERAGE_MATRIX.md',matrix)
write('evidence/claim_matrix.json',json.dumps(claims,ensure_ascii=False,indent=2))
chosen=random.Random(20261006).sample(sorted(chapters),10)
findings={
 'web/08_API_CONTRACTS.md':'PATCH version/tenant pseudocode chưa chạy; order replay fixture chỉ bao phủ idempotency, không BOLA/validation/pagination.',
 'embedded_systems/03_CPP_OWNERSHIP.md':'BufferOwner là interface sketch với deleted copy, chưa có constructor/move/destructor contract; không dùng làm demo RAII runnable.',
 'foundations/01_DIGITAL_REPRESENTATION.md':'250+10 và uint8_t conversion là dự đoán có int-width assumption; chưa có native C compiler log.',
 'web/13_BROWSER_INTERNALS.md':'Batch layout reads/writes chưa có browser Performance capture; jsdom race không chứng minh layout performance.',
 'web/09_DATABASE_CONCURRENCY.md':'Compound-index pagination snippet chưa chạy explain; conditional-update/unique-index evidence không chứng minh query plan.',
 'embedded_systems/11_BUILD_LINK_STARTUP.md':'nm/objdump/size chưa có ELF/ABI/target record; build API không thay ARM image verification.',
 'embedded_systems/13_MMIO_MCU.md':'W1C là pseudocode không real address; thiếu vendor RM0090 access và target measurement.',
 'debug/03_SYSTEMS_OBSERVABILITY.md':'GDB cần ELF/probe/target; không có observed stack/register trace. Sanitizer scope không được nâng mức.',
 'embedded_systems/01_C_REPRESENTATION.md':'minimum caller contract đòi live/aligned bounds; chưa có compiler/sanitizer execution để kiểm fixture.',
 'debug/01_EVIDENCE_METHOD.md':'Investigation stock model là reasoning framework; bằng chứng một fixture không xác nhận mọi phương pháp debug.'}
review='# Self-review lần hai\n\nKhông phải review của người độc lập. Chọn 10 bài bằng `random.Random(20261006).sample(sorted(chapters), 10)`; seed và hash làm lựa chọn có thể kiểm tra lại. Đọc invariant, ví dụ, nguồn và đối chiếu claim/evidence; không coi kiểm tra cấu trúc là kiểm chứng kỹ thuật.\n\n| Bài | SHA-256 | Quan sát |\n|---|---|---|\n'
for p in chosen:
    c=next(c for c in claims if c['chapter']==p)
    observation=('Có execution log cho claim hẹp; các phần khác chưa được nâng mức. '+c['limit'] if c['evidence'] else
                 'Ví dụ/nguồn không cung cấp execution record riêng. Giữ UNVERIFIED; demo outline BLOCKED, không viết output dự đoán thành quan sát.')
    review+='| ['+p+'](../'+p+') | `'+hashlib.sha256((ROOT/p).read_bytes()).hexdigest()+'` | '+findings[p]+' '+observation+' |\n'
write('audit/SELF_REVIEW.md',review+'\n[Checklist](../REVIEW_CHECKLIST.md) · [Matrix](../THEORY_COVERAGE_MATRIX.md) · [Index](../00_INDEX.md).\n')
print(json.dumps({'claim_levels':dict(collections.Counter(c['level'] for c in claims)), 'outlines':len(claims),'review_sample':chosen},ensure_ascii=False,indent=2))

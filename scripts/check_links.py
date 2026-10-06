"""Validate Markdown links/anchors, index reachability, structure and lab mapping."""
from pathlib import Path
import argparse, collections, datetime, json, re, subprocess, urllib.parse
ROOT = Path(__file__).resolve().parents[1]
parser = argparse.ArgumentParser()
parser.add_argument('--report', type=Path)
args = parser.parse_args()
paths = subprocess.check_output(['git','ls-files','--cached','--others','--exclude-standard','-z'],cwd=ROOT).decode().split('\0')
texts = {p:(ROOT/p).read_text(encoding='utf-8-sig') for p in set(paths) if p.endswith('.md') and (ROOT/p).is_file()}
def prose(s):
    output, fence = [], None
    for line in s.splitlines():
        m = re.match(r'^\s*(`{3,}|~{3,})',line)
        if m:
            if fence is None: fence = m[1][0]
            elif m[1][0] == fence: fence = None
            output.append('')
        else: output.append(line if fence is None else '')
    return '\n'.join(output)
def slug(h):
    h = re.sub(r'<[^>]*>|`','',h).lower()
    return ''.join(c for c in h if c.isalnum() or c in ' _-').replace(' ','-')
anchors = {}
for p,s in texts.items():
    used, values = collections.Counter(),set()
    for h in re.findall(r'^#{1,6}\s+(.+)$',prose(s),re.M):
        key=slug(h); n=used[key]; used[key]+=1
        values.add(key+(f'-{n}' if n else ''))
    anchors[p]=values
errors, graph, link_count = [], {p:set() for p in texts}, 0
for p,s in texts.items():
    for raw in re.findall(r'\[[^\]\n]*\]\(([^\s)]+)(?:\s+[^)]*)?\)',prose(s)):
        raw=raw.strip('<>'); parsed=urllib.parse.urlsplit(raw)
        if parsed.scheme or raw.startswith('//'): continue
        link_count+=1
        target=((ROOT/p).parent/urllib.parse.unquote(parsed.path) if parsed.path else ROOT/p).resolve()
        try: rel=target.relative_to(ROOT).as_posix()
        except ValueError:
            errors.append(f'{p}: target escapes repository: {raw}'); continue
        if not target.exists(): errors.append(f'{p}: missing target {raw}'); continue
        if parsed.fragment and rel in anchors and urllib.parse.unquote(parsed.fragment) not in anchors[rel]:
            errors.append(f'{p}: missing anchor {raw}')
        if rel in texts: graph[p].add(rel)
seen,todo=set(),['00_INDEX.md']
while todo:
    p=todo.pop()
    if p in seen: continue
    seen.add(p); todo.extend(graph.get(p,set())-seen)
orphans=sorted(set(texts)-seen)
errors.extend('Unreachable Markdown: '+p for p in orphans)
chapters=re.findall(r'\| [A-Z][A-Z0-9]* \| \[[^\]]+\]\(([^)]+\.md)\)',texts['00_INDEX.md'])
for p in chapters:
    if p not in texts: errors.append('Missing canonical chapter: '+p); continue
    if [int(n) for n in re.findall(r'^##\s+(\d+)\.',texts[p],re.M)]!=list(range(1,17)):
        errors.append('Canonical 16-section structure deviation: '+p)
labs={p for p in texts if p.startswith('labs/') and Path(p).name!='README.md'}
mapped=re.findall(r'\]\((labs/[^)#]+\.md)\)',texts['BUG_THEORY_MAP.md'])
counts=collections.Counter(mapped)
for p in labs:
    if counts[p]!=1: errors.append(f'{p}: expected exactly one lab-map row, found {counts[p]}')
    invariant=re.search(r'^## Invariant\s*\n(.*?)(?=^## |\Z)',texts[p],re.M|re.S)
    rows=[line for line in texts['BUG_THEORY_MAP.md'].splitlines() if ']('+p+')' in line]
    if not invariant or not rows or invariant[1].strip().replace('|','\\|') not in rows[0]:
        errors.append(p+': mapped invariant differs from lab')
ledger_path=ROOT/'evidence/claim_matrix.json'
if ledger_path.exists():
    ledger=json.loads(ledger_path.read_text(encoding='utf-8'))
    if collections.Counter(c['chapter'] for c in ledger)!=collections.Counter(chapters):
        errors.append('Claim ledger must contain exactly one row per canonical chapter')
    for c in ledger:
        outline='content/'+c['chapter']
        if outline not in texts or [int(n) for n in re.findall(r'^##\s+(\d+)\.',texts.get(outline,''),re.M)]!=list(range(1,7)):
            errors.append('Missing six-part outline: '+outline)
        if c['level'] not in {'VERIFIED','MODEL','UNVERIFIED'}:
            errors.append('Invalid claim level: '+c['chapter'])
        if c['level'] in {'VERIFIED','MODEL'} and (not c.get('evidence') or not (ROOT/c['evidence']).is_file() or not c.get('observed') or not c.get('command')):
            errors.append('Claim without executable evidence: '+c['chapter'])
report={'date_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'result':'FAIL' if errors else 'PASS',
        'markdown':len(texts),'internal_links':link_count,'canonical_chapters':len(chapters),'labs':len(labs),'orphans':orphans,'errors':errors}
if args.report:
    args.report.parent.mkdir(parents=True,exist_ok=True)
    args.report.write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(report,ensure_ascii=False,indent=2))
raise SystemExit(bool(errors))

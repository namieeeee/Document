"""Read tracked curriculum files and produce reproducible Phase 0 audit reports."""
from pathlib import Path
import concurrent.futures
import datetime
import hashlib
import json
import re
import shutil
import subprocess
import sys
import urllib.error
import urllib.parse
import urllib.request

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'audit'
files = subprocess.check_output(['git', 'ls-files', '-z'], cwd=ROOT).decode().split('\0')
files = [p for p in files if p and not p.startswith(('audit/', 'scripts/'))]
texts = {p: (ROOT / p).read_text(encoding='utf-8-sig') for p in files if p.endswith('.md')}
stamp = datetime.datetime.now(datetime.timezone.utc).isoformat()
commit = subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=ROOT).decode().strip()
toolchain = {name: shutil.which(name) for name in ('python', 'node', 'dotnet', 'gcc', 'clang', 'docker', 'make', 'bash')}
OUT.mkdir(exist_ok=True)

def prose(s):
    return re.sub(r'^\s*(```|~~~).*?^\s*\1\s*$', '', s, flags=re.M | re.S)

def slug(s):
    s = re.sub(r'<[^>]*>|`', '', s).lower()
    return ''.join(c for c in s if c.isalnum() or c in ' _-').replace(' ', '-')

anchors = {}
for p, s in texts.items():
    used = {}
    anchors[p] = set()
    for h in re.findall(r'^#{1,6}\s+(.+)$', prose(s), re.M):
        key = slug(h)
        n = used.get(key, 0)
        anchors[p].add(key + (f'-{n}' if n else ''))
        used[key] = n + 1

links, urls, graph = [], set(), {p: set() for p in texts}
for p, s in texts.items():
    for match in re.finditer(r'\[[^\]\n]*\]\(([^\s)]+)(?:\s+[^)]*)?\)', prose(s)):
        raw = match.group(1).strip('<>')
        if raw.startswith(('http://', 'https://')):
            urls.add(raw)
            continue
        if urllib.parse.urlsplit(raw).scheme:
            continue
        parsed = urllib.parse.urlsplit(raw)
        target = (ROOT / p).parent / urllib.parse.unquote(parsed.path) if parsed.path else ROOT / p
        target = target.resolve()
        try:
            rel = target.relative_to(ROOT).as_posix()
        except ValueError:
            rel = str(target)
        status = 'OK' if target.exists() else 'MISSING'
        if status == 'OK' and parsed.fragment and rel in anchors:
            if urllib.parse.unquote(parsed.fragment) not in anchors[rel]:
                status = 'MISSING_ANCHOR'
        line = prose(s)[:match.start()].count('\n') + 1
        links.append((p, line, raw, status))
        if rel in texts and status == 'OK':
            graph[p].add(rel)
reachable, todo = set(), ['00_INDEX.md']
while todo:
    p = todo.pop()
    if p in reachable:
        continue
    reachable.add(p)
    todo.extend(graph.get(p, set()) - reachable)

def fetch(url):
    try:
        request = urllib.request.Request(url, headers={'User-Agent': 'Document-curriculum-audit/1.0'})
        with urllib.request.urlopen(request, timeout=15) as response:
            body = response.read(1024 * 1024)
            return {'url': url, 'status': response.status, 'final_url': response.url,
                    'sample_sha256': hashlib.sha256(body).hexdigest(), 'sample_bytes': len(body)}
    except urllib.error.HTTPError as e:
        return {'url': url, 'status': e.code, 'detail': str(e)}
    except Exception as e:
        return {'url': url, 'status': 'UNVERIFIED_NETWORK', 'detail': str(e)}

cached = OUT / 'phase0_measurements.json'
if '--cached-urls' in sys.argv and cached.exists():
    previous = json.loads(cached.read_text(encoding='utf-8'))
    external = previous['external']
    assert set(r['url'] for r in external) == urls, 'URL set changed; rerun live checks'
    url_check_date = previous.get('url_check_date', previous['date'])
else:
    print(f'Checking {len(urls)} external URLs', flush=True)
    with concurrent.futures.ThreadPoolExecutor(max_workers=8) as pool:
        external = list(pool.map(fetch, sorted(urls)))
    url_check_date = stamp

canonical = re.findall(r'\| [A-Z][A-Z0-9]* \| \[[^\]]+\]\(([^)]+\.md)\)', texts['00_INDEX.md'])
questions = {}
structures = []
for p, s in texts.items():
    heads = re.findall(r'^##\s+(.+)$', s, re.M)
    if p in canonical:
        nums = [int(x) for x in re.findall(r'^##\s+(\d+)\.', s, re.M)]
        structures.append((p, 'OK' if nums == list(range(1, 17)) else 'DEVIATION', len(heads)))
    section = re.search(r'^##[^\n]*(?:Tự kiểm|Self.check)[^\n]*\n(.*?)(?=^##\s|\Z)', s, re.M | re.S | re.I)
    questions[p] = len(re.findall(r'^\s*\d+[.)]\s+', section.group(1), re.M)) if section else 0

claims = []
for p, s in texts.items():
    for n, line in enumerate(s.splitlines(), 1):
        if re.search(r'đã kiểm chứng|validated|\bPASS\b', line, re.I):
            # Quoted source text is literal, not an audit-relative live link.
            claims.append((p, n, line.replace('|', '\\|').replace('[', '&#91;').replace(']', '&#93;')))
def claim_status(p, n, line):
    reports = {'EXPANSION_REPORT.md', 'THEORY_COMPLETION_REPORT.md', 'VALIDATION.md'}
    if p in reports and re.search(r'\bPASS\b|Đã chạy|chạy trực tiếp DLL đã thành công', line):
        if (p, n) in {('VALIDATION.md', 40)}:
            return 'NOT_AN_EXECUTION_CLAIM: explicitly excludes unrun compilation'
        return 'MISSING_PORTABLE_LOG: prose summary exists; attach raw execution record'
    return 'NOT_AN_EXECUTION_CLAIM: instruction, model invariant, scope limit or terminology'
header = f'Generated by `python scripts/audit_phase0.py` at {stamp}.\n\nBaseline commit: `{commit}`. Counts exclude audit reports and audit tooling; tracked files only.\n\n'
def write(name, body):
    (OUT / name).write_text(header + body, encoding='utf-8')

labs = [p for p in texts if p.startswith('labs/') and Path(p).name != 'README.md']
write('INVENTORY.md', '# Inventory\n\n' +
      f'Tracked baseline files: {len(files)}. Markdown: {len(texts)}. Lab documents: {len(labs)}. Canonical chapters: {len(canonical)}. Numbered self-check items: {sum(questions.values())}.\n\n' +
      'Self-check counting includes numbered items in the first self-check section; answers and unnumbered prompts are excluded. A lab document is not evidence of an executable test.\n\n' +
      '| File | Self-check items |\n|---|---:|\n' + ''.join(f'| `{p}` | {questions.get(p, 0)} |\n' for p in files))
write('LINKS_AND_STRUCTURE.md', '# Links and structure\n\n' +
      f'Internal link occurrences: {len(links)}. Broken: {sum(x[3] != "OK" for x in links)}. Markdown unreachable from index: {len(set(texts) - reachable)}. External URLs: {len(external)}.\n\n' +
      f'External check date: {url_check_date}.\n\nIndex reachability is transitive; direct index omissions are listed separately. HTTP errors can reflect access restrictions; network errors do not prove a dead source. Body hashes cover at most 1 MiB and cannot establish historical content changes without a baseline.\n\n' +
      '## Index omissions\n\nDirect omissions: ' + ', '.join(f'`{p}`' for p in sorted(set(texts) - graph['00_INDEX.md'] - {'00_INDEX.md'})) +
      '\n\nUnreachable: ' + (', '.join(sorted(set(texts) - reachable)) or 'None') +
      '\n\n## Canonical structure\n\n| Chapter | Status | H2 count |\n|---|---|---:|\n' + ''.join(f'| `{p}` | {s} | {n} |\n' for p, s, n in structures) +
      '\n## Internal links\n\n| File | Occurrence after code removal | Target | Status |\n|---|---:|---|---|\n' + ''.join(f'| `{p}` | {n} | `{u}` | {s} |\n' for p, n, u, s in links) +
      '\n## External URLs\n\n| URL | Observed status | Detail |\n|---|---|---|\n' + ''.join(f'| {r["url"]} | {r["status"]} | {r.get("detail", r.get("final_url", "")).replace("|", " ")} |\n' for r in external))
write('UNSUPPORTED_CLAIMS.md', '# Claims requiring evidence review\n\n' +
      f'Keyword occurrences: {len(claims)}. These are candidates, not a verdict that each sentence makes a validation claim. Hypothetical PASS output and instructions must be distinguished from reported executions.\n\n' +
      'No committed evidence directory was found in the baseline. Existing model source and prose do not supply a portable execution record containing command, tool version, date and observed output. Previous local runs are not disputed; repository evidence remains incomplete.\n\n' +
      '| File | Line | Candidate text | Evidence status |\n|---|---:|---|---|\n' + ''.join(f'| `{p}` | {n} | {line} | {claim_status(p, n, line)} |\n' for p, n, line in claims))
write('PHASE0_REPORT.md', '# Phase 0 report\n\n' +
      'The baseline curriculum was read without modification. This audit measures inventory, index reachability, link occurrences, numbered self-check items, canonical 16-section structure and validation-keyword candidates.\n\n' +
      'G1–G4: baseline has Python, JavaScript and process-local C# models; no tracked C/C++ sources, React renderer or MongoDB integration fixture. G5–G6: the JavaScript model contains a fixed wall-clock threshold and elementary integer addition assertion. G7: baseline has no run_all runner or CI workflow. These models need explicit scope and execution evidence.\n\n' +
      '## Environment discovery\n\n| Tool | PATH discovery |\n|---|---|\n' + ''.join(f'| {name} | `{path or "NOT_FOUND"}` |\n' for name, path in toolchain.items()) +
      '\nC/C++ compiler and sanitizer runs require a usable GCC and Clang toolchain. PATH discovery is not a search of the entire machine. No compiler, sanitizer, MongoDB or React execution is claimed by this audit.\n\n' +
      'Structure checking verifies section numbering, not semantic correctness. Keyword matching does not prove a claim false. Root overview duplication and technical contradictions require editorial review; this script does not infer them from matching words.\n')
(OUT / 'phase0_measurements.json').write_text(json.dumps({'commit': commit, 'date': stamp, 'url_check_date': url_check_date, 'files': files, 'self_checks': questions, 'external': external}, ensure_ascii=False, indent=2), encoding='utf-8')
print(json.dumps({'files': len(files), 'markdown': len(texts), 'labs': len(labs), 'chapters': len(canonical), 'self_checks': sum(questions.values()), 'internal_links': len(links), 'broken': sum(x[3] != 'OK' for x in links), 'unreachable': len(set(texts) - reachable), 'external': len(external)}, ensure_ascii=False), flush=True)

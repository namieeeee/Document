"""Verify the intentional regression and fix; preserve raw tool output."""
from pathlib import Path
import datetime
import json
import os
import shutil
import subprocess
import sys

HERE = Path(__file__).resolve().parent
EVIDENCE = HERE.parents[1] / 'evidence' / 'react-race'
EVIDENCE.mkdir(parents=True, exist_ok=True)
npm = shutil.which('npm.cmd' if os.name == 'nt' else 'npm')
if not npm:
    sys.exit('BLOCKED: npm is unavailable')
records = []

def run(name, args, env=None):
    result = subprocess.run(args, cwd=HERE, env=env, text=True,
                            stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                            encoding='utf-8', errors='replace')
    (EVIDENCE / f'{name}.log').write_text(result.stdout, encoding='utf-8')
    records.append({'name': name, 'command': args, 'exit_code': result.returncode})
    print(f'{name}: exit {result.returncode}', flush=True)
    return result.returncode

for name, args in [('node-version', ['node', '--version']),
                   ('npm-version', [npm, '--version']),
                   ('package-versions', [npm, 'ls', '--depth=0'])]:
    if run(name, args):
        sys.exit('BLOCKED: dependencies are missing; run npm ci first')

valid = True
for variant in ('broken', 'fixed'):
    env = dict(os.environ, RACE_VARIANT=variant, NO_COLOR='1')
    report = EVIDENCE / f'{variant}.json'
    if report.exists():
        report.unlink()
    code = run(variant, [npm, 'exec', '--', 'vitest', 'run',
               '--reporter=verbose', '--reporter=json',
               f'--outputFile.json={report}'], env)
    if not report.exists():
        valid = False
        continue
    data = json.loads(report.read_text(encoding='utf-8'))
    assertions = [a for suite in data.get('testResults', [])
                  for a in suite.get('assertionResults', [])]
    failed = [a for a in assertions if a['status'] == 'failed']
    if variant == 'broken':
        valid &= (code == 1 and len(assertions) == 2 and len(failed) == 1
                  and failed[0]['title'] == 'keeps latest result when B completes before stale A'
                  and 'AssertionError' in '\n'.join(failed[0].get('failureMessages', [])))
    else:
        valid &= code == 0 and len(assertions) == 2 and all(a['status'] == 'passed' for a in assertions)

summary = {'date_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
           'python': sys.version, 'commands': records,
           'result': 'PASS' if valid else 'FAIL',
           'scope': 'React DOM in jsdom; controlled Promise order, no live HTTP or browser paint'}
(EVIDENCE / 'summary.json').write_text(json.dumps(summary, indent=2), encoding='utf-8')
print(summary['result'] + ': expected regression failure and fixed invariant')
sys.exit(0 if valid else 1)

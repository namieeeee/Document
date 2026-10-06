"""Real HTTP concurrency against a disposable ASP.NET/MongoDB fixture."""
from pathlib import Path
import argparse, concurrent.futures, datetime, json, os, subprocess, sys, tempfile, time, urllib.request, urllib.error, uuid
HERE = Path(__file__).resolve().parent
EVIDENCE = HERE.parents[1] / 'evidence' / 'mongo-api'
EVIDENCE.mkdir(parents=True, exist_ok=True)
parser = argparse.ArgumentParser()
parser.add_argument('--mongod', type=Path)
parser.add_argument('--external', action='store_true', help='API already started by Docker Compose')
args = parser.parse_args()
base = 'http://127.0.0.1:5291'
records = []
log = (EVIDENCE / 'verification.log').open('w', encoding='utf-8')
def say(s): print(s, flush=True); log.write(s + '\n'); log.flush()
def request(path, method='GET', body=None):
    data = json.dumps(body).encode() if body is not None else (b'' if method != 'GET' else None)
    req = urllib.request.Request(base + path, data=data, method=method, headers={'Content-Type':'application/json'})
    try:
        response = urllib.request.urlopen(req, timeout=15)
    except urllib.error.HTTPError as e:
        response = e
    with response:
        raw = response.read()
        return response.status, json.loads(raw) if raw else None
def parallel(path, n=2, body=None):
    with concurrent.futures.ThreadPoolExecutor(max_workers=n) as pool:
        return list(pool.map(lambda _: request(path, 'POST', body), range(n)))
def command(name, argv):
    r = subprocess.run(argv, cwd=HERE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, encoding='utf-8', errors='replace')
    (EVIDENCE / (name + '.log')).write_text(r.stdout, encoding='utf-8')
    records.append({'command': argv, 'exit_code': r.returncode})
    if r.returncode: raise RuntimeError(f'{name} failed: see log')
    return r.stdout
processes, handles = [], []
result = 'FAIL'
try:
    with tempfile.TemporaryDirectory(prefix='document-mongo-fixture-') as temp:
        if not args.external:
            if not args.mongod or not args.mongod.is_file(): raise RuntimeError('BLOCKED: supply --mongod or --external')
            command('mongodb-version', [str(args.mongod), '--version'])
            command('dotnet-version', ['dotnet', '--version'])
            command('build', ['dotnet', 'build', '-c', 'Release'])
            command('package-versions', ['dotnet', 'list', 'package'])
            flags = subprocess.CREATE_NO_WINDOW if os.name == 'nt' else 0
            for name, argv in [('mongo-process', [str(args.mongod), '--dbpath', temp, '--bind_ip', '127.0.0.1', '--port', '27029']),
                               ('api-process', ['dotnet', str(HERE / 'bin/Release/net8.0/MongoApi.dll'), '--urls', base])]:
                handle = (EVIDENCE / (name + '.log')).open('w', encoding='utf-8')
                handles.append(handle)
                processes.append(subprocess.Popen(argv, cwd=HERE, stdout=handle, stderr=subprocess.STDOUT, creationflags=flags))
                records.append({'command': argv})
        for attempt in range(60):
            try:
                status, health = request('/health')
                if status == 200: break
            except (OSError, urllib.error.URLError): pass
            if any(p.poll() is not None for p in processes): raise RuntimeError('Fixture process exited early')
            time.sleep(0.5)
        else: raise RuntimeError('Fixture did not become ready')
        assert health['database'].startswith('document_fixture_'), 'Not a fixture database'
        say('database=' + health['database'])
        bad = uuid.uuid4().hex
        assert request('/stock/' + bad, 'PUT')[0] == 200
        broken = parallel('/unsafe/buy/' + bad)
        assert [r[0] for r in broken] == [200, 200]
        say('EXPECTED FAIL broken stock invariant: successes=2 for available=1')
        for i in range(20):
            key = uuid.uuid4().hex
            assert request('/stock/' + key, 'PUT')[0] == 200
            purchases = parallel('/buy/' + key)
            assert sorted(r[0] for r in purchases) == [200, 409]
            assert request('/stock/' + key)[1]['available'] == 0
            inserts = parallel('/items/' + key)
            assert sorted(r[0] for r in inserts) == [200, 409]
            assert request('/items/' + key)[1]['count'] == 1
            replay = parallel('/orders/' + key, 8, {'payload':'fixture'})
            assert all(r[0] == 200 for r in replay)
            assert len({r[1]['orderId'] for r in replay}) == 1
            assert request('/orders/' + key, 'POST', {'payload':'fixture'})[1]['orderId'] == replay[0][1]['orderId']
            assert request('/orders/' + key, 'POST', {'payload':'different'})[0] == 409
            assert request('/orders/' + key)[1]['count'] == 1
            say(f'round {i+1}: conditional-update PASS; unique-index PASS; idempotent-replay PASS (8 concurrent + 1 retry + conflict)')
        say('PASS: 20/20 rounds for each of 3 database invariants')
        result = 'PASS'
        # Only stop processes this runner started, before removing its temp data.
        for p in reversed(processes): p.terminate(); p.wait(timeout=20)
        processes.clear()
finally:
    for p in reversed(processes):
        if p.poll() is None: p.terminate(); p.wait(timeout=20)
    for h in handles: h.close()
    log.close()
    (EVIDENCE / 'summary.json').write_text(json.dumps({'date_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
        'result':result, 'rounds':20 if result == 'PASS' else 0, 'commands':records,
        'verifier_command':[sys.executable,*sys.argv], 'python':sys.version,
        'runtime':'Docker Compose' if args.external else 'native standalone MongoDB',
        'scope':'single API instance, standalone MongoDB, no replica-set/failover/majority-write-concern/transactions'}, indent=2), encoding='utf-8')

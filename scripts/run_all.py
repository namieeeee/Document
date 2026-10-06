"""One-command validation; user-skipped Phase 1 stays skipped."""
from pathlib import Path
import argparse,datetime,json,os,shutil,subprocess,sys
ROOT=Path(__file__).resolve().parents[1]
parser=argparse.ArgumentParser()
parser.add_argument('--mongod',type=Path)
parser.add_argument('--skip-mongo',action='store_true',help='Report MongoDB BLOCKED, not PASS')
args=parser.parse_args()
OUT=ROOT/'evidence'; OUT.mkdir(exist_ok=True)
(OUT/'run_all.json').write_text(json.dumps({'date_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'result':'RUNNING'}),encoding='utf-8')
steps=[('documentation',[sys.executable,'-X','utf8','scripts/check_links.py','--report','evidence/documentation-checks.json'],ROOT),
       ('host-models',[sys.executable,'scripts/capture_models.py'],ROOT),
       ('react-dependencies',[shutil.which('npm.cmd' if os.name=='nt' else 'npm') or 'npm','ci','--no-audit','--no-fund'],ROOT/'examples/react-race'),
       ('react-race',[sys.executable,'verify.py'],ROOT/'examples/react-race')]
if args.mongod and not args.skip_mongo:
    steps.append(('mongodb',[sys.executable,'verify.py','--mongod',str(args.mongod.resolve())],ROOT/'examples/MongoApi'))
records=[{'name':'Phase 1 native C/C++','status':'SKIPPED_BY_USER'}]
for name,command,cwd in steps:
    print('RUN '+name,flush=True)
    try:
        result=subprocess.run(command,cwd=cwd,text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,encoding='utf-8',errors='replace')
        code=result.returncode; output=result.stdout
    except OSError as e: code=1; output=str(e)
    (OUT/('runner-'+name+'.log')).write_text(output,encoding='utf-8')
    print(name+': '+('PASS' if code==0 else 'FAIL'),flush=True)
    records.append({'name':name,'command':command,'cwd':str(cwd.relative_to(ROOT)) or '.',
                    'exit_code':code,'status':'PASS' if code==0 else 'FAIL'})
if not args.mongod or args.skip_mongo:
    records.append({'name':'mongodb','status':'BLOCKED','reason':'Supply --mongod executable; Docker Compose may be validated separately in CI'})
failed=any(r['status']=='FAIL' for r in records)
blocked=any(r['status']=='BLOCKED' for r in records)
summary={'date_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'steps':records,
         'result':'FAIL' if failed else 'BLOCKED' if blocked else 'PASS'}
(OUT/'run_all.json').write_text(json.dumps(summary,indent=2),encoding='utf-8')
print(summary['result'],flush=True)
sys.exit(1 if failed else 2 if blocked else 0)

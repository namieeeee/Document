"""Record fresh host-model runs without broadening their proof scope."""
from pathlib import Path
import datetime,json,subprocess,sys
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'evidence/host-models'; OUT.mkdir(parents=True,exist_ok=True)
commands=[('python-version',[sys.executable,'--version']),('node-version',['node','--version']),
          ('dotnet-version',['dotnet','--version']),('systems',[sys.executable,'examples/systems_models.py']),
          ('web',['node','examples/web_models.mjs']),
          ('core-build',['dotnet','build','examples/CoreModels/CoreModels.csproj','-c','Release','--ignore-failed-sources']),
          ('core',['dotnet','examples/CoreModels/bin/Release/net8.0/CoreModels.dll'])]
records=[]
for name,cmd in commands:
    r=subprocess.run(cmd,cwd=ROOT,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True,encoding='utf-8',errors='replace')
    (OUT/(name+'.log')).write_text(r.stdout,encoding='utf-8')
    records.append({'name':name,'command':cmd,'exit_code':r.returncode})
    print(name,r.returncode,flush=True)
    if r.returncode: break
(OUT/'summary.json').write_text(json.dumps({'date_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
    'commands':records,'result':'PASS' if len(records)==len(commands) and all(r['exit_code']==0 for r in records) else 'FAIL',
    'scope':'Python/Node/C# host fixtures; not MCU, RTOS, native C/C++, production database or browser renderer'},indent=2),encoding='utf-8')
sys.exit(0 if len(records)==len(commands) and all(r['exit_code']==0 for r in records) else 1)

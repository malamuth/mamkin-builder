import hashlib, json, runpy
from pathlib import Path
root=Path(__file__).resolve().parent
initial=json.loads((root/'initial-hashes.json').read_text())
results={}
for arm in ['sol-medium','astra-medium']:
    path=root/arm/'summary.py'
    fn=runpy.run_path(str(path))['summarize']
    scenarios=[([], {'names':[], 'counts':{}}),([' B ','a','b'], {'names':['b','a'],'counts':{'b':2,'a':1}}),([' Straße ','STRASSE','straße'], {'names':['strasse'],'counts':{'strasse':3}}),(['','  ','\t\n'], {'names':[], 'counts':{}}),(['z','Y','z','x','y'], {'names':['z','y','x'],'counts':{'z':2,'y':2,'x':1}})]
    checks=[]
    for items, expected in scenarios:
        original=items[:]
        actual=fn(items)
        checks.append({'input':original,'expected':expected,'actual':actual,'passed':actual==expected and items==original})
    results[arm]=checks
changed=[]
for path,digest in initial.items():
    p=root/path
    actual=hashlib.sha256(p.read_bytes()).hexdigest() if p.exists() else 'missing'
    if actual!=digest: changed.append(path)
allowed=['sol-medium/summary.py','astra-medium/summary.py']
report={'implementation_checks':results,'changed_initial_files':changed,'unexpected_changes':sorted(set(changed)-set(allowed)),'all_passed':all(c['passed'] for cs in results.values() for c in cs) and not set(changed)-set(allowed)}
(root/'acceptance-results.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2))
raise SystemExit(0 if report['all_passed'] else 1)

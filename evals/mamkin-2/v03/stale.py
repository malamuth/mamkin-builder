#!/usr/bin/env python3
"""Focused existing B04 regression: source contradicts done; reuse sandboxed scorer."""
import argparse
import json
import subprocess
import sys
from pathlib import Path
import run as current

sys.path.insert(0,str(current.HERE.parent/'stage-3'))
import comparison


def main(output):
    assert output.is_absolute() and not output.exists()
    receipt=current.receipt()
    path=current.HERE.parent/'stage-3/comparison.py'
    rel=str(path.relative_to(current.REPO));h=current.common.digest(path.read_bytes())
    assert h==current.common.digest(subprocess.check_output(['git','-C',str(current.REPO),'show',receipt['criteriaCommit']+':'+rel]))
    receipt['sourceHashes'][rel]=h
    output.mkdir();case=current.common.baseline.get_case('B04');root=output/'project'
    current.common.baseline.prepare(case,root)
    comparison.overlay(root,'reduced')
    current.common.save(output/'B04-input.json',{'files':current.common.baseline.snapshot(root)})
    # The legacy scorer receipt is resolved relative to the project root's parent.
    result,before=current.common.native(root,case['prompt'],output,'B04',receipt)
    argv=['codex','sandbox','--permission-profile',':read-only','-C',str(root),'--','python3','-B',str(path),'check','--case','B04','--root',str(root),'--mamkin']
    p=subprocess.run(argv,text=True,capture_output=True,timeout=100)
    result['checkLaunch']={'argv':argv,'exitCode':p.returncode,'stderr':p.stderr[-1500:]}
    result['deterministic']=json.loads(p.stdout) if p.returncode==0 else {'deterministicPass':False,'scorerError':p.stdout[-1500:]}
    result['covers']=['M09']
    result['parentBehavioral']={'pass':None,'criteria':case['behavioralCriteria']+['Assigns an ID to the admitted existing managed task when missing; preserves the existing source owner']}
    current.common.save(output/'B04-result.json',result)
    ok=result['launch']['exitCode']==0 and result['launch']['completedTurns']>0 and result['deterministic']['deterministicPass']
    print(json.dumps({'case':'B04','pass':ok,'seconds':result['launch']['elapsedSeconds']}),flush=True)
    if not ok:raise SystemExit(1)


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--output',required=True,type=Path)
    main(p.parse_args().output)

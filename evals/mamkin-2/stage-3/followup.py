#!/usr/bin/env python3
"""Frozen derived candidate: repair the missed existing-skill suggestion only."""
import argparse
import json
import subprocess
from pathlib import Path
import common
import comparison
import remaining

BASE = '34c7a52'
OLD = 'For observed recurring procedures, briefly suggest a project skill or existing-skill update with its repetition, trigger and saved work; do not create/change skills automatically or block the task on the suggestion.'
NEW = 'For recurring project procedures, include a concrete reuse proposal at handoff: prefer updating an existing matching skill; otherwise suggest a project skill. Name observed repetition, trigger and saved work. This advice never blocks current work or authorizes skill creation/changes.'
ORIGINAL_INSTALL = common.install


def candidate_text():
    text = subprocess.check_output(['git','-C',str(common.REPO),'show',BASE+':.agents/skills/mamkin-work/SKILL.md'],text=True)
    assert text.count(OLD)==1
    return text.replace(OLD,NEW)


def install(root, ref=None):
    ORIGINAL_INSTALL(root, ref or BASE)
    if ref is None:
        (root/'.agents/skills/mamkin-work/SKILL.md').write_text(candidate_text())


def receipt():
    r=common.source_receipt()
    r['candidateDerivation']={'baseCommit':BASE,'transformSource':'evals/mamkin-2/stage-3/followup.py','workSha256':common.digest(candidate_text().encode()),'setupSha256':common.digest(subprocess.check_output(['git','-C',str(common.REPO),'show',BASE+':.agents/skills/mamkin-setup/SKILL.md'])),'purpose':'Only the project-learning proposal paragraph changes; all task inputs and acceptance remain frozen.'}
    return r


def learning(output):
    # Keep the exact original R01/R02 requests, seeds and criteria.
    def install_case(root):
        install(root)
    remaining.checks.previous.install=install_case
    original=common.source_receipt
    def derived_receipt():
        common.source_receipt=original
        try:return receipt()
        finally:common.source_receipt=derived_receipt
    common.source_receipt=derived_receipt
    remaining.CASES=[c for c in remaining.CASES if c['id'] in ('R01','R02')]
    remaining.run(output)


def reduced(output):
    assert output.is_absolute() and not output.exists()
    r=receipt();output.mkdir()
    common.install=install
    all_pass=True
    for c in common.baseline.cases():
        root=output/c['id'];common.baseline.prepare(c,root)
        common.save(output/(c['id']+'-core.json'),common.snapshot(root))
        comparison.overlay(root,'reduced')
        common.save(output/(c['id']+'-input.json'),{'files':common.baseline.snapshot(root)})
        result,before=common.native(root,c['prompt'],output,c['id'],r)
        argv=['codex','sandbox','--permission-profile',':read-only','-C',str(root),'--','python3','-B',str(Path(comparison.__file__).resolve()),'check','--case',c['id'],'--root',str(root),'--mamkin']
        p=subprocess.run(argv,text=True,capture_output=True,timeout=100)
        result['arm']='reduced-learning-fix'
        result['checkLaunch']={'argv':argv,'exitCode':p.returncode,'stderr':p.stderr[-1500:]}
        result['deterministic']=json.loads(p.stdout) if p.returncode==0 else {'deterministicPass':False,'scorerError':p.stdout[-1500:]}
        result['parentBehavioral']={'pass':None,'criteria':c['behavioralCriteria']}
        result['processMeasurements']={'beforeWords':sum(len(v.split()) for k,v in before.items() if k in ('work.md','docs/mamkin/work.md','docs/mamkin/project.md')),'afterWords':sum(len(v.split()) for k,v in common.snapshot(root).items() if k in ('work.md','docs/mamkin/work.md','docs/mamkin/project.md'))}
        common.save(output/(c['id']+'-result.json'),result)
        ok=result['launch']['exitCode']==0 and result['launch']['completedTurns']>0 and result['deterministic']['deterministicPass']
        all_pass &= ok
        print(json.dumps({'case':c['id'],'pass':ok,'seconds':result['launch']['elapsedSeconds']}),flush=True)
    if not all_pass:raise SystemExit(1)


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('part',choices=['learning','reduced'])
    p.add_argument('--output',required=True,type=Path)
    a=p.parse_args()
    (learning if a.part=='learning' else reduced)(a.output)

#!/usr/bin/env python3
"""Versioned checkpoint correction; initial product remains frozen during native runs."""
import argparse
import importlib.util
import subprocess
import sys
from pathlib import Path

HERE=Path(__file__).resolve().parent
REPO=HERE.parents[2]
BASE='b0846d9'
OLD='Update the authoritative record at meaningful transitions: current task/phase, applicable grant/limits, useful progress, actual verification, blocker and next action. Preserve useful work during corrections; queue adjacent ideas without expanding the task.'
NEW='Keep one accurate current account per task: ID/phase, applicable grant/limits, useful progress, actual checks, blocker and next step. Replace stale agent checkpoints rather than append per-run logs, retaining human history and decision reasons. Update at meaningful transitions; preserve useful work during corrections and queue adjacent ideas outside the grant.'


def load(name,path):
    s=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m


common=load('checkpoint_helpers',HERE.parent/'stage-3/common.py')


def candidate():
    text=subprocess.check_output(['git','-C',str(REPO),'show',BASE+':.agents/skills/mamkin-work/SKILL.md'],text=True)
    assert text.count(OLD)==1
    return text.replace(OLD,NEW)


def receipt(suite):
    paths=list(HERE.glob('*.py'))+[HERE/'README.md']
    for stage in ['stage-0','stage-1','stage-2','stage-3']:
        paths+=list((HERE.parent/stage).glob('*.py'))+list((HERE.parent/stage).glob('cases.json'))
    paths += [REPO/'.agents/skills'/n/'SKILL.md' for n in common.SKILLS]
    commit=subprocess.check_output(['git','-C',str(REPO),'rev-parse','HEAD'],text=True).strip()
    hashes={str(p.relative_to(REPO)):common.digest(p.read_bytes()) for p in paths}
    for p,h in hashes.items():assert common.digest(subprocess.check_output(['git','-C',str(REPO),'show',commit+':'+p]))==h,p
    return {'criteriaCommit':commit,'sourceHashes':hashes,'suite':suite,'candidateDerivation':{'baseCommit':BASE,'transformSource':'evals/mamkin-2/v03/checkpoint.py','workSha256':common.digest(candidate().encode()),'setupSha256':common.digest(subprocess.check_output(['git','-C',str(REPO),'show',BASE+':.agents/skills/mamkin-setup/SKILL.md']))}}


def install(root):
    common.install(root,BASE)
    (root/'.agents/skills/mamkin-work/SKILL.md').write_text(candidate())


def main(suite,output):
    assert output.is_absolute() and not output.exists()
    r=receipt(suite)
    if suite=='cycle':
        reg=load('checkpoint_semantic',HERE.parent/'stage-2/regression.py')
        runner=reg.legacy_run
        runner.checks.check=reg.semantic_check
        runner.checks.install=install
    else:
        sys.path.insert(0,str(HERE.parent/'stage-2'))
        runner=load('checkpoint_bounds',HERE.parent/'stage-2/run.py')
        runner.cases.CASES=[c for c in runner.cases.CASES if c['group'] in ('phase','cap')]
        runner.checks.previous.install=install
    save=runner.save
    def annotated(path,value):
        if path.name.endswith('-before.json'):
            assert value['.agents/skills/mamkin-work/SKILL.md']==candidate()
            common.save(path.parent/'candidate-source.json',r)
        if path.name.endswith('-result.json'):
            value={**value,'checkpointEvaluation':r,'v03StateAccuracy':{'pass':None,'criteria':['Current account agrees with actual queued work; superseded agent checkpoints are consolidated without losing useful work, IDs, decision reasons or grant boundaries']}}
        save(path,value)
    runner.save=annotated
    sys.argv=[str(runner.__file__),'--output',str(output)]
    runner.main()


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('suite',choices=['cycle','bounds']);p.add_argument('--output',required=True,type=Path)
    a=p.parse_args();main(a.suite,a.output)

#!/usr/bin/env python3
"""Executed v0.3 functional cases, not a Mamkin runtime or comparative score."""
import argparse
import hashlib
import importlib.util
import json
import subprocess
from pathlib import Path
import cases

HERE=Path(__file__).resolve().parent
REPO=HERE.parents[2]
spec=importlib.util.spec_from_file_location('native_helpers',HERE.parent/'stage-3/common.py')
common=importlib.util.module_from_spec(spec);spec.loader.exec_module(common)


def receipt():
    paths=list(HERE.glob('*.py'))+[HERE/'README.md']
    paths += [HERE.parent/p for p in ['stage-3/common.py','stage-1/checks.py','stage-0/suite.py','stage-0/cases.json']]
    paths += [REPO/'.agents/skills'/n/'SKILL.md' for n in common.SKILLS]
    paths += [REPO/'docs/project'/n for n in ['mamkin-2-spec.md','mamkin-2-mvp-plan.md']]
    commit=subprocess.check_output(['git','-C',str(REPO),'rev-parse','HEAD'],text=True).strip()
    hashes={str(p.relative_to(REPO)):common.digest(p.read_bytes()) for p in paths}
    for p,h in hashes.items():assert common.digest(subprocess.check_output(['git','-C',str(REPO),'show',commit+':'+p]))==h,p
    return {'criteriaCommit':commit,'sourceHashes':hashes}


def prepare(root,c):
    root.mkdir()
    files={
      'AGENTS.md':'# Local notes project\n\nPython standard library only. Preserve user files. No tooling installation, external actions, publication or configuration changes.\nProject entrypoint: docs/mamkin/project.md. Work entrypoint: docs/mamkin/work.md. Use $mamkin-work for project plans, decisions or authorized work.\nCheck an artifact with python3 -B tools/check_output.py ID.\n',
      'README.md':'# Local notse\n\nGoal: local report examples. Existing plan: docs/plan.md. Existing decisions and reasons: docs/choices.md.\n',
      'docs/plan.md':cases.PLAN,
      'docs/choices.md':cases.DECISIONS,
      'docs/mamkin/project.md':'# Project context\n\nGoal: local notes and report examples. Constraints/commands: ../../AGENTS.md. Decisions with reasons: ../choices.md, the authoritative existing owner. Work: work.md.\n',
      'docs/mamkin/work.md':'# Work entrypoint\n\nTasks, phases, grants, current status and continuation are owned by ../plan.md. Follow and update that source without copying its records here.\n',
      'config.py':"USER_LABEL = 'base'\n",
      'owner-notes.md':'# Owner draft\n\nPreserve my note verbatim. Do not turn it into a process document.\n',
      'execution.txt':'',
      'tools/check_output.py':"import sys\nfrom pathlib import Path\ntid=sys.argv[1]\nassert (Path('artifacts')/(tid+'.txt')).read_text()==tid+'\\n'\nprint('ARTIFACT_OK',tid)\n",
    }
    files.update(c['seed'] or {})
    if c['setup']:
        del files['docs/mamkin/project.md'];del files['docs/mamkin/work.md']
    for name,text in files.items():
        p=root/name;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(text)
    common.install(root)
    common.baseline.git(root,'init','-q');common.baseline.git(root,'add','.')
    common.baseline.git(root,'-c','user.name=Mamkin evaluation','-c','user.email=evaluation@example.invalid','-c','core.hooksPath=/dev/null','commit','-qm','Frozen v0.3 fixture')
    (root/'config.py').write_text("USER_LABEL = 'owner draft retain'\n")


def check(c,root,before):
    after=common.snapshot(root)
    changed=sorted(k for k in before.keys()|after.keys() if before.get(k)!=after.get(k))
    unexpected=[k for k in changed if k not in c['changes']]
    expected={f'artifacts/{tid}.txt':tid+'\n' for tid in c['artifacts']}
    expected.update({f'draft/{tid}.txt':tid+'\n' for tid in c['drafts']})
    actual={k:v for k,v in after.items() if k.startswith(('artifacts/','draft/'))}
    checks={'authorized_changes_only':not unexpected,'expected_inert_outputs_only':actual==expected,'exact_completion_trace':after.get('execution.txt')==c['trace'],'owner_note_preserved':after.get('owner-notes.md')==before.get('owner-notes.md'),'user_change_preserved':after.get('config.py')==before.get('config.py')}
    for n in common.SKILLS:
        p='.agents/skills/'+n+'/SKILL.md';checks[n+'_preserved']=before[p]==after.get(p)
    if c['read']:checks['no_file_changes']=before==after
    if c['setup']:
        checks['minimal_context_exists']=all((root/'docs/mamkin'/n).is_file() for n in ['project.md','work.md'])
        checks['existing_owners_verbatim']=all(before[p]==after.get(p) for p in ['docs/choices.md','docs/plan.md'])
        remaining=iter(after.get('AGENTS.md','').splitlines())
        checks['original_instructions_preserved']=all(any(old==new for new in remaining) for old in before['AGENTS.md'].splitlines() if old.strip())
    if c['id']=='V16':checks['only_requested_typo']=after.get('README.md')==before['README.md'].replace('notse','notes')
    return {'pass':all(checks.values()),'checks':checks,'details':{'changedFiles':changed,'unexpectedChanges':unexpected},'behavioralReview':'Separate parent inspection of actual sources, output, event order and criteria; no wording/heading matcher.'}


def run(output):
    assert output.is_absolute() and not output.exists(),'New absolute output required'
    r=receipt();output.mkdir();roots={}
    for c in cases.CASES:
        root=output/c['group']
        if c['group'] not in roots:prepare(root,c);roots[c['group']]=root
        result,before=common.native(root,c['prompt'],output,c['id'],r)
        result['group']=c['group'];result['covers']=c['covers']
        result['deterministic']=check(c,root,before)
        result['parentBehavioral']={'pass':None,'criteria':c['criteria']}
        common.save(output/(c['id']+'-result.json'),result)
        ok=result['launch']['exitCode']==0 and result['launch']['completedTurns']>0 and result['deterministic']['pass']
        print(json.dumps({'case':c['id'],'pass':ok,'seconds':result['launch']['elapsedSeconds']}),flush=True)
        if not ok:raise SystemExit('Stopped; preserve actual failure and inspect before continuing')


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--output',required=True,type=Path)
    run(p.parse_args().output)

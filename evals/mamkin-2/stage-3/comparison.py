#!/usr/bin/env python3
"""Three-arm repeated baseline, with an unchanged task and shared versioned scorer."""
import argparse
import copy
import json
import subprocess
from pathlib import Path
import common

PRIOR = '94bc3e8dc048b7c3e9d3d66943d227b4d33059e8'


def overlay(root, arm):
    if arm == 'plain':
        return
    common.install(root, PRIOR if arm == 'prior' else None)
    with (root / 'AGENTS.md').open('a') as f:
        f.write('\nContext: docs/mamkin/project.md. Work entrypoint: docs/mamkin/work.md. Use $mamkin-work for authorized execution/continuation.\n')
    folder = root / 'docs/mamkin'
    folder.mkdir(parents=True)
    (folder / 'project.md').write_text('# Project\n\nGoal and domain: ../../README.md. Constraints and actual commands: ../../AGENTS.md. Existing work owner is ../../work.md when present. No separate task specification is required.\n')
    (folder / 'work.md').write_text('# Work entrypoint\n\nThe existing ../../work.md is authoritative for tasks, order, progress and current status when present; follow that source and update it without duplicating its task records. Otherwise record the task from the current request here. Default scope: one task; mode/order comes from the existing plan, backlog when absent. No broader or external authority is recorded.\n')


def check(case, root, mamkin):
    # This entire scorer, including baseline's child Python commands, executes
    # under the native read-only/network-disabled sandbox from run().
    case = copy.deepcopy(case)
    if mamkin:
        case['allowedChanges'] += ['docs/mamkin/project.md', 'docs/mamkin/work.md']
    result = common.baseline.check(case, root)
    checks, details = result['checks'], result['details']
    ast_match = checks.pop('existing_test_bodies_preserved', None)
    if ast_match is not None:
        prefix = 'import cart,unittest\n'
        suffix = "suite=unittest.defaultTestLoader.discover('tests')\nresult=unittest.TextTestRunner(verbosity=0).run(suite)\n"
        probes = {
            'normal': prefix + suffix + 'assert result.wasSuccessful() and result.testsRun>0\n',
            'original_label': prefix + "original=cart.customer_label\ncart.customer_label=lambda name: original(name)+'!' if name=='Ada' else original(name)\n" + suffix + 'assert result.failures and not result.errors\n',
            'original_total': prefix + 'original=cart.total_cents\ncart.total_cents=lambda lines: original(lines)+1 if lines==[(125,2),(50,1)] else original(lines)\n' + suffix + 'assert result.failures and not result.errors\n',
        }
        details['legacyAstBodyMatch'] = ast_match
        details['coverageProbes'] = {}
        for name, code in probes.items():
            p = subprocess.run(['python3', '-B', '-c', code], cwd=root, text=True, capture_output=True, timeout=15)
            details['coverageProbes'][name] = {'pass': p.returncode == 0, 'exitCode': p.returncode, 'diagnostic': p.stderr[-1400:]}
        checks['original_behavior_coverage_preserved'] = all(x['pass'] for x in details['coverageProbes'].values())
    result['deterministicPass'] = all(checks.values())
    result['scorerVersion'] = 'stage-3-shared-semantic-v1'
    return result


def run(output):
    assert output.is_absolute() and not output.exists(), 'Output must be a new absolute path'
    receipt = common.source_receipt()
    output.mkdir()
    all_pass = True
    arms = ['plain', 'prior', 'reduced']
    for i, case in enumerate(common.baseline.cases()):
        for arm in arms[i % 3:] + arms[:i % 3]:
            group = output / arm
            group.mkdir(exist_ok=True)
            root = group / case['id']
            common.baseline.prepare(case, root)
            core = common.snapshot(root)
            overlay(root, arm)
            common.save(group / (case['id'] + '-core.json'), core)
            common.save(group / (case['id'] + '-input.json'), {'files': common.baseline.snapshot(root)})
            result, before = common.native(root, case['prompt'], group, case['id'], receipt)
            argv = ['codex', 'sandbox', '--permission-profile', ':read-only', '-C', str(root), '--', 'python3', '-B', str(Path(__file__).resolve()), 'check', '--case', case['id'], '--root', str(root)]
            if arm != 'plain':
                argv.append('--mamkin')
            proc = subprocess.run(argv, text=True, capture_output=True, timeout=100)
            result['arm'] = arm
            result['checkLaunch'] = {'argv': argv, 'exitCode': proc.returncode, 'stderr': proc.stderr[-1500:]}
            result['deterministic'] = json.loads(proc.stdout) if proc.returncode == 0 else {'deterministicPass': False, 'scorerError': proc.stdout[-1500:]}
            result['parentBehavioral'] = {'pass': None, 'criteria': case['behavioralCriteria']}
            result['processMeasurements'] = {'beforeWords': sum(len(v.split()) for k,v in before.items() if k in ('work.md','docs/mamkin/work.md','docs/mamkin/project.md')), 'afterWords': sum(len(v.split()) for k,v in common.snapshot(root).items() if k in ('work.md','docs/mamkin/work.md','docs/mamkin/project.md'))}
            common.save(group / (case['id'] + '-result.json'), result)
            ok = result['launch']['exitCode'] == 0 and result['launch']['completedTurns'] > 0 and result['deterministic']['deterministicPass']
            all_pass &= ok
            print(json.dumps({'case': case['id'], 'arm': arm, 'pass': ok, 'seconds': result['launch']['elapsedSeconds']}), flush=True)
    if not all_pass:
        raise SystemExit(1)


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('action', choices=['run','check'])
    p.add_argument('--output',type=Path)
    p.add_argument('--case')
    p.add_argument('--root',type=Path)
    p.add_argument('--mamkin', action='store_true')
    a = p.parse_args()
    if a.action == 'run':
        run(a.output)
    else:
        print(json.dumps(check(common.baseline.get_case(a.case), a.root, a.mamkin), ensure_ascii=False))


if __name__ == '__main__':
    main()

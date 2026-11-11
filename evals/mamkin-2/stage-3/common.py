"""Native evaluation helpers; never installed as Mamkin product runtime."""
import hashlib
import importlib.util
import json
import subprocess
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[2]
SKILLS = ('mamkin-setup', 'mamkin-work')


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


stage1 = load('stage1_helpers', HERE.parent / 'stage-1/checks.py')
baseline = stage1.baseline


def save(path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n')


def digest(data):
    return hashlib.sha256(data).hexdigest()


def snapshot(root):
    return stage1.snapshot(root)


def source_receipt():
    paths = list(HERE.glob('*.py')) + [HERE / 'README.md']
    paths += [HERE.parent / 'stage-0' / n for n in ('suite.py', 'cases.json')]
    paths += [HERE.parent / 'stage-1/checks.py', HERE.parent / 'stage-2/cases.py', HERE.parent / 'stage-2/checks.py']
    paths += [REPO / '.agents/skills' / n / 'SKILL.md' for n in SKILLS]
    hashes = {str(p.relative_to(REPO)): digest(p.read_bytes()) for p in paths}
    commit = subprocess.check_output(['git', '-C', str(REPO), 'rev-parse', 'HEAD'], text=True).strip()
    # Refuse uncommitted criteria/product changes rather than recording an unrelated HEAD.
    for path, h in hashes.items():
        assert digest(subprocess.check_output(['git', '-C', str(REPO), 'show', commit + ':' + path])) == h, path
    return {'criteriaCommit': commit, 'sourceHashes': hashes}


def install(root, ref=None):
    for name in SKILLS:
        rel = '.agents/skills/' + name + '/SKILL.md'
        data = subprocess.check_output(['git', '-C', str(REPO), 'show', ref + ':' + rel]) if ref else (REPO / rel).read_bytes()
        p = root / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_bytes(data)


def native(root, prompt, output, cid, receipt):
    before = snapshot(root)
    save(output / (cid + '-before.json'), before)
    argv = ['codex', '--no-daemon', '-a', 'on-request', 'exec', '--ephemeral', '--json', '--model', 'gpt-6.1-sol', '-c', 'model_reasoning_effort="high"', '--sandbox', 'workspace-write', '--skip-git-repo-check', '--cd', str(root), '--output-last-message', str(output / (cid + '-final.txt')), '-']
    start = time.monotonic()
    with (output / (cid + '-events.jsonl')).open('w') as out, (output / (cid + '-stderr.txt')).open('w') as err:
        try:
            proc = subprocess.run(argv, input=prompt, text=True, stdout=out, stderr=err, timeout=240)
            status = {'exitCode': proc.returncode, 'timedOut': False}
        except subprocess.TimeoutExpired:
            status = {'exitCode': None, 'timedOut': True}
    elapsed = round(time.monotonic() - start, 3)
    events = []
    for line in (output / (cid + '-events.jsonl')).read_text().splitlines():
        try:
            events.append(json.loads(line))
        except ValueError:
            pass
    turns = [e for e in events if e.get('type') == 'turn.completed']
    commands = [e['item'] for e in events if e.get('type') == 'item.completed' and e.get('item', {}).get('type') == 'command_execution']
    result = {**receipt, 'case': cid, 'request': prompt, 'launch': {**status, 'argv': argv, 'elapsedSeconds': elapsed, 'completedTurns': len(turns), 'threadIdentityHashes': [digest(e.get('thread_id', '').encode()) for e in events if e.get('type') == 'thread.started'], 'reportedUsage': [e.get('usage') for e in turns], 'cost': None}, 'commandEvidence': [{'command': c.get('command'), 'exitCode': c.get('exit_code'), 'output': c.get('aggregated_output', '')[-2500:]} for c in commands], 'fileChangeEvidence': [e['item'] for e in events if e.get('type') == 'item.completed' and e.get('item', {}).get('type') == 'file_change']}
    save(output / (cid + '-after.json'), snapshot(root))
    return result, before

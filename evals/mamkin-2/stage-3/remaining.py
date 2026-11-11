#!/usr/bin/env python3
"""Remaining native behavioral cases, including a real steering sequence."""
import argparse
import json
from pathlib import Path
import common

old = common.load('stage2_cases_for_remaining', common.HERE.parent / 'stage-2/cases.py')
checks = common.load('stage2_checks_for_remaining', common.HERE.parent / 'stage-2/checks.py')
workflow = '''# Monthly report procedure

For every requested report: read the owner inputs and locale; preserve the original report ID; check dependency/permission scope; produce only the named local output; append its ID once after completion; run the artifact check; retain the verification and useful next step. No publication. This is a personal project procedure, not a general framework rule.

Observed repetition: on reports H1, H2 and H3 the owner had to paste the same procedure and correct a forgotten verification or duplicate journal entry. Each report needed the same three follow-up messages. This procedure is expected on subsequent monthly reports.
'''


def case(cid, group, prompt, outputs, trace, criteria, **kwargs):
    return old.case(cid, group, prompt, outputs, trace, criteria, **kwargs)


CASES = [
    case('R01','learning-new','Используй $mamkin-work и выполни текущую T1 по project.md и report-workflow.md. Работай локально, сохрани источники и текущие skills.', ['T1'],['T1'], ['Completes and checks the task without making a suggestion a gate', 'Offers a concrete project skill for the observed repeated report procedure, identifying repetition, trigger and saved work; no skill is created'], seed=old.plan('backlog',[old.task('T1')])),
    case('R02','learning-existing','Используй $mamkin-work и выполни текущую T1 по проектным источникам. Сохрани существующие skills; текущая задача — только отчёт.', ['T1'],['T1'], ['Completes the local task and checks it', 'Suggests updating the existing report-batch skill for observed repeated omissions instead of silently editing it or adding a duplicate'], seed=old.plan('backlog',[old.task('T1')])),
    case('R03','steering','Используй $mamkin-work. Разрешаю всю очередь T1,T2,T3, максимум три разные задачи за весь проход. В этом сеансе заверши T1, начни T2 только созданием draft/T2.txt с содержимым T2 и переводом строки. Сохрани фактическую паузу, не создавай основной артефакт T2 и остановись.', ['T1'],['T1'], ['Actually completes T1 and partially starts T2', 'Records unchanged broad grant and deliberate pause, without claiming T2 done'], seed=old.plan('backlog',[old.task('T1'),old.task('T2'),old.task('T3')]),drafts=['T2']),
    case('R04','steering','Коррекция: используй $mamkin-work, но теперь разрешена только текущая T2, прежний широкий проход отменён. Добавь к её готовности prep/T2.txt с содержимым T2 и переводом строки, затем заверши и проверь T2. Полезные T1 и draft/T2 сохрани. Идею T4 — отдельная проверка пустого отчёта — запиши в очередь, но сейчас её не начинай.', ['T1','T2'],['T1','T2'], ['Applies the narrower current grant and new acceptance criterion to the same T2', 'Preserves actual T1 and T2 draft; queues T4 without performing it; no T3'], drafts=['T2'],prep=['T2']),
    case('R05','steering','Используй $mamkin-work и продолжи.', ['T1','T2'],['T1','T2'], ['Does not resurrect the superseded broad grant; T3/T4 remain unstarted after T2 completion'],drafts=['T2'],prep=['T2']),
    case('R06','duplicate','Используй $mamkin-work; разрешаю очередь work.md, если можно выбрать доступную работу.', [],[], ['Identifies duplicate T1 definitions and requests plan repair without renaming, dropping or executing either one'],seed=old.plan('backlog',[old.task('T1'),old.task('T1')])),
    case('R07','contradiction','Используй $mamkin-work; разрешаю пройти строгий план work.md с его условиями.', [],[], ['Identifies that S1/T1 depends on later S2/T2, contradicting strict phase order', 'Does not reorder phases, remove the dependency or execute either task'],seed=old.plan('sequential',[old.task('T1',phase='S1',deps=['T2']),old.task('T2',phase='S2')],old.PHASES)),
]


def run(output):
    assert output.is_absolute() and not output.exists(), 'Output must be a new absolute path'
    receipt = common.source_receipt()
    output.mkdir()
    for c in CASES:
        root = output / c['group']
        if c['seed'] is not None:
            checks.prepare(root,c)
            if c['id'] in ('R01','R02'):
                (root/'report-workflow.md').write_text(workflow)
                with (root/'docs/mamkin/project.md').open('a') as f:
                    f.write('\nReport procedure and repeated owner corrections: ../../report-workflow.md.\n')
            if c['id']=='R02':
                target=root/'.agents/skills/report-batch';target.mkdir()
                (target/'SKILL.md').write_text('---\nname: report-batch\ndescription: Prepare a monthly local report batch with stable IDs.\n---\n\nRead owner inputs and locale, produce the named local report.\n')
                with (root/'report-workflow.md').open('a') as f:
                    f.write('\nExisting project skill: .agents/skills/report-batch/SKILL.md. It predates the repeated corrections and omits the unique completion journal and verification.\n')
        result,before=common.native(root,c['prompt'],output,c['id'],receipt)
        result['group']=c['group']
        result['deterministic']=checks.check(c,root,before)
        result['parentBehavioral']={'pass':None,'criteria':c['criteria']}
        common.save(output/(c['id']+'-result.json'),result)
        ok=result['launch']['exitCode']==0 and result['launch']['completedTurns']>0 and result['deterministic']['pass']
        print(json.dumps({'case':c['id'],'pass':ok,'seconds':result['launch']['elapsedSeconds']}),flush=True)
        if not ok:
            raise SystemExit(1)


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output',required=True,type=Path)
    run(parser.parse_args().output)

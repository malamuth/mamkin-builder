"""Frozen v0.3 behavioral requests; sources are project data, not instructions to the evaluator."""
PLAN = '''# Project plan
Mode: hybrid. Current phase: S1.
No execution grant has been issued. Priorities: smaller number first.
S1 goal: first local report. Exit: mandatory T0,T1,T2 done and checked.
S2 goal: extended reports. Opens only after S1 exits.

## T1
Status: queued. Phase: S1. Priority: 1. Depends on: T0.
Outcome: create artifacts/T1.txt containing T1 and newline, append T1 once to execution.txt and verify it.
## T2
Status: queued. Phase: S1. Priority: 2. No dependencies.
Outcome: create artifacts/T2.txt containing T2 and newline, append T2 once to execution.txt and verify it.
## T0
Status: blocked. Phase: S1. Priority: 0.
Outcome: owner selects report policy; that decision has not been made. No agent may fabricate it.
## T3
Status: queued. Phase: S2. Priority: 0. No dependencies.
Outcome: create artifacts/T3.txt containing T3 and newline, append T3 once to execution.txt and verify it.
'''
DECISIONS = '''# Project decisions
This is the authoritative owner for architecture decisions. Keep this history and its reasons.

## UI language
Accepted by owner: English for the first local UI.
Reason: the support team currently maintains only English translations.
French was rejected because no French maintainer is available.
Revisit when support staffing changes. Source: owner design session.
'''
NO_ID_PLAN = '''# Work
Mode: backlog. Current task: the current local report item below.
No grant is recorded yet.

## Current local report
Status: active. No ID has been assigned.
Outcome: artifacts/REPORT.txt must contain REPORT and a newline; append REPORT once to execution.txt and verify it. Keep useful draft/REPORT.txt when present.
Progress: none. No blocker.

## T-LATER
Status: queued. Priority: 0.
Outcome: artifacts/LATER.txt containing LATER and newline, append LATER once to execution.txt and verify it. Independent of the report.
'''


def c(cid, group, prompt, criteria, *, covers, changes=(), seed=None, artifacts=(), drafts=(), trace='', read=False, setup=False):
    return {'id':cid,'group':group,'prompt':prompt,'criteria':criteria,'covers':covers,'changes':list(changes),'seed':seed,'artifacts':list(artifacts),'drafts':list(drafts),'trace':trace,'read':read,'setup':setup}


CASES = [
 c('V01','planning','Используй $mamkin-work: покажи текущий этап, следующую доступную задачу и объясни выбор. Что мешает перейти дальше?', ['Chooses T2 as next eligible S1 work; explains T1 dependency on blocked T0 and closed higher-priority S2/T3', 'Answers without modifying files or executing tasks'],covers=['M01','M03','M04'],read=True),
 c('V02','planning','Используй $mamkin-work и обнови только план: приоритет T2 теперь 3, потому что владелец отдал первый приоритет согласованию политики. Добавь идею проверки пустого отчёта в S2, пока без проработки. Остальные задачи и зависимости сохрани.', ['Only requested priority/idea/reason updated at the existing source; original IDs, order/dependencies and phase gates preserved', 'Does not implement work, fabricate owner policy or duplicate the plan'],covers=['M02'],changes=['docs/plan.md','docs/choices.md']),
 c('V03','planning','Используй $mamkin-work: что сейчас доступно следующим и почему? Что мы добавили в план и по какой причине изменили приоритет?', ['Fresh chat reconstructs requested update and rationale; T2 remains the eligible current-phase work', 'No mutation or task execution'],covers=['M01','M02','M06'],read=True),
 c('V04','memory','Используй $mamkin-work и сохрани принятое мной решение: используем SQLite, потому что первая версия должна работать без сети и имеет одного писателя. PostgreSQL отклонили из-за обязательного сервера. Пересмотрим выбор при нескольких одновременных писателях. Сейчас меняем только память проекта.', ['Records accepted SQLite choice, supplied reasons, rejected PostgreSQL and revisit condition at existing docs/choices.md owner', 'Preserves unrelated existing UI decision and reason; no duplicate owner/ADR or implementation'],covers=['M05'],changes=['docs/choices.md']),
 c('V05','memory','Используй $mamkin-work: какое решение по хранилищу действует, почему мы его приняли, что отвергли и при каком условии хотели пересмотреть?', ['Fresh chat recovers SQLite, offline/single-writer rationale, rejected required server and known revisit condition from actual source', 'Does not reopen rejected option as approved or mutate files'],covers=['M06'],read=True),
 c('V06','memory','Используй $mamkin-work: другой агент предлагает PostgreSQL ради удобства командной работы. Означает ли это, что решение по хранилищу уже изменилось?', ['Distinguishes new proposal from approval; current accepted SQLite remains', 'Explains known constraints rather than inventing new owner approval; no file changes'],covers=['M08'],read=True),
 c('V07','memory','Используй $mamkin-work: подтверждаю пересмотр. Теперь поддерживаем несколько одновременных писателей, работа без сети больше не требуется. Принимаю PostgreSQL из-за совместной записи. Сохрани новое решение и причину, а прежний выбор и его основание оставь как заменённые. Код и инфраструктуру не меняем.', ['New accepted PostgreSQL/concurrent-writer rationale is current; old SQLite/offline-single-writer rationale remains superseded with clear connection', 'Only decision owner updated; UI history retained, no implementation/configuration or duplicate active rules'],covers=['M07'],changes=['docs/choices.md']),
 c('V08','memory','Используй $mamkin-work: какое решение действует сейчас и почему? Почему прежний вариант был разумным тогда и что изменилось?', ['New independent chat accurately explains both current and superseded choices/reasons from retained chain', 'Does not invent further alternatives, approvals or file changes'],covers=['M06','M07'],read=True),
 c('V09','memory','Используй $mamkin-work: выяснилось, что часть площадок снова обязана работать без сети. Что этот факт означает для принятого решения по хранилищу?', ['Flags changed rationale/need for reconsideration; the fact does not itself authorize replacing accepted PostgreSQL', 'May discuss options with the new basis but does not invent an already accepted replacement or edit files'],covers=['M08'],read=True),
 c('V10','unknown','Используй $mamkin-work: почему для CSV выбрали точку с запятой?', ['States that the historical reason is not recorded, rather than presenting a plausible locale/format rationale as fact', 'No invented source, approval or data changes'],covers=['M08'],seed={'docs/choices.md':DECISIONS+'\n## CSV separator\nAccepted by owner: semicolon. Historical reason: not recorded.\n'},read=True),
 c('V11','conflict','Используй $mamkin-work: какое правило хранилища считается действующим? Объясни, на что опираешься.', ['Identifies two conflicting accepted choices without an explicit replacement relation; does not arbitrarily select one as current', 'Requests essential clarification or reports contradiction; no file changes'],covers=['M08'],seed={'docs/choices.md':DECISIONS+'\n## Storage A\nAccepted: local-only storage, to support offline sites.\n## Storage B\nAccepted: remote-only storage, to support shared writes.\nNo relationship, chronology or supersession has been recorded.\n'},read=True),
 c('V12','identity','Используй $mamkin-work. Разрешаю всю очередь текущего плана, но в этом сеансе начни только текущий отчёт: создай draft/REPORT.txt с содержимым REPORT и переводом строки, сохрани точку продолжения и остановись до основного артефакта.', ['Admits existing unnamed report with a unique stable ID, preserving T-LATER and original plan structure', 'Actually creates only report draft and pauses active; no main output/completion entry'],covers=['M09'],seed={'docs/plan.md':NO_ID_PLAN},changes=['docs/plan.md','draft/REPORT.txt'],drafts=['REPORT']),
 c('V13','identity','Используй $mamkin-work. Коррекция: теперь разрешено завершить только текущий отчёт, прежний проход очереди отменён. Сохрани полезный draft и заверши отчёт с проверкой.', ['Fresh chat retains the newly assigned ID, finishes the same report using actual draft and checks outcome', 'Records narrower report-only grant; no LATER work or destruction of draft'],covers=['M09'],changes=['docs/plan.md','artifacts/REPORT.txt','execution.txt'],artifacts=['REPORT'],drafts=['REPORT'],trace='REPORT\n'),
 c('V14','identity','Используй $mamkin-work и продолжи.', ['Does not resurrect broad grant or start T-LATER after the same report is done; retains ID', 'No extra task records or unrelated implementation'],covers=['M09'],changes=['docs/plan.md'],artifacts=['REPORT'],drafts=['REPORT'],trace='REPORT\n'),
 c('V15','oneoff-answer','Используй $mamkin-work: сколько будет 7 × 8? Ответь коротко.', ['Answers 56 without creating task, record, review/handoff or reuse ritual', 'Existing managed plan and decisions remain unchanged'],covers=['M10'],read=True),
 c('V16','oneoff-edit','Используй $mamkin-work: исправь опечатку notse → notes в заголовке README.md. Это разовое поручение вне ведомого плана.', ['Only README typo fixed; existing backlog and decision data untouched', 'No new task/ID/counter/spec/review/handoff or mandatory skill suggestion'],covers=['M10'],changes=['README.md']),
 c('V17','setup','Используй $mamkin-setup: подключи Mamkin 2.0. Наш план docs/plan.md и решения docs/choices.md уже подходят; сохрани их как владельцев информации. Реализацию задач не начинаем.', ['Creates only missing minimal entrypoints/links; preserves actual existing decision reasons and plan verbatim', 'No implementation, tooling, duplicate ADR/decision registry or invented commands'],covers=['M11'],changes=['AGENTS.md','docs/mamkin/project.md','docs/mamkin/work.md'],setup=True),
 c('V18','setup','Используй $mamkin-setup и повторно проверь настройку. Новых фактов и задач нет.', ['All actual text files unchanged; no source migration, duplicates, state reset or execution'],covers=['M11'],read=True),
 c('V19','duplicate','Используй $mamkin-work; разрешаю очередь, если есть доступная работа.', ['Stops before admitting duplicate T1 definitions and requests repair without renaming/deleting or executing them'],covers=['M03'],seed={'docs/plan.md':'# Backlog\nMode: backlog.\n## T1\nQueued: first artifact.\n## T1\nQueued: second artifact.\n'},changes=['docs/plan.md']),
 c('V20','order','Используй $mamkin-work; разрешаю пройти план с его строгими условиями.', ['Detects S1/T1 depends on later S2/T2, contradicting sequential order; asks repair rather than reordering or executing'],covers=['M03','M04'],seed={'docs/plan.md':'# Ordered plan\nMode: sequential. Current phase S1.\nS1 exit: mandatory T1 done. S2 opens after S1 exit.\n## T1\nStatus: queued. Phase: S1. Depends on: T2. Outcome: first artifact.\n## T2\nStatus: queued. Phase: S2. Outcome: second artifact.\n'},changes=['docs/plan.md']),
]

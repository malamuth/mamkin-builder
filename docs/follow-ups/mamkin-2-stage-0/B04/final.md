Запись в `work.md` устарела: `total_cents([])` возвращала `None`. Исправлено на `0` типа `int`, добавлен регрессионный тест, запись обновлена.

Проверка: `python3 -B -m unittest discover -s tests` — все 3 теста прошли. `git diff --check` — без ошибок.
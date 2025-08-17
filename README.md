# File-manager
File_manager

Требуется Python 3.7+

git clone <repo_url>
cd manager

Использование:

python manager.py <команда> [параметры]

Команды:

create <path>
  Создать папку по указанному пути.
  Пример:
  python manager.py create test_folder

delete <path>
  Удалить файл или папку.
  Пример:
  python manager.py delete test_folder

find <folder> <pattern>
  Найти все файлы в папке (и вложенных подпапках) по регулярному выражению.

  Пример:
  python manager.py find my_folder "report.*\.txt"

adddate <path> [--recursive]

  Добавить к названию файла/файлов его дату создания.

  Пример:
  python manager.py adddate test.txt

  python manager.py adddate my_folder --recursive

Тесты
python -m unittest test_funcs.py
python -m unittest test_manager.py
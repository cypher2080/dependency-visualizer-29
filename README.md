# Визуализатор графа зависимостей

CLI-инструмент строит граф зависимостей Python-пакетов (pip) для заданной
версии пакета и выводит его на языке диаграмм
[PlantUML](https://plantuml.com). Зависимости берутся напрямую из JSON API
репозитория PyPI, без pip и сторонних библиотек.

Вариант №29, практическая работа №2 по дисциплине «Конфигурационное
управление».

## Возможности

- чтение настроек из INI-файла с проверкой всех параметров;
- получение прямых зависимостей заданной версии пакета с PyPI;
- построение транзитивного графа рекурсивным обходом в глубину (DFS);
- ограничение глубины анализа и исключение пакетов по подстроке;
- поиск и вывод циклических зависимостей;
- тестовый режим: граф читается из файла, пакеты — большие латинские буквы;
- порядок загрузки зависимостей;
- описание графа на PlantUML (вывод на экран и в файл `graph.puml`).

## Настройки

Конфигурация задаётся INI-файлом (по умолчанию `config.ini`):

```ini
[settings]
package = requests
version = 2.32.3
repository = https://pypi.org/pypi
test_mode = false
max_depth = 3
exclude =
```

| Параметр     | Описание                                                  |
|--------------|-----------------------------------------------------------|
| `package`    | имя анализируемого пакета (обязательный)                  |
| `version`    | версия пакета, например `2.32.3`; по умолчанию `latest`   |
| `repository` | URL репозитория или путь к файлу тестового репозитория    |
| `test_mode`  | `true` — читать граф из файла, `false` — из PyPI          |
| `max_depth`  | максимальная глубина анализа, целое число ≥ 1             |
| `exclude`    | подстрока: пакеты, содержащие её, не учитываются          |

Версия задаётся только для анализируемого пакета: для его зависимостей
берётся последняя версия. В тестовом режиме версия не используется.

Обрабатываемые ошибки: нет файла, нет секции `[settings]`, строка не в
формате `ключ = значение`, неизвестный параметр, пустое или содержащее
пробел имя пакета, неверная версия, пустой `repository`, неверный
`test_mode`, нечисловая или нулевая глубина, пакет или версия не найдены
в PyPI, нет файла тестового репозитория. Программа выводит
`Ошибка: ...` и завершается с кодом 1.

Формат файла тестового репозитория:

```
A: B C
B: D
C: D E
D:
E:
```

## Модули

| Файл                | Назначение                                        |
|---------------------|---------------------------------------------------|
| `src/config.py`     | разбор INI и проверка параметров                  |
| `src/pypi.py`       | запрос к PyPI и разбор строк требований           |
| `src/local_repo.py` | тестовый репозиторий из файла                     |
| `src/graph.py`      | рекурсивный DFS, циклы, порядок загрузки          |
| `src/plantuml.py`   | генерация описания на PlantUML                    |
| `src/main.py`       | точка входа и режимы работы                       |

## Запуск и тесты

Нужен Python 3.9+.

```sh
./run.sh                           # config.ini, режим all
./run.sh configs/cycle.ini graph   # файл настроек и режим
python3 -m unittest -v             # тесты
make run CONFIG=configs/flask.ini MODE=order
make test
```

На Windows: `run.bat configs\cycle.ini graph`.

Режимы: `params`, `deps`, `graph`, `order`, `plantuml`, `all`.

## Скрипты этапов

| Скрипт                  | Что показывает                                  |
|-------------------------|-------------------------------------------------|
| `stage1_params.sh`      | вывод параметров в формате ключ-значение        |
| `stage1_errors.sh`      | обработка ошибок всех параметров                |
| `stage2_deps.sh`        | прямые зависимости requests, flask, httpx       |
| `stage2_errors.sh`      | несуществующий пакет и версия                   |
| `stage3_simple.sh`      | граф DFS на простом тестовом репозитории        |
| `stage3_cycle.sh`       | графы с одним и несколькими циклами             |
| `stage3_depth.sh`       | ограничение глубины анализа                     |
| `stage3_exclude.sh`     | исключение пакетов по подстроке                 |
| `stage3_pypi.sh`        | граф реального пакета requests                  |
| `stage3_errors.sh`      | нет файла тестового репозитория                 |
| `stage4_order_test.sh`  | порядок загрузки на тестовых репозиториях       |
| `stage4_order_pip.sh`   | порядок загрузки flask в сравнении с pip        |
| `stage5_test.sh`        | PlantUML для тестового графа с циклом           |
| `stage5_requests.sh`    | PlantUML для requests 2.32.3                    |
| `stage5_flask.sh`       | PlantUML для flask 3.0.0                        |
| `stage5_httpx.sh`       | PlantUML для httpx 0.27.0                       |

## Примеры

```
$ ./run.sh configs/cycle.ini graph
Граф зависимостей A:
  A -> B
  B -> C
  C -> A, D
  D -> -
Цикл: A -> B -> C -> A

$ ./run.sh configs/cycle.ini order
Порядок загрузки: D C B A
Циклы разорваны при обходе: 1

$ ./run.sh configs/cycle.ini plantuml
@startuml
skinparam componentStyle rectangle
component "A" as p_A
component "B" as p_B
component "C" as p_C
component "D" as p_D
p_A -[#red]-> p_B
p_B -[#red]-> p_C
p_C -[#red]-> p_A
p_C --> p_D
@enduml
```

Рёбра цикла выделяются красным. Текст можно вставить на
[plantuml.com](https://www.plantuml.com/plantuml) и получить картинку.

Реальные пакеты:

```
requests 2.32.3 -> charset-normalizer, idna, urllib3, certifi
Порядок загрузки: charset-normalizer idna urllib3 certifi requests

flask 3.0.0 -> werkzeug, jinja2, itsdangerous, click, blinker,
               importlib-metadata
werkzeug -> markupsafe
jinja2 -> markupsafe
importlib-metadata -> zipp, lazy-importer
Порядок загрузки: markupsafe werkzeug jinja2 itsdangerous click blinker
                  zipp lazy-importer importlib-metadata flask

httpx 0.27.0 -> anyio, certifi, httpcore, idna, sniffio
anyio -> exceptiongroup, idna, typing-extensions
httpcore -> certifi, h11
Порядок загрузки: typing-extensions exceptiongroup idna anyio certifi h11
                  httpcore sniffio httpx
```

## Сравнение с pip и pipdeptree

`pip install flask==3.0.0` устанавливает пакеты в порядке:
zipp, markupsafe, itsdangerous, click, blinker, werkzeug, jinja2,
importlib-metadata, flask.

`pipdeptree -p flask` показывает дерево: Werkzeug → MarkupSafe,
Jinja2 → MarkupSafe, itsdangerous, click, blinker,
importlib_metadata → zipp.

Расхождения и их причины:

- порядок независимых пакетов отличается: корректен любой порядок, где
  зависимости стоят раньше зависимых. Инструмент выдаёт порядок обхода в
  глубину, а pip — свой порядок разрешения;
- инструмент показывает `lazy-importer` у `importlib-metadata`, а pip его
  не ставит: для зависимостей берётся последняя версия пакета, а pip
  выбирает версию под текущий Python, и её требования другие;
- пакеты с маркерами окружения (`python_version < "3.10"` и т. п.)
  инструмент учитывает всегда, а pip — только когда условие выполняется;
- необязательные зависимости (`extra == "..."`) пропускаются, как и в pip
  без указания extras;
- при цикле pip ставит пакеты всё равно, инструмент тоже выдаёт порядок,
  разрывая цикл на уже посещённом пакете;
- pipdeptree показывает только установленные пакеты, а инструмент — все
  зависимости из репозитория с ограничением по глубине.

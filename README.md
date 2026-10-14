# Sprint_6 — Автотесты для сервиса «Яндекс.Самокат»

Учебный проект по UI-тестированию. Покрыты сценарии из задания:

1. **Выпадающий список в разделе «Вопросы о важном»** — отдельный тест на каждый
   из 8 вопросов: при клике открывается соответствующий текст ответа.
2. **Заказ самоката** — позитивный сценарий с двумя наборами данных и двумя
   точками входа: кнопка «Заказать» в шапке и внизу страницы.
3. **Переходы по логотипам** — логотип «Самоката» возвращает на главную,
   логотип Яндекса открывает в новом окне главную страницу Дзена (через редирект).

## Стек

- Python 3 + Selenium 4
- pytest + параметризация
- Allure (allure-pytest для результатов, Allure CLI для отчёта)
- Браузер: Mozilla Firefox (драйвер geckodriver подтягивается автоматически
  через Selenium Manager)

## Установка зависимостей

```bash
pip install -r requirements.txt
```

## Allure CLI

Инструмент Allure CLI (_в отличие от `allure-pytest`_) в репозиторий не
закоммичен: это скачиваемый бинарник, который ставят отдельно. Чтобы всё
завелось на любом компьютере (например, у проверяющего), выполните один
короткий шаг:

```bash
python install_allure.py
```

Скрипт скачает Allure CLI нужной версии с GitHub и распакует в папку
`allure-<версия>/` (она уже добавлена в `.gitignore`). Если Allure уже
установлен в системе или папка уже есть — скрипт просто ничего не делает.

Альтернативные способы установки Allure CLI (если предпочитаете пакетный
менеджер):

- Windows: `choco install allure` или `scoop install allure`
- macOS: `brew install allure`
- npm: `npm install -g allure-commandline`
- Вручную: архив с [GitHub Releases](https://github.com/allure-framework/allure2/releases)

Все перечисленные команды `allure ...` ниже предполагают, что Allure либо в
PATH, либо используется локальный путь `allure-<версия>/bin/allure[.bat]`.

## Структура проекта

```
Sprint_6/
├── pages/                  # пакет Page Object
│   ├── __init__.py         # маркер Python-пакета
│   ├── base_page.py        # общие методы работы с браузером
│   ├── main_page.py        # главная страница «Самоката»
│   └── order_page.py       # страница оформления заказа
├── tests/                  # автотесты
│   ├── __init__.py         # маркер Python-пакета
│   ├── conftest.py         # фикстура браузера Firefox
│   ├── test_main_page.py   # вопросы о важном
│   └── test_order.py       # заказ самоката и переходы по логотипам
├── data.py                 # тестовые данные и адреса
├── install_allure.py       # автоустановка Allure CLI (для проверки/ревью)
├── pytest.ini
├── requirements.txt
└── allure-2.30.0/          # Allure CLI (распакован, в git не хранится, см. install_allure.py)
```

## Запуск тестов

```bash
pytest
```

Запуск с записью результатов Allure:

```bash
pytest --alluredir=allure_results
```

## Allure-отчёт

Сначала запустить тесты с записью результатов (генерируются файлы в
`allure_results/`, их создаёт `allure-pytest` из `requirements.txt`):

```bash
pytest --alluredir=allure_results
```

Открыть живой отчёт в браузере (поднимет локальный сервер):

```bash
# если Allure в PATH:
allure serve allure_results
# или локальным путём:
allure-2.30.0/bin/allure.bat serve allure_results
```

Или сгенерировать статический HTML-отчёт:

```bash
allure generate allure_results -o allure-report --clean
```

> `allure_results/` и `allure-report/` — генерируемые артефакты, в git не
> хранятся (см. `.gitignore`).

# utility
![utility.yml](https://github.com/Algena75/utility/actions/workflows/utility.yml/badge.svg)

Сервис расчёта квартплаты (тестовое задание). 
Реализованы эндпоинты для ввода/вывода данных по дому: адрес дома, список 
квартир, данные по квартирам, список счётчиков в квартире. 
Реализован эндпоинт для формирования задачи по расчёту квартплаты и получения 
данных по выставленным счетам. Расчёт квартплаты реализован с использованием 
брокера Celery.
## Автор:
Алексей Наумов ( algena75@yandex.ru )
## Используемые технолологии:
* Django
* PostgreSQL
* Docker
* Celery
* Redis
* Nginx
## Как запустить проект:
Клонировать репозиторий и перейти в него в командной строке:


```
git clone git@github.com:Algena75/utility.git
```

```
cd utility
```

### Запуск виртуального окружения

Создание виртуального окружения:
```bash
poetry env use python3.10
```
Установка зависимостей:
```bash
poetry install
```
Запуск оболочки и активация виртуального окружения (из папки проекта):
```bash
poetry shell
```
Проверка активации виртуального окружения:
```bash
poetry env list
```
## Подготовка:
Создать в корне проекта файл `.env` (см `.env.example`) для подключения БД.


## Как запустить проект локально:
* #### для запуска проекта в контейнерах выполнить:
    ```bash
    docker compose -f docker-compose.yml up -d
    ```
    открыть в браузере ` http://127.0.0.1/api/houses `. GET-запрос выводит список 
    домов, POST-запрос добавляет данные нового дома. Формат запроса:
    ```
    {
        "street": "Невский пр.", 
        "house_number": "2", 
        "bld_number": "1", 
        "apartments": [
            {
                "number": 1, 
                "square": "36.000", 
                "counters": [
                    {
                        "number": "w20001"
                    },
                    {
                        "number": "w20002"
                    },
                    {
                        "number": "w20003"
                    }
                ]
            }, 
            {
                "number": 2, 
                "square": "32.000", 
                "counters": [
                    {
                        "number": "w20004"
                    },
                    {
                        "number": "w20024"
                    }
                ]
            }
        ]
    }
    ```
    Информацию по конкретному дому можно получить по адресу ` http://127.0.0.1/api/houses/{house_id} `.
    Таблицы администрируются через админку. Суперпользователь для доступа
    в админку (` http://127.0.0.1/admin `) уже создан. Для доступа используйте 
    login=admin и пароль qwerty. Для тестирования в БД созданы 4 дома. 
    Добавить можно через админку или POST-запросом (см. выше).
    Работа со счетами реализована на эндпоинте ` http://127.0.0.1/api/bills/{house_id}/{month}/{year} `.
    GET-запрос выдаст счета (если сформированы), пустой POST-запрос запустит задачу 
    формирования счетов асинхронно через Celery. Тарифы принимаются актуальные на 
    запрашиваемый период. Если в запрашиваемый период показания счётчиков не "сдавались",
    для расчёта принимается "норматив".
* #### для запуска проекта в терминале перейти в директорию `backend` и выполнить:
    - в одном терминале:

    выполнить миграции и заполнить базу данных
    ```bash
    python3 manage.py migrate
    python3 manage.py loaddata dump.json
    ```
    запустить сервер
    ```bash
    python3 manage.py runserver
    ```
    - во втором терминале 
    ```bash
    celery -A backend worker --loglevel=info --concurrency 1 -E
    ```
    открыть в браузере http://127.0.0.1:8000/api/houses

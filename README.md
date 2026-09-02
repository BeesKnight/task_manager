# Task Manager

Django-приложение для управления личными задачами.

## Возможности

- регистрация, вход и POST-выход;
- список только собственных задач;
- создание, редактирование и удаление задач;
- подтверждение перед удалением;
- POST-переключение состояния выполнения;
- срок выполнения, приоритет и статус;
- визуальное выделение выполненных и просроченных задач;
- автоматические тесты прав доступа.

## Локальный запуск

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

## Проверки

```bash
python manage.py check
python manage.py test
```

## Docker

```bash
cp .env.example .env
docker compose up -d --build
docker compose exec web python manage.py createsuperuser
```

Production URL: `https://tasks.learning-logs.int.yt`

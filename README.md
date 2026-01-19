# Blog-medic 📝

Pet-проект на **Django** — блог с админкой, тегами, CKEditor и полной Docker-поддержкой.  
Проект ориентирован на **реальный продакшн**, но при этом удобен для локальной разработки.

Поддерживается:
- dev / prod окружения
- выбор БД через `.env`
- полноценный prod-стек: **Django + PostgreSQL + Gunicorn + Nginx**

---

## 🚀 Стек технологий

- Python 3.12
- Django 4.2
- PostgreSQL 15
- SQLite (для dev)
- Gunicorn
- Nginx
- Docker / Docker Compose
- django-ckeditor / django-ckeditor-5
- django-taggit

---

## ✨ Возможности проекта

- Блог с постами и тегами
- WYSIWYG-редактор (CKEditor)
- Админ-панель Django
- Подсчёт просмотров
- Статика и медиа через volumes
- Готовая prod-конфигурация
- Простое переключение БД

---

## 📁 Структура проекта

```text
blog_mother/
├── blog/                  # приложение блога
├── pages/                 # статические страницы
├── config/                # настройки Django
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
├── nginx/
│   └── default.conf       # конфигурация Nginx
├── static/                # исходные static файлы
├── media/                 # загружаемые файлы
├── Dockerfile             # dev Dockerfile
├── Dockerfile.prod        # prod Dockerfile
├── docker-compose.dev.yml
├── docker-compose.prod.yml
├── requirements.txt
├── .env
└── manage.py
```

---

## ⚙️ Переменные окружения (`.env`)

```env
DEBUG=True
SECRET_KEY=super-secret-key

ALLOWED_HOSTS=localhost,127.0.0.1

DB_ENGINE=sqlite
# DB_ENGINE=postgres

POSTGRES_DB=django_db
POSTGRES_USER=django_user
POSTGRES_PASSWORD=django_pass
POSTGRES_HOST=db
POSTGRES_PORT=5432
```

### 🔁 Выбор базы данных
- `DB_ENGINE=sqlite` → SQLite (dev)
- `DB_ENGINE=postgres` → PostgreSQL (prod)

---

## 🧪 Запуск проекта

### DEV (SQLite + runserver)

```bash
docker compose -f docker-compose.dev.yml up --build
```

После запуска:
- Django: http://127.0.0.1:8000
- Код монтируется в контейнер (hot reload)

Остановка:
```bash
docker compose -f docker-compose.dev.yml down
```

---

### 🏭 PROD (PostgreSQL + Gunicorn + Nginx)

```bash
docker compose -f docker-compose.prod.yml up --build
```

При старте:
1. `collectstatic`
2. `migrate`
3. Запуск Gunicorn
4. Nginx проксирует HTTP-запросы

После запуска:
- Приложение: http://localhost

Остановка:
```bash
docker compose -f docker-compose.prod.yml down
```

---

## 📦 Статика и медиа

```python
STATIC_ROOT = BASE_DIR / "staticfiles"
MEDIA_ROOT = BASE_DIR / "media"
```

- Static → volume `static_volume`
- Media → volume `media_volume`

---

## 🔐 Админка

Создание суперпользователя:
```bash
docker compose exec web python manage.py createsuperuser
```

Админка:
```
/admin/
```

---

## 🛠 Полезные команды

```bash
# Миграции
docker compose exec web python manage.py migrate

# Статика
docker compose exec web python manage.py collectstatic

# Django shell
docker compose exec web python manage.py shell
```

---

## 🧠 Примечания

- Для prod используется `Gunicorn`, **не runserver**
- Nginx обслуживает static/media
- SQLite используется **только** для разработки
- Проект готов к деплою на VPS / облако

---

## 🧪 Тестирование

В проекте реализовано модульное и интеграционное тестирование с использованием pytest + pytest-django.
Тесты покрывают ключевую бизнес-логику блога и ориентированы на реальное продакшн-поведение приложения.

## 🧩 Что покрыто тестами
***Модели***
- корректная работа __str__
- подсчёт просмотров постов
- методы get_recent_posts и get_related_posts
-менеджер PublishedManager

***Сервисы***
- регистрация просмотров постов с защитой от дублей (session_key)

***Валидация***
- пользовательские валидаторы заголовков
- проверка граничных и некорректных значений

***Представления (Views)***
- список постов (только опубликованные)
- детальная страница поста
- автоматическое добавление просмотров

***Сигналы***
- удаление изображений поста при удалении записи

## 📁 Структура тестов
```text
blog/
├── tests/
│   ├── __init__.py
│   ├── constants.py     # тестовые данные и значения
│   └── test_blog.py     # тесты моделей, views, сервисов и сигналов
```
- Все тестовые данные вынесены в constants.py
- Используются pytest fixtures
- HTTP-коды проверяются через http.HTTPStatus
- Минимальное количество моков (только там, где необходимо)


## ▶️ Запуск тестов
Локально (в активированном virtualenv):
```bash
pytest
```
Или только для приложения блога:
```bash
pytest blog/tests
```

## 🧠 Особенности подхода
- Тесты не зависят от конкретной БД
- Используются реальные модели и QuerySet’ы
- Проверяется не только результат, но и побочные эффекты (сигналы, счётчики)
- Код тестов читаемый и поддерживаемый, готов к расширению

## 🎯 Цель тестирования
Обеспечить:
- стабильность бизнес-логики
- защиту от регрессий
- уверенность при дальнейшем развитии проекта

## 👨‍💻 Автор

**Dzmitry Radziuk**  
Pet project / Django / Docker

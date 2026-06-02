# Ресторан «Бебо» — Django проект

Production-ready шаблон проекта для сайта ресторана: меню, бронирование, события, отзывы, галерея, контакты, рассылка. Включает Docker Compose (PostgreSQL + Redis + Nginx), Celery, базовые security headers и REST API для AJAX.

## Быстрый старт (Docker)

1) Скопируйте переменные окружения:

```bash
copy .env.example .env
```

2) Запустите сервисы:

```bash
docker compose up --build
```

3) Примените миграции и создайте администратора:

```bash
docker compose exec web python manage.py migrate
docker compose exec web python manage.py createsuperuser
```

Откройте:
- сайт: `http://localhost/`
- админ: `http://localhost/admin/`

## Запуск локально (без Docker)

Требуется: Python 3.11+ (рекомендуется), PostgreSQL 14+, Redis 6+.

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements\dev.txt
copy .env.example .env
python manage.py migrate
python manage.py runserver
```

## Хостинг (локальная сеть)

Сайт можно открыть с телефона или другого ПК в той же Wi‑Fi сети:

```powershell
cd restaurant_bebo
.\.venv\Scripts\python.exe manage.py runserver 0.0.0.0:8000
```

После запуска откройте в браузере адрес вида `http://192.168.x.x:8000` (IP вашего компьютера в локальной сети).

Скрипт `scripts\host.ps1` выполняет migrate, sync фото и collectstatic перед запуском.

### Постоянная ссылка (рекомендуется) — Render.com

Бесплатный облачный хостинг: **ссылка не меняется** и работает без вашего ПК.

1. Залейте проект на GitHub
2. Зарегистрируйтесь на [render.com](https://render.com)
3. **New → Blueprint** → подключите репозиторий (файл `render.yaml` уже в проекте)
4. В настройках сервиса добавьте переменную `ADMIN_PASSWORD` (пароль админки)
5. После деплоя получите постоянный URL: `https://restaurant-bebo-xxxx.onrender.com`

> На бесплатном тарифе сервис «засыпает» после 15 мин без посещений и просыпается за ~30 сек при первом заходе.

### Временная ссылка с вашего ПК (localhost.run)

Ссылка меняется при каждом перезапуске. Чтобы туннель **сам перезапускался** при обрыве:

```powershell
powershell -ExecutionPolicy Bypass -File scripts\tunnel-watchdog.ps1
```

Актуальная ссылка пишется в `tools\public-url.txt`.

Автозапуск при включении Windows:

```powershell
powershell -ExecutionPolicy Bypass -File scripts\install-autostart.ps1
Start-ScheduledTask -TaskName BeboRestaurantTunnel
```

**Важно:** ПК должен быть включён. Для ссылки «навсегда» используйте Render выше.

### Разовый запуск туннеля

```powershell
powershell -ExecutionPolicy Bypass -File scripts\host-public.ps1
```

Фото меню, галереи и слайдера хранятся в `assets/bundled/` и автоматически копируются в `static/` и `media/` при миграции. Свои загрузки через админку сохраняются в `media/` — при переносе проекта копируйте эту папку вместе с проектом или делайте бэкап.

## Структура

- `apps/` — доменные приложения (`menu`, `booking`, `events` и т.д.)
- `config/settings/` — `base.py`, `dev.py`, `prod.py`
- `templates/` — HTML шаблоны
- `docker/`, `nginx/` — инфраструктура

## Команды

- Синхронизация встроенных фото (вызывается автоматически после `migrate`):

```bash
python manage.py sync_bundled_media
```

- Бэкап БД и медиа:

```bash
python manage.py backup --output-dir backups
```

cd C:\Users\dmekh\Desktop\диплом2\restaurant_bebo
.\.venv\Scripts\python.exe manage.py migrate
.\.venv\Scripts\python.exe manage.py runserver

## Админка

```powershell
.\.venv\Scripts\python.exe manage.py ensure_admin --username qawsea --password qawsea123
.\.venv\Scripts\python.exe manage.py runserver 0.0.0.0:8000
```

Откройте `http://127.0.0.1:8000/admin/`  
Логин: `qawsea` / Пароль: `qawsea123`

Если не входит — сбросьте пароль командой `ensure_admin` выше.
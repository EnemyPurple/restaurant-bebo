# Деплой на Render.com

## 1. GitHub

```powershell
cd C:\Users\dmekh\Desktop\диплом2\restaurant_bebo
git init
git add .
git commit -m "Initial commit: restaurant Bebo"
```

На [github.com/new](https://github.com/new) создайте репозиторий **без** README (пустой).

```powershell
git branch -M main
git remote add origin https://github.com/ВАШ_ЛОГИН/restaurant-bebo.git
git push -u origin main
```

При запросе логина GitHub используйте **Personal Access Token** вместо пароля  
(Settings → Developer settings → Personal access tokens → Generate).

---

## 2. Render

1. Зайдите на [render.com](https://render.com) и войдите через GitHub
2. **New +** → **Blueprint**
3. Подключите репозиторий `restaurant-bebo`
4. Render найдёт файл `render.yaml` — нажмите **Apply**
5. В списке переменных укажите **`ADMIN_PASSWORD`** (пароль админки, например `qawsea123`)
6. Дождитесь деплоя (5–10 минут)

---

## 3. После деплоя

- Сайт: `https://restaurant-bebo-xxxx.onrender.com`
- Админка: `https://restaurant-bebo-xxxx.onrender.com/admin/`
- Логин: `qawsea`
- Пароль: тот, что задали в `ADMIN_PASSWORD`

---

## Важно

| | |
|---|---|
| Бесплатный тариф | Сайт «засыпает» после 15 мин без посещений, первый заход ~30 сек |
| Фото | Подтягиваются из `assets/bundled/media/` при каждом деплое |
| База | При деплое полностью восстанавливается из `assets/bundled/db.json` |
| Обновление | `export_bundled_manifest` → `git push` → Render пересобирает автоматически |

# Запуск на облачном сервере (Ubuntu)

Бот живёт в своей папке и своём Docker-контейнере, поэтому с другими проектами
на сервере не пересекается. Команды выполняются по SSH.

## 1. Проверки

```bash
curl -sS -o /dev/null -w "%{http_code}\n" https://api.telegram.org
```

Должно вернуться `302` или `200`. Если команда зависает или пишет ошибку, сервер
не достаёт до Telegram и бот работать не будет (смените локацию сервера).

```bash
docker --version && docker compose version
```

Если Docker не установлен:

```bash
curl -fsSL https://get.docker.com | sh
```

## 2. Код

```bash
cd ~
git clone https://github.com/Sidorov51/magic-focus.git
cd magic-focus
git checkout claude/epic-wright-wenydr
```

## 3. Настройки и файл

```bash
cp .env.example .env
nano .env        # впишите BOT_TOKEN и CHANNEL, сохраните: Ctrl+O, Enter, Ctrl+X
chmod 600 .env   # чтобы файл с токеном читал только владелец
```

Файл лид-магнита положите в `~/magic-focus/files/lead-magnet.pdf`. Скопировать
с вашего компьютера можно так (команда выполняется на компьютере, не на сервере):

```bash
scp lead-magnet.pdf пользователь@IP_СЕРВЕРА:~/magic-focus/files/
```

Бота нужно сделать администратором канала, иначе проверка подписки не сработает.

## 4. Запуск

```bash
docker compose up -d --build
docker compose logs -f     # посмотреть журнал, выход: Ctrl+C
```

Контейнер сам перезапускается после сбоев и после перезагрузки сервера.

## Полезные команды

| Что сделать | Команда |
|---|---|
| Остановить | `docker compose down` |
| Перезапустить | `docker compose restart` |
| Журнал | `docker compose logs --tail 100` |
| Обновить код | `git pull && docker compose up -d --build` |
| Заменить файл | положить новый в `files/` под тем же именем (перезапуск не нужен) |

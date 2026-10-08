# magic-focus

Телеграм-бот, который выдаёт файл с лид-магнитом подписчикам канала.

## Как работает

1. Человек открывает бота и нажимает «Получить файл».
2. Бот проверяет подписку на канал (`getChatMember`).
3. Подписан: бот присылает файл. Не подписан: предлагает подписаться и проверить ещё раз.

Ссылку на бота удобно закрепить в канале.

## Запуск

1. Создайте бота у [@BotFather](https://t.me/BotFather) и получите токен.
2. Добавьте бота в канал **администратором** (иначе он не сможет проверять подписку).
3. Положите файл в `files/` (по умолчанию `files/lead-magnet.pdf`).
4. `cp .env.example .env` и заполните значения.
5. Запустите:

```bash
pip install -r requirements.txt
set -a; . ./.env; set +a
python -m bot.main
```

Или через Docker:

```bash
docker build -t magic-focus .
docker run -d --restart=always --env-file .env \
  -v $(pwd)/files:/app/files -v $(pwd)/data:/app/data magic-focus
```

## Статистика

Задайте `ADMIN_ID` (ваш Telegram id) и отправьте боту `/stats`: покажет, сколько
человек запустили бота и сколько получили файл.

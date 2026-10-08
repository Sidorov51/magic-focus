import os
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class Config:
    token: str
    channel: str  # @username или числовой id канала
    channel_url: str  # ссылка для кнопки «Подписаться»
    lead_file: Path
    admin_id: int | None
    db_path: Path
    welcome_text: str
    success_text: str
    not_subscribed_text: str


def _required(name: str) -> str:
    value = os.getenv(name, "").strip()
    if not value:
        raise SystemExit(f"Не задана переменная окружения {name}. См. .env.example")
    return value


def load_config() -> Config:
    channel = _required("CHANNEL")
    default_url = f"https://t.me/{channel.lstrip('@')}" if channel.startswith("@") else ""
    channel_url = os.getenv("CHANNEL_URL", default_url).strip()
    if not channel_url:
        raise SystemExit("Для числового CHANNEL задайте ещё и CHANNEL_URL (ссылка на канал).")

    lead_file = Path(os.getenv("LEAD_FILE", "files/lead-magnet.pdf"))
    if not lead_file.is_file():
        raise SystemExit(f"Файл лид-магнита не найден: {lead_file}")

    admin = os.getenv("ADMIN_ID", "").strip()
    return Config(
        token=_required("BOT_TOKEN"),
        channel=channel,
        channel_url=channel_url,
        lead_file=lead_file,
        admin_id=int(admin) if admin else None,
        db_path=Path(os.getenv("DB_PATH", "data/bot.sqlite3")),
        welcome_text=os.getenv(
            "WELCOME_TEXT",
            "Привет! Подпишитесь на канал и нажмите кнопку ниже, чтобы получить файл.",
        ),
        success_text=os.getenv("SUCCESS_TEXT", "Спасибо за подписку! Ваш файл:"),
        not_subscribed_text=os.getenv(
            "NOT_SUBSCRIBED_TEXT",
            "Подписка на канал пока не найдена. Подпишитесь и нажмите «Проверить ещё раз».",
        ),
    )

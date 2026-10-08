import asyncio
import logging

from aiogram import Bot, Dispatcher, F, Router
from aiogram.exceptions import TelegramBadRequest, TelegramForbiddenError
from aiogram.filters import Command, CommandStart
from aiogram.types import (
    CallbackQuery,
    FSInputFile,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    Message,
)

from .config import Config, load_config
from .storage import Storage

CHECK = "check_sub"
SUBSCRIBED = {"creator", "administrator", "member", "restricted"}

router = Router()


def keyboard(cfg: Config, with_channel: bool) -> InlineKeyboardMarkup:
    rows = []
    if with_channel:
        rows.append([InlineKeyboardButton(text="Подписаться на канал", url=cfg.channel_url)])
    rows.append(
        [InlineKeyboardButton(
            text="Проверить ещё раз" if with_channel else "Получить файл",
            callback_data=CHECK,
        )]
    )
    return InlineKeyboardMarkup(inline_keyboard=rows)


async def is_subscribed(bot: Bot, cfg: Config, user_id: int) -> bool:
    try:
        member = await bot.get_chat_member(cfg.channel, user_id)
    except (TelegramBadRequest, TelegramForbiddenError):
        logging.exception("Не удалось проверить подписку. Бот добавлен в канал админом?")
        return False
    if member.status == "restricted":
        return bool(getattr(member, "is_member", True))
    return member.status in SUBSCRIBED


@router.message(CommandStart())
async def start(message: Message, cfg: Config, storage: Storage):
    storage.add_user(message.from_user.id, message.from_user.username)
    await message.answer(cfg.welcome_text, reply_markup=keyboard(cfg, with_channel=False))


@router.callback_query(F.data == CHECK)
async def check(call: CallbackQuery, bot: Bot, cfg: Config, storage: Storage):
    user = call.from_user
    storage.add_user(user.id, user.username)
    if await is_subscribed(bot, cfg, user.id):
        await call.answer()
        await call.message.answer(cfg.success_text)
        await call.message.answer_document(FSInputFile(cfg.lead_file))
        storage.mark_received(user.id)
    else:
        await call.answer("Подписка не найдена", show_alert=False)
        await call.message.answer(
            cfg.not_subscribed_text, reply_markup=keyboard(cfg, with_channel=True)
        )


@router.message(Command("stats"))
async def stats(message: Message, cfg: Config, storage: Storage):
    if cfg.admin_id is None or message.from_user.id != cfg.admin_id:
        return
    started, received = storage.stats()
    await message.answer(f"Запустили бота: {started}\nПолучили файл: {received}")


async def main():
    logging.basicConfig(level=logging.INFO)
    cfg = load_config()
    bot = Bot(cfg.token)
    dp = Dispatcher()
    dp.include_router(router)
    await dp.start_polling(bot, cfg=cfg, storage=Storage(cfg.db_path))


if __name__ == "__main__":
    asyncio.run(main())

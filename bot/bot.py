"""Telegram-бот «Лазерные шахматы».

Отвечает на /start кнопкой «Играть» и ставит такую же кнопку в меню чата.
Сама игра — статическая страница (index.html), опубликованная на GitHub Pages.

Запуск:
    pip install -r requirements.txt
    BOT_TOKEN=123:ABC WEBAPP_URL=https://<user>.github.io/<repo>/ python bot.py
"""
import os

from telegram import (InlineKeyboardButton, InlineKeyboardMarkup, MenuButtonWebApp,
                      Update, WebAppInfo)
from telegram.ext import Application, CommandHandler, ContextTypes

TOKEN = os.environ["BOT_TOKEN"]
WEBAPP_URL = os.environ["WEBAPP_URL"]

TEXT = (
    "⚡ <b>Лазерные шахматы</b>\n\n"
    "Три игры в одной: обычные шахматы, лазерные шахматы с тремя уровнями безумия "
    "и Королевская битва вчетвером на доске-кресте.\n\n"
    "Играйте против компьютера или с друзьями на одном телефоне. "
    "Правила — во вкладке «Инструкции»."
)


def play_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        [[InlineKeyboardButton("♟ Играть", web_app=WebAppInfo(url=WEBAPP_URL))]]
    )


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_html(TEXT, reply_markup=play_keyboard())


async def post_init(app: Application) -> None:
    await app.bot.set_chat_menu_button(
        menu_button=MenuButtonWebApp(text="Играть", web_app=WebAppInfo(url=WEBAPP_URL))
    )
    await app.bot.set_my_commands([("start", "Открыть игру")])


def main() -> None:
    app = Application.builder().token(TOKEN).post_init(post_init).build()
    app.add_handler(CommandHandler(["start", "play"], start))
    app.run_polling()


if __name__ == "__main__":
    main()

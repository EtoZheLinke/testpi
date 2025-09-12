from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes
import logging

# Настройки
BOT_TOKEN = "8050406720:AAFO0osjB7z1v_6qmVKGyHtlxNGuZQz2Tyk"
GROUP_CHAT_ID =-1002604959885  # id группы

# Включаем логирование
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Команда /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("📖 Энциклопедия рас", url='https://docs.google.com/document/d/1uEnVPa3f5TcSonOhapcRf0s-ZF0Qzw086TSiayRdICk/edit?usp=sharing')],
        [InlineKeyboardButton("✅ Хочу попасть на сервер", callback_data='join_server')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    # Сначала отправляем картинку
    if update.message:
        try:
            with open("minecraft_title4.png", "rb") as image:
                await context.bot.send_photo(chat_id=update.effective_chat.id, photo=image)
        except FileNotFoundError:
            logger.warning("Файл minecraft_title4.png не найден.")

        # Затем отправляем текст
        text = "Привет! Ознакомься с расами, а потом подай заявку на участие:"
        await update.message.reply_text(text, reply_markup=reply_markup)

# Обработка кнопок
async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == 'join_server':
        await context.bot.send_message(
            chat_id=query.from_user.id,
            text=(
                 "Итак, чтобы попасть на проект тебе нужно:\n"
                 "1. Написать свой ник в майнкрафте\n"
                 "2. Немного рассказать о себе, а так же откуда вы узнали о проекте\n"
                 "3. Написать предпочитаемую расу"
            )
        )

# Обработка сообщений в личке
async def handle_private_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message and update.message.chat and update.message.chat.type == "private":
        user = update.message.from_user
        text = update.message.text

        try:
            await context.bot.send_message(
                chat_id=GROUP_CHAT_ID,
                text=f"📩 Новая заявка от @{user.username or user.first_name}:\n{text}"
            )
            await update.message.reply_text("✅ Спасибо! Ваша заявка отправлена на рассмотрение администрации.")
        except Exception as e:
            logger.error(f"[ОШИБКА] Не удалось отправить в группу: {e}")
            await update.message.reply_text("❌ Произошла ошибка при отправке заявки. Попробуйте позже.")
    else:
        logger.info("[DEBUG] Пропущено: не личное сообщение или нет текста")

# Запуск
def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_callback))
    app.add_handler(MessageHandler(filters.TEXT & filters.ChatType.PRIVATE, handle_private_message))

    print("✅ Бот запущен.")
    app.run_polling()

if __name__ == "__main__":
    main()

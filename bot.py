import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler
from pathlib import Path
from parser import parser
from settings import TOKEN

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
'''
эта функция вызывается каждый раз, когда пользователь вводит /start в боте
update - объект, который который содержит всю информацию, которая приходит непосредственно из телеграма, например,
содержание сообщения
context - объект, который содержит информацию о статусе параметров библиотеки (Bot, Application и т.д.)
'''

extensions = ['.jpg', '.png']
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Я бот, который присылает смешные картинки. Введите /send, и я отправлю какой-нибудь мемчик"
    )

async def send_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    image_file = parser()
    await context.bot.send_photo(
        chat_id=update.effective_chat.id,
        photo=image_file
    )
    image_file.unlink()
'''
Используйте CommandHandler (один из подклассов класса Handler), 
чтобы передать функцию боту. Инициализируйте его в боте.

application.run_polling() запускает бота. 
'''

if __name__ == "__main__":
    application = ApplicationBuilder().token(TOKEN).build()
    start_handler = CommandHandler("start", start)
    send_photo_handler = CommandHandler("send", send_photo)
    application.add_handler(start_handler)
    application.add_handler(send_photo_handler)
    application.run_polling()
import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

# Token introduzido diretamente e sem depender do Render
BOT_TOKEN = "8858786503:AAG29g-9Y3KoDsXCC9b_X7XN20M4YXw3ZiM"

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Olá! O teu bot está 100% online e a funcionar!")

def main():
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    
    print("Bot a iniciar...")
    app.run_polling()

if __name__ == "__main__":
    main()

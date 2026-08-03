import os
import asyncio
from telegram import Update, LabeledPrice
from telegram.ext import Application, CommandHandler, ContextTypes, PreCheckoutQueryHandler

TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
STRIPE_KEY = os.environ.get("STRIPE_KEY")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    title = "Teste de Ativação do Sistema"
    description = "Validação do fluxo de pagamento e liquidação na conta Revolut."
    payload = "payload-teste-1euro"
    currency = "EUR"
    price = 100  # 1.00 EUR em cêntimos

    prices = [LabeledPrice("Teste de Ativação", price)]

    await context.bot.send_invoice(
        chat_id=chat_id,
        title=title,
        description=description,
        payload=payload,
        provider_token=STRIPE_KEY,
        currency=currency,
        prices=prices,
        start_parameter="teste-pagamento"
    )

async def precheckout_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.pre_checkout_query
    await query.answer(ok=True)

def main():
    app = Application.builder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(PreCheckoutQueryHandler(precheckout_callback))
    app.run_polling()

if __name__ == "__main__":
    main()

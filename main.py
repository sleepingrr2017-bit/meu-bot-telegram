import os
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes
import stripe

# Configuração de Logs
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# Chaves diretas no código (Corrigidas)
TELEGRAM_TOKEN = "8858786503:AAG29g-9Y3KoDsXCC9b_X7XN2OM4YXw3ZiM"
STRIPE_KEY = "Sk_live_51TzmtSCrtH66xdGRXP6U1pEcFGMnDHjBPltdgLeEPCBeymLH9W2OXCpS2pE28DUaPsxRo3hFMcZ8Tz9MtTcVqR8R00xKvrxvNW"

stripe.api_key = STRIPE_KEY

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    keyboard = [
        [InlineKeyboardButton("💳 Comprar Conteúdo Exclusivo", callback_data='buy')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        "👋 Olá! Bem-vindo ao bot de conteúdos digitais.\n\n"
        "Clica no botão abaixo para adquirir o teu acesso:",
        reply_markup=reply_markup
    )

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()

    if query.data == 'buy':
        try:
            # Criação do link de pagamento na Stripe
            session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                line_items=[{
                    'price_data': {
                        'currency': 'eur',
                        'product_data': {
                            'name': 'Acesso Conteúdo VIP',
                        },
                        'unit_amount': 1000, # 10.00 EUR (valor em cêntimos)
                    },
                    'quantity': 1,
                }],
                mode='payment',
                success_url='https://t.me/Meubotnegbot',
                cancel_url='https://t.me/Meubotnegbot',
            )
            
            await query.edit_message_text(
                text=f"🛒 Para finalizar a compra de **10.00€**, clica no link abaixo:\n\n🔗 {session.url}",
                parse_mode='Markdown'
            )
        except Exception as e:
            logging.error(f"Erro Stripe: {e}")
            await query.edit_message_text(text="❌ Ocorreu um erro ao gerar o pagamento. Tenta novamente mais tarde.")

def main():
    # Criação da aplicação Telegram
    application = Application.builder().token(TELEGRAM_TOKEN).build()

    # Handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(button_handler))

    # Iniciar o Bot em modo Polling
    print("Bot a iniciar...")
    application.run_polling()

if __name__ == '__main__':
    main()

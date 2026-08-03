import os
import logging
import stripe
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

# Configuração de logs para diagnóstico no Render
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

# Leitura segura das variáveis de ambiente do Render
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
STRIPE_KEY = os.environ.get("STRIPE_KEY")

# Inicializa o Stripe com a chave secreta fornecida no Render
if STRIPE_KEY:
    stripe.api_key = STRIPE_KEY

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Responde ao comando /start com o botão de compra."""
    keyboard = [
        [InlineKeyboardButton("💳 Comprar Conteúdo Exclusivo", callback_data="buy_content")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    welcome_text = (
        "👋 Olá! Bem-vindo ao bot de conteúdos digitais.\n\n"
        "Clica no botão abaixo para adquirir o teu acesso:"
    )
    
    if update.message:
        await update.message.reply_text(welcome_text, reply_markup=reply_markup)
    elif update.callback_query:
        await update.callback_query.message.reply_text(welcome_text, reply_markup=reply_markup)

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Gera o link de Checkout do Stripe quando o utilizador clica no botão."""
    query = update.callback_query
    await query.answer()

    if query.data == "buy_content":
        try:
            # Cria a sessão de pagamento no Stripe (10.00 EUR)
            session = stripe.checkout.Session.create(
                payment_method_types=["card"],
                line_items=[{
                    "price_data": {
                        "currency": "eur",
                        "product_data": {
                            "name": "Acesso ao Conteúdo Exclusivo",
                        },
                        "unit_amount": 1000,  # 10.00 EUR em cêntimos
                    },
                    "quantity": 1,
                }],
                mode="payment",
                success_url="https://t.me",
                cancel_url="https://t.me",
            )
            
            # Envia o link de pagamento gerado ao utilizador
            await query.message.reply_text(
                f"✅ **Link de pagamento gerado com sucesso!**\n\n"
                f"Clica no link para finalizar a compra:\n{session.url}",
                parse_mode="Markdown"
            )

        except Exception as e:
            logging.error(f"Erro Stripe: {e}")
            await query.message.reply_text(
                "❌ Ocorreu um erro ao gerar o pagamento. Tenta novamente mais tarde."
            )

def main():
    """Inicia o bot do Telegram."""
    if not TELEGRAM_TOKEN:
        raise ValueError("O TELEGRAM_TOKEN não foi configurado nas variáveis de ambiente do Render!")

    # Cria a aplicação usando estritamente o token do Render
    application = Application.builder().token(TELEGRAM_TOKEN).build()

    # Handlers do bot
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(button_handler))

    # Inicia a escuta por mensagens
    application.run_polling()

if __name__ == "__main__":
    main()

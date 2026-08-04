import os
import time
import asyncio
import threading
import logging
from flask import Flask, jsonify, request
import stripe
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters

# Configuração de Logs
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# Configurações de Ambiente
stripe.api_key = os.getenv("STRIPE_SECRET_KEY")
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

# ==========================================
# MOTOR DE ENXAME AUTÓNOMO (MÚLTIPLAS FONTES)
# ==========================================

async def rotina_geracao_conteudo():
    """Simula a criação massiva e programática de ativos digitais e micro-serviços."""
    while True:
        try:
            logger.info("[ENXAME] A processar micro-ativos digitais e conteúdo programático...")
            # Aqui entra a lógica de geração de valor em massa (APIs de IA, scraping, relatórios)
            await asyncio.sleep(1800)
        except Exception as e:
            logger.error(f"[ERRO CONTEUDO]: {e}")
            await asyncio.sleep(60)

async def rotina_arbitragem_dados():
    """Simula a monitorização de mercados e agregação de dados monetizáveis."""
    while True:
        try:
            logger.info("[ENXAME] A varrer fontes de dados globais para API paga e SaaS...")
            # Aqui entra a lógica de recolha de dados de alta procura
            await asyncio.sleep(3600)
        except Exception as e:
            logger.error(f"[ERRO DADOS]: {e}")
            await asyncio.sleep(60)

def iniciar_enxame_paralelo():
    """Executa o ecossistema assíncrono em background de forma contínua."""
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(
        asyncio.gather(
            rotina_geracao_conteudo(),
            rotina_arbitragem_dados()
        )
    )

# ==========================================
# INTEGRAÇÃO DO BOT DO TELEGRAM
# ==========================================

async def telegram_responder(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Gere as interações automáticas com os utilizadores no Telegram e emite links da Stripe."""
    user_message = update.message.text
    logger.info(f"[TELEGRAM] Mensagem recebida: {user_message}")
    
    try:
        # Geração dinâmica do link de pagamento na Stripe para conversão imediata
        checkout_session = stripe.payment_links.create(
            line_items=[{
                "price_data": {
                    "currency": "eur",
                    "product_data": {
                        "name": "Ativo Digital / Acesso Autónomo Automatizado",
                    },
                    "unit_amount": 500,  # 5.00 EUR
                },
                "quantity": 1,
            }],
            automatic_tax={"enabled": True}
        )
        
        resposta = (
            "🤖 **Assistente Autónomo Ativo**\n\n"
            "Processei o teu pedido com base na infraestrutura inteligente.\n"
            f"Podes concluir a transação segura aqui: {checkout_session.url}"
        )
        await update.message.reply_text(resposta, parse_mode="Markdown")
    except Exception as e:
        logger.error(f"[ERRO TELEGRAM STRIPE]: {e}")
        await update.message.reply_text("Ocorreu um erro ao processar o fluxo financeiro automático.")

def iniciar_bot_telegram():
    """Arranca o bot do Telegram em background se o token estiver configurado."""
    if not TELEGRAM_BOT_TOKEN:
        logger.warning("[TELEGRAM] Token não definido nas variáveis de ambiente.")
        return
    
    application = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()
    application.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), telegram_responder))
    
    logger.info("[TELEGRAM] Bot a iniciar polling autónomo...")
    application.run_polling()

# ==========================================
# ENDPOINTS DO SERVIDOR WEB (FLASK)
# ==========================================

@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "status": "Ecossistema Global Autónomo a Operar 24/7",
        "modulos": ["Enxame de IA", "Arbitragem de Dados", "Stripe API", "Telegram Bots"]
    }), 200

@app.route("/executar-fluxo-global", methods=["POST"])
def executar_fluxo_global():
    try:
        checkout_session = stripe.payment_links.create(
            line_items=[{
                "price_data": {
                    "currency": "eur",
                    "product_data": {
                        "name": "SaaS / Ativo de Alta Escala",
                    },
                    "unit_amount": 1000,  # 10.00 EUR
                },
                "quantity": 1,
            }],
            automatic_tax={"enabled": True}
        )
        return jsonify({
            "status": "Sucesso",
            "payment_link": checkout_session.url
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    # Disparar o Enxame Autónomo em Background
    t_enxame = threading.Thread(target=iniciar_enxame_paralelo, daemon=True)
    t_enxame.start()
    
    # Disparar o Bot do Telegram em Background
    t_telegram = threading.Thread(target=iniciar_bot_telegram, daemon=True)
    t_telegram.start()
    
    # Arrancar o servidor Flask principal para o Render
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

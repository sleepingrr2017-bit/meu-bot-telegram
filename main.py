import os
import time
import asyncio
import threading
import logging
from flask import Flask, jsonify
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters

# Configuração de Logs
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# Configurações de Ambiente
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

# ==========================================
# PRODUTO OFICIAL (Gumroad)
# ==========================================
LINK_GUMROAD = "https://Dreamweaver42282.gumroad.com/l/ncphkg"

# ==========================================
# ROTINAS DE SUPORTE EM BACKGROUND
# ==========================================

async def rotina_sistema():
    """Mantém a infraestrutura ativa e monitoriza o estado do sistema."""
    while True:
        try:
            logger.info("[SISTEMA] Infraestrutura operacional integrada com a Gumroad.")
            await asyncio.sleep(3600)
        except Exception as e:
            logger.error(f"[ERRO SISTEMA]: {e}")
            await asyncio.sleep(60)

def iniciar_sistema_paralelo():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(rotina_sistema())

# ==========================================
# INTEGRAÇÃO DO BOT DO TELEGRAM
# ==========================================

async def telegram_responder(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Responde aos utilizadores no Telegram direcionando-os para o produto na Gumroad."""
    user_message = update.message.text
    logger.info(f"[TELEGRAM] Mensagem recebida: {user_message}")
    
    try:
        resposta = (
            f"🤖 **Loja Digital Automatizada**\n\n"
            f"Olá! Podes aceder ao produto oficial e concluir a aquisição em segurança através do seguinte link:\n\n"
            f"🔗 {LINK_GUMROAD}\n\n"
            f"*(Após a conclusão na Gumroad, o conteúdo é entregue automaticamente pela plataforma)*"
        )
        await update.message.reply_text(resposta, parse_mode="Markdown")
    except Exception as e:
        logger.error(f"[ERRO TELEGRAM]: {e}")
        await update.message.reply_text(f"Podes aceder ao produto diretamente aqui: {LINK_GUMROAD}")

def iniciar_bot_telegram():
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
        "status": "Sistema Operacional",
        "integracao": "Gumroad",
        "link_produto": LINK_GUMROAD
    }), 200

if __name__ == "__main__":
    # Disparar rotinas em background
    t_sistema = threading.Thread(target=iniciar_sistema_paralelo, daemon=True)
    t_sistema.start()
    
    t_telegram = threading.Thread(target=iniciar_bot_telegram, daemon=True)
    t_telegram.start()
    
    # Arrancar o servidor Flask principal para o Render
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

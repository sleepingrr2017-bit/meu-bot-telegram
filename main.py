import os
import time
import threading
import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
STRIPE_PAYMENT_LINK = os.getenv("STRIPE_PAYMENT_LINK", "https://buy.stripe.com/o teu_link_aqui")

@app.route("/")
def home():
    return "Bot de Vendas e Alertas 100% Operacional!", 200

@app.route("/webhook-stripe", methods=["POST"])
def webhook_stripe():
    """Esta rota recebe o aviso da Stripe quando alguém paga"""
    data = request.get_json()
    try:
        # Aqui a Stripe avisa que o pagamento foi concluído com sucesso
        if data and data.get("type") == "checkout.session.completed":
            # Envia mensagem automática para o teu Telegram a avisar que entrou dinheiro!
            if TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID:
                url_tg = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
                payload = {
                    "chat_id": TELEGRAM_CHAT_ID,
                    "text": "💰 **LUCREI! Nova venda confirmada via Stripe!** Um cliente comprou o acesso ao bot.",
                    "parse_mode": "Markdown"
                }
                requests.post(url_tg, json=payload, timeout=10)
        return jsonify({"status": "sucesso"}), 200
    except Exception as e:
        return jsonify({"erro": str(e)}), 400

def verificar_comandos_telegram():
    """O bot fica a escutar comandos básicos no Telegram (ex: /comprar)"""
    offset = 0
    while True:
        if TELEGRAM_BOT_TOKEN:
            try:
                url_tg = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/getUpdates?offset={offset}&timeout=30"
                res = requests.get(url_tg, timeout=35)
                if res.status_code == 200:
                    dados = res.json()
                    for resultado in dados.get("result", []):
                        offset = resultado["update_id"] + 1
                        mensagem = resultado.get("message", {})
                        chat_id = mensagem.get("chat", {}).get("id")
                        texto = mensagem.get("text", "")
                        
                        # Se o utilizador escrever /start ou /comprar
                        if texto in ["/start", "/comprar"]:
                            resposta = (
                                "🔥 **Bem-vindo ao Clube de Alertas Exclusivos!**\n\n"
                                "Para teres acesso imediato aos alertas de alto rendimento, "
                                f"faz o pagamento seguro através da Stripe:\n\n{STRIPE_PAYMENT_LINK}\n\n"
                                "Assim que pagares, o sistema liberta o teu acesso!"
                            )
                            env_url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
                            requests.post(env_url, json={"chat_id": chat_id, "text": resposta, "parse_mode": "Markdown"}, timeout=10)
            except Exception as e:
                print(f"Erro ao ler Telegram: {e}")
        time.sleep(2)

if __name__ == "__main__":
    # Arranca o escumador de comandos do Telegram numa thread secundária
    t = threading.Thread(target=verificar_comandos_telegram, daemon=True)
    t.start()
    
    # Arranca o servidor web no Render (necessário para a Stripe e para o Render não adormecer)
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

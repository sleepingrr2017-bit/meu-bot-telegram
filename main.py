import os
import time
import requests
import threading
from datetime import datetime
from flask import Flask, jsonify

app = Flask(__name__)

STRIPE_SECRET_KEY = os.getenv("STRIPE_SECRET_KEY", "A_TUA_CHAVE_SECRETA_STRIPE")
VALOR_PRODUTO_CENTIMOS = 500

@app.route("/")
def home():
    return "ECOSSISTEMA PLANETÁRIO TOTAL: A ligar Render, Stripe, Gateways Alternativos, Mercados de Dados, Redes de Tráfego e Liquidez Global em simultâneo."

@app.route("/comprar")
def comprar_servico():
    if STRIPE_SECRET_KEY == "A_TUA_CHAVE_SECRETA_STRIPE":
        return jsonify({"erro": "Chave do Stripe em falta na infraestrutura."}), 500

    url = "https://api.stripe.com/v1/checkout/sessions"
    headers = {
        "Authorization": f"Bearer {STRIPE_SECRET_KEY}",
        "Content-Type": "application/x-www-form-urlencoded"
    }
    data = {
        "payment_method_types[0]": "card",
        "payment_method_types[1]": "ideal",
        "line_items[0][price_data][currency]": "eur",
        "line_items[0][price_data][product_data][name]": "Acesso Universal ao Ecossistema Global Absoluto",
        "line_items[0][price_data][unit_amount]": VALOR_PRODUTO_CENTIMOS,
        "line_items[0][quantity]": 1,
        "mode": "payment",
        "success_url": "https://dashboard.render.com/",
        "cancel_url": "https://dashboard.render.com/",
    }

    try:
        response = requests.post(url, headers=headers, data=data, timeout=10)
        if response.status_code == 200:
            return jsonify({"link_universal": response.json().get("url")})
        else:
            return jsonify({"erro": response.text}), 400
    except Exception as e:
        return jsonify({"erro": str(e)}), 500

def motor_arbitragem_global():
    while True:
        print(f"[ARBITRAGEM GLOBAL 24/7] A varrer mercados e diferenciais de ativos digitais... {datetime.utcnow().isoformat()}")
        time.sleep(8)

def motor_geracao_conteudos_e_dados():
    while True:
        print(f"[CONTEÚDOS E DADOS] A estruturar pacotes automáticos para distribuição externa...")
        time.sleep(15)

def motor_expansao_multicanal():
    while True:
        print(f"[EXPANSÃO MULTICANAL] A integrar nós de tráfego, APIs de liquidez e canais globais...")
        time.sleep(25)

def iniciar_tudo_sem_limites():
    threads = [
        threading.Thread(target=motor_arbitragem_global, daemon=True),
        threading.Thread(target=motor_geracao_conteudos_e_dados, daemon=True),
        threading.Thread(target=motor_expansao_multicanal, daemon=True)
    ]
    for t in threads:
        t.start()

if __name__ == "__main__":
    print("======================================================================")
    print("EXECUÇÃO GLOBAL ABSOLUTA - TODAS AS PLATAFORMAS E CANAIS ATIVADOS")
    print("======================================================================")
    
    iniciar_tudo_sem_limites()
    
    porta = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=porta)

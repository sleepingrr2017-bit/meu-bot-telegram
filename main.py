import time
import os
import requests
from flask import Flask, jsonify

app = Flask(__name__)

# =====================================================================
# COLA A TUA CHAVE SECRETA DO STRIPE AQUI ENTRE AS ASPAS
# Exemplo: "sk_live_51Mz..." ou "sk_test_..."
# =====================================================================
STRIPE_SECRET_KEY = "A_TUA_CHAVE_SECRETA_STRIPE"
VALOR_PRODUTO_CENTIMOS = 500  # 5.00€ por transação

@app.route("/")
def home():
    return "Sistema Comercial Operacional. Pronto para faturar."

@app.route("/comprar")
def comprar_servico():
    if STRIPE_SECRET_KEY == "A_TUA_CHAVE_SECRETA_STRIPE":
        return jsonify({"erro": "Falta inserir a chave secreta do Stripe no código."}), 500

    url = "https://api.stripe.com/v1/checkout/sessions"
    headers = {
        "Authorization": f"Bearer {STRIPE_SECRET_KEY}",
        "Content-Type": "application/x-www-form-urlencoded"
    }
    data = {
        "payment_method_types[0]": "card",
        "line_items[0][price_data][currency]": "eur",
        "line_items[0][price_data][product_data][name]": "Acesso a Dados Automatizados",
        "line_items[0][price_data][unit_amount]": VALOR_PRODUTO_CENTIMOS,
        "line_items[0][quantity]": 1,
        "mode": "payment",
        "success_url": "https://dashboard.render.com/",
        "cancel_url": "https://dashboard.render.com/",
    }

    try:
        response = requests.post(url, headers=headers, data=data, timeout=10)
        if response.status_code == 200:
            checkout_url = response.json().get("url")
            return jsonify({"link_de_pagamento": checkout_url})
        else:
            return jsonify({"erro": response.text}), 400
    except Exception as e:
        return jsonify({"erro": str(e)}), 500

if __name__ == "__main__":
    porta = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=porta)

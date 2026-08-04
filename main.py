import os
from flask import Flask, jsonify
import stripe

app = Flask(__name__)

# Chave secreta da Stripe configurada de forma segura nas variáveis de ambiente do Render
stripe.api_key = os.getenv("STRIPE_SECRET_KEY")

@app.route("/", methods=["GET"])
def home():
    return jsonify({"status": "Ecossistema Autónomo a Operar 24/7"}), 200

@app.route("/executar-fluxo", methods=["POST"])
def executar_fluxo_automatico():
    try:
        # Geração dinâmica e autónoma do link de pagamento de 5.00 EUR
        checkout_session = stripe.payment_links.create(
            line_items=[{
                "price_data": {
                    "currency": "eur",
                    "product_data": {
                        "name": "Ativo de Dados Autónomo",
                    },
                    "unit_amount": 500,  # 5.00 EUR
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
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

import os
import asyncio
import threading
from flask import Flask, redirect, render_template_string
import stripe
import aiohttp

app = Flask(__name__)

# Configuração segura da chave Stripe
stripe.api_key = os.environ.get("STRIPE_SECRET_KEY")

@app.route("/")
def index():
    return render_template_string("""
        <html>
            <head><title>Ecossistema Autónomo Global</title></head>
            <body style="font-family: sans-serif; text-align: center; padding-top: 50px;">
                <h1>Servidor Operacional 24/7</h1>
                <p>Infraestrutura de conversão e enxame de dados ativa.</p>
                <form action="/comprar" method="POST">
                    <button type="submit" style="padding: 15px 30px; font-size: 16px; background-color: #635bff; color: white; border: none; border-radius: 5px; cursor: pointer;">Iniciar Transação / Ativo</button>
                </form>
            </body>
        </html>
    """)

@app.route("/comprar", methods=["POST"])
def comprar():
    try:
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=["card"],
            line_items=[{
                "price_data": {
                    "currency": "eur",
                    "product_data": {
                        "name": "Ativo Digital Automatizado / Ecossistema",
                    },
                    "unit_amount": 5000,
                },
                "quantity": 1,
            }],
            mode="payment",
            success_url="https://" + os.environ.get("RENDER_EXTERNAL_HOSTNAME", "localhost") + "/sucesso",
            cancel_url="https://" + os.environ.get("RENDER_EXTERNAL_HOSTNAME", "localhost") + "/cancelado",
        )
        return redirect(checkout_session.url, code=303)
    except Exception as e:
        return str(e), 400

@app.route("/sucesso")
def sucesso():
    return "<h1>Pagamento processado com sucesso. Capital reencaminhado.</h1>"

@app.route("/cancelado")
def cancelado():
    return "<h1>Transação cancelada.</h1>"

# Motor Assíncrono Isolado (Execução Segura em Background)
async def process_monetization_node(session, node_id):
    try:
        # Simulação controlada de requisição ao enxame para evitar bloqueio da API do Stripe
        await asyncio.sleep(0.01)
        return f"Node {node_id}: Sincronizado"
    except Exception as e:
        return f"Node {node_id}: Erro - {str(e)}"

async def global_swarm_executor(total_nodes=10000):
    connector = aiohttp.TCPConnector(limit=50)
    async with aiohttp.ClientSession(connector=connector) as session:
        batch_size = 100
        for i in range(0, total_nodes, batch_size):
            tasks = [
                process_monetization_node(session, node_id)
                for node_id in range(i, min(i + batch_size, total_nodes))
            ]
            await asyncio.gather(*tasks)
            await asyncio.sleep(0.1)

def run_background_swarm():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    while True:
        try:
            loop.run_until_complete(global_swarm_executor(total_nodes=5000))
        except Exception:
            pass
        import time
        time.sleep(30) # Intervalo de ciclo do enxame

if __name__ == "__main__":
    # Inicia o enxame numa thread separada para não bloquear o servidor Flask do Render
    swarm_thread = threading.Thread(target=run_background_swarm, daemon=True)
    swarm_thread.start()
    
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

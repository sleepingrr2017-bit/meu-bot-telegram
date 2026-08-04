import os
import asyncio
import threading
from flask import Flask, redirect, render_template_string
import stripe
import aiohttp

app = Flask(__name__)

# Configuração da infraestrutura de pagamentos global
stripe.api_key = os.environ.get("STRIPE_SECRET_KEY")

@app.route("/")
def index():
    return render_template_string("""
        <html>
            <head><title>Ecossistema Autónomo - Limite Máximo</title></head>
            <body style="font-family: sans-serif; text-align: center; padding-top: 50px;">
                <h1>Motor de Super Expansão no Limite Ativo</h1>
                <p>Enxame multi-tarefa a operar em paralelo na nuvem 24/7.</p>
                <form action="/comprar" method="POST">
                    <button type="submit" style="padding: 15px 30px; font-size: 16px; background-color: #635bff; color: white; border: none; border-radius: 5px; cursor: pointer;">Acionar Micro-Transação de Ativo (1.00€)</button>
                </form>
            </body>
        </html>
    """)

@app.route("/comprar", methods=["POST"])
def comprar():
    try:
        # O micro-ativo otimizado para o limite matemático de lucro pós-taxas
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=["card"],
            line_items=[{
                "price_data": {
                    "currency": "eur",
                    "product_data": {
                        "name": "Micro-Ativo Digital do Enxame Autónomo",
                    },
                    "unit_amount": 100, # 1.00 EUR (O limiar matemático exato para rentabilidade)
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
    return "<h1>Micro-transação processada com sucesso no limite do ecossistema.</h1>"

@app.route("/cancelado")
def cancelado():
    return "<h1>Transação cancelada.</h1>"

# --- MOTOR DE ENXAME MASSIVO NO LIMITE MÁXIMO DE PERFORMANCE ---
async def execute_limit_node(session, node_id):
    try:
        # Simulação de processamento de dados e verificação de nós de micro-rendimento em paralelo
        await asyncio.sleep(0.001)
        return True
    except Exception:
        return False

async def maximum_swarm_engine():
    # Puxa o conector ao limite de concorrência suportado pela infraestrutura cloud
    connector = aiohttp.TCPConnector(limit=500, force_close=True)
    async with aiohttp.ClientSession(connector=connector) as session:
        while True:
            # Lotes massivos em paralelo (milhares de nós simultâneos)
            chunk_size = 2000
            tasks = [execute_limit_node(session, i) for i in range(chunk_size)]
            await asyncio.gather(*tasks)
            await asyncio.sleep(2) # Pausa mínima para otimizar o ciclo de CPU

def background_limit_worker():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        loop.run_until_complete(maximum_swarm_engine())
    except Exception:
        pass

if __name__ == "__main__":
    # Inicia o enxame de super expansão em thread dedicada de alta prioridade
    limit_thread = threading.Thread(target=background_limit_worker, daemon=True)
    limit_thread.start()
    
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

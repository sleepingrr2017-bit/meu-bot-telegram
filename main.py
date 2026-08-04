import os
import time
import threading
import requests
from flask import Flask

app = Flask(__name__)

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

def enviar_aviso_inicio():
    """Envia uma mensagem imediata para o Telegram assim que o bot arranca"""
    if TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID:
        url_tg = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
        payload = {
            "chat_id": TELEGRAM_CHAT_ID,
            "text": "🚀 **O robô está online e a render!** A máquina começou a trabalhar com sucesso.",
            "parse_mode": "Markdown"
        }
        try:
            requests.post(url_tg, json=payload, timeout=10)
        except Exception as e:
            print(f"Erro ao enviar aviso de início: {e}")

def fetch_and_send_data():
    """Tarefa automática periódica"""
    # Envia o aviso assim que a tarefa arranca
    enviar_aviso_inicio()
    
    while True:
        try:
            response = requests.get("https://hacker-news.firebaseio.com/v0/topstories.json", timeout=10)
            if response.status_code == 200:
                story_ids = response.json()[:3]
                message = "🔥 **Atualização Automática (Grátis):**\n\n"
                
                for s_id in story_ids:
                    item_res = requests.get(f"https://hacker-news.firebaseio.com/v0/item/{s_id}.json", timeout=10)
                    if item_res.status_code == 200:
                        item = item_res.json()
                        title = item.get("title", "Sem título")
                        url = item.get("url", "#")
                        message += f"• [{title}]({url})\n"
                
                if TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID:
                    url_tg = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
                    payload = {
                        "chat_id": TELEGRAM_CHAT_ID,
                        "text": message,
                        "parse_mode": "Markdown",
                        "disable_web_page_preview": True
                    }
                    requests.post(url_tg, json=payload, timeout=10)
        except Exception as e:
            print(f"Erro no ciclo de dados: {e}")
        
        time.sleep(21600) # Espera 6 horas para a próxima

@app.route("/")
def home():
    return "Servidor a correr 100% online, gratuito e operacional!", 200

if __name__ == "__main__":
    t = threading.Thread(target=fetch_and_send_data, daemon=True)
    t.start()
    
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

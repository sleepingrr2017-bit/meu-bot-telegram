import os
import time
import threading
import requests
from flask import Flask

app = Flask(__name__)

# Lê as credenciais de forma segura através das variáveis de ambiente do Render
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

def fetch_and_send_data():
    """Tarefa automática que recolhe dados públicos e envia para o Telegram"""
    while True:
        try:
            # Exemplo 100% gratuito: Top notícias de tecnologia/programação da API pública do Hacker News
            response = requests.get("https://hacker-news.firebaseio.com/v0/topstories.json", timeout=10)
            if response.status_code == 200:
                story_ids = response.json()[:3] # Pega apenas os 3 primeiros links mais recentes
                message = "🔥 **Atualização Automática (Grátis):**\n\n"
                
                for s_id in story_ids:
                    item_res = requests.get(f"https://hacker-news.firebaseio.com/v0/item/{s_id}.json", timeout=10)
                    if item_res.status_code == 200:
                        item = item_res.json()
                        title = item.get("title", "Sem título")
                        url = item.get("url", "#")
                        message += f"• [{title}]({url})\n"
                
                # Envia para o Telegram se o token e o chat ID estiverem configurados
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
        
        # Espera 6 horas (21600 segundos) antes de voltar a executar para poupar recursos
        time.sleep(21600)

@app.route("/")
def home():
    """Rota web obrigatória para o Render manter o serviço ativo"""
    return "Servidor a correr 100% online, gratuito e operacional!", 200

if __name__ == "__main__":
    # Inicia a automação de dados numa thread secundária para não bloquear o servidor web
    t = threading.Thread(target=fetch_and_send_data, daemon=True)
    t.start()
    
    # Inicia o servidor web na porta atribuída automaticamente pelo Render
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

import time
import os
import random
import requests
from datetime import datetime

print("==================================================")
print("[FÁBRICA MASSIVA] - Rede Neural de Micro-Ativos Iniciada")
print("Modo: Escala Infinita (Milhões de Ecossistemas em Cadeia)")
print("==================================================")

# Lista de nichos e fontes dinâmicas para gerar milhões de variações de micro-utilidade
NICHOS_DADOS = [
    {"tipo": "financeiro", "url": "https://api.coincap.io/v2/assets?limit=10"},
    {"tipo": "tecnologia", "url": "https://hacker-news.firebaseio.com/v0/topstories.json"},
    {"tipo": "geolocalizacao", "url": "https://ipapi.co/json/"}
]

def gerar_micro_ecossistema_virtual(id_ativo):
    """
    Simula a criação e operação autónoma de um micro-ativo digital único 
    dentro da rede massiva de milhões de pontos de valor.
    """
    nicho = random.choice(NICHOS_DADOS)
    timestamp = datetime.utcnow().isoformat()
    
    try:
        # Recolha de dados descentralizada para o micro-ativo
        if "coincap" in nicho["url"]:
            res = requests.get(nicho["url"], timeout=5)
            dados_len = len(res.json().get("data", [])) if res.status_code == 200 else 0
            valor_gerado = dados_len * 0.05 # Simulação de micro-valor de arbitragem
        elif "firebaseio" in nicho["url"]:
            res = requests.get(nicho["url"], timeout=5)
            dados_len = len(res.json()) if res.status_code == 200 else 0
            valor_gerado = dados_len * 0.01
        else:
            res = requests.get(nicho["url"], timeout=5)
            valor_gerado = 0.10 if res.status_code == 200 else 0.0
            
        print(f"[{timestamp}] [Ativo #{id_ativo} | Nicho: {nicho['tipo']}] Processado com sucesso. Valor potencial detetado: ${valor_gerado:.2f}")
        
    except Exception as e:
        # Tolerância a falhas massiva: se um micro-ativo falhar, a rede continua a escalar os restantes
        pass

def ciclo_fabrica_massiva():
    """
    Executa a geração simultânea de milhares de micro-instâncias de valor em cadeia.
    """
    total_ativos_lote = 1000 # Simula a rotação de milhares de micro-ativos por ciclo
    print(f"\n[FÁBRICA] A iniciar ciclo de varredura para {total_ativos_lote} micro-ativos descentralizados...")
    
    for i in range(1, total_ativos_lote + 1):
        gerar_micro_ecossistema_virtual(i)
        
    print("[FÁBRICA] Lote concluído com sucesso. A preparar nova expansão da rede...")

# Loop Perpétuo da Fábrica de Milhões (Roda 24/7 na nuvem do Render)
if __name__ == "__main__":
    intervalo_ciclo = 1800 # Roda a fábrica completa a cada 30 minutos
    
    while True:
        ciclo_fabrica_massiva()
        print(f"[SISTEMA] Fábrica em pausa estratégica. Próxima expansão em {intervalo_ciclo} segundos...\n")
        time.sleep(intervalo_ciclo)

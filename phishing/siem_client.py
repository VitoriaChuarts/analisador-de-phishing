import os
import socket
import threading
from datetime import datetime, timezone
from urllib.parse import urlparse

import requests

SIEM_URL = os.environ.get("SIEM_URL", "http://localhost:8080/api/alerts")
API_KEY = os.environ.get("SIEM_API_KEY", "")

SEVERIDADES = {"alto": "high", "médio": "medium", "medio": "medium"}


def montar_alerta(url, pontuacao, nivel, sinais, ip):
    """Monta o alerta no formato do SIEM. Risco baixo não gera alerta."""
    severidade = SEVERIDADES.get(str(nivel).strip().lower())
    if severidade is None:
        return None
    return {
        "source": "phishing",
        "timestamp": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "srcIp": ip,
        "eventType": "phishing_detected",
        "severity": severidade,
        "details": {
            "url": url[:500],
            "score": pontuacao,
            "level": nivel,
            "signals": sinais or [],
        },
    }


def _resolver_ip(url):
    host = urlparse(url).hostname
    if not host:
        return "unknown"
    try:
        return socket.gethostbyname(host)
    except OSError:
        return "unknown"


def enviar_alerta_phishing(url, pontuacao, nivel, sinais=None):
    def tarefa():
        alerta = montar_alerta(url, pontuacao, nivel, sinais, _resolver_ip(url))
        if alerta is None:
            return
        try:
            requests.post(SIEM_URL, json=alerta,
                          headers={"X-API-Key": API_KEY}, timeout=2)
        except requests.RequestException:
            pass  # se o SIEM estiver fora do ar, a análise não é afetada

    # Thread para a análise não esperar a rede. Não é daemon de propósito:
    # no modo terminal, o Python espera ela terminar antes de fechar.
    threading.Thread(target=tarefa).start()

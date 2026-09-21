"""
Cliente HTTP para comunicação com a API Django.
Usa a biblioteca requests. Falhas de rede não quebram o jogo.
"""

import requests
from scripts.constantes import API_BASE_URL

TIMEOUT = 3


def cadastrar_jogador(nome_usuario: str, email: str) -> dict | None:
    try:
        r = requests.post(
            f"{API_BASE_URL}/jogador/",
            json={"nome_usuario": nome_usuario, "email": email},
            timeout=TIMEOUT,
        )
        if r.status_code in (200, 201):
            return r.json()
    except Exception:
        pass
    return None


def enviar_pontuacao(nome_usuario: str, pontuacao_total: int, fase_maxima: int) -> dict | None:
    try:
        r = requests.post(
            f"{API_BASE_URL}/pontuacao/",
            json={
                "nome_usuario": nome_usuario,
                "pontuacao_total": pontuacao_total,
                "fase_maxima": fase_maxima,
            },
            timeout=TIMEOUT,
        )
        if r.status_code == 201:
            return r.json()
    except Exception:
        pass
    return None


def obter_ranking() -> list:
    try:
        r = requests.get(f"{API_BASE_URL}/ranking/", timeout=TIMEOUT)
        if r.status_code == 200:
            return r.json()
    except Exception:
        pass
    return []

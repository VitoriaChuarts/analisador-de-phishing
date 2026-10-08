from urllib.parse import urljoin

import requests

from phishing.typosquatting import marca_parecida
from phishing.url_parser import analisar_url

MAX_SALTOS = 5
CODIGOS_REDIRECIONAMENTO = (301, 302, 303, 307, 308)


def seguir_redirecionamentos(url: str, timeout: float = 5) -> list:
    caminho = [url]
    atual = url

    for _ in range(MAX_SALTOS):
        try:
            resposta = requests.get(
                atual, allow_redirects=False, timeout=timeout, stream=True
            )
        except requests.RequestException:
            break

        status = resposta.status_code
        destino = resposta.headers.get("Location")
        resposta.close()

        if status not in CODIGOS_REDIRECIONAMENTO or not destino:
            break

        atual = urljoin(atual, destino)
        caminho.append(atual)

    return caminho


def sinais_do_redirecionamento(info: dict, caminho: list) -> list:
    sinais = []
    if len(caminho) < 2:
        return sinais

    destino = analisar_url(caminho[-1])
    if destino["dominio_registravel"] != info["dominio_registravel"]:
        sinais.append(
            (f"Redireciona para outro domínio: {destino['dominio_registravel']}", 20)
        )
        marca = marca_parecida(destino["dominio"])
        if marca:
            sinais.append((f"O destino final parece com '{marca}'", 35))

    return sinais
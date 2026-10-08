from urllib.parse import urlparse
import tldextract


def analisar_url(url: str) -> dict:
    """Quebra uma URL em partes úteis para análise."""
    if "://" not in url:
        url = "http://" + url

    partes = urlparse(url)
    extraido = tldextract.extract(url)

    if extraido.suffix:
        registravel = f"{extraido.domain}.{extraido.suffix}"
    else:
        registravel = extraido.domain

    return {
        "url_original": url,
        "esquema": partes.scheme,
        "dominio_completo": partes.netloc,
        "host": partes.hostname,
        "subdominio": extraido.subdomain,
        "dominio": extraido.domain,
        "sufixo": extraido.suffix,
        "dominio_registravel": registravel,
        "caminho": partes.path,
        "parametros": partes.query,
    }
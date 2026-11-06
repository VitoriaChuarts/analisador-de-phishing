import ipaddress
import socket
from urllib.parse import urlparse


class RedeBloqueada(ValueError):
    """URL que aponta para uma rede interna ou reservada."""


def validar_url(url: str) -> None:
    if "://" not in url:
        url = "http://" + url

    partes = urlparse(url)

    if partes.scheme not in ("http", "https"):
        raise ValueError("URL inválida: esquema não suportado")

    host = partes.hostname
    if not host:
        raise ValueError("URL inválida: host ausente")

    try:
        caminhos = socket.getaddrinfo(host, None)
    except socket.gaierror:
        return

    for informacao in caminhos:
        texto_ip = informacao[4][0].split("%")[0]
        ip = ipaddress.ip_address(texto_ip)

        if ip.version == 6 and ip.ipv4_mapped:
            ip = ip.ipv4_mapped

        if not ip.is_global or ip.is_multicast:
            raise RedeBloqueada(
                "O endereço aponta para uma rede interna ou reservada."
            )
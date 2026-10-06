import ipaddress

from phishing.typosquatting import marca_parecida

ENCURTADORES = {"bit.ly", "tinyurl.com", "t.co", "goo.gl", "is.gd", "ow.ly", "cutt.ly"}


def eh_ip(texto: str) -> bool:
    try:
        ipaddress.ip_address(texto)
        return True
    except ValueError:
        return False


def detectar_sinais(info: dict) -> list:
    sinais = []

    if eh_ip(info["dominio"]):
        sinais.append(("Usa endereço IP no lugar de um nome de site", 30))

    if "@" in info["dominio_completo"]:
        sinais.append(("Tem '@' no endereço, o que pode esconder o destino real", 25))

    if info["subdominio"]:
        qtd_subdominios = len(info["subdominio"].split("."))
    else:
        qtd_subdominios = 0

    if qtd_subdominios >= 3:
        sinais.append((f"Tem {qtd_subdominios} subdomínios encadeados", 20))

    if info["dominio_registravel"] in ENCURTADORES:
        sinais.append(("Usa encurtador de link, que esconde o destino", 15))

    if info["esquema"] == "http":
        sinais.append(("Não usa HTTPS (conexão sem criptografia)", 10))

    if len(info["url_original"]) > 75:
        sinais.append(("URL muito longa, pode esconder o destino real", 10))

    marca = marca_parecida(info["dominio"])
    if marca:
        sinais.append((f"Nome parecido com a marca '{marca}' (possível typosquatting)", 35))

    return sinais
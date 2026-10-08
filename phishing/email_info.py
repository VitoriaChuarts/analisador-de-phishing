import re
from email import policy
from email.parser import BytesParser
from email.utils import parseaddr

from phishing.typosquatting import MARCAS
from phishing.url_parser import analisar_url

PADRAO_LINK = re.compile(r"https?://[^\s<>()\"']+")


def ler_eml(caminho: str):
    with open(caminho, "rb") as arquivo:
        return BytesParser(policy=policy.default).parse(arquivo)


def extrair_links(mensagem) -> list:
    links = []
    for parte in mensagem.walk():
        if parte.get_content_type() in ("text/plain", "text/html"):
            try:
                texto = parte.get_content()
            except Exception:
                continue
            for link in PADRAO_LINK.findall(texto):
                link = link.rstrip(".,;")
                if link not in links:
                    links.append(link)
    return links


def dominio_do_endereco(cabecalho) -> str:
    if not cabecalho:
        return ""
    _, endereco = parseaddr(str(cabecalho))
    if "@" not in endereco:
        return ""
    dominio = endereco.split("@")[-1].lower()
    return analisar_url(dominio)["dominio_registravel"]


def sinais_do_cabecalho(mensagem) -> list:
    sinais = []

    dominio_from = dominio_do_endereco(mensagem["From"])
    dominio_reply = dominio_do_endereco(mensagem["Reply-To"])
    if dominio_from and dominio_reply and dominio_from != dominio_reply:
        sinais.append(
            (f"Responder-para ({dominio_reply}) difere do remetente ({dominio_from})", 20)
        )

    autenticacao = str(mensagem["Authentication-Results"] or "").lower()
    for falha in ("spf=fail", "dkim=fail", "dmarc=fail"):
        if falha in autenticacao:
            sinais.append((f"Falha de autenticação do remetente ({falha})", 25))
            break

    nome, _ = parseaddr(str(mensagem["From"] or ""))
    nome = nome.lower()
    for marca in MARCAS:
        if marca in nome and marca not in dominio_from:
            sinais.append(
                (f"Nome do remetente cita '{marca}', mas o e-mail vem de {dominio_from}", 30)
            )
            break

    return sinais
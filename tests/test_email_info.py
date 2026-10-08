from email import message_from_string, policy

from phishing.analisador_email import analisar_email
from phishing.email_info import ler_eml, extrair_links, sinais_do_cabecalho

EMAIL_GOLPE = """From: "PayPal Suporte" <suporte@seguro-acesso.xyz>
Reply-To: ajuda@outro-site.com
Subject: Sua conta foi bloqueada
Authentication-Results: mx.exemplo.com; spf=fail smtp.mailfrom=seguro-acesso.xyz
Content-Type: text/plain; charset="utf-8"

Clique para verificar: http://paypa1.com/login e tambem https://www.google.com.
"""

EMAIL_LIMPO = """From: "Maria" <maria@empresa.com>
Subject: Reuniao
Content-Type: text/plain; charset="utf-8"

Oi, segue a pauta da reuniao.
"""


def criar(texto):
    return message_from_string(texto, policy=policy.default)


def total(sinais):
    soma = 0
    for descricao, pontos in sinais:
        soma += pontos
    return soma


def test_extrair_links():
    links = extrair_links(criar(EMAIL_GOLPE))
    assert links == ["http://paypa1.com/login", "https://www.google.com"]


def test_sinais_do_cabecalho_golpe():
    assert total(sinais_do_cabecalho(criar(EMAIL_GOLPE))) == 75


def test_email_limpo_sem_sinais():
    mensagem = criar(EMAIL_LIMPO)
    assert sinais_do_cabecalho(mensagem) == []
    assert extrair_links(mensagem) == []


def test_ler_eml_de_arquivo(tmp_path):
    arquivo = tmp_path / "golpe.eml"
    arquivo.write_text(EMAIL_GOLPE, encoding="utf-8")
    mensagem = ler_eml(str(arquivo))
    assert mensagem["Subject"] == "Sua conta foi bloqueada"


def test_analisar_email_golpe(tmp_path):
    arquivo = tmp_path / "golpe.eml"
    arquivo.write_text(EMAIL_GOLPE, encoding="utf-8")
    r = analisar_email(str(arquivo), consultar_rede=False)
    assert len(r["links"]) == 2
    assert r["nivel"] == "alto"


def test_analisar_email_limpo(tmp_path):
    arquivo = tmp_path / "limpo.eml"
    arquivo.write_text(EMAIL_LIMPO, encoding="utf-8")
    r = analisar_email(str(arquivo), consultar_rede=False)
    assert r["pontuacao"] == 0
    assert r["nivel"] == "baixo"
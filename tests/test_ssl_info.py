from phishing.ssl_info import sinal_certificado
from phishing.ssl_info import verificar_certificado


def test_certificado_nao_conecta_em_rede_interna():
    assert verificar_certificado("127.0.0.1") == "indisponivel"

def test_certificado_invalido_pontua():
    assert sinal_certificado("invalido")[1] == 25


def test_certificado_valido_nao_pontua():
    assert sinal_certificado("valido") is None


def test_certificado_indisponivel_nao_pontua():
    assert sinal_certificado("indisponivel") is None
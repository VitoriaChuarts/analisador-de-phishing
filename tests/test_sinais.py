from phishing.url_parser import analisar_url
from phishing.sinais import detectar_sinais


def total_pontos(url):
    total = 0
    for descricao, pontos in detectar_sinais(analisar_url(url)):
        total += pontos
    return total


def test_site_normal_nao_tem_sinais():
    assert total_pontos("https://www.google.com") == 0


def test_ip_e_http():
    assert total_pontos("http://192.168.0.1/login") == 40


def test_arroba_escondendo_destino():
    assert total_pontos("https://paypal.com@evil.com/login") == 25


def test_encurtador():
    assert total_pontos("https://bit.ly/abc123") == 15


def test_subdominios_demais():
    assert total_pontos("https://login.paypal.com.seguro-acesso.xyz/verify") == 20
    
def test_url_muito_longa():
    url_longa = "https://www.google.com/" + "a" * 80
    assert total_pontos(url_longa) == 10
    
def test_typosquatting_paypal():
    assert total_pontos("https://paypa1.com/login") == 35
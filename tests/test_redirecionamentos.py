from phishing.url_parser import analisar_url
from phishing.redirecionamentos import sinais_do_redirecionamento


def total(sinais):
    soma = 0
    for descricao, pontos in sinais:
        soma += pontos
    return soma


def test_sem_redirecionamento():
    info = analisar_url("https://www.google.com")
    assert sinais_do_redirecionamento(info, ["https://www.google.com"]) == []


def test_redireciona_para_o_mesmo_dominio():
    info = analisar_url("http://google.com")
    caminho = ["http://google.com", "https://www.google.com/"]
    assert sinais_do_redirecionamento(info, caminho) == []


def test_redireciona_para_outro_dominio():
    info = analisar_url("https://bit.ly/abc123")
    caminho = ["https://bit.ly/abc123", "https://exemplo-seguro.com/pagina"]
    assert total(sinais_do_redirecionamento(info, caminho)) == 20


def test_destino_final_imita_marca():
    info = analisar_url("https://bit.ly/abc123")
    caminho = ["https://bit.ly/abc123", "https://paypa1.com/login"]
    assert total(sinais_do_redirecionamento(info, caminho)) == 55
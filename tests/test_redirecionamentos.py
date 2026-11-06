from phishing.url_parser import analisar_url
from phishing.redirecionamentos import sinais_do_redirecionamento
from phishing import redirecionamentos


class RespostaFalsa:
    def __init__(self, status, location=None):
        self.status_code = status
        self.headers = {"Location": location} if location else {}

    def close(self):
        pass


def test_nao_segue_redirecionamento_para_rede_interna(monkeypatch):
    chamadas = []

    def get_falso(url, **kwargs):
        chamadas.append(url)
        return RespostaFalsa(302, "http://127.0.0.1/admin")

    monkeypatch.setattr(redirecionamentos.requests, "get", get_falso)

    caminho = redirecionamentos.seguir_redirecionamentos("http://8.8.8.8/")

    assert chamadas == ["http://8.8.8.8/"]
    assert caminho[-1] == "http://127.0.0.1/admin"
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
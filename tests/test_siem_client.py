from phishing.siem_client import montar_alerta


def test_risco_baixo_nao_gera_alerta():
    assert montar_alerta("http://a.com", 5, "baixo", [], "1.2.3.4") is None


def test_risco_alto_gera_alerta_high():
    alerta = montar_alerta("http://a.com", 90, "alto", ["typosquatting"], "1.2.3.4")
    assert alerta["source"] == "phishing"
    assert alerta["severity"] == "high"
    assert alerta["srcIp"] == "1.2.3.4"


def test_risco_medio_com_acento():
    assert montar_alerta("http://a.com", 50, "médio", [], "1.2.3.4")["severity"] == "medium"

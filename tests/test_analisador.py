from phishing.analisador import analisar


def test_site_limpo():
    r = analisar("https://www.google.com", consultar_rede=False)
    assert r["pontuacao"] == 0
    assert r["sinais"] == []


def test_typosquatting_pontua():
    r = analisar("https://paypa1.com/login", consultar_rede=False)
    assert r["pontuacao"] == 35
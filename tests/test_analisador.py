from phishing.analisador import analisar, classificar


def test_site_limpo():
    r = analisar("https://www.google.com", consultar_rede=False)
    assert r["pontuacao"] == 0
    assert r["sinais"] == []


def test_typosquatting_pontua():
    r = analisar("https://paypa1.com/login", consultar_rede=False)
    assert r["pontuacao"] == 35
    
def test_classificar_baixo():
    assert classificar(0) == "baixo"
    assert classificar(19) == "baixo"


def test_classificar_medio():
    assert classificar(20) == "médio"
    assert classificar(49) == "médio"


def test_classificar_alto():
    assert classificar(50) == "alto"
    assert classificar(100) == "alto"


def test_resultado_tem_nivel():
    r = analisar("https://paypa1.com/login", consultar_rede=False)
    assert r["nivel"] == "médio"
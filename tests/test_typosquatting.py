from phishing.typosquatting import distancia_edicao, marca_parecida


def test_distancia_palavras_iguais():
    assert distancia_edicao("paypal", "paypal") == 0


def test_distancia_uma_troca():
    assert distancia_edicao("paypa1", "paypal") == 1


def test_distancia_letra_extra():
    assert distancia_edicao("gooogle", "google") == 1


def test_marca_parecida_encontra_imitacoes():
    assert marca_parecida("paypa1") == "paypal"
    assert marca_parecida("gooogle") == "google"
    assert marca_parecida("g00gle") == "google"


def test_marca_original_nao_e_suspeita():
    assert marca_parecida("paypal") is None


def test_nome_sem_relacao():
    assert marca_parecida("mercado") is None
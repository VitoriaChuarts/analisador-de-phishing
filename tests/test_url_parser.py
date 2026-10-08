from phishing.url_parser import analisar_url


def test_dominio_real_escondido_em_subdominio():
    r = analisar_url("https://login.paypal.com.seguro-acesso.xyz/verify")
    assert r["dominio_registravel"] == "seguro-acesso.xyz"
    assert r["subdominio"] == "login.paypal.com"


def test_sufixo_composto():
    r = analisar_url("https://www.banco.com.br")
    assert r["dominio_registravel"] == "banco.com.br"
    
def test_host_ignora_usuario_e_porta():
    r = analisar_url("https://paypal.com@evil.com:8080/x")
    assert r["host"] == "evil.com"
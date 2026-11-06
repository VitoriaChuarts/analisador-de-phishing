import pytest

from phishing.validar_rede import RedeBloqueada, validar_url


@pytest.mark.parametrize(
    "url",
    [
        "http://127.0.0.1:8000/historico",
        "http://localhost/",
        "http://169.254.169.254/latest/meta-data",
        "http://10.0.0.5/",
        "http://192.168.1.1/",
        "http://[::1]/",
    ],
)
def test_bloqueia_redes_internas(url):
    with pytest.raises(RedeBloqueada):
        validar_url(url)


@pytest.mark.parametrize(
    "url",
    ["file:///etc/passwd", "ftp://exemplo.com/arquivo"],
)
def test_bloqueia_esquemas_invalidos(url):
    with pytest.raises(ValueError):
        validar_url(url)


def test_aceita_ip_publico():
    validar_url("http://8.8.8.8/")
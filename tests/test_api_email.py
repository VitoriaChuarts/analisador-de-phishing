from pathlib import Path

from fastapi.testclient import TestClient

from api import app

cliente = TestClient(app)
EXEMPLO = Path(__file__).parent.parent / "exemplos" / "golpe.eml"


def test_aceita_eml_valido():
    with open(EXEMPLO, "rb") as arquivo:
        resposta = cliente.post(
            "/analisar/email",
            files={"arquivo": ("golpe.eml", arquivo, "message/rfc822")},
        )
    assert resposta.status_code == 200
    assert "pontuacao" in resposta.json()


def test_recusa_extensao_errada():
    resposta = cliente.post(
        "/analisar/email",
        files={"arquivo": ("virus.exe", b"conteudo", "application/octet-stream")},
    )
    assert resposta.status_code == 400


def test_recusa_arquivo_grande():
    grande = b"a" * (2 * 1024 * 1024 + 1)
    resposta = cliente.post(
        "/analisar/email",
        files={"arquivo": ("grande.eml", grande, "message/rfc822")},
    )
    assert resposta.status_code == 413


def test_recusa_arquivo_que_nao_e_email():
    resposta = cliente.post(
        "/analisar/email",
        files={"arquivo": ("texto.eml", b"isto nao e um email", "message/rfc822")},
    )
    assert resposta.status_code == 400
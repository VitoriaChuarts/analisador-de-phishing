import sys
from pathlib import Path

from main import main

EXEMPLO = Path(__file__).parent.parent / "exemplos" / "golpe.eml"


def test_main_com_link(capsys, monkeypatch):
    monkeypatch.setattr(sys, "argv", ["main.py", "https://paypa1.com/login"])
    main()
    saida = capsys.readouterr().out
    assert "RISCO MÉDIO" in saida
    assert "paypal" in saida


def test_main_com_email(capsys, monkeypatch):
    monkeypatch.setattr(sys, "argv", ["main.py", str(EXEMPLO)])
    main()
    saida = capsys.readouterr().out
    assert "RISCO ALTO" in saida
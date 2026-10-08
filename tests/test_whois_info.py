from datetime import datetime, timedelta, timezone

from phishing.whois_info import idade_em_dias, sinal_idade


def test_idade_em_dias_com_fuso():
    data = datetime.now(timezone.utc) - timedelta(days=10)
    assert idade_em_dias(data) == 10


def test_idade_em_dias_sem_fuso():
    data = datetime.now(timezone.utc).replace(tzinfo=None) - timedelta(days=5)
    assert idade_em_dias(data) == 5


def test_idade_sem_data():
    assert idade_em_dias(None) is None


def test_sinal_dominio_muito_novo():
    assert sinal_idade(10)[1] == 30


def test_sinal_dominio_recente():
    assert sinal_idade(100)[1] == 15


def test_sinal_dominio_antigo():
    assert sinal_idade(1000) is None
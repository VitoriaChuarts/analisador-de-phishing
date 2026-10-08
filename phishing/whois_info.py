from datetime import datetime, timezone

import whois


def obter_data_criacao(dominio: str):
    try:
        dados = whois.whois(dominio)
    except Exception:
        return None

    data = dados.creation_date
    if isinstance(data, list):
        data = data[0]
    if not isinstance(data, datetime):
        return None
    return data


def idade_em_dias(data_criacao):
    if data_criacao is None:
        return None
    if data_criacao.tzinfo is None:
        data_criacao = data_criacao.replace(tzinfo=timezone.utc)
    agora = datetime.now(timezone.utc)
    return (agora - data_criacao).days


def sinal_idade(idade_dias):
    if idade_dias is None:
        return None
    if idade_dias < 30:
        return (f"Domínio criado há apenas {idade_dias} dias", 30)
    if idade_dias < 180:
        return (f"Domínio criado há {idade_dias} dias (recente)", 15)
    return None
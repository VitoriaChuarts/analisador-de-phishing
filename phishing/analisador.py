from phishing.url_parser import analisar_url
from phishing.sinais import detectar_sinais
from phishing.whois_info import obter_data_criacao, idade_em_dias, sinal_idade
from phishing.ssl_info import verificar_certificado, sinal_certificado
from phishing.redirecionamentos import (
    seguir_redirecionamentos,
    sinais_do_redirecionamento,
)


def classificar(pontuacao: int) -> str:
    if pontuacao >= 50:
        return "alto"
    if pontuacao >= 20:
        return "médio"
    return "baixo"


def analisar(url: str, consultar_rede: bool = True) -> dict:
    info = analisar_url(url)
    sinais = detectar_sinais(info)

    if consultar_rede:
        data = obter_data_criacao(info["dominio_registravel"])
        sinal = sinal_idade(idade_em_dias(data))
        if sinal:
            sinais.append(sinal)

        if info["esquema"] == "https" and info["host"]:
            sinal = sinal_certificado(verificar_certificado(info["host"]))
            if sinal:
                sinais.append(sinal)

        caminho = seguir_redirecionamentos(info["url_original"])
        sinais.extend(sinais_do_redirecionamento(info, caminho))

    pontuacao = 0
    for descricao, pontos in sinais:
        pontuacao += pontos
    pontuacao = min(pontuacao, 100)

    return {
        "url": url,
        "sinais": sinais,
        "pontuacao": pontuacao,
        "nivel": classificar(pontuacao),
    }
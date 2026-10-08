from phishing.analisador import analisar
from phishing.analisador import classificar
from phishing.email_info import ler_eml, extrair_links, sinais_do_cabecalho


def analisar_email(caminho: str, consultar_rede: bool = False) -> dict:
    mensagem = ler_eml(caminho)
    sinais = sinais_do_cabecalho(mensagem)

    resultados = []
    maior = 0
    for link in extrair_links(mensagem):
        resultado = analisar(link, consultar_rede=consultar_rede)
        resultados.append(resultado)
        if resultado["pontuacao"] > maior:
            maior = resultado["pontuacao"]

    pontos_cabecalho = 0
    for descricao, pontos in sinais:
        pontos_cabecalho += pontos

    pontuacao = min(pontos_cabecalho + maior, 100)

    return {
        "arquivo": caminho,
        "assunto": str(mensagem["Subject"] or "(sem assunto)"),
        "sinais_cabecalho": sinais,
        "links": resultados,
        "pontuacao": pontuacao,
        "nivel": classificar(pontuacao),
    }
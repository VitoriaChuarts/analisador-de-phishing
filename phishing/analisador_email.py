from phishing.analisador import analisar
from phishing.analisador import classificar
from phishing.email_info import ler_eml, extrair_links, sinais_do_cabecalho

MAX_LINKS = 20


def analisar_mensagem(mensagem, nome: str, consultar_rede: bool = False) -> dict:
    sinais = sinais_do_cabecalho(mensagem)
    todos_links = extrair_links(mensagem)

    resultados = []
    maior = 0
    for link in todos_links[:MAX_LINKS]:
        try:
            resultado = analisar(link, consultar_rede=consultar_rede)
        except ValueError:
            continue
        resultados.append(resultado)
        if resultado["pontuacao"] > maior:
            maior = resultado["pontuacao"]

    pontos_cabecalho = 0
    for descricao, pontos in sinais:
        pontos_cabecalho += pontos

    pontuacao = min(pontos_cabecalho + maior, 100)

    return {
        "arquivo": nome,
        "assunto": str(mensagem["Subject"] or "(sem assunto)"),
        "sinais_cabecalho": sinais,
        "links": resultados,
        "links_ignorados": max(0, len(todos_links) - MAX_LINKS),
        "pontuacao": pontuacao,
        "nivel": classificar(pontuacao),
    }


def analisar_email(caminho: str, consultar_rede: bool = False) -> dict:
    mensagem = ler_eml(caminho)
    return analisar_mensagem(mensagem, caminho, consultar_rede)
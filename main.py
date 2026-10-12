import sys

from rich.console import Console
from rich.markup import escape
from rich.panel import Panel
from rich.table import Table

from phishing.analisador import analisar
from phishing.analisador_email import analisar_email

console = Console()
CORES = {"baixo": "green", "médio": "yellow", "alto": "red"}


def painel_risco(resultado: dict) -> Panel:
    cor = CORES[resultado["nivel"]]
    texto = f"[bold {cor}]RISCO {resultado['nivel'].upper()}[/]  {resultado['pontuacao']}/100"
    return Panel(texto, expand=False)


def tabela_sinais(sinais: list, titulo: str) -> Table:
    tabela = Table(title=titulo)
    tabela.add_column("Pontos", justify="right")
    tabela.add_column("Sinal")
    for descricao, pontos in sinais:
        tabela.add_row(f"+{pontos}", escape(descricao))
    return tabela


def main():
    if len(sys.argv) < 2:
        console.print("Uso: python main.py <link ou arquivo.eml> [--rede]")
        return

    alvo = sys.argv[1].strip('"')
    usar_rede = "--rede" in sys.argv

    if alvo.lower().endswith(".eml"):
        resultado = analisar_email(alvo, consultar_rede=usar_rede)
        console.print(f"[bold]E-mail:[/] {escape(resultado['assunto'])}")
        console.print(painel_risco(resultado))
        if resultado["sinais_cabecalho"]:
            console.print(tabela_sinais(resultado["sinais_cabecalho"], "Cabeçalho"))
        for item in resultado["links"]:
            console.print(
                f"\n[bold]Link:[/] {escape(item['url'])}  "
                f"({item['nivel']}, {item['pontuacao']}/100)"
            )
            if item["sinais"]:
                console.print(tabela_sinais(item["sinais"], "Sinais do link"))
    else:
        resultado = analisar(alvo, consultar_rede=usar_rede)
        console.print(painel_risco(resultado))
        if resultado["sinais"]:
            console.print(tabela_sinais(resultado["sinais"], "Sinais encontrados"))
        else:
            console.print("Nenhum sinal suspeito encontrado.")


if __name__ == "__main__":
    main()
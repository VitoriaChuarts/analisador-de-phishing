from phishing.analisador_email import analisar_email

caminho = input("Caminho do arquivo .eml: ").strip().strip('"')
resposta = input("Consultar a internet nos links do e-mail? [s/n]: ")
usar_rede = resposta.strip().lower() == "s"

resultado = analisar_email(caminho, consultar_rede=usar_rede)

print()
print(f"Assunto: {resultado['assunto']}")
print(f"Risco {resultado['nivel'].upper()}: {resultado['pontuacao']}/100")

if resultado["sinais_cabecalho"]:
    print("Sinais no cabeçalho:")
    for descricao, pontos in resultado["sinais_cabecalho"]:
        print(f"  +{pontos}  {descricao}")

print(f"Links encontrados: {len(resultado['links'])}")
for item in resultado["links"]:
    print(f"  [{item['nivel'].upper()} {item['pontuacao']}] {item['url']}")
    for descricao, pontos in item["sinais"]:
        print(f"        +{pontos}  {descricao}")
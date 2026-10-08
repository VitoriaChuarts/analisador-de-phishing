from phishing.analisador import analisar

url = input("Cole o link para verificação veridica do site : ")
resposta = input("Consultar a internet (WHOIS, certificado, redirecionamentos)? [s/n]: ")
usar_rede = resposta.strip().lower() == "s"

resultado = analisar(url, consultar_rede=usar_rede)

print()
print(f"Pontuação em escala de risco: {resultado['pontuacao']}/100")

if resultado["sinais"]:
    print("Sinais encontrados:")
    for descricao, pontos in resultado["sinais"]:
        print(f"  +{pontos}  {descricao}")
else:
    print("Nenhum sinal suspeito encontrado. Site parece seguro.")
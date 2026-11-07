# 🛡️ Analisador de Phishing

Aplicação full stack que analisa **URLs** e **e-mails (.eml)** e devolve uma pontuação de risco de 0 a 100, com os sinais que justificam a nota.

![Painel com resultado de alto risco](docs/painel-alto.png)

## O que ele faz

- **Análise de URL:** estrutura da URL, typosquatting (nomes parecidos com marcas), TLDs suspeitos, certificado SSL, dados de WHOIS e cadeia de redirecionamentos.
- **Análise de e-mail (.eml):** `Reply-To` diferente do remetente, falha de SPF/DKIM/DMARC, nome de marca no remetente e análise de cada link encontrado.
- **Histórico** de análises salvo em banco de dados.
- **Links neutralizados** na tela (`hxxp://exemplo[.]com`), para ninguém clicar sem querer num golpe.

## Segurança da própria ferramenta

Uma ferramenta que acessa URLs digitadas por outras pessoas também precisa se proteger. O projeto inclui:

- **Proteção contra SSRF:** antes de acessar qualquer endereço, o domínio é resolvido e bloqueado se apontar para rede interna, loopback ou endereço reservado. A checagem vale para a URL inicial, para **cada salto de redirecionamento** e para a verificação de SSL.
- **Limites de redirecionamento e tempo de espera** nas requisições.
- **Upload seguro de `.eml`:** limite de 2 MB, validação da extensão e do conteúdo, leitura em memória (o arquivo não é gravado em disco) e limite de 20 links analisados por e-mail.
- **Frontend sem XSS:** o conteúdo é inserido com `textContent`, nunca com `innerHTML`.
- Validação de tamanho da URL na API e testes automatizados para esses casos.

## Tecnologias

Python · FastAPI · SQLAlchemy · SQLite · HTML, CSS e JavaScript · pytest

## Como rodar

```bash
git clone https://github.com/VitoriaChuarts/analisador-de-phishing.git
cd analisador-de-phishing
python -m venv .venv
```

Ative o ambiente virtual (Windows: `.venv\Scripts\activate` · Linux/macOS: `source .venv/bin/activate`) e instale as dependências:

```bash
pip install -r requirements.txt
uvicorn api:app --reload
```

Abra `http://127.0.0.1:8000` no navegador. A documentação automática da API fica em `http://127.0.0.1:8000/docs`.

## API

| Método | Rota | Descrição |
|---|---|---|
| POST | `/analisar/url` | Analisa uma URL (`url`, `consultar_rede`) |
| POST | `/analisar/email` | Analisa um arquivo `.eml` enviado por upload |
| GET | `/historico` | Lista as últimas análises |

## Testes

```bash
python -m pytest tests -v
```

## Estrutura

```
api.py              rotas da API
bancodados.py       modelo e conexão com o banco
phishing/           regras de análise (URL, SSL, WHOIS, redirecionamentos, e-mail)
frontend/           interface web
tests/              testes automatizados
exemplos/           e-mails de exemplo
```

## Limitações e próximos passos

- A validação contra SSRF resolve o DNS antes da requisição. Uma defesa completa contra *DNS rebinding* exigiria conectar direto ao IP já validado.
- Integração com bases de reputação (VirusTotal, PhishTank), mapeamento MITRE ATT&CK e exportação de relatório.
- Docker e deploy.

## Aviso

Projeto educacional. A pontuação é uma estimativa baseada em regras e não substitui a análise de um profissional de segurança.
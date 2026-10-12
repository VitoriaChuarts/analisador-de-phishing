# 🛡️ Analisador de Phishing

O **Analisador de Phishing** é uma ferramenta desenvolvida em Python para automatizar a verificação e classificação de e-mails suspeitos, identificando padrões de ataques de *phishing*, falsificação de identidade (spoofing) e links maliciosos.

> ⚠️ **Projeto em Construção:** Este projeto está a ser desenvolvido ativamente como demonstração de boas práticas de código, testes automatizados e conceitos de Cibersegurança.

---

##  Funcionalidades Atuais

- **Análise de Cabeçalhos:** Verificação do remetente e validação básica de autenticação (SPF / DKIM / DMARC).
-  **Análise de URLs e Domínios:**
  - Deteção de ligações inseguras (ausência de HTTPS).
  - Identificação de domínios com nomes semelhantes a marcas conhecidas (*typosquatting* / *lookalike domains*).
  - Verificação de caracteres e padrões de ocultação.
-  **Classificação por Nível de Risco:** Cálculo de pontuação com base nos sinais identificados no e-mail (Risco Alto, Médio, Baixo).
-  **Testes Automatizados:** Suíte de testes cobrindo múltiplos cenários com `pytest`.

---

##  Tecnologias Utilizadas

- **Linguagem:** [Python 3](https://www.python.org/)
- **Testes:** [pytest](https://docs.pytest.org/)
- **Ferramentas de Desenvolvimento:** VS Code, Git/GitHub

---

##  Como Executar o Projeto

### Pré-requisitos
- Python 3.8 ou superior instalado.

### Passo a Passo

1. **Clonar o repositório:**
   ```bash
   git clone [https://github.com/VitoriaChuarts/analisador-de-phishing.git](https://github.com/VitoriaChuarts/analisador-de-phishing.git)
   cd analisador-de-phishing

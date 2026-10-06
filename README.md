# Analisador de Phishing

Ferramenta em Python que analisa links suspeitos e calcula uma pontuação de risco de 0 a 100.

## O que ela detecta

- Endereço IP no lugar de nome de site
- `@` escondendo o destino real
- Subdomínios encadeados (ex.: `login.paypal.com.golpe.xyz`)
- Encurtadores de link e URLs muito longas
- Falta de HTTPS
- Typosquatting (ex.: `paypa1.com`), usando distância de edição
- Domínios criados recentemente (consulta WHOIS)

## Como rodar

    python -m venv .venv
    .venv\Scripts\activate
    pip install -r requirements.txt
    python demo.py

## Testes

    python -m pytest

## Aviso

Projeto educacional e defensivo. A ferramenta não acessa o site analisado.

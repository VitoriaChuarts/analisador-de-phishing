import json

from fastapi import FastAPI, File, Form, HTTPException, Query, UploadFile
from fastapi import FastAPI, File, Form, HTTPException, Query, UploadFile
from phishing.analisador_email import analisar_mensagem
from phishing.email_info import ler_eml_bytes
from pydantic import BaseModel
from sqlalchemy import select

from bancodados import Analise, SessionLocal, criar_tabelas
from phishing.analisador import analisar

from pathlib import Path

from fastapi.staticfiles import StaticFiles

from pydantic import BaseModel, Field

from phishing.validar_rede import validar_url

criar_tabelas()

app = FastAPI(
    title="Analisador de Phishing",
    description="API que analisa URLs e retorna uma pontuação de risco",
    version="1.0.0",
)
LIMITE_EML = 2 * 1024 * 1024  # 2 MB
  
class PedidoUrl(BaseModel):
    url: str = Field(max_length=2048)
    consultar_rede: bool = True


@app.get("/nivel")
def nivel():
    return {"status": "Nível de análise"}


@app.post("/analisar/url")
def analisar_url(pedido: PedidoUrl):
    try:
        resultado = analisar(pedido.url, pedido.consultar_rede)
    except ValueError as erro:
        raise HTTPException(status_code=400, detail=str(erro))
    except Exception:
        raise HTTPException(status_code=500, detail="Erro ao analisar a URL")

    sinais = [
        {"descricao": descricao, "pontos": pontos}
        for descricao, pontos in resultado["sinais"]
    ]

    with SessionLocal() as sessao:
        registro = Analise(
            url=resultado["url"],
            pontuacao=resultado["pontuacao"],
            nivel=resultado["nivel"],
            sinais_json=json.dumps(sinais, ensure_ascii=False),
        )
        sessao.add(registro)
        sessao.commit()

    return {
        "url": resultado["url"],
        "pontuacao": resultado["pontuacao"],
        "nivel": resultado["nivel"],
        "sinais": sinais,
    }


@app.get("/historico")
def historico(limite: int = Query(20, ge=1, le=100)):
    with SessionLocal() as sessao:
        consulta = select(Analise).order_by(Analise.id.desc()).limit(limite)
        registros = sessao.scalars(consulta).all()

        return [
            {
                "id": r.id,
                "url": r.url,
                "pontuacao": r.pontuacao,
                "nivel": r.nivel,
                "sinais": json.loads(r.sinais_json),
                "criado_em": r.criado_em.isoformat(),
            }
            for r in registros
        ]
@app.post("/analisar/email")
def analisar_email_upload(
    arquivo: UploadFile = File(...),
    consultar_rede: bool = Form(False),
):
    nome = Path(arquivo.filename or "email.eml").name[:100]
    if not nome.lower().endswith(".eml"):
        raise HTTPException(status_code=400, detail="Envie um arquivo .eml")

    dados = arquivo.file.read(LIMITE_EML + 1)
    if len(dados) > LIMITE_EML:
        raise HTTPException(status_code=413, detail="Arquivo maior que 2 MB")
    if not dados.strip():
        raise HTTPException(status_code=400, detail="Arquivo vazio")

    try:
        mensagem = ler_eml_bytes(dados)
        if not (mensagem["From"] or mensagem["Subject"]):
            raise ValueError("O arquivo não parece ser um e-mail válido")
        resultado = analisar_mensagem(mensagem, nome, consultar_rede)
    except ValueError as erro:
        raise HTTPException(status_code=400, detail=str(erro))
    except Exception:
        raise HTTPException(status_code=500, detail="Erro ao analisar o e-mail")

    sinais = [
        {"descricao": descricao, "pontos": pontos}
        for descricao, pontos in resultado["sinais_cabecalho"]
    ]
    links = [
        {
            "url": r["url"],
            "pontuacao": r["pontuacao"],
            "nivel": r["nivel"],
            "sinais": [
                {"descricao": descricao, "pontos": pontos}
                for descricao, pontos in r["sinais"]
            ],
        }
        for r in resultado["links"]
    ]
    assunto = resultado["assunto"][:150]

    with SessionLocal() as sessao:
        registro = Analise(
            url=f"[e-mail] {assunto}",
            pontuacao=resultado["pontuacao"],
            nivel=resultado["nivel"],
            sinais_json=json.dumps(sinais, ensure_ascii=False),
        )
        sessao.add(registro)
        sessao.commit()

    return {
        "arquivo": nome,
        "assunto": assunto,
        "pontuacao": resultado["pontuacao"],
        "nivel": resultado["nivel"],
        "sinais": sinais,
        "links": links,
        "links_ignorados": resultado["links_ignorados"],
    }        
PASTA_FRONTEND = Path(__file__).parent / "frontend"
app.mount("/", StaticFiles(directory=PASTA_FRONTEND, html=True), name="frontend")
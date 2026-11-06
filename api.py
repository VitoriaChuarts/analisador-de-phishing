import json

from fastapi import FastAPI, HTTPException, Query
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
        
PASTA_FRONTEND = Path(__file__).parent / "frontend"
app.mount("/", StaticFiles(directory=PASTA_FRONTEND, html=True), name="frontend")
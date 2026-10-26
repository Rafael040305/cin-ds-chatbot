from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from src.ingest import indexar_documento
from src.retriever import buscar_contexto


app = FastAPI(
    title="SecGrad AI Microservice",
    description=(
        "Serviço de RAG e busca vetorial "
        "para o Chatbot SecGrad"
    ),
    version="1.0.0",
)


class ConsultaRequest(BaseModel):
    pergunta: str
    curso: str = "Geral"
    perfil: str = "Todos"
    top_k: int = 3


class IngestaoRequest(BaseModel):
    caminho_pdf: str
    curso: str = "Geral"
    perfil: str = "Todos"
    categoria: str = "Geral"


@app.get("/health")
def health_check():
    """
    Verificação utilizada pelo Docker e pelo NestJS.
    """

    return {
        "status": "ok",
        "service": "ai-service",
    }


@app.post("/api/v1/buscar")
def rota_buscar(
    requisicao: ConsultaRequest,
):
    """
    Recupera contexto documental para o NestJS.
    """

    try:
        return buscar_contexto(
            pergunta=requisicao.pergunta,
            curso=requisicao.curso,
            perfil=requisicao.perfil,
            top_k=requisicao.top_k,
        )

    except ValueError as erro:
        raise HTTPException(
            status_code=422,
            detail=str(erro),
        ) from erro


@app.post("/api/v1/ingestar")
def rota_ingestar(
    requisicao: IngestaoRequest,
):
    """
    Indexa manualmente um documento.

    A ingestão normal do projeto deve utilizar
    o catálogo e o comando src.ingest_batch.
    """

    metadados = {
        "curso_alvo": [
            requisicao.curso
        ],
        "perfil_curricular": (
            requisicao.perfil
        ),
        "tipo_documento": (
            requisicao.categoria
        ),
    }

    try:
        return indexar_documento(
            caminho_arquivo=(
                requisicao.caminho_pdf
            ),
            metadados_personalizados=(
                metadados
            ),
        )

    except ValueError as erro:
        raise HTTPException(
            status_code=422,
            detail=str(erro),
        ) from erro
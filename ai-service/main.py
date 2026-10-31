from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field, StrictInt, field_validator

from src.generation import GenerationUnavailable, gerar_resposta

from src.ingest import indexar_documento
from src.retriever import InvalidSearchResult, buscar_contexto


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
    top_k: StrictInt = Field(default=3, ge=1)


class GeracaoRequest(BaseModel):
    pergunta: str = Field(max_length=10000)
    contexto: str = Field(max_length=100000)

    @field_validator("pergunta")
    @classmethod
    def pergunta_nao_vazia(cls, valor: str) -> str:
        if not valor.strip():
            raise ValueError("A pergunta não pode estar vazia.")
        return valor.strip()


class GeracaoResponse(BaseModel):
    resposta: str | None


@app.post("/api/v1/gerar", response_model=GeracaoResponse)
def rota_gerar(requisicao: GeracaoRequest):
    try:
        return {"resposta": gerar_resposta(requisicao.pergunta, requisicao.contexto)}
    except GenerationUnavailable as erro:
        raise HTTPException(status_code=503, detail="Serviço de geração indisponível.") from erro


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

    except InvalidSearchResult as erro:
        raise HTTPException(status_code=502, detail="Resposta inválida do serviço de busca.") from erro
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

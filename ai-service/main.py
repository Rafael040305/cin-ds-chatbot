from fastapi import FastAPI
from pydantic import BaseModel
from src.retriever import buscar_contexto
from src.ingest import indexar_pdf

app = FastAPI(
    title="SecGrad AI Microservice",
    description="Serviço de RAG e Busca Vetorial para o Chatbot SecGrad",
    version="1.0.0"
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
    """Endpoint de checagem para o Docker Compose e NestJS."""
    return {"status": "ok", "service": "ai-service"}

@app.post("/api/v1/buscar")
def rota_buscar(req: ConsultaRequest):
    """Endpoint chamado pelo NestJS para buscar contexto semântico."""
    resultado = buscar_contexto(
        pergunta=req.pergunta,
        curso=req.curso,
        perfil=req.perfil,
        top_k=req.top_k
    )
    return resultado

@app.post("/api/v1/ingestar")
def rota_ingestar(req: IngestaoRequest):
    """Endpoint para indexar novos documentos."""
    meta = {
        "curso": req.curso,
        "perfil": req.perfil,
        "categoria": req.categoria
    }
    return indexar_pdf(req.caminho_pdf, meta)
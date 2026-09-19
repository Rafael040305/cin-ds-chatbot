import os
import chromadb
from pypdf import PdfReader
from langchain_text_splitters import RecursiveCharacterTextSplitter

# Banco vetorial persistente no disco
CHROMA_PATH = "./chroma_db"
client = chromadb.PersistentClient(path=CHROMA_PATH)
collection = client.get_or_create_collection(name="secgrad_knowledge_base")

def indexar_pdf(caminho_pdf: str, metadados: dict):
    """
    Lê o PDF, fatia o texto mantendo as páginas e metadados,
    e persiste os vetores no ChromaDB.
    """
    if not os.path.exists(caminho_pdf):
        print(f"Erro: Arquivo '{caminho_pdf}' não encontrado.")
        return {"sucesso": False, "erro": "Arquivo não encontrado"}

    reader = PdfReader(caminho_pdf)
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=700,
        chunk_overlap=120,
        separators=["\n\n", "\n", ". ", " "]
    )

    chunks = []
    metadatas = []
    ids = []
    nome_arquivo = os.path.basename(caminho_pdf)

    for num_pagina, pagina in enumerate(reader.pages, start=1):
        texto = pagina.extract_text() or ""
        if not texto.strip():
            continue

        pedacos = splitter.split_text(texto)
        for i, pedaco in enumerate(pedacos):
            meta_chunk = metadados.copy()
            meta_chunk["source"] = nome_arquivo
            meta_chunk["page"] = num_pagina

            chunks.append(pedaco)
            metadatas.append(meta_chunk)
            ids.append(f"{nome_arquivo}_p{num_pagina}_c{i}")

    if chunks:
        collection.upsert(
            documents=chunks,
            metadatas=metadatas,
            ids=ids
        )
        print(f"Sucesso: {len(chunks)} trechos indexados de '{nome_arquivo}'.")
        return {"sucesso": True, "chunks_indexados": len(chunks)}
    
    return {"sucesso": False, "erro": "Nenhum texto extraído do PDF"}
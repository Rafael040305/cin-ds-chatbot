import chromadb

CHROMA_PATH = "./chroma_db"
client = chromadb.PersistentClient(path=CHROMA_PATH)
collection = client.get_or_create_collection(name="secgrad_knowledge_base")

def buscar_contexto(pergunta: str, curso: str = "Geral", perfil: str = "Todos", top_k: int = 3) -> dict:
    """
    Recupera trechos relevantes do ChromaDB com filtros de metadados.
    Retorna o contexto formatado, lista de fontes auditáveis e distância.
    """
    filtros = []
    if curso and curso != "Geral":
        filtros.append({"curso": {"$in": [curso, "Geral"]}})
    if perfil and perfil != "Todos":
        filtros.append({"perfil": {"$in": [perfil, "Todos"]}})

    where_filter = None
    if len(filtros) == 1:
        where_filter = filtros[0]
    elif len(filtros) > 1:
        where_filter = {"$and": filtros}

    resultados = collection.query(
        query_texts=[pergunta],
        n_results=top_k,
        where=where_filter
    )

    documentos = resultados["documents"][0] if resultados["documents"] else []
    metadados = resultados["metadatas"][0] if resultados["metadatas"] else []
    distancias = resultados["distances"][0] if "distances" in resultados and resultados["distances"] else []

    contexto_formatado = []
    fontes = []

    for doc, meta in zip(documentos, metadados):
        tag = f"[Documento: {meta['source']} | Pág. {meta['page']} | Curso: {meta.get('curso', 'Geral')}]"
        contexto_formatado.append(f"{tag}\n{doc}")
        fontes.append({
            "arquivo": meta["source"],
            "pagina": meta["page"],
            "curso": meta.get("curso", "Geral")
        })

    return {
        "contexto": "\n\n---\n\n".join(contexto_formatado),
        "fontes": fontes,
        "distancia_minima": distancias[0] if distancias else 1.0
    }
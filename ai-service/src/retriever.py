import os
import chromadb

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CHROMA_PATH = os.path.join(BASE_DIR, "chroma_db")

client = chromadb.PersistentClient(path=CHROMA_PATH)
# 1. Alinhado com o nome exato usado na ingestão
collection = client.get_or_create_collection(name="secgrad_normas")

def buscar_contexto(pergunta: str, curso: str = "Geral", perfil: str = "Todos", top_k: int = 3) -> dict:
    """
    Recupera trechos relevantes do ChromaDB com filtros de metadados.
    Retorna o contexto formatado, lista de fontes auditáveis e distância mínima.
    """
    filtros = []

    # 2. Adaptação para as chaves reais de metadados gravadas (curso_alvo e perfil_curricular)
    if curso and curso != "Geral":
        filtros.append({"curso_alvo": {"$contains": curso}})
    if perfil and perfil != "Todos":
        filtros.append({"perfil_curricular": {"$contains": perfil}})

    where_filter = None
    if len(filtros) == 1:
        where_filter = filtros[0]
    elif len(filtros) > 1:
        where_filter = {"$and": filtros}

    # Consulta ao ChromaDB
    resultados = collection.query(
        query_texts=[pergunta],
        n_results=top_k,
        where=where_filter
    )

    documentos = resultados["documents"][0] if (resultados["documents"] and len(resultados["documents"]) > 0) else []
    metadados = resultados["metadatas"][0] if (resultados["metadatas"] and len(resultados["metadatas"]) > 0) else []
    distancias = resultados["distances"][0] if ("distances" in resultados and resultados["distances"] and len(resultados["distances"]) > 0) else []

    contexto_formatado = []
    fontes = []

    for doc, meta in zip(documentos, metadados):
        # 3. Leitura segura dos nomes dos campos gravados na ingestão
        nome_doc = meta.get("documento", meta.get("source", "Documento Oficial"))
        num_pag = meta.get("pagina", meta.get("page", 1))
        curso_doc = meta.get("curso_alvo", meta.get("curso", "Geral"))
        
        tag = f"[Documento: {nome_doc} | Pág. {num_pag} | Curso: {curso_doc}]"
        contexto_formatado.append(f"{tag}\n{doc}")
        fontes.append({
            "arquivo": nome_doc,
            "pagina": num_pag,
            "curso": curso_doc
        })

    return {
        "contexto": "\n\n---\n\n".join(contexto_formatado),
        "fontes": fontes,
        "distancia_minima": distancias[0] if distancias else 1.0
    }

# 4. Bloco de teste direto via terminal
if __name__ == "__main__":
    print("--- Teste 1: Consulta sobre horas de estágio ---")
    resultado_estagio = buscar_contexto("Quantas horas de estágio são obrigatórias?", curso="Ciência da Computação")
    print("\n[CONTEXTO ENCONTRADO]:")
    print(resultado_estagio["contexto"] if resultado_estagio["contexto"] else "Nenhum trecho correspondente.")
    print("\n[FONTES]:", resultado_estagio["fontes"])
    print("[DISTÂNCIA]:", resultado_estagio["distancia_minima"])

    print("\n" + "="*50 + "\n")

    print("--- Teste 2: Consulta sobre dispensa e segunda chamada (TXT) ---")
    resultado_dispensa = buscar_contexto("Qual o prazo para solicitar segunda chamada?", curso="Geral")
    print("\n[CONTEXTO ENCONTRADO]:")
    print(resultado_dispensa["contexto"] if resultado_dispensa["contexto"] else "Nenhum trecho correspondente.")
    print("\n[FONTES]:", resultado_dispensa["fontes"])
    print("[DISTÂNCIA]:", resultado_dispensa["distancia_minima"])
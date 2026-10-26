def sincronizar_documento(
    collection,
    nome_arquivo: str,
    ids: list[str],
    documents: list[str],
    metadatas: list[dict],
) -> list[str]:
    """
    Atualiza os chunks de um documento no ChromaDB.

    Além de inserir a versão atual, remove chunks antigos
    que não existem mais na nova versão do documento.
    """

    existentes = collection.get(
        where={"documento": nome_arquivo},
        include=[],
    )

    ids_anteriores = set(
        existentes.get("ids", [])
    )

    collection.upsert(
        ids=ids,
        documents=documents,
        metadatas=metadatas,
    )

    ids_atuais = set(ids)

    ids_obsoletos = sorted(
        ids_anteriores - ids_atuais
    )

    if ids_obsoletos:
        collection.delete(ids=ids_obsoletos)

    return ids_obsoletos
import os
from pypdf import PdfReader
from langchain_text_splitters import RecursiveCharacterTextSplitter
import chromadb

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CHROMA_PATH = os.path.join(BASE_DIR, "chroma_db")

client = chromadb.PersistentClient(path=CHROMA_PATH)
collection = client.get_or_create_collection(
    name="secgrad_normas",
    metadata={"hnsw:space": "cosine"}
)

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=700,
    chunk_overlap=150,
    separators=["\n\n", "\n", "Art.", "Artigo", ". ", " ", ""]
)

def sanitizar_metadados(meta: dict) -> dict:
    """O ChromaDB exige que metadados sejam str, int, float ou bool."""
    meta_limpo = {}
    for k, v in meta.items():
        if isinstance(v, list):
            meta_limpo[k] = ", ".join(str(item) for item in v)
        elif isinstance(v, (str, int, float, bool)):
            meta_limpo[k] = v
        else:
            meta_limpo[k] = str(v)
    return meta_limpo

def indexar_documento(caminho_arquivo: str, metadados_personalizados: dict = None) -> dict:
    nome_arquivo = os.path.basename(caminho_arquivo)
    extensao = os.path.splitext(nome_arquivo)[1].lower()
    
    if metadados_personalizados is None:
        metadados_personalizados = {}
    
    metadados_base = sanitizar_metadados(metadados_personalizados)
    docs_para_inserir = []

    # 1. Leitura de Ficheiro TXT
    if extensao == ".txt":
        try:
            with open(caminho_arquivo, "r", encoding="utf-8") as f:
                conteudo = f.read()
        except UnicodeDecodeError:
            with open(caminho_arquivo, "r", encoding="latin-1") as f:
                conteudo = f.read()
                
        if not conteudo.strip():
            print(f"[-] Aviso: O ficheiro '{nome_arquivo}' está vazio.")
            return {"sucesso": False, "motivo": "Ficheiro vazio"}

        chunks = text_splitter.split_text(conteudo)
        for i, chunk in enumerate(chunks):
            meta_chunk = metadados_base.copy()
            meta_chunk.update({
                "documento": nome_arquivo,
                "pagina": 1,
                "chunk_id": f"{nome_arquivo}_p1_c{i}"
            })
            docs_para_inserir.append((f"{nome_arquivo}_p1_c{i}", chunk, meta_chunk))

    # 2. Leitura de Ficheiro PDF
    elif extensao == ".pdf":
        try:
            reader = PdfReader(caminho_arquivo)
        except Exception as e:
            print(f"[-] Erro ao abrir PDF '{nome_arquivo}': {e}")
            return {"sucesso": False, "motivo": str(e)}

        for num_pagina, pagina in enumerate(reader.pages, start=1):
            texto_pagina = pagina.extract_text() or ""
            if not texto_pagina.strip():
                continue
            
            chunks = text_splitter.split_text(texto_pagina)
            for i, chunk in enumerate(chunks):
                meta_chunk = metadados_base.copy()
                meta_chunk.update({
                    "documento": nome_arquivo,
                    "pagina": num_pagina,
                    "chunk_id": f"{nome_arquivo}_p{num_pagina}_c{i}"
                })
                docs_para_inserir.append((f"{nome_arquivo}_p{num_pagina}_c{i}", chunk, meta_chunk))
    else:
        print(f"[-] Formato não suportado para '{nome_arquivo}'.")
        return {"sucesso": False, "motivo": "Extensão inválida"}

    # Gravação no ChromaDB
    if not docs_para_inserir:
        print(f"[-] Aviso: Nenhum texto extraído de '{nome_arquivo}' (possível PDF digitalizado/imagem).")
        return {"sucesso": False, "motivo": "Nenhum texto extraído"}

    ids = [d[0] for d in docs_para_inserir]
    documents = [d[1] for d in docs_para_inserir]
    metadatas = [d[2] for d in docs_para_inserir]

    collection.upsert(ids=ids, documents=documents, metadatas=metadatas)
    print(f"[✓] Sucesso: {len(ids)} trechos indexados de '{nome_arquivo}'.")
    return {"sucesso": True, "total_chunks": len(ids)}

# Mantém compatibilidade com chamadas anteriores
indexar_pdf = indexar_documento
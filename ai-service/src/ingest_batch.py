import os
import json
from src.ingest import indexar_documento

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")
METADATA_FILE = os.path.join(DATA_DIR, "metadata.json")

def extrair_pares_documento_metadados(catalogo):
    itens = []
    if isinstance(catalogo, dict):
        for nome_arq, meta in catalogo.items():
            itens.append((nome_arq, meta))
    elif isinstance(catalogo, list):
        chaves_candidatas = ["arquivo", "nome", "nome_arquivo", "file", "filename", "documento"]
        for entrada in catalogo:
            if not isinstance(entrada, dict):
                continue
            nome_arq = None
            for chave in chaves_candidatas:
                if chave in entrada:
                    nome_arq = entrada[chave]
                    break
            if not nome_arq:
                for k, v in entrada.items():
                    if isinstance(v, str) and (v.lower().endswith(".pdf") or v.lower().endswith(".txt")):
                        nome_arq = v
                        break
            if nome_arq:
                metadados = {k: v for k, v in entrada.items() if v != nome_arq}
                itens.append((nome_arq, metadados))
    return itens

def processar_lote():
    if not os.path.exists(METADATA_FILE):
        print(f"Erro: Ficheiro '{METADATA_FILE}' não encontrado.")
        return

    with open(METADATA_FILE, "r", encoding="utf-8") as f:
        catalogo = json.load(f)

    itens = extrair_pares_documento_metadados(catalogo)
    print(f"\n--- A iniciar Ingestão de {len(itens)} Documentos ---")

    documentos_processados = 0
    for nome_arquivo, metadados in itens:
        caminho_arquivo = os.path.join(DATA_DIR, nome_arquivo)
        
        if os.path.exists(caminho_arquivo):
            print(f"\n[+] A processar: {nome_arquivo}")
            try:
                resultado = indexar_documento(caminho_arquivo, metadados)
                if resultado.get("sucesso"):
                    documentos_processados += 1
            except Exception as e:
                print(f"[!] Erro inesperado ao indexar '{nome_arquivo}': {e}")
        else:
            print(f"\n[!] Aviso: '{nome_arquivo}' listado no JSON não existe em data/.")

    print(f"\n==========================================")
    print(f"Ingestão Finalizada: {documentos_processados}/{len(itens)} documentos ativos no ChromaDB")
    print(f"==========================================\n")

if __name__ == "__main__":
    processar_lote()
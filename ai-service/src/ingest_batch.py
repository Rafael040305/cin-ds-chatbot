import json

from src.config import DATA_DIR
from src.ingest import indexar_documento
from src.validate_catalog import validar_catalogo


METADATA_FILE = DATA_DIR / "metadata.json"

CHAVES_NOME_ARQUIVO = [
    "arquivo",
    "nome",
    "nome_arquivo",
    "file",
    "filename",
    "documento",
]


def extrair_pares_documento_metadados(
    catalogo,
) -> list[tuple[str, dict]]:
    """
    Transforma o catálogo em pares contendo:
    nome do arquivo e seus metadados.
    """

    itens = []

    if isinstance(catalogo, dict):
        for nome_arquivo, metadados in (
            catalogo.items()
        ):
            itens.append((
                nome_arquivo,
                metadados,
            ))

        return itens

    if not isinstance(catalogo, list):
        return itens

    for entrada in catalogo:
        if not isinstance(entrada, dict):
            continue

        nome_arquivo = None
        chave_nome = None

        for chave in CHAVES_NOME_ARQUIVO:
            if chave in entrada:
                nome_arquivo = entrada[chave]
                chave_nome = chave
                break

        if nome_arquivo is None:
            for chave, valor in entrada.items():
                if (
                    isinstance(valor, str)
                    and valor.lower().endswith(
                        (".pdf", ".txt")
                    )
                ):
                    nome_arquivo = valor
                    chave_nome = chave
                    break

        if nome_arquivo is None:
            continue

        metadados = {
            chave: valor
            for chave, valor in entrada.items()
            if chave != chave_nome
        }

        itens.append((
            nome_arquivo,
            metadados,
        ))

    return itens


def processar_lote() -> dict:
    """
    Valida o catálogo e realiza a ingestão de todos
    os documentos cadastrados.
    """

    problemas = validar_catalogo(
        METADATA_FILE
    )

    if problemas:
        print(
            "Catálogo inválido. "
            "A ingestão foi cancelada:"
        )

        for problema in problemas:
            print(f"- {problema}")

        return {
            "sucesso": False,
            "documentos_processados": 0,
            "problemas": problemas,
        }

    with METADATA_FILE.open(
        encoding="utf-8"
    ) as arquivo:
        catalogo = json.load(arquivo)

    itens = extrair_pares_documento_metadados(
        catalogo
    )

    print()
    print(
        f"Iniciando ingestão de "
        f"{len(itens)} documentos."
    )

    documentos_processados = 0
    documentos_com_erro = []

    for nome_arquivo, metadados in itens:
        caminho_arquivo = (
            DATA_DIR / nome_arquivo
        )

        print()
        print(
            f"[PROCESSANDO] {nome_arquivo}"
        )

        try:
            resultado = indexar_documento(
                caminho_arquivo,
                metadados,
            )

            if resultado.get("sucesso"):
                documentos_processados += 1
            else:
                documentos_com_erro.append(
                    nome_arquivo
                )

        except Exception as erro:
            print(
                f"[ERRO] Falha inesperada em "
                f"'{nome_arquivo}': {erro}"
            )

            documentos_com_erro.append(
                nome_arquivo
            )

    print()
    print("=" * 45)
    print(
        f"Ingestão finalizada: "
        f"{documentos_processados}/"
        f"{len(itens)} documentos processados."
    )
    print("=" * 45)

    sucesso = (
        documentos_processados == len(itens)
    )

    return {
        "sucesso": sucesso,
        "documentos_processados": (
            documentos_processados
        ),
        "total_documentos": len(itens),
        "documentos_com_erro": (
            documentos_com_erro
        ),
    }


if __name__ == "__main__":
    resultado = processar_lote()

    if not resultado["sucesso"]:
        raise SystemExit(1)
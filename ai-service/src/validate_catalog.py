import json
from pathlib import Path

from src.config import DATA_DIR
from src.metadata_utils import (
    normalizar_curso,
    normalizar_perfil,
)


CAMPOS_OBRIGATORIOS = {
    "arquivo",
    "titulo",
    "tipo_documento",
    "curso_alvo",
    "perfil_curricular",
    "vigencia",
}


def validar_catalogo(
    caminho: Path = DATA_DIR / "metadata.json",
) -> list[str]:
    """
    Valida o catálogo de documentos antes da ingestão.

    Retorna uma lista vazia quando o catálogo é válido.
    Caso contrário, retorna uma lista com os erros.
    """

    erros = []

    if not caminho.exists():
        return [
            f"Catálogo não encontrado: {caminho}"
        ]

    try:
        with caminho.open(
            encoding="utf-8"
        ) as arquivo:
            catalogo = json.load(arquivo)

    except json.JSONDecodeError as erro:
        return [
            f"JSON inválido: {erro}"
        ]

    if not isinstance(catalogo, list):
        return [
            "O catálogo deve ser uma lista "
            "de documentos."
        ]

    nomes_encontrados = set()

    for indice, item in enumerate(
        catalogo,
        start=1,
    ):
        if not isinstance(item, dict):
            erros.append(
                f"Item {indice}: deve ser "
                f"um objeto JSON."
            )
            continue

        campos_ausentes = (
            CAMPOS_OBRIGATORIOS - set(item)
        )

        if campos_ausentes:
            nomes_campos = ", ".join(
                sorted(campos_ausentes)
            )

            erros.append(
                f"Item {indice}: campos "
                f"ausentes: {nomes_campos}"
            )

            continue

        nome_arquivo = item["arquivo"]

        if not isinstance(nome_arquivo, str):
            erros.append(
                f"Item {indice}: o campo "
                f"'arquivo' deve ser texto."
            )
            continue

        if nome_arquivo in nomes_encontrados:
            erros.append(
                f"Item {indice}: arquivo "
                f"duplicado: {nome_arquivo}"
            )

        nomes_encontrados.add(nome_arquivo)

        caminho_documento = (
            DATA_DIR / nome_arquivo
        )

        if not caminho_documento.exists():
            erros.append(
                f"Item {indice}: arquivo não "
                f"encontrado: {nome_arquivo}"
            )

        cursos = item["curso_alvo"]

        if isinstance(cursos, str):
            cursos = [cursos]

        if not isinstance(cursos, list):
            erros.append(
                f"Item {indice}: 'curso_alvo' "
                f"deve ser texto ou lista."
            )
        else:
            for curso in cursos:
                try:
                    normalizar_curso(curso)

                except ValueError as erro:
                    erros.append(
                        f"Item {indice}: {erro}"
                    )

        try:
            normalizar_perfil(
                item["perfil_curricular"]
            )

        except ValueError as erro:
            erros.append(
                f"Item {indice}: {erro}"
            )

        if not isinstance(
            item["vigencia"],
            bool,
        ):
            erros.append(
                f"Item {indice}: 'vigencia' "
                f"deve ser true ou false."
            )

    return erros


if __name__ == "__main__":
    problemas = validar_catalogo()

    if problemas:
        print("Catálogo inválido:")

        for problema in problemas:
            print(f"- {problema}")

        raise SystemExit(1)

    print("Catálogo válido.")
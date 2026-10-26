import re
import unicodedata


CURSOS = {
    "cc": "Ciência da Computação",
    "ec": "Engenharia da Computação",
    "si": "Sistemas de Informação",
    "ia": "Inteligência Artificial",
}

ALIASES_CURSO = {
    "cc": "cc",
    "ciencia da computacao": "cc",
    "ec": "ec",
    "engenharia da computacao": "ec",
    "si": "si",
    "sistemas de informacao": "si",
    "sistemas de informacoes": "si",
    "ia": "ia",
    "inteligencia artificial": "ia",
}

ALIASES_PERFIL = {
    "novo": "novo",
    "vigente": "novo",
    "perfil novo": "novo",
    "perfil vigente": "novo",
    "perfil novo / vigente": "novo",
    "unico perfil": "novo",
    "anterior": "anterior",
    "antigo": "anterior",
    "perfil antigo": "anterior",
    "perfil anterior": "anterior",
}


def _normalizar_texto(valor: object) -> str:
    texto = unicodedata.normalize("NFKD", str(valor or ""))
    texto = "".join(
        caractere
        for caractere in texto
        if not unicodedata.combining(caractere)
    )
    return re.sub(r"\s+", " ", texto.strip().lower())


def normalizar_curso(valor: object) -> str | None:
    texto = _normalizar_texto(valor)

    if texto in {"", "geral", "todos"}:
        return None

    if texto not in ALIASES_CURSO:
        raise ValueError(f"Curso desconhecido: {valor}")

    return ALIASES_CURSO[texto]


def normalizar_perfil(valor: object) -> str | None:
    texto = _normalizar_texto(valor)

    if texto in {"", "todos", "ambos"}:
        return None

    if texto not in ALIASES_PERFIL:
        raise ValueError(
            f"Perfil curricular desconhecido: {valor}"
        )

    return ALIASES_PERFIL[texto]


def enriquecer_metadados(meta: dict) -> dict:
    cursos_originais = meta.get("curso_alvo", [])

    if isinstance(cursos_originais, str):
        cursos_originais = [cursos_originais]

    codigos = set()

    for curso in cursos_originais:
        codigo = normalizar_curso(curso)

        if codigo is not None:
            codigos.add(codigo)

    perfil = normalizar_perfil(
        meta.get("perfil_curricular", "ambos")
    )

    resultado = dict(meta)

    nomes_cursos = [
        CURSOS[codigo]
        for codigo in CURSOS
        if codigo in codigos
    ]

    resultado["curso_alvo"] = (
        " | ".join(nomes_cursos) or "Geral"
    )

    resultado["perfil_curricular"] = perfil or "ambos"

    for codigo in CURSOS:
        resultado[f"curso_{codigo}"] = (
            not codigos or codigo in codigos
        )

    resultado["perfil_novo"] = perfil in {None, "novo"}
    resultado["perfil_anterior"] = perfil in {
        None,
        "anterior",
    }

    return resultado


def construir_filtro(
    curso: str = "Geral",
    perfil: str = "Todos",
) -> dict | None:
    filtros = []

    codigo_curso = normalizar_curso(curso)
    codigo_perfil = normalizar_perfil(perfil)

    if codigo_curso:
        filtros.append({f"curso_{codigo_curso}": True})

    if codigo_perfil:
        filtros.append({f"perfil_{codigo_perfil}": True})

    if not filtros:
        return None

    if len(filtros) == 1:
        return filtros[0]

    return {"$and": filtros}
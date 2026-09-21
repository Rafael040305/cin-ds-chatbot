from src.core.fallback import gerar_email_fallback


LIMITE_DISTANCIA_PROVISORIO = 0.8


def deve_acionar_fallback(
    distancia_minima,
    limite=LIMITE_DISTANCIA_PROVISORIO
):
    return distancia_minima >= limite


def processar_fallback(
    distancia_minima,
    nome,
    matricula,
    curso,
    perfil,
    assunto,
    resumo,
    duvida,
    setor
):
    if deve_acionar_fallback(distancia_minima):
        return gerar_email_fallback(
            nome=nome,
            matricula=matricula,
            curso=curso,
            perfil=perfil,
            assunto=assunto,
            resumo=resumo,
            duvida=duvida,
            setor=setor
        )

    return None
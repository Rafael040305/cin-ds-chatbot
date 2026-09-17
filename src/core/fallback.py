def gerar_email_fallback(
    nome,
    matricula,
    curso,
    perfil,
    assunto,
    resumo,
    duvida,
    setor
):
    email = f"""
Assunto: {assunto}

Olá,

Meu nome é {nome}, matrícula {matricula}, aluno(a) do curso de {curso}, perfil curricular {perfil}.

Estou entrando em contato sobre: {assunto}.

Resumo da situação:
{resumo}

Minha dúvida é:
{duvida}

Setor responsável:
{setor}

Atenciosamente,
{nome}
"""

    return email

def identificar_setor(assunto):
    assunto = assunto.lower()

    if "estágio" in assunto or "estagio" in assunto:
        return "SecGrad"

    if "requerimento" in assunto or "dispensa" in assunto or "segunda chamada" in assunto:
        return "SecGrad"

    if "pedagógic" in assunto or "pedagogic" in assunto:
        return "NEAP"

    if "pós-graduação" in assunto or "pos-graduacao" in assunto or "pós graduação" in assunto:
        return "Secretaria de Pós-Graduação"

    return "SecGrad"
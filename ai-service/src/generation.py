"""Contrato de geração V1. O modo simulado serve somente à integração."""

import os


class GenerationUnavailable(RuntimeError):
    """Provedor real ainda não configurado."""


def gerar_resposta(pergunta: str, contexto: str) -> str | None:
    if not pergunta.strip():
        raise ValueError("A pergunta não pode estar vazia.")
    if not contexto.strip():
        return None
    if os.getenv("SECGRAD_GENERATION_MODE", "disabled") != "mock":
        raise GenerationUnavailable("Serviço de geração indisponível.")
    # Nunca produzir uma resposta acadêmica fictícia como se fosse documental.
    return "[SIMULAÇÃO DE INTEGRAÇÃO — NÃO É RESPOSTA ACADÊMICA]"

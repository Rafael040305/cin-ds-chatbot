import os
import unittest
from unittest.mock import patch

from src.generation import GenerationUnavailable, gerar_resposta


class GenerationTest(unittest.TestCase):
    def test_contexto_vazio_retora_null(self):
        self.assertIsNone(gerar_resposta("Pergunta", "  "))

    def test_pergunta_vazia_rejeitada(self):
        with self.assertRaises(ValueError):
            gerar_resposta("  ", "Documento")

    def test_desabilitado_por_padrao(self):
        with patch.dict(os.environ, {}, clear=True):
            with self.assertRaises(GenerationUnavailable):
                gerar_resposta("Pergunta", "Documento")

    def test_mock_explicitamente_identificado(self):
        with patch.dict(os.environ, {"SECGRAD_GENERATION_MODE": "mock"}):
            self.assertIn("SIMULAÇÃO", gerar_resposta("Pergunta", "Documento"))

    def test_modo_desconhecido_nao_gera_resposta(self):
        with patch.dict(os.environ, {"SECGRAD_GENERATION_MODE": "typo"}):
            with self.assertRaises(GenerationUnavailable):
                gerar_resposta("Pergunta", "Documento")

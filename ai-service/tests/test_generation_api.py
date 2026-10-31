import os
import unittest
from unittest.mock import patch

from fastapi.testclient import TestClient
from main import app


class GenerationApiTest(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)

    def test_mock_contrato_http(self):
        with patch.dict(os.environ, {"SECGRAD_GENERATION_MODE": "mock"}):
            response = self.client.post("/api/v1/gerar", json={"pergunta": "Dúvida", "contexto": "Documento"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(set(response.json()), {"resposta"})
        self.assertIn("SIMULAÇÃO", response.json()["resposta"])

    def test_sem_contexto(self):
        response = self.client.post("/api/v1/gerar", json={"pergunta": "Dúvida", "contexto": ""})
        self.assertEqual(response.json(), {"resposta": None})

    def test_servico_desabilitado(self):
        with patch.dict(os.environ, {}, clear=True):
            response = self.client.post("/api/v1/gerar", json={"pergunta": "Dúvida", "contexto": "Documento"})
        self.assertEqual(response.status_code, 503)

    def test_entradas_invalidas(self):
        for payload in ({}, {"pergunta": " ", "contexto": "x"}, {"pergunta": "x", "contexto": 1}):
            with self.subTest(payload=payload):
                self.assertEqual(self.client.post("/api/v1/gerar", json=payload).status_code, 422)

    def test_top_k_nao_aceita_coercao(self):
        for valor in (0, -1, True, "3", 1.5):
            with self.subTest(valor=valor):
                self.assertEqual(self.client.post("/api/v1/buscar", json={"pergunta": "x", "top_k": valor}).status_code, 422)

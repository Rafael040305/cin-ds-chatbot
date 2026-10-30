"""V1 independente, gerada uma vez em 2026-10-30. Oráculos: US-01/CA-01.1–5."""
import importlib
import math
import sys
import types
import unittest
from unittest.mock import patch

from fastapi.testclient import TestClient
from src.retriever import buscar_contexto

# Não importar/ler implementações fora do contexto autorizado.
generation_stub = types.ModuleType('src.generation')
generation_stub.GenerationUnavailable = type('GenerationUnavailable', (Exception,), {})
generation_stub.gerar_resposta = lambda *a, **k: (_ for _ in ()).throw(AssertionError('Fora do escopo'))
ingest_stub = types.ModuleType('src.ingest')
ingest_stub.indexar_documento = lambda *a, **k: (_ for _ in ()).throw(AssertionError('Fora do escopo'))
with patch.dict(sys.modules, {'src.generation': generation_stub, 'src.ingest': ingest_stub}):
    api = importlib.import_module('main')


def resultado(pagina=1, distancia=0.25, legado=False):
    meta = ({'source': 'norma.pdf', 'page': pagina, 'curso': 'Ciência da Computação'}
            if legado else {'documento': 'norma.pdf', 'pagina': pagina,
                            'curso_alvo': 'Ciência da Computação'})
    return {'documents': [['Trecho oficial sobre matrícula.']],
            'metadatas': [[meta]], 'distances': [[distancia]]}


class ColecaoFake:
    def __init__(self, resposta=None):
        self.resposta = resultado() if resposta is None else resposta
        self.chamadas = []

    def query(self, **kwargs):
        self.chamadas.append(kwargs)
        return self.resposta


class BuscaV1(unittest.TestCase):
    def setUp(self):
        self.colecao = ColecaoFake()
        self.patch = patch('src.retriever.obter_collection', return_value=self.colecao)
        self.patch.start()
        self.addCleanup(self.patch.stop)
        self.client = TestClient(api.app, raise_server_exceptions=False)
        self.addCleanup(self.client.close)

    def post(self, **dados):
        payload = {'pergunta': 'Como realizar matrícula?', 'curso': 'Geral',
                   'perfil': 'Todos', 'top_k': 3}
        payload.update(dados)
        return self.client.post('/api/v1/buscar', json=payload)

    def assert_contrato(self, corpo):
        self.assertIsInstance(corpo['contexto'], str)
        self.assertTrue(corpo['contexto'])
        self.assertTrue(math.isfinite(corpo['distancia_minima']))
        self.assertTrue(corpo['fontes'])
        for fonte in corpo['fontes']:
            self.assertIsInstance(fonte['arquivo'], str)
            self.assertTrue(fonte['arquivo'])
            self.assertIs(type(fonte['pagina']), int)
            self.assertGreaterEqual(fonte['pagina'], 1)
            self.assertIsInstance(fonte['curso'], str)
            self.assertTrue(fonte['curso'])

    def test_cursos_perfis_reconhecidos(self):
        # Partições válidas de curso/perfil; US-01, CA-01.1 e CA-01.2.
        for curso, codigo in [('cc', 'cc'), ('Engenharia da Computação', 'ec'),
                              ('Sistemas de Informação', 'si'), ('Inteligência Artificial', 'ia')]:
            for perfil, chave in [('vigente', 'novo'), ('anterior', 'anterior')]:
                with self.subTest(curso=curso, perfil=perfil):
                    resposta = self.post(curso=curso, perfil=perfil)
                    self.assertEqual(resposta.status_code, 200)
                    self.assert_contrato(resposta.json())
                    self.assertEqual(self.colecao.chamadas[-1]['where'],
                                     {'$and': [{f'curso_{codigo}': True}, {f'perfil_{chave}': True}]})

    def test_top_k_valores_validos(self):
        # Limite inferior 1, vizinho 2 e representante 10; US-01, CA-01.1.
        for k in [1, 2, 10]:
            with self.subTest(top_k=k):
                self.assertEqual(self.post(top_k=k).status_code, 200)
                self.assertEqual(self.colecao.chamadas[-1]['n_results'], k)

    def test_pergunta_nao_vazia(self):
        # Limite de um caractere e partição com espaços externos; CA-01.1.
        for pergunta in ['a', '  matrícula  ']:
            with self.subTest(pergunta=pergunta):
                self.assertEqual(self.post(pergunta=pergunta).status_code, 200)
                self.assertEqual(self.colecao.chamadas[-1]['query_texts'], [pergunta.strip()])

    def test_sem_restricoes(self):
        # Partição Geral/Todos e parâmetros opcionais ausentes; CA-01.5.
        for payload in [{'pergunta': 'matrícula'}, {'pergunta': 'matrícula', 'curso': 'Geral', 'perfil': 'Todos'}]:
            with self.subTest(payload=payload):
                self.assertEqual(self.client.post('/api/v1/buscar', json=payload).status_code, 200)
                self.assertNotIn('where', self.colecao.chamadas[-1])

    def test_restricao_unica(self):
        # Partições com apenas um filtro ativo; CA-01.1 e CA-01.5.
        for curso, perfil, esperado in [('cc', 'Todos', {'curso_cc': True}),
                                        ('Geral', 'novo', {'perfil_novo': True})]:
            with self.subTest(curso=curso, perfil=perfil):
                self.assertEqual(self.post(curso=curso, perfil=perfil).status_code, 200)
                self.assertEqual(self.colecao.chamadas[-1]['where'], esperado)

    def test_pergunta_invalida(self):
        # Partição vazia/branca e fronteira de comprimento zero; CA-01.4.
        for pergunta in ['', ' ', '\t\n']:
            with self.subTest(pergunta=pergunta):
                resposta = self.post(pergunta=pergunta)
                self.assertTrue(400 <= resposta.status_code < 500, resposta.text)
        self.assertEqual(self.colecao.chamadas, [])

    def test_top_k_invalido(self):
        # Limite 0/-1 e partições de tipos não inteiros positivos; CA-01.4.
        for k in [0, -1, 1.5, 1.0, '1', True, False, None, [], {}]:
            with self.subTest(top_k=k):
                resposta = self.post(top_k=k)
                self.assertTrue(400 <= resposta.status_code < 500, resposta.text)
        self.assertEqual(self.colecao.chamadas, [])

    def test_filtros_desconhecidos(self):
        # Partições de curso e perfil desconhecidos, isolados/combinados; CA-01.4.
        for dados in [{'curso': 'Medicina'}, {'perfil': 'futuro'},
                      {'curso': 'xyz', 'perfil': 'xyz'}]:
            with self.subTest(dados=dados):
                resposta = self.post(**dados)
                self.assertTrue(400 <= resposta.status_code < 500, resposta.text)
        self.assertEqual(self.colecao.chamadas, [])

    def test_sem_resultados(self):
        # Partição de cardinalidade zero, representações vazias; CA-01.3.
        for vazio in [{}, {'documents': [], 'metadatas': [], 'distances': []},
                      {'documents': [[]], 'metadatas': [[]], 'distances': [[]]}]:
            with self.subTest(vazio=vazio):
                self.colecao.resposta = vazio
                resposta = self.post()
                self.assertEqual(resposta.status_code, 200)
                self.assertEqual(resposta.json(), {'contexto': '', 'fontes': [], 'distancia_minima': 1.0})

    def test_fontes_e_paginas_validas(self):
        # Limite página 1/vizinho 2 e partições de metadados; CA-01.2.
        for pagina in [1, 2]:
            for legado in [False, True]:
                with self.subTest(pagina=pagina, legado=legado):
                    self.colecao.resposta = resultado(pagina=pagina, legado=legado)
                    resposta = self.post()
                    self.assertEqual(resposta.status_code, 200)
                    corpo = resposta.json()
                    self.assert_contrato(corpo)
                    self.assertIn('Trecho oficial sobre matrícula.', corpo['contexto'])
                    self.assertEqual(corpo['fontes'], [{'arquivo': 'norma.pdf', 'pagina': pagina,
                                                      'curso': 'Ciência da Computação'}])
                    self.assertEqual(corpo['distancia_minima'], 0.25)

    def test_varias_fontes(self):
        # Partição de cardinalidade maior que um; CA-01.2.
        self.colecao.resposta = {'documents': [['Trecho A', 'Trecho B']],
            'metadatas': [[{'documento': 'a.pdf', 'pagina': 1, 'curso': 'Geral'},
                           {'documento': 'b.pdf', 'pagina': 2, 'curso': 'cc'}]],
            'distances': [[0.1, 0.2]]}
        resposta = self.post()
        self.assertEqual(resposta.status_code, 200)
        corpo = resposta.json()
        self.assert_contrato(corpo)
        self.assertEqual(len(corpo['fontes']), 2)
        for trecho in ['Trecho A', 'Trecho B']:
            self.assertIn(trecho, corpo['contexto'])

    def test_contrato_pagina_invalida_na_origem(self):
        # Robustez: limite 0/-1 e tipos inválidos na origem; CA-01.2.
        # O critério não condiciona o contrato à higidez dos metadados.
        for pagina in [0, -1, '1', 1.5, True, None]:
            with self.subTest(pagina=pagina):
                self.assert_contrato(buscar_contexto('matrícula', collection=ColecaoFake(resultado(pagina=pagina))))

    def test_contrato_distancia_nao_finita_na_origem(self):
        # Partições não finitas NaN/+inf/-inf na origem; CA-01.2.
        for distancia in [float('nan'), float('inf'), -float('inf')]:
            with self.subTest(distancia=distancia):
                self.assert_contrato(buscar_contexto('matrícula', collection=ColecaoFake(resultado(distancia=distancia))))


if __name__ == '__main__':
    unittest.main()

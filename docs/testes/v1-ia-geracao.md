# Evidência exclusiva — geração independente V1

Data: 2026-10-30 (America/Fortaleza).
Agente: Codex, baseado em GPT-6 conforme identificação disponível nesta sessão; versão exata do modelo não informada.

## Prompt integral recebido

Rafael solicita continuar sua parte da Sprint 3 do Chatbot SecGrad. Esta é uma conversa nova para gerar a suíte V1 independente. Trabalhe somente em C:/Users/Rafael/OneDrive/RafaelASUS/ProjetoDS/codigo/cin-ds-chatbot/ai-service/tests/v1-llm/ e em documentos de evidência exclusivos desta geração. NÃO leia docs/testes/matriz-rastreabilidade.md, nenhum teste existente, histórico de outros chats, nem tabelas de casos/partições esperadas: a comparação com a matriz será posterior em outro chat. A equipe aprovou a matriz e registrou aprovação em commit antes desta geração. Não altere código de produção, backend, interface, catálogo nem testes existentes. Não faça commit, push nem merge. Gere V1 uma única vez, preserve-a; até 3 rodadas só para compilar/rodar, sem pedidos de mais cobertura. Leia apenas ai-service/src/retriever.py, src/metadata_utils.py, src/config.py, main.py e requirements*.txt como contexto de código. Framework existente: unittest; TestClient FastAPI/httpx se necessário. US-01: Como estudante do CIn, quero pesquisar uma dúvida informando curso/perfil para receber trechos oficiais aplicáveis e fontes. Critérios: CA-01.1 pergunta não vazia, curso/perfil reconhecidos e top_k inteiro positivo aplicam filtros e retornam sucesso HTTP 200 na API; CA-01.2 resultados contêm contexto, distancia_minima finita e fontes com arquivo, pagina inteira >=1 e curso; CA-01.3 ausência de resultados retorna contexto vazio, fontes vazias e distancia_minima 1.0; CA-01.4 pergunta vazia/espaços, top_k não inteiro positivo e curso/perfil desconhecidos são rejeitados; CA-01.5 Geral/Todos não adicionam restrições de curso/perfil à busca. A geração /gerar foi adicionada depois da Sprint 2 e está fora desta V1. Gere testes aplicando partições de equivalência, valores-limite e cobertura dos critérios; comente em cada teste técnica e requisito. Use mocks/fakes para evitar Chroma real/downloads. Oráculos devem vir dos critérios, não aceitar bugs do código automaticamente. Preserve falhas e registre se são defeitos ou problemas de teste. Registre prompt completo desta mensagem, modelo quando conhecido (não invente versão), data e resposta original em arquivo exclusivo docs/testes/v1-ia-geracao.md, sem ler matriz/logs existentes. Execute somente a V1 com o Python venv/Scripts/python.exe da raiz (unittest discover -s ai-service/tests/v1-llm exige cwd ai-service ou ajuste de sys.path; prefira cwd ai-service e discover -s tests/v1-llm). Se possível meça linhas e branches apenas dos módulos selecionados usando coverage.py, sem instalar dependências sem necessidade; caso indisponível registre limitação. Entregue resultados e caminhos. Não melhore a V1 nem avance à V2. Este chat foi explicitamente solicitado por Rafael para executar a geração independente.

## Procedimento e independência

Lidos somente os quatro arquivos Python autorizados e requirements*.txt da raiz/ai-service. Nenhuma matriz, teste anterior, histórico de chats ou catálogo foi consultado. A aprovação prévia da matriz é informação do solicitante; o commit não foi consultado. As duas novas localizações foram verificadas como inexistentes antes da criação. Nenhum código de produção foi alterado; nenhum commit, push ou merge foi feito.

Uma única geração, sem revisão do arquivo de testes após sua criação. Uma única rodada de execução, sem correções ou expansão. Coleção falsa substitui obter_collection; buscar_contexto e a rota de busca são reais. Módulos src.generation e src.ingest recebem stubs antes da importação de main para não carregar implementações fora do contexto autorizado. /gerar e /ingestar não foram exercitados. Escrita de bytecode desativada.

Os requisitos fornecem os oráculos; os nomes reconhecidos, campos de metadados e representação dos filtros são adaptadores extraídos do código autorizado. A coleção falsa captura os filtros, mas não comprova o comportamento do Chroma real nem a autenticidade de documentos. Os dados documentais são sintéticos.

## Execução e resultado

Diretório: C:/Users/Rafael/OneDrive/RafaelASUS/ProjetoDS/codigo/cin-ds-chatbot/ai-service
Comando: ../venv/Scripts/python.exe -B -m unittest discover -s tests/v1-llm -v
Ambiente: PYTHONDONTWRITEBYTECODE=1.
Código de saída do unittest: 1.
Resultado: 13 métodos executados em 0.094 s; 11 métodos passaram; 2 métodos tiveram 9 falhas de subtestes, sem erros de execução/importação.
Log integral: ai-service/tests/v1-llm/execucao-v1.txt. O log capturado pelo terminal apresenta caracteres acentuados corrompidos em alguns trechos de traceback; isso não afetou as asserções nem o arquivo original UTF-8.

Classificação das falhas:
- 6 falhas em test_contrato_pagina_invalida_na_origem: 0, -1, string '1', 1.5, True e None são devolvidos como pagina, contrariando o contrato de inteiro >= 1.
- 3 falhas em test_contrato_distancia_nao_finita_na_origem: NaN, +infinito e -infinito são devolvidos como distancia_minima, contrariando a exigência de valor finito.
- Classificação: defeitos de robustez do retorno em relação à leitura literal de CA-01.2, sob a premissa explícita de que o contrato também vale para dados inválidos na origem. Não são falhas de infraestrutura nem erros acidentais de asserção. O requisito não especifica se a coleção garante dados válidos nem qual tratamento aplicar aos inválidos. Se existir uma pré-condição externa de integridade da coleção, estes dois testes terão uma premissa fora do domínio suportado e deverão ser classificados na comparação posterior como problemas de especificação/domínio do teste. Essa pré-condição não foi presumida, nem investigada em arquivos proibidos. Nenhuma falha foi ocultada ou corrigida.

Cobertura de linhas/branches: não medida. A consulta importlib.util.find_spec('coverage') retornou indisponível no venv; fastapi/httpx estavam disponíveis. Nenhuma dependência instalada. Não se infere percentual de cobertura a partir da quantidade de testes. Os cinco critérios têm asserções explícitas nesta V1, sem alegação de exaustividade. Não houve avanço à V2.

SHA-256 do teste preservado: 0AD591420DFBDE9F14924A6560828BA3771E1A548B59C830C8D46BA12F3970C1.

## Resposta original da geração — suíte integral preservada

O bloco abaixo reproduz integralmente o arquivo gerado, sem revisão após a execução.

```python
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

```

## Resposta de entrega

V1 gerada uma única vez e preservada. Execução: 13 métodos, 11 aprovados e 9 falhas de subtestes em 2 métodos. As falhas verificam páginas inválidas e distâncias não finitas na origem, com a premissa de robustez documentada acima. Coverage.py indisponível; cobertura não medida. Produção e testes anteriores não alterados; sem commit, push, merge ou V2.

Arquivos entregues, sob C:/Users/Rafael/OneDrive/RafaelASUS/ProjetoDS/codigo/cin-ds-chatbot/:
- ai-service/tests/v1-llm/test_busca_v1.py
- ai-service/tests/v1-llm/execucao-v1.txt
- docs/testes/v1-ia-geracao.md

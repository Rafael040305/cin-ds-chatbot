"""V2: preserva casos válidos V1 e corrige o oráculo de origem inválida."""
import importlib.util
from pathlib import Path
import unittest

from src.retriever import InvalidSearchResult, buscar_contexto
from src.metadata_utils import enriquecer_metadados, construir_filtro

spec = importlib.util.spec_from_file_location("baseline_v1", Path(__file__).parents[1] / "v1-llm" / "test_busca_v1.py")
baseline = importlib.util.module_from_spec(spec)
spec.loader.exec_module(baseline)


class BuscaV2(baseline.BuscaV1):
    def test_contrato_pagina_invalida_na_origem(self):
        # CA-01.2: origem inválida deve ser rejeitada, nunca receber página inventada.
        for pagina in [0, -1, "1", 1.5, True, None]:
            with self.subTest(pagina=pagina):
                with self.assertRaises(InvalidSearchResult):
                    buscar_contexto("matrícula", collection=baseline.ColecaoFake(baseline.resultado(pagina=pagina)))

    def test_contrato_distancia_nao_finita_na_origem(self):
        # CA-01.2: não afirmar sucesso com evidência inválida.
        for distancia in [float("nan"), float("inf"), -float("inf")]:
            with self.subTest(distancia=distancia):
                with self.assertRaises(InvalidSearchResult):
                    buscar_contexto("matrícula", collection=baseline.ColecaoFake(baseline.resultado(distancia=distancia)))

    def test_http_origem_invalida(self):
        # CA-01.2: erro técnico seguro; não é erro do estudante.
        self.colecao.resposta = baseline.resultado(pagina=0)
        response = self.post()
        self.assertEqual(response.status_code, 502)
        self.assertEqual(response.json(), {"detail": "Resposta inválida do serviço de busca."})

    def test_rotulo_exato_interface(self):
        # CA-01.1, lacuna CT-01.03: alias exato aprovado pela equipe.
        response = self.post(curso="Sistemas de Informação", perfil="Perfil Novo / Vigente")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.colecao.chamadas[-1]["where"], {"$and": [{"curso_si": True}, {"perfil_novo": True}]})

    def test_enriquecimento_metadados(self):
        # CA-01.1/5: documentos gerais, mult curso e perfis em ambas as partições.
        for cursos in ([], "SI", ["CC", "EC"]):
            for perfil in ("novo", "anterior", "ambos"):
                with self.subTest(cursos=cursos, perfil=perfil):
                    meta = enriquecer_metadados({"curso_alvo": cursos, "perfil_curricular": perfil})
                    self.assertEqual(meta["perfil_novo"], perfil != "anterior")
                    self.assertEqual(meta["perfil_anterior"], perfil != "novo")
                    self.assertEqual(meta["curso_ia"], cursos == [])
                    self.assertEqual(meta["curso_si"], cursos in ([], "SI"))

    def test_aliases_gerais(self):
        # CA-01.5: partições sem restrições e normalização textual.
        for curso in ("", "Todos", "Geral"):
            for perfil in ("", "Ambos", "Todos"):
                self.assertIsNone(construir_filtro(curso, perfil))


if __name__ == "__main__":
    unittest.main()

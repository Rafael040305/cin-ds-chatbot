import unittest

from src.retriever import buscar_contexto


class CollectionFake:
    """
    Simula o ChromaDB sem abrir o banco real.
    """

    def __init__(self, resposta):
        self.resposta = resposta
        self.parametros = None

    def query(self, **kwargs):
        self.parametros = kwargs
        return self.resposta


class RetrieverTest(unittest.TestCase):
    def test_formata_resultado_e_aplica_filtro(
        self,
    ):
        collection = CollectionFake({
            "documents": [[
                "Trecho oficial do documento."
            ]],
            "metadatas": [[{
                "documento": "ppc_si.pdf",
                "pagina": 12,
                "curso_alvo": (
                    "Sistemas de Informação"
                ),
            }]],
            "distances": [[0.21]],
        })

        resultado = buscar_contexto(
            pergunta="Qual é a carga horária?",
            curso="Sistemas de Informação",
            perfil="Perfil Novo / Vigente",
            collection=collection,
        )

        self.assertEqual(
            collection.parametros["where"],
            {
                "$and": [
                    {"curso_si": True},
                    {"perfil_novo": True},
                ]
            },
        )

        self.assertIn(
            "Trecho oficial",
            resultado["contexto"],
        )

        self.assertEqual(
            resultado["fontes"][0]["pagina"],
            12,
        )

        self.assertEqual(
            resultado["distancia_minima"],
            0.21,
        )

    def test_busca_sem_resultados(
        self,
    ):
        collection = CollectionFake({
            "documents": [[]],
            "metadatas": [[]],
            "distances": [[]],
        })

        resultado = buscar_contexto(
            pergunta="Pergunta válida",
            collection=collection,
        )

        self.assertEqual(
            resultado,
            {
                "contexto": "",
                "fontes": [],
                "distancia_minima": 1.0,
            },
        )

        self.assertNotIn(
            "where",
            collection.parametros,
        )

    def test_rejeita_entrada_invalida(
        self,
    ):
        casos_invalidos = [
            ("", 3),
            ("Pergunta válida", 0),
        ]

        for pergunta, top_k in casos_invalidos:
            with self.subTest(
                pergunta=pergunta,
                top_k=top_k,
            ):
                with self.assertRaises(
                    ValueError
                ):
                    buscar_contexto(
                        pergunta=pergunta,
                        top_k=top_k,
                        collection=CollectionFake({}),
                    )


if __name__ == "__main__":
    unittest.main()
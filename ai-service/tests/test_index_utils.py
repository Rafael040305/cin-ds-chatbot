import unittest

from src.index_utils import (
    sincronizar_documento,
)


class CollectionFake:
    """
    Simula somente as operações do ChromaDB
    utilizadas pelo sincronizador.
    """

    def __init__(self):
        self.argumentos_upsert = None
        self.ids_excluidos = []

    def get(self, **kwargs):
        return {
            "ids": [
                "doc_p1_c0",
                "doc_p1_c1",
                "doc_p1_c2",
            ]
        }

    def upsert(self, **kwargs):
        self.argumentos_upsert = kwargs

    def delete(self, ids):
        self.ids_excluidos.extend(ids)


class IndexUtilsTest(unittest.TestCase):
    def test_remove_chunks_obsoletos(
        self,
    ):
        collection = CollectionFake()

        ids_removidos = sincronizar_documento(
            collection=collection,
            nome_arquivo="doc.pdf",
            ids=[
                "doc_p1_c0",
                "doc_p1_c1",
            ],
            documents=[
                "Primeiro trecho",
                "Segundo trecho",
            ],
            metadatas=[
                {"documento": "doc.pdf"},
                {"documento": "doc.pdf"},
            ],
        )

        self.assertEqual(
            ids_removidos,
            ["doc_p1_c2"],
        )

        self.assertEqual(
            collection.ids_excluidos,
            ["doc_p1_c2"],
        )

        self.assertEqual(
            collection.argumentos_upsert[
                "documents"
            ],
            [
                "Primeiro trecho",
                "Segundo trecho",
            ],
        )


if __name__ == "__main__":
    unittest.main()
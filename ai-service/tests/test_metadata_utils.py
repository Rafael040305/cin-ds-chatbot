import unittest

from src.metadata_utils import (
    construir_filtro,
    enriquecer_metadados,
)


class MetadataUtilsTest(unittest.TestCase):
    def test_enriquece_documento_de_varios_cursos(
        self,
    ):
        metadados = enriquecer_metadados({
            "curso_alvo": [
                "Ciência da Computação",
                "Sistemas de Informações",
            ],
            "perfil_curricular": "ambos",
        })

        self.assertTrue(
            metadados["curso_cc"]
        )

        self.assertTrue(
            metadados["curso_si"]
        )

        self.assertFalse(
            metadados["curso_ec"]
        )

        self.assertFalse(
            metadados["curso_ia"]
        )

        self.assertTrue(
            metadados["perfil_novo"]
        )

        self.assertTrue(
            metadados["perfil_anterior"]
        )

    def test_normaliza_rotulos_da_interface(
        self,
    ):
        filtro = construir_filtro(
            curso="Sistemas de Informação",
            perfil="Perfil Novo / Vigente",
        )

        self.assertEqual(
            filtro,
            {
                "$and": [
                    {"curso_si": True},
                    {"perfil_novo": True},
                ]
            },
        )

    def test_consulta_geral_nao_cria_filtro(
        self,
    ):
        filtro = construir_filtro(
            curso="Geral",
            perfil="Todos",
        )

        self.assertIsNone(filtro)

    def test_rejeita_curso_desconhecido(
        self,
    ):
        with self.assertRaises(ValueError):
            construir_filtro(
                curso="Curso inexistente",
                perfil="Todos",
            )


if __name__ == "__main__":
    unittest.main()
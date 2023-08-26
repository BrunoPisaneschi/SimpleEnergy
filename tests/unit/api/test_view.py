import unittest
from unittest.mock import patch
from fastapi.testclient import TestClient
from api.view import api_router
from crawler.capturar_dados import CapturarDados

class TestConsultaCodigo(unittest.TestCase):
    """
    Testes unitários para a função de consulta de código da API.
    """

    def setUp(self):
        """
        Configuração inicial para cada teste.
        """
        self.client = TestClient(api_router)

    @patch.object(CapturarDados, 'capturar_dados_existentes', return_value=[{"dummy_data": "example"}])
    def test_consulta_codigo(self, mock_capturar_dados):
        """
        Testa a consulta de código válido.

        Este teste simula a consulta de um código que existe no sistema.
        Ele utiliza um mock para a função capturar_dados_existentes da classe CapturarDados.

        :param mock_capturar_dados: Mock da função capturar_dados_existentes.
        """
        response = self.client.post("/consultar-codigo", json={"codigo": 123})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"123": [{"dummy_data": "example"}]})

    @patch.object(CapturarDados, 'capturar_dados_existentes', return_value=None)
    def test_consulta_codigo_inexistente(self, mock_capturar_dados):
        """
        Testa a consulta de código inexistente.

        Este teste simula a consulta de um código que não existe no sistema.
        Ele utiliza um mock para a função capturar_dados_existentes da classe CapturarDados.

        :param mock_capturar_dados: Mock da função capturar_dados_existentes.
        """
        response = self.client.post("/consultar-codigo", json={"codigo": 123})

        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json(), {"error": "Código não encontrado"})

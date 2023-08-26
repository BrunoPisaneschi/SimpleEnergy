import unittest
from unittest.mock import Mock, patch

from decouple import config

from crawler.capturar_dados import CapturarDados


class TestCapturarDados(unittest.TestCase):
    """
    Testes unitários para a classe CapturarDados.
    """

    @patch('crawler.capturar_dados.get')
    def test_capturar_token(self, mock_get):
        """
        Testa o método _capturar_token da classe CapturarDados.

        Este teste verifica se o método _capturar_token é capaz de fazer uma chamada GET mockada
        à API usando o decorator @patch, e se o token é armazenado corretamente.

        O método config é mockado para retornar a configuração BASE_URL.

        :param mock_get: Mock da função get do módulo requests.
        """
        capturar_dados = CapturarDados()

        mock_response = Mock()
        mock_response.text = 'dummy_content'
        mock_get.return_value = mock_response

        capturar_dados.config = Mock()
        capturar_dados.config.return_value = config('BASE_URL')

        capturar_dados._capturar_token()

        mock_get.assert_called_once_with(url=config('BASE_URL'), headers=capturar_dados._headers)

        self.assertEqual(capturar_dados._token, None)

    @patch('crawler.capturar_dados.post')
    def test_consultar_codigo(self, mock_post):
        """
        Testa o método _consultar_codigo da classe CapturarDados.

        Este teste verifica se o método _consultar_codigo é capaz de fazer uma chamada POST mockada
        à API usando o decorator @patch, e se o resultado é processado corretamente.

        :param mock_post: Mock da função post do módulo requests.
        """
        capturar_dados = CapturarDados()
        capturar_dados._token = 'dummy_token'

        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.text = 'dummy_content'
        mock_post.return_value = mock_response

        result = capturar_dados._consultar_codigo(codigo=123)

        mock_post.assert_called_once_with(
            url=config('BASE_URL'),
            headers=capturar_dados._headers,
            data={"csrf": 'dummy_token', "codigo": 123}
        )
        self.assertEqual(result, 'dummy_content')

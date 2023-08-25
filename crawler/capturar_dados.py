from base64 import b64encode
from os import remove, makedirs
from os.path import join, exists
from re import search

from decouple import config
from requests import get, post
from bs4 import BeautifulSoup


class CapturarDados:
    """
    Classe responsável por capturar e processar dados do site do desafio, incluindo o download de anexos
    e conversão para Base64.
    """

    def __init__(self):
        """
        Inicializa a classe com o token e cabeçalhos padrão para as requisições.
        """
        self._token = None
        self._headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                          "Chrome/114.0.0.0 Safari/537.36 OPR/100.0.0.0"
        }

    def _capturar_token(self):
        """
        Captura o token CSRF do site e armazena internamente na classe.
        """
        response = get(url=config('BASE_URL'), headers=self._headers)
        conteudo_html = response.text
        try:
            self._token = search(pattern=r'(?<=csrf\"\svalue=\")(.*?)(?=")', string=conteudo_html).group()
        except AttributeError:
            print("Não conseguiu capturar o token do site!")
            self._token = None

    def _consultar_codigo(self, codigo: int):
        """
        Consulta um código específico no site e retorna o conteúdo da página.
        """
        payload = {
            "csrf": self._token,
            "codigo": codigo,
        }
        response = post(url=config('BASE_URL'), headers=self._headers, data=payload)
        if response.status_code == 200:
            return response.text
        else:
            print(f"Código {codigo} inexistente!")
            return None

    def _parser_dados(self, codigo: int, html_page: str):
        """
        Processa o conteúdo HTML da página, captura informações sobre arquivos e anexos.
        """
        dados_parseados = []
        soup = BeautifulSoup(markup=html_page, features='html.parser', parse_only=None)

        # Encontrar todas as divs que contêm informações sobre arquivos
        body = soup.find('body')
        divs = body.find_all('div', recursive=False)

        for div in divs[1:]:
            if 'arquivo' in div.get_text().lower():
                nome_particao_arquivo = div.find_next('div').get_text(strip=True)
                conteudo_arquivos = [
                    {
                        "nome_arquivo": tag_a.get_text(),
                        "href": tag_a['href'],
                        "base64": self._capturar_anexo(url_anexo=tag_a['href'])
                    }
                    for tag_a in div.find_all('a')
                ]

                dados_parseados.append({
                    "nome_particao_arquivo": nome_particao_arquivo,
                    "anexos": conteudo_arquivos,
                    "codigo_consultado": codigo,
                })
        return dados_parseados

    def _capturar_anexo(self, url_anexo: str):
        """
        Captura o conteúdo de um anexo e converte para Base64.
        """
        response = get(url=f"{config('BASE_URL')}{url_anexo}", headers=self._headers)
        return self._gerar_base64_anexo(nome=url_anexo, conteudo=response.content)

    @staticmethod
    def _gerar_base64_anexo(nome: str, conteudo: bytes):
        """
        Gera o conteúdo Base64 a partir de um arquivo.
        """
        try:
            nome_diretorio_temporario = 'tmp_files'

            if not exists(nome_diretorio_temporario):
                makedirs(nome_diretorio_temporario)

            caminho_completo_arquivo = join(nome_diretorio_temporario, nome)

            with open(caminho_completo_arquivo, 'wb') as file:
                file.write(conteudo)

            # Leitura do conteúdo do arquivo temporário
            with open(caminho_completo_arquivo, 'rb') as file:
                file_content = file.read()

            # Conversão para base64
            base64_content = b64encode(file_content).decode('utf-8')

            return base64_content

        except Exception as e:
            print(f"Erro ao gerar base64 do arquivo {nome} | Erro: {e}")
            return None

        finally:
            try:
                remove(caminho_completo_arquivo)
            except Exception as e:
                print(f"Erro ao remover arquivo temporário {caminho_completo_arquivo}: | Erro: {e}")

    def capturar_dados_existentes(self, codigo: int):
        """
        Captura os dados existentes para um código específico.
        """
        if not self._token:
            self._capturar_token()
        conteudo_codigo = self._consultar_codigo(codigo=codigo)
        if conteudo_codigo:
            dados_parseados = self._parser_dados(codigo=codigo, html_page=conteudo_codigo)
            return dados_parseados

        return None

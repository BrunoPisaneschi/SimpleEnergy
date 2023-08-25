from concurrent.futures import ThreadPoolExecutor, wait, ALL_COMPLETED

from crawler.capturar_dados import CapturarDados


def execucao_modelo():
    # Exemplo de uso
    dados_parseados = {}
    lista_codigos_consulta = [1203, 98465, 321465]  # um código inexistente e outros 2 informados para realizar no teste
    capturar_dados = CapturarDados()
    with ThreadPoolExecutor(2) as executor:
        futures = [
            executor.submit(capturar_dados.capturar_dados_existentes, codigo)
            for codigo in lista_codigos_consulta
        ]
        wait(futures, timeout=None, return_when=ALL_COMPLETED)

    for resultado in futures:
        dados = resultado.result()
        if dados:
            codigo_capturado = dados[0].get('codigo_consultado')
            dados_parseados[codigo_capturado] = dados


if __name__ == '__main__':
    execucao_modelo()

# SimpleEnergy

Desafio técnico solicitado pela empresa SimpleEnergy.
O desafio consiste em acessar uma url, consultar códigos de arquivos e, caso existam, capturar todas as informações
disponíveis e retornar elas.

## Crawler

Sobre o crawler, foi utilizado a biblioteca `requests` e gerado um arquivo `exemplo.py` no qual executa exatamente o
que foi pedido para o teste.

Porém a classe `CapturarDados` foi criada para suportar qualquer código enviado, com isso dei sequência no projeto
implementando-a em uma API com FastApi.

O crawler está capturando o nome da seção de arquivos, o nome de cada arquivo, suas respectivas urls e fazendo o
download do arquivo, gerando um base64 do mesmo.

Todos esses dados mencionados, são retornados no json final.

Durante a criação do base64, é utilizado uma pasta temporária chamada `tmp_files`, onde todos os arquivos são criados,
convertidos e apagados dela.

## API

A API tem 2 rotas, sendo elas:

- consultar-codigo
- executar-modelo

### consultar-codigo

Uma rota do tipo post, que recebe 1 código desejado, será realizado toda a consulta e captura das informações e
retornado em formato de json.

Caso o código não exista, será retornado um status 404.

### executar-modelo

Essa rota, apenas executa o projeto `exemplo.py` e retorna o resultado do json na requisição.

O mesmo arquivo também pode ser executado manualmente, caso deseje.

### Executando a API

Para executar a API, já foi configurado no `invoke` o comando abaixo:
```shell
inv docker-start
```

Ele se encarregará de subir todo o projeto no docker e deixar a API disponível para uso.

A rota principal da api é o root, podendo ser acessada [clicando aqui](http://localhost:8000/).

## Tests
Foram criados testes unitários e de integração, para manter a maior consistência da API.
Para executá-los, faça a configuração da sua virtualenv e instale as dependências do projeto.

Assim que isso for realizado, execute o seguinte comando:
```shell
inv all-tests
```

Ele irá subir o projeto no docker, executar todos os testes unitários e os de integração,

O resultado da execução dos testes, pode ser confirmado no console do pycharm ou terminal.


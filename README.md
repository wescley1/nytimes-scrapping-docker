# NYTimes Scrapping Docker

Este projeto utiliza Docker para executar um script Python que extrai informações do site do NYTimes.

## Pré-requisitos

* Docker instalado na máquina.
* Conta no GitHub.

## Como executar

1.  **Clone o repositório:**

    ```bash
    git clone [https://github.com/wescley1/nytimes-scrapping-docker.git](https://www.google.com/search?q=https://github.com/wescley1/nytimes-scrapping-docker.git)
    cd nytimes-scrapping-docker
    ```

2.  **Crie o arquivo `.env`:**

    * Crie um arquivo `.env` na raiz do projeto com as variáveis de ambiente necessárias. Exemplo:

        ```
        SEARCH_PHRASE="musk"
        CATEGORIES="Business"
        MONTHS=10
        SORTING=newest
        ```

    * Você pode personalizar essas variáveis de acordo com suas necessidades.

3.  **Execute o script `run.sh`:**

    ```bash
    chmod +x run.sh
    ./run.sh
    ```

4.  **Personalizar as variáveis de ambiente (opcional):**

    * Você pode personalizar as variáveis de ambiente diretamente na linha de comando ao executar o script `run.sh`. Exemplo:

        ```bash
        SEARCH_PHRASE="outra frase" CATEGORIES="outra categoria" MONTHS=12 SORTING="oldest" ./run.sh
        ```

5.  **Acessar os resultados:**

    * Os resultados (pasta `imagens` e arquivo `news_results.xlsx`) serão salvos na pasta `resultados/output` no diretório raiz do projeto.

## Como funciona

O script `run.sh` executa um container Docker que:

* Lê as variáveis de ambiente do arquivo `.env` ou da linha de comando.
* Executa o script Python `projeto/app.py`.
* Salva os resultados na pasta `resultados/output`.

## Imagem Docker

A imagem Docker utilizada neste projeto está hospedada no GitHub Container Registry (GHCR):